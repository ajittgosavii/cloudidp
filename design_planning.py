"""
Design & Planning Module
Handles blueprint definition, tagging standards, naming conventions, etc.
Enhanced with cost analysis, architecture visualization, and advanced validation
"""

import streamlit as st
import pandas as pd
import json
import yaml
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from demo_data import DemoDataProvider
import plotly.graph_objects as go
import plotly.express as px

class DesignPlanningModule:
    """Design & Planning functionality"""
    
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
    
    @staticmethod
    def render_cost_analysis():
        """Advanced Cost Analysis & Optimization"""
        
        st.markdown("## 💰 Cost Analysis & Optimization")
        st.markdown("Analyze and optimize infrastructure costs across blueprints")
        
        # Mode indicator
        if st.session_state.demo_mode:
            st.info("📋 Demo Mode: Viewing sample cost analysis")
        else:
            st.warning("🟢 Live Mode: Real cost data")
        
        st.markdown("---")
        
        # Cost Overview
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Current Monthly Cost", "$12,450", "-8%")
        with col2:
            st.metric("Projected (Next Month)", "$11,850", "-$600")
        with col3:
            st.metric("Potential Savings", "$2,340", "+12%")
        with col4:
            st.metric("Optimization Score", "78%", "+5%")
        
        st.markdown("---")
        
        # Cost breakdown by service
        st.markdown("### 📊 Cost Breakdown by Service")
        
        cost_data = {
            'Service': ['EC2', 'RDS', 'S3', 'Lambda', 'CloudFront', 'ALB', 'NAT Gateway', 'Others'],
            'Current': [4200, 2800, 1500, 850, 1200, 600, 800, 500],
            'Optimized': [3400, 2400, 1200, 750, 1000, 500, 600, 400]
        }
        
        df_cost = pd.DataFrame(cost_data)
        df_cost['Savings'] = df_cost['Current'] - df_cost['Optimized']
        df_cost['Savings %'] = ((df_cost['Savings'] / df_cost['Current']) * 100).round(1)
        
        # Create cost comparison chart
        fig = go.Figure(data=[
            go.Bar(name='Current', x=df_cost['Service'], y=df_cost['Current'], marker_color='lightblue'),
            go.Bar(name='Optimized', x=df_cost['Service'], y=df_cost['Optimized'], marker_color='green')
        ])
        fig.update_layout(
            barmode='group',
            title='Current vs Optimized Costs by Service',
            xaxis_title='AWS Service',
            yaxis_title='Monthly Cost ($)',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed cost table
        st.markdown("### 📋 Detailed Cost Analysis")
        st.dataframe(df_cost, use_container_width=True)
        
        st.markdown("---")
        
        # Optimization recommendations
        st.markdown("### 💡 Cost Optimization Recommendations")
        
        recommendations = [
            {
                'priority': 'High',
                'category': 'EC2 Right-Sizing',
                'description': 'Downsize 12 over-provisioned EC2 instances',
                'savings': '$800/mo',
                'effort': 'Low',
                'impact': 'High'
            },
            {
                'priority': 'High',
                'category': 'Reserved Instances',
                'description': 'Purchase RDS reserved instances for production databases',
                'savings': '$600/mo',
                'effort': 'Low',
                'impact': 'High'
            },
            {
                'priority': 'Medium',
                'category': 'S3 Lifecycle',
                'description': 'Implement lifecycle policies for infrequently accessed data',
                'savings': '$300/mo',
                'effort': 'Medium',
                'impact': 'Medium'
            },
            {
                'priority': 'Medium',
                'category': 'Lambda Optimization',
                'description': 'Optimize Lambda memory allocation based on usage patterns',
                'savings': '$100/mo',
                'effort': 'Low',
                'impact': 'Low'
            },
            {
                'priority': 'Low',
                'category': 'NAT Gateway',
                'description': 'Consolidate NAT Gateways across availability zones',
                'savings': '$200/mo',
                'effort': 'High',
                'impact': 'Medium'
            }
        ]
        
        for rec in recommendations:
            with st.expander(f"{'🔴' if rec['priority'] == 'High' else '🟡' if rec['priority'] == 'Medium' else '🟢'} {rec['category']} - {rec['savings']}", expanded=rec['priority'] == 'High'):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"**Priority:** {rec['priority']}")
                    st.markdown(f"**Savings:** {rec['savings']}")
                
                with col2:
                    st.markdown(f"**Effort:** {rec['effort']}")
                    st.markdown(f"**Impact:** {rec['impact']}")
                
                with col3:
                    if st.button("Apply", key=f"apply_{rec['category']}"):
                        st.success(f"Optimization applied: {rec['category']}")
                
                st.markdown(f"**Description:** {rec['description']}")
        
        st.markdown("---")
        
        # Cost forecast
        st.markdown("### 📈 Cost Forecast (Next 6 Months)")
        
        forecast_data = {
            'Month': ['Current', 'Month 1', 'Month 2', 'Month 3', 'Month 4', 'Month 5', 'Month 6'],
            'Without Optimization': [12450, 12800, 13100, 13500, 13900, 14200, 14600],
            'With Optimization': [12450, 11850, 11650, 11500, 11400, 11300, 11200]
        }
        
        df_forecast = pd.DataFrame(forecast_data)
        
        fig_forecast = go.Figure()
        fig_forecast.add_trace(go.Scatter(
            x=df_forecast['Month'], 
            y=df_forecast['Without Optimization'],
            mode='lines+markers',
            name='Without Optimization',
            line=dict(color='red', width=2)
        ))
        fig_forecast.add_trace(go.Scatter(
            x=df_forecast['Month'], 
            y=df_forecast['With Optimization'],
            mode='lines+markers',
            name='With Optimization',
            line=dict(color='green', width=2)
        ))
        
        fig_forecast.update_layout(
            title='Cost Projection',
            xaxis_title='Time Period',
            yaxis_title='Monthly Cost ($)',
            height=400
        )
        st.plotly_chart(fig_forecast, use_container_width=True)
    
    @staticmethod
    def render_architecture_diagrams():
        """Architecture Diagram Generator"""
        
        st.markdown("## 🎨 Architecture Diagram Generator")
        st.markdown("Generate visual architecture diagrams from blueprints")
        
        # Mode indicator
        if st.session_state.demo_mode:
            st.info("📋 Demo Mode: Viewing sample diagrams")
        else:
            st.warning("🟢 Live Mode: Generate real architecture diagrams")
        
        st.markdown("---")
        
        # Diagram options
        col1, col2 = st.columns(2)
        
        with col1:
            blueprint = st.selectbox(
                "Select Blueprint",
                ["Three-Tier Web Application", "Serverless API Backend", "Microservices Platform", "Data Lake Analytics"]
            )
            
            diagram_type = st.selectbox(
                "Diagram Type",
                ["AWS Architecture", "Network Topology", "Data Flow", "Deployment Pipeline", "Security Groups"]
            )
        
        with col2:
            style = st.selectbox(
                "Diagram Style",
                ["AWS Official", "Detailed Technical", "High-Level Overview", "Minimalist"]
            )
            
            include_annotations = st.checkbox("Include Annotations", value=True)
            show_costs = st.checkbox("Show Cost Estimates", value=False)
        
        if st.button("🎨 Generate Diagram", type="primary"):
            with st.spinner("Generating architecture diagram..."):
                import time
                time.sleep(2)
                
                st.success("✅ Diagram generated successfully!")
                
                # Placeholder for diagram
                st.markdown("### Generated Architecture Diagram")
                st.info("📊 Interactive diagram would be displayed here with mermaid or other visualization library")
                
                # Sample mermaid diagram
                mermaid_code = """
                graph TB
                    User[User] -->|HTTPS| CF[CloudFront]
                    CF -->|Origin| ALB[Application Load Balancer]
                    ALB -->|Route| EC2_1[EC2 Instance 1]
                    ALB -->|Route| EC2_2[EC2 Instance 2]
                    ALB -->|Route| EC2_3[EC2 Instance 3]
                    EC2_1 -->|Query| RDS[(RDS Database)]
                    EC2_2 -->|Query| RDS
                    EC2_3 -->|Query| RDS
                    EC2_1 -->|Store| S3[S3 Bucket]
                    EC2_2 -->|Store| S3
                    EC2_3 -->|Store| S3
                    RDS -->|Backup| S3_Backup[S3 Backup Bucket]
                    
                    style CF fill:#FF9900
                    style ALB fill:#FF9900
                    style EC2_1 fill:#FF9900
                    style EC2_2 fill:#FF9900
                    style EC2_3 fill:#FF9900
                    style RDS fill:#3B48CC
                    style S3 fill:#569A31
                    style S3_Backup fill:#569A31
                """
                
                st.code(mermaid_code, language='mermaid')
                
                # Export options
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("📥 Export PNG"):
                        st.info("PNG exported")
                with col2:
                    if st.button("📥 Export SVG"):
                        st.info("SVG exported")
                with col3:
                    if st.button("📥 Export PDF"):
                        st.info("PDF exported")
    
    @staticmethod
    def render_blueprint_comparison():
        """Blueprint Comparison Tool"""
        
        st.markdown("## ⚖️ Blueprint Comparison")
        st.markdown("Compare multiple blueprints side-by-side")
        
        # Mode indicator
        if st.session_state.demo_mode:
            st.info("📋 Demo Mode: Comparing sample blueprints")
        else:
            st.warning("🟢 Live Mode: Compare real blueprints")
        
        st.markdown("---")
        
        # Select blueprints to compare
        blueprints = [
            "Three-Tier Web Application",
            "Serverless API Backend",
            "Microservices Platform",
            "Data Lake Analytics",
            "Event-Driven Architecture"
        ]
        
        col1, col2 = st.columns(2)
        with col1:
            bp1 = st.selectbox("Blueprint 1", blueprints, index=0)
        with col2:
            bp2 = st.selectbox("Blueprint 2", blueprints, index=1)
        
        if st.button("🔄 Compare Blueprints", type="primary"):
            st.markdown("---")
            st.markdown("### 📊 Comparison Results")
            
            # Comparison table
            comparison_data = {
                'Attribute': [
                    'Architecture Style',
                    'AWS Services Used',
                    'Estimated Monthly Cost',
                    'Complexity',
                    'Setup Time',
                    'Scalability',
                    'Availability',
                    'Compliance Ready',
                    'Deployment Count',
                    'Average Rating'
                ],
                bp1: [
                    'Traditional 3-Tier',
                    'VPC, EC2, RDS, ALB, S3',
                    '$1,200/mo',
                    'Medium',
                    '2-3 hours',
                    'High (Auto-scaling)',
                    '99.95%',
                    'PCI DSS, HIPAA',
                    '245',
                    '4.5 ⭐'
                ],
                bp2: [
                    'Serverless',
                    'API Gateway, Lambda, DynamoDB',
                    '$450/mo',
                    'Low',
                    '1-2 hours',
                    'Very High (Unlimited)',
                    '99.99%',
                    'SOC 2, GDPR',
                    '187',
                    '4.7 ⭐'
                ]
            }
            
            df_comparison = pd.DataFrame(comparison_data)
            st.dataframe(df_comparison, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            
            # Detailed comparison
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"### 📋 {bp1}")
                st.markdown("**Pros:**")
                st.markdown("- ✅ Battle-tested architecture")
                st.markdown("- ✅ Easy to understand and maintain")
                st.markdown("- ✅ Good for traditional workloads")
                st.markdown("- ✅ Predictable performance")
                
                st.markdown("**Cons:**")
                st.markdown("- ❌ Higher operational costs")
                st.markdown("- ❌ Requires capacity planning")
                st.markdown("- ❌ Manual scaling configuration")
            
            with col2:
                st.markdown(f"### 📋 {bp2}")
                st.markdown("**Pros:**")
                st.markdown("- ✅ Lower costs (pay-per-use)")
                st.markdown("- ✅ Automatic scaling")
                st.markdown("- ✅ No server management")
                st.markdown("- ✅ Fast deployment")
                
                st.markdown("**Cons:**")
                st.markdown("- ❌ Cold start latency")
                st.markdown("- ❌ Limited execution time")
                st.markdown("- ❌ Vendor lock-in")
            
            st.markdown("---")
            
            # Recommendation
            st.markdown("### 💡 Recommendation")
            st.info(f"""
            **Best Choice:** {bp2}
            
            Based on the comparison, {bp2} is recommended for:
            - Lower operational costs (60% savings)
            - Better scalability characteristics
            - Faster deployment cycles
            - Modern serverless architecture
            
            Consider {bp1} if you need:
            - Traditional architecture patterns
            - Predictable, consistent performance
            - Long-running processes
            """)
    
    @staticmethod
    def render_dependency_analysis():
        """Dependency & Impact Analysis"""
        
        st.markdown("## 🔗 Dependency & Impact Analysis")
        st.markdown("Analyze dependencies between resources and assess change impact")
        
        # Mode indicator
        if st.session_state.demo_mode:
            st.info("📋 Demo Mode: Viewing sample dependency graph")
        else:
            st.warning("🟢 Live Mode: Real dependency analysis")
        
        st.markdown("---")
        
        # Select resource for analysis
        col1, col2 = st.columns(2)
        
        with col1:
            resource_type = st.selectbox(
                "Resource Type",
                ["VPC", "EC2 Instance", "RDS Database", "S3 Bucket", "Lambda Function", "API Gateway"]
            )
        
        with col2:
            resource_name = st.text_input("Resource Name/ID", placeholder="e.g., vpc-abc123")
        
        if st.button("🔍 Analyze Dependencies", type="primary"):
            st.markdown("---")
            
            # Dependency metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Direct Dependencies", "12")
            with col2:
                st.metric("Indirect Dependencies", "34")
            with col3:
                st.metric("Dependent Resources", "18")
            with col4:
                st.metric("Risk Level", "Medium", "⚠️")
            
            st.markdown("---")
            
            # Dependency tree
            st.markdown("### 🌳 Dependency Tree")
            
            dependency_tree = """
            VPC (vpc-abc123)
            ├── Subnet-Public-1a
            │   ├── EC2-WebServer-1
            │   │   ├── Security-Group-Web
            │   │   └── EBS-Volume-1
            │   ├── EC2-WebServer-2
            │   │   ├── Security-Group-Web
            │   │   └── EBS-Volume-2
            │   └── NAT-Gateway-1a
            ├── Subnet-Public-1b
            │   ├── EC2-WebServer-3
            │   │   ├── Security-Group-Web
            │   │   └── EBS-Volume-3
            │   └── NAT-Gateway-1b
            ├── Subnet-Private-1a
            │   ├── RDS-Primary
            │   │   ├── Security-Group-DB
            │   │   └── DB-Subnet-Group
            │   └── ElastiCache-Redis
            └── Subnet-Private-1b
                ├── RDS-Replica
                │   ├── Security-Group-DB
                │   └── DB-Subnet-Group
                └── ElastiCache-Redis-Replica
            """
            
            st.code(dependency_tree)
            
            st.markdown("---")
            
            # Impact analysis
            st.markdown("### 💥 Change Impact Analysis")
            
            st.warning("""
            **⚠️ Deleting or modifying this resource will affect:**
            
            - **12 direct dependencies** will be impacted
            - **3 production workloads** may experience downtime
            - **5 security groups** need to be updated
            - **18 dependent resources** require validation
            
            **Estimated Impact:**
            - Downtime: 15-30 minutes
            - Affected Users: ~2,500
            - Recovery Time: 1-2 hours
            """)
            
            # Mitigation steps
            st.markdown("### 🛡️ Mitigation Steps")
            
            mitigation_steps = [
                "1. Create snapshot/backup of all affected resources",
                "2. Notify stakeholders of planned change window",
                "3. Update dependent security groups in staging first",
                "4. Deploy changes during off-peak hours (2-4 AM)",
                "5. Monitor all dependent resources for 1 hour post-change",
                "6. Keep rollback plan ready with backup configurations"
            ]
            
            for step in mitigation_steps:
                st.markdown(step)
            
            # Action buttons
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📥 Export Analysis"):
                    st.success("Analysis exported to PDF")
            with col2:
                if st.button("📧 Send Report"):
                    st.success("Report sent to stakeholders")
            with col3:
                if st.button("📋 Create Change Ticket"):
                    st.success("Change ticket created")
    
    @staticmethod
    def render_template_testing():
        """Infrastructure Template Testing Framework"""
        
        st.markdown("## 🧪 Template Testing Framework")
        st.markdown("Test and validate infrastructure templates before deployment")
        
        # Mode indicator
        if st.session_state.demo_mode:
            st.info("📋 Demo Mode: Viewing sample test results")
        else:
            st.warning("🟢 Live Mode: Run real template tests")
        
        st.markdown("---")
        
        # Test configuration
        with st.form("template_test"):
            col1, col2 = st.columns(2)
            
            with col1:
                template_source = st.selectbox(
                    "Template Source",
                    ["Blueprint Library", "Local File", "Git Repository", "S3 Bucket"]
                )
                
                template_name = st.selectbox(
                    "Template Name",
                    ["three-tier-web.tf", "serverless-api.yaml", "microservices-eks.tf"]
                )
            
            with col2:
                test_type = st.multiselect(
                    "Test Types",
                    ["Syntax Validation", "Security Scan", "Cost Estimation", "Compliance Check", 
                     "Best Practices", "Performance Analysis", "Resource Limits"],
                    default=["Syntax Validation", "Security Scan"]
                )
                
                environment = st.selectbox("Target Environment", ["Development", "Staging", "Production"])
            
            submitted = st.form_submit_button("▶️ Run Tests", type="primary")
            
            if submitted:
                st.markdown("---")
                st.markdown("### 🔄 Running Tests...")
                
                # Progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                test_stages = [
                    "Parsing template...",
                    "Running syntax validation...",
                    "Executing security scans...",
                    "Checking compliance...",
                    "Analyzing best practices...",
                    "Generating report..."
                ]
                
                import time
                for i, stage in enumerate(test_stages):
                    status_text.text(stage)
                    progress_bar.progress((i + 1) / len(test_stages))
                    time.sleep(0.5)
                
                status_text.text("✅ Tests complete!")
                
                st.markdown("---")
                st.markdown("### 📊 Test Results")
                
                # Test summary
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Tests", "24")
                with col2:
                    st.metric("Passed", "21", "✅")
                with col3:
                    st.metric("Warnings", "2", "⚠️")
                with col4:
                    st.metric("Failed", "1", "❌")
                
                st.markdown("---")
                
                # Detailed results
                test_results = [
                    {'Test': 'Syntax Validation', 'Status': 'Passed', 'Duration': '0.3s', 'Details': 'Template syntax is valid'},
                    {'Test': 'Security - IAM Policies', 'Status': 'Passed', 'Duration': '1.2s', 'Details': 'No overly permissive policies found'},
                    {'Test': 'Security - Encryption', 'Status': 'Warning', 'Duration': '0.8s', 'Details': 'S3 bucket encryption not enforced'},
                    {'Test': 'Security - Public Access', 'Status': 'Passed', 'Duration': '0.6s', 'Details': 'No public exposure detected'},
                    {'Test': 'Compliance - PCI DSS', 'Status': 'Passed', 'Duration': '2.1s', 'Details': 'All PCI DSS requirements met'},
                    {'Test': 'Cost Estimation', 'Status': 'Warning', 'Duration': '1.5s', 'Details': 'Estimated cost: $1,250/mo (above budget)'},
                    {'Test': 'Best Practices - Tagging', 'Status': 'Passed', 'Duration': '0.4s', 'Details': 'Required tags present'},
                    {'Test': 'Best Practices - High Availability', 'Status': 'Failed', 'Duration': '0.7s', 'Details': 'Single AZ deployment detected'}
                ]
                
                for result in test_results:
                    if result['Status'] == 'Passed':
                        icon = '✅'
                        color = 'success'
                    elif result['Status'] == 'Warning':
                        icon = '⚠️'
                        color = 'warning'
                    else:
                        icon = '❌'
                        color = 'error'
                    
                    with st.expander(f"{icon} {result['Test']} - {result['Duration']}", expanded=result['Status'] != 'Passed'):
                        if color == 'success':
                            st.success(result['Details'])
                        elif color == 'warning':
                            st.warning(result['Details'])
                        else:
                            st.error(result['Details'])
                
                st.markdown("---")
                
                # Recommendations
                st.markdown("### 💡 Recommendations")
                st.info("""
                **Critical:**
                - Enable multi-AZ deployment for high availability
                
                **Important:**
                - Enable default encryption for S3 buckets
                - Review cost estimation and optimize resources
                
                **Nice to Have:**
                - Add CloudWatch alarms for critical metrics
                - Implement backup strategies
                """)
                
                # Export options
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("📥 Export Report"):
                        st.success("Test report exported")
                with col2:
                    if st.button("📧 Email Results"):
                        st.success("Results emailed to team")
                with col3:
                    if st.button("🔄 Re-run Tests"):
                        st.info("Tests scheduled for re-run")
    
    @staticmethod
    def render_multi_region_planner():
        """Multi-Region Deployment Planner"""
        
        st.markdown("## 🌍 Multi-Region Deployment Planner")
        st.markdown("Plan and optimize multi-region infrastructure deployments")
        
        # Mode indicator
        if st.session_state.demo_mode:
            st.info("📋 Demo Mode: Viewing sample multi-region configuration")
        else:
            st.warning("🟢 Live Mode: Real multi-region planning")
        
        st.markdown("---")
        
        # Region selection
        st.markdown("### 🗺️ Select Deployment Regions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            primary_region = st.selectbox(
                "Primary Region",
                ["us-east-1 (N. Virginia)", "us-west-2 (Oregon)", "eu-west-1 (Ireland)", 
                 "ap-southeast-1 (Singapore)", "ap-northeast-1 (Tokyo)"]
            )
        
        with col2:
            secondary_regions = st.multiselect(
                "Secondary Regions",
                ["us-east-2 (Ohio)", "us-west-1 (N. California)", "eu-central-1 (Frankfurt)",
                 "ap-south-1 (Mumbai)", "sa-east-1 (São Paulo)", "ca-central-1 (Canada)"],
                default=["us-west-1 (N. California)", "eu-central-1 (Frankfurt)"]
            )
        
        dr_enabled = st.checkbox("Enable Disaster Recovery", value=True)
        
        if dr_enabled:
            dr_region = st.selectbox(
                "DR Region",
                ["us-west-2 (Oregon)", "eu-west-2 (London)", "ap-southeast-2 (Sydney)"]
            )
        
        st.markdown("---")
        
        # Regional configuration
        st.markdown("### ⚙️ Regional Configuration")
        
        config_data = {
            'Region': [primary_region] + secondary_regions + ([dr_region] if dr_enabled else []),
            'Role': ['Primary'] + ['Secondary'] * len(secondary_regions) + (['DR'] if dr_enabled else []),
            'Capacity': ['100%'] + ['50%'] * len(secondary_regions) + (['Standby'] if dr_enabled else []),
            'Latency (ms)': [0] + [45, 120] + ([180] if dr_enabled else []),
            'Est. Cost/Month': ['$4,500'] + ['$2,250', '$2,250'] + (['$500'] if dr_enabled else [])
        }
        
        df_regions = pd.DataFrame(config_data)
        st.dataframe(df_regions, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Data replication
        st.markdown("### 🔄 Data Replication Strategy")
        
        replication_type = st.radio(
            "Replication Type",
            ["Active-Active", "Active-Passive", "Active-Standby"],
            horizontal=True
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            rpo = st.selectbox("Recovery Point Objective (RPO)", ["< 1 minute", "< 5 minutes", "< 1 hour", "< 24 hours"])
            sync_type = st.selectbox("Synchronization", ["Synchronous", "Asynchronous", "Semi-Synchronous"])
        
        with col2:
            rto = st.selectbox("Recovery Time Objective (RTO)", ["< 1 minute", "< 15 minutes", "< 1 hour", "< 4 hours"])
            consistency = st.selectbox("Consistency Model", ["Strong", "Eventual", "Causal"])
        
        st.markdown("---")
        
        # Traffic distribution
        st.markdown("### 🌐 Traffic Distribution")
        
        routing_policy = st.selectbox(
            "Routing Policy",
            ["Weighted", "Latency-based", "Geolocation", "Geoproximity", "Failover"]
        )
        
        # Traffic distribution chart
        traffic_data = {
            'Region': [primary_region] + secondary_regions,
            'Traffic %': [50, 25, 25][:len([primary_region] + secondary_regions)],
            'Users': [12500, 6250, 6250][:len([primary_region] + secondary_regions)]
        }
        
        df_traffic = pd.DataFrame(traffic_data)
        
        fig = px.pie(df_traffic, values='Traffic %', names='Region', title='Traffic Distribution by Region')
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Cost analysis
        st.markdown("### 💰 Multi-Region Cost Analysis")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Monthly Cost", "$9,500")
        with col2:
            st.metric("Data Transfer Cost", "$1,200")
        with col3:
            st.metric("Replication Cost", "$800")
        with col4:
            st.metric("DR Cost", "$500")
        
        st.info("""
        **Cost Breakdown:**
        - Primary Region: $4,500/mo (compute, storage, networking)
        - Secondary Regions: $4,500/mo ($2,250 each)
        - Data Transfer: $1,200/mo (cross-region replication)
        - DR Standby: $500/mo (minimal capacity)
        
        **Potential Savings:**
        - Use Regional Reserved Instances: -15% ($1,425/mo)
        - Optimize data transfer: -20% ($240/mo)
        """)
        
        st.markdown("---")
        
        # Deployment plan
        st.markdown("### 📋 Deployment Plan")
        
        if st.button("🚀 Generate Deployment Plan", type="primary"):
            st.success("""
            ✅ **Multi-Region Deployment Plan Generated**
            
            **Phase 1: Primary Region Setup**
            - Deploy core infrastructure in us-east-1
            - Configure monitoring and logging
            - Test primary workloads
            Duration: 2-3 hours
            
            **Phase 2: Secondary Regions**
            - Replicate infrastructure to us-west-1 and eu-central-1
            - Configure data replication
            - Test failover scenarios
            Duration: 3-4 hours
            
            **Phase 3: DR Region**
            - Setup standby infrastructure in us-west-2
            - Configure automated failover
            - Conduct DR drills
            Duration: 2 hours
            
            **Phase 4: Traffic Migration**
            - Gradually shift traffic to new regions
            - Monitor performance and costs
            - Optimize based on metrics
            Duration: 1 week (gradual)
            
            Total Estimated Time: 1-2 weeks
            """)

    @staticmethod
    def render_performance_estimation():
        """Performance & Capacity Estimation"""
        
        st.markdown("## 📊 Performance & Capacity Estimation")
        st.markdown("Estimate performance characteristics and capacity requirements")
        
        # Mode indicator
        if st.session_state.demo_mode:
            st.info("📋 Demo Mode: Viewing sample performance estimates")
        else:
            st.warning("🟢 Live Mode: Real performance estimation")
        
        st.markdown("---")
        
        # Workload characteristics
        st.markdown("### 📈 Workload Characteristics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            expected_users = st.number_input("Expected Concurrent Users", min_value=100, value=10000, step=100)
            requests_per_user = st.number_input("Requests per User (per hour)", min_value=1, value=50, step=5)
            avg_request_size = st.number_input("Avg Request Size (KB)", min_value=1, value=50, step=10)
        
        with col2:
            peak_multiplier = st.slider("Peak Load Multiplier", min_value=1.0, max_value=5.0, value=2.5, step=0.5)
            growth_rate = st.slider("Annual Growth Rate (%)", min_value=0, max_value=100, value=25, step=5)
            data_retention = st.selectbox("Data Retention", ["30 days", "90 days", "1 year", "3 years", "7 years"])
        
        st.markdown("---")
        
        # Calculated metrics
        st.markdown("### 📊 Estimated Requirements")
        
        # Calculate metrics
        total_requests_per_hour = expected_users * requests_per_user
        peak_requests_per_hour = total_requests_per_hour * peak_multiplier
        requests_per_second = peak_requests_per_hour / 3600
        bandwidth_mbps = (requests_per_second * avg_request_size) / 1024
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Requests/Second (Peak)",
                f"{requests_per_second:,.0f}",
                help="Peak requests per second during high load"
            )
        
        with col2:
            st.metric(
                "Required Bandwidth",
                f"{bandwidth_mbps:.1f} Mbps",
                help="Network bandwidth required for peak load"
            )
        
        with col3:
            storage_per_day_gb = (total_requests_per_hour * 24 * avg_request_size) / (1024 * 1024)
            st.metric(
                "Storage/Day",
                f"{storage_per_day_gb:.1f} GB",
                help="Daily storage requirements"
            )
        
        with col4:
            compute_units = int(requests_per_second / 100)  # Assuming 100 RPS per unit
            st.metric(
                "Compute Units",
                f"{compute_units}",
                help="Estimated compute instances needed"
            )
        
        st.markdown("---")
        
        # Resource recommendations
        st.markdown("### 💡 Resource Recommendations")
        
        rec_col1, rec_col2 = st.columns(2)
        
        with rec_col1:
            st.markdown("**Compute Resources**")
            st.info(f"""
            - **Application Servers:** {compute_units} x c5.xlarge instances
            - **Auto-scaling:** Min: {compute_units}, Max: {compute_units * 3}
            - **Load Balancers:** 2 x Application Load Balancer
            - **CPU Target:** 70% average utilization
            - **Memory:** 8GB per instance
            """)
            
            st.markdown("**Storage Resources**")
            st.info(f"""
            - **Database:** RDS db.r5.xlarge (Multi-AZ)
            - **Database Storage:** {storage_per_day_gb * 90:.0f} GB (90-day retention)
            - **S3 Storage:** {storage_per_day_gb * 365:.0f} GB/year
            - **EBS Volumes:** {compute_units * 100} GB (gp3)
            """)
        
        with rec_col2:
            st.markdown("**Network Resources**")
            st.info(f"""
            - **Bandwidth:** {bandwidth_mbps * 1.3:.1f} Mbps (with 30% buffer)
            - **CloudFront:** Enabled with edge caching
            - **VPC:** /20 subnet (4096 IPs)
            - **NAT Gateway:** 2 (Multi-AZ)
            """)
            
            st.markdown("**Caching Resources**")
            st.info("""
            - **ElastiCache:** cache.r5.large (Redis cluster)
            - **Cache Hit Ratio:** Target 80%+
            - **CloudFront Cache:** 24-hour TTL
            - **CDN:** Multi-region distribution
            """)
        
        st.markdown("---")
        
        # Performance projections
        st.markdown("### 📈 Performance Projections")
        
        months = ['Current', 'Month 3', 'Month 6', 'Month 9', 'Month 12']
        growth_factor = [1, 1 + (growth_rate/400), 1 + (growth_rate/200), 1 + (growth_rate*3/400), 1 + (growth_rate/100)]
        
        projection_data = {
            'Month': months,
            'Users': [int(expected_users * gf) for gf in growth_factor],
            'RPS': [int(requests_per_second * gf) for gf in growth_factor],
            'Storage (GB)': [int(storage_per_day_gb * 90 * gf) for gf in growth_factor],
            'Compute Units': [int(compute_units * gf) for gf in growth_factor]
        }
        
        df_projection = pd.DataFrame(projection_data)
        st.dataframe(df_projection, use_container_width=True, hide_index=True)
        
        # Growth chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_projection['Month'],
            y=df_projection['Users'],
            name='Concurrent Users',
            mode='lines+markers',
            line=dict(color='blue', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=df_projection['Month'],
            y=df_projection['Compute Units'],
            name='Compute Units',
            mode='lines+markers',
            line=dict(color='green', width=2),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title='Growth Projection (12 Months)',
            xaxis_title='Timeline',
            yaxis_title='Concurrent Users',
            yaxis2=dict(
                title='Compute Units',
                overlaying='y',
                side='right'
            ),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Cost projection
        st.markdown("### 💰 Cost Projection")
        
        base_cost = compute_units * 150  # $150 per compute unit
        storage_cost = (storage_per_day_gb * 90 * 0.10)  # $0.10 per GB
        network_cost = bandwidth_mbps * 50  # $50 per Mbps
        
        total_monthly_cost = base_cost + storage_cost + network_cost
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Current Monthly Cost", f"${total_monthly_cost:,.0f}")
        with col2:
            st.metric("12-Month Cost", f"${total_monthly_cost * (1 + growth_rate/100):,.0f}")
        with col3:
            st.metric("Annual Total", f"${total_monthly_cost * 12:,.0f}")
        
        # Export recommendations
        st.markdown("---")
        
        if st.button("📥 Export Capacity Plan", type="primary"):
            st.success("Capacity plan exported successfully!")
            st.info("""
            **Exported Documents:**
            - Capacity Planning Report (PDF)
            - Resource Recommendations (Excel)
            - Performance Projections (CSV)
            - Cost Analysis (Excel)
            """)

    @staticmethod
    def render_quota_management():
        """Resource Quota & Limit Management"""
        
        st.markdown("## 📊 Resource Quota & Limit Management")
        st.markdown("Monitor and manage AWS service quotas and resource limits")
        
        # Mode indicator
        if st.session_state.demo_mode:
            st.info("📋 Demo Mode: Viewing sample quota data")
        else:
            st.warning("🟢 Live Mode: Real quota monitoring")
        
        st.markdown("---")
        
        # Quota overview
        st.markdown("### 📈 Quota Usage Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Quotas", "156")
        with col2:
            st.metric("Near Limit (>80%)", "12", "⚠️")
        with col3:
            st.metric("At Limit (>95%)", "3", "🔴")
        with col4:
            st.metric("Requests Pending", "5")
        
        st.markdown("---")
        
        # Critical quotas
        st.markdown("### 🔴 Critical Quota Alerts")
        
        critical_quotas = [
            {
                'service': 'EC2',
                'quota': 'Running On-Demand Instances (c5.xlarge)',
                'current': 95,
                'limit': 100,
                'usage_pct': 95,
                'recommendation': 'Request increase to 200'
            },
            {
                'service': 'VPC',
                'quota': 'VPCs per Region',
                'current': 48,
                'limit': 50,
                'usage_pct': 96,
                'recommendation': 'Clean up unused VPCs or request increase'
            },
            {
                'service': 'RDS',
                'quota': 'DB Instances',
                'current': 38,
                'limit': 40,
                'usage_pct': 95,
                'recommendation': 'Request increase to 60'
            }
        ]
        
        for quota in critical_quotas:
            with st.expander(f"🔴 {quota['service']} - {quota['quota']} ({quota['usage_pct']}%)", expanded=True):
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    st.markdown(f"**Current Usage:** {quota['current']} / {quota['limit']}")
                    st.progress(quota['usage_pct'] / 100)
                
                with col2:
                    st.markdown(f"**Status:** {'🔴 Critical' if quota['usage_pct'] >= 95 else '⚠️ Warning'}")
                    st.markdown(f"**Recommendation:** {quota['recommendation']}")
                
                with col3:
                    if st.button("📝 Request Increase", key=f"request_{quota['service']}_{quota['quota']}"):
                        st.success("Quota increase requested!")
        
        st.markdown("---")
        
        # Warning quotas
        st.markdown("### ⚠️ Warning: High Usage Quotas (80-95%)")
        
        warning_quotas = [
            {'service': 'Lambda', 'quota': 'Concurrent Executions', 'current': 850, 'limit': 1000, 'usage_pct': 85},
            {'service': 'S3', 'quota': 'Buckets per Account', 'current': 82, 'limit': 100, 'usage_pct': 82},
            {'service': 'EBS', 'quota': 'Volume Storage (GB)', 'current': 85000, 'limit': 100000, 'usage_pct': 85},
            {'service': 'Route53', 'quota': 'Hosted Zones', 'current': 410, 'limit': 500, 'usage_pct': 82},
        ]
        
        df_warnings = pd.DataFrame(warning_quotas)
        st.dataframe(df_warnings, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Service quota details
        st.markdown("### 📋 Detailed Quota Status by Service")
        
        service_filter = st.selectbox(
            "Filter by Service",
            ["All Services", "EC2", "VPC", "RDS", "Lambda", "S3", "ELB", "CloudFormation", "IAM"]
        )
        
        all_quotas = [
            {'Service': 'EC2', 'Quota Name': 'Running On-Demand Instances', 'Current': 95, 'Limit': 100, 'Usage': '95%', 'Status': '🔴'},
            {'Service': 'EC2', 'Quota Name': 'EBS Volumes', 'Current': 450, 'Limit': 5000, 'Usage': '9%', 'Status': '🟢'},
            {'Service': 'VPC', 'Quota Name': 'VPCs per Region', 'Current': 48, 'Limit': 50, 'Usage': '96%', 'Status': '🔴'},
            {'Service': 'VPC', 'Quota Name': 'Subnets per VPC', 'Current': 145, 'Limit': 200, 'Usage': '73%', 'Status': '🟢'},
            {'Service': 'RDS', 'Quota Name': 'DB Instances', 'Current': 38, 'Limit': 40, 'Usage': '95%', 'Status': '🔴'},
            {'Service': 'RDS', 'Quota Name': 'Storage (GB)', 'Current': 15000, 'Limit': 100000, 'Usage': '15%', 'Status': '🟢'},
            {'Service': 'Lambda', 'Quota Name': 'Concurrent Executions', 'Current': 850, 'Limit': 1000, 'Usage': '85%', 'Status': '⚠️'},
            {'Service': 'S3', 'Quota Name': 'Buckets', 'Current': 82, 'Limit': 100, 'Usage': '82%', 'Status': '⚠️'},
            {'Service': 'ELB', 'Quota Name': 'Application Load Balancers', 'Current': 15, 'Limit': 50, 'Usage': '30%', 'Status': '🟢'},
            {'Service': 'IAM', 'Quota Name': 'Users', 'Current': 3500, 'Limit': 5000, 'Usage': '70%', 'Status': '🟢'},
        ]
        
        df_all_quotas = pd.DataFrame(all_quotas)
        
        if service_filter != "All Services":
            df_filtered = df_all_quotas[df_all_quotas['Service'] == service_filter]
        else:
            df_filtered = df_all_quotas
        
        st.dataframe(df_filtered, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Quota increase history
        st.markdown("### 📜 Recent Quota Increase Requests")
        
        request_history = [
            {'Date': '2024-11-15', 'Service': 'EC2', 'Quota': 'Spot Instance Requests', 'Requested': '200', 'Current': '100', 'Status': 'Approved', 'Approved Date': '2024-11-16'},
            {'Date': '2024-11-10', 'Service': 'Lambda', 'Quota': 'Concurrent Executions', 'Requested': '1500', 'Current': '1000', 'Status': 'Pending', 'Approved Date': '-'},
            {'Date': '2024-11-05', 'Service': 'RDS', 'Quota': 'DB Instances', 'Requested': '60', 'Current': '40', 'Status': 'Pending', 'Approved Date': '-'},
            {'Date': '2024-11-01', 'Service': 'VPC', 'Quota': 'VPCs per Region', 'Requested': '100', 'Current': '50', 'Status': 'Approved', 'Approved Date': '2024-11-03'},
        ]
        
        df_history = pd.DataFrame(request_history)
        st.dataframe(df_history, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Request new quota increase
        st.markdown("### 📝 Request Quota Increase")
        
        with st.form("quota_request"):
            col1, col2 = st.columns(2)
            
            with col1:
                request_service = st.selectbox(
                    "Service",
                    ["EC2", "VPC", "RDS", "Lambda", "S3", "ELB", "CloudFormation", "IAM", "DynamoDB"]
                )
                
                quota_name = st.text_input("Quota Name", placeholder="e.g., Running On-Demand Instances")
            
            with col2:
                current_limit = st.number_input("Current Limit", min_value=0, value=100)
                requested_limit = st.number_input("Requested Limit", min_value=0, value=200)
            
            justification = st.text_area(
                "Business Justification",
                placeholder="Explain why you need this quota increase...",
                height=100
            )
            
            use_case = st.text_area(
                "Use Case Description",
                placeholder="Describe your use case and expected growth...",
                height=100
            )
            
            submitted = st.form_submit_button("📤 Submit Request", type="primary")
            
            if submitted:
                if quota_name and justification and use_case:
                    st.success(f"""
                    ✅ **Quota Increase Request Submitted**
                    
                    - Service: {request_service}
                    - Quota: {quota_name}
                    - Current: {current_limit}
                    - Requested: {requested_limit}
                    - Increase: {requested_limit - current_limit} ({((requested_limit - current_limit) / current_limit * 100):.0f}%)
                    
                    Your request has been submitted to AWS Support.
                    Typical processing time: 1-3 business days.
                    
                    Ticket ID: SR-20241118-XXXXX
                    """)
                else:
                    st.error("❌ Please fill in all required fields")
        
        st.markdown("---")
        
        # Proactive monitoring
        st.markdown("### 🔔 Proactive Quota Monitoring")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Alert Thresholds**")
            warning_threshold = st.slider("Warning Threshold", min_value=50, max_value=90, value=80, step=5)
            critical_threshold = st.slider("Critical Threshold", min_value=80, max_value=100, value=95, step=5)
            
            if st.button("💾 Save Alert Settings"):
                st.success("Alert thresholds updated!")
        
        with col2:
            st.markdown("**Notification Settings**")
            notify_email = st.checkbox("Email Notifications", value=True)
            notify_slack = st.checkbox("Slack Notifications", value=True)
            notify_sns = st.checkbox("SNS Topic", value=False)
            
            if notify_email:
                email_address = st.text_input("Email Address", value="cloud-ops@company.com")
            
            if st.button("💾 Save Notification Settings"):
                st.success("Notification settings updated!")