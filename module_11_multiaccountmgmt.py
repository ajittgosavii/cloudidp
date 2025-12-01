"""
Module: Multi-Account Management & AWS Organizations
Enterprise multi-account governance with SSO, CMDB, and account lifecycle management
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json

class MultiAccountManagementModule:
    """Multi-Account & AWS Organizations Management"""
    
    def __init__(self):
        self.module_name = "Multi-Account Management"
        self.version = "2.0.0"
        
    def render(self):
        """Main render method"""
        st.header("🏢 Multi-Account Management & AWS Organizations")
        
        # Mode indicator
        mode_color = "#28a745" if st.session_state.get('mode', 'Demo') == 'Live' else "#ffc107"
        mode_text = "🟢 Live Mode" if st.session_state.get('mode', 'Demo') == 'Live' else "📊 Demo Mode"
        st.markdown(f'<div style="background-color: {mode_color}; color: white; padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 20px;"><b>{mode_text}</b></div>', unsafe_allow_html=True)
        
        st.markdown("**🌐 Multi-Account Governance | AWS Organizations | SSO Integration | CMDB**")
        
        # Organization overview metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("AWS Accounts", "47", "+2", help="Total AWS accounts in organization")
        with col2:
            st.metric("Active Regions", "12", help="Regions with active resources")
        with col3:
            st.metric("Total Resources", "3,456", "+89", help="Resources across all accounts")
        with col4:
            st.metric("Pending Requests", "3", help="Account requests awaiting approval")
        with col5:
            st.metric("Monthly Cost", "$125K", "+$8K", help="Organization-wide cost")
        
        st.markdown("---")
        
        # Main tabs
        tabs = st.tabs([
            "🏢 Account Directory",
            "➕ Account Onboarding",
            "🔐 Cross-Account Access",
            "📊 CMDB & Inventory",
            "⚙️ Organization Settings"
        ])
        
        with tabs[0]:
            self.account_directory()
        with tabs[1]:
            self.account_onboarding()
        with tabs[2]:
            self.cross_account_access()
        with tabs[3]:
            self.cmdb_inventory()
        with tabs[4]:
            self.organization_settings()
    
    def account_directory(self):
        """AWS Accounts directory with multi-account selector"""
        st.subheader("🏢 AWS Account Directory")
        st.markdown("**View and manage all AWS accounts in your organization**")
        
        # Account selector for operations
        st.markdown("### 🎯 Quick Account & Region Selector")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Multi-account selector
            accounts = [
                "Production (123456789012)",
                "Staging (234567890123)",
                "Development (345678901234)",
                "Data Analytics (456789012345)",
                "Security (567890123456)",
                "Shared Services (678901234567)"
            ]
            selected_accounts = st.multiselect(
                "Select AWS Account(s)",
                accounts,
                default=[accounts[0]],
                help="Select one or more AWS accounts to operate on"
            )
        
        with col2:
            # Multi-region selector
            regions = [
                "us-east-1 (N. Virginia)",
                "us-west-2 (Oregon)",
                "eu-west-1 (Ireland)",
                "eu-central-1 (Frankfurt)",
                "ap-southeast-1 (Singapore)",
                "ap-northeast-1 (Tokyo)"
            ]
            selected_regions = st.multiselect(
                "Select AWS Region(s)",
                regions,
                default=[regions[0]],
                help="Select one or more AWS regions"
            )
        
        with col3:
            st.markdown("**Current Selection**")
            st.info(f"✅ {len(selected_accounts)} account(s)\n✅ {len(selected_regions)} region(s)")
            if st.button("🔄 Switch Context", type="primary", use_container_width=True):
                st.success(f"Context switched to {len(selected_accounts)} account(s) in {len(selected_regions)} region(s)")
        
        st.markdown("---")
        
        # Organization structure
        st.markdown("### 🌳 Organization Structure")
        
        # OU filter
        col1, col2 = st.columns([3, 1])
        with col1:
            search = st.text_input("🔍 Search accounts", placeholder="Search by name, ID, or tag...")
        with col2:
            ou_filter = st.selectbox("Filter by OU", ["All", "Production", "Non-Production", "Workloads", "Security", "Infrastructure"])
        
        # Accounts table with status
        accounts_data = pd.DataFrame([
            {
                "Account ID": "123456789012",
                "Account Name": "Production",
                "OU": "Production",
                "Status": "🟢 Active",
                "Email": "aws-prod@company.com",
                "Created": "2023-01-15",
                "Resources": "1,234",
                "Monthly Cost": "$45,000",
                "SSO Access": "✅ Enabled"
            },
            {
                "Account ID": "234567890123",
                "Account Name": "Staging",
                "OU": "Non-Production",
                "Status": "🟢 Active",
                "Email": "aws-staging@company.com",
                "Created": "2023-02-10",
                "Resources": "567",
                "Monthly Cost": "$18,500",
                "SSO Access": "✅ Enabled"
            },
            {
                "Account ID": "345678901234",
                "Account Name": "Development",
                "OU": "Non-Production",
                "Status": "🟢 Active",
                "Email": "aws-dev@company.com",
                "Created": "2023-03-05",
                "Resources": "892",
                "Monthly Cost": "$12,300",
                "SSO Access": "✅ Enabled"
            },
            {
                "Account ID": "456789012345",
                "Account Name": "Data Analytics",
                "OU": "Workloads",
                "Status": "🟢 Active",
                "Email": "aws-data@company.com",
                "Created": "2023-06-20",
                "Resources": "445",
                "Monthly Cost": "$32,100",
                "SSO Access": "✅ Enabled"
            },
            {
                "Account ID": "567890123456",
                "Account Name": "Security",
                "OU": "Security",
                "Status": "🟢 Active",
                "Email": "aws-security@company.com",
                "Created": "2023-01-10",
                "Resources": "156",
                "Monthly Cost": "$8,900",
                "SSO Access": "✅ Enabled"
            },
            {
                "Account ID": "678901234567",
                "Account Name": "Shared Services",
                "OU": "Infrastructure",
                "Status": "🟢 Active",
                "Email": "aws-shared@company.com",
                "Created": "2023-01-10",
                "Resources": "234",
                "Monthly Cost": "$15,200",
                "SSO Access": "✅ Enabled"
            },
            {
                "Account ID": "789012345678",
                "Account Name": "Legacy Application",
                "OU": "Workloads",
                "Status": "🟡 Suspended",
                "Email": "aws-legacy@company.com",
                "Created": "2022-08-15",
                "Resources": "89",
                "Monthly Cost": "$2,400",
                "SSO Access": "❌ Disabled"
            },
            {
                "Account ID": "890123456789",
                "Account Name": "Sandbox-Team-A",
                "OU": "Non-Production",
                "Status": "🟢 Active",
                "Email": "aws-sandbox-a@company.com",
                "Created": "2024-11-15",
                "Resources": "45",
                "Monthly Cost": "$890",
                "SSO Access": "✅ Enabled"
            },
        ])
        
        st.dataframe(accounts_data, use_container_width=True, hide_index=True)
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("📊 View Account Details", use_container_width=True):
                st.info("Opening account details dashboard...")
        with col2:
            if st.button("🔐 Configure SSO Access", use_container_width=True):
                st.info("Opening SSO configuration...")
        with col3:
            if st.button("💰 Cost Breakdown", use_container_width=True):
                st.info("Opening cost analysis...")
        with col4:
            if st.button("🏷️ Manage Tags", use_container_width=True):
                st.info("Opening tag editor...")
    
    def account_onboarding(self):
        """Account onboarding and offboarding with approval workflow"""
        st.subheader("➕ AWS Account Onboarding & Lifecycle Management")
        st.markdown("**Request new AWS accounts with automated approval workflow**")
        
        # Workflow tabs
        workflow_tabs = st.tabs([
            "📝 New Account Request",
            "✅ Pending Approvals",
            "📋 Request History",
            "🗑️ Account Offboarding"
        ])
        
        with workflow_tabs[0]:
            self.render_account_request_form()
        
        with workflow_tabs[1]:
            self.render_pending_approvals()
        
        with workflow_tabs[2]:
            self.render_request_history()
        
        with workflow_tabs[3]:
            self.render_account_offboarding()
    
    def render_account_request_form(self):
        """Form to request a new AWS account"""
        st.markdown("### 📝 Request New AWS Account")
        
        with st.form("account_request"):
            st.markdown("#### Account Details")
            col1, col2 = st.columns(2)
            
            with col1:
                account_name = st.text_input(
                    "Account Name *",
                    placeholder="e.g., ML-Training-Production",
                    help="Descriptive name for the AWS account"
                )
                
                account_purpose = st.selectbox(
                    "Account Purpose *",
                    ["Production Workload", "Non-Production Workload", "Development/Testing", 
                     "Data & Analytics", "Security/Audit", "Sandbox", "Shared Services", "DR/Backup"]
                )
                
                organizational_unit = st.selectbox(
                    "Organizational Unit (OU) *",
                    ["Production", "Non-Production", "Workloads", "Security", "Infrastructure", "Sandbox"]
                )
            
            with col2:
                owner_email = st.text_input(
                    "Account Owner Email *",
                    placeholder="owner@company.com",
                    help="Email address for the root account"
                )
                
                cost_center = st.text_input(
                    "Cost Center",
                    placeholder="CC-1234",
                    help="Cost center for billing"
                )
                
                expected_monthly_cost = st.number_input(
                    "Expected Monthly Cost (USD)",
                    min_value=0,
                    max_value=1000000,
                    value=5000,
                    step=100
                )
            
            st.markdown("#### Configuration Options")
            
            col1, col2 = st.columns(2)
            with col1:
                enable_sso = st.checkbox("Enable AWS SSO Access", value=True)
                enable_cloudtrail = st.checkbox("Enable CloudTrail", value=True)
                enable_config = st.checkbox("Enable AWS Config", value=True)
            
            with col2:
                enable_guardduty = st.checkbox("Enable GuardDuty", value=True)
                enable_security_hub = st.checkbox("Enable Security Hub", value=True)
                enable_vpc_flow_logs = st.checkbox("Enable VPC Flow Logs", value=True)
            
            st.markdown("#### Baseline Configuration")
            
            baseline_config = st.multiselect(
                "Apply Baseline Configurations",
                ["Standard VPC Setup", "IAM Password Policy", "S3 Block Public Access", 
                 "EBS Encryption", "Required Tags", "Budget Alerts", "Backup Policy"],
                default=["Standard VPC Setup", "IAM Password Policy", "S3 Block Public Access"]
            )
            
            st.markdown("#### Access & Permissions")
            
            col1, col2 = st.columns(2)
            with col1:
                admin_users = st.text_area(
                    "Administrator Users (emails, one per line)",
                    placeholder="admin1@company.com\nadmin2@company.com",
                    help="Users who will have administrative access"
                )
            
            with col2:
                readonly_users = st.text_area(
                    "Read-Only Users (emails, one per line)",
                    placeholder="viewer1@company.com\nviewer2@company.com",
                    help="Users who will have read-only access"
                )
            
            st.markdown("#### Business Justification")
            
            justification = st.text_area(
                "Business Justification *",
                placeholder="Explain the business need for this AWS account...",
                height=100,
                help="Required for approval process"
            )
            
            approver = st.selectbox(
                "Select Approver *",
                ["John Smith (Cloud Architect)", "Jane Doe (Security Lead)", "Bob Johnson (FinOps Manager)", "Alice Wong (Director of Engineering)"]
            )
            
            st.markdown("---")
            
            col1, col2, col3 = st.columns([2, 1, 1])
            with col2:
                if st.form_submit_button("📤 Submit Request", type="primary", use_container_width=True):
                    if account_name and account_purpose and owner_email and justification:
                        st.success(f"✅ Account request submitted successfully!")
                        st.info(f"📧 Approval email sent to {approver}")
                        st.balloons()
                        
                        # Show request details
                        st.markdown("### 📋 Request Summary")
                        st.json({
                            "request_id": "REQ-2024-0042",
                            "account_name": account_name,
                            "purpose": account_purpose,
                            "ou": organizational_unit,
                            "owner": owner_email,
                            "approver": approver,
                            "status": "Pending Approval",
                            "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                    else:
                        st.error("❌ Please fill in all required fields marked with *")
            
            with col3:
                if st.form_submit_button("❌ Cancel", use_container_width=True):
                    st.info("Request cancelled")
    
    def render_pending_approvals(self):
        """Show pending account requests for approval"""
        st.markdown("### ✅ Pending Account Requests")
        
        # Check if user is an approver
        user_role = st.selectbox("Your Role", ["Approver", "Requester", "Viewer"])
        
        if user_role == "Approver":
            st.info("🔔 You have 3 pending account requests to review")
            
            pending_requests = pd.DataFrame([
                {
                    "Request ID": "REQ-2024-0042",
                    "Account Name": "ML-Training-Production",
                    "Purpose": "Production Workload",
                    "OU": "Production",
                    "Requester": "john.doe@company.com",
                    "Cost Center": "CC-ML-001",
                    "Est. Monthly Cost": "$15,000",
                    "Submitted": "2024-11-28 14:30",
                    "Status": "⏳ Awaiting Approval"
                },
                {
                    "Request ID": "REQ-2024-0041",
                    "Account Name": "Data-Lake-Analytics",
                    "Purpose": "Data & Analytics",
                    "OU": "Workloads",
                    "Requester": "jane.smith@company.com",
                    "Cost Center": "CC-DATA-005",
                    "Est. Monthly Cost": "$8,500",
                    "Submitted": "2024-11-27 10:15",
                    "Status": "⏳ Awaiting Approval"
                },
                {
                    "Request ID": "REQ-2024-0040",
                    "Account Name": "Sandbox-Team-B",
                    "Purpose": "Sandbox",
                    "OU": "Sandbox",
                    "Requester": "bob.jones@company.com",
                    "Cost Center": "CC-ENG-012",
                    "Est. Monthly Cost": "$1,200",
                    "Submitted": "2024-11-26 16:45",
                    "Status": "⏳ Awaiting Approval"
                }
            ])
            
            st.dataframe(pending_requests, use_container_width=True, hide_index=True)
            
            # Approval interface
            st.markdown("---")
            st.markdown("### 📝 Review Request")
            
            selected_request = st.selectbox(
                "Select Request to Review",
                ["REQ-2024-0042 (ML-Training-Production)", "REQ-2024-0041 (Data-Lake-Analytics)", "REQ-2024-0040 (Sandbox-Team-B)"]
            )
            
            # Show request details
            with st.expander("📋 Request Details", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Account Name:** ML-Training-Production")
                    st.markdown("**Purpose:** Production Workload")
                    st.markdown("**OU:** Production")
                    st.markdown("**Owner Email:** john.doe@company.com")
                    st.markdown("**Cost Center:** CC-ML-001")
                
                with col2:
                    st.markdown("**Expected Monthly Cost:** $15,000")
                    st.markdown("**SSO Enabled:** ✅ Yes")
                    st.markdown("**Security Services:** GuardDuty, Security Hub, Config")
                    st.markdown("**Baseline Configs:** Standard VPC, IAM Policy, Encryption")
                
                st.markdown("**Business Justification:**")
                st.info("We need a dedicated AWS account for our ML training pipelines in production. This will isolate ML workloads from other production services and allow us to apply ML-specific cost controls and security policies.")
            
            # Approval decision
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                approval_comments = st.text_area(
                    "Approval Comments (optional)",
                    placeholder="Add comments about your decision...",
                    height=100
                )
            
            with col2:
                if st.button("✅ Approve", type="primary", use_container_width=True):
                    st.success("✅ Request REQ-2024-0042 approved!")
                    st.info("🔄 Account creation initiated. Estimated completion: 10-15 minutes")
                    st.balloons()
            
            with col3:
                if st.button("❌ Reject", use_container_width=True):
                    st.error("❌ Request rejected")
                    st.info("📧 Rejection notification sent to requester")
        
        else:
            st.info("ℹ️ You don't have approval permissions. Contact your administrator.")
    
    def render_request_history(self):
        """Show historical account requests"""
        st.markdown("### 📋 Account Request History")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.selectbox("Status", ["All", "Approved", "Rejected", "Pending", "Provisioned"])
        with col2:
            date_range = st.selectbox("Date Range", ["Last 7 Days", "Last 30 Days", "Last 90 Days", "All Time"])
        with col3:
            requester_filter = st.text_input("Filter by Requester", placeholder="email@company.com")
        
        # Historical requests
        history_data = pd.DataFrame([
            {
                "Request ID": "REQ-2024-0042",
                "Account Name": "ML-Training-Production",
                "Requester": "john.doe@company.com",
                "Status": "⏳ Pending Approval",
                "Submitted": "2024-11-28",
                "Approved By": "-",
                "Provisioned": "-"
            },
            {
                "Request ID": "REQ-2024-0039",
                "Account Name": "Sandbox-Team-A",
                "Requester": "alice.wong@company.com",
                "Status": "✅ Provisioned",
                "Submitted": "2024-11-15",
                "Approved By": "Jane Doe",
                "Provisioned": "2024-11-15"
            },
            {
                "Request ID": "REQ-2024-0038",
                "Account Name": "IoT-Data-Processing",
                "Requester": "bob.jones@company.com",
                "Status": "✅ Provisioned",
                "Submitted": "2024-11-10",
                "Approved By": "John Smith",
                "Provisioned": "2024-11-10"
            },
            {
                "Request ID": "REQ-2024-0037",
                "Account Name": "Test-Account-XYZ",
                "Requester": "charlie.brown@company.com",
                "Status": "❌ Rejected",
                "Submitted": "2024-11-08",
                "Approved By": "Bob Johnson",
                "Provisioned": "-"
            },
            {
                "Request ID": "REQ-2024-0036",
                "Account Name": "Legacy-Migration",
                "Requester": "david.miller@company.com",
                "Status": "✅ Provisioned",
                "Submitted": "2024-11-01",
                "Approved By": "Alice Wong",
                "Provisioned": "2024-11-01"
            },
        ])
        
        st.dataframe(history_data, use_container_width=True, hide_index=True)
        
        # Statistics
        st.markdown("---")
        st.markdown("### 📊 Request Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Requests", "127")
        with col2:
            st.metric("Approved", "98", help="77% approval rate")
        with col3:
            st.metric("Rejected", "24", help="19% rejection rate")
        with col4:
            st.metric("Pending", "5", help="4% pending")
    
    def render_account_offboarding(self):
        """Account decommissioning and offboarding"""
        st.markdown("### 🗑️ Account Offboarding & Decommissioning")
        st.markdown("**Safely decommission and close AWS accounts**")
        
        st.warning("⚠️ **Important:** Account offboarding is irreversible. Ensure all data is backed up and resources are properly migrated.")
        
        with st.form("offboard_account"):
            st.markdown("#### Select Account to Offboard")
            
            account_to_offboard = st.selectbox(
                "AWS Account",
                ["Legacy Application (789012345678)", "Old-Sandbox-1 (890123456789)", "Deprecated-API (901234567890)"]
            )
            
            st.markdown("#### Pre-Offboarding Checklist")
            
            col1, col2 = st.columns(2)
            with col1:
                data_backed_up = st.checkbox("✅ All data backed up")
                resources_migrated = st.checkbox("✅ Resources migrated/terminated")
                users_notified = st.checkbox("✅ Users notified")
            
            with col2:
                billing_reviewed = st.checkbox("✅ Final billing reviewed")
                compliance_checked = st.checkbox("✅ Compliance requirements met")
                security_audit = st.checkbox("✅ Security audit completed")
            
            st.markdown("#### Offboarding Options")
            
            offboard_action = st.radio(
                "Action",
                ["Suspend Account (Reversible)", "Close Account (Permanent)"],
                help="Suspend keeps the account but disables access. Close permanently removes the account."
            )
            
            reason = st.text_area(
                "Reason for Offboarding *",
                placeholder="Explain why this account is being offboarded...",
                height=100
            )
            
            approver = st.selectbox(
                "Approval Required From",
                ["Alice Wong (Director of Engineering)", "Bob Johnson (FinOps Manager)", "Jane Doe (Security Lead)"]
            )
            
            col1, col2, col3 = st.columns([2, 1, 1])
            with col2:
                if st.form_submit_button("📤 Submit Offboarding Request", type="primary", use_container_width=True):
                    all_checks = data_backed_up and resources_migrated and users_notified and billing_reviewed and compliance_checked and security_audit
                    
                    if all_checks and reason:
                        st.success("✅ Offboarding request submitted successfully!")
                        st.info(f"📧 Approval request sent to {approver}")
                        st.warning("⏳ Account will be offboarded upon approval")
                    elif not all_checks:
                        st.error("❌ Please complete all checklist items before proceeding")
                    else:
                        st.error("❌ Please provide a reason for offboarding")
            
            with col3:
                if st.form_submit_button("❌ Cancel", use_container_width=True):
                    st.info("Offboarding request cancelled")
    
    def cross_account_access(self):
        """Cross-account access management with SSO"""
        st.subheader("🔐 Cross-Account Access & SSO Management")
        st.markdown("**Configure IAM roles and AWS SSO for cross-account access**")
        
        # Access tabs
        access_tabs = st.tabs([
            "👥 SSO Configuration",
            "🔑 IAM Roles",
            "📋 Access Requests",
            "🔍 Access Audit"
        ])
        
        with access_tabs[0]:
            self.render_sso_configuration()
        
        with access_tabs[1]:
            self.render_iam_roles()
        
        with access_tabs[2]:
            self.render_access_requests()
        
        with access_tabs[3]:
            self.render_access_audit()
    
    def render_sso_configuration(self):
        """AWS SSO configuration"""
        st.markdown("### 👥 AWS IAM Identity Center (SSO) Configuration")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("SSO Users", "156", "+5")
        with col2:
            st.metric("Permission Sets", "12")
        with col3:
            st.metric("Active Sessions", "47")
        
        st.markdown("---")
        st.markdown("### 📋 Permission Sets")
        
        permission_sets = pd.DataFrame([
            {
                "Name": "AdministratorAccess",
                "Description": "Full administrative access",
                "Accounts": "6 accounts",
                "Users": "8 users",
                "Session Duration": "12 hours",
                "MFA Required": "✅ Yes"
            },
            {
                "Name": "PowerUserAccess",
                "Description": "Full access except IAM",
                "Accounts": "12 accounts",
                "Users": "23 users",
                "Session Duration": "8 hours",
                "MFA Required": "✅ Yes"
            },
            {
                "Name": "ReadOnlyAccess",
                "Description": "Read-only access to all services",
                "Accounts": "47 accounts",
                "Users": "89 users",
                "Session Duration": "4 hours",
                "MFA Required": "❌ No"
            },
            {
                "Name": "DeveloperAccess",
                "Description": "Development and testing permissions",
                "Accounts": "8 accounts",
                "Users": "45 users",
                "Session Duration": "8 hours",
                "MFA Required": "✅ Yes"
            },
            {
                "Name": "DataScientistAccess",
                "Description": "Access to data and ML services",
                "Accounts": "3 accounts",
                "Users": "12 users",
                "Session Duration": "12 hours",
                "MFA Required": "✅ Yes"
            }
        ])
        
        st.dataframe(permission_sets, use_container_width=True, hide_index=True)
        
        st.markdown("### ⚡ Quick Actions")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("➕ Create Permission Set", use_container_width=True, type="primary"):
                st.info("Opening permission set creation wizard...")
        with col2:
            if st.button("👥 Manage User Assignments", use_container_width=True):
                st.info("Opening user assignment manager...")
        with col3:
            if st.button("🔐 Configure MFA", use_container_width=True):
                st.info("Opening MFA configuration...")
    
    def render_iam_roles(self):
        """IAM role management for cross-account access"""
        st.markdown("### 🔑 Cross-Account IAM Roles")
        
        st.info("📘 Cross-account roles allow services and users to assume roles in other AWS accounts")
        
        # Cross-account roles
        roles_data = pd.DataFrame([
            {
                "Role Name": "OrganizationAccountAccessRole",
                "Account": "All accounts",
                "Trusted Entity": "Management Account",
                "Permissions": "AdministratorAccess",
                "Created": "2023-01-10",
                "Last Used": "2 hours ago"
            },
            {
                "Role Name": "DataAnalytics-CrossAccount-Role",
                "Account": "Data Analytics (456789012345)",
                "Trusted Entity": "Production (123456789012)",
                "Permissions": "S3 Read, Athena Query",
                "Created": "2023-06-20",
                "Last Used": "1 day ago"
            },
            {
                "Role Name": "SecurityAudit-ReadOnly-Role",
                "Account": "All accounts",
                "Trusted Entity": "Security (567890123456)",
                "Permissions": "SecurityAudit, ReadOnly",
                "Created": "2023-01-15",
                "Last Used": "3 hours ago"
            },
            {
                "Role Name": "Backup-CrossAccount-Role",
                "Account": "Production (123456789012)",
                "Trusted Entity": "Shared Services (678901234567)",
                "Permissions": "AWS Backup",
                "Created": "2023-04-01",
                "Last Used": "5 hours ago"
            }
        ])
        
        st.dataframe(roles_data, use_container_width=True, hide_index=True)
        
        # Role creation
        st.markdown("---")
        st.markdown("### ➕ Create Cross-Account Role")
        
        with st.expander("Create New Cross-Account Role"):
            col1, col2 = st.columns(2)
            with col1:
                role_name = st.text_input("Role Name", placeholder="e.g., DataAccess-CrossAccount-Role")
                target_account = st.selectbox("Target Account", ["Production", "Staging", "Data Analytics", "Security"])
            
            with col2:
                trusted_account = st.selectbox("Trusted Account/Principal", ["Security Account", "Management Account", "Shared Services"])
                permissions = st.multiselect("Permissions", ["S3 Read/Write", "EC2 Full Access", "RDS Read", "Lambda Invoke", "Custom Policy"])
            
            if st.button("🔑 Create Role", type="primary"):
                st.success(f"✅ Role '{role_name}' created successfully!")
    
    def render_access_requests(self):
        """Access request workflow"""
        st.markdown("### 📋 Cross-Account Access Requests")
        
        # Request form
        with st.form("access_request"):
            st.markdown("#### Request Access to AWS Account")
            
            col1, col2 = st.columns(2)
            with col1:
                target_account = st.selectbox("Target Account", ["Production (123456789012)", "Data Analytics (456789012345)", "Security (567890123456)"])
                permission_level = st.selectbox("Permission Level", ["AdministratorAccess", "PowerUserAccess", "ReadOnlyAccess", "DeveloperAccess"])
            
            with col2:
                duration = st.selectbox("Access Duration", ["4 hours", "8 hours", "12 hours", "1 day", "7 days", "30 days"])
                justification = st.text_area("Business Justification", placeholder="Explain why you need this access...", height=80)
            
            col1, col2 = st.columns([3, 1])
            with col2:
                if st.form_submit_button("📤 Submit Request", type="primary", use_container_width=True):
                    st.success("✅ Access request submitted!")
                    st.info("⏳ Awaiting approval from account owner")
        
        # Pending requests
        st.markdown("---")
        st.markdown("### ⏳ My Pending Requests")
        
        pending_access = pd.DataFrame([
            {"Request ID": "ACC-2024-089", "Account": "Production", "Permission": "PowerUserAccess", "Duration": "8 hours", "Status": "⏳ Pending", "Requested": "10 mins ago"},
            {"Request ID": "ACC-2024-088", "Account": "Data Analytics", "Permission": "ReadOnlyAccess", "Duration": "4 hours", "Status": "✅ Approved", "Requested": "2 hours ago"}
        ])
        
        st.dataframe(pending_access, use_container_width=True, hide_index=True)
    
    def render_access_audit(self):
        """Access audit and compliance"""
        st.markdown("### 🔍 Access Audit & Compliance")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Access Events", "1,234", help="Last 30 days")
        with col2:
            st.metric("Unique Users", "87")
        with col3:
            st.metric("Cross-Account Assumes", "456")
        with col4:
            st.metric("Failed Attempts", "12", delta_color="inverse")
        
        st.markdown("---")
        st.markdown("### 📊 Recent Access Activity")
        
        access_logs = pd.DataFrame([
            {"Timestamp": "2024-11-30 14:23:45", "User": "john.doe@company.com", "Action": "AssumeRole", "Account": "Production", "Role": "PowerUserAccess", "Result": "✅ Success"},
            {"Timestamp": "2024-11-30 14:18:12", "User": "jane.smith@company.com", "Action": "AssumeRole", "Account": "Data Analytics", "Role": "DataScientistAccess", "Result": "✅ Success"},
            {"Timestamp": "2024-11-30 14:05:33", "User": "bob.jones@company.com", "Action": "AssumeRole", "Account": "Production", "Role": "AdministratorAccess", "Result": "❌ Denied - MFA Required"},
            {"Timestamp": "2024-11-30 13:45:21", "User": "alice.wong@company.com", "Action": "AssumeRole", "Account": "Security", "Role": "SecurityAudit", "Result": "✅ Success"},
        ])
        
        st.dataframe(access_logs, use_container_width=True, hide_index=True)
    
    def cmdb_inventory(self):
        """CMDB and resource inventory across accounts"""
        st.subheader("📊 CMDB & Multi-Account Resource Inventory")
        st.markdown("**Configuration Management Database for all AWS resources**")
        
        # CMDB overview
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total Resources", "3,456", "+89")
        with col2:
            st.metric("EC2 Instances", "234", "+12")
        with col3:
            st.metric("RDS Databases", "45", "+2")
        with col4:
            st.metric("S3 Buckets", "567", "+23")
        with col5:
            st.metric("Lambda Functions", "892", "+45")
        
        st.markdown("---")
        
        # CMDB tabs
        cmdb_tabs = st.tabs([
            "🔍 Resource Search",
            "📈 Resource Distribution",
            "🏷️ Tagging Compliance",
            "💰 Cost Attribution"
        ])
        
        with cmdb_tabs[0]:
            self.render_resource_search()
        
        with cmdb_tabs[1]:
            self.render_resource_distribution()
        
        with cmdb_tabs[2]:
            self.render_tagging_compliance()
        
        with cmdb_tabs[3]:
            self.render_cost_attribution()
    
    def render_resource_search(self):
        """Multi-account resource search"""
        st.markdown("### 🔍 Search Resources Across All Accounts")
        
        # Search filters
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            search_query = st.text_input("🔍 Search", placeholder="Resource name, ID, or tag...")
        with col2:
            account_filter = st.multiselect("Accounts", ["All", "Production", "Staging", "Development"], default=["All"])
        with col3:
            resource_type = st.selectbox("Resource Type", ["All", "EC2", "RDS", "S3", "Lambda", "VPC", "ELB"])
        with col4:
            region_filter = st.multiselect("Regions", ["All", "us-east-1", "us-west-2", "eu-west-1"], default=["All"])
        
        # Search results
        st.markdown("### 📋 Search Results")
        
        resources = pd.DataFrame([
            {
                "Resource ID": "i-0abc123def456",
                "Name": "prod-web-server-01",
                "Type": "EC2 Instance",
                "Account": "Production (123456789012)",
                "Region": "us-east-1",
                "State": "🟢 Running",
                "Tags": "Env=Production, App=WebServer",
                "Monthly Cost": "$145"
            },
            {
                "Resource ID": "db-instance-prod-01",
                "Name": "prod-mysql-primary",
                "Type": "RDS MySQL",
                "Account": "Production (123456789012)",
                "Region": "us-east-1",
                "State": "🟢 Available",
                "Tags": "Env=Production, App=Database",
                "Monthly Cost": "$456"
            },
            {
                "Resource ID": "my-data-bucket-123",
                "Name": "company-data-lake",
                "Type": "S3 Bucket",
                "Account": "Data Analytics (456789012345)",
                "Region": "us-east-1",
                "State": "🟢 Active",
                "Tags": "Env=Production, Type=DataLake",
                "Monthly Cost": "$234"
            },
            {
                "Resource ID": "lambda-api-handler",
                "Name": "api-request-handler",
                "Type": "Lambda Function",
                "Account": "Production (123456789012)",
                "Region": "us-east-1",
                "State": "🟢 Active",
                "Tags": "Env=Production, App=API",
                "Monthly Cost": "$23"
            }
        ])
        
        st.dataframe(resources, use_container_width=True, hide_index=True)
        
        # Export options
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("📊 Export to CSV", use_container_width=True):
                st.info("Exporting resource inventory...")
        with col2:
            if st.button("📄 Generate Report", use_container_width=True):
                st.info("Generating CMDB report...")
        with col3:
            if st.button("🏷️ Bulk Tag", use_container_width=True):
                st.info("Opening bulk tagging tool...")
        with col4:
            if st.button("🔄 Sync CMDB", use_container_width=True):
                st.success("CMDB sync initiated!")
    
    def render_resource_distribution(self):
        """Resource distribution across accounts and regions"""
        st.markdown("### 📈 Resource Distribution")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### By Account")
            account_dist = pd.DataFrame({
                'Account': ['Production', 'Staging', 'Development', 'Data Analytics', 'Security', 'Shared'],
                'Resources': [1234, 567, 892, 445, 156, 162]
            })
            st.bar_chart(account_dist.set_index('Account'))
        
        with col2:
            st.markdown("#### By Region")
            region_dist = pd.DataFrame({
                'Region': ['us-east-1', 'us-west-2', 'eu-west-1', 'ap-southeast-1', 'ap-northeast-1'],
                'Resources': [1567, 892, 534, 289, 174]
            })
            st.bar_chart(region_dist.set_index('Region'))
        
        st.markdown("---")
        
        st.markdown("#### Resource Type Distribution")
        resource_types = pd.DataFrame({
            'Type': ['EC2', 'Lambda', 'S3', 'RDS', 'DynamoDB', 'VPC', 'ELB', 'CloudFront', 'Route53', 'ECS'],
            'Count': [234, 892, 567, 45, 123, 89, 67, 34, 56, 78]
        })
        st.bar_chart(resource_types.set_index('Type'))
    
    def render_tagging_compliance(self):
        """Tagging compliance dashboard"""
        st.markdown("### 🏷️ Tagging Compliance")
        
        # Compliance metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Overall Compliance", "87%", "+3%")
        with col2:
            st.metric("Required Tags Met", "3,012")
        with col3:
            st.metric("Missing Tags", "444", delta_color="inverse")
        with col4:
            st.metric("Invalid Tag Values", "67", delta_color="inverse")
        
        st.markdown("---")
        
        # Required tags policy
        st.markdown("### 📋 Required Tags Policy")
        
        required_tags = pd.DataFrame([
            {"Tag Key": "Environment", "Valid Values": "Production, Staging, Development", "Compliance": "92%", "Resources": "3,180 / 3,456"},
            {"Tag Key": "CostCenter", "Valid Values": "CC-XXXX format", "Compliance": "85%", "Resources": "2,937 / 3,456"},
            {"Tag Key": "Owner", "Valid Values": "Email address", "Compliance": "89%", "Resources": "3,076 / 3,456"},
            {"Tag Key": "Application", "Valid Values": "Any string", "Compliance": "78%", "Resources": "2,695 / 3,456"},
            {"Tag Key": "DataClassification", "Valid Values": "Public, Internal, Confidential", "Compliance": "73%", "Resources": "2,523 / 3,456"},
        ])
        
        st.dataframe(required_tags, use_container_width=True, hide_index=True)
        
        # Non-compliant resources
        st.markdown("---")
        st.markdown("### ⚠️ Non-Compliant Resources")
        
        non_compliant = pd.DataFrame([
            {"Resource ID": "i-0abc123", "Type": "EC2", "Account": "Production", "Missing Tags": "CostCenter, Owner", "Created": "2024-11-20", "Age": "10 days"},
            {"Resource ID": "db-xyz789", "Type": "RDS", "Account": "Staging", "Missing Tags": "DataClassification", "Created": "2024-11-18", "Age": "12 days"},
            {"Resource ID": "bucket-data", "Type": "S3", "Account": "Data Analytics", "Missing Tags": "Owner", "Created": "2024-11-15", "Age": "15 days"},
        ])
        
        st.dataframe(non_compliant, use_container_width=True, hide_index=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔧 Auto-Remediate", use_container_width=True, type="primary"):
                st.info("Auto-remediation started for non-compliant resources...")
        with col2:
            if st.button("📧 Send Notifications", use_container_width=True):
                st.success("Compliance notifications sent to resource owners!")
        with col3:
            if st.button("📊 Compliance Report", use_container_width=True):
                st.info("Generating compliance report...")
    
    def render_cost_attribution(self):
        """Cost attribution by tags"""
        st.markdown("### 💰 Cost Attribution via Tags")
        
        st.info("📊 Track costs across accounts, cost centers, and applications using tags")
        
        # Cost by tag
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Cost by Cost Center")
            cost_center_data = pd.DataFrame({
                'Cost Center': ['CC-ENG-001', 'CC-DATA-005', 'CC-ML-001', 'CC-SEC-002', 'Untagged'],
                'Monthly Cost': [45000, 32000, 28000, 12000, 8000]
            })
            st.bar_chart(cost_center_data.set_index('Cost Center'))
        
        with col2:
            st.markdown("#### Cost by Application")
            app_data = pd.DataFrame({
                'Application': ['Web Platform', 'Data Pipeline', 'ML Training', 'API Services', 'Monitoring'],
                'Monthly Cost': [38000, 29000, 25000, 18000, 15000]
            })
            st.bar_chart(app_data.set_index('Application'))
        
        st.markdown("---")
        
        # Detailed cost breakdown
        st.markdown("### 📋 Detailed Cost Attribution")
        
        cost_details = pd.DataFrame([
            {"Tag": "Environment=Production", "Accounts": "6", "Resources": "1,234", "Monthly Cost": "$78,450", "% of Total": "62.8%"},
            {"Tag": "Environment=Staging", "Accounts": "4", "Resources": "567", "Monthly Cost": "$23,120", "% of Total": "18.5%"},
            {"Tag": "Environment=Development", "Accounts": "8", "Resources": "892", "Monthly Cost": "$15,670", "% of Total": "12.5%"},
            {"Tag": "CostCenter=CC-ENG-001", "Accounts": "5", "Resources": "678", "Monthly Cost": "$45,000", "% of Total": "36.0%"},
            {"Tag": "Application=WebPlatform", "Accounts": "3", "Resources": "456", "Monthly Cost": "$38,000", "% of Total": "30.4%"},
        ])
        
        st.dataframe(cost_details, use_container_width=True, hide_index=True)
    
    def organization_settings(self):
        """AWS Organizations settings and policies"""
        st.subheader("⚙️ AWS Organization Settings")
        st.markdown("**Configure organization-wide policies and settings**")
        
        # Organization info
        st.markdown("### 🏢 Organization Information")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Organization ID:** o-abc123xyz456")
            st.markdown("**Management Account:** 111122223333")
        with col2:
            st.markdown("**Organization Name:** Company AWS Org")
            st.markdown("**Created:** 2023-01-10")
        with col3:
            st.markdown("**Feature Set:** All Features")
            st.markdown("**Total Accounts:** 47")
        
        st.markdown("---")
        
        # Organization settings tabs
        org_tabs = st.tabs([
            "🏗️ Organizational Units",
            "📜 Service Control Policies",
            "💼 Consolidated Billing",
            "🔧 Organization Policies"
        ])
        
        with org_tabs[0]:
            self.render_organizational_units()
        
        with org_tabs[1]:
            self.render_service_control_policies()
        
        with org_tabs[2]:
            self.render_consolidated_billing()
        
        with org_tabs[3]:
            self.render_organization_policies()
    
    def render_organizational_units(self):
        """Organizational Units structure"""
        st.markdown("### 🏗️ Organizational Units (OUs)")
        
        st.markdown("""
        ```
        Root
        ├── Production (12 accounts)
        ├── Non-Production (15 accounts)
        │   ├── Staging (6 accounts)
        │   └── Development (9 accounts)
        ├── Workloads (8 accounts)
        ├── Security (4 accounts)
        ├── Infrastructure (5 accounts)
        └── Sandbox (3 accounts)
        ```
        """)
        
        # OU details
        ou_data = pd.DataFrame([
            {"OU Name": "Production", "Parent": "Root", "Accounts": 12, "SCPs Attached": "ProductionSCP, BaselineSCP", "Description": "Production workloads"},
            {"OU Name": "Non-Production", "Parent": "Root", "Accounts": 15, "SCPs Attached": "NonProdSCP, BaselineSCP", "Description": "Non-production environments"},
            {"OU Name": "Staging", "Parent": "Non-Production", "Accounts": 6, "SCPs Attached": "StagingSCP", "Description": "Staging environments"},
            {"OU Name": "Development", "Parent": "Non-Production", "Accounts": 9, "SCPs Attached": "DevSCP", "Description": "Development environments"},
            {"OU Name": "Workloads", "Parent": "Root", "Accounts": 8, "SCPs Attached": "WorkloadSCP", "Description": "Specialized workloads"},
            {"OU Name": "Security", "Parent": "Root", "Accounts": 4, "SCPs Attached": "SecuritySCP", "Description": "Security and audit"},
            {"OU Name": "Infrastructure", "Parent": "Root", "Accounts": 5, "SCPs Attached": "InfraSCP", "Description": "Shared infrastructure"},
            {"OU Name": "Sandbox", "Parent": "Root", "Accounts": 3, "SCPs Attached": "SandboxSCP", "Description": "Experimental sandboxes"},
        ])
        
        st.dataframe(ou_data, use_container_width=True, hide_index=True)
    
    def render_service_control_policies(self):
        """Service Control Policies management"""
        st.markdown("### 📜 Service Control Policies (SCPs)")
        
        st.info("📘 SCPs set permission guardrails for all IAM principals in member accounts")
        
        scp_data = pd.DataFrame([
            {"Policy Name": "BaselineSCP", "Description": "Baseline security controls", "Attached To": "All OUs", "Effect": "Deny risky actions", "Status": "✅ Active"},
            {"Policy Name": "ProductionSCP", "Description": "Production environment restrictions", "Attached To": "Production OU", "Effect": "Deny destructive actions", "Status": "✅ Active"},
            {"Policy Name": "DenyRegionsSCP", "Description": "Restrict to approved regions", "Attached To": "All OUs", "Effect": "Deny non-approved regions", "Status": "✅ Active"},
            {"Policy Name": "RequireTagsSCP", "Description": "Enforce required tags", "Attached To": "All OUs", "Effect": "Deny untagged resources", "Status": "✅ Active"},
        ])
        
        st.dataframe(scp_data, use_container_width=True, hide_index=True)
        
        # SCP example
        with st.expander("📄 View SCP Example"):
            st.code("""
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Deny",
      "Action": [
        "ec2:RunInstances"
      ],
      "Resource": "*",
      "Condition": {
        "StringNotEquals": {
          "ec2:Region": [
            "us-east-1",
            "us-west-2",
            "eu-west-1"
          ]
        }
      }
    }
  ]
}
            """, language="json")
    
    def render_consolidated_billing(self):
        """Consolidated billing overview"""
        st.markdown("### 💼 Consolidated Billing")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Current Month Total", "$125,340")
        with col2:
            st.metric("Last Month Total", "$117,890", "+6.3%")
        with col3:
            st.metric("Savings Plans Savings", "$12,450")
        with col4:
            st.metric("Reserved Instance Savings", "$8,920")
        
        st.markdown("---")
        
        # Cost by account
        st.markdown("#### Cost by Account (Current Month)")
        
        account_costs = pd.DataFrame([
            {"Account": "Production (123456789012)", "Current MTD": "$45,230", "Last Month": "$42,100", "Change": "+7.4%", "Forecast": "$48,500"},
            {"Account": "Data Analytics (456789012345)", "Current MTD": "$32,140", "Last Month": "$29,800", "Change": "+7.9%", "Forecast": "$34,200"},
            {"Account": "Staging (234567890123)", "Current MTD": "$18,560", "Last Month": "$19,200", "Change": "-3.3%", "Forecast": "$19,100"},
            {"Account": "Development (345678901234)", "Current MTD": "$12,340", "Last Month": "$11,890", "Change": "+3.8%", "Forecast": "$13,000"},
            {"Account": "Security (567890123456)", "Current MTD": "$8,920", "Last Month": "$8,450", "Change": "+5.6%", "Forecast": "$9,100"},
        ])
        
        st.dataframe(account_costs, use_container_width=True, hide_index=True)
    
    def render_organization_policies(self):
        """Organization-wide policies"""
        st.markdown("### 🔧 Organization Policies")
        
        st.markdown("#### AI Services Opt-Out Policy")
        ai_optout = st.checkbox("Opt out of AI services using customer content for service improvements", value=True)
        if ai_optout:
            st.success("✅ Enabled - Customer content will not be used for AI service improvements")
        
        st.markdown("---")
        
        st.markdown("#### Backup Policy")
        backup_enabled = st.checkbox("Enforce backup policy across organization", value=True)
        if backup_enabled:
            st.success("✅ Enabled - All resources must follow backup retention policies")
        
        st.markdown("---")
        
        st.markdown("#### Tag Policy")
        tag_policy = st.checkbox("Enforce tag policy across organization", value=True)
        if tag_policy:
            st.success("✅ Enabled - Required tags must be present on all resources")
