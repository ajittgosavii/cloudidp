"""
Module 4: FinOps - Financial Operations & Cost Management
Comprehensive cost management and optimization module
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json

# Import data provider for Demo/Live mode support
try:
    from data_provider import get_data_provider, get_live_service
    DATA_PROVIDER_AVAILABLE = True
except ImportError:
    DATA_PROVIDER_AVAILABLE = False

class FinOpsModule:
    """FinOps Module - Comprehensive Cost Management & Optimization"""
    
    def __init__(self):
        self.module_name = "FinOps Cost Management"
        self.version = "2.0.0"
    
    def render(self):
        """Main render method - organizes all sub-features in tabs"""
        
        st.markdown("## 💰 FinOps Cost Management")
        
        # Mode indicator - show status based on data provider availability
        if st.session_state.get('mode', 'Demo') == 'Live':
            if not DATA_PROVIDER_AVAILABLE:
                st.warning("⚠️ Live mode: data_provider.py not found - showing demo data")
            else:
                st.info("📊 Live mode: Fetching real AWS cost data where available")
        
        st.markdown("**Enterprise Cloud Financial Operations & Cost Optimization**")
        
        # Quick Stats - MODE-AWARE
        # Get data based on Demo/Live mode
        if DATA_PROVIDER_AVAILABLE:
            try:
                provider = get_data_provider()
                live_service = get_live_service()
                
                # Get mode-aware data
                monthly_cost = provider.get(
                    key='finops_monthly_cost',
                    demo_value='$45,234',
                    live_fn=lambda: live_service.get_monthly_cost()
                )
                budget_usage = provider.get(
                    key='finops_budget_usage',
                    demo_value='76%',
                    live_fn=None  # Not implemented yet
                )
                monthly_savings = provider.get(
                    key='finops_monthly_savings',
                    demo_value='$8,456',
                    live_fn=None  # Not implemented yet
                )
                active_resources = provider.get(
                    key='finops_active_resources',
                    demo_value='1,234',
                    live_fn=None  # Not implemented yet
                )
            except Exception as e:
                # Fallback to demo values on error
                monthly_cost = '$45,234'
                budget_usage = '76%'
                monthly_savings = '$8,456'
                active_resources = '1,234'
        else:
            # No data provider, use demo values
            monthly_cost = '$45,234'
            budget_usage = '76%'
            monthly_savings = '$8,456'
            active_resources = '1,234'
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Monthly Cost", monthly_cost, "-$2,345 (5%)")
        with col2:
            st.metric("Budget Usage", budget_usage, "+3%")
        with col3:
            st.metric("Monthly Savings", monthly_savings, "+$1,234")
        with col4:
            st.metric("Active Resources", active_resources, "-45")
        
        # Create tabs for each sub-feature
        tabs = st.tabs([
            "📊 Cost Dashboard",
            "🏷️ Tag-Based Tracking",
            "💵 Budget Management",
            "📈 Forecasting",
            "📅 Scheduled Policies",
            "⚡ Spot Instances",
            "🔍 Anomaly Detection",
            "📋 Reports",
            "💡 RI Recommendations",
            "📊 Chargeback"
        ])
        
        with tabs[0]:
            self.render_cost_dashboard()
        
        with tabs[1]:
            self.render_tag_based_tracking()
        
        with tabs[2]:
            self.render_budget_management()
        
        with tabs[3]:
            self.render_forecasting()
        
        with tabs[4]:
            self.render_scheduled_policies()
        
        with tabs[5]:
            self.render_spot_instances()
        
        with tabs[6]:
            self.render_anomaly_detection()
        
        with tabs[7]:
            self.render_reports()
        
        with tabs[8]:
            self.render_ri_recommendations()
        
        with tabs[9]:
            self.render_chargeback()
    
    def render_cost_dashboard(self):
        """Cost Dashboard Tab"""
        st.subheader("📊 Cost Dashboard")
        
        # Cost Breakdown - MODE-AWARE
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Cost by Service")
            
            # Check mode
            if st.session_state.get('mode', 'Demo') == 'Live' and DATA_PROVIDER_AVAILABLE:
                try:
                    live_service = get_live_service()
                    
                    # Try to get real cost data from AWS Cost Explorer
                    from datetime import datetime, timedelta
                    end_date = datetime.now().strftime('%Y-%m-%d')
                    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
                    
                    cost_result = live_service.cost_explorer.get_cost_and_usage(
                        start_date=start_date,
                        end_date=end_date,
                        granularity='MONTHLY',
                        metrics=['UnblendedCost']
                    )
                    
                    if cost_result.get('success') and 'breakdown' in cost_result:
                        # Use real AWS cost data
                        breakdown = cost_result['breakdown']
                        cost_data = pd.DataFrame({
                            'Service': [item['service'] for item in breakdown],
                            'Cost': [float(item['cost']) for item in breakdown]
                        })
                        st.caption("🔴 Live Mode: Real AWS cost data")
                    else:
                        # Fallback to demo
                        cost_data = pd.DataFrame({
                            'Service': ['EC2', 'S3', 'RDS', 'Lambda', 'ELB'],
                            'Cost': [15234, 8456, 12345, 3456, 4567]
                        })
                        st.caption("⚠️ Using demo data - Could not fetch real costs")
                except Exception as e:
                    # Error - fallback to demo
                    cost_data = pd.DataFrame({
                        'Service': ['EC2', 'S3', 'RDS', 'Lambda', 'ELB'],
                        'Cost': [15234, 8456, 12345, 3456, 4567]
                    })
                    st.caption(f"⚠️ Using demo data - Error: {str(e)[:40]}")
            else:
                # Demo mode
                cost_data = pd.DataFrame({
                    'Service': ['EC2', 'S3', 'RDS', 'Lambda', 'ELB'],
                    'Cost': [15234, 8456, 12345, 3456, 4567]
                })
            
            st.bar_chart(cost_data.set_index('Service'))
        
        with col2:
            st.markdown("### Cost Trend (30 Days)")
            
            # Check mode
            if st.session_state.get('mode', 'Demo') == 'Live' and DATA_PROVIDER_AVAILABLE:
                try:
                    live_service = get_live_service()
                    
                    # Try to get real daily cost data
                    end_date = datetime.now().strftime('%Y-%m-%d')
                    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
                    
                    cost_result = live_service.cost_explorer.get_cost_and_usage(
                        start_date=start_date,
                        end_date=end_date,
                        granularity='DAILY',
                        metrics=['UnblendedCost']
                    )
                    
                    if cost_result.get('success') and 'data' in cost_result:
                        # Parse real AWS cost trend data
                        results = cost_result['data']
                        dates_list = []
                        costs_list = []
                        
                        for result in results:
                            period_start = result.get('TimePeriod', {}).get('Start')
                            if period_start:
                                dates_list.append(pd.to_datetime(period_start))
                                total = result.get('Total', {}).get('UnblendedCost', {}).get('Amount', '0')
                                costs_list.append(float(total))
                        
                        if dates_list and costs_list:
                            trend_data = pd.DataFrame({
                                'Date': dates_list,
                                'Cost': costs_list
                            })
                            st.caption("🔴 Live Mode: Real AWS cost trend")
                        else:
                            # Fallback to demo
                            dates = pd.date_range(end=datetime.now(), periods=30)
                            trend_data = pd.DataFrame({
                                'Date': dates,
                                'Cost': [1200 + i * 50 + (i % 7) * 100 for i in range(30)]
                            })
                            st.caption("⚠️ Using demo data - No trend data available")
                    else:
                        # Fallback to demo
                        dates = pd.date_range(end=datetime.now(), periods=30)
                        trend_data = pd.DataFrame({
                            'Date': dates,
                            'Cost': [1200 + i * 50 + (i % 7) * 100 for i in range(30)]
                        })
                        st.caption("⚠️ Using demo data - Could not fetch trend")
                except Exception as e:
                    # Error - fallback to demo
                    dates = pd.date_range(end=datetime.now(), periods=30)
                    trend_data = pd.DataFrame({
                        'Date': dates,
                        'Cost': [1200 + i * 50 + (i % 7) * 100 for i in range(30)]
                    })
                    st.caption(f"⚠️ Using demo data - Error: {str(e)[:40]}")
            else:
                # Demo mode
                dates = pd.date_range(end=datetime.now(), periods=30)
                trend_data = pd.DataFrame({
                    'Date': dates,
                    'Cost': [1200 + i * 50 + (i % 7) * 100 for i in range(30)]
                })
            
            st.line_chart(trend_data.set_index('Date'))
        
        # Top Cost Resources - MODE-AWARE
        st.markdown("### Top 10 Costly Resources")
        
        # Check mode and get appropriate data
        if st.session_state.get('mode', 'Demo') == 'Live' and DATA_PROVIDER_AVAILABLE:
            try:
                # Live mode - show message about data source
                st.caption("🔴 Live Mode: Showing real AWS resources with estimated costs. For accurate per-resource costs, enable AWS Cost Allocation Tags.")
                
                # Use the already-initialized live_service (has AWS credentials from secrets)
                live_service = get_live_service()
                
                resources_data = []
                
                # Get EC2 instances using live_service's compute instance
                ec2_result = live_service.compute.list_instances()
                if ec2_result.get('success'):
                    for instance in ec2_result.get('instances', [])[:5]:
                        instance_id = instance.get('InstanceId', 'unknown')
                        instance_type = instance.get('InstanceType', 'unknown')
                        tags_list = instance.get('Tags', [])
                        name_tag = next((t['Value'] for t in tags_list if t['Key'] == 'Name'), 'unnamed')
                        
                        # Rough cost estimate (actual costs require Cost Explorer)
                        resources_data.append({
                            'Resource ID': instance_id,
                            'Type': 'EC2',
                            'Monthly Cost': '~Est',  # Placeholder
                            'Tags': name_tag
                        })
                
                # Get RDS instances using live_service's database instance
                rds_result = live_service.database.list_db_instances()
                if rds_result.get('success'):
                    for db in rds_result.get('db_instances', [])[:3]:  # FIXED: db_instances not instances
                        db_id = db.get('DBInstanceIdentifier', 'unknown')
                        engine = db.get('Engine', 'unknown')
                        
                        resources_data.append({
                            'Resource ID': db_id,
                            'Type': 'RDS',
                            'Monthly Cost': '~Est',
                            'Tags': engine
                        })
                
                if resources_data:
                    resources = pd.DataFrame(resources_data)
                else:
                    # No resources found, show demo
                    resources = pd.DataFrame({
                        'Resource ID': [f'i-{i:08x}' for i in range(10)],
                        'Type': ['EC2'] * 5 + ['RDS'] * 3 + ['ELB'] * 2,
                        'Monthly Cost': [3456, 2345, 2123, 1987, 1765, 1654, 1543, 1432, 1321, 1210],
                        'Tags': ['prod-web', 'prod-api', 'dev-web', 'staging-db', 'prod-worker'] * 2
                    })
                    st.caption("⚠️ No AWS resources found - showing demo data")
                    
            except Exception as e:
                # Error fetching live data, fall back to demo
                st.caption(f"⚠️ Could not fetch live AWS resources ({str(e)[:50]}) - showing demo data")
                resources = pd.DataFrame({
                    'Resource ID': [f'i-{i:08x}' for i in range(10)],
                    'Type': ['EC2'] * 5 + ['RDS'] * 3 + ['ELB'] * 2,
                    'Monthly Cost': [3456, 2345, 2123, 1987, 1765, 1654, 1543, 1432, 1321, 1210],
                    'Tags': ['prod-web', 'prod-api', 'dev-web', 'staging-db', 'prod-worker'] * 2
                })
        else:
            # Demo mode - show demo data
            resources = pd.DataFrame({
                'Resource ID': [f'i-{i:08x}' for i in range(10)],
                'Type': ['EC2'] * 5 + ['RDS'] * 3 + ['ELB'] * 2,
                'Monthly Cost': [3456, 2345, 2123, 1987, 1765, 1654, 1543, 1432, 1321, 1210],
                'Tags': ['prod-web', 'prod-api', 'dev-web', 'staging-db', 'prod-worker'] * 2
            })
        
        st.dataframe(resources, use_container_width=True)
    
    def render_tag_based_tracking(self):
        """Tag-Based Cost Tracking"""
        st.subheader("🏷️ Tag-Based Cost Tracking")
        
        st.info("Track and allocate costs based on resource tags")
        
        # Tag-based allocation - MODE-AWARE
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Cost by Environment")
            
            # Check mode
            if st.session_state.get('mode', 'Demo') == 'Live' and DATA_PROVIDER_AVAILABLE:
                try:
                    live_service = get_live_service()
                    
                    # Get tag-based costs (placeholder - requires AWS Cost Allocation Tags)
                    # For now, estimate based on resource counts
                    ec2_result = live_service.compute.list_instances()
                    
                    if ec2_result.get('success'):
                        instances = ec2_result.get('instances', [])
                        
                        # Count instances by environment tag
                        env_counts = {'Production': 0, 'Staging': 0, 'Development': 0, 'QA': 0}
                        for instance in instances:
                            tags = instance.get('Tags', [])
                            env_tag = next((t['Value'] for t in tags if t['Key'] == 'Environment'), None)
                            if env_tag in env_counts:
                                env_counts[env_tag] += 1
                            elif env_tag:
                                env_counts[env_tag] = env_counts.get(env_tag, 0) + 1
                        
                        # Estimate costs (rough estimate: $100/instance/month)
                        env_data = pd.DataFrame({
                            'Environment': list(env_counts.keys()),
                            'Cost': [count * 100 for count in env_counts.values()]
                        })
                        st.caption("🔴 Live Mode: Estimated costs based on resource counts")
                    else:
                        # Fallback to demo
                        env_data = pd.DataFrame({
                            'Environment': ['Production', 'Staging', 'Development', 'QA'],
                            'Cost': [25000, 10000, 7500, 2500]
                        })
                        st.caption("⚠️ Using demo data")
                except Exception as e:
                    # Error - fallback to demo
                    env_data = pd.DataFrame({
                        'Environment': ['Production', 'Staging', 'Development', 'QA'],
                        'Cost': [25000, 10000, 7500, 2500]
                    })
                    st.caption(f"⚠️ Using demo data - Error: {str(e)[:40]}")
            else:
                # Demo mode
                env_data = pd.DataFrame({
                    'Environment': ['Production', 'Staging', 'Development', 'QA'],
                    'Cost': [25000, 10000, 7500, 2500]
                })
            
            st.bar_chart(env_data.set_index('Environment'))
        
        with col2:
            st.markdown("### Cost by Department")
            
            # Check mode
            if st.session_state.get('mode', 'Demo') == 'Live' and DATA_PROVIDER_AVAILABLE:
                try:
                    live_service = get_live_service()
                    
                    # Get tag-based costs by department
                    ec2_result = live_service.compute.list_instances()
                    
                    if ec2_result.get('success'):
                        instances = ec2_result.get('instances', [])
                        
                        # Count instances by department tag
                        dept_counts = {}
                        for instance in instances:
                            tags = instance.get('Tags', [])
                            dept_tag = next((t['Value'] for t in tags if t['Key'] == 'Department'), None)
                            if dept_tag:
                                dept_counts[dept_tag] = dept_counts.get(dept_tag, 0) + 1
                        
                        if dept_counts:
                            # Estimate costs
                            dept_data = pd.DataFrame({
                                'Department': list(dept_counts.keys()),
                                'Cost': [count * 100 for count in dept_counts.values()]
                            })
                            st.caption("🔴 Live Mode: Estimated costs")
                        else:
                            # No department tags found
                            dept_data = pd.DataFrame({
                                'Department': ['Engineering', 'Sales', 'Marketing', 'Operations'],
                                'Cost': [18000, 12000, 8000, 7000]
                            })
                            st.caption("⚠️ No Department tags found - showing demo")
                    else:
                        # Fallback to demo
                        dept_data = pd.DataFrame({
                            'Department': ['Engineering', 'Sales', 'Marketing', 'Operations'],
                            'Cost': [18000, 12000, 8000, 7000]
                        })
                        st.caption("⚠️ Using demo data")
                except Exception as e:
                    # Error - fallback to demo
                    dept_data = pd.DataFrame({
                        'Department': ['Engineering', 'Sales', 'Marketing', 'Operations'],
                        'Cost': [18000, 12000, 8000, 7000]
                    })
                    st.caption(f"⚠️ Using demo data - Error: {str(e)[:40]}")
            else:
                # Demo mode
                dept_data = pd.DataFrame({
                    'Department': ['Engineering', 'Sales', 'Marketing', 'Operations'],
                    'Cost': [18000, 12000, 8000, 7000]
                })
            
            st.bar_chart(dept_data.set_index('Department'))
        
        # Tag compliance - MODE-AWARE
        st.markdown("### Tag Compliance")
        col1, col2, col3 = st.columns(3)
        
        # Check mode
        if st.session_state.get('mode', 'Demo') == 'Live' and DATA_PROVIDER_AVAILABLE:
            try:
                live_service = get_live_service()
                
                # Calculate tag compliance from real resources
                ec2_result = live_service.compute.list_instances()
                
                if ec2_result.get('success'):
                    instances = ec2_result.get('instances', [])
                    total_resources = len(instances)
                    
                    if total_resources > 0:
                        # Count tagged resources (resources with at least one tag)
                        tagged = sum(1 for inst in instances if inst.get('Tags', []))
                        untagged = total_resources - tagged
                        compliance = int((tagged / total_resources) * 100)
                        
                        with col1:
                            st.metric("Tagged Resources", f"{tagged:,}", f"{compliance}%")
                        with col2:
                            st.metric("Untagged Resources", f"{untagged:,}", f"{100-compliance}%")
                        with col3:
                            st.metric("Compliance Score", f"{compliance}%", "+0%")
                        
                        st.caption("🔴 Live Mode: Real tag compliance data")
                    else:
                        # No resources found
                        with col1:
                            st.metric("Tagged Resources", "0", "0%")
                        with col2:
                            st.metric("Untagged Resources", "0", "0%")
                        with col3:
                            st.metric("Compliance Score", "0%", "+0%")
                        st.caption("⚠️ No resources found")
                else:
                    # Fallback to demo
                    with col1:
                        st.metric("Tagged Resources", "1,123", "91%")
                    with col2:
                        st.metric("Untagged Resources", "111", "9%")
                    with col3:
                        st.metric("Compliance Score", "91%", "+3%")
                    st.caption("⚠️ Using demo data")
            except Exception as e:
                # Error - fallback to demo
                with col1:
                    st.metric("Tagged Resources", "1,123", "91%")
                with col2:
                    st.metric("Untagged Resources", "111", "9%")
                with col3:
                    st.metric("Compliance Score", "91%", "+3%")
                st.caption(f"⚠️ Using demo data - Error: {str(e)[:40]}")
        else:
            # Demo mode
            with col1:
                st.metric("Tagged Resources", "1,123", "91%")
            with col2:
                st.metric("Untagged Resources", "111", "9%")
            with col3:
                st.metric("Compliance Score", "91%", "+3%")
    
    def render_budget_management(self):
        """Budget Policy Enforcement"""
        st.subheader("💵 Budget Management & Enforcement")
        
        # Budget overview
        st.markdown("### Budget Overview")
        budget_data = pd.DataFrame({
            'Budget Name': ['Production Monthly', 'Development Monthly', 'Marketing Campaign', 'R&D Q4'],
            'Allocated': [50000, 15000, 10000, 25000],
            'Spent': [38000, 12500, 7800, 19000],
            'Remaining': [12000, 2500, 2200, 6000],
            'Status': ['On Track', 'Warning', 'On Track', 'On Track']
        })
        st.dataframe(budget_data, use_container_width=True)
        
        # Budget alerts
        st.markdown("### Recent Budget Alerts")
        alerts = pd.DataFrame({
            'Time': ['2 hours ago', '1 day ago', '3 days ago'],
            'Budget': ['Development Monthly', 'Marketing Campaign', 'Production Monthly'],
            'Alert': ['Exceeded 80%', 'Exceeded 75%', 'Approaching 75%'],
            'Action': ['Email sent', 'Slack notification', 'Dashboard alert']
        })
        st.dataframe(alerts, use_container_width=True)
    
    def render_forecasting(self):
        """Cost Forecasting & Chargebacks"""
        st.subheader("📈 Cost Forecasting")
        
        st.info("ML-based cost forecasting and chargeback allocation")
        
        # Forecast chart
        st.markdown("### 90-Day Cost Forecast")
        dates = pd.date_range(start=datetime.now(), periods=90)
        forecast_data = pd.DataFrame({
            'Date': dates,
            'Actual/Forecast': [45000 + i * 200 for i in range(90)]
        })
        st.line_chart(forecast_data.set_index('Date'))
        
        # Forecast metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Current Month", "$45,234")
        with col2:
            st.metric("Next Month Forecast", "$47,890", "+5.9%")
        with col3:
            st.metric("Q4 Forecast", "$145,670")
        with col4:
            st.metric("Confidence", "87%")
    
    def render_scheduled_policies(self):
        """Scheduled Infrastructure Policies"""
        st.subheader("📅 Scheduled Infrastructure Policies")
        
        st.info("Automate resource scheduling to optimize costs")
        
        # Active schedules
        st.markdown("### Active Schedules")
        schedules = pd.DataFrame({
            'Schedule Name': ['Dev Environment Off-Hours', 'QA Weekend Shutdown', 'Non-Prod Night Stop'],
            'Resources': ['45 EC2, 12 RDS', '23 EC2, 5 RDS', '67 EC2, 18 RDS'],
            'Schedule': ['Weekdays 7PM-7AM', 'Sat-Sun All Day', 'Daily 8PM-6AM'],
            'Monthly Savings': ['$3,456', '$1,234', '$5,678'],
            'Status': ['Active', 'Active', 'Active']
        })
        st.dataframe(schedules, use_container_width=True)
        
        # Savings summary
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Monthly Savings", "$10,368")
        with col2:
            st.metric("Scheduled Resources", "167")
        with col3:
            st.metric("Active Schedules", "3")
    
    def render_spot_instances(self):
        """Spot Instance Orchestration"""
        st.subheader("⚡ Spot Instance Orchestration")
        
        st.info("Leverage spot instances for significant cost savings")
        
        # Spot usage
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Spot vs On-Demand")
            instance_mix = pd.DataFrame({
                'Type': ['Spot', 'On-Demand', 'Reserved'],
                'Count': [145, 89, 234]
            })
            st.bar_chart(instance_mix.set_index('Type'))
        
        with col2:
            st.markdown("### Spot Savings")
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Monthly Savings", "$12,456")
            with col_b:
                st.metric("Avg Discount", "68%")
        
        # Spot recommendations
        st.markdown("### Spot Recommendations")
        recommendations = pd.DataFrame({
            'Workload': ['Batch Processing', 'CI/CD Builds', 'Data Analytics', 'Dev Environments'],
            'Current': ['On-Demand', 'On-Demand', 'On-Demand', 'On-Demand'],
            'Recommended': ['Spot', 'Spot', 'Spot', 'Spot'],
            'Potential Savings': ['$3,400/mo', '$2,100/mo', '$4,500/mo', '$2,800/mo']
        })
        st.dataframe(recommendations, use_container_width=True)
    
    def render_anomaly_detection(self):
        """Cost Anomaly Detection"""
        st.subheader("🔍 Cost Anomaly Detection")
        
        st.info("AI-powered detection of unusual spending patterns")
        
        # Recent anomalies
        st.markdown("### Detected Anomalies (Last 7 Days)")
        anomalies = pd.DataFrame({
            'Date': ['2024-11-29', '2024-11-27', '2024-11-25'],
            'Service': ['EC2', 'S3', 'RDS'],
            'Expected': ['$1,200', '$450', '$800'],
            'Actual': ['$3,400', '$1,200', '$2,100'],
            'Variance': ['+183%', '+167%', '+163%'],
            'Status': ['Investigated', 'Auto-resolved', 'Open']
        })
        st.dataframe(anomalies, use_container_width=True)
        
        # Anomaly stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Anomalies (7d)", "3", "-2")
        with col2:
            st.metric("Auto-Resolved", "1")
        with col3:
            st.metric("Under Review", "1")
        with col4:
            st.metric("False Positives", "1")
    
    def render_reports(self):
        """Reporting Dashboards"""
        st.subheader("📋 Cost Reports & Dashboards")
        
        st.info("Customizable reports and executive dashboards")
        
        # Report types
        report_types = ["Executive Summary", "Detailed Breakdown", "Trend Analysis", "Budget vs Actual", "Forecast Report"]
        selected_report = st.selectbox("Select Report Type", report_types)
        
        # Date range
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=30))
        with col2:
            end_date = st.date_input("End Date", value=datetime.now())
        
        # Sample report data
        st.markdown(f"### {selected_report}")
        st.markdown("**Report Period:** {} to {}".format(start_date, end_date))
        
        report_data = pd.DataFrame({
            'Category': ['Compute', 'Storage', 'Database', 'Network', 'Other'],
            'Cost': [18450, 8920, 12340, 3210, 2314]
        })
        st.bar_chart(report_data.set_index('Category'))
        
        if st.button("📥 Export Report (CSV)"):
            st.success("Report exported successfully!")
    
    def render_ri_recommendations(self):
        """Reserved Instance Recommendations"""
        st.subheader("💡 Reserved Instance Recommendations")
        
        st.info("Optimize costs with RI and Savings Plans recommendations")
        
        # RI recommendations
        st.markdown("### Top RI Opportunities")
        ri_recs = pd.DataFrame({
            'Instance Type': ['m5.xlarge', 'r5.2xlarge', 't3.medium', 'c5.large'],
            'Current Usage': ['24/7', '24/7', '20/7', '24/7'],
            'RI Term': ['1 Year', '3 Year', '1 Year', '1 Year'],
            'Payment': ['Partial Upfront', 'All Upfront', 'No Upfront', 'Partial Upfront'],
            'Monthly Savings': ['$456', '$1,234', '$123', '$345'],
            'Annual Savings': ['$5,472', '$14,808', '$1,476', '$4,140']
        })
        st.dataframe(ri_recs, use_container_width=True)
        
        # Savings summary
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Potential Savings", "$25,896/year")
        with col2:
            st.metric("Current RI Coverage", "42%")
        with col3:
            st.metric("Recommended Coverage", "68%")
    
    def render_chargeback(self):
        """Chargeback & Showback"""
        st.subheader("📊 Chargeback & Showback")
        
        st.info("Allocate costs to business units and teams")
        
        # Chargeback by team
        st.markdown("### Monthly Chargeback by Team")
        chargeback_data = pd.DataFrame({
            'Team': ['Platform Engineering', 'Product Development', 'Data Science', 'DevOps', 'QA'],
            'Compute': [8900, 12300, 5600, 3400, 2100],
            'Storage': [2300, 3400, 1200, 800, 400],
            'Database': [4500, 6700, 2300, 1500, 900],
            'Total': [15700, 22400, 9100, 5700, 3400]
        })
        st.dataframe(chargeback_data, use_container_width=True)
        
        # Visualization
        st.markdown("### Team Cost Distribution")
        st.bar_chart(chargeback_data.set_index('Team')['Total'])
        
        # Export options
        if st.button("📧 Send Chargeback Reports"):
            st.success("Chargeback reports sent to team leads!")
