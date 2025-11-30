"""
Provisioning & Deployment Module
Handles multi-cloud provisioning, environment promotion, and CI/CD integration
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from demo_data import DemoDataProvider

class ProvisioningDeploymentModule:
    """Provisioning & Deployment functionality"""
    def render(self):
        """Main render method - organizes all sub-features in tabs"""
        
        st.markdown("## Provisioningdeployment")        
        # Mode indicator
        if st.session_state.get('mode', 'Demo') == 'Live':
            st.warning("⚠️ Live mode not yet implemented - showing demo data")

        
        # Create tabs for each sub-feature
        tabs = st.tabs([
            "📋 Multi Cloud Provisioning",
            "⚙️ Environment Promotion",
            "⚙️ Cicd Integration"
        ])
        
        with tabs[0]:
            self.render_multi_cloud_provisioning()
        
        with tabs[1]:
            self.render_environment_promotion()
        
        with tabs[2]:
            self.render_cicd_integration()


    
    @staticmethod
    def render_multi_cloud_provisioning():
        """Multi-Cloud Provisioning interface"""
        
        st.markdown("## ☁️ Multi-Cloud Provisioning")
        st.markdown("Deploy and manage infrastructure across AWS, Azure, and GCP")
        
        # Mode indicator
        if st.session_state.demo_mode:
            st.info("📋 Demo Mode: Viewing sample provisioning data")
        else:
            st.warning("🟢 Live Mode: Real provisioning operations will be executed")
        
        st.markdown("---")
        
        # Tabs for different views
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Provisioning Dashboard",
            "🚀 New Deployment",
            "🔄 Active Deployments",
            "📈 Cloud Comparison"
        ])
        
        with tab1:
            ProvisioningDeploymentModule._render_provisioning_dashboard()
        
        with tab2:
            ProvisioningDeploymentModule._render_new_deployment()
        
        with tab3:
            ProvisioningDeploymentModule._render_active_deployments()
        
        with tab4:
            ProvisioningDeploymentModule._render_cloud_comparison()
    
    @staticmethod
    def _render_provisioning_dashboard():
        """Provisioning dashboard with metrics"""
        
        data = DemoDataProvider.get_provisioning_dashboard()
        
        # Key metrics
        st.markdown("### 📊 Provisioning Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Deployments",
                data['total_deployments'],
                f"+{data['deployments_this_month']} this month"
            )
        
        with col2:
            st.metric(
                "Success Rate",
                f"{data['success_rate']}%",
                f"+{data['success_rate_change']}%"
            )
        
        with col3:
            st.metric(
                "Active Resources",
                data['active_resources'],
                f"+{data['resources_growth']} today"
            )
        
        with col4:
            st.metric(
                "Avg Deploy Time",
                data['avg_deploy_time'],
                f"-{data['time_improvement']}"
            )
        
        st.markdown("---")
        
        # Cloud distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ☁️ Cloud Provider Distribution")
            df_clouds = pd.DataFrame(data['cloud_distribution'])
            st.dataframe(df_clouds, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("### 📅 Recent Deployments")
            df_recent = pd.DataFrame(data['recent_deployments'])
            st.dataframe(df_recent, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Deployment trends
        st.markdown("### 📈 Deployment Trends (Last 30 Days)")
        df_trends = pd.DataFrame(data['deployment_trends'])
        st.line_chart(df_trends.set_index('date'))
    
    @staticmethod
    def _render_new_deployment():
        """New deployment wizard"""
        
        st.markdown("### 🚀 Create New Deployment")
        
        with st.form("new_deployment_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                deployment_name = st.text_input(
                    "Deployment Name*",
                    placeholder="my-app-production"
                )
                
                cloud_provider = st.selectbox(
                    "Cloud Provider*",
                    ["AWS", "Azure", "GCP", "Multi-Cloud"]
                )
                
                blueprint = st.selectbox(
                    "Architecture Blueprint*",
                    ["Three-Tier Web Application", "Serverless API Backend", 
                     "Data Lake Analytics", "Microservices on EKS",
                     "Custom Configuration"]
                )
                
                environment = st.selectbox(
                    "Target Environment*",
                    ["Development", "Staging", "Production"]
                )
            
            with col2:
                region = st.selectbox(
                    "Primary Region*",
                    ["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1"]
                )
                
                high_availability = st.checkbox("Enable High Availability", value=True)
                auto_scaling = st.checkbox("Enable Auto Scaling", value=True)
                backup_enabled = st.checkbox("Enable Automated Backups", value=True)
                monitoring = st.checkbox("Enable Advanced Monitoring", value=True)
            
            st.markdown("---")
            
            # Advanced options
            with st.expander("⚙️ Advanced Configuration", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    vpc_cidr = st.text_input("VPC CIDR Block", value="10.0.0.0/16")
                    subnet_config = st.selectbox(
                        "Subnet Configuration",
                        ["Public + Private", "Private Only", "Custom"]
                    )
                    nat_gateway = st.selectbox(
                        "NAT Gateway",
                        ["One per AZ", "Single NAT", "No NAT"]
                    )
                
                with col2:
                    encryption = st.selectbox(
                        "Encryption Level",
                        ["AES-256", "AES-128", "Custom KMS"]
                    )
                    compliance = st.multiselect(
                        "Compliance Frameworks",
                        ["PCI DSS", "HIPAA", "GDPR", "SOC 2", "ISO 27001"]
                    )
                    tags = st.text_area(
                        "Additional Tags (key=value, one per line)",
                        placeholder="Project=MyApp\nOwner=TeamA\nCostCenter=CC123"
                    )
            
            # Cost estimation
            st.markdown("---")
            st.markdown("### 💰 Estimated Monthly Cost")
            
            estimated_cost = 1250.00  # This would be calculated based on selections
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Compute", f"${450:.2f}")
            with col2:
                st.metric("Storage", f"${350:.2f}")
            with col3:
                st.metric("Total", f"${estimated_cost:.2f}")
            
            st.markdown("---")
            
            # Submit buttons
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                submitted = st.form_submit_button(
                    "🚀 Deploy Now",
                    type="primary",
                    use_container_width=True
                )
            
            with col2:
                validate = st.form_submit_button(
                    "✅ Validate Only",
                    use_container_width=True
                )
            
            if submitted:
                if deployment_name and cloud_provider and blueprint:
                    with st.spinner("Deploying infrastructure..."):
                        # Simulate deployment
                        import time
                        time.sleep(2)
                        
                        if st.session_state.demo_mode:
                            st.success(f"""
                            ✅ **Demo Deployment Initiated**
                            
                            - Deployment: {deployment_name}
                            - Cloud: {cloud_provider}
                            - Blueprint: {blueprint}
                            - Environment: {environment}
                            - Status: In Progress (Demo)
                            
                            In live mode, this would provision real resources.
                            """)
                        else:
                            st.success(f"""
                            ✅ **Deployment Initiated**
                            
                            - Deployment ID: dep-{datetime.now().strftime('%Y%m%d%H%M%S')}
                            - Status: Provisioning
                            - Estimated Time: 15-20 minutes
                            
                            You can monitor progress in the Active Deployments tab.
                            """)
                else:
                    st.error("❌ Please fill in all required fields (marked with *)")
            
            if validate:
                with st.spinner("Validating configuration..."):
                    import time
                    time.sleep(1)
                    st.info("""
                    ✅ **Validation Results**
                    
                    - Blueprint: Valid
                    - Network Configuration: Valid
                    - Security Settings: Valid
                    - Compliance Checks: 4/4 Passed
                    - Cost Estimate: Approved
                    
                    Ready to deploy!
                    """)
    
    @staticmethod
    def _render_active_deployments():
        """Show active deployments"""
        
        st.markdown("### 🔄 Active Deployments")
        
        data = DemoDataProvider.get_active_deployments()
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.multiselect(
                "Filter by Status",
                ["Provisioning", "Running", "Updating", "Failed"],
                default=["Provisioning", "Running", "Updating"]
            )
        with col2:
            cloud_filter = st.multiselect(
                "Filter by Cloud",
                ["AWS", "Azure", "GCP"],
                default=["AWS", "Azure", "GCP"]
            )
        with col3:
            env_filter = st.multiselect(
                "Filter by Environment",
                ["Development", "Staging", "Production"],
                default=["Development", "Staging", "Production"]
            )
        
        st.markdown("---")
        
        # Deployments table
        for deployment in data:
            if deployment['status'] in status_filter and \
               deployment['cloud'] in cloud_filter and \
               deployment['environment'] in env_filter:
                
                with st.expander(
                    f"{deployment['name']} - {deployment['status']} ({deployment['cloud']})",
                    expanded=deployment['status'] == 'Provisioning'
                ):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown(f"**Deployment ID:** {deployment['id']}")
                        st.markdown(f"**Blueprint:** {deployment['blueprint']}")
                        st.markdown(f"**Environment:** {deployment['environment']}")
                    
                    with col2:
                        st.markdown(f"**Region:** {deployment['region']}")
                        st.markdown(f"**Started:** {deployment['started_at']}")
                        st.markdown(f"**Resources:** {deployment['resources_created']}/{deployment['resources_total']}")
                    
                    with col3:
                        # Status badge
                        if deployment['status'] == 'Running':
                            st.success(f"✅ {deployment['status']}")
                        elif deployment['status'] == 'Provisioning':
                            st.info(f"🔄 {deployment['status']}")
                        elif deployment['status'] == 'Failed':
                            st.error(f"❌ {deployment['status']}")
                        else:
                            st.warning(f"⚠️ {deployment['status']}")
                        
                        st.markdown(f"**Progress:** {deployment['progress']}%")
                        st.progress(deployment['progress'] / 100)
                    
                    # Action buttons
                    st.markdown("---")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        if st.button("📊 View Details", key=f"details_{deployment['id']}"):
                            st.info(f"Viewing details for {deployment['name']}")
                    
                    with col2:
                        if st.button("📝 View Logs", key=f"logs_{deployment['id']}"):
                            st.text("""
[2024-11-18 10:23:15] Creating VPC...
[2024-11-18 10:23:45] VPC created: vpc-0abc123
[2024-11-18 10:24:10] Creating subnets...
[2024-11-18 10:24:55] Subnets created successfully
[2024-11-18 10:25:20] Provisioning compute resources...
                            """)
                    
                    with col3:
                        if deployment['status'] == 'Running':
                            if st.button("⏸️ Pause", key=f"pause_{deployment['id']}"):
                                st.warning("Deployment paused")
                    
                    with col4:
                        if st.button("🗑️ Destroy", key=f"destroy_{deployment['id']}"):
                            st.error("⚠️ This will destroy all resources. Confirm in production.")
    
    @staticmethod
    def _render_cloud_comparison():
        """Cloud provider comparison"""
        
        st.markdown("### 📈 Cloud Provider Comparison")
        
        data = DemoDataProvider.get_cloud_comparison()
        
        # Comparison table
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Detailed comparison
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### AWS Strengths")
            st.markdown("""
            - 🟢 Largest service portfolio
            - 🟢 Most mature offerings
            - 🟢 Best enterprise support
            - 🟢 Extensive compliance
            - 🟡 Higher complexity
            """)
        
        with col2:
            st.markdown("#### Azure Strengths")
            st.markdown("""
            - 🟢 Best for Microsoft stack
            - 🟢 Hybrid cloud integration
            - 🟢 Active Directory integration
            - 🟡 Growing service catalog
            - 🟡 Regional availability
            """)
        
        with col3:
            st.markdown("#### GCP Strengths")
            st.markdown("""
            - 🟢 Best for data/ML
            - 🟢 Competitive pricing
            - 🟢 Modern architecture
            - 🟡 Smaller service catalog
            - 🟡 Less enterprise features
            """)
    
    @staticmethod
    def render_environment_promotion():
        """Environment Promotion Pathing interface"""
        
        st.markdown("## 🔄 Environment Promotion Pathing")
        st.markdown("Manage code and infrastructure promotion across environments")
        
        # Mode indicator
        if st.session_state.demo_mode:
            st.info("📋 Demo Mode: Viewing sample promotion workflows")
        else:
            st.warning("🟢 Live Mode: Real promotion actions will be executed")
        
        st.markdown("---")
        
        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "🔄 Promotion Pipeline",
            "📋 Pending Promotions",
            "✅ Approval Workflow",
            "📊 Promotion History"
        ])
        
        with tab1:
            ProvisioningDeploymentModule._render_promotion_pipeline()
        
        with tab2:
            ProvisioningDeploymentModule._render_pending_promotions()
        
        with tab3:
            ProvisioningDeploymentModule._render_approval_workflow()
        
        with tab4:
            ProvisioningDeploymentModule._render_promotion_history()
    
    @staticmethod
    def _render_promotion_pipeline():
        """Promotion pipeline visualization"""
        
        st.markdown("### 🔄 Environment Promotion Pipeline")
        
        # Visual pipeline
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown("#### Development")
            st.success("✅ Healthy")
            # Mode-aware metric
            version_value = self._get_data('version', "v1.2.5")
            st.metric("Version", version_value)
            # Mode-aware metric
            commits_value = self._get_data('commits', "247")
            st.metric("Commits", commits_value)
        
        with col2:
            st.markdown("→")
            st.markdown("**Auto Deploy**")
            st.caption("On merge to main")
        
        with col3:
            st.markdown("#### Staging")
            st.success("✅ Healthy")
            # Mode-aware metric
            version_value = self._get_data('version', "v1.2.4")
            st.metric("Version", version_value)
            # Mode-aware metric
            age_value = self._get_data('age', "2 days")
            st.metric("Age", age_value)
        
        with col4:
            st.markdown("→")
            st.markdown("**Manual Approval**")
            st.caption("Requires 2 approvers")
        
        with col5:
            st.markdown("#### Production")
            st.success("✅ Healthy")
            # Mode-aware metric
            version_value = self._get_data('version', "v1.2.3")
            st.metric("Version", version_value)
            # Mode-aware metric
            age_value = self._get_data('age', "7 days")
            st.metric("Age", age_value)
        
        st.markdown("---")
        
        # Promotion rules
        data = DemoDataProvider.get_promotion_rules()
        
        st.markdown("### 📋 Promotion Rules")
        
        for rule in data:
            with st.expander(f"{rule['from_env']} → {rule['to_env']}", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Trigger:** {rule['trigger']}")
                    st.markdown(f"**Approvers Required:** {rule['approvers_required']}")
                    st.markdown(f"**Automated Tests:** {rule['automated_tests']}")
                
                with col2:
                    st.markdown("**Gates:**")
                    for gate in rule['gates']:
                        st.markdown(f"- {gate}")
                
                st.markdown(f"**Rollback Strategy:** {rule['rollback_strategy']}")
        
        st.markdown("---")
        
        # Quick promotion
        st.markdown("### 🚀 Quick Promotion")
        
        with st.form("quick_promotion"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                from_env = st.selectbox("From Environment", ["Development", "Staging"])
            
            with col2:
                to_env = st.selectbox("To Environment", ["Staging", "Production"])
            
            with col3:
                version = st.text_input("Version/Tag", value="v1.2.5")
            
            include_config = st.checkbox("Include configuration changes", value=True)
            include_data = st.checkbox("Include data migrations", value=False)
            
            notes = st.text_area("Promotion Notes", placeholder="Describe changes...")
            
            submitted = st.form_submit_button("🚀 Initiate Promotion", type="primary")
            
            if submitted:
                with st.spinner("Initiating promotion..."):
                    import time
                    time.sleep(2)
                    
                    if st.session_state.demo_mode:
                        st.success(f"""
                        ✅ **Demo Promotion Initiated**
                        
                        - From: {from_env}
                        - To: {to_env}
                        - Version: {version}
                        - Status: Pending Approval (Demo)
                        
                        In live mode, this would create a promotion request.
                        """)
                    else:
                        st.success(f"""
                        ✅ **Promotion Request Created**
                        
                        - Request ID: PR-{datetime.now().strftime('%Y%m%d%H%M')}
                        - From: {from_env} → {to_env}
                        - Version: {version}
                        - Status: Awaiting Approval
                        
                        Notification sent to approvers.
                        """)
    
    @staticmethod
    def _render_pending_promotions():
        """Show pending promotions"""
        
        st.markdown("### 📋 Pending Promotions")
        
        data = DemoDataProvider.get_pending_promotions()
        
        for promo in data:
            with st.expander(
                f"{promo['id']}: {promo['from_env']} → {promo['to_env']} ({promo['status']})",
                expanded=True
            ):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"**Application:** {promo['application']}")
                    st.markdown(f"**Version:** {promo['version']}")
                    st.markdown(f"**Requested By:** {promo['requested_by']}")
                
                with col2:
                    st.markdown(f"**Created:** {promo['created_at']}")
                    st.markdown(f"**Approvals:** {promo['approvals']}/{promo['approvals_required']}")
                    st.markdown(f"**Tests Status:** {promo['tests_status']}")
                
                with col3:
                    if promo['status'] == 'Pending Approval':
                        st.warning("⏳ Awaiting Approval")
                    elif promo['status'] == 'Ready':
                        st.success("✅ Ready to Deploy")
                    else:
                        st.info(f"ℹ️ {promo['status']}")
                
                st.markdown("---")
                st.markdown("**Description:**")
                st.markdown(promo['description'])
                
                # Action buttons
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button("✅ Approve", key=f"approve_{promo['id']}"):
                        st.success("Promotion approved")
                
                with col2:
                    if st.button("❌ Reject", key=f"reject_{promo['id']}"):
                        st.error("Promotion rejected")
                
                with col3:
                    if promo['status'] == 'Ready':
                        if st.button("🚀 Deploy", key=f"deploy_{promo['id']}"):
                            st.info("Deployment initiated")
                
                with col4:
                    if st.button("📊 Details", key=f"details_{promo['id']}"):
                        st.json(promo)
    
    @staticmethod
    def _render_approval_workflow():
        """Approval workflow configuration"""
        
        st.markdown("### ✅ Approval Workflow Configuration")
        
        data = DemoDataProvider.get_approval_workflows()
        
        for workflow in data:
            with st.expander(f"{workflow['name']} ({workflow['environment']})", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Environment:** {workflow['environment']}")
                    st.markdown(f"**Required Approvers:** {workflow['required_approvers']}")
                    st.markdown(f"**Status:** {workflow['status']}")
                    st.markdown(f"**Auto-approve on:** {', '.join(workflow['auto_approve_conditions'])}")
                
                with col2:
                    st.markdown("**Approvers:**")
                    for approver in workflow['approvers']:
                        st.markdown(f"- {approver}")
                    
                    st.markdown("**Notification Channels:**")
                    for channel in workflow['notification_channels']:
                        st.markdown(f"- {channel}")
                
                st.markdown("---")
                st.markdown("**Gates:**")
                for gate in workflow['gates']:
                    st.markdown(f"- ✓ {gate}")
    
    @staticmethod
    def _render_promotion_history():
        """Promotion history"""
        
        st.markdown("### 📊 Promotion History")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            date_range = st.selectbox("Time Range", ["Last 7 Days", "Last 30 Days", "Last 90 Days"])
        with col2:
            env_filter = st.selectbox("Environment", ["All", "Development", "Staging", "Production"])
        with col3:
            status_filter = st.selectbox("Status", ["All", "Success", "Failed", "Rolled Back"])
        
        st.markdown("---")
        
        data = DemoDataProvider.get_promotion_history()
        df = pd.DataFrame(data)
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Statistics
        st.markdown("---")
        st.markdown("### 📈 Promotion Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Promotions", len(data))
        with col2:
            success_count = len([p for p in data if p['status'] == 'Success'])
            st.metric("Success Rate", f"{(success_count/len(data)*100):.1f}%")
        with col3:
            # Mode-aware metric
            avg_time_value = self._get_data('avg_time', "12.5 min")
            st.metric("Avg Time", avg_time_value)
        with col4:
            # Mode-aware metric
            rollbacks_value = self._get_data('rollbacks', "2")
            st.metric("Rollbacks", rollbacks_value)
    
    @staticmethod
    def render_cicd_integration():
        """CI/CD Pipeline Integration interface"""
        
        st.markdown("## 🔧 CI/CD Pipeline Integration")
        st.markdown("Integrate with Jenkins, GitLab CI, GitHub Actions, and more")
        
        # Mode indicator
        if st.session_state.demo_mode:
            st.info("📋 Demo Mode: Viewing sample CI/CD configurations")
        else:
            st.warning("🟢 Live Mode: Real pipeline configurations will be modified")
        
        st.markdown("---")
        
        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "🔗 Pipeline Connections",
            "⚙️ Pipeline Configuration",
            "📊 Build Status",
            "📝 Pipeline Templates"
        ])
        
        with tab1:
            ProvisioningDeploymentModule._render_pipeline_connections()
        
        with tab2:
            ProvisioningDeploymentModule._render_pipeline_configuration()
        
        with tab3:
            ProvisioningDeploymentModule._render_build_status()
        
        with tab4:
            ProvisioningDeploymentModule._render_pipeline_templates()
    
    @staticmethod
    def _render_pipeline_connections():
        """Pipeline connections"""
        
        st.markdown("### 🔗 Connected CI/CD Systems")
        
        data = DemoDataProvider.get_cicd_connections()
        
        for connection in data:
            with st.expander(f"{connection['name']} - {connection['status']}", expanded=True):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"**Type:** {connection['type']}")
                    st.markdown(f"**URL:** {connection['url']}")
                    st.markdown(f"**Connected:** {connection['connected_at']}")
                
                with col2:
                    st.markdown(f"**Pipelines:** {connection['pipelines']}")
                    st.markdown(f"**Last Build:** {connection['last_build']}")
                    if connection['status'] == 'Active':
                        st.success("✅ Active")
                    else:
                        st.error("❌ Inactive")
                
                with col3:
                    st.markdown("**Actions:**")
                    if st.button("🔄 Test Connection", key=f"test_{connection['id']}"):
                        st.success("Connection successful!")
                    if st.button("⚙️ Configure", key=f"config_{connection['id']}"):
                        st.info("Configuration panel opened")
                    if st.button("🗑️ Disconnect", key=f"disconnect_{connection['id']}"):
                        st.warning("Disconnected")
        
        st.markdown("---")
        
        # Add new connection
        st.markdown("### ➕ Add New CI/CD Connection")
        
        with st.form("new_cicd_connection"):
            col1, col2 = st.columns(2)
            
            with col1:
                cicd_type = st.selectbox(
                    "CI/CD System",
                    ["Jenkins", "GitLab CI", "GitHub Actions", "CircleCI", "Azure DevOps", "AWS CodePipeline"]
                )
                connection_name = st.text_input("Connection Name", placeholder="my-jenkins-server")
            
            with col2:
                cicd_url = st.text_input("Server URL", placeholder="https://jenkins.example.com")
                api_token = st.text_input("API Token/Key", type="password")
            
            submitted = st.form_submit_button("➕ Add Connection", type="primary")
            
            if submitted:
                if connection_name and cicd_url and api_token:
                    st.success(f"✅ {cicd_type} connection '{connection_name}' added successfully!")
                else:
                    st.error("❌ Please fill in all fields")
    
    @staticmethod
    def _render_pipeline_configuration():
        """Pipeline configuration"""
        
        st.markdown("### ⚙️ Pipeline Configuration")
        
        data = DemoDataProvider.get_pipeline_configurations()
        
        for pipeline in data:
            with st.expander(f"{pipeline['name']} ({pipeline['type']})", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Repository:** {pipeline['repository']}")
                    st.markdown(f"**Branch:** {pipeline['branch']}")
                    st.markdown(f"**Build Trigger:** {pipeline['trigger']}")
                    st.markdown(f"**Status:** {pipeline['status']}")
                
                with col2:
                    st.markdown("**Stages:**")
                    for stage in pipeline['stages']:
                        st.markdown(f"- {stage}")
                    
                    st.markdown(f"**Deploy Target:** {pipeline['deploy_target']}")
                
                st.markdown("---")
                st.markdown("**Pipeline Configuration:**")
                st.code(pipeline['configuration'], language='yaml')
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("▶️ Run Pipeline", key=f"run_{pipeline['id']}"):
                        st.info("Pipeline started")
                with col2:
                    if st.button("✏️ Edit", key=f"edit_{pipeline['id']}"):
                        st.info("Edit mode enabled")
                with col3:
                    if st.button("📊 View History", key=f"history_{pipeline['id']}"):
                        st.info("Showing pipeline history")
    
    @staticmethod
    def _render_build_status():
        """Build status dashboard"""
        
        st.markdown("### 📊 Build Status Dashboard")
        
        data = DemoDataProvider.get_build_status()
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Builds", data['total_builds'], "+12 today")
        with col2:
            st.metric("Success Rate", f"{data['success_rate']}%", "+2%")
        with col3:
            st.metric("Avg Duration", data['avg_duration'])
        with col4:
            st.metric("Failed Builds", data['failed_builds'], "-3")
        
        st.markdown("---")
        
        # Recent builds
        st.markdown("### 📋 Recent Builds")
        
        df = pd.DataFrame(data['recent_builds'])
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Build trends
        st.markdown("### 📈 Build Trends (Last 7 Days)")
        
        df_trends = pd.DataFrame(data['build_trends'])
        st.line_chart(df_trends.set_index('date'))
    
    @staticmethod
    def _render_pipeline_templates():
        """Pipeline templates"""
        
        st.markdown("### 📝 Pipeline Templates")
        
        data = DemoDataProvider.get_pipeline_templates()
        
        for template in data:
            with st.expander(f"{template['name']} - {template['type']}", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Type:** {template['type']}")
                    st.markdown(f"**Category:** {template['category']}")
                    st.markdown(f"**Language:** {template['language']}")
                
                with col2:
                    st.markdown(f"**Description:** {template['description']}")
                    st.markdown(f"**Use Count:** {template['use_count']}")
                
                st.markdown("---")
                st.markdown("**Template Configuration:**")
                st.code(template['template'], language='yaml')
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📋 Copy Template", key=f"copy_{template['id']}"):
                        st.success("Template copied to clipboard!")
                with col2:
                    if st.button("🚀 Use Template", key=f"use_{template['id']}"):
                        st.info("Creating pipeline from template...")
