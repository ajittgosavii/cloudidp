"""
AWS Cost Explorer Helper - Real Cost Analysis
Fetch actual cost data from AWS Cost Explorer
"""

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pandas as pd

class AWSCostExplorerHelper:
    """Helper class to interact with AWS Cost Explorer"""
    
    def __init__(self):
        self.session = None
        self.ce_client = None
        self.initialized = False
        
    def initialize(self) -> bool:
        """Initialize AWS Cost Explorer client"""
        try:
            # Try to get AWS credentials from Streamlit secrets
            if hasattr(st, 'secrets') and 'aws' in st.secrets:
                aws_config = st.secrets['aws']
                self.session = boto3.Session(
                    aws_access_key_id=aws_config.get('access_key_id'),
                    aws_secret_access_key=aws_config.get('secret_access_key'),
                    region_name=aws_config.get('region', 'us-east-1')
                )
            else:
                # Fall back to default credentials
                self.session = boto3.Session()
            
            self.ce_client = self.session.client('ce', region_name='us-east-1')  # Cost Explorer is always us-east-1
            self.initialized = True
            return True
            
        except (NoCredentialsError, Exception) as e:
            st.warning(f"⚠️ Could not initialize AWS Cost Explorer: {str(e)}")
            return False
    
    def get_month_to_date_cost(self) -> Optional[Dict]:
        """Get month-to-date cost"""
        try:
            if not self.initialized:
                if not self.initialize():
                    return None
            
            # Get first day of current month
            today = datetime.now()
            start_date = today.replace(day=1).strftime('%Y-%m-%d')
            end_date = today.strftime('%Y-%m-%d')
            
            response = self.ce_client.get_cost_and_usage(
                TimePeriod={
                    'Start': start_date,
                    'End': end_date
                },
                Granularity='MONTHLY',
                Metrics=['UnblendedCost']
            )
            
            if response.get('ResultsByTime'):
                amount = float(response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount'])
                return {
                    'amount': amount,
                    'currency': response['ResultsByTime'][0]['Total']['UnblendedCost']['Unit'],
                    'start_date': start_date,
                    'end_date': end_date
                }
            
            return None
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'AccessDeniedException':
                st.warning("⚠️ No access to AWS Cost Explorer. Enable Cost Explorer in your AWS account or add the following IAM permission: `ce:GetCostAndUsage`")
            else:
                st.error(f"Error getting cost data: {e.response['Error']['Message']}")
            return None
        except Exception as e:
            st.error(f"Error getting cost data: {str(e)}")
            return None
    
    def get_last_month_cost(self) -> Optional[Dict]:
        """Get last month's total cost"""
        try:
            if not self.initialized:
                if not self.initialize():
                    return None
            
            # Get first and last day of last month
            today = datetime.now()
            first_day_this_month = today.replace(day=1)
            last_day_last_month = first_day_this_month - timedelta(days=1)
            first_day_last_month = last_day_last_month.replace(day=1)
            
            start_date = first_day_last_month.strftime('%Y-%m-%d')
            end_date = first_day_this_month.strftime('%Y-%m-%d')
            
            response = self.ce_client.get_cost_and_usage(
                TimePeriod={
                    'Start': start_date,
                    'End': end_date
                },
                Granularity='MONTHLY',
                Metrics=['UnblendedCost']
            )
            
            if response.get('ResultsByTime'):
                amount = float(response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount'])
                return {
                    'amount': amount,
                    'currency': response['ResultsByTime'][0]['Total']['UnblendedCost']['Unit'],
                    'start_date': start_date,
                    'end_date': end_date
                }
            
            return None
            
        except Exception as e:
            st.error(f"Error getting last month cost: {str(e)}")
            return None
    
    def get_cost_by_service(self, days: int = 30) -> Optional[List[Dict]]:
        """Get cost breakdown by service for the last N days"""
        try:
            if not self.initialized:
                if not self.initialize():
                    return None
            
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            response = self.ce_client.get_cost_and_usage(
                TimePeriod={
                    'Start': start_date.strftime('%Y-%m-%d'),
                    'End': end_date.strftime('%Y-%m-%d')
                },
                Granularity='MONTHLY',
                Metrics=['UnblendedCost'],
                GroupBy=[
                    {
                        'Type': 'DIMENSION',
                        'Key': 'SERVICE'
                    }
                ]
            )
            
            services = []
            if response.get('ResultsByTime'):
                for group in response['ResultsByTime'][0]['Groups']:
                    service_name = group['Keys'][0]
                    amount = float(group['Metrics']['UnblendedCost']['Amount'])
                    if amount > 0:  # Only include services with cost
                        services.append({
                            'service': service_name,
                            'cost': amount
                        })
            
            # Sort by cost descending
            services.sort(key=lambda x: x['cost'], reverse=True)
            return services
            
        except Exception as e:
            st.error(f"Error getting cost by service: {str(e)}")
            return None
    
    def get_daily_cost_trend(self, days: int = 30) -> Optional[List[Dict]]:
        """Get daily cost trend for the last N days"""
        try:
            if not self.initialized:
                if not self.initialize():
                    return None
            
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            response = self.ce_client.get_cost_and_usage(
                TimePeriod={
                    'Start': start_date.strftime('%Y-%m-%d'),
                    'End': end_date.strftime('%Y-%m-%d')
                },
                Granularity='DAILY',
                Metrics=['UnblendedCost']
            )
            
            daily_costs = []
            if response.get('ResultsByTime'):
                for result in response['ResultsByTime']:
                    daily_costs.append({
                        'date': result['TimePeriod']['Start'],
                        'cost': float(result['Total']['UnblendedCost']['Amount'])
                    })
            
            return daily_costs
            
        except Exception as e:
            st.error(f"Error getting daily cost trend: {str(e)}")
            return None
    
    def get_forecast(self, days_ahead: int = 30) -> Optional[Dict]:
        """Get cost forecast for the next N days"""
        try:
            if not self.initialized:
                if not self.initialize():
                    return None
            
            start_date = datetime.now()
            end_date = start_date + timedelta(days=days_ahead)
            
            response = self.ce_client.get_cost_forecast(
                TimePeriod={
                    'Start': start_date.strftime('%Y-%m-%d'),
                    'End': end_date.strftime('%Y-%m-%d')
                },
                Metric='UNBLENDED_COST',
                Granularity='MONTHLY'
            )
            
            if response.get('Total'):
                amount = float(response['Total']['Amount'])
                return {
                    'amount': amount,
                    'currency': response['Total']['Unit'],
                    'start_date': start_date.strftime('%Y-%m-%d'),
                    'end_date': end_date.strftime('%Y-%m-%d')
                }
            
            return None
            
        except ClientError as e:
            # Forecast might not be available for new accounts
            st.info("ℹ️ Cost forecast not available (requires at least 30 days of cost data)")
            return None
        except Exception as e:
            st.warning(f"Could not get forecast: {str(e)}")
            return None

# Global instance
_cost_explorer_helper = None

def get_cost_explorer_helper() -> AWSCostExplorerHelper:
    """Get or create Cost Explorer helper singleton"""
    global _cost_explorer_helper
    if _cost_explorer_helper is None:
        _cost_explorer_helper = AWSCostExplorerHelper()
    return _cost_explorer_helper

def show_cost_analysis_modal(account_name: str, account_id: str):
    """
    Show comprehensive cost analysis in a modal
    """
    st.subheader(f"💰 Cost Analysis: {account_name}")
    st.caption(f"Account ID: {account_id}")
    
    helper = get_cost_explorer_helper()
    
    # Check if Cost Explorer is accessible
    with st.spinner("Fetching cost data from AWS Cost Explorer..."):
        mtd_cost = helper.get_month_to_date_cost()
    
    if mtd_cost is None:
        st.error("❌ Unable to access AWS Cost Explorer")
        st.info("""
        **To enable cost analysis:**
        
        1. **Enable AWS Cost Explorer** in your AWS account:
           - Go to AWS Console → Billing → Cost Explorer
           - Click "Enable Cost Explorer"
           - Wait 24 hours for data to populate
        
        2. **Add IAM permissions** to your CloudIDP user/role:
           ```json
           {
             "Effect": "Allow",
             "Action": [
               "ce:GetCostAndUsage",
               "ce:GetCostForecast"
             ],
             "Resource": "*"
           }
           ```
        
        3. **Refresh this page** after enabling
        """)
        return
    
    # Month-to-date cost
    st.markdown("### 📊 Current Month")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Month-to-Date Cost",
            f"${mtd_cost['amount']:.2f}",
            help=f"From {mtd_cost['start_date']} to {mtd_cost['end_date']}"
        )
    
    with col2:
        last_month = helper.get_last_month_cost()
        if last_month:
            change = mtd_cost['amount'] - last_month['amount']
            change_pct = (change / last_month['amount'] * 100) if last_month['amount'] > 0 else 0
            st.metric(
                "Last Month Total",
                f"${last_month['amount']:.2f}",
                f"{change_pct:+.1f}%",
                help="Comparison to current month-to-date"
            )
        else:
            st.metric("Last Month Total", "N/A")
    
    with col3:
        forecast = helper.get_forecast(30)
        if forecast:
            st.metric(
                "30-Day Forecast",
                f"${forecast['amount']:.2f}",
                help=f"Forecasted cost for next 30 days"
            )
        else:
            st.metric("30-Day Forecast", "N/A", help="Requires 30+ days of cost data")
    
    st.markdown("---")
    
    # Cost by service
    st.markdown("### 🔧 Cost by Service (Last 30 Days)")
    services = helper.get_cost_by_service(30)
    
    if services:
        # Show top services
        top_services = services[:10]  # Top 10
        
        service_df = pd.DataFrame(top_services)
        service_df['cost'] = service_df['cost'].apply(lambda x: f"${x:.2f}")
        service_df.columns = ['Service', 'Cost (Last 30 Days)']
        
        st.dataframe(service_df, use_container_width=True, hide_index=True)
        
        # Chart
        if len(services) > 0:
            chart_data = pd.DataFrame(top_services)
            st.bar_chart(chart_data.set_index('service')['cost'])
    else:
        st.info("No cost data available for services")
    
    st.markdown("---")
    
    # Daily cost trend
    st.markdown("### 📈 Daily Cost Trend (Last 30 Days)")
    daily_costs = helper.get_daily_cost_trend(30)
    
    if daily_costs:
        trend_df = pd.DataFrame(daily_costs)
        trend_df['date'] = pd.to_datetime(trend_df['date'])
        trend_df = trend_df.set_index('date')
        
        st.line_chart(trend_df['cost'])
        
        # Show summary stats
        col1, col2, col3 = st.columns(3)
        with col1:
            avg_daily = trend_df['cost'].mean()
            st.metric("Average Daily Cost", f"${avg_daily:.2f}")
        with col2:
            max_daily = trend_df['cost'].max()
            st.metric("Highest Daily Cost", f"${max_daily:.2f}")
        with col3:
            min_daily = trend_df['cost'].min()
            st.metric("Lowest Daily Cost", f"${min_daily:.2f}")
    else:
        st.info("No daily cost trend data available")
