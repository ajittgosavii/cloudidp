"""
CloudIDP - AWS Cost Explorer Integration Module
Real-time cost data and optimizatiosn recommendations
"""

import streamlit as st
import boto3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from botocore.exceptions import ClientError


class CostExplorerIntegration:
    """AWS Cost Explorer integration for CloudIDP"""
    
    def __init__(self, demo_mode: bool = True, region: str = 'us-east-1'):
        self.demo_mode = demo_mode
        self.region = region
        
        if not demo_mode:
            try:
                # Try to read from Streamlit secrets first
                if hasattr(st, 'secrets') and 'aws' in st.secrets:
                    self.ce_client = boto3.client(
                        'ce',
                        aws_access_key_id=st.secrets["aws"]["access_key"],
                        aws_secret_access_key=st.secrets["aws"]["secret_access_key"],
                        region_name=st.secrets["aws"].get("region", region)
                    )
                else:
                    # Fallback to default credentials (IAM role, env vars, etc.)
                    self.ce_client = boto3.client('ce', region_name=region)
            except Exception as e:
                print(f"Warning: {e}")
                self.demo_mode = True
    
    def get_cost_and_usage(self, start_date: str, end_date: str,
                           granularity: str = 'DAILY',
                           metrics: List[str] = None) -> Dict[str, Any]:
        """Get cost and usage data"""
        if self.demo_mode:
            return {
                'success': True,
                'total_cost': 12543.78,
                'currency': 'USD',
                'period': f'{start_date} to {end_date}',
                'breakdown': [
                    {'service': 'EC2', 'cost': 5234.56},
                    {'service': 'RDS', 'cost': 3456.78},
                    {'service': 'S3', 'cost': 1234.90},
                    {'service': 'Other', 'cost': 2617.54}
                ],
                'demo_mode': True
            }
        
        try:
            response = self.ce_client.get_cost_and_usage(
                TimePeriod={'Start': start_date, 'End': end_date},
                Granularity=granularity,
                Metrics=metrics or ['UnblendedCost'],
                GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
            )
            return {'success': True, 'data': response['ResultsByTime']}
        except ClientError as e:
            return {'success': False, 'error': str(e)}
    
    def get_cost_forecast(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """Get cost forecast"""
        if self.demo_mode:
            return {
                'success': True,
                'forecasted_cost': 15678.90,
                'currency': 'USD',
                'confidence': 0.85,
                'period': f'{start_date} to {end_date}',
                'demo_mode': True
            }
        
        try:
            response = self.ce_client.get_cost_forecast(
                TimePeriod={'Start': start_date, 'End': end_date},
                Metric='UNBLENDED_COST',
                Granularity='MONTHLY'
            )
            return {
                'success': True,
                'forecast': response['Total']['Amount'],
                'unit': response['Total']['Unit']
            }
        except ClientError as e:
            return {'success': False, 'error': str(e)}
    
    def get_rightsizing_recommendations(self) -> Dict[str, Any]:
        """Get EC2 rightsizing recommendations"""
        if self.demo_mode:
            return {
                'success': True,
                'recommendations': [
                    {
                        'instance_id': 'i-1234567890abcdef0',
                        'current_type': 't3.large',
                        'recommended_type': 't3.medium',
                        'estimated_monthly_savings': 45.67
                    },
                    {
                        'instance_id': 'i-0fedcba0987654321',
                        'current_type': 'm5.xlarge',
                        'recommended_type': 'm5.large',
                        'estimated_monthly_savings': 87.23
                    }
                ],
                'total_savings': 132.90,
                'demo_mode': True
            }
        
        try:
            response = self.ce_client.get_rightsizing_recommendation(
                Service='AmazonEC2'
            )
            return {
                'success': True,
                'recommendations': response.get('RightsizingRecommendations', [])
            }
        except ClientError as e:
            return {'success': False, 'error': str(e)}


if __name__ == "__main__":
    print("Cost Explorer Integration Demo")
    ce = CostExplorerIntegration(demo_mode=True)
    today = datetime.now().strftime('%Y-%m-%d')
    last_month = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    costs = ce.get_cost_and_usage(last_month, today)
    print(f"Total cost: ${costs['total_cost']:.2f}")
    print("✅ Demo completed!")
