"""Design & Planning Module - All 6 Sub-modules"""

import streamlit as st
import pandas as pd
from demo_data import DemoDataProvider

class DesignPlanningModule:
    """Design & Planning module with 6 sub-modules"""
    
    @staticmethod
    def render_blueprint_definition():
        """Blueprint Definition Module"""
        st.markdown("## 📋 Blueprint Definition")
        st.markdown("Define and manage reusable architecture blueprints.")
        
        tabs = st.tabs(["Blueprint Library", "Create New", "Blueprint Details"])
        
        with tabs[0]:
            st.markdown("### 📚 Blueprint Library")
            
            if st.session_state.demo_mode:
                blueprints = DemoDataProvider.get_blueprint_library()
                
                # Filter options
                col1, col2 = st.columns(2)
                with col1:
                    category = st.selectbox("Category", ["All", "Web Application", "Serverless", "Data Analytics", "Microservices"])
                with col2:
                    env = st.selectbox("Environment", ["All", "Production", "Development", "Staging"])
                
                # Display blueprints
                for bp in blueprints:
                    with st.expander(f"📋 {bp['name']} - v{bp['version']}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"**Category:** {bp['category']}")
                            st.markdown(f"**Status:** {bp['status']}")
                            st.markdown(f"**Description:** {bp['description']}")
                            st.markdown(f"**Author:** {bp['author']}")
                        
                        with col2:
                            st.metric("Est. Monthly Cost", f"${bp['estimated_cost']}")
                            st.metric("Deployments", bp['deployment_count'])
                            st.markdown(f"**Services:** {', '.join(bp['aws_services'][:4])}")
                            st.markdown(f"**Compliance:** {', '.join(bp['compliance_frameworks'])}")
                        
                        st.markdown("**IaC Template:**")
                        st.code(bp['iac_template'], language='hcl')
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.button("Clone", key=f"clone_{bp['id']}")
                        with col2:
                            st.button("Deploy", key=f"deploy_{bp['id']}")
                        with col3:
                            st.button("Export", key=f"export_{bp['id']}")
            else:
                st.info("Connect to AWS to view your blueprints")
        
        with tabs[1]:
            st.markdown("### ➕ Create New Blueprint")
            
            with st.form("create_blueprint"):
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input("Blueprint Name *", placeholder="My Architecture")
                    category = st.selectbox("Category *", ["Web Application", "Serverless", "Data Analytics", "Microservices"])
                    version = st.text_input("Version *", value="1.0.0")
                
                with col2:
                    author = st.text_input("Author", placeholder="Your Name")
                    status = st.selectbox("Status", ["Draft", "Active", "Deprecated"])
                
                description = st.text_area("Description *", placeholder="Describe your architecture...")
                
                st.markdown("#### AWS Services")
                services = st.multiselect(
                    "Select Services",
                    ["VPC", "EC2", "Lambda", "RDS", "S3", "DynamoDB", "EKS", "ALB", "CloudFront"]
                )
                
                st.markdown("#### Compliance")
                compliance = st.multiselect(
                    "Compliance Frameworks",
                    ["PCI DSS", "HIPAA", "GDPR", "SOC 2", "ISO 27001"]
                )
                
                iac_template = st.text_area("IaC Template", placeholder="Paste your template...", height=150)
                
                submitted = st.form_submit_button("Create Blueprint", type="primary")
                
                if submitted and name:
                    st.success(f"✅ Blueprint '{name}' created successfully!")
        
        with tabs[2]:
            st.markdown("### 🔍 Blueprint Details")
            
            if st.session_state.demo_mode:
                blueprints = DemoDataProvider.get_blueprint_library()
                selected = st.selectbox(
                    "Select Blueprint",
                    range(len(blueprints)),
                    format_func=lambda i: blueprints[i]['name']
                )
                
                bp = blueprints[selected]
                
                st.markdown(f"## {bp['name']}")
                st.markdown(f"**Version:** {bp['version']} | **Status:** {bp['status']}")
                st.markdown(f"**Category:** {bp['category']}")
                st.markdown(f"**Description:** {bp['description']}")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Monthly Cost", f"${bp['estimated_cost']}")
                with col2:
                    st.metric("Services", len(bp['aws_services']))
                with col3:
                    st.metric("Deployments", bp['deployment_count'])
    
    @staticmethod
    def render_tagging_standards():
        """Tagging Standards Module"""
        st.markdown("## 🏷️ Tagging Standards")
        st.markdown("Define and enforce consistent tagging policies.")
        
        tabs = st.tabs(["Tag Policies", "Create Policy", "Validation", "Reports"])
        
        with tabs[0]:
            st.markdown("### 📋 Active Tag Policies")
            
            if st.session_state.demo_mode:
                policies = DemoDataProvider.get_tag_policies()
                
                for policy in policies:
                    with st.expander(f"🏷️ {policy['name']} - {policy['status']}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"**Description:** {policy['description']}")
                            st.markdown(f"**Scope:** {policy['scope']}")
                            st.markdown(f"**Enforcement:** {policy['enforcement']}")
                        
                        with col2:
                            st.markdown("**Required Tags:**")
                            for tag in policy['required_tags']:
                                st.markdown(f"- `{tag['key']}`: {tag['description']}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.button("Edit", key=f"edit_{policy['id']}")
                        with col2:
                            st.button("Disable", key=f"disable_{policy['id']}")
            else:
                st.info("No policies defined. Create your first policy.")
        
        with tabs[1]:
            st.markdown("### ➕ Create Tag Policy")
            
            with st.form("create_policy"):
                col1, col2 = st.columns(2)
                
                with col1:
                    policy_name = st.text_input("Policy Name *", placeholder="Production Tagging")
                    scope = st.selectbox("Scope", ["Organization", "Account", "OU"])
                
                with col2:
                    enforcement = st.selectbox("Enforcement", ["Mandatory", "Recommended", "Optional"])
                    status = st.selectbox("Status", ["Active", "Draft", "Disabled"])
                
                description = st.text_area("Description", placeholder="Describe this policy...")
                
                st.markdown("#### Required Tags")
                num_tags = st.number_input("Number of Tags", min_value=1, max_value=10, value=4)
                
                for i in range(num_tags):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.text_input(f"Tag Key {i+1}", key=f"key_{i}", placeholder="Environment")
                    with col2:
                        st.text_input(f"Description {i+1}", key=f"desc_{i}", placeholder="Environment name")
                
                submitted = st.form_submit_button("Create Policy", type="primary")
                
                if submitted and policy_name:
                    st.success(f"✅ Policy '{policy_name}' created!")
        
        with tabs[2]:
            st.markdown("### ✅ Tag Validation")
            
            if st.session_state.demo_mode:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Resources", "1543")
                with col2:
                    st.metric("Compliant", "1421", delta="92%")
                with col3:
                    st.metric("Non-Compliant", "122")
                
                st.markdown("---")
                
                violations = [
                    {"Resource": "i-0abc123", "Type": "EC2", "Missing Tags": "Environment, Owner", "Severity": "High"},
                    {"Resource": "s3-prod-data", "Type": "S3", "Missing Tags": "Compliance", "Severity": "Critical"},
                    {"Resource": "rds-main", "Type": "RDS", "Missing Tags": "CostCenter", "Severity": "Medium"}
                ]
                
                st.dataframe(pd.DataFrame(violations), use_container_width=True, hide_index=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Run Validation", type="primary"):
                        st.success("✅ Validation completed!")
                with col2:
                    if st.button("Export Report"):
                        st.info("Report exported")
            else:
                st.info("Configure AWS to run validation")
        
        with tabs[3]:
            st.markdown("### 📊 Compliance Reports")
            
            if st.session_state.demo_mode:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### Compliance Trend")
                    trend_data = pd.DataFrame({
                        "Week": ["Week 1", "Week 2", "Week 3", "Week 4"],
                        "Compliance %": [85, 87, 89, 92]
                    })
                    st.line_chart(trend_data.set_index("Week"))
                
                with col2:
                    st.markdown("#### Top Violations")
                    violations_data = pd.DataFrame({
                        "Type": ["Missing Environment", "Missing Owner", "Missing Cost Center"],
                        "Count": [45, 38, 32]
                    })
                    st.bar_chart(violations_data.set_index("Type"))
    
    @staticmethod
    def render_naming_conventions():
        """Naming Conventions Module"""
        st.markdown("## 📛 Naming Conventions")
        st.markdown("Define and enforce standardized resource naming.")
        
        tabs = st.tabs(["Naming Rules", "Create Rule", "Validation", "Examples"])
        
        with tabs[0]:
            st.markdown("### 📋 Active Naming Rules")
            
            if st.session_state.demo_mode:
                rules = DemoDataProvider.get_naming_rules()
                
                for rule in rules:
                    with st.expander(f"📛 {rule['resource_type']} - {rule['enforcement']}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"**Pattern:** `{rule['pattern']}`")
                            st.markdown(f"**Description:** {rule['description']}")
                            st.markdown(f"**Enforcement:** {rule['enforcement']}")
                        
                        with col2:
                            st.markdown(f"**Example:** `{rule['example']}`")
                            st.markdown("**Pattern Breakdown:**")
                            st.markdown("- {project}: Project code")
                            st.markdown("- {env}: Environment")
                            st.markdown("- {purpose}: Resource purpose")
        
        with tabs[1]:
            st.markdown("### ➕ Create Naming Rule")
            
            with st.form("create_naming_rule"):
                col1, col2 = st.columns(2)
                
                with col1:
                    resource_type = st.selectbox(
                        "Resource Type *",
                        ["EC2 Instance", "S3 Bucket", "RDS Database", "Lambda Function", "IAM Role"]
                    )
                    enforcement = st.selectbox("Enforcement", ["Mandatory", "Recommended", "Optional"])
                
                with col2:
                    scope = st.selectbox("Scope", ["Global", "Account", "Region"])
                    status = st.selectbox("Status", ["Active", "Draft"])
                
                st.markdown("#### Pattern Components")
                components = st.multiselect(
                    "Select Components (in order)",
                    ["Project", "Environment", "Region", "Resource Type", "Purpose", "Counter"],
                    default=["Project", "Environment", "Resource Type", "Counter"]
                )
                
                separator = st.selectbox("Separator", ["-", "_", "."])
                
                # Generate pattern
                pattern = separator.join([f"{{{c.lower()}}}" for c in components])
                st.info(f"Generated Pattern: `{pattern}`")
                
                example = st.text_input("Example", placeholder="myapp-prod-ec2-web-001")
                description = st.text_area("Description")
                
                submitted = st.form_submit_button("Create Rule", type="primary")
                
                if submitted:
                    st.success(f"✅ Naming rule for '{resource_type}' created!")
        
        with tabs[2]:
            st.markdown("### ✅ Name Validation")
            
            col1, col2 = st.columns(2)
            
            with col1:
                resource_type = st.selectbox("Resource Type", ["EC2 Instance", "S3 Bucket", "RDS Database"])
                resource_name = st.text_input("Resource Name", placeholder="myapp-prod-ec2-web-001")
                
                if st.button("Validate", type="primary"):
                    if resource_name and "-" in resource_name:
                        st.success(f"✅ '{resource_name}' is valid!")
                        st.info("Follows pattern: {project}-{env}-{type}-{counter}")
                    else:
                        st.error(f"❌ '{resource_name}' is invalid!")
                        st.warning("Missing required separator '-'")
            
            with col2:
                st.markdown("#### Validation Stats")
                st.metric("Total Validated", "1543")
                st.metric("Passed", "1421")
                st.metric("Failed", "122")
        
        with tabs[3]:
            st.markdown("### 📝 Naming Examples")
            
            examples = [
                {"Type": "EC2 Instance", "Example": "myapp-prod-ec2-web-001", "Explanation": "Project: myapp, Env: prod, Purpose: web"},
                {"Type": "S3 Bucket", "Example": "acme-myapp-prod-data", "Explanation": "Org: acme, Project: myapp, Env: prod"},
                {"Type": "Lambda Function", "Example": "myapp-prod-lambda-api", "Explanation": "Project: myapp, Env: prod, Purpose: api"},
            ]
            
            for ex in examples:
                st.markdown(f"#### {ex['Type']}")
                st.code(ex['Example'])
                st.markdown(ex['Explanation'])
                st.markdown("---")
    
    @staticmethod
    def render_artifact_versioning():
        """Image/Artifact Versioning Module"""
        st.markdown("## 📦 Image/Artifact Versioning")
        st.markdown("Manage container images and deployment artifacts.")
        
        tabs = st.tabs(["Image Registry", "Versions", "Lifecycle", "Security"])
        
        with tabs[0]:
            st.markdown("### 📚 Container Image Registry")
            
            if st.session_state.demo_mode:
                images = DemoDataProvider.get_container_images()
                
                for img in images:
                    with st.expander(f"📦 {img['name']} - v{img['latest_version']}"):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.markdown(f"**Registry:** {img['registry']}")
                            st.markdown(f"**Latest:** {img['latest_version']}")
                            st.markdown(f"**Total Versions:** {img['total_versions']}")
                        
                        with col2:
                            st.markdown(f"**Updated:** {img['last_updated']}")
                            st.markdown(f"**Size:** {img['size']}")
                            st.markdown(f"**Deployments:** {img['deployments']}")
                        
                        with col3:
                            status_color = "🟢" if img['security_status'] == "Clean" else "🟡"
                            st.markdown(f"**Security:** {status_color} {img['security_status']}")
                            st.markdown(f"**Vulnerabilities:** {img['vulnerabilities']}")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.button("View Details", key=f"view_{img['name']}")
                        with col2:
                            st.button("Scan", key=f"scan_{img['name']}")
                        with col3:
                            st.button("Deploy", key=f"deploy_{img['name']}")
        
        with tabs[1]:
            st.markdown("### 🔄 Version Management")
            
            versions = [
                {"Image": "api-service", "Version": "2.3.1", "Date": "2024-11-17", "Env": "Production", "Status": "Active"},
                {"Image": "api-service", "Version": "2.3.0", "Date": "2024-11-10", "Env": "Staging", "Status": "Stable"},
                {"Image": "web-frontend", "Version": "1.8.5", "Date": "2024-11-16", "Env": "Production", "Status": "Active"},
            ]
            
            st.dataframe(pd.DataFrame(versions), use_container_width=True, hide_index=True)
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Promote Version")
                current_version = st.text_input("Version", value="2.3.1")
                target_env = st.selectbox("Target", ["Staging", "Production"])
                if st.button("Promote", type="primary"):
                    st.success(f"✅ Promoted v{current_version} to {target_env}")
            
            with col2:
                st.markdown("#### Create Version")
                base_version = st.text_input("Base", value="2.3.1")
                version_type = st.selectbox("Type", ["Major", "Minor", "Patch"])
                if st.button("Create"):
                    st.success("✅ New version created!")
        
        with tabs[2]:
            st.markdown("### ♻️ Lifecycle Policies")
            
            st.markdown("""
            **Production Image Retention**
            - Keep last 10 versions
            - Delete untagged after 7 days
            - Archive after 90 days
            """)
            
            st.markdown("""
            **Development Cleanup**
            - Keep last 5 versions
            - Delete untagged after 1 day
            - Delete old after 30 days
            """)
            
            if st.button("Create Policy"):
                st.info("Policy creation form would open here")
        
        with tabs[3]:
            st.markdown("### 🔒 Security Scanning")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Images Scanned", "87")
            with col2:
                st.metric("Critical", "2", delta="-1")
            with col3:
                st.metric("High", "5")
            with col4:
                st.metric("Medium/Low", "23")
            
            st.markdown("---")
            
            vulnerabilities = [
                {"Image": "api-service:2.3.1", "CVE": "CVE-2024-1234", "Severity": "Critical", "Package": "openssl"},
                {"Image": "web-frontend:1.8.5", "CVE": "CVE-2024-5678", "Severity": "High", "Package": "nginx"},
            ]
            
            st.dataframe(pd.DataFrame(vulnerabilities), use_container_width=True, hide_index=True)
            
            if st.button("Run Scan", type="primary"):
                st.success("✅ Security scan initiated")
    
    @staticmethod
    def render_iac_registry():
        """IaC Module Registry"""
        st.markdown("## 📚 IaC Module Registry")
        st.markdown("Centralized Infrastructure as Code modules and templates.")
        
        tabs = st.tabs(["Module Library", "Upload Module", "Module Details", "Analytics"])
        
        with tabs[0]:
            st.markdown("### 📚 Module Library")
            
            if st.session_state.demo_mode:
                modules = DemoDataProvider.get_iac_modules()
                
                # Filters
                col1, col2, col3 = st.columns(3)
                with col1:
                    iac_type = st.selectbox("IaC Type", ["All", "Terraform", "CloudFormation", "CDK"])
                with col2:
                    category = st.selectbox("Category", ["All", "Network", "Compute", "Database", "Security"])
                with col3:
                    search = st.text_input("Search", placeholder="Search modules...")
                
                # Display modules
                for mod in modules:
                    with st.expander(f"📦 {mod['name']} - v{mod['version']}"):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.markdown(f"**Type:** {mod['type']}")
                            st.markdown(f"**Category:** {mod['category']}")
                            st.markdown(f"**Description:** {mod['description']}")
                            st.markdown(f"**Author:** {mod['author']}")
                        
                        with col2:
                            st.metric("Downloads", mod['downloads'])
                            st.metric("Rating", f"{'⭐' * mod['rating']}")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.button("View", key=f"view_{mod['id']}")
                        with col2:
                            st.button("Download", key=f"dl_{mod['id']}")
                        with col3:
                            st.button("Use", key=f"use_{mod['id']}")
        
        with tabs[1]:
            st.markdown("### ⬆️ Upload Module")
            
            with st.form("upload_module"):
                col1, col2 = st.columns(2)
                
                with col1:
                    module_name = st.text_input("Module Name *", placeholder="my-module")
                    module_type = st.selectbox("Type *", ["Terraform", "CloudFormation", "CDK", "Pulumi"])
                    version = st.text_input("Version *", value="1.0.0")
                
                with col2:
                    category = st.selectbox("Category", ["Network", "Compute", "Database", "Security", "Storage"])
                    visibility = st.selectbox("Visibility", ["Public", "Private", "Organization"])
                
                description = st.text_area("Description *", placeholder="Module description...")
                
                uploaded_files = st.file_uploader("Module Files", accept_multiple_files=True)
                
                readme = st.text_area("README", placeholder="# Module Documentation", height=150)
                
                submitted = st.form_submit_button("Upload Module", type="primary")
                
                if submitted and module_name:
                    st.success(f"✅ Module '{module_name}' uploaded!")
        
        with tabs[2]:
            st.markdown("### 🔍 Module Details")
            
            if st.session_state.demo_mode:
                modules = DemoDataProvider.get_iac_modules()
                selected = st.selectbox(
                    "Select Module",
                    range(len(modules)),
                    format_func=lambda i: modules[i]['name']
                )
                
                mod = modules[selected]
                
                st.markdown(f"## {mod['name']}")
                st.markdown(f"**Version:** {mod['version']} | **Type:** {mod['type']}")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Downloads", mod['downloads'])
                with col2:
                    st.metric("Rating", f"{'⭐' * mod['rating']}")
                with col3:
                    st.metric("Version", mod['version'])
                
                st.markdown("---")
                st.markdown(f"**Description:** {mod['description']}")
        
        with tabs[3]:
            st.markdown("### 📊 Usage Analytics")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Modules", "87")
            with col2:
                st.metric("Total Downloads", "15,432")
            with col3:
                st.metric("Active Users", "234")
            with col4:
                st.metric("Avg Rating", "4.6⭐")
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Downloads by Type")
                dl_data = pd.DataFrame({
                    "Type": ["Terraform", "CloudFormation", "CDK", "Pulumi"],
                    "Downloads": [8500, 4200, 2100, 632]
                })
                st.bar_chart(dl_data.set_index("Type"))
            
            with col2:
                st.markdown("#### Popular Modules")
                pop_data = pd.DataFrame({
                    "Module": ["vpc-standard", "eks-cluster", "rds-postgres"],
                    "Downloads": [312, 289, 189]
                })
                st.bar_chart(pop_data.set_index("Module"))
    
    @staticmethod
    def render_design_validation():
        """Design-Time Validation Module"""
        st.markdown("## ✅ Design-Time Validation")
        st.markdown("Validate infrastructure designs before deployment.")
        
        tabs = st.tabs(["Dashboard", "Run Validation", "Validation Rules", "Remediation"])
        
        with tabs[0]:
            st.markdown("### 📊 Validation Dashboard")
            
            if st.session_state.demo_mode:
                dashboard = DemoDataProvider.get_validation_dashboard()
                
                # Key metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Validations", dashboard['total_validations'])
                with col2:
                    st.metric("Passed", dashboard['passed'], delta=f"+{dashboard['pass_rate']}%")
                with col3:
                    st.metric("Failed", dashboard['failed'])
                with col4:
                    st.metric("Warnings", dashboard['warnings'])
                
                st.markdown("---")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### Security Checks")
                    for check in dashboard['security_checks']:
                        status = "✅" if check['passed'] else "❌"
                        st.markdown(f"{status} {check['name']}: {check['score']}%")
                
                with col2:
                    st.markdown("#### Compliance Checks")
                    for check in dashboard['compliance_checks']:
                        status = "✅" if check['passed'] else "❌"
                        st.markdown(f"{status} {check['name']}: {check['score']}%")
        
        with tabs[1]:
            st.markdown("### ▶️ Run Validation")
            
            validation_type = st.multiselect(
                "Validation Categories",
                ["Security", "Compliance", "Best Practices", "Cost", "Performance"],
                default=["Security", "Compliance"]
            )
            
            target = st.selectbox(
                "Target",
                ["Current Blueprint", "IaC Template", "Deployed Resources"]
            )
            
            if target == "IaC Template":
                uploaded_file = st.file_uploader("Upload Template", type=['tf', 'yaml', 'json'])
            
            severity = st.multiselect(
                "Severity Levels",
                ["Critical", "High", "Medium", "Low"],
                default=["Critical", "High"]
            )
            
            if st.button("🚀 Run Validation", type="primary"):
                with st.spinner("Running validation..."):
                    import time
                    time.sleep(1)
                    
                    st.success("✅ Validation completed!")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Checks", "127")
                    with col2:
                        st.metric("Passed", "98")
                    with col3:
                        st.metric("Failed", "18")
                    
                    st.markdown("---")
                    
                    issues = [
                        {"Resource": "vpc-prod", "Issue": "Security Group Too Open", "Severity": "High"},
                        {"Resource": "rds-main", "Issue": "Backup < 30 days", "Severity": "Medium"},
                        {"Resource": "s3-data", "Issue": "No Lifecycle Policy", "Severity": "Low"},
                    ]
                    
                    st.dataframe(pd.DataFrame(issues), use_container_width=True, hide_index=True)
        
        with tabs[2]:
            st.markdown("### 📜 Validation Rules")
            
            rules = [
                {
                    "name": "S3 Encryption Required",
                    "severity": "Critical",
                    "category": "Security",
                    "description": "All S3 buckets must have encryption",
                    "auto_fix": True
                },
                {
                    "name": "RDS Backup Retention",
                    "severity": "High",
                    "category": "Reliability",
                    "description": "RDS backups >= 30 days",
                    "auto_fix": False
                },
                {
                    "name": "Security Group 0.0.0.0/0",
                    "severity": "Critical",
                    "category": "Security",
                    "description": "No ingress from 0.0.0.0/0",
                    "auto_fix": False
                }
            ]
            
            for rule in rules:
                with st.expander(f"{rule['severity']} - {rule['name']}"):
                    st.markdown(f"**Category:** {rule['category']}")
                    st.markdown(f"**Description:** {rule['description']}")
                    st.markdown(f"**Auto-Remediate:** {'Yes' if rule['auto_fix'] else 'No'}")
        
        with tabs[3]:
            st.markdown("### 🔧 Remediation")
            
            issues = [
                {
                    "title": "Unencrypted S3 Bucket",
                    "resource": "s3://prod-data",
                    "severity": "Critical",
                    "auto_fix": True
                },
                {
                    "title": "Security Group Too Open",
                    "resource": "sg-0abc123",
                    "severity": "High",
                    "auto_fix": False
                }
            ]
            
            for issue in issues:
                with st.expander(f"{issue['severity']} - {issue['title']}"):
                    st.markdown(f"**Resource:** {issue['resource']}")
                    st.markdown(f"**Severity:** {issue['severity']}")
                    
                    if issue['auto_fix']:
                        if st.button("🔧 Auto-Remediate", key=f"fix_{issue['title']}"):
                            st.success("✅ Issue remediated!")
                    else:
                        st.info("Manual remediation required")
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔧 Remediate All Auto-Fix"):
                    st.success("✅ Auto-remediation initiated")
            with col2:
                if st.button("📥 Export Issues"):
                    st.info("Issues exported to CSV")
