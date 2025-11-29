"""Module 4: FinOps - Financial Operations & Cost Management"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from demo_data import DemoDataProvider

class FinOpsModule:
    """FinOps Module - Cost Management & Optimization"""
    def render(self):
        """Main render method - organizes all sub-features in tabs"""
        
        st.markdown("## Finops")
        
        # Create tabs for each sub-feature
        tabs = st.tabs([
            "📋 Finops Overview",
            "⚙️ Tag Based Cost Tracking",
            "⚙️ Budget Policy Enforcement",
            "⚙️ Forecasting Chargebacks",
            "⚙️ Scheduled Infrastructure Policies",
            "⚙️ Spot Instance Orchestration",
            "⚙️ Cost Anomaly Detection",
            "⚙️ Reporting Dashboards",
            "⚙️ Pmo Vs Fmo",
            "⚙️ Ri Recommendations",
            "⚙️ Use Case Tracking"
        ])
        
        with tabs[0]:
            self.render_finops_overview()
        
        with tabs[1]:
            self.render_tag_based_cost_tracking()
        
        with tabs[2]:
            self.render_budget_policy_enforcement()
        
        with tabs[3]:
            self.render_forecasting_chargebacks()
        
        with tabs[4]:
            self.render_scheduled_infrastructure_policies()
        
        with tabs[5]:
            self.render_spot_instance_orchestration()
        
        with tabs[6]:
            self.render_cost_anomaly_detection()
        
        with tabs[7]:
            self.render_reporting_dashboards()
        
        with tabs[8]:
            self.render_pmo_vs_fmo()
        
        with tabs[9]:
            self.render_ri_recommendations()
        
        with tabs[10]:
            self.render_use_case_tracking()


    
    @staticmethod
    def render_finops_overview():
        """FinOps Overview Dashboard"""
        st.markdown("## 💰 FinOps - Financial Operations Dashboard")
        
        demo_mode = st.session_state.get('demo_mode', True)
        
        # Key Metrics Row
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Monthly Spend", "$234,567", "-8.2%")
        with col2:
            st.metric("Budget Utilization", "78%", "+3%")
        with col3:
            st.metric("Cost Savings", "$45,890", "+15%")
        with col4:
            st.metric("Anomalies Detected", "3", "-2")
        with col5:
            st.metric("RI Coverage", "67%", "+5%")
        
        st.markdown("---")
        
        # Quick Stats
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 📊 Current Month Overview")
            st.markdown(f"""
            - **Total Spend:** $234,567
            - **Forecasted:** $298,450
            - **Budget:** $300,000
            - **Variance:** +$1,550 (0.5%)
            - **Top Service:** EC2 ($89,234)
            - **Optimization Opportunities:** $22,340
            """)
        
        with col2:
            st.markdown("### 🎯 Cost Optimization Status")
            st.markdown("""
            - **Right-sizing Savings:** $12,450/mo
            - **Spot Instance Savings:** $18,900/mo
            - **RI Savings:** $8,760/mo
            - **Storage Tiering:** $5,780/mo
            - **Idle Resources:** $3,450/mo
            """)
        
        with col3:
            st.markdown("### 🚨 Active Alerts")
            st.markdown("""
            - 🔴 Budget threshold 80% - Project Alpha
            - 🟠 Anomaly: RDS spike +140%
            - 🟡 Untagged resources: 23
            - ✅ All forecasts within budget
            - ✅ No compliance violations
            """)
    
    @staticmethod
    def render_tag_based_cost_tracking():
        """Tag-Based Cost Tracking"""
        st.markdown("## 🏷️ Tag-Based Cost Tracking & Allocation")
        
        demo_mode = st.session_state.get('demo_mode', True)
        
        st.info("📊 Track and allocate costs across projects, departments, and environments using AWS tags")
        
        # Tag Coverage Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Tag Coverage", "94.3%", "+2.1%")
        with col2:
            st.metric("Untagged Resources", "23", "-12")
        with col3:
            st.metric("Untagged Cost", "$4,567", "-$1,234")
        with col4:
            st.metric("Cost Centers", "12", "0")
        
        st.markdown("---")
        
        # Cost by Tag Dimension
        st.markdown("### 💵 Cost Allocation by Tag Dimension")
        
        tab1, tab2, tab3, tab4 = st.tabs(["By Environment", "By Project", "By Department", "By Owner"])
        
        with tab1:
            st.markdown("#### Cost by Environment")
            env_data = [
                {"Environment": "Production", "Monthly Cost": "$145,890", "Budget": "$150,000", "Utilization": "97%", "Trend": "📈 +3%", "Resources": 1245},
                {"Environment": "Staging", "Monthly Cost": "$45,670", "Budget": "$50,000", "Utilization": "91%", "Trend": "📊 Stable", "Resources": 456},
                {"Environment": "Development", "Monthly Cost": "$32,450", "Budget": "$40,000", "Utilization": "81%", "Trend": "📉 -2%", "Resources": 789},
                {"Environment": "Testing", "Monthly Cost": "$10,557", "Budget": "$15,000", "Utilization": "70%", "Trend": "📊 Stable", "Resources": 234}
            ]
            st.dataframe(pd.DataFrame(env_data), use_container_width=True, hide_index=True)
        
        with tab2:
            st.markdown("#### Cost by Project")
            project_data = [
                {"Project": "Mobile App Rewrite", "Owner": "Engineering", "Cost": "$67,890", "Budget": "$70,000", "Variance": "+$2,110", "Status": "✅"},
                {"Project": "Data Analytics Platform", "Owner": "Data Team", "Cost": "$54,320", "Budget": "$55,000", "Variance": "+$680", "Status": "✅"},
                {"Project": "Customer Portal", "Owner": "Product", "Cost": "$43,210", "Budget": "$40,000", "Variance": "-$3,210", "Status": "⚠️"},
                {"Project": "ML Pipeline", "Owner": "AI/ML", "Cost": "$38,650", "Budget": "$45,000", "Variance": "+$6,350", "Status": "✅"},
                {"Project": "Infrastructure Migration", "Owner": "Platform", "Cost": "$30,497", "Budget": "$35,000", "Variance": "+$4,503", "Status": "✅"}
            ]
            st.dataframe(pd.DataFrame(project_data), use_container_width=True, hide_index=True)
        
        with tab3:
            st.markdown("#### Cost by Department")
            dept_data = [
                {"Department": "Engineering", "Head Count": 45, "Cost": "$112,340", "Per Employee": "$2,496", "Budget": "$120,000", "Variance": "6.4%"},
                {"Department": "Product", "Head Count": 22, "Cost": "$56,780", "Per Employee": "$2,581", "Budget": "$60,000", "Variance": "5.4%"},
                {"Department": "Data & Analytics", "Head Count": 18, "Cost": "$43,220", "Per Employee": "$2,401", "Budget": "$50,000", "Variance": "13.6%"},
                {"Department": "DevOps", "Head Count": 12, "Cost": "$22,227", "Per Employee": "$1,852", "Budget": "$25,000", "Variance": "11.1%"}
            ]
            st.dataframe(pd.DataFrame(dept_data), use_container_width=True, hide_index=True)
        
        with tab4:
            st.markdown("#### Cost by Owner/Team")
            owner_data = [
                {"Owner": "john.doe@company.com", "Team": "Backend", "Resources": 156, "Cost": "$23,450", "Untagged": 3, "Compliance": "98%"},
                {"Owner": "jane.smith@company.com", "Team": "Frontend", "Resources": 89, "Cost": "$12,340", "Untagged": 0, "Compliance": "100%"},
                {"Owner": "bob.wilson@company.com", "Team": "Data", "Resources": 234, "Cost": "$45,670", "Untagged": 12, "Compliance": "95%"},
                {"Owner": "alice.brown@company.com", "Team": "ML/AI", "Resources": 67, "Cost": "$18,900", "Untagged": 2, "Compliance": "97%"}
            ]
            st.dataframe(pd.DataFrame(owner_data), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Untagged Resources
        st.markdown("### ⚠️ Untagged Resources Requiring Attention")
        untagged = [
            {"Resource ID": "i-0abc123def456", "Type": "EC2 Instance", "Region": "us-east-1", "Cost (MTD)": "$234.56", "Age": "45 days", "Action": "Tag Now"},
            {"Resource ID": "vol-0xyz789abc123", "Type": "EBS Volume", "Region": "us-west-2", "Cost (MTD)": "$12.45", "Age": "12 days", "Action": "Tag Now"},
            {"Resource ID": "db-prod-untagged", "Type": "RDS Instance", "Region": "eu-west-1", "Cost (MTD)": "$456.78", "Age": "3 days", "Action": "Tag Now"}
        ]
        st.dataframe(pd.DataFrame(untagged), use_container_width=True, hide_index=True)
        
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("🏷️ Auto-Tag Resources", type="primary"):
                st.success("✅ Initiated auto-tagging for 23 resources")
    
    @staticmethod
    def render_budget_policy_enforcement():
        """Budget Policy Enforcement"""
        st.markdown("## 📋 Budget Policy Enforcement & Governance")
        
        demo_mode = st.session_state.get('demo_mode', True)
        
        st.info("🎯 Enforce budget limits, spending caps, and automated actions when thresholds are breached")
        
        # Budget Status Overview
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Active Budgets", "18", "+2")
        with col2:
            st.metric("Alerts Triggered", "5", "+2")
        with col3:
            st.metric("Auto-Actions", "12", "+3")
        with col4:
            st.metric("Budget Compliance", "94%", "-1%")
        
        st.markdown("---")
        
        # Active Budgets
        st.markdown("### 💼 Active Budget Policies")
        
        budgets = [
            {
                "Budget Name": "Production Infrastructure",
                "Period": "Monthly",
                "Budget": "$150,000",
                "Actual": "$145,890",
                "Forecast": "$148,200",
                "Utilization": "97%",
                "Status": "🟡 Warning (80%)",
                "Alert": "Email + Slack"
            },
            {
                "Budget Name": "Development Environments",
                "Period": "Monthly",
                "Budget": "$40,000",
                "Actual": "$32,450",
                "Forecast": "$35,600",
                "Utilization": "81%",
                "Status": "✅ Healthy",
                "Alert": "None"
            },
            {
                "Budget Name": "Data Analytics Project",
                "Period": "Quarterly",
                "Budget": "$165,000",
                "Actual": "$138,750",
                "Forecast": "$162,300",
                "Utilization": "84%",
                "Status": "✅ Healthy",
                "Alert": "None"
            },
            {
                "Budget Name": "ML Training Workloads",
                "Period": "Monthly",
                "Budget": "$50,000",
                "Actual": "$43,890",
                "Forecast": "$52,100",
                "Utilization": "88%",
                "Status": "🔴 Critical (90%)",
                "Alert": "Email + Auto-stop"
            }
        ]
        st.dataframe(pd.DataFrame(budgets), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Budget Policy Configuration
        st.markdown("### ⚙️ Create/Edit Budget Policy")
        
        col1, col2 = st.columns(2)
        
        with col1:
            budget_name = st.text_input("Budget Name", "Q1 Development Budget")
            budget_scope = st.selectbox("Scope", ["Account", "Tag: Environment", "Tag: Project", "Tag: Department", "Service Type"])
            budget_period = st.selectbox("Period", ["Monthly", "Quarterly", "Annually"])
            budget_amount = st.number_input("Budget Amount ($)", min_value=1000, value=50000, step=1000)
            
            st.markdown("#### Alert Thresholds")
            threshold_1 = st.slider("Warning Threshold (%)", 50, 100, 80)
            threshold_2 = st.slider("Critical Threshold (%)", 50, 100, 90)
        
        with col2:
            st.markdown("#### Actions on Threshold Breach")
            
            st.markdown("**At 80% (Warning):**")
            st.checkbox("📧 Send email to budget owner", value=True)
            st.checkbox("💬 Send Slack notification", value=True)
            st.checkbox("📊 Generate cost report", value=True)
            
            st.markdown("**At 90% (Critical):**")
            st.checkbox("🚨 Send escalation email to leadership", value=True)
            st.checkbox("🛑 Block new resource provisioning", value=False)
            st.checkbox("⏸️ Stop non-production resources", value=False)
            st.checkbox("📈 Require approval for new spend", value=True)
            
            if st.button("💾 Save Budget Policy", type="primary"):
                st.success("✅ Budget policy created successfully")
        
        st.markdown("---")
        
        # Recent Budget Alerts
        st.markdown("### 🚨 Recent Budget Alerts & Actions")
        
        alerts = [
            {
                "Timestamp": "2024-11-18 14:35",
                "Budget": "ML Training Workloads",
                "Event": "Critical threshold (90%) exceeded",
                "Current": "$43,890 / $50,000",
                "Action Taken": "Email sent + Auto-stop scheduled",
                "Status": "🔴 Active"
            },
            {
                "Timestamp": "2024-11-18 09:12",
                "Budget": "Production Infrastructure",
                "Event": "Warning threshold (80%) exceeded",
                "Current": "$145,890 / $150,000",
                "Action Taken": "Notification sent to team",
                "Status": "🟡 Acknowledged"
            },
            {
                "Timestamp": "2024-11-17 16:45",
                "Budget": "Development Environments",
                "Event": "Forecast exceeds budget",
                "Current": "$32,450 / $40,000 (Forecast: $41,200)",
                "Action Taken": "Alert sent to engineering lead",
                "Status": "✅ Resolved"
            }
        ]
        st.dataframe(pd.DataFrame(alerts), use_container_width=True, hide_index=True)
    
    @staticmethod
    def render_forecasting_chargebacks():
        """Cost Forecasting & Chargebacks"""
        st.markdown("## 📈 Cost Forecasting & Chargeback Management")
        
        demo_mode = st.session_state.get('demo_mode', True)
        
        st.info("🔮 Predict future costs using ML models and allocate costs back to departments/projects")
        
        # Forecast Summary
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Current Month Forecast", "$298,450", "")
        with col2:
            st.metric("Confidence", "87%", "+3%")
        with col3:
            st.metric("Q4 Forecast", "$892,340", "")
        with col4:
            st.metric("Annual Projection", "$3.2M", "+12%")
        
        st.markdown("---")
        
        # Forecasting Dashboard
        st.markdown("### 📊 Cost Forecast - Next 6 Months")
        
        forecast_data = [
            {"Month": "Dec 2024", "Actual": "", "Forecast": "$298,450", "Lower Bound": "$285,200", "Upper Bound": "$312,700", "Confidence": "87%"},
            {"Month": "Jan 2025", "Actual": "", "Forecast": "$312,890", "Lower Bound": "$296,500", "Upper Bound": "$329,280", "Confidence": "82%"},
            {"Month": "Feb 2025", "Actual": "", "Forecast": "$305,670", "Lower Bound": "$288,100", "Upper Bound": "$323,240", "Confidence": "78%"},
            {"Month": "Mar 2025", "Actual": "", "Forecast": "$318,900", "Lower Bound": "$299,200", "Upper Bound": "$338,600", "Confidence": "74%"},
            {"Month": "Apr 2025", "Actual": "", "Forecast": "$325,450", "Lower Bound": "$304,800", "Upper Bound": "$346,100", "Confidence": "70%"},
            {"Month": "May 2025", "Actual": "", "Forecast": "$332,120", "Lower Bound": "$309,500", "Upper Bound": "$354,740", "Confidence": "66%"}
        ]
        st.dataframe(pd.DataFrame(forecast_data), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Forecast Drivers
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📌 Key Forecast Drivers")
            drivers = [
                {"Factor": "Seasonal growth pattern", "Impact": "+8%", "Confidence": "High"},
                {"Factor": "Planned infrastructure expansion", "Impact": "+12%", "Confidence": "High"},
                {"Factor": "New ML training workloads", "Impact": "+15%", "Confidence": "Medium"},
                {"Factor": "Right-sizing initiatives", "Impact": "-5%", "Confidence": "High"},
                {"Factor": "RI/SP coverage increase", "Impact": "-8%", "Confidence": "Medium"}
            ]
            st.dataframe(pd.DataFrame(drivers), use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("### 🎯 Forecast Accuracy (Last 6 Months)")
            accuracy = [
                {"Month": "Nov 2024", "Actual": "$234,567", "Forecast": "$235,890", "Variance": "-0.6%", "Accuracy": "99.4%"},
                {"Month": "Oct 2024", "Actual": "$228,340", "Forecast": "$232,100", "Variance": "-1.6%", "Accuracy": "98.4%"},
                {"Month": "Sep 2024", "Actual": "$219,890", "Forecast": "$215,670", "Variance": "+1.9%", "Accuracy": "98.1%"},
                {"Month": "Aug 2024", "Actual": "$212,450", "Forecast": "$218,900", "Variance": "-3.0%", "Accuracy": "97.0%"}
            ]
            st.dataframe(pd.DataFrame(accuracy), use_container_width=True, hide_index=True)
            st.metric("Average Forecast Accuracy", "98.2%", "+1.2%")
        
        st.markdown("---")
        
        # Chargeback Management
        st.markdown("### 💳 Chargeback & Showback Reports")
        
        tab1, tab2, tab3 = st.tabs(["Monthly Chargebacks", "YTD Summary", "Custom Report"])
        
        with tab1:
            st.markdown("#### November 2024 Chargeback Report")
            chargeback = [
                {
                    "Department": "Engineering",
                    "Projects": 8,
                    "Compute": "$45,670",
                    "Storage": "$12,340",
                    "Database": "$23,450",
                    "Network": "$8,900",
                    "Other": "$6,780",
                    "Total": "$97,140",
                    "% of Total": "41.4%"
                },
                {
                    "Department": "Product",
                    "Projects": 5,
                    "Compute": "$23,450",
                    "Storage": "$6,780",
                    "Database": "$12,340",
                    "Network": "$4,560",
                    "Other": "$3,450",
                    "Total": "$50,580",
                    "% of Total": "21.6%"
                },
                {
                    "Department": "Data & Analytics",
                    "Projects": 4,
                    "Compute": "$18,900",
                    "Storage": "$15,670",
                    "Database": "$8,760",
                    "Network": "$3,450",
                    "Other": "$2,340",
                    "Total": "$49,120",
                    "% of Total": "20.9%"
                },
                {
                    "Department": "DevOps/Platform",
                    "Projects": 3,
                    "Compute": "$12,340",
                    "Storage": "$4,560",
                    "Database": "$5,670",
                    "Network": "$6,780",
                    "Other": "$8,377",
                    "Total": "$37,727",
                    "% of Total": "16.1%"
                }
            ]
            st.dataframe(pd.DataFrame(chargeback), use_container_width=True, hide_index=True)
            
            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button("📊 Export CSV"):
                    st.success("✅ Report exported")
                if st.button("📧 Email Report"):
                    st.success("✅ Report sent")
        
        with tab2:
            st.markdown("#### Year-to-Date Chargeback Summary")
            ytd = [
                {"Department": "Engineering", "Q1": "$287,450", "Q2": "$312,890", "Q3": "$345,670", "Q4 (PTD)": "$97,140", "YTD Total": "$1,043,150", "Trend": "📈"},
                {"Department": "Product", "Q1": "$145,670", "Q2": "$156,780", "Q3": "$178,900", "Q4 (PTD)": "$50,580", "YTD Total": "$531,930", "Trend": "📈"},
                {"Department": "Data & Analytics", "Q1": "$134,560", "Q2": "$148,900", "Q3": "$167,890", "Q4 (PTD)": "$49,120", "YTD Total": "$500,470", "Trend": "📈"},
                {"Department": "DevOps/Platform", "Q1": "$98,760", "Q2": "$112,340", "Q3": "$123,450", "Q4 (PTD)": "$37,727", "YTD Total": "$372,277", "Trend": "📈"}
            ]
            st.dataframe(pd.DataFrame(ytd), use_container_width=True, hide_index=True)
        
        with tab3:
            st.markdown("#### Generate Custom Chargeback Report")
            
            col1, col2 = st.columns(2)
            with col1:
                report_period = st.selectbox("Period", ["Last Month", "Last Quarter", "Last 6 Months", "Year to Date", "Custom Range"])
                allocation_method = st.selectbox("Allocation Method", ["Tag-Based", "Resource-Based", "Proportional", "Usage-Based"])
                group_by = st.multiselect("Group By", ["Department", "Project", "Environment", "Owner", "Service"], default=["Department"])
            
            with col2:
                include_untagged = st.checkbox("Include untagged resources", value=True)
                include_shared = st.checkbox("Include shared services", value=True)
                breakdown_level = st.selectbox("Detail Level", ["Summary", "Detailed", "Full Itemization"])
                
                if st.button("🔄 Generate Report", type="primary"):
                    st.success("✅ Custom chargeback report generated")
    
    @staticmethod
    def render_scheduled_infrastructure_policies():
        """Scheduled Infrastructure Policies"""
        st.markdown("## ⏰ Scheduled Infrastructure Policies & Automation")
        
        demo_mode = st.session_state.get('demo_mode', True)
        
        st.info("🕐 Automate resource scheduling to reduce costs during non-business hours")
        
        # Scheduling Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Active Schedules", "23", "+3")
        with col2:
            st.metric("Resources Managed", "456", "+45")
        with col3:
            st.metric("Monthly Savings", "$18,900", "+$3,200")
        with col4:
            st.metric("Automation Rate", "89%", "+5%")
        
        st.markdown("---")
        
        # Active Schedules
        st.markdown("### 📅 Active Infrastructure Schedules")
        
        schedules = [
            {
                "Schedule Name": "Dev Environment Shutdown",
                "Resources": "Dev EC2, RDS, EKS",
                "Count": 89,
                "Schedule": "Mon-Fri: Stop 7PM, Start 7AM",
                "Weekend": "Stopped",
                "Status": "🟢 Active",
                "Monthly Savings": "$6,780"
            },
            {
                "Schedule Name": "Test Environment Management",
                "Resources": "Test EC2, RDS",
                "Count": 45,
                "Schedule": "Mon-Fri: Stop 9PM, Start 6AM",
                "Weekend": "Stopped",
                "Status": "🟢 Active",
                "Monthly Savings": "$4,560"
            },
            {
                "Schedule Name": "Staging Auto-scaling",
                "Resources": "Staging ASG",
                "Count": 34,
                "Schedule": "Scale down 50% after 8PM",
                "Weekend": "Minimum capacity",
                "Status": "🟢 Active",
                "Monthly Savings": "$3,450"
            },
            {
                "Schedule Name": "Analytics Cluster Weekend",
                "Resources": "EMR Clusters",
                "Count": 12,
                "Schedule": "Weekends: Terminate",
                "Weekend": "Stopped",
                "Status": "🟢 Active",
                "Monthly Savings": "$4,110"
            }
        ]
        st.dataframe(pd.DataFrame(schedules), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Create New Schedule
        st.markdown("### ➕ Create New Schedule Policy")
        
        col1, col2 = st.columns(2)
        
        with col1:
            schedule_name = st.text_input("Schedule Name", "QA Environment Schedule")
            target_selector = st.selectbox("Target Selection", ["Tags", "Resource IDs", "Auto Scaling Groups", "Resource Type"])
            
            if target_selector == "Tags":
                tag_key = st.selectbox("Tag Key", ["Environment", "Project", "Owner", "Department"])
                tag_value = st.text_input("Tag Value", "qa")
            
            resource_types = st.multiselect(
                "Resource Types",
                ["EC2 Instances", "RDS Databases", "Auto Scaling Groups", "ECS Services", "EKS Clusters"],
                default=["EC2 Instances"]
            )
        
        with col2:
            st.markdown("#### Schedule Configuration")
            
            schedule_type = st.selectbox("Schedule Type", ["Time-based", "Event-based", "Usage-based"])
            
            if schedule_type == "Time-based":
                st.markdown("**Weekday Schedule:**")
                start_time = st.time_input("Start Time", value=None)
                stop_time = st.time_input("Stop Time", value=None)
                
                weekend_action = st.selectbox("Weekend Action", ["Stop All Weekend", "Run Normal Schedule", "Custom Weekend Schedule"])
                
                timezone = st.selectbox("Timezone", ["UTC", "America/New_York", "America/Los_Angeles", "Europe/London"])
            
            if st.button("💾 Create Schedule", type="primary"):
                st.success("✅ Schedule policy created successfully")
        
        st.markdown("---")
        
        # Schedule Execution History
        st.markdown("### 📊 Recent Schedule Executions")
        
        executions = [
            {"Timestamp": "2024-11-18 19:00", "Schedule": "Dev Environment Shutdown", "Action": "Stop 89 resources", "Duration": "3m 45s", "Status": "✅ Success", "Savings": "$156"},
            {"Timestamp": "2024-11-18 07:00", "Schedule": "Dev Environment Shutdown", "Action": "Start 89 resources", "Duration": "4m 12s", "Status": "✅ Success", "Savings": "-"},
            {"Timestamp": "2024-11-17 21:00", "Schedule": "Test Environment Management", "Action": "Stop 45 resources", "Duration": "2m 18s", "Status": "✅ Success", "Savings": "$98"},
            {"Timestamp": "2024-11-17 20:00", "Schedule": "Staging Auto-scaling", "Action": "Scale down to 50%", "Duration": "1m 34s", "Status": "✅ Success", "Savings": "$67"}
        ]
        st.dataframe(pd.DataFrame(executions), use_container_width=True, hide_index=True)
    
    @staticmethod
    def render_spot_instance_orchestration():
        """Spot Instance Orchestration"""
        st.markdown("## 🎯 Spot Instance Orchestration & Management")
        
        demo_mode = st.session_state.get('demo_mode', True)
        
        st.info("💡 Maximize savings with intelligent spot instance orchestration and fallback strategies")
        
        # Spot Metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Spot Instances", "234", "+23")
        with col2:
            st.metric("Monthly Savings", "$18,900", "+$2,400")
        with col3:
            st.metric("Interruption Rate", "2.3%", "-0.5%")
        with col4:
            st.metric("Avg Discount", "72%", "+3%")
        with col5:
            st.metric("Spot Coverage", "45%", "+8%")
        
        st.markdown("---")
        
        # Spot Fleet Management
        st.markdown("### 🚀 Active Spot Fleets")
        
        fleets = [
            {
                "Fleet Name": "Web App Workers",
                "Target Capacity": "100 vCPUs",
                "Fulfilled": "98 vCPUs (98%)",
                "Instance Types": "t3.large, t3a.large, t2.large",
                "Allocation": "Lowest Price",
                "Interruptions (24h)": "2",
                "Savings": "$1,234/day"
            },
            {
                "Fleet Name": "Batch Processing",
                "Target Capacity": "500 vCPUs",
                "Fulfilled": "489 vCPUs (98%)",
                "Instance Types": "c5.xlarge, c5a.xlarge, c5n.xlarge",
                "Allocation": "Capacity Optimized",
                "Interruptions (24h)": "5",
                "Savings": "$3,456/day"
            },
            {
                "Fleet Name": "ML Training",
                "Target Capacity": "32 GPUs",
                "Fulfilled": "32 GPUs (100%)",
                "Instance Types": "p3.2xlarge, p3.8xlarge",
                "Allocation": "Diversified",
                "Interruptions (24h)": "1",
                "Savings": "$2,890/day"
            }
        ]
        st.dataframe(pd.DataFrame(fleets), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Spot Interruption Handling
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ⚡ Interruption Management")
            
            interruptions = [
                {"Time": "2024-11-18 14:23", "Instance": "i-0abc123", "Type": "c5.xlarge", "AZ": "us-east-1a", "Action": "Replaced", "Downtime": "38s"},
                {"Time": "2024-11-18 11:45", "Instance": "i-0def456", "Type": "t3.large", "AZ": "us-east-1b", "Action": "Replaced", "Downtime": "42s"},
                {"Time": "2024-11-18 09:12", "Instance": "i-0ghi789", "Type": "c5a.xlarge", "AZ": "us-east-1c", "Action": "Replaced", "Downtime": "35s"}
            ]
            st.dataframe(pd.DataFrame(interruptions), use_container_width=True, hide_index=True)
            
            st.markdown("**Interruption Handling Strategy:**")
            st.markdown("- ✅ 2-minute warning monitoring enabled")
            st.markdown("- ✅ Automatic workload migration")
            st.markdown("- ✅ On-Demand fallback configured")
            st.markdown("- ✅ Application-level checkpointing")
        
        with col2:
            st.markdown("### 📊 Spot Price History & Trends")
            
            price_history = [
                {"Instance Type": "t3.large", "Current": "$0.0250", "Avg (7d)": "$0.0245", "On-Demand": "$0.0832", "Savings": "70%"},
                {"Instance Type": "c5.xlarge", "Current": "$0.0420", "Avg (7d)": "$0.0438", "On-Demand": "$0.1700", "Savings": "75%"},
                {"Instance Type": "p3.2xlarge", "Current": "$0.9180", "Avg (7d)": "$0.9250", "On-Demand": "$3.0600", "Savings": "70%"},
                {"Instance Type": "r5.large", "Current": "$0.0315", "Avg (7d)": "$0.0325", "On-Demand": "$0.1260", "Savings": "75%"}
            ]
            st.dataframe(pd.DataFrame(price_history), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Create Spot Request
        st.markdown("### ➕ Create New Spot Fleet Request")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fleet_name = st.text_input("Fleet Name", "My Spot Fleet")
            target_capacity = st.number_input("Target Capacity (vCPUs)", min_value=1, value=100)
            
            allocation_strategy = st.selectbox(
                "Allocation Strategy",
                ["Lowest Price", "Capacity Optimized", "Diversified", "Capacity Optimized Prioritized"]
            )
            
            instance_types = st.multiselect(
                "Instance Types",
                ["t3.large", "t3a.large", "t2.large", "c5.xlarge", "c5a.xlarge", "c5n.xlarge"],
                default=["t3.large", "t3a.large"]
            )
        
        with col2:
            on_demand_base = st.slider("On-Demand Base Capacity (%)", 0, 100, 10)
            on_demand_above_base = st.slider("On-Demand Above Base (%)", 0, 100, 20)
            
            st.markdown("#### Interruption Handling")
            interruption_behavior = st.selectbox("Behavior", ["Terminate", "Stop", "Hibernate"])
            enable_fallback = st.checkbox("Enable On-Demand Fallback", value=True)
            enable_rebalancing = st.checkbox("Enable Capacity Rebalancing", value=True)
            
            if st.button("🚀 Launch Spot Fleet", type="primary"):
                st.success("✅ Spot fleet request submitted")
    
    @staticmethod
    def render_cost_anomaly_detection():
        """Real-time Cost Anomaly Detection"""
        st.markdown("## 🚨 Real-Time Cost Anomaly Detection")
        
        demo_mode = st.session_state.get('demo_mode', True)
        
        st.info("🔍 AI-powered anomaly detection identifies unusual spending patterns in real-time")
        
        # Anomaly Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Anomalies (24h)", "3", "-1")
        with col2:
            st.metric("False Positives", "1", "0")
        with col3:
            st.metric("Avg Detection Time", "8 min", "-2 min")
        with col4:
            st.metric("Cost Impact", "$4,567", "-$1,234")
        
        st.markdown("---")
        
        # Active Anomalies
        st.markdown("### 🔴 Active Cost Anomalies")
        
        anomalies = [
            {
                "Detected": "2024-11-18 13:45",
                "Service": "RDS",
                "Resource": "prod-analytics-db",
                "Anomaly": "+140% spike in cost",
                "Baseline": "$145/day",
                "Current": "$348/day",
                "Root Cause": "Increased IOPS utilization",
                "Status": "🔴 Investigating",
                "Severity": "High"
            },
            {
                "Detected": "2024-11-18 11:20",
                "Service": "Lambda",
                "Resource": "image-processor-*",
                "Anomaly": "+85% increase in invocations",
                "Baseline": "2.3M/day",
                "Current": "4.3M/day",
                "Root Cause": "Bot traffic detected",
                "Status": "🟡 Monitoring",
                "Severity": "Medium"
            },
            {
                "Detected": "2024-11-18 09:15",
                "Service": "Data Transfer",
                "Resource": "us-east-1 → eu-west-1",
                "Anomaly": "+220% data transfer",
                "Baseline": "1.2 TB/day",
                "Current": "3.8 TB/day",
                "Root Cause": "Unoptimized replication",
                "Status": "🟢 Resolved",
                "Severity": "High"
            }
        ]
        st.dataframe(pd.DataFrame(anomalies), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Anomaly Details
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Anomaly Detection Model Performance")
            
            model_metrics = [
                {"Metric": "Detection Accuracy", "Value": "94.5%", "Target": ">90%", "Status": "✅"},
                {"Metric": "False Positive Rate", "Value": "5.2%", "Target": "<10%", "Status": "✅"},
                {"Metric": "Mean Time to Detect", "Value": "8 minutes", "Target": "<15 min", "Status": "✅"},
                {"Metric": "Coverage", "Value": "98.7%", "Target": ">95%", "Status": "✅"}
            ]
            st.dataframe(pd.DataFrame(model_metrics), use_container_width=True, hide_index=True)
            
            st.markdown("**Detection Methods:**")
            st.markdown("- Statistical (Z-score, IQR)")
            st.markdown("- Machine Learning (Isolation Forest)")
            st.markdown("- Time-series analysis (Prophet)")
            st.markdown("- Business rules & thresholds")
        
        with col2:
            st.markdown("### 🎯 Anomaly Types & Distribution")
            
            types = [
                {"Type": "Cost Spike", "Count (30d)": 23, "Avg Impact": "$1,234", "Resolution Time": "2.3h"},
                {"Type": "Usage Surge", "Count (30d)": 18, "Avg Impact": "$890", "Resolution Time": "1.8h"},
                {"Type": "Resource Provisioning", "Count (30d)": 12, "Avg Impact": "$2,450", "Resolution Time": "0.5h"},
                {"Type": "Service Degradation", "Count (30d)": 8, "Avg Impact": "$567", "Resolution Time": "3.1h"}
            ]
            st.dataframe(pd.DataFrame(types), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Configure Anomaly Detection
        st.markdown("### ⚙️ Configure Anomaly Detection Rules")
        
        col1, col2 = st.columns(2)
        
        with col1:
            sensitivity = st.slider("Detection Sensitivity", 1, 10, 7,
                help="Higher = More sensitive (more alerts)")
            
            monitored_services = st.multiselect(
                "Monitored Services",
                ["EC2", "RDS", "Lambda", "S3", "DynamoDB", "Data Transfer", "All"],
                default=["All"]
            )
            
            threshold_pct = st.number_input("Alert Threshold (% change)", min_value=10, value=50, step=10)
            
            notification_channels = st.multiselect(
                "Notification Channels",
                ["Email", "Slack", "PagerDuty", "SNS Topic"],
                default=["Email", "Slack"]
            )
        
        with col2:
            st.markdown("#### Anomaly Actions")
            
            auto_investigate = st.checkbox("Auto-investigate anomalies", value=True)
            create_ticket = st.checkbox("Auto-create JIRA ticket", value=False)
            send_report = st.checkbox("Send daily anomaly report", value=True)
            
            st.markdown("#### Exclusions")
            exclude_planned = st.checkbox("Exclude planned maintenance windows", value=True)
            exclude_dev = st.checkbox("Exclude development resources", value=False)
            
            if st.button("💾 Save Configuration", type="primary"):
                st.success("✅ Anomaly detection rules updated")
        
        st.markdown("---")
        
        # Historical Anomalies
        st.markdown("### 📈 Anomaly Detection History (Last 30 Days)")
        
        history = [
            {"Date": "Nov 18", "Detected": 3, "Confirmed": 2, "False Positives": 1, "Avg Resolution": "1.8h", "Cost Impact": "$4,567"},
            {"Date": "Nov 17", "Detected": 5, "Confirmed": 4, "False Positives": 1, "Avg Resolution": "2.1h", "Cost Impact": "$6,890"},
            {"Date": "Nov 16", "Detected": 2, "Confirmed": 2, "False Positives": 0, "Avg Resolution": "1.5h", "Cost Impact": "$2,340"},
            {"Date": "Nov 15", "Detected": 4, "Confirmed": 3, "False Positives": 1, "Avg Resolution": "2.5h", "Cost Impact": "$5,670"}
        ]
        st.dataframe(pd.DataFrame(history), use_container_width=True, hide_index=True)
    
    @staticmethod
    def render_reporting_dashboards():
        """FinOps Reporting & Dashboards"""
        st.markdown("## 📊 FinOps Reporting & Executive Dashboards")
        
        demo_mode = st.session_state.get('demo_mode', True)
        
        st.info("📈 Comprehensive cost analytics and executive-ready financial reports")
        
        # Report Types
        tab1, tab2, tab3, tab4 = st.tabs(["Executive Summary", "Cost Analysis", "Optimization Reports", "Custom Reports"])
        
        with tab1:
            st.markdown("### 📋 Executive Summary - November 2024")
            
            # Key Highlights
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("#### 💰 Financial Overview")
                st.markdown("""
                - **Total Spend:** $234,567 (-8.2%)
                - **Budget:** $300,000
                - **Utilization:** 78%
                - **Forecast EOY:** $3.2M
                - **YoY Growth:** +12%
                """)
            
            with col2:
                st.markdown("#### 🎯 Optimization Impact")
                st.markdown("""
                - **Monthly Savings:** $45,890
                - **YTD Savings:** $512,340
                - **Right-sizing:** $12,450/mo
                - **Spot Instances:** $18,900/mo
                - **RI/SP:** $8,760/mo
                """)
            
            with col3:
                st.markdown("#### 📊 Key Metrics")
                st.markdown("""
                - **Cost per Env:** 35% lower
                - **RI Coverage:** 67% (+5%)
                - **Spot Coverage:** 45% (+8%)
                - **Waste Detected:** $8,340
                - **Compliance:** 94%
                """)
            
            st.markdown("---")
            
            # Top Cost Centers
            st.markdown("#### Top 5 Cost Centers")
            cost_centers = [
                {"Rank": 1, "Department": "Engineering", "Current": "$97,140", "Budget": "$120,000", "Variance": "+19%", "Trend": "📉 Optimizing"},
                {"Rank": 2, "Department": "Product", "Current": "$50,580", "Budget": "$60,000", "Variance": "+16%", "Trend": "📊 Stable"},
                {"Rank": 3, "Department": "Data & Analytics", "Current": "$49,120", "Budget": "$50,000", "Variance": "+2%", "Trend": "📈 Growing"},
                {"Rank": 4, "Department": "DevOps/Platform", "Current": "$37,727", "Budget": "$45,000", "Variance": "+16%", "Trend": "📊 Stable"}
            ]
            st.dataframe(pd.DataFrame(cost_centers), use_container_width=True, hide_index=True)
            
            if st.button("📧 Email Executive Summary"):
                st.success("✅ Executive summary sent to leadership")
        
        with tab2:
            st.markdown("### 🔍 Detailed Cost Analysis")
            
            analysis_type = st.selectbox(
                "Analysis Type",
                ["Service Breakdown", "Regional Analysis", "Environment Comparison", "Time Series"]
            )
            
            if analysis_type == "Service Breakdown":
                service_costs = [
                    {"Service": "EC2", "Cost": "$89,234", "% of Total": "38.0%", "Trend": "📊 Stable", "Top Resource": "web-prod-asg"},
                    {"Service": "RDS", "Cost": "$45,670", "% of Total": "19.5%", "Trend": "📈 +12%", "Top Resource": "prod-analytics-db"},
                    {"Service": "S3", "Cost": "$23,450", "% of Total": "10.0%", "Trend": "📉 -5%", "Top Resource": "data-lake-prod"},
                    {"Service": "Lambda", "Cost": "$12,340", "% of Total": "5.3%", "Trend": "📈 +8%", "Top Resource": "api-gateway-*"},
                    {"Service": "Data Transfer", "Cost": "$18,900", "% of Total": "8.1%", "Trend": "📊 Stable", "Top Resource": "CloudFront"},
                    {"Service": "Other", "Cost": "$44,973", "% of Total": "19.1%", "Trend": "📊 Stable", "Top Resource": "Various"}
                ]
                st.dataframe(pd.DataFrame(service_costs), use_container_width=True, hide_index=True)
        
        with tab3:
            st.markdown("### 💡 Cost Optimization Reports")
            
            st.markdown("#### Identified Optimization Opportunities")
            
            opportunities = [
                {
                    "ID": "OPT-001",
                    "Category": "Right-sizing",
                    "Description": "18 over-provisioned EC2 instances",
                    "Current Cost": "$4,567/mo",
                    "Optimized Cost": "$1,890/mo",
                    "Savings": "$2,677/mo (59%)",
                    "Effort": "Low",
                    "Priority": "🔴 High"
                },
                {
                    "ID": "OPT-002",
                    "Category": "Storage Tiering",
                    "Description": "S3 data eligible for Glacier",
                    "Current Cost": "$3,450/mo",
                    "Optimized Cost": "$890/mo",
                    "Savings": "$2,560/mo (74%)",
                    "Effort": "Low",
                    "Priority": "🔴 High"
                },
                {
                    "ID": "OPT-003",
                    "Category": "Reserved Instances",
                    "Description": "Steady-state RDS workloads",
                    "Current Cost": "$12,340/mo",
                    "Optimized Cost": "$8,760/mo",
                    "Savings": "$3,580/mo (29%)",
                    "Effort": "Medium",
                    "Priority": "🟡 Medium"
                }
            ]
            st.dataframe(pd.DataFrame(opportunities), use_container_width=True, hide_index=True)
            
            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button("📊 Export Recommendations"):
                    st.success("✅ Report exported")
        
        with tab4:
            st.markdown("### 📝 Create Custom Report")
            
            col1, col2 = st.columns(2)
            
            with col1:
                report_name = st.text_input("Report Name", "Monthly Cost Review")
                report_period = st.selectbox("Time Period", ["Last 7 Days", "Last 30 Days", "Last Quarter", "YTD", "Custom"])
                
                metrics = st.multiselect(
                    "Include Metrics",
                    ["Total Spend", "Budget Variance", "Cost by Service", "Cost by Project", "Optimization Savings", "Forecast"],
                    default=["Total Spend", "Cost by Service"]
                )
                
                grouping = st.multiselect(
                    "Group By",
                    ["Service", "Region", "Environment", "Project", "Department", "Owner"],
                    default=["Service"]
                )
            
            with col2:
                format_type = st.selectbox("Report Format", ["PDF", "Excel", "CSV", "PowerPoint"])
                recipients = st.text_area("Email Recipients", "finance@company.com\nexec-team@company.com")
                
                schedule = st.selectbox("Schedule", ["One-time", "Daily", "Weekly", "Monthly"])
                
                if schedule != "One-time":
                    schedule_day = st.selectbox("Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
                
                if st.button("📊 Generate Report", type="primary"):
                    st.success("✅ Custom report generated")
    
    @staticmethod
    def render_pmo_vs_fmo():
        """PMO vs FMO Analysis"""
        st.markdown("## 🏢 PMO vs FMO - Project vs Financial Perspective")
        
        demo_mode = st.session_state.get('demo_mode', True)
        
        st.info("🔄 Compare project management (PMO) and financial management (FMO) views of cloud spend")
        
        # Overview
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 PMO Perspective")
            st.markdown("""
            **Focus: Project Delivery & Resource Utilization**
            
            - Track costs by project/workstream
            - Monitor resource allocation
            - Sprint/iteration cost tracking
            - Delivery milestone costs
            - Team velocity vs spend
            - Feature/epic cost attribution
            """)
            
            pmo_metrics = {
                "Metric": ["Active Projects", "Avg Project Cost", "On-Budget Projects", "Resource Utilization", "Velocity Score"],
                "Value": ["18", "$13,031/mo", "14 (78%)", "87%", "8.5/10"]
            }
            st.dataframe(pd.DataFrame(pmo_metrics), use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("### 💰 FMO Perspective")
            st.markdown("""
            **Focus: Financial Planning & Cost Control**
            
            - Budget tracking & forecasting
            - Cost center allocation
            - ROI & financial metrics
            - Chargeback/showback
            - Variance analysis
            - Financial compliance
            """)
            
            fmo_metrics = {
                "Metric": ["Total Budget", "Actual Spend", "Variance", "Budget Utilization", "Forecast Accuracy"],
                "Value": ["$300,000", "$234,567", "+$65,433", "78%", "98.2%"]
            }
            st.dataframe(pd.DataFrame(fmo_metrics), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Comparative Analysis
        st.markdown("### 🔄 PMO vs FMO Comparative View")
        
        tab1, tab2, tab3 = st.tabs(["Project Analysis", "Cost Attribution", "Alignment Dashboard"])
        
        with tab1:
            st.markdown("#### Project-Level Analysis")
            
            projects = [
                {
                    "Project": "Mobile App Rewrite",
                    "PMO View": "On Track",
                    "PMO Cost": "$67,890",
                    "PMO Status": "87% complete, $2.1K under",
                    "FMO View": "Within Budget",
                    "FMO Cost": "$67,890",
                    "FMO Status": "97% budget utilized",
                    "Alignment": "✅ Aligned"
                },
                {
                    "Project": "Customer Portal",
                    "PMO View": "At Risk",
                    "PMO Cost": "$43,210",
                    "PMO Status": "Behind schedule, need +$5K",
                    "FMO View": "Over Budget",
                    "FMO Cost": "$43,210",
                    "FMO Status": "108% budget utilized",
                    "Alignment": "⚠️ Misaligned"
                },
                {
                    "Project": "ML Pipeline",
                    "PMO View": "On Track",
                    "PMO Cost": "$38,650",
                    "PMO Status": "Ahead of schedule",
                    "FMO View": "Under Budget",
                    "FMO Cost": "$38,650",
                    "FMO Status": "86% budget utilized",
                    "Alignment": "✅ Aligned"
                }
            ]
            st.dataframe(pd.DataFrame(projects), use_container_width=True, hide_index=True)
        
        with tab2:
            st.markdown("#### Cost Attribution Methodology")
            
            attribution = [
                {"Method": "Direct Tagging", "PMO Use": "Primary", "FMO Use": "Primary", "Coverage": "94%", "Accuracy": "High"},
                {"Method": "Resource Allocation", "PMO Use": "Secondary", "FMO Use": "Low", "Coverage": "87%", "Accuracy": "Medium"},
                {"Method": "Time-based Split", "PMO Use": "Occasional", "FMO Use": "Secondary", "Coverage": "100%", "Accuracy": "Medium"},
                {"Method": "Cost Center Mapping", "PMO Use": "Low", "FMO Use": "Primary", "Coverage": "100%", "Accuracy": "High"}
            ]
            st.dataframe(pd.DataFrame(attribution), use_container_width=True, hide_index=True)
        
        with tab3:
            st.markdown("#### PMO-FMO Alignment Dashboard")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Aligned Projects", "14/18", "78%")
            with col2:
                st.metric("Cost Discrepancies", "4", "-2")
            with col3:
                st.metric("Data Quality", "94%", "+3%")
            
            st.markdown("---")
            
            st.markdown("**Key Alignment Issues:**")
            issues = [
                {"Issue": "Customer Portal budget overrun", "PMO Impact": "Need scope reduction", "FMO Impact": "Budget reallocation required", "Resolution": "🔄 In Progress"},
                {"Issue": "Untagged infrastructure costs", "PMO Impact": "Can't attribute to projects", "FMO Impact": "Department allocation unclear", "Resolution": "✅ Auto-tagging deployed"},
                {"Issue": "Shared service allocation", "PMO Impact": "Project cost inflation", "FMO Impact": "Complex chargeback rules", "Resolution": "📋 Policy review needed"}
            ]
            st.dataframe(pd.DataFrame(issues), use_container_width=True, hide_index=True)
    
    @staticmethod
    def render_ri_recommendations():
        """Reserved Instance Recommendations"""
        st.markdown("## 🎟️ Reserved Instance & Savings Plans Recommendations")
        
        demo_mode = st.session_state.get('demo_mode', True)
        
        st.info("💡 AI-powered recommendations for Reserved Instances and Savings Plans to maximize savings")
        
        # RI/SP Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Current RI Coverage", "67%", "+5%")
        with col2:
            st.metric("Potential Savings", "$8,760/mo", "")
        with col3:
            st.metric("Recommendation Confidence", "92%", "+3%")
        with col4:
            st.metric("Active RIs", "45", "+3")
        
        st.markdown("---")
        
        # Top Recommendations
        st.markdown("### 🎯 Top RI/SP Recommendations")
        
        recommendations = [
            {
                "Rank": 1,
                "Type": "EC2 RI",
                "Instance Type": "m5.2xlarge",
                "Quantity": "12",
                "Term": "1-Year No Upfront",
                "Region": "us-east-1",
                "Monthly Savings": "$2,340",
                "Annual Savings": "$28,080",
                "Utilization": "98%",
                "Confidence": "High",
                "Payback": "4 months"
            },
            {
                "Rank": 2,
                "Type": "RDS RI",
                "Instance Type": "db.r5.xlarge",
                "Quantity": "6",
                "Term": "3-Year Partial Upfront",
                "Region": "us-east-1",
                "Monthly Savings": "$1,890",
                "Annual Savings": "$22,680",
                "Utilization": "95%",
                "Confidence": "High",
                "Payback": "3 months"
            },
            {
                "Rank": 3,
                "Type": "Compute SP",
                "Instance Type": "Flexible",
                "Quantity": "100 $/hour commitment",
                "Term": "1-Year No Upfront",
                "Region": "All",
                "Monthly Savings": "$1,450",
                "Annual Savings": "$17,400",
                "Utilization": "92%",
                "Confidence": "Medium",
                "Payback": "2 months"
            },
            {
                "Rank": 4,
                "Type": "EC2 RI",
                "Instance Type": "c5.xlarge",
                "Quantity": "8",
                "Term": "1-Year Partial Upfront",
                "Region": "us-west-2",
                "Monthly Savings": "$980",
                "Annual Savings": "$11,760",
                "Utilization": "89%",
                "Confidence": "Medium",
                "Payback": "5 months"
            }
        ]
        st.dataframe(pd.DataFrame(recommendations), use_container_width=True, hide_index=True)
        
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("📊 Purchase RIs", type="primary"):
                st.info("Redirecting to AWS Console...")
        
        st.markdown("---")
        
        # Current RI Inventory
        st.markdown("### 📋 Current RI & SP Inventory")
        
        tab1, tab2, tab3 = st.tabs(["Active RIs", "Savings Plans", "Expiring Soon"])
        
        with tab1:
            active_ris = [
                {"Instance Type": "m5.large", "Count": "15", "Region": "us-east-1", "Term": "1-Year", "Expires": "2025-03-15", "Utilization": "97%", "Savings": "$1,234/mo"},
                {"Instance Type": "r5.xlarge", "Count": "8", "Region": "us-east-1", "Term": "3-Year", "Expires": "2026-08-22", "Utilization": "94%", "Savings": "$890/mo"},
                {"Instance Type": "c5.2xlarge", "Count": "12", "Region": "us-west-2", "Term": "1-Year", "Expires": "2025-01-10", "Utilization": "89%", "Savings": "$1,567/mo"},
                {"Instance Type": "db.r5.large", "Count": "6", "Region": "us-east-1", "Term": "3-Year", "Expires": "2027-02-18", "Utilization": "98%", "Savings": "$678/mo"}
            ]
            st.dataframe(pd.DataFrame(active_ris), use_container_width=True, hide_index=True)
        
        with tab2:
            savings_plans = [
                {"Type": "Compute SP", "Commitment": "$50/hour", "Region": "All", "Term": "1-Year", "Expires": "2025-06-30", "Utilization": "92%", "Savings": "$2,340/mo"},
                {"Type": "EC2 Instance SP", "Commitment": "$30/hour", "Region": "us-east-1", "Term": "3-Year", "Expires": "2026-12-15", "Utilization": "88%", "Savings": "$1,450/mo"}
            ]
            st.dataframe(pd.DataFrame(savings_plans), use_container_width=True, hide_index=True)
        
        with tab3:
            expiring = [
                {"Type": "EC2 RI", "Instance": "c5.2xlarge", "Count": "12", "Expires": "2025-01-10", "Days Left": "53", "Action": "⚠️ Renew or Replace", "Recommendation": "Replace with Compute SP"},
                {"Type": "EC2 RI", "Instance": "m5.large", "Count": "15", "Expires": "2025-03-15", "Days Left": "117", "Action": "✅ Auto-renew enabled", "Recommendation": "Keep current"},
                {"Type": "RDS RI", "Instance": "db.m5.xlarge", "Count": "4", "Expires": "2025-02-28", "Days Left": "102", "Action": "🔄 Review needed", "Recommendation": "Downsize to db.m5.large"}
            ]
            st.dataframe(pd.DataFrame(expiring), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # RI Analysis Tools
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Utilization Analysis")
            
            utilization = [
                {"Category": "High Utilization (>90%)", "Count": 28, "Percentage": "62%", "Status": "✅ Optimal"},
                {"Category": "Good Utilization (75-90%)", "Count": 12, "Percentage": "27%", "Status": "✅ Acceptable"},
                {"Category": "Low Utilization (<75%)", "Count": 5, "Percentage": "11%", "Status": "⚠️ Review needed"}
            ]
            st.dataframe(pd.DataFrame(utilization), use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("### 💰 Savings Summary")
            
            savings = [
                {"Category": "EC2 RIs", "Monthly": "$4,234", "Annual": "$50,808", "Percentage": "48%"},
                {"Category": "RDS RIs", "Monthly": "$1,567", "Annual": "$18,804", "Percentage": "18%"},
                {"Category": "Compute SP", "Monthly": "$2,340", "Annual": "$28,080", "Percentage": "27%"},
                {"Category": "EC2 Instance SP", "Monthly": "$619", "Annual": "$7,428", "Percentage": "7%"}
            ]
            st.dataframe(pd.DataFrame(savings), use_container_width=True, hide_index=True)
            
            st.metric("Total RI/SP Savings", "$8,760/mo", "$105,120/year")
    
    @staticmethod
    def render_use_case_tracking():
        """Use Case Tracking"""
        st.markdown("## 📝 Use Case Tracking & Cost Attribution")
        
        demo_mode = st.session_state.get('demo_mode', True)
        
        st.info("🎯 Track cloud costs by business use cases, features, and workloads")
        
        # Use Case Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Active Use Cases", "34", "+4")
        with col2:
            st.metric("Tracked Resources", "1,234", "+89")
        with col3:
            st.metric("Attribution Coverage", "91%", "+6%")
        with col4:
            st.metric("Avg Cost/Use Case", "$6,899", "-8%")
        
        st.markdown("---")
        
        # Use Case Catalog
        st.markdown("### 📚 Use Case Catalog")
        
        tab1, tab2, tab3 = st.tabs(["By Category", "By Cost", "By Business Value"])
        
        with tab1:
            st.markdown("#### Use Cases by Category")
            
            categories = [
                {
                    "Category": "Customer-Facing",
                    "Use Cases": 12,
                    "Resources": 456,
                    "Monthly Cost": "$98,760",
                    "% of Total": "42%",
                    "Top Use Case": "Mobile App Backend",
                    "Business Value": "High"
                },
                {
                    "Category": "Data & Analytics",
                    "Use Cases": 8,
                    "Resources": 234,
                    "Monthly Cost": "$56,890",
                    "% of Total": "24%",
                    "Top Use Case": "Customer Analytics Pipeline",
                    "Business Value": "High"
                },
                {
                    "Category": "Internal Tools",
                    "Use Cases": 9,
                    "Resources": 312,
                    "Monthly Cost": "$45,670",
                    "% of Total": "19%",
                    "Top Use Case": "HR Management System",
                    "Business Value": "Medium"
                },
                {
                    "Category": "Development & Testing",
                    "Use Cases": 5,
                    "Resources": 232,
                    "Monthly Cost": "$33,247",
                    "% of Total": "14%",
                    "Top Use Case": "CI/CD Infrastructure",
                    "Business Value": "Medium"
                }
            ]
            st.dataframe(pd.DataFrame(categories), use_container_width=True, hide_index=True)
        
        with tab2:
            st.markdown("#### Top 10 Use Cases by Cost")
            
            use_cases = [
                {"Rank": 1, "Use Case": "Mobile App Backend", "Category": "Customer-Facing", "Cost": "$34,560/mo", "Resources": 156, "Business Owner": "Product", "ROI": "High"},
                {"Rank": 2, "Use Case": "Customer Analytics Pipeline", "Category": "Data & Analytics", "Cost": "$28,900/mo", "Resources": 89, "Business Owner": "Data Team", "ROI": "High"},
                {"Rank": 3, "Use Case": "E-commerce Platform", "Category": "Customer-Facing", "Cost": "$23,450/mo", "Resources": 134, "Business Owner": "Engineering", "ROI": "High"},
                {"Rank": 4, "Use Case": "ML Recommendation Engine", "Category": "Data & Analytics", "Cost": "$18,760/mo", "Resources": 67, "Business Owner": "AI/ML", "ROI": "Medium"},
                {"Rank": 5, "Use Case": "Video Processing Pipeline", "Category": "Customer-Facing", "Cost": "$15,670/mo", "Resources": 45, "Business Owner": "Media Team", "ROI": "Medium"}
            ]
            st.dataframe(pd.DataFrame(use_cases), use_container_width=True, hide_index=True)
        
        with tab3:
            st.markdown("#### Use Cases by Business Value")
            
            value_analysis = [
                {
                    "Use Case": "Mobile App Backend",
                    "Monthly Cost": "$34,560",
                    "Revenue Impact": "$450,000/mo",
                    "ROI": "13:1",
                    "Business Value": "🟢 High",
                    "Cost Trend": "📊 Stable",
                    "Status": "✅ Optimized"
                },
                {
                    "Use Case": "Customer Analytics",
                    "Monthly Cost": "$28,900",
                    "Revenue Impact": "$280,000/mo",
                    "ROI": "10:1",
                    "Business Value": "🟢 High",
                    "Cost Trend": "📈 +12%",
                    "Status": "⚠️ Review needed"
                },
                {
                    "Use Case": "HR Management System",
                    "Monthly Cost": "$12,340",
                    "Revenue Impact": "Cost savings: $45K/mo",
                    "ROI": "4:1",
                    "Business Value": "🟡 Medium",
                    "Cost Trend": "📉 -5%",
                    "Status": "✅ Optimized"
                }
            ]
            st.dataframe(pd.DataFrame(value_analysis), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Create/Edit Use Case
        st.markdown("### ➕ Create/Edit Use Case")
        
        col1, col2 = st.columns(2)
        
        with col1:
            use_case_name = st.text_input("Use Case Name", "Customer Notification Service")
            category = st.selectbox("Category", ["Customer-Facing", "Data & Analytics", "Internal Tools", "Development & Testing", "Infrastructure"])
            business_owner = st.selectbox("Business Owner", ["Engineering", "Product", "Data Team", "DevOps", "Marketing"])
            
            st.markdown("#### Resource Tagging Rules")
            tag_rules = st.text_area(
                "Tag Matching Rules",
                "UseCase=customer-notifications\nProject=notifications",
                height=100
            )
        
        with col2:
            business_value = st.select_slider("Business Value", options=["Low", "Medium", "High", "Critical"], value="High")
            revenue_impact = st.text_input("Monthly Revenue/Savings Impact", "$125,000")
            
            st.markdown("#### Cost Allocation")
            allocation_method = st.selectbox("Method", ["Direct Tagging", "Resource ID", "Proportional Split"])
            
            expected_monthly_cost = st.number_input("Expected Monthly Cost ($)", min_value=0, value=8500)
            
            if st.button("💾 Save Use Case", type="primary"):
                st.success("✅ Use case created successfully")
        
        st.markdown("---")
        
        # Use Case Performance
        st.markdown("### 📊 Use Case Performance Dashboard")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Cost Efficiency Metrics")
            
            efficiency = [
                {"Use Case": "Mobile App Backend", "Cost/Request": "$0.0012", "Cost/User": "$2.34", "Efficiency": "✅ Excellent"},
                {"Use Case": "E-commerce Platform", "Cost/Transaction": "$0.034", "Cost/User": "$4.56", "Efficiency": "✅ Good"},
                {"Use Case": "Video Processing", "Cost/Video": "$0.23", "Cost/Minute": "$0.045", "Efficiency": "⚠️ Review"}
            ]
            st.dataframe(pd.DataFrame(efficiency), use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("#### Resource Utilization")
            
            utilization = [
                {"Use Case": "Mobile App Backend", "Avg CPU": "68%", "Avg Memory": "72%", "Status": "✅ Optimal"},
                {"Use Case": "E-commerce Platform", "Avg CPU": "45%", "Avg Memory": "38%", "Status": "⚠️ Over-provisioned"},
                {"Use Case": "ML Training Pipeline", "Avg CPU": "92%", "Avg Memory": "88%", "Status": "✅ Well-utilized"}
            ]
            st.dataframe(pd.DataFrame(utilization), use_container_width=True, hide_index=True)
