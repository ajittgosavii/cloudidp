"""Policy & Guardrails Module - Comprehensive Policy Management"""

import streamlit as st
from typing import Dict, List, Any
from demo_data import DemoDataProvider
from anthropic_helper import AnthropicHelper

class PolicyGuardrailsModule:
    """Policy & Guardrails Module with comprehensive policy management"""
    
    def __init__(self):
        self.demo_data = DemoDataProvider()
    
    def render_overview(self):
        """Render Policy & Guardrails overview"""
        st.title("🛡️ Policy & Guardrails")
        st.markdown("### Automated Policy Enforcement & Compliance Guardrails")
        
        # Mode indicator
        if st.session_state.demo_mode:
            st.info("📋 **Demo Mode**: Viewing sample policy configurations")
        else:
            st.success("🟢 **Live Mode**: Connected to real AWS Organizations")
        
        # Overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Active Policies", "147", "+12")
        with col2:
            st.metric("Compliance Rate", "94.2%", "+2.1%")
        with col3:
            st.metric("Violations Today", "23", "-8")
        with col4:
            st.metric("Auto-Remediated", "18", "+5")
        
        st.markdown("---")
        
        # Key capabilities
        st.markdown("### 🎯 Key Capabilities")
        
        capabilities = {
            "Policy as Code Engine": {
                "icon": "📜",
                "desc": "Version-controlled policies using OPA/Cedar",
                "features": ["YAML/JSON definitions", "GitOps workflow", "CI/CD integration"]
            },
            "Cross-Cloud Consistency": {
                "icon": "🌐",
                "desc": "Unified policies across AWS, Azure, GCP",
                "features": ["Multi-cloud support", "Single source of truth", "Centralized management"]
            },
            "Tag Enforcement": {
                "icon": "🏷️",
                "desc": "Automated tag policy validation",
                "features": ["Required tags", "Tag inheritance", "Cost allocation"]
            },
            "Naming Conventions": {
                "icon": "📝",
                "desc": "Enforce naming standards & placement rules",
                "features": ["Regex patterns", "Resource type rules", "Auto-validation"]
            },
            "Quota Management": {
                "icon": "⚖️",
                "desc": "Proactive quota monitoring & enforcement",
                "features": ["Service limits", "Threshold alerts", "Auto-requests"]
            }
        }
        
        cols = st.columns(2)
        for idx, (title, details) in enumerate(capabilities.items()):
            with cols[idx % 2]:
                with st.expander(f"{details['icon']} {title}", expanded=False):
                    st.markdown(f"**{details['desc']}**")
                    for feature in details['features']:
                        st.markdown(f"- {feature}")
        
        # Architecture diagram
        st.markdown("---")
        st.markdown("### 🏗️ Policy & Guardrails Architecture")
        
        architecture_code = '''
┌─────────────────────────────────────────────────────────────────┐
│                    POLICY & GUARDRAILS LAYER                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌───────────────┐  ┌──────────────┐  ┌───────────────────┐   │
│  │ Policy Engine │  │ Compliance   │  │  Enforcement      │   │
│  │  (OPA/Cedar)  │  │   Scanner    │  │    Actions        │   │
│  └───────┬───────┘  └──────┬───────┘  └────────┬──────────┘   │
│          │                  │                     │              │
│  ┌───────▼──────────────────▼─────────────────────▼─────────┐  │
│  │              POLICY DECISION POINT (PDP)                  │  │
│  │    • Evaluate policies • Check violations • Actions       │  │
│  └───────────────────────────┬───────────────────────────────┘  │
│                               │                                  │
│  ┌────────────────────────────▼──────────────────────────────┐  │
│  │              ENFORCEMENT POINTS                           │  │
│  ├─────────────┬──────────────┬─────────────┬────────────────┤  │
│  │ Tag Policy  │   Naming     │   Quota     │   Placement    │  │
│  │ Enforcement │  Conventions │  Guardrails │   Rules        │  │
│  └─────────────┴──────────────┴─────────────┴────────────────┘  │
│                               │                                  │
│  ┌────────────────────────────▼──────────────────────────────┐  │
│  │         AWS Organizations / SCPs / Config Rules          │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
        '''
        st.code(architecture_code, language='text')
        
        # Recent activity
        st.markdown("---")
        st.markdown("### 📊 Recent Policy Activity")
        
        activities = self.demo_data.get_policy_activities()
        
        for activity in activities[:5]:
            status_icon = "✅" if activity['status'] == "Compliant" else "⚠️"
            with st.expander(f"{status_icon} {activity['policy']} - {activity['resource']}", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Action:** {activity['action']}")
                    st.markdown(f"**Timestamp:** {activity['timestamp']}")
                with col2:
                    st.markdown(f"**User:** {activity['user']}")
                    st.markdown(f"**Status:** {activity['status']}")
    
    def render_policy_as_code(self):
        """Policy as Code Engine"""
        st.title("📜 Policy as Code Engine")
        st.markdown("### Version-Controlled Policy Definitions")
        
        if st.session_state.demo_mode:
            st.info("📋 **Demo Mode**: Viewing sample policies")
        
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Policy Library", "✏️ Create Policy", "🔄 Version Control", "🧪 Testing"])
        
        with tab1:
            self._render_policy_library()
        
        with tab2:
            self._render_create_policy()
        
        with tab3:
            self._render_version_control()
        
        with tab4:
            self._render_policy_testing()
    
    def _render_policy_library(self):
        """Render policy library"""
        st.markdown("### 📚 Policy Library")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            policy_type = st.selectbox("Policy Type", ["All", "Tag", "Naming", "Security", "Cost", "Compliance"])
        with col2:
            status = st.selectbox("Status", ["All", "Active", "Draft", "Deprecated"])
        with col3:
            framework = st.selectbox("Framework", ["All", "AWS", "Azure", "GCP", "Multi-Cloud"])
        
        # Policy list
        policies = self.demo_data.get_policy_as_code()
        
        for policy in policies:
            with st.expander(f"📜 {policy['name']} (v{policy['version']})", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Description:** {policy['description']}")
                    st.markdown(f"**Type:** {policy['type']}")
                    st.markdown(f"**Language:** {policy['language']}")
                    st.markdown(f"**Scope:** {policy['scope']}")
                
                with col2:
                    st.markdown(f"**Status:** {policy['status']}")
                    st.markdown(f"**Author:** {policy['author']}")
                    st.markdown(f"**Last Updated:** {policy['last_updated']}")
                    st.markdown(f"**Resources:** {policy['resources_affected']}")
                
                # Policy code
                st.markdown("**Policy Code:**")
                st.code(policy['policy_code'], language='yaml')
                
                # Actions
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.button(f"✏️ Edit", key=f"edit_{policy['id']}")
                with col2:
                    st.button(f"🧪 Test", key=f"test_{policy['id']}")
                with col3:
                    st.button(f"🚀 Deploy", key=f"deploy_{policy['id']}")
    
    def _render_create_policy(self):
        """Create new policy"""
        st.markdown("### ✏️ Create New Policy")
        
        col1, col2 = st.columns(2)
        
        with col1:
            policy_name = st.text_input("Policy Name", "my-policy")
            policy_type = st.selectbox("Policy Type", ["Tag Policy", "Naming Policy", "Security Policy", "Cost Policy", "Quota Policy"])
            language = st.selectbox("Policy Language", ["OPA (Rego)", "Cedar", "Python", "JSON Schema"])
        
        with col2:
            version = st.text_input("Version", "1.0.0")
            scope = st.selectbox("Scope", ["Organization", "OU", "Account", "Resource"])
            enforcement = st.selectbox("Enforcement", ["Mandatory", "Advisory", "Audit Only"])
        
        description = st.text_area("Description", "Policy description here...")
        
        st.markdown("**Policy Definition:**")
        
        # Template selection
        template = st.selectbox("Start from Template", [
            "Blank",
            "Tag Enforcement Template",
            "Naming Convention Template",
            "Security Baseline Template",
            "Cost Optimization Template"
        ])
        
        # Policy editor
        default_policy = '''package aws.tagging

deny[msg] {
    input.resource_type == "aws_instance"
    not input.tags.Environment
    msg = "EC2 instances must have Environment tag"
}

deny[msg] {
    input.resource_type == "aws_instance"
    not input.tags.Owner
    msg = "EC2 instances must have Owner tag"
}'''
        
        policy_code = st.text_area("Policy Code", default_policy, height=300)
        
        # Test data
        st.markdown("**Test Data (Optional):**")
        test_data = st.text_area("Test Input JSON", '''{
  "resource_type": "aws_instance",
  "tags": {
    "Environment": "production"
  }
}''', height=150)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("💾 Save as Draft"):
                st.success("✅ Policy saved as draft")
        with col2:
            if st.button("🧪 Validate"):
                st.success("✅ Policy syntax valid")
        with col3:
            if st.button("🚀 Publish"):
                st.success("✅ Policy published successfully")
    
    def _render_version_control(self):
        """Version control for policies"""
        st.markdown("### 🔄 Policy Version Control")
        
        # Git integration status
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Commits", "1,247")
        with col2:
            st.metric("Active Branches", "8")
        with col3:
            st.metric("Pending PRs", "3")
        
        st.markdown("---")
        
        # Version history
        st.markdown("**Recent Changes:**")
        
        versions = self.demo_data.get_policy_versions()
        
        for version in versions:
            with st.expander(f"v{version['version']} - {version['commit_message']}", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Author:** {version['author']}")
                    st.markdown(f"**Date:** {version['date']}")
                    st.markdown(f"**Branch:** {version['branch']}")
                with col2:
                    st.markdown(f"**Changes:** {version['changes']}")
                    st.markdown(f"**Status:** {version['status']}")
                
                # Diff view
                if st.button(f"View Diff", key=f"diff_{version['version']}"):
                    st.code(version['diff'], language='diff')
    
    def _render_policy_testing(self):
        """Policy testing framework"""
        st.markdown("### 🧪 Policy Testing Framework")
        
        st.markdown("Test your policies before deployment")
        
        # Test suite
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("**Select Policy to Test:**")
            policy = st.selectbox("Policy", ["Production Tagging Policy", "EC2 Naming Convention", "S3 Encryption Policy"])
            
            st.markdown("**Test Scenarios:**")
            scenarios = st.multiselect("Scenarios", [
                "Valid resource configuration",
                "Missing required tags",
                "Invalid naming format",
                "Non-compliant encryption",
                "Quota exceeded"
            ], default=["Valid resource configuration"])
        
        with col2:
            st.markdown("**Test Configuration:**")
            test_env = st.selectbox("Test Environment", ["Development", "Staging", "Production"])
            auto_fix = st.checkbox("Enable Auto-Remediation Suggestions", value=True)
        
        if st.button("▶️ Run Tests"):
            st.markdown("---")
            st.markdown("**Test Results:**")
            
            results = [
                {"scenario": "Valid resource configuration", "status": "✅ PASS", "time": "0.23s"},
                {"scenario": "Missing required tags", "status": "⚠️ VIOLATION", "time": "0.18s"},
                {"scenario": "Invalid naming format", "status": "⚠️ VIOLATION", "time": "0.21s"},
            ]
            
            for result in results:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.markdown(f"**{result['scenario']}**")
                with col2:
                    st.markdown(result['status'])
                with col3:
                    st.markdown(result['time'])
            
            st.success("✅ Test suite completed: 1 passed, 2 violations detected")
    
    def render_cross_cloud_policy(self):
        """Cross-Cloud Policy Consistency"""
        st.title("🌐 Cross-Cloud Policy Consistency")
        st.markdown("### Unified Policy Management Across Cloud Providers")
        
        if st.session_state.demo_mode:
            st.info("📋 **Demo Mode**: Viewing multi-cloud policy mappings")
        
        tab1, tab2, tab3 = st.tabs(["🗺️ Policy Mapping", "🔄 Sync Status", "📊 Compliance Matrix"])
        
        with tab1:
            self._render_policy_mapping()
        
        with tab2:
            self._render_sync_status()
        
        with tab3:
            self._render_compliance_matrix()
    
    def _render_policy_mapping(self):
        """Policy mapping across clouds"""
        st.markdown("### 🗺️ Cross-Cloud Policy Mapping")
        
        # Cloud provider selection
        col1, col2, col3 = st.columns(3)
        with col1:
            aws_enabled = st.checkbox("AWS", value=True)
        with col2:
            azure_enabled = st.checkbox("Azure", value=True)
        with col3:
            gcp_enabled = st.checkbox("GCP", value=True)
        
        st.markdown("---")
        
        # Policy mappings
        mappings = self.demo_data.get_cross_cloud_mappings()
        
        for mapping in mappings:
            with st.expander(f"🔗 {mapping['policy_name']}", expanded=False):
                st.markdown(f"**Description:** {mapping['description']}")
                
                # Cloud-specific implementations
                cols = st.columns(3)
                
                if aws_enabled:
                    with cols[0]:
                        st.markdown("**AWS Implementation:**")
                        st.code(mapping['aws_implementation'], language='yaml')
                
                if azure_enabled:
                    with cols[1]:
                        st.markdown("**Azure Implementation:**")
                        st.code(mapping['azure_implementation'], language='yaml')
                
                if gcp_enabled:
                    with cols[2]:
                        st.markdown("**GCP Implementation:**")
                        st.code(mapping['gcp_implementation'], language='yaml')
                
                # Sync status
                st.markdown("**Sync Status:**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"✅ AWS: {mapping['aws_status']}")
                with col2:
                    st.markdown(f"✅ Azure: {mapping['azure_status']}")
                with col3:
                    st.markdown(f"✅ GCP: {mapping['gcp_status']}")
    
    def _render_sync_status(self):
        """Policy sync status"""
        st.markdown("### 🔄 Policy Synchronization Status")
        
        # Sync metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Synced Policies", "127")
        with col2:
            st.metric("Pending Sync", "5")
        with col3:
            st.metric("Failed Sync", "2")
        with col4:
            st.metric("Last Sync", "2m ago")
        
        st.markdown("---")
        
        # Sync history
        sync_history = self.demo_data.get_sync_history()
        
        for sync in sync_history:
            status_icon = "✅" if sync['status'] == "Success" else "❌"
            with st.expander(f"{status_icon} {sync['policy']} - {sync['timestamp']}", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Clouds:** {sync['clouds']}")
                    st.markdown(f"**Duration:** {sync['duration']}")
                with col2:
                    st.markdown(f"**Status:** {sync['status']}")
                    st.markdown(f"**Resources:** {sync['resources_updated']}")
                
                if sync['status'] == "Failed":
                    st.error(f"**Error:** {sync.get('error', 'Unknown error')}")
        
        if st.button("🔄 Sync All Policies Now"):
            with st.spinner("Synchronizing policies..."):
                import time
                time.sleep(2)
            st.success("✅ All policies synchronized successfully")
    
    def _render_compliance_matrix(self):
        """Compliance matrix across clouds"""
        st.markdown("### 📊 Cross-Cloud Compliance Matrix")
        
        import pandas as pd
        
        # Compliance data
        compliance_data = {
            "Policy": ["Encryption at Rest", "MFA Required", "Network Segmentation", "Logging Enabled", "Backup Policy"],
            "AWS": ["✅ 98%", "✅ 96%", "⚠️ 87%", "✅ 99%", "✅ 94%"],
            "Azure": ["✅ 95%", "✅ 94%", "✅ 92%", "✅ 97%", "⚠️ 88%"],
            "GCP": ["✅ 97%", "✅ 95%", "✅ 91%", "✅ 98%", "✅ 93%"],
            "Overall": ["✅ 97%", "✅ 95%", "⚠️ 90%", "✅ 98%", "✅ 92%"]
        }
        
        df = pd.DataFrame(compliance_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Detailed violations
        st.markdown("**Top Violations by Cloud:**")
        
        violations = {
            "AWS": [
                {"resource": "ec2-instance-i-12345", "policy": "Network Segmentation", "severity": "Medium"},
                {"resource": "s3-bucket-data-2023", "policy": "Backup Policy", "severity": "Low"}
            ],
            "Azure": [
                {"resource": "vm-prod-web-01", "policy": "Backup Policy", "severity": "Medium"},
                {"resource": "storage-account-logs", "policy": "Encryption at Rest", "severity": "High"}
            ],
            "GCP": [
                {"resource": "compute-instance-prod", "policy": "Network Segmentation", "severity": "Low"}
            ]
        }
        
        for cloud, items in violations.items():
            st.markdown(f"**{cloud}:**")
            for item in items:
                severity_color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
                st.markdown(f"{severity_color[item['severity']]} `{item['resource']}` - {item['policy']}")
    
    def render_tag_enforcement(self):
        """Tag Policy Enforcement"""
        st.title("🏷️ Tag Policy Enforcement")
        st.markdown("### Automated Tag Validation & Compliance")
        
        if st.session_state.demo_mode:
            st.info("📋 **Demo Mode**: Viewing tag policy configurations")
        
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Tag Policies", "✅ Validation", "📊 Compliance", "🔧 Remediation"])
        
        with tab1:
            self._render_tag_policies()
        
        with tab2:
            self._render_tag_validation()
        
        with tab3:
            self._render_tag_compliance()
        
        with tab4:
            self._render_tag_remediation()
    
    def _render_tag_policies(self):
        """Tag policies management"""
        st.markdown("### 📋 Tag Policy Definitions")
        
        policies = self.demo_data.get_tag_enforcement_policies()
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Active Policies", "12")
        with col2:
            st.metric("Required Tags", "8")
        with col3:
            st.metric("Optional Tags", "15")
        with col4:
            st.metric("Compliance Rate", "91.3%")
        
        st.markdown("---")
        
        # Policy list
        for policy in policies:
            with st.expander(f"🏷️ {policy['name']}", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Scope:** {policy['scope']}")
                    st.markdown(f"**Enforcement:** {policy['enforcement']}")
                    st.markdown(f"**Status:** {policy['status']}")
                
                with col2:
                    st.markdown(f"**Resources:** {policy['resource_types']}")
                    st.markdown(f"**Created:** {policy['created']}")
                    st.markdown(f"**Updated:** {policy['updated']}")
                
                # Required tags
                st.markdown("**Required Tags:**")
                for tag in policy['required_tags']:
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.code(tag['key'])
                    with col2:
                        st.markdown(f"{tag['description']} • Pattern: `{tag.get('pattern', '*')}`")
                
                # Optional tags
                if policy['optional_tags']:
                    st.markdown("**Optional Tags:**")
                    for tag in policy['optional_tags']:
                        st.markdown(f"- `{tag['key']}`: {tag['description']}")
    
    def _render_tag_validation(self):
        """Tag validation"""
        st.markdown("### ✅ Tag Validation Engine")
        
        st.markdown("Validate resource tags against policies")
        
        # Validation options
        col1, col2 = st.columns(2)
        with col1:
            resource_type = st.selectbox("Resource Type", ["All", "EC2", "S3", "RDS", "Lambda", "EKS"])
        with col2:
            account = st.selectbox("Account", ["All Accounts", "Production", "Development", "Staging"])
        
        if st.button("🔍 Run Validation"):
            with st.spinner("Validating tags..."):
                import time
                time.sleep(2)
            
            st.markdown("---")
            st.markdown("**Validation Results:**")
            
            # Results summary
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Resources Scanned", "1,234")
            with col2:
                st.metric("Compliant", "1,127", "+45")
            with col3:
                st.metric("Non-Compliant", "107", "-12")
            with col4:
                st.metric("Compliance Rate", "91.3%", "+1.2%")
            
            st.markdown("---")
            
            # Violations
            st.markdown("**Top Violations:**")
            
            violations = [
                {"resource": "i-0abc123def456", "type": "EC2", "missing": ["CostCenter", "Owner"], "severity": "High"},
                {"resource": "my-data-bucket-2023", "type": "S3", "missing": ["Environment"], "severity": "Medium"},
                {"resource": "prod-db-cluster", "type": "RDS", "missing": ["BackupPolicy"], "severity": "Medium"},
            ]
            
            for violation in violations:
                col1, col2, col3, col4 = st.columns([2, 1, 2, 1])
                with col1:
                    st.markdown(f"`{violation['resource']}`")
                with col2:
                    st.markdown(violation['type'])
                with col3:
                    st.markdown(f"Missing: {', '.join(violation['missing'])}")
                with col4:
                    severity_color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
                    st.markdown(severity_color[violation['severity']])
    
    def _render_tag_compliance(self):
        """Tag compliance dashboard"""
        st.markdown("### 📊 Tag Compliance Dashboard")
        
        import pandas as pd
        
        # Compliance by resource type
        st.markdown("**Compliance by Resource Type:**")
        
        compliance_data = {
            "Resource Type": ["EC2", "S3", "RDS", "Lambda", "EKS", "DynamoDB"],
            "Total": [450, 230, 85, 320, 45, 104],
            "Compliant": [412, 218, 82, 305, 43, 100],
            "Non-Compliant": [38, 12, 3, 15, 2, 4],
            "Compliance %": ["91.6%", "94.8%", "96.5%", "95.3%", "95.6%", "96.2%"]
        }
        
        df = pd.DataFrame(compliance_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Trend chart
        st.markdown("**Compliance Trend (Last 30 Days):**")
        chart_data = pd.DataFrame({
            'Day': list(range(1, 31)),
            'Compliance %': [85 + i * 0.2 for i in range(30)]
        })
        st.line_chart(chart_data.set_index('Day'))
    
    def _render_tag_remediation(self):
        """Tag remediation actions"""
        st.markdown("### 🔧 Automated Remediation")
        
        st.markdown("Configure auto-remediation for tag violations")
        
        # Remediation config
        col1, col2 = st.columns(2)
        
        with col1:
            auto_remediate = st.checkbox("Enable Auto-Remediation", value=True)
            default_tags = st.checkbox("Apply Default Tags", value=True)
            notify_owner = st.checkbox("Notify Resource Owner", value=True)
        
        with col2:
            remediation_delay = st.slider("Remediation Delay (hours)", 0, 72, 24)
            max_attempts = st.number_input("Max Remediation Attempts", 1, 5, 3)
        
        st.markdown("---")
        
        # Remediation actions
        st.markdown("**Available Remediation Actions:**")
        
        actions = [
            {"action": "Apply Default Tags", "description": "Add missing required tags with default values"},
            {"action": "Inherit from Parent", "description": "Copy tags from parent resource (VPC, EKS cluster, etc.)"},
            {"action": "Block Resource Creation", "description": "Prevent creation of non-compliant resources"},
            {"action": "Send Notification", "description": "Alert resource owner via email/Slack"},
            {"action": "Create Service Ticket", "description": "Auto-create Jira ticket for manual review"}
        ]
        
        for action in actions:
            col1, col2 = st.columns([1, 3])
            with col1:
                st.checkbox(action['action'], value=True, key=f"action_{action['action']}")
            with col2:
                st.markdown(f"*{action['description']}*")
        
        if st.button("💾 Save Remediation Configuration"):
            st.success("✅ Remediation configuration saved")
    
    def render_naming_enforcement(self):
        """Naming Convention & Placement Enforcement"""
        st.title("📝 Naming & Placement Enforcement")
        st.markdown("### Automated Naming Standards & Resource Placement")
        
        if st.session_state.demo_mode:
            st.info("📋 **Demo Mode**: Viewing naming convention rules")
        
        tab1, tab2, tab3 = st.tabs(["📝 Naming Rules", "🗺️ Placement Rules", "✅ Validation"])
        
        with tab1:
            self._render_naming_rules()
        
        with tab2:
            self._render_placement_rules()
        
        with tab3:
            self._render_naming_validation()
    
    def _render_naming_rules(self):
        """Naming convention rules"""
        st.markdown("### 📝 Naming Convention Rules")
        
        rules = self.demo_data.get_naming_enforcement_rules()
        
        for rule in rules:
            with st.expander(f"📝 {rule['resource_type']} Naming Rule", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Pattern:** `{rule['pattern']}`")
                    st.markdown(f"**Example:** `{rule['example']}`")
                    st.markdown(f"**Enforcement:** {rule['enforcement']}")
                
                with col2:
                    st.markdown(f"**Status:** {rule['status']}")
                    st.markdown(f"**Scope:** {rule['scope']}")
                    st.markdown(f"**Violations:** {rule['violations']}")
                
                # Pattern explanation
                st.markdown("**Pattern Components:**")
                for component in rule['components']:
                    st.markdown(f"- `{component['part']}`: {component['description']}")
                
                # Test the pattern
                st.markdown("**Test This Pattern:**")
                test_name = st.text_input("Enter name to test", key=f"test_{rule['resource_type']}")
                if st.button("Validate", key=f"validate_{rule['resource_type']}"):
                    # Simple regex test (demo)
                    import re
                    pattern = rule['pattern'].replace('*', '.*')
                    if re.match(pattern, test_name):
                        st.success(f"✅ '{test_name}' matches the pattern")
                    else:
                        st.error(f"❌ '{test_name}' does not match the pattern")
    
    def _render_placement_rules(self):
        """Placement rules"""
        st.markdown("### 🗺️ Resource Placement Rules")
        
        st.markdown("Define where resources can be deployed")
        
        placement_rules = self.demo_data.get_placement_rules()
        
        for rule in placement_rules:
            with st.expander(f"🗺️ {rule['name']}", expanded=False):
                st.markdown(f"**Description:** {rule['description']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Resource Type:** {rule['resource_type']}")
                    st.markdown(f"**Environment:** {rule['environment']}")
                with col2:
                    st.markdown(f"**Enforcement:** {rule['enforcement']}")
                    st.markdown(f"**Priority:** {rule['priority']}")
                
                # Allowed locations
                st.markdown("**Allowed Regions:**")
                st.markdown(f"{', '.join(rule['allowed_regions'])}")
                
                # Restrictions
                if rule['restrictions']:
                    st.markdown("**Restrictions:**")
                    for restriction in rule['restrictions']:
                        st.markdown(f"- {restriction}")
    
    def _render_naming_validation(self):
        """Naming validation"""
        st.markdown("### ✅ Naming & Placement Validation")
        
        # Bulk validation
        st.markdown("**Bulk Validation:**")
        
        uploaded_file = st.file_uploader("Upload CSV with resource names", type=['csv'])
        
        if st.button("🔍 Validate All Resources"):
            st.markdown("---")
            
            # Validation results
            results = [
                {"name": "prod-web-app-01", "type": "EC2", "status": "✅ Valid", "region": "us-east-1"},
                {"name": "my-test-bucket", "type": "S3", "status": "❌ Invalid", "issue": "Missing environment prefix"},
                {"name": "dev-db-cluster-primary", "type": "RDS", "status": "✅ Valid", "region": "us-east-1"},
                {"name": "lambda_function", "type": "Lambda", "status": "⚠️ Warning", "issue": "Use hyphens instead of underscores"},
            ]
            
            for result in results:
                col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
                with col1:
                    st.markdown(f"`{result['name']}`")
                with col2:
                    st.markdown(result['type'])
                with col3:
                    st.markdown(result['status'])
                with col4:
                    if 'issue' in result:
                        st.markdown(f"*{result['issue']}*")
                    else:
                        st.markdown(f"*{result.get('region', 'N/A')}*")
    
    def render_quota_guardrails(self):
        """Quota Guardrails Management"""
        st.title("⚖️ Quota Guardrails")
        st.markdown("### Proactive Service Limit Monitoring & Management")
        
        if st.session_state.demo_mode:
            st.info("📋 **Demo Mode**: Viewing quota configurations")
        
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Quota Dashboard", "⚠️ Alerts", "📝 Requests", "📈 Trending"])
        
        with tab1:
            self._render_quota_dashboard()
        
        with tab2:
            self._render_quota_alerts()
        
        with tab3:
            self._render_quota_requests()
        
        with tab4:
            self._render_quota_trending()
    
    def _render_quota_dashboard(self):
        """Quota dashboard"""
        st.markdown("### 📊 Service Quota Overview")
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Monitored Quotas", "347")
        with col2:
            st.metric("At Risk (>80%)", "23", "⚠️")
        with col3:
            st.metric("Critical (>90%)", "5", "🔴")
        with col4:
            st.metric("Increase Requests", "12")
        
        st.markdown("---")
        
        # Quota status
        quotas = self.demo_data.get_quota_status()
        
        st.markdown("**Critical Quotas:**")
        
        for quota in quotas:
            # Calculate percentage
            usage_pct = (quota['current'] / quota['limit']) * 100
            
            # Determine status color
            if usage_pct >= 90:
                status_color = "🔴"
                status_text = "CRITICAL"
            elif usage_pct >= 80:
                status_color = "🟡"
                status_text = "WARNING"
            else:
                status_color = "🟢"
                status_text = "OK"
            
            with st.expander(f"{status_color} {quota['service']} - {quota['quota_name']}", expanded=usage_pct >= 90):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"**Current:** {quota['current']:,}")
                    st.markdown(f"**Limit:** {quota['limit']:,}")
                    st.markdown(f"**Usage:** {usage_pct:.1f}%")
                
                with col2:
                    st.markdown(f"**Region:** {quota['region']}")
                    st.markdown(f"**Account:** {quota['account']}")
                    st.markdown(f"**Status:** {status_text}")
                
                with col3:
                    st.markdown(f"**Growth Rate:** {quota['growth_rate']}")
                    st.markdown(f"**Days to Limit:** {quota['days_to_limit']}")
                
                # Progress bar
                st.progress(usage_pct / 100)
                
                # Actions
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📈 Request Increase", key=f"increase_{quota['quota_name']}"):
                        st.success("Quota increase request submitted")
                with col2:
                    if st.button("📧 Set Alert", key=f"alert_{quota['quota_name']}"):
                        st.success("Alert configured")
    
    def _render_quota_alerts(self):
        """Quota alerts configuration"""
        st.markdown("### ⚠️ Quota Alert Configuration")
        
        # Alert thresholds
        col1, col2, col3 = st.columns(3)
        with col1:
            warning_threshold = st.slider("Warning Threshold (%)", 0, 100, 80)
        with col2:
            critical_threshold = st.slider("Critical Threshold (%)", 0, 100, 90)
        with col3:
            forecast_days = st.number_input("Forecast Days", 1, 90, 30)
        
        st.markdown("---")
        
        # Alert channels
        st.markdown("**Alert Channels:**")
        
        col1, col2 = st.columns(2)
        with col1:
            email_alerts = st.checkbox("Email Alerts", value=True)
            slack_alerts = st.checkbox("Slack Alerts", value=True)
            sns_alerts = st.checkbox("AWS SNS", value=True)
        
        with col2:
            pagerduty_alerts = st.checkbox("PagerDuty", value=False)
            webhook_alerts = st.checkbox("Custom Webhook", value=False)
        
        if email_alerts:
            email_recipients = st.text_area("Email Recipients (one per line)", "devops@company.com\ncloudops@company.com")
        
        st.markdown("---")
        
        # Recent alerts
        st.markdown("**Recent Alerts:**")
        
        alerts = [
            {"service": "EC2", "quota": "Running On-Demand Instances", "level": "Warning", "time": "10m ago"},
            {"service": "VPC", "quota": "VPCs per Region", "level": "Critical", "time": "1h ago"},
            {"service": "RDS", "quota": "DB Instances", "level": "Warning", "time": "3h ago"},
        ]
        
        for alert in alerts:
            level_icon = "🔴" if alert['level'] == "Critical" else "🟡"
            st.markdown(f"{level_icon} **{alert['service']}** - {alert['quota']} • {alert['time']}")
        
        if st.button("💾 Save Alert Configuration"):
            st.success("✅ Alert configuration saved")
    
    def _render_quota_requests(self):
        """Quota increase requests"""
        st.markdown("### 📝 Quota Increase Requests")
        
        # New request form
        with st.expander("➕ Request Quota Increase", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                service = st.selectbox("AWS Service", ["EC2", "VPC", "RDS", "Lambda", "S3", "ELB"])
                quota_name = st.selectbox("Quota Name", [
                    "Running On-Demand Instances",
                    "VPCs per Region",
                    "DB Instances",
                    "Concurrent Executions"
                ])
            
            with col2:
                current_limit = st.number_input("Current Limit", value=100)
                requested_limit = st.number_input("Requested Limit", value=200)
            
            region = st.selectbox("Region", ["us-east-1", "us-west-2", "eu-west-1"])
            justification = st.text_area("Business Justification", "Scaling for Q4 traffic increase...")
            
            if st.button("📤 Submit Request"):
                st.success("✅ Quota increase request submitted to AWS Support")
        
        st.markdown("---")
        
        # Request history
        st.markdown("**Request History:**")
        
        requests = self.demo_data.get_quota_requests()
        
        for req in requests:
            status_icon = {"Approved": "✅", "Pending": "⏳", "Rejected": "❌"}[req['status']]
            
            with st.expander(f"{status_icon} {req['service']} - {req['quota']} ({req['status']})", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Requested:** {req['requested']}")
                    st.markdown(f"**Submitted:** {req['submitted_date']}")
                    st.markdown(f"**Requester:** {req['requester']}")
                
                with col2:
                    st.markdown(f"**Status:** {req['status']}")
                    st.markdown(f"**Case ID:** {req['case_id']}")
                    if req['status'] == "Approved":
                        st.markdown(f"**Approved Date:** {req['approved_date']}")
    
    def _render_quota_trending(self):
        """Quota usage trending"""
        st.markdown("### 📈 Usage Trending & Forecasting")
        
        import pandas as pd
        
        # Service selection
        service = st.selectbox("Select Service", ["EC2", "VPC", "RDS", "Lambda", "S3"])
        
        st.markdown("---")
        
        # Usage trend chart
        st.markdown(f"**{service} Quota Usage Trend (Last 90 Days):**")
        
        # Generate sample trend data
        import random
        days = list(range(1, 91))
        usage = [50 + i * 0.5 + random.uniform(-5, 5) for i in range(90)]
        limit = [100] * 90
        
        chart_data = pd.DataFrame({
            'Day': days,
            'Usage': usage,
            'Limit': limit,
            'Warning (80%)': [80] * 90,
            'Critical (90%)': [90] * 90
        })
        
        st.line_chart(chart_data.set_index('Day'))
        
        st.markdown("---")
        
        # Forecast
        st.markdown("**30-Day Forecast:**")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Current Usage", "87%", "+2.3%")
        with col2:
            st.metric("Forecasted (30d)", "96%", "+9%")
        with col3:
            st.metric("Days to Limit", "23", "-7")
        
        st.warning("⚠️ Forecast indicates quota will be reached in 23 days. Consider requesting an increase.")
        
        if st.button("📈 Request Proactive Increase"):
            st.success("✅ Proactive quota increase request submitted")
