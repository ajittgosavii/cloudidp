"""
Design & Planning Module
Handles blueprint definition, tagging standards, naming conventions, etc.
"""

import streamlit as st
import pandas as pd
from demo_data import DemoDataProvider

class DesignPlanningModule:
    """Design & Planning functionality"""
    def render(self):
        """Main render method - organizes all sub-features in tabs"""
        
        st.markdown("## Designplanning")        
        # Mode indicator
        if st.session_state.get('mode', 'Demo') == 'Live':
            st.warning("⚠️ Live mode not yet implemented - showing demo data")

        
        # Create tabs for each sub-feature
        tabs = st.tabs([
            "📋 Blueprint",
            "⚙️ Tagging",
            "⚙️ Naming Conventions",
            "⚙️ Artifact Versioning",
            "⚙️ Iac Registry",
            "⚙️ Design Validation"
        ])
        
        with tabs[0]:
            self.render_blueprint_definition()
        
        with tabs[1]:
            self.render_tagging_standards()
        
        with tabs[2]:
            self.render_naming_conventions()
        
        with tabs[3]:
            self.render_artifact_versioning()
        
        with tabs[4]:
            self.render_iac_registry()
        
        with tabs[5]:
            self.render_design_validation()


    
    @staticmethod
    def render_blueprint_definition():
        """Blueprint Definition interface"""
        
        st.markdown("## 📋 Blueprint Definition")
        st.markdown("Define and manage reusable architecture blueprints")
        
        # Mode indicator
        if st.session_state.demo_mode:
            st.info("📋 Demo Mode: Viewing sample blueprints")
        else:
            st.warning("🟢 Live Mode: Real blueprint operations will be performed")
        
        st.markdown("---")
        
        # Tabs
        tab1, tab2 = st.tabs(["📚 Blueprint Library", "➕ Create Blueprint"])
        
        with tab1:
            DesignPlanningModule._render_blueprint_library()
        
        with tab2:
            DesignPlanningModule._render_create_blueprint()
    
    @staticmethod
    def _render_blueprint_library():
        """Show blueprint library"""
        
        st.markdown("### 📚 Architecture Blueprint Library")
        
        blueprints = DemoDataProvider.get_blueprint_library()
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            category_filter = st.selectbox(
                "Category",
                ["All"] + list(set([bp['category'] for bp in blueprints]))
            )
        with col2:
            status_filter = st.selectbox("Status", ["All", "Active", "Draft", "Deprecated"])
        with col3:
            search = st.text_input("Search", placeholder="Search blueprints...")
        
        st.markdown("---")
        
        # Display blueprints
        for bp in blueprints:
            if (category_filter == "All" or bp['category'] == category_filter) and \
               (status_filter == "All" or bp['status'] == status_filter) and \
               (not search or search.lower() in bp['name'].lower()):
                
                with st.expander(f"📋 {bp['name']} - {bp['version']}", expanded=False):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**Description:** {bp['description']}")
                        st.markdown(f"**Category:** {bp['category']}")
                        st.markdown(f"**Status:** {bp['status']}")
                        st.markdown(f"**Version:** {bp['version']}")
                        
                        st.markdown("**AWS Services:**")
                        st.markdown(", ".join(bp['aws_services']))
                    
                    with col2:
                        st.markdown(f"**Author:** {bp['author']}")
                        st.markdown(f"**Deployments:** {bp['deployment_count']}")
                        st.markdown(f"**Est. Cost:** ${bp['estimated_cost']:.2f}/mo")
                        
                        st.markdown("**Compliance:**")
                        for framework in bp['compliance_frameworks']:
                            st.markdown(f"- {framework}")
                    
                    st.markdown("---")
                    st.markdown("**Environments:**")
                    st.markdown(", ".join(bp['environments']))
                    
                    st.markdown("---")
                    st.markdown("**IaC Template Preview:**")
                    st.code(bp['iac_template'], language='hcl')
                    
                    # Action buttons
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        if st.button("🚀 Deploy", key=f"deploy_{bp['id']}"):
                            st.success(f"Deployment initiated for {bp['name']}")
                    with col2:
                        if st.button("📋 Clone", key=f"clone_{bp['id']}"):
                            st.info(f"Blueprint cloned: {bp['name']}")
                    with col3:
                        if st.button("✏️ Edit", key=f"edit_{bp['id']}"):
                            st.info("Edit mode enabled")
                    with col4:
                        if st.button("📥 Export", key=f"export_{bp['id']}"):
                            st.success("Blueprint exported")
    
    @staticmethod
    def _render_create_blueprint():
        """Create new blueprint"""
        
        st.markdown("### ➕ Create New Blueprint")
        
        with st.form("create_blueprint"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Blueprint Name*", placeholder="e.g., Three-Tier Web Application")
                category = st.selectbox("Category*", [
                    "Web Application",
                    "Serverless",
                    "Data Analytics",
                    "Microservices",
                    "Storage",
                    "Network",
                    "Security"
                ])
                version = st.text_input("Version*", value="1.0.0")
            
            with col2:
                author = st.text_input("Author", placeholder="Your name or team")
                status = st.selectbox("Status", ["Draft", "Active", "Deprecated"])
                estimated_cost = st.number_input("Estimated Monthly Cost ($)", min_value=0.0, value=1000.0)
            
            description = st.text_area("Description*", placeholder="Describe your blueprint...")
            
            # AWS Services
            st.markdown("**AWS Services**")
            services = st.multiselect(
                "Select AWS Services",
                ["VPC", "EC2", "RDS", "S3", "Lambda", "API Gateway", "DynamoDB", 
                 "EKS", "ECR", "ALB", "CloudFront", "Route53", "WAF", "CloudWatch",
                 "Glue", "Athena", "EMR", "Kinesis", "QuickSight"]
            )
            
            # Environments
            st.markdown("**Target Environments**")
            environments = st.multiselect(
                "Select Environments",
                ["Development", "Staging", "Production", "DR"]
            )
            
            # Compliance
            st.markdown("**Compliance Frameworks**")
            compliance = st.multiselect(
                "Select Compliance Frameworks",
                ["PCI DSS", "HIPAA", "GDPR", "SOC 2", "ISO 27001", "FedRAMP"]
            )
            
            # IaC Template
            st.markdown("**Infrastructure as Code Template**")
            iac_format = st.selectbox("IaC Format", ["Terraform", "CloudFormation", "CDK"])
            iac_template = st.text_area(
                "Template Code",
                placeholder="Paste your IaC template here...",
                height=200
            )
            
            submitted = st.form_submit_button("➕ Create Blueprint", type="primary")
            
            if submitted:
                if name and category and version and description:
                    st.success(f"""
                    ✅ **Blueprint Created Successfully**
                    
                    - Name: {name}
                    - Category: {category}
                    - Version: {version}
                    - Status: {status}
                    - Services: {len(services)}
                    - Environments: {len(environments)}
                    
                    Blueprint is now available in the library!
                    """)
                else:
                    st.error("❌ Please fill in all required fields (marked with *)")
    
    @staticmethod
    def render_tagging_standards():
        """Tagging Standards interface"""
        
        st.markdown("## 🏷️ Tagging Standards")
        st.markdown("Define and enforce resource tagging policies")
        
        # Mode indicator
        if st.session_state.demo_mode:
            st.info("📋 Demo Mode: Viewing sample tag policies")
        else:
            st.warning("🟢 Live Mode: Real tag policies will be applied")
        
        st.markdown("---")
        
        # Tag policies
        policies = DemoDataProvider.get_tag_policies()
        
        for policy in policies:
            with st.expander(f"🏷️ {policy['name']}", expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Description:** {policy['description']}")
                    st.markdown(f"**Scope:** {policy['scope']}")
                    st.markdown(f"**Enforcement:** {policy['enforcement']}")
                    st.markdown(f"**Status:** {policy['status']}")
                
                with col2:
                    st.markdown("**Required Tags:**")
                    for tag in policy['required_tags']:
                        st.markdown(f"- **{tag['key']}**: {tag['description']}")
        
        st.markdown("---")
        
        # Create new tag policy
        st.markdown("### ➕ Create New Tag Policy")
        
        with st.form("create_tag_policy"):
            policy_name = st.text_input("Policy Name", placeholder="Production Resources Tagging")
            description = st.text_area("Description", placeholder="Describe the tagging policy...")
            
            col1, col2 = st.columns(2)
            with col1:
                scope = st.selectbox("Scope", ["All Accounts", "Production Accounts", "Development Accounts", "Specific Projects"])
                enforcement = st.selectbox("Enforcement Level", ["Mandatory", "Recommended", "Optional"])
            
            with col2:
                auto_remediation = st.checkbox("Enable Auto-Remediation")
                notification = st.checkbox("Send Notifications on Violations")
            
            st.markdown("**Required Tags**")
            num_tags = st.number_input("Number of required tags", min_value=1, max_value=10, value=4)
            
            tags = []
            for i in range(int(num_tags)):
                col1, col2 = st.columns(2)
                with col1:
                    tag_key = st.text_input(f"Tag Key {i+1}", key=f"tag_key_{i}")
                with col2:
                    tag_desc = st.text_input(f"Description {i+1}", key=f"tag_desc_{i}")
                tags.append({"key": tag_key, "description": tag_desc})
            
            submitted = st.form_submit_button("➕ Create Policy", type="primary")
            
            if submitted:
                st.success("✅ Tag policy created successfully!")
    
    @staticmethod
    def render_naming_conventions():
        """Naming Conventions interface"""
        
        st.markdown("## 📛 Naming Conventions")
        st.markdown("Define standardized naming patterns for AWS resources")
        
        # Mode indicator
        if st.session_state.demo_mode:
            st.info("📋 Demo Mode: Viewing sample naming rules")
        else:
            st.warning("🟢 Live Mode: Real naming rules will be enforced")
        
        st.markdown("---")
        
        # Naming rules
        rules = DemoDataProvider.get_naming_rules()
        
        st.markdown("### 📋 Current Naming Rules")
        
        df = pd.DataFrame(rules)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Create new naming rule
        st.markdown("### ➕ Create New Naming Rule")
        
        with st.form("create_naming_rule"):
            col1, col2 = st.columns(2)
            
            with col1:
                resource_type = st.selectbox(
                    "Resource Type",
                    ["EC2 Instance", "S3 Bucket", "RDS Database", "Lambda Function", 
                     "VPC", "Subnet", "Security Group", "IAM Role", "DynamoDB Table"]
                )
                pattern = st.text_input(
                    "Naming Pattern",
                    placeholder="{project}-{env}-{resource}-{purpose}",
                    help="Use {placeholders} for dynamic parts"
                )
            
            with col2:
                enforcement = st.selectbox("Enforcement", ["Mandatory", "Recommended", "Optional"])
                example = st.text_input("Example", placeholder="myapp-prod-ec2-web-001")
            
            description = st.text_area("Description", placeholder="Describe when and how to use this naming pattern...")
            
            submitted = st.form_submit_button("➕ Create Rule", type="primary")
            
            if submitted:
                st.success(f"✅ Naming rule created for {resource_type}")
    
    @staticmethod
    def render_artifact_versioning():
        """Image/Artifact Versioning interface"""
        
        st.markdown("## 📦 Image/Artifact Versioning")
        st.markdown("Manage container images and artifact versions")
        
        # Mode indicator
        if st.session_state.demo_mode:
            st.info("📋 Demo Mode: Viewing sample container images")
        else:
            st.warning("🟢 Live Mode: Real container registry data")
        
        st.markdown("---")
        
        images = DemoDataProvider.get_container_images()
        
        # Display images
        for image in images:
            with st.expander(f"📦 {image['name']} - v{image['latest_version']}", expanded=True):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"**Registry:** {image['registry']}")
                    st.markdown(f"**Latest Version:** {image['latest_version']}")
                    st.markdown(f"**Total Versions:** {image['total_versions']}")
                
                with col2:
                    st.markdown(f"**Last Updated:** {image['last_updated']}")
                    st.markdown(f"**Size:** {image['size']}")
                    st.markdown(f"**Deployments:** {image['deployments']}")
                
                with col3:
                    if image['security_status'] == 'Clean':
                        st.success(f"✅ {image['security_status']}")
                    else:
                        st.warning(f"⚠️ {image['security_status']}")
                    st.markdown(f"**Vulnerabilities:** {image['vulnerabilities']}")
                
                # Action buttons
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    if st.button("📋 View Versions", key=f"versions_{image['name']}"):
                        st.info("Version history displayed")
                with col2:
                    if st.button("🔍 Scan", key=f"scan_{image['name']}"):
                        st.success("Security scan initiated")
                with col3:
                    if st.button("🚀 Deploy", key=f"deploy_img_{image['name']}"):
                        st.success("Deployment initiated")
                with col4:
                    if st.button("🗑️ Delete Old", key=f"delete_{image['name']}"):
                        st.warning("Old versions marked for deletion")
    
    @staticmethod
    def render_iac_registry():
        """IaC Module Registry interface"""
        
        st.markdown("## 📚 IaC Module Registry")
        st.markdown("Centralized registry for Infrastructure as Code modules")
        
        # Mode indicator
        if st.session_state.demo_mode:
            st.info("📋 Demo Mode: Viewing sample IaC modules")
        else:
            st.warning("🟢 Live Mode: Real IaC module registry")
        
        st.markdown("---")
        
        modules = DemoDataProvider.get_iac_modules()
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            type_filter = st.selectbox("Type", ["All", "Terraform", "CloudFormation", "CDK"])
        with col2:
            category_filter = st.selectbox("Category", ["All", "Network", "Compute", "Database", "Storage"])
        with col3:
            search = st.text_input("Search", placeholder="Search modules...")
        
        st.markdown("---")
        
        # Display modules
        for module in modules:
            if (type_filter == "All" or module['type'] == type_filter) and \
               (category_filter == "All" or module['category'] == category_filter):
                
                with st.expander(f"📦 {module['name']} - v{module['version']}", expanded=False):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**Description:** {module['description']}")
                        st.markdown(f"**Type:** {module['type']}")
                        st.markdown(f"**Category:** {module['category']}")
                        st.markdown(f"**Version:** {module['version']}")
                    
                    with col2:
                        st.markdown(f"**Author:** {module['author']}")
                        st.markdown(f"**Downloads:** {module['downloads']}")
                        st.markdown(f"**Rating:** {'⭐' * module['rating']}")
                    
                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("📥 Download", key=f"download_{module['id']}"):
                            st.success("Module downloaded")
                    with col2:
                        if st.button("📋 View Docs", key=f"docs_{module['id']}"):
                            st.info("Documentation displayed")
                    with col3:
                        if st.button("🚀 Use Module", key=f"use_{module['id']}"):
                            st.success("Module added to project")
    
    @staticmethod
    def render_design_validation():
        """Design-Time Validation interface"""
        
        st.markdown("## ✅ Design-Time Validation")
        st.markdown("Validate architecture designs before deployment")
        
        # Mode indicator
        if st.session_state.demo_mode:
            st.info("📋 Demo Mode: Viewing sample validation results")
        else:
            st.warning("🟢 Live Mode: Real validation checks")
        
        st.markdown("---")
        
        data = DemoDataProvider.get_validation_dashboard()
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Validations", data['total_validations'])
        with col2:
            st.metric("Passed", data['passed'], f"{data['pass_rate']}%")
        with col3:
            st.metric("Failed", data['failed'])
        with col4:
            st.metric("Warnings", data['warnings'])
        
        st.markdown("---")
        
        # Security checks
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔒 Security Checks")
            for check in data['security_checks']:
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    if check['passed']:
                        st.success(f"✅ {check['name']}")
                    else:
                        st.error(f"❌ {check['name']}")
                with col_b:
                    st.metric("Score", f"{check['score']}%")
        
        with col2:
            st.markdown("### 📋 Compliance Checks")
            for check in data['compliance_checks']:
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    if check['passed']:
                        st.success(f"✅ {check['name']}")
                    else:
                        st.error(f"❌ {check['name']}")
                with col_b:
                    st.metric("Score", f"{check['score']}%")
        
        st.markdown("---")
        
        # Run new validation
        st.markdown("### 🔍 Run New Validation")
        
        with st.form("run_validation"):
            validation_type = st.selectbox(
                "Validation Type",
                ["Full Architecture Review", "Security Only", "Compliance Only", "Cost Optimization"]
            )
            
            blueprint_select = st.selectbox(
                "Select Blueprint",
                ["Three-Tier Web Application", "Serverless API Backend", "Data Lake Analytics"]
            )
            
            frameworks = st.multiselect(
                "Compliance Frameworks",
                ["PCI DSS", "HIPAA", "GDPR", "SOC 2", "ISO 27001"]
            )
            
            submitted = st.form_submit_button("▶️ Run Validation", type="primary")
            
            if submitted:
                with st.spinner("Running validation checks..."):
                    import time
                    time.sleep(2)
                    st.success("""
                    ✅ **Validation Complete**
                    
                    - Security: 92% (2 warnings)
                    - Compliance: 88% (All frameworks passed)
                    - Cost: Optimized (Estimated $1,250/mo)
                    - Best Practices: 95% (1 recommendation)
                    
                    Ready for deployment!
                    """)
