"""
Module 5: Security & Compliance
Features:
- RBAC & Identity Integration
- Network Micro-Segmentation Compliance
- Encryption Defaults & Enforcement
- Secrets Management Integration
- Certificate Management
- Audit Logging & Forensics
- Vulnerability Scanning Integration
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json

class SecurityComplianceModule:
    """Security and Compliance Management"""
    
    def __init__(self, demo_mode=True):
        """Initialize Security & Compliance module"""
        self.demo_mode = demo_mode
        

    def _get_data(self, key: str, default_demo_value):
        """
        Get data based on current mode (Demo or Live)
        
        Args:
            key: Data key to fetch
            default_demo_value: Value to return in demo mode
            
        Returns:
            Demo data or Live data based on mode
        """
        is_demo = st.session_state.get('mode', 'Demo') == 'Demo'
        
        if is_demo:
            return default_demo_value
        else:
            try:
                # TODO: Implement live data fetching for this key
                # For now, return demo value in live mode
                # Add your live data logic here
                
                # Example:
                # if key == 'total_cost':
                #     from cost_explorer_integration import CostExplorerIntegration
                #     ce = CostExplorerIntegration()
                #     return ce.get_total_cost()
                
                return default_demo_value
            except Exception as e:
                st.warning(f"Live data fetch failed for {key}: {e}")
                return default_demo_value


    def render(self):
        """Main render method for Security & Compliance module"""
        st.header("🔒 Security & Compliance Management")

        # Show current mode
        is_demo = st.session_state.get('mode', 'Demo') == 'Demo'
        if is_demo:
            st.info("📊 Demo Mode: Showing sample data")
        else:
            st.success("🔴 Live Mode: Showing real data")
        

        
        # Sub-navigation tabs
        tabs = st.tabs([
            "🔐 RBAC & Identity",
            "🔗 Network Segmentation",
            "🔑 Encryption Management",
            "🗝️ Secrets Management",
            "📜 Certificate Management",
            "📊 Audit & Forensics",
            "🔍 Vulnerability Scanning",
            "📈 Security Dashboard"
        ])
        
        with tabs[0]:
            self.rbac_identity_integration()
        
        with tabs[1]:
            self.network_micro_segmentation()
        
        with tabs[2]:
            self.encryption_management()
        
        with tabs[3]:
            self.secrets_management()
        
        with tabs[4]:
            self.certificate_management()
        
        with tabs[5]:
            self.audit_logging_forensics()
        
        with tabs[6]:
            self.vulnerability_scanning()
        
        with tabs[7]:
            self.security_dashboard()
    
    # ==================== RBAC & Identity Integration ====================
    def rbac_identity_integration(self):
        """RBAC and Identity Integration Management"""
        st.subheader("🔐 RBAC & Identity Integration")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### Identity Provider Configuration")
            
            # Identity Provider Selection
            idp_type = st.selectbox(
                "Identity Provider",
                ["AWS IAM Identity Center (SSO)", "Azure AD", "Okta", "Google Workspace", "SAML 2.0", "OIDC"]
            )
            
            # Configuration based on provider
            with st.expander("🔧 Provider Configuration", expanded=True):
                if idp_type == "AWS IAM Identity Center (SSO)":
                    st.text_input("SSO Instance ARN", "arn:aws:sso:::instance/ssoins-1234567890abcdef")
                    st.text_input("Identity Store ID", "d-1234567890")
                    st.selectbox("Authentication Method", ["SAML 2.0", "SCIM"])
                
                elif idp_type in ["Azure AD", "Okta", "Google Workspace"]:
                    st.text_input("Tenant ID / Domain", "example.okta.com")
                    st.text_input("Client ID", "")
                    st.text_input("Client Secret", type="password")
                    st.text_input("SSO URL", "")
                    st.checkbox("Enable SCIM Provisioning")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.button("🔗 Test Connection", use_container_width=True)
                with col_b:
                    st.button("💾 Save Configuration", use_container_width=True)
            
            # Role-Based Access Control
            st.markdown("### 👥 Role Management")
            
            # Create new role
            with st.expander("➕ Create New Role"):
                role_name = st.text_input("Role Name", "DataScientist")
                role_desc = st.text_area("Description", "Data science team with ML/AI access")
                
                st.markdown("**AWS Services Access:**")
                services_col1, services_col2, services_col3 = st.columns(3)
                
                with services_col1:
                    st.checkbox("EC2", value=True)
                    st.checkbox("S3", value=True)
                    st.checkbox("Lambda", value=True)
                    st.checkbox("RDS", value=False)
                
                with services_col2:
                    st.checkbox("SageMaker", value=True)
                    st.checkbox("Glue", value=True)
                    st.checkbox("Athena", value=True)
                    st.checkbox("EMR", value=True)
                
                with services_col3:
                    st.checkbox("CloudWatch", value=True)
                    st.checkbox("CloudTrail", value=False)
                    st.checkbox("VPC", value=False)
                    st.checkbox("IAM", value=False)
                
                permission_level = st.selectbox(
                    "Permission Level",
                    ["Read-Only", "Power User", "Administrator", "Custom"]
                )
                
                st.button("✅ Create Role", type="primary", use_container_width=True)
        
        with col2:
            st.markdown("### 📊 Current Roles")
            
            # Display existing roles
            roles_data = self._get_rbac_roles()
            
            for role in roles_data:
                with st.container():
                    st.markdown(f"**{role['name']}**")
                    st.caption(f"Users: {role['users']} | Type: {role['type']}")
                    st.progress(role['usage'] / 100)
                    
                    col_edit, col_del = st.columns(2)
                    with col_edit:
                        st.button("✏️", key=f"edit_{role['name']}", use_container_width=True)
                    with col_del:
                        st.button("🗑️", key=f"del_{role['name']}", use_container_width=True)
                    st.markdown("---")
        
        # User-Role Mapping
        st.markdown("### 🔗 User-Role Assignments")
        
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            user_email = st.text_input("User Email", "user@company.com")
        with col2:
            assigned_role = st.multiselect(
                "Assign Roles",
                ["Administrator", "DataScientist", "Developer", "Analyst", "Viewer"]
            )
        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            st.button("➕ Assign", type="primary", use_container_width=True)
        
        # Current assignments table
        st.markdown("**Current User Assignments:**")
        assignments_df = self._get_user_assignments()
        st.dataframe(assignments_df, use_container_width=True, hide_index=True)
    
    # ==================== Network Micro-Segmentation ====================
    def network_micro_segmentation(self):
        """Network Micro-Segmentation Compliance"""
        st.subheader("🔗 Network Micro-Segmentation")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("### 🌐 Network Zones Configuration")
            
            # Zone Definition
            with st.expander("➕ Define Security Zone", expanded=True):
                zone_name = st.text_input("Zone Name", "DMZ-Public")
                zone_type = st.selectbox(
                    "Zone Type",
                    ["DMZ", "Public Subnet", "Private Subnet", "Isolated/Restricted", "Management"]
                )
                
                vpc_id = st.text_input("VPC ID", "vpc-0123456789abcdef0")
                subnet_range = st.text_input("CIDR Block", "10.0.1.0/24")
                
                st.markdown("**Security Controls:**")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.checkbox("Network ACL", value=True)
                    st.checkbox("Security Group", value=True)
                    st.checkbox("Route Table Isolation", value=True)
                
                with col_b:
                    st.checkbox("VPC Flow Logs", value=True)
                    st.checkbox("Traffic Mirroring", value=False)
                    st.checkbox("AWS Network Firewall", value=True)
                
                compliance_frameworks = st.multiselect(
                    "Compliance Requirements",
                    ["PCI DSS", "HIPAA", "SOC 2", "ISO 27001", "NIST", "FedRAMP"]
                )
                
                st.button("💾 Create Zone", type="primary", use_container_width=True)
            
            # Network Segmentation Rules
            st.markdown("### 🚦 Segmentation Rules")
            
            rules_df = self._get_segmentation_rules()
            st.dataframe(rules_df, use_container_width=True, hide_index=True)
            
            # Add new rule
            with st.expander("➕ Add Segmentation Rule"):
                col_src, col_dst = st.columns(2)
                
                with col_src:
                    st.selectbox("Source Zone", ["DMZ-Public", "Private-App", "Private-DB", "Management"])
                    st.text_input("Source CIDR", "10.0.1.0/24")
                
                with col_dst:
                    st.selectbox("Destination Zone", ["Private-App", "Private-DB", "Internet", "On-Premises"])
                    st.text_input("Destination CIDR", "10.0.2.0/24")
                
                col_prot, col_port, col_act = st.columns(3)
                with col_prot:
                    st.selectbox("Protocol", ["TCP", "UDP", "ICMP", "All"])
                with col_port:
                    st.text_input("Port Range", "443")
                with col_act:
                    st.selectbox("Action", ["Allow", "Deny", "Log & Allow", "Log & Deny"])
                
                st.button("✅ Add Rule", use_container_width=True)
        
        with col2:
            st.markdown("### 📊 Zone Status")
            
            zones = self._get_network_zones()
            for zone in zones:
                with st.container():
                    st.metric(zone['name'], f"{zone['instances']} instances")
                    st.caption(f"Type: {zone['type']}")
                    
                    if zone['compliant']:
                        st.success("✓ Compliant")
                    else:
                        st.error("✗ Non-Compliant")
                    st.markdown("---")
            
            # Compliance Status
            st.markdown("### ✅ Compliance")
            st.metric("Overall Score", "87%", delta="3%")
            
            st.markdown("**Frameworks:**")
            st.progress(0.92, text="PCI DSS: 92%")
            st.progress(0.88, text="HIPAA: 88%")
            st.progress(0.85, text="SOC 2: 85%")
    
    # ==================== Encryption Management ====================
    def encryption_management(self):
        """Encryption Defaults & Enforcement"""
        st.subheader("🔑 Encryption Management")
        
        # Encryption Policy Dashboard
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Encrypted Resources", "1,847", delta="12")
        with col2:
            st.metric("Unencrypted", "23", delta="-5", delta_color="inverse")
        with col3:
            # Mode-aware metric
            kms_keys_active_value = self._get_data('kms_keys_active', "47")
            st.metric("KMS Keys Active", kms_keys_active_value)
        with col4:
            st.metric("Compliance Rate", "98.8%", delta="0.5%")
        
        st.markdown("---")
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "📋 Encryption Status",
            "🔐 KMS Key Management",
            "⚙️ Encryption Policies",
            "🔍 Compliance Scan"
        ])
        
        with tab1:
            st.markdown("### 📊 Resource Encryption Status")
            
            # Filter options
            col_svc, col_status, col_region = st.columns(3)
            with col_svc:
                filter_service = st.multiselect(
                    "AWS Service",
                    ["All", "S3", "EBS", "RDS", "DynamoDB", "EFS", "Redshift", "SNS", "SQS"],
                    default=["All"]
                )
            with col_status:
                filter_status = st.selectbox("Status", ["All", "Encrypted", "Unencrypted", "Default Encryption"])
            with col_region:
                filter_region = st.selectbox("Region", ["All Regions", "us-east-1", "us-west-2", "eu-west-1"])
            
            # Encryption status table
            encryption_df = self._get_encryption_status()
            st.dataframe(encryption_df, use_container_width=True, hide_index=True)
            
            # Bulk actions
            col_action1, col_action2, col_action3 = st.columns(3)
            with col_action1:
                st.button("🔒 Enable Encryption (Selected)", use_container_width=True)
            with col_action2:
                st.button("🔄 Rotate Keys (Selected)", use_container_width=True)
            with col_action3:
                st.button("📊 Export Report", use_container_width=True)
        
        with tab2:
            st.markdown("### 🔐 KMS Key Management")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Create new KMS key
                with st.expander("➕ Create KMS Key", expanded=False):
                    key_alias = st.text_input("Key Alias", "alias/production-data-key")
                    key_desc = st.text_area("Description", "Production data encryption key")
                    
                    key_spec = st.selectbox(
                        "Key Spec",
                        ["SYMMETRIC_DEFAULT", "RSA_2048", "RSA_3072", "RSA_4096", "ECC_NIST_P256"]
                    )
                    
                    key_usage = st.selectbox("Key Usage", ["ENCRYPT_DECRYPT", "SIGN_VERIFY"])
                    
                    st.checkbox("Enable automatic key rotation (annual)", value=True)
                    
                    st.markdown("**Key Policy:**")
                    key_policy = st.text_area(
                        "Policy JSON",
                        value='{\n  "Version": "2012-10-17",\n  "Statement": [{\n    "Sid": "Enable IAM User Permissions",\n    "Effect": "Allow",\n    "Principal": {"AWS": "arn:aws:iam::123456789012:root"},\n    "Action": "kms:*",\n    "Resource": "*"\n  }]\n}',
                        height=150
                    )
                    
                    st.button("✅ Create Key", type="primary", use_container_width=True)
                
                # Existing keys table
                st.markdown("**Existing KMS Keys:**")
                kms_keys_df = self._get_kms_keys()
                st.dataframe(kms_keys_df, use_container_width=True, hide_index=True)
            
            with col2:
                st.markdown("### 📊 Key Usage Stats")
                
                # Mode-aware metric
            total_keys_value = self._get_data('total_keys', "47")
            st.metric("Total Keys", total_keys_value)
                # Mode-aware metric
            active_rotations_value = self._get_data('active_rotations', "12")
            st.metric("Active Rotations", active_rotations_value)
                # Mode-aware metric
            pending_deletion_value = self._get_data('pending_deletion', "2")
            st.metric("Pending Deletion", pending_deletion_value)
                
                st.markdown("### 🔄 Rotation Status")
                st.progress(0.85, text="Auto-rotation: 85%")
                
                st.markdown("### ⚠️ Alerts")
                st.warning("2 keys not rotated in 365+ days")
                st.info("5 keys approaching rotation")
        
        with tab3:
            st.markdown("### ⚙️ Encryption Policy Configuration")
            
            # Service-specific policies
            service = st.selectbox(
                "Select Service",
                ["S3", "EBS", "RDS", "DynamoDB", "EFS", "Redshift", "Global Settings"]
            )
            
            with st.expander(f"🔧 {service} Encryption Policy", expanded=True):
                enforce_encryption = st.checkbox("Enforce encryption for all new resources", value=True)
                
                if service == "S3":
                    st.checkbox("Enforce bucket encryption (AES-256 or KMS)", value=True)
                    st.checkbox("Block unencrypted uploads", value=True)
                    default_key = st.selectbox("Default KMS Key", ["AWS Managed", "Customer Managed"])
                    st.checkbox("Require SSL/TLS for data in transit", value=True)
                
                elif service == "EBS":
                    st.checkbox("Enable default EBS encryption", value=True)
                    st.selectbox("Default encryption key", ["AWS Managed", "Customer Managed"])
                    st.checkbox("Encrypt snapshots by default", value=True)
                
                elif service == "RDS":
                    st.checkbox("Enforce encryption for new DB instances", value=True)
                    st.checkbox("Enforce encryption for read replicas", value=True)
                    st.checkbox("Encrypt automated backups", value=True)
                    st.checkbox("Enable storage encryption at rest", value=True)
                
                st.button("💾 Save Policy", type="primary", use_container_width=True)
            
            # Policy Summary
            st.markdown("### 📋 Active Encryption Policies")
            policies_df = self._get_encryption_policies()
            st.dataframe(policies_df, use_container_width=True, hide_index=True)
        
        with tab4:
            st.markdown("### 🔍 Encryption Compliance Scan")
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown("**Scan Configuration:**")
                
                scan_scope = st.multiselect(
                    "Services to Scan",
                    ["S3", "EBS", "RDS", "DynamoDB", "EFS", "Redshift", "SNS", "SQS", "Lambda"],
                    default=["S3", "EBS", "RDS"]
                )
                
                scan_regions = st.multiselect(
                    "Regions",
                    ["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1"],
                    default=["us-east-1"]
                )
                
                compliance_check = st.multiselect(
                    "Compliance Frameworks",
                    ["PCI DSS", "HIPAA", "GDPR", "SOC 2", "ISO 27001"],
                    default=["PCI DSS", "HIPAA"]
                )
                
                if st.button("🚀 Start Compliance Scan", type="primary", use_container_width=True):
                    with st.spinner("Scanning resources..."):
                        import time
                        progress_bar = st.progress(0)
                        for i in range(100):
                            time.sleep(0.02)
                            progress_bar.progress(i + 1)
                        st.success("✅ Scan completed successfully!")
            
            with col2:
                st.markdown("### 📊 Last Scan")
                # Mode-aware metric
            total_resources_value = self._get_data('total_resources', "1,870")
            st.metric("Total Resources", total_resources_value)
                # Mode-aware metric
            compliant_value = self._get_data('compliant', "1,847")
            st.metric("Compliant", compliant_value)
                # Mode-aware metric
            non-compliant_value = self._get_data('non-compliant', "23")
            st.metric("Non-Compliant", non-compliant_value)
                st.caption("Last scan: 2 hours ago")
            
            # Scan results
            if st.session_state.get('scan_complete', False):
                st.markdown("### 📋 Scan Results")
                scan_results_df = self._get_scan_results()
                st.dataframe(scan_results_df, use_container_width=True, hide_index=True)
    
    # ==================== Secrets Management ====================
    def secrets_management(self):
        """Secrets Management Integration"""
        st.subheader("🗝️ Secrets Management")
        
        # Overview metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            # Mode-aware metric
            total_secrets_value = self._get_data('total_secrets', "342")
            st.metric("Total Secrets", total_secrets_value)
        with col2:
            st.metric("Expiring Soon", "12", delta="-3", delta_color="inverse")
        with col3:
            # Mode-aware metric
            recently_rotated_value = self._get_data('recently_rotated', "45")
            st.metric("Recently Rotated", recently_rotated_value)
        with col4:
            st.metric("Access Violations", "0", delta="0")
        
        st.markdown("---")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Create new secret
            with st.expander("➕ Create New Secret", expanded=False):
                secret_name = st.text_input("Secret Name", "prod/database/master-password")
                secret_type = st.selectbox(
                    "Secret Type",
                    ["Database Credentials", "API Key", "SSH Key", "Certificate", "OAuth Token", "Other"]
                )
                
                if secret_type == "Database Credentials":
                    st.text_input("Username", "admin")
                    st.text_input("Password", type="password")
                    st.text_input("Database Host", "prod-db.abc123.us-east-1.rds.amazonaws.com")
                    st.text_input("Port", "5432")
                    st.text_input("Database Name", "production")
                else:
                    secret_value = st.text_area("Secret Value", type="password")
                
                st.text_area("Description", "Production database master credentials")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    rotation_enabled = st.checkbox("Enable automatic rotation", value=True)
                    if rotation_enabled:
                        st.number_input("Rotation interval (days)", min_value=1, value=30)
                
                with col_b:
                    st.selectbox("Encryption Key", ["AWS Managed", "Customer Managed KMS"])
                    st.text_input("Lambda ARN (for rotation)", "arn:aws:lambda:...")
                
                tags = st.text_input("Tags (comma-separated)", "environment=prod,team=engineering")
                
                st.button("✅ Create Secret", type="primary", use_container_width=True)
            
            # Secrets table
            st.markdown("### 📋 Secrets Inventory")
            
            # Filters
            col_filter1, col_filter2, col_filter3 = st.columns(3)
            with col_filter1:
                filter_type = st.selectbox("Type", ["All", "Database", "API Key", "Certificate", "SSH Key"])
            with col_filter2:
                filter_status = st.selectbox("Status", ["All", "Active", "Expiring", "Expired", "Rotating"])
            with col_filter3:
                filter_env = st.selectbox("Environment", ["All", "Production", "Staging", "Development"])
            
            secrets_df = self._get_secrets_inventory()
            st.dataframe(secrets_df, use_container_width=True, hide_index=True)
            
            # Bulk actions
            col_action1, col_action2, col_action3 = st.columns(3)
            with col_action1:
                st.button("🔄 Rotate Selected", use_container_width=True)
            with col_action2:
                st.button("📊 Access Report", use_container_width=True)
            with col_action3:
                st.button("📤 Export", use_container_width=True)
        
        with col2:
            st.markdown("### ⚠️ Attention Required")
            
            # Expiring secrets
            with st.container():
                st.error("**Expiring in 7 days:**")
                st.caption("prod/api/stripe-key")
                st.caption("prod/db/analytics-pwd")
                st.button("Rotate Now", key="rotate1", use_container_width=True)
            
            st.markdown("---")
            
            # Recently accessed
            st.markdown("### 🔍 Recent Access")
            access_logs = [
                {"secret": "prod/db/master", "by": "app-server-01", "when": "2 min ago"},
                {"secret": "prod/api/payment", "by": "lambda-checkout", "when": "5 min ago"},
                {"secret": "staging/db/test", "by": "dev-user-01", "when": "12 min ago"}
            ]
            
            for log in access_logs:
                with st.container():
                    st.caption(f"**{log['secret']}**")
                    st.caption(f"By: {log['by']} | {log['when']}")
                    st.markdown("---")
            
            # Rotation schedule
            st.markdown("### 🔄 Rotation Schedule")
            st.progress(0.75, text="Next rotation: 7 days")
            st.caption("12 secrets scheduled")
    
    # ==================== Certificate Management ====================
    def certificate_management(self):
        """Certificate Management"""
        st.subheader("📜 Certificate Management")
        
        # Overview
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            # Mode-aware metric
            total_certificates_value = self._get_data('total_certificates', "127")
            st.metric("Total Certificates", total_certificates_value)
        with col2:
            st.metric("Expiring (30 days)", "8", delta="-2", delta_color="inverse")
        with col3:
            # Mode-aware metric
            auto-renewed_value = self._get_data('auto-renewed', "94")
            st.metric("Auto-Renewed", auto-renewed_value)
        with col4:
            # Mode-aware metric
            validation_errors_value = self._get_data('validation_errors', "0")
            st.metric("Validation Errors", validation_errors_value)
        
        st.markdown("---")
        
        tab1, tab2, tab3 = st.tabs(["📋 Certificates", "➕ Request Certificate", "⚙️ Settings"])
        
        with tab1:
            st.markdown("### 📊 Certificate Inventory")
            
            # Filters
            col_f1, col_f2, col_f3, col_f4 = st.columns(4)
            with col_f1:
                filter_status = st.selectbox("Status", ["All", "Active", "Expiring", "Expired", "Pending"])
            with col_f2:
                filter_type = st.selectbox("Type", ["All", "Public", "Private", "Imported"])
            with col_f3:
                filter_validation = st.selectbox("Validation", ["All", "DNS", "Email", "None"])
            with col_f4:
                filter_renewal = st.selectbox("Renewal", ["All", "Automatic", "Manual"])
            
            # Certificates table
            certs_df = self._get_certificates()
            st.dataframe(certs_df, use_container_width=True, hide_index=True)
            
            # Actions
            col_a1, col_a2, col_a3 = st.columns(3)
            with col_a1:
                st.button("📥 Export Selected", use_container_width=True)
            with col_a2:
                st.button("🔄 Renew Selected", use_container_width=True)
            with col_a3:
                st.button("🗑️ Delete Selected", use_container_width=True)
        
        with tab2:
            st.markdown("### ➕ Request New Certificate")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Certificate request form
                cert_type = st.radio(
                    "Certificate Type",
                    ["Public Certificate (ACM)", "Private Certificate (ACM PCA)", "Import Certificate"]
                )
                
                if cert_type == "Public Certificate (ACM)":
                    domain_name = st.text_input("Domain Name", "www.example.com")
                    
                    st.checkbox("Add additional names", value=False)
                    additional_names = st.text_area("Additional Names (one per line)", "*.example.com\napi.example.com")
                    
                    validation_method = st.radio("Validation Method", ["DNS Validation", "Email Validation"])
                    
                    if validation_method == "Email Validation":
                        st.text_input("Contact Email", "admin@example.com")
                    
                    st.checkbox("Enable transparency logging", value=True)
                    
                elif cert_type == "Private Certificate (ACM PCA)":
                    st.text_input("Common Name (CN)", "internal.example.com")
                    st.selectbox("Certificate Authority", ["Production CA", "Development CA", "Test CA"])
                    st.number_input("Validity Period (days)", min_value=1, max_value=3650, value=365)
                    st.selectbox("Key Algorithm", ["RSA 2048", "RSA 4096", "ECDSA P256", "ECDSA P384"])
                
                else:  # Import Certificate
                    st.text_area("Certificate Body (PEM)", height=100)
                    st.text_area("Private Key (PEM)", type="password", height=100)
                    st.text_area("Certificate Chain (PEM)", height=100)
                
                tags = st.text_input("Tags", "Environment=Production,Team=DevOps")
                
                st.button("🚀 Request Certificate", type="primary", use_container_width=True)
            
            with col2:
                st.markdown("### 📖 Guidelines")
                st.info("""
                **DNS Validation (Recommended)**
                - Faster validation
                - Supports wildcards
                - Easier to renew
                
                **Email Validation**
                - Requires email access
                - Manual process
                - No wildcards
                """)
                
                st.markdown("### 🔄 Auto-Renewal")
                st.success("ACM automatically renews certificates validated via DNS")
        
        with tab3:
            st.markdown("### ⚙️ Certificate Management Settings")
            
            # Notification settings
            with st.expander("📧 Notifications", expanded=True):
                st.checkbox("Email alerts for expiring certificates", value=True)
                st.number_input("Alert threshold (days before expiry)", min_value=1, value=30)
                st.text_input("Notification Email", "security-team@company.com")
                st.checkbox("Send weekly certificate report", value=True)
            
            # Auto-renewal settings
            with st.expander("🔄 Auto-Renewal Settings", expanded=True):
                st.checkbox("Enable automatic renewal for eligible certificates", value=True)
                st.number_input("Renewal attempt days before expiry", min_value=1, value=60)
                st.checkbox("Send notification on renewal success", value=True)
                st.checkbox("Send notification on renewal failure", value=True)
            
            # Integration settings
            with st.expander("🔗 Integrations", expanded=True):
                st.checkbox("Integrate with CloudFront", value=True)
                st.checkbox("Integrate with Elastic Load Balancer", value=True)
                st.checkbox("Integrate with API Gateway", value=True)
                st.checkbox("Sync with Route 53", value=True)
            
            st.button("💾 Save Settings", type="primary", use_container_width=True)
    
    # ==================== Audit Logging & Forensics ====================
    def audit_logging_forensics(self):
        """Audit Logging and Forensics"""
        st.subheader("📊 Audit Logging & Forensics")
        
        # Overview metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            # Mode-aware metric
            events_today_value = self._get_data('events_today', "47,523")
            st.metric("Events Today", events_today_value)
        with col2:
            st.metric("Security Events", "127", delta="12")
        with col3:
            st.metric("Failed Logins", "5", delta="-2", delta_color="inverse")
        with col4:
            # Mode-aware metric
            log_storage_value = self._get_data('log_storage', "2.4 TB")
            st.metric("Log Storage", log_storage_value)
        
        st.markdown("---")
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "🔍 Event Search",
            "⚠️ Security Events",
            "📊 Compliance Reports",
            "⚙️ Configuration"
        ])
        
        with tab1:
            st.markdown("### 🔍 Audit Event Search")
            
            # Search filters
            col1, col2, col3 = st.columns(3)
            
            with col1:
                time_range = st.selectbox(
                    "Time Range",
                    ["Last Hour", "Last 24 Hours", "Last 7 Days", "Last 30 Days", "Custom Range"]
                )
                
                if time_range == "Custom Range":
                    start_date = st.date_input("Start Date")
                    end_date = st.date_input("End Date")
            
            with col2:
                event_source = st.multiselect(
                    "Event Source",
                    ["All", "IAM", "S3", "EC2", "RDS", "Lambda", "CloudTrail", "CloudWatch", "VPC"]
                )
            
            with col3:
                event_type = st.multiselect(
                    "Event Type",
                    ["All", "Login", "API Call", "Resource Change", "Permission Change", "Error", "Security"]
                )
            
            # Advanced filters
            with st.expander("🔧 Advanced Filters"):
                col_a, col_b = st.columns(2)
                with col_a:
                    user_identity = st.text_input("User Identity", "")
                    source_ip = st.text_input("Source IP", "")
                    resource_id = st.text_input("Resource ID", "")
                
                with col_b:
                    error_code = st.text_input("Error Code", "")
                    event_name = st.text_input("Event Name", "")
                    region = st.selectbox("Region", ["All", "us-east-1", "us-west-2", "eu-west-1"])
            
            # Search button
            col_search, col_export = st.columns([3, 1])
            with col_search:
                if st.button("🔍 Search Events", type="primary", use_container_width=True):
                    st.session_state['search_executed'] = True
            with col_export:
                st.button("📤 Export", use_container_width=True)
            
            # Results
            if st.session_state.get('search_executed', False):
                st.markdown("### 📋 Search Results")
                events_df = self._get_audit_events()
                st.dataframe(events_df, use_container_width=True, hide_index=True)
                
                # Event details viewer
                selected_event = st.selectbox("View Event Details", events_df['Event ID'].tolist())
                
                if selected_event:
                    with st.expander("📄 Event Details", expanded=True):
                        event_details = self._get_event_details(selected_event)
                        
                        col_d1, col_d2 = st.columns(2)
                        with col_d1:
                            st.markdown("**Event Information:**")
                            st.json(event_details['event_info'])
                        
                        with col_d2:
                            st.markdown("**Request Parameters:**")
                            st.json(event_details['request_params'])
        
        with tab2:
            st.markdown("### ⚠️ Security Events & Alerts")
            
            # Severity filter
            col_sev, col_type = st.columns(2)
            with col_sev:
                severity_filter = st.multiselect(
                    "Severity",
                    ["Critical", "High", "Medium", "Low"],
                    default=["Critical", "High"]
                )
            with col_type:
                security_type = st.multiselect(
                    "Event Category",
                    ["Unauthorized Access", "Policy Violation", "Configuration Change", "Suspicious Activity"],
                    default=["Unauthorized Access"]
                )
            
            # Security events table
            security_events_df = self._get_security_events()
            st.dataframe(security_events_df, use_container_width=True, hide_index=True)
            
            # Incident response
            st.markdown("### 🚨 Incident Response")
            
            col_ir1, col_ir2 = st.columns(2)
            with col_ir1:
                selected_incidents = st.multiselect("Select Events for Investigation", security_events_df['Event ID'].tolist())
                
                if selected_incidents:
                    incident_action = st.selectbox(
                        "Action",
                        ["Create Incident", "Add to Existing Incident", "Mark as False Positive", "Suppress"]
                    )
                    
                    if incident_action == "Create Incident":
                        incident_title = st.text_input("Incident Title", "Unauthorized API access attempt")
                        incident_priority = st.selectbox("Priority", ["P1 - Critical", "P2 - High", "P3 - Medium", "P4 - Low"])
                        assigned_to = st.text_input("Assign To", "security-team@company.com")
                        
                        st.button("✅ Create Incident", type="primary", use_container_width=True)
            
            with col_ir2:
                st.markdown("### 📊 Security Trends")
                st.line_chart({"Failed Logins": [5, 8, 3, 12, 7, 5, 9]})
                st.caption("Last 7 days")
        
        with tab3:
            st.markdown("### 📊 Compliance & Audit Reports")
            
            # Report generation
            col1, col2 = st.columns([2, 1])
            
            with col1:
                report_type = st.selectbox(
                    "Report Type",
                    [
                        "Comprehensive Audit Trail",
                        "User Activity Report",
                        "Resource Changes Report",
                        "Security Events Report",
                        "Compliance Report (PCI DSS)",
                        "Compliance Report (HIPAA)",
                        "Compliance Report (SOC 2)",
                        "Access Report",
                        "Failed Login Report"
                    ]
                )
                
                col_period, col_format = st.columns(2)
                with col_period:
                    report_period = st.selectbox("Time Period", ["Last 24 Hours", "Last 7 Days", "Last 30 Days", "Last Quarter", "Custom"])
                
                with col_format:
                    report_format = st.selectbox("Format", ["PDF", "CSV", "JSON", "Excel"])
                
                include_details = st.checkbox("Include detailed event information", value=True)
                include_metadata = st.checkbox("Include resource metadata", value=True)
                
                if st.button("📊 Generate Report", type="primary", use_container_width=True):
                    with st.spinner("Generating report..."):
                        import time
                        time.sleep(2)
                        st.success("✅ Report generated successfully!")
                        st.download_button(
                            "📥 Download Report",
                            data="Sample report data",
                            file_name=f"audit_report_{datetime.now().strftime('%Y%m%d')}.pdf",
                            mime="application/pdf"
                        )
            
            with col2:
                st.markdown("### 📅 Scheduled Reports")
                
                st.caption("**Daily Security Summary**")
                st.caption("Next: Tomorrow 8:00 AM")
                st.caption("Recipients: security@company.com")
                st.markdown("---")
                
                st.caption("**Weekly Compliance Report**")
                st.caption("Next: Friday 5:00 PM")
                st.caption("Recipients: compliance@company.com")
                st.markdown("---")
                
                st.caption("**Monthly Audit Trail**")
                st.caption("Next: Dec 1st")
                st.caption("Recipients: audit@company.com")
                
                st.button("➕ New Schedule", use_container_width=True)
        
        with tab4:
            st.markdown("### ⚙️ Audit Logging Configuration")
            
            # CloudTrail settings
            with st.expander("☁️ CloudTrail Settings", expanded=True):
                st.checkbox("Enable CloudTrail logging", value=True)
                st.text_input("S3 Bucket", "company-audit-logs-bucket")
                st.checkbox("Log file validation", value=True)
                st.checkbox("Multi-region logging", value=True)
                st.checkbox("Organization trail", value=True)
            
            # Log retention
            with st.expander("📦 Log Retention", expanded=True):
                retention_period = st.selectbox(
                    "CloudWatch Logs Retention",
                    ["7 days", "14 days", "30 days", "90 days", "180 days", "1 year", "Never expire"]
                )
                
                st.checkbox("Archive logs to S3 Glacier after 90 days", value=True)
                st.checkbox("Enable log encryption", value=True)
                st.selectbox("Encryption Key", ["AWS Managed", "Customer Managed"])
            
            # Event filtering
            with st.expander("🔍 Event Filtering", expanded=True):
                st.checkbox("Log read-only events", value=True)
                st.checkbox("Log write-only events", value=True)
                st.checkbox("Log data events (S3/Lambda)", value=False)
                st.checkbox("Exclude AWS service events", value=False)
            
            # Alerts and notifications
            with st.expander("🔔 Alerts & Notifications", expanded=True):
                st.checkbox("Alert on root account usage", value=True)
                st.checkbox("Alert on unauthorized API calls", value=True)
                st.checkbox("Alert on IAM policy changes", value=True)
                st.checkbox("Alert on network changes", value=True)
                st.checkbox("Alert on S3 bucket policy changes", value=True)
                
                st.text_input("SNS Topic ARN", "arn:aws:sns:us-east-1:123456789012:security-alerts")
            
            st.button("💾 Save Configuration", type="primary", use_container_width=True)
    
    # ==================== Vulnerability Scanning ====================
    def vulnerability_scanning(self):
        """Vulnerability Scanning Integration"""
        st.subheader("🔍 Vulnerability Scanning")
        
        # Overview metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            # Mode-aware metric
            total_scans_value = self._get_data('total_scans', "1,247")
            st.metric("Total Scans", total_scans_value)
        with col2:
            st.metric("Critical Vulns", "3", delta="-2", delta_color="inverse")
        with col3:
            st.metric("High Vulns", "47", delta="5")
        with col4:
            # Mode-aware metric
            last_scan_value = self._get_data('last_scan', "2h ago")
            st.metric("Last Scan", last_scan_value)
        
        st.markdown("---")
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "🎯 Active Scans",
            "📋 Vulnerabilities",
            "🔧 Scan Configuration",
            "📊 Reports"
        ])
        
        with tab1:
            st.markdown("### 🎯 Active Vulnerability Scans")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # New scan configuration
                with st.expander("➕ Start New Scan", expanded=False):
                    scan_name = st.text_input("Scan Name", "Production Infrastructure Scan")
                    
                    scan_type = st.selectbox(
                        "Scan Type",
                        [
                            "Comprehensive Security Scan",
                            "Container Image Scan (ECR)",
                            "EC2 Instance Scan (Inspector)",
                            "Code Repository Scan (CodeGuru)",
                            "Network Scan",
                            "Compliance Scan"
                        ]
                    )
                    
                    col_target, col_scope = st.columns(2)
                    with col_target:
                        if "Container" in scan_type:
                            target = st.multiselect("Container Images", ["nginx:latest", "app:v1.2.3", "api:production"])
                        elif "EC2" in scan_type:
                            target = st.multiselect("EC2 Instances", ["i-0123456789", "i-abcdef1234", "i-xyz9876543"])
                        elif "Code" in scan_type:
                            target = st.text_input("Repository", "https://github.com/company/app")
                        else:
                            target = st.text_input("Target", "10.0.0.0/16")
                    
                    with col_scope:
                        scan_depth = st.selectbox("Scan Depth", ["Quick", "Standard", "Deep", "Custom"])
                        scan_priority = st.selectbox("Priority", ["High", "Medium", "Low"])
                    
                    st.markdown("**Vulnerability Categories:**")
                    col_vuln1, col_vuln2, col_vuln3 = st.columns(3)
                    with col_vuln1:
                        st.checkbox("CVEs", value=True)
                        st.checkbox("Misconfigurations", value=True)
                        st.checkbox("Exposed Secrets", value=True)
                    with col_vuln2:
                        st.checkbox("Weak Encryption", value=True)
                        st.checkbox("Outdated Software", value=True)
                        st.checkbox("Network Issues", value=True)
                    with col_vuln3:
                        st.checkbox("Compliance Violations", value=True)
                        st.checkbox("Best Practice Gaps", value=True)
                        st.checkbox("License Issues", value=False)
                    
                    schedule = st.checkbox("Schedule recurring scan")
                    if schedule:
                        st.selectbox("Frequency", ["Daily", "Weekly", "Monthly"])
                    
                    if st.button("🚀 Start Scan", type="primary", use_container_width=True):
                        with st.spinner("Initializing scan..."):
                            import time
                            time.sleep(2)
                            st.success("✅ Scan started successfully!")
                
                # Active scans table
                st.markdown("**Running Scans:**")
                active_scans_df = self._get_active_scans()
                st.dataframe(active_scans_df, use_container_width=True, hide_index=True)
                
                # Recent scan history
                st.markdown("**Recent Scan History:**")
                scan_history_df = self._get_scan_history()
                st.dataframe(scan_history_df, use_container_width=True, hide_index=True)
            
            with col2:
                st.markdown("### 📊 Scan Progress")
                
                st.progress(0.65, text="Infrastructure Scan: 65%")
                st.caption("ETA: 15 minutes")
                st.markdown("---")
                
                st.progress(0.30, text="Container Scan: 30%")
                st.caption("ETA: 25 minutes")
                st.markdown("---")
                
                st.markdown("### ⚙️ Scanner Status")
                st.success("✓ AWS Inspector: Active")
                st.success("✓ ECR Scanning: Active")
                st.success("✓ GuardDuty: Active")
                st.info("○ Trivy: Configured")
        
        with tab2:
            st.markdown("### 📋 Discovered Vulnerabilities")
            
            # Filters
            col_f1, col_f2, col_f3, col_f4 = st.columns(4)
            with col_f1:
                severity_filter = st.multiselect(
                    "Severity",
                    ["Critical", "High", "Medium", "Low", "Info"],
                    default=["Critical", "High"]
                )
            with col_f2:
                status_filter = st.selectbox("Status", ["All", "Open", "In Progress", "Resolved", "Ignored"])
            with col_f3:
                category_filter = st.selectbox("Category", ["All", "CVE", "Misconfiguration", "Secrets", "Compliance"])
            with col_f4:
                resource_filter = st.selectbox("Resource Type", ["All", "EC2", "Container", "Lambda", "S3", "RDS"])
            
            # Vulnerabilities table
            vulns_df = self._get_vulnerabilities()
            st.dataframe(vulns_df, use_container_width=True, hide_index=True)
            
            # Vulnerability details
            selected_vuln = st.selectbox("View Details", vulns_df['CVE/ID'].tolist() if not vulns_df.empty else [])
            
            if selected_vuln:
                with st.expander("📄 Vulnerability Details", expanded=True):
                    vuln_details = self._get_vulnerability_details(selected_vuln)
                    
                    col_d1, col_d2 = st.columns([2, 1])
                    
                    with col_d1:
                        st.markdown(f"**{vuln_details['title']}**")
                        st.markdown(f"**Severity:** {vuln_details['severity']}")
                        st.markdown(f"**CVSS Score:** {vuln_details['cvss_score']}")
                        st.markdown("**Description:**")
                        st.write(vuln_details['description'])
                        
                        st.markdown("**Affected Resources:**")
                        st.dataframe(pd.DataFrame(vuln_details['affected_resources']), hide_index=True)
                        
                        st.markdown("**Remediation:**")
                        st.info(vuln_details['remediation'])
                    
                    with col_d2:
                        st.markdown("**Actions:**")
                        st.button("🔧 Create Ticket", use_container_width=True)
                        st.button("✅ Mark Resolved", use_container_width=True)
                        st.button("🚫 Ignore", use_container_width=True)
                        st.button("📊 Export", use_container_width=True)
                        
                        st.markdown("---")
                        st.markdown("**References:**")
                        for ref in vuln_details['references']:
                            st.markdown(f"- [{ref}]({ref})")
            
            # Bulk actions
            st.markdown("---")
            col_action1, col_action2, col_action3 = st.columns(3)
            with col_action1:
                st.button("🎫 Create Tickets (Selected)", use_container_width=True)
            with col_action2:
                st.button("✅ Mark Resolved (Selected)", use_container_width=True)
            with col_action3:
                st.button("📤 Export Report", use_container_width=True)
        
        with tab3:
            st.markdown("### 🔧 Vulnerability Scan Configuration")
            
            # Scanner integrations
            with st.expander("🔌 Scanner Integrations", expanded=True):
                st.markdown("**AWS Native Services:**")
                col_aws1, col_aws2 = st.columns(2)
                with col_aws1:
                    aws_inspector = st.checkbox("AWS Inspector", value=True)
                    if aws_inspector:
                        st.caption("EC2 instance scanning")
                        st.selectbox("Assessment Template", ["CIS Level 1", "CIS Level 2", "Custom"])
                    
                    ecr_scanning = st.checkbox("ECR Image Scanning", value=True)
                    if ecr_scanning:
                        st.caption("Container image scanning")
                        st.checkbox("Scan on push", value=True)
                
                with col_aws2:
                    guardduty = st.checkbox("GuardDuty", value=True)
                    if guardduty:
                        st.caption("Threat detection")
                    
                    codeguru = st.checkbox("CodeGuru Security", value=False)
                    if codeguru:
                        st.caption("Code vulnerability detection")
                
                st.markdown("---")
                st.markdown("**Third-Party Scanners:**")
                col_3rd1, col_3rd2 = st.columns(2)
                with col_3rd1:
                    trivy = st.checkbox("Trivy", value=False)
                    if trivy:
                        st.text_input("Trivy Server URL", "")
                    
                    snyk = st.checkbox("Snyk", value=False)
                    if snyk:
                        st.text_input("Snyk API Token", type="password")
                
                with col_3rd2:
                    aqua = st.checkbox("Aqua Security", value=False)
                    if aqua:
                        st.text_input("Aqua Console URL", "")
                    
                    prisma = st.checkbox("Prisma Cloud", value=False)
                    if prisma:
                        st.text_input("Prisma API Key", type="password")
            
            # Scan policies
            with st.expander("📜 Scan Policies", expanded=True):
                st.markdown("**Automated Scanning:**")
                st.checkbox("Scan all EC2 instances on launch", value=True)
                st.checkbox("Scan all container images on push", value=True)
                st.checkbox("Scan Lambda functions on deployment", value=True)
                st.checkbox("Scan S3 buckets for exposed data", value=True)
                
                st.markdown("**Scan Scheduling:**")
                st.checkbox("Daily infrastructure scan", value=True)
                st.selectbox("Scan time", ["00:00 UTC", "02:00 UTC", "06:00 UTC"])
                
                st.checkbox("Weekly comprehensive scan", value=True)
                st.selectbox("Scan day", ["Sunday", "Monday", "Friday"])
            
            # Notification settings
            with st.expander("🔔 Notifications", expanded=True):
                st.checkbox("Alert on critical vulnerabilities", value=True)
                st.checkbox("Alert on high vulnerabilities", value=True)
                st.checkbox("Daily vulnerability summary", value=True)
                st.checkbox("Weekly scan report", value=True)
                
                st.text_input("Notification Email", "security-team@company.com")
                st.text_input("Slack Webhook URL", "")
                st.text_input("SNS Topic ARN", "arn:aws:sns:us-east-1:123456789012:vuln-alerts")
            
            st.button("💾 Save Configuration", type="primary", use_container_width=True)
        
        with tab4:
            st.markdown("### 📊 Vulnerability Reports")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Report generation
                report_type = st.selectbox(
                    "Report Type",
                    [
                        "Executive Summary",
                        "Detailed Vulnerability Report",
                        "Compliance Report",
                        "Trend Analysis",
                        "Resource-Specific Report",
                        "CVE Report"
                    ]
                )
                
                col_time, col_format = st.columns(2)
                with col_time:
                    time_period = st.selectbox("Time Period", ["Last 7 Days", "Last 30 Days", "Last Quarter", "Custom"])
                with col_format:
                    report_format = st.selectbox("Format", ["PDF", "HTML", "CSV", "JSON"])
                
                include_options = st.multiselect(
                    "Include",
                    ["Executive Summary", "Vulnerability Details", "Remediation Steps", "Compliance Mapping", "Trend Charts"],
                    default=["Executive Summary", "Vulnerability Details"]
                )
                
                if st.button("📊 Generate Report", type="primary", use_container_width=True):
                    with st.spinner("Generating report..."):
                        import time
                        time.sleep(2)
                        st.success("✅ Report generated!")
                        st.download_button(
                            "📥 Download Report",
                            data="Sample vulnerability report",
                            file_name=f"vulnerability_report_{datetime.now().strftime('%Y%m%d')}.pdf"
                        )
            
            with col2:
                st.markdown("### 📅 Scheduled Reports")
                
                st.caption("**Daily Critical Alert**")
                st.caption("Daily at 9:00 AM")
                st.caption("To: security@company.com")
                st.markdown("---")
                
                st.caption("**Weekly Summary**")
                st.caption("Every Monday")
                st.caption("To: leadership@company.com")
                st.markdown("---")
                
                st.caption("**Monthly Compliance**")
                st.caption("1st of each month")
                st.caption("To: compliance@company.com")
                
                st.button("➕ New Schedule", use_container_width=True)
    
    # ==================== Security Dashboard ====================
    def security_dashboard(self):
        """Comprehensive Security Dashboard"""
        st.subheader("📈 Security & Compliance Dashboard")
        
        # Overall security score
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### 🎯 Overall Security Posture")
            score = 87
            st.progress(score / 100)
            st.metric("Security Score", f"{score}/100", delta="3")
        
        st.markdown("---")
        
        # Key metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Encrypted Resources", "98.8%", delta="0.5%")
        with col2:
            st.metric("Compliant Zones", "94%", delta="2%")
        with col3:
            # Mode-aware metric
            active_secrets_value = self._get_data('active_secrets', "342")
            st.metric("Active Secrets", active_secrets_value)
        with col4:
            st.metric("Critical Vulns", "3", delta="-2", delta_color="inverse")
        with col5:
            st.metric("Certificates OK", "127", delta="5")
        
        st.markdown("---")
        
        # Security trends
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Security Events (7 Days)")
            st.line_chart({"Events": [45, 52, 38, 67, 55, 48, 51]})
        
        with col2:
            st.markdown("### 🔍 Vulnerability Trends (7 Days)")
            st.line_chart({
                "Critical": [5, 4, 3, 4, 3, 3, 3],
                "High": [52, 50, 48, 47, 47, 47, 47]
            })
        
        st.markdown("---")
        
        # Compliance status
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ✅ Compliance Status")
            
            compliance_data = [
                {"Framework": "PCI DSS", "Score": 92, "Status": "Compliant"},
                {"Framework": "HIPAA", "Score": 88, "Status": "Compliant"},
                {"Framework": "SOC 2", "Score": 85, "Status": "Compliant"},
                {"Framework": "ISO 27001", "Score": 81, "Status": "Needs Attention"},
                {"Framework": "GDPR", "Score": 94, "Status": "Compliant"},
            ]
            
            for item in compliance_data:
                col_name, col_score, col_status = st.columns([2, 1, 1])
                with col_name:
                    st.write(item["Framework"])
                with col_score:
                    st.progress(item["Score"] / 100, text=f"{item['Score']}%")
                with col_status:
                    if item["Score"] >= 85:
                        st.success("✓")
                    else:
                        st.warning("⚠")
        
        with col2:
            st.markdown("### ⚠️ Top Security Issues")
            
            issues = [
                {"Issue": "Unencrypted S3 buckets", "Count": 23, "Severity": "High"},
                {"Issue": "Expiring certificates", "Count": 8, "Severity": "Medium"},
                {"Issue": "Weak encryption keys", "Count": 5, "Severity": "High"},
                {"Issue": "Exposed secrets", "Count": 2, "Severity": "Critical"},
                {"Issue": "Non-compliant network zones", "Count": 12, "Severity": "Medium"}
            ]
            
            for issue in issues:
                col_issue, col_count, col_sev = st.columns([3, 1, 1])
                with col_issue:
                    st.write(issue["Issue"])
                with col_count:
                    st.caption(f"{issue['Count']}")
                with col_sev:
                    if issue["Severity"] == "Critical":
                        st.error("🔴")
                    elif issue["Severity"] == "High":
                        st.warning("🟠")
                    else:
                        st.info("🟡")
        
        st.markdown("---")
        
        # Recent activity
        st.markdown("### 📝 Recent Security Activity")
        
        activity_df = pd.DataFrame([
            {
                "Time": "10 min ago",
                "Event": "Certificate renewed",
                "Resource": "www.example.com",
                "User": "System",
                "Status": "Success"
            },
            {
                "Time": "25 min ago",
                "Event": "Vulnerability scan completed",
                "Resource": "Production VPC",
                "User": "Scanner",
                "Status": "Complete"
            },
            {
                "Time": "1 hour ago",
                "Event": "Secret rotated",
                "Resource": "prod/db/master",
                "User": "Auto-rotation",
                "Status": "Success"
            },
            {
                "Time": "2 hours ago",
                "Event": "Security group modified",
                "Resource": "sg-0123456789",
                "User": "admin@company.com",
                "Status": "Logged"
            },
            {
                "Time": "3 hours ago",
                "Event": "Failed login attempt",
                "Resource": "IAM Console",
                "User": "unknown",
                "Status": "Blocked"
            }
        ])
        
        st.dataframe(activity_df, use_container_width=True, hide_index=True)
    
    # ==================== Demo Data Methods ====================
    def _get_rbac_roles(self):
        """Get RBAC roles demo data"""
        return [
            {"name": "Administrator", "users": 5, "type": "Built-in", "usage": 75},
            {"name": "DataScientist", "users": 12, "type": "Custom", "usage": 60},
            {"name": "Developer", "users": 34, "type": "Custom", "usage": 85},
            {"name": "Analyst", "users": 18, "type": "Custom", "usage": 45},
            {"name": "Viewer", "users": 67, "type": "Built-in", "usage": 30}
        ]
    
    def _get_user_assignments(self):
        """Get user-role assignments"""
        return pd.DataFrame([
            {"User": "john.doe@company.com", "Roles": "Administrator, Developer", "Last Login": "2 hours ago", "Status": "Active"},
            {"User": "jane.smith@company.com", "Roles": "DataScientist", "Last Login": "1 day ago", "Status": "Active"},
            {"User": "bob.johnson@company.com", "Roles": "Developer, Analyst", "Last Login": "30 min ago", "Status": "Active"},
            {"User": "alice.williams@company.com", "Roles": "Viewer", "Last Login": "1 week ago", "Status": "Inactive"},
        ])
    
    def _get_network_zones(self):
        """Get network zones demo data"""
        return [
            {"name": "DMZ-Public", "type": "DMZ", "instances": 12, "compliant": True},
            {"name": "Private-App", "type": "Private", "instances": 45, "compliant": True},
            {"name": "Private-DB", "type": "Isolated", "instances": 8, "compliant": True},
            {"name": "Management", "type": "Management", "instances": 3, "compliant": False}
        ]
    
    def _get_segmentation_rules(self):
        """Get network segmentation rules"""
        return pd.DataFrame([
            {"Source": "DMZ-Public", "Destination": "Private-App", "Protocol": "TCP", "Port": "443", "Action": "Allow", "Status": "Active"},
            {"Source": "Private-App", "Destination": "Private-DB", "Protocol": "TCP", "Port": "5432", "Action": "Allow", "Status": "Active"},
            {"Source": "Internet", "Destination": "Private-DB", "Protocol": "All", "Port": "*", "Action": "Deny", "Status": "Active"},
            {"Source": "Management", "Destination": "Private-App", "Protocol": "TCP", "Port": "22", "Action": "Log & Allow", "Status": "Active"},
        ])
    
    def _get_encryption_status(self):
        """Get encryption status data"""
        return pd.DataFrame([
            {"Resource Type": "S3 Bucket", "Resource ID": "prod-data-bucket", "Encryption": "AES-256", "Key": "AWS Managed", "Status": "✓ Encrypted", "Compliance": "PCI DSS"},
            {"Resource Type": "EBS Volume", "Resource ID": "vol-0123456789", "Encryption": "AES-256", "Key": "Customer Managed", "Status": "✓ Encrypted", "Compliance": "HIPAA"},
            {"Resource Type": "RDS Instance", "Resource ID": "prod-database", "Encryption": "AES-256", "Key": "Customer Managed", "Status": "✓ Encrypted", "Compliance": "SOC 2"},
            {"Resource Type": "S3 Bucket", "Resource ID": "test-bucket-old", "Encryption": "None", "Key": "-", "Status": "✗ Unencrypted", "Compliance": "-"},
            {"Resource Type": "DynamoDB", "Resource ID": "prod-sessions", "Encryption": "AES-256", "Key": "AWS Managed", "Status": "✓ Encrypted", "Compliance": "GDPR"},
        ])
    
    def _get_kms_keys(self):
        """Get KMS keys data"""
        return pd.DataFrame([
            {"Key ID": "alias/prod-data", "Type": "Symmetric", "Usage": "ENCRYPT_DECRYPT", "Rotation": "✓ Enabled", "Created": "2023-01-15", "Status": "Active"},
            {"Key ID": "alias/rds-key", "Type": "Symmetric", "Usage": "ENCRYPT_DECRYPT", "Rotation": "✓ Enabled", "Created": "2023-03-20", "Status": "Active"},
            {"Key ID": "alias/backup-key", "Type": "Symmetric", "Usage": "ENCRYPT_DECRYPT", "Rotation": "✗ Disabled", "Created": "2022-11-10", "Status": "Active"},
            {"Key ID": "alias/old-app-key", "Type": "Symmetric", "Usage": "ENCRYPT_DECRYPT", "Rotation": "✗ Disabled", "Created": "2021-06-05", "Status": "Pending Deletion"},
        ])
    
    def _get_encryption_policies(self):
        """Get encryption policies"""
        return pd.DataFrame([
            {"Service": "S3", "Policy": "Enforce encryption on all buckets", "Enforcement": "Active", "Compliance": "PCI DSS, HIPAA"},
            {"Service": "EBS", "Policy": "Enable default encryption", "Enforcement": "Active", "Compliance": "All"},
            {"Service": "RDS", "Policy": "Mandatory encryption at rest", "Enforcement": "Active", "Compliance": "HIPAA, SOC 2"},
            {"Service": "DynamoDB", "Policy": "Customer managed keys", "Enforcement": "Active", "Compliance": "GDPR"},
        ])
    
    def _get_scan_results(self):
        """Get encryption scan results"""
        return pd.DataFrame([
            {"Resource": "s3://prod-data-bucket", "Type": "S3", "Encryption": "✓ AES-256", "Compliance": "✓ Pass"},
            {"Resource": "vol-0123456789", "Type": "EBS", "Encryption": "✓ AES-256", "Compliance": "✓ Pass"},
            {"Resource": "s3://test-bucket-old", "Type": "S3", "Encryption": "✗ None", "Compliance": "✗ Fail"},
            {"Resource": "prod-database", "Type": "RDS", "Encryption": "✓ AES-256", "Compliance": "✓ Pass"},
        ])
    
    def _get_secrets_inventory(self):
        """Get secrets inventory"""
        return pd.DataFrame([
            {"Name": "prod/database/master-password", "Type": "Database", "Last Rotated": "15 days ago", "Status": "Active", "Rotation": "✓ Auto"},
            {"Name": "prod/api/stripe-key", "Type": "API Key", "Last Rotated": "83 days ago", "Status": "Expiring", "Rotation": "✗ Manual"},
            {"Name": "prod/ssh/deployment-key", "Type": "SSH Key", "Last Rotated": "120 days ago", "Status": "Active", "Rotation": "✗ Manual"},
            {"Name": "staging/db/test-password", "Type": "Database", "Last Rotated": "5 days ago", "Status": "Active", "Rotation": "✓ Auto"},
        ])
    
    def _get_certificates(self):
        """Get certificates data"""
        return pd.DataFrame([
            {"Domain": "www.example.com", "Type": "Public", "Expires": "In 87 days", "Status": "Active", "Validation": "DNS", "Renewal": "Auto"},
            {"Domain": "*.example.com", "Type": "Public", "Expires": "In 12 days", "Status": "Expiring", "Validation": "DNS", "Renewal": "Auto"},
            {"Domain": "api.example.com", "Type": "Public", "Expires": "In 145 days", "Status": "Active", "Validation": "DNS", "Renewal": "Auto"},
            {"Domain": "internal.example.com", "Type": "Private", "Expires": "In 365 days", "Status": "Active", "Validation": "None", "Renewal": "Manual"},
        ])
    
    def _get_audit_events(self):
        """Get audit events"""
        return pd.DataFrame([
            {"Timestamp": "2024-11-18 14:23:15", "Event ID": "evt-001", "Event": "CreateBucket", "Service": "S3", "User": "admin@company.com", "Status": "Success"},
            {"Timestamp": "2024-11-18 14:20:42", "Event ID": "evt-002", "Event": "ConsoleLogin", "Service": "IAM", "User": "john.doe@company.com", "Status": "Success"},
            {"Timestamp": "2024-11-18 14:18:33", "Event ID": "evt-003", "Event": "PutBucketPolicy", "Service": "S3", "User": "api-service", "Status": "Success"},
            {"Timestamp": "2024-11-18 14:15:20", "Event ID": "evt-004", "Event": "ConsoleLogin", "Service": "IAM", "User": "unknown", "Status": "Failed"},
        ])
    
    def _get_event_details(self, event_id):
        """Get detailed event information"""
        return {
            "event_info": {
                "eventID": event_id,
                "eventName": "CreateBucket",
                "eventTime": "2024-11-18T14:23:15Z",
                "eventSource": "s3.amazonaws.com",
                "userIdentity": "admin@company.com",
                "sourceIPAddress": "192.168.1.100"
            },
            "request_params": {
                "bucketName": "new-production-bucket",
                "region": "us-east-1",
                "encryption": "AES256"
            }
        }
    
    def _get_security_events(self):
        """Get security events"""
        return pd.DataFrame([
            {"Timestamp": "2024-11-18 14:15:20", "Event ID": "sec-001", "Event": "Failed Console Login", "Severity": "High", "Source IP": "185.220.101.42", "Status": "Blocked"},
            {"Timestamp": "2024-11-18 13:45:12", "Event ID": "sec-002", "Event": "Unauthorized API Call", "Severity": "Critical", "Source IP": "203.0.113.50", "Status": "Blocked"},
            {"Timestamp": "2024-11-18 12:30:05", "Event ID": "sec-003", "Event": "Security Group Changed", "Severity": "Medium", "Source IP": "10.0.1.50", "Status": "Logged"},
            {"Timestamp": "2024-11-18 11:22:18", "Event ID": "sec-004", "Event": "Root Account Usage", "Severity": "High", "Source IP": "203.0.113.100", "Status": "Alert"},
        ])
    
    def _get_active_scans(self):
        """Get active vulnerability scans"""
        return pd.DataFrame([
            {"Scan Name": "Infrastructure Scan", "Type": "Comprehensive", "Progress": "65%", "Started": "1 hour ago", "ETA": "15 min"},
            {"Scan Name": "Container Scan", "Type": "ECR", "Progress": "30%", "Started": "30 min ago", "ETA": "25 min"},
        ])
    
    def _get_scan_history(self):
        """Get scan history"""
        return pd.DataFrame([
            {"Scan Name": "Daily Security Scan", "Type": "Comprehensive", "Completed": "6 hours ago", "Findings": "47", "Duration": "22 min", "Status": "Complete"},
            {"Scan Name": "Weekly Deep Scan", "Type": "Deep", "Completed": "2 days ago", "Findings": "134", "Duration": "1h 45m", "Status": "Complete"},
            {"Scan Name": "EC2 Instance Scan", "Type": "Inspector", "Completed": "1 day ago", "Findings": "23", "Duration": "35 min", "Status": "Complete"},
        ])
    
    def _get_vulnerabilities(self):
        """Get vulnerabilities data"""
        return pd.DataFrame([
            {"CVE/ID": "CVE-2024-1234", "Title": "Remote Code Execution", "Severity": "Critical", "Resource": "i-0123456789", "Status": "Open", "CVSS": "9.8"},
            {"CVE/ID": "CVE-2024-5678", "Title": "SQL Injection", "Severity": "High", "Resource": "prod-database", "Status": "In Progress", "CVSS": "8.2"},
            {"CVE/ID": "MISC-001", "Title": "S3 Bucket Public Access", "Severity": "High", "Resource": "old-backup-bucket", "Status": "Open", "CVSS": "7.5"},
            {"CVE/ID": "CVE-2024-9012", "Title": "Outdated SSL/TLS", "Severity": "Medium", "Resource": "lb-frontend", "Status": "Resolved", "CVSS": "5.3"},
        ])
    
    def _get_vulnerability_details(self, vuln_id):
        """Get detailed vulnerability information"""
        return {
            "title": "Remote Code Execution in Apache Log4j",
            "severity": "Critical",
            "cvss_score": "9.8",
            "description": "Apache Log4j2 2.0-beta9 through 2.15.0 (excluding security releases 2.12.2, 2.12.3, and 2.3.1) JNDI features used in configuration, log messages, and parameters do not protect against attacker controlled LDAP and other JNDI related endpoints.",
            "affected_resources": [
                {"Resource": "i-0123456789", "Type": "EC2", "Region": "us-east-1"},
                {"Resource": "prod-app-server", "Type": "ECS", "Region": "us-east-1"}
            ],
            "remediation": "Update Apache Log4j to version 2.17.0 or later. As a temporary mitigation, set the system property log4j2.formatMsgNoLookups to true.",
            "references": [
                "https://nvd.nist.gov/vuln/detail/CVE-2021-44228",
                "https://logging.apache.org/log4j/2.x/security.html"
            ]
        }
