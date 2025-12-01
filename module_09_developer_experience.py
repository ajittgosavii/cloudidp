"""
Module 09: Developer Experience
Beautiful self-service portal with interactive tools and automation
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

class DeveloperExperienceModule:
    """Developer Experience & Productivity Module - Enhanced UI"""
    
    def __init__(self):
        self.module_name = "Developer Experience"
        self.version = "2.0.0"
    
    def render(self):
        """Main render method with beautiful interface"""
        st.header("💻 Developer Experience Platform")
        
        # Mode indicator
        mode_color = "#28a745" if st.session_state.get('mode', 'Demo') == 'Live' else "#ffc107"
        mode_text = "🟢 Live Mode" if st.session_state.get('mode', 'Demo') == 'Live' else "📊 Demo Mode"
        st.markdown(f'<div style="background-color: {mode_color}; color: white; padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 20px;"><b>{mode_text}</b></div>', unsafe_allow_html=True)
        
        st.markdown("**🚀 Self-Service Portal | Infrastructure Automation | Developer Tools**")
        
        # Beautiful metrics dashboard
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("👨‍💻 Active Developers", "45", "+5", help="Developers active this week")
        with col2:
            st.metric("🚀 Deployments Today", "28", "+3", help="Successful deployments")
        with col3:
            st.metric("⚡ Avg Build Time", "3.2 min", "-0.5 min", help="Average CI/CD build time")
        with col4:
            st.metric("✅ Success Rate", "97%", "+2%", help="Deployment success rate")
        with col5:
            st.metric("🌍 Environments", "156", "+12", help="Active environments")
        
        st.markdown("---")
        
        # Main tabs with rich content
        tabs = st.tabs([
            "🛠️ Self-Service Portal",
            "📦 Template Gallery",
            "🚀 CI/CD Pipelines",
            "🧪 Test Environments",
            "📊 Developer Metrics"
        ])
        
        with tabs[0]:
            self.self_service_portal()
        with tabs[1]:
            self.template_gallery()
        with tabs[2]:
            self.cicd_dashboard()
        with tabs[3]:
            self.environment_manager()
        with tabs[4]:
            self.developer_metrics()
    
    def self_service_portal(self):
        """Beautiful self-service portal with interactive forms"""
        st.subheader("🛠️ Self-Service Developer Portal")
        st.markdown("**Provision infrastructure resources in seconds without waiting for approvals**")
        
        # Quick actions in columns
        st.markdown("### 🚀 Quick Actions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            with st.container():
                st.markdown("""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            padding: 20px; border-radius: 10px; color: white; margin-bottom: 10px;">
                    <h3 style="margin: 0; color: white;">🌐 Create Environment</h3>
                    <p style="margin: 10px 0 0 0; opacity: 0.9;">Deploy a new environment instantly</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("🚀 Create New Environment", use_container_width=True, type="primary"):
                    st.session_state['show_env_form'] = True
        
        with col2:
            with st.container():
                st.markdown("""
                <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                            padding: 20px; border-radius: 10px; color: white; margin-bottom: 10px;">
                    <h3 style="margin: 0; color: white;">📦 Deploy Application</h3>
                    <p style="margin: 10px 0 0 0; opacity: 0.9;">Deploy from template or custom config</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("🚀 Deploy Application", use_container_width=True, type="primary"):
                    st.session_state['show_deploy_form'] = True
        
        with col3:
            with st.container():
                st.markdown("""
                <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                            padding: 20px; border-radius: 10px; color: white; margin-bottom: 10px;">
                    <h3 style="margin: 0; color: white;">🗄️ Request Database</h3>
                    <p style="margin: 10px 0 0 0; opacity: 0.9;">Provision RDS, DynamoDB, or Aurora</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("🗄️ Request Database", use_container_width=True, type="primary"):
                    st.session_state['show_db_form'] = True
        
        st.markdown("---")
        
        # Show forms based on button clicks
        if st.session_state.get('show_env_form', False):
            self.render_environment_form()
        
        if st.session_state.get('show_deploy_form', False):
            self.render_deployment_form()
        
        if st.session_state.get('show_db_form', False):
            self.render_database_form()
        
        # Recent requests
        st.markdown("### 📋 Recent Requests")
        requests_data = pd.DataFrame([
            {"Request ID": "REQ-2024-001", "Type": "Environment", "Resource": "dev-api-backend", "Status": "✅ Completed", "Time": "2 mins ago", "Owner": "john.doe"},
            {"Request ID": "REQ-2024-002", "Type": "Database", "Resource": "postgres-staging", "Status": "🔄 In Progress", "Time": "5 mins ago", "Owner": "jane.smith"},
            {"Request ID": "REQ-2024-003", "Type": "Application", "Resource": "web-app-prod", "Status": "✅ Completed", "Time": "15 mins ago", "Owner": "bob.jones"},
            {"Request ID": "REQ-2024-004", "Type": "Cache", "Resource": "redis-cache", "Status": "✅ Completed", "Time": "1 hour ago", "Owner": "alice.wong"}
        ])
        st.dataframe(requests_data, use_container_width=True, hide_index=True)
    
    def render_environment_form(self):
        """Interactive form to create a new environment"""
        st.markdown("### 🌐 Create New Environment")
        
        with st.form("create_environment"):
            col1, col2 = st.columns(2)
            
            with col1:
                env_name = st.text_input("Environment Name", placeholder="e.g., dev-myapp-api")
                env_type = st.selectbox("Environment Type", ["Development", "Staging", "Testing", "Production"])
                template = st.selectbox("Template", ["Web Application", "API Backend", "Microservice", "Static Website", "Custom"])
            
            with col2:
                region = st.selectbox("AWS Region", ["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1"])
                instance_type = st.selectbox("Instance Type", ["t3.micro", "t3.small", "t3.medium", "t3.large"])
                auto_delete = st.checkbox("Auto-delete after 7 days", value=True)
            
            tags = st.text_area("Tags (key=value, one per line)", placeholder="Project=MyApp\nOwner=john.doe")
            
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                if st.form_submit_button("🚀 Create Environment", type="primary", use_container_width=True):
                    with st.spinner("Creating environment..."):
                        st.success(f"✅ Environment '{env_name}' created successfully!")
                        st.balloons()
                        st.session_state['show_env_form'] = False
                        st.rerun()
            
            with col2:
                if st.form_submit_button("❌ Cancel", use_container_width=True):
                    st.session_state['show_env_form'] = False
                    st.rerun()
    
    def render_deployment_form(self):
        """Interactive form to deploy an application"""
        st.markdown("### 📦 Deploy Application")
        
        with st.form("deploy_application"):
            col1, col2 = st.columns(2)
            
            with col1:
                app_name = st.text_input("Application Name", placeholder="e.g., web-app-v2")
                deploy_type = st.selectbox("Deployment Type", ["Docker Container", "Lambda Function", "EC2 Instance", "EKS Pod"])
                source = st.selectbox("Source", ["GitHub", "GitLab", "S3 Bucket", "Container Registry"])
            
            with col2:
                environment = st.selectbox("Target Environment", ["dev-environment-1", "staging-environment-2", "prod-environment-1"])
                replicas = st.number_input("Number of Replicas", min_value=1, max_value=10, value=2)
                health_check = st.checkbox("Enable Health Checks", value=True)
            
            repo_url = st.text_input("Repository/Source URL", placeholder="https://github.com/user/repo")
            
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                if st.form_submit_button("🚀 Deploy Now", type="primary", use_container_width=True):
                    with st.spinner("Deploying application..."):
                        st.success(f"✅ Application '{app_name}' deployed successfully!")
                        st.balloons()
                        st.session_state['show_deploy_form'] = False
                        st.rerun()
            
            with col2:
                if st.form_submit_button("❌ Cancel", use_container_width=True):
                    st.session_state['show_deploy_form'] = False
                    st.rerun()
    
    def render_database_form(self):
        """Interactive form to request a database"""
        st.markdown("### 🗄️ Request Database")
        
        with st.form("request_database"):
            col1, col2 = st.columns(2)
            
            with col1:
                db_name = st.text_input("Database Name", placeholder="e.g., myapp-production-db")
                db_engine = st.selectbox("Database Engine", ["PostgreSQL", "MySQL", "Aurora PostgreSQL", "Aurora MySQL", "DynamoDB"])
                db_version = st.selectbox("Version", ["14.5", "13.8", "12.11"] if db_engine == "PostgreSQL" else ["8.0", "5.7"])
            
            with col2:
                instance_class = st.selectbox("Instance Class", ["db.t3.micro", "db.t3.small", "db.t3.medium", "db.r5.large"])
                storage = st.number_input("Storage (GB)", min_value=20, max_value=1000, value=100)
                multi_az = st.checkbox("Multi-AZ Deployment", value=False)
            
            backup_retention = st.slider("Backup Retention (days)", min_value=1, max_value=35, value=7)
            
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                if st.form_submit_button("🗄️ Create Database", type="primary", use_container_width=True):
                    with st.spinner("Creating database..."):
                        st.success(f"✅ Database '{db_name}' creation initiated!")
                        st.info("📧 You'll receive connection details via email once ready (typically 10-15 minutes)")
                        st.session_state['show_db_form'] = False
                        st.rerun()
            
            with col2:
                if st.form_submit_button("❌ Cancel", use_container_width=True):
                    st.session_state['show_db_form'] = False
                    st.rerun()
    
    def template_gallery(self):
        """Beautiful template gallery with cards"""
        st.subheader("📦 Infrastructure as Code Template Gallery")
        st.markdown("**Pre-built, production-ready templates that follow best practices**")
        
        # Filter options
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            search = st.text_input("🔍 Search templates", placeholder="Search by name or technology...")
        with col2:
            category = st.selectbox("Category", ["All", "Web Applications", "Microservices", "Data & Analytics", "Machine Learning", "Networking"])
        with col3:
            sort_by = st.selectbox("Sort by", ["Popular", "Recent", "Name"])
        
        st.markdown("---")
        
        # Template cards in grid
        templates = [
            {
                "name": "Three-Tier Web Application",
                "icon": "🌐",
                "category": "Web Applications",
                "description": "Complete web app with ALB, EC2 auto-scaling, and RDS database",
                "language": "Terraform",
                "stars": 245,
                "uses": "1.2k",
                "color": "#667eea"
            },
            {
                "name": "Serverless API Backend",
                "icon": "⚡",
                "category": "Microservices",
                "description": "API Gateway, Lambda functions, and DynamoDB with CloudWatch monitoring",
                "language": "CloudFormation",
                "stars": 189,
                "uses": "856",
                "color": "#f093fb"
            },
            {
                "name": "Container Microservice",
                "icon": "🐳",
                "category": "Microservices",
                "description": "ECS Fargate with ALB, auto-scaling, and service discovery",
                "language": "Terraform",
                "stars": 167,
                "uses": "734",
                "color": "#4facfe"
            },
            {
                "name": "Data Lake Pipeline",
                "icon": "💾",
                "category": "Data & Analytics",
                "description": "S3, Glue, Athena setup for scalable data analytics",
                "language": "CloudFormation",
                "stars": 143,
                "uses": "521",
                "color": "#43e97b"
            },
            {
                "name": "ML Training Pipeline",
                "icon": "🤖",
                "category": "Machine Learning",
                "description": "SageMaker training pipeline with S3 data storage and model registry",
                "language": "Terraform",
                "stars": 98,
                "uses": "287",
                "color": "#fa709a"
            },
            {
                "name": "VPC with Subnets",
                "icon": "🌐",
                "category": "Networking",
                "description": "Multi-AZ VPC with public/private subnets, NAT gateways, and VPN",
                "language": "CloudFormation",
                "stars": 312,
                "uses": "2.1k",
                "color": "#30cfd0"
            }
        ]
        
        # Display templates in grid (3 per row)
        for i in range(0, len(templates), 3):
            cols = st.columns(3)
            for j, col in enumerate(cols):
                if i + j < len(templates):
                    template = templates[i + j]
                    with col:
                        self.render_template_card(template)
    
    def render_template_card(self, template):
        """Render a beautiful template card"""
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {template['color']} 0%, {template['color']}cc 100%); 
                    padding: 20px; border-radius: 10px; color: white; margin-bottom: 15px; min-height: 200px;">
            <div style="font-size: 3em; margin-bottom: 10px;">{template['icon']}</div>
            <h4 style="margin: 0; color: white;">{template['name']}</h4>
            <p style="margin: 10px 0; opacity: 0.9; font-size: 0.9em;">{template['description']}</p>
            <div style="margin-top: 15px;">
                <span style="background: rgba(255,255,255,0.3); padding: 3px 8px; border-radius: 3px; font-size: 0.8em; margin-right: 5px;">
                    {template['language']}
                </span>
                <span style="font-size: 0.85em;">⭐ {template['stars']} | 📦 {template['uses']} uses</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📖 View Details", key=f"view_{template['name']}", use_container_width=True):
                st.info(f"Viewing details for: {template['name']}")
        with col2:
            if st.button("🚀 Use Template", key=f"use_{template['name']}", use_container_width=True, type="primary"):
                st.success(f"✅ Template '{template['name']}' ready to deploy!")
    
    def cicd_dashboard(self):
        """Beautiful CI/CD pipeline dashboard"""
        st.subheader("🚀 CI/CD Pipeline Management")
        st.markdown("**Monitor and manage your continuous integration and deployment pipelines**")
        
        # Pipeline status overview
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Active Pipelines", "67", "+3")
        with col2:
            st.metric("Success Rate", "97.2%", "+1.1%")
        with col3:
            st.metric("Avg Build Time", "3.2 min", "-0.5 min", delta_color="inverse")
        with col4:
            st.metric("Failed Builds (24h)", "2", "-3", delta_color="inverse")
        
        st.markdown("---")
        
        # Recent pipeline runs
        st.markdown("### 🔄 Recent Pipeline Runs")
        
        pipelines = pd.DataFrame([
            {"Pipeline": "web-app-frontend", "Branch": "main", "Status": "✅ Success", "Duration": "2m 45s", "Triggered": "5 mins ago", "By": "john.doe"},
            {"Pipeline": "api-backend", "Branch": "develop", "Status": "🔄 Running", "Duration": "1m 23s", "Triggered": "Just now", "By": "jane.smith"},
            {"Pipeline": "data-pipeline", "Branch": "main", "Status": "✅ Success", "Duration": "4m 12s", "Triggered": "15 mins ago", "By": "bob.jones"},
            {"Pipeline": "ml-model-training", "Branch": "feature/v2", "Status": "❌ Failed", "Duration": "0m 34s", "Triggered": "23 mins ago", "By": "alice.wong"},
            {"Pipeline": "infrastructure-deploy", "Branch": "main", "Status": "✅ Success", "Duration": "5m 56s", "Triggered": "1 hour ago", "By": "charlie.brown"},
        ])
        
        st.dataframe(pipelines, use_container_width=True, hide_index=True)
        
        # Pipeline details
        st.markdown("---")
        st.markdown("### 📊 Pipeline Performance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Build Time Trend (Last 7 Days)")
            build_times = pd.DataFrame({
                'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                'Avg Build Time (min)': [4.2, 3.8, 3.5, 3.2, 3.4, 3.1, 3.2]
            })
            st.line_chart(build_times.set_index('Day'))
        
        with col2:
            st.markdown("#### Success Rate by Pipeline")
            success_data = pd.DataFrame({
                'Pipeline': ['Frontend', 'Backend', 'Data', 'ML', 'Infra'],
                'Success Rate': [99, 97, 95, 92, 98]
            })
            st.bar_chart(success_data.set_index('Pipeline'))
    
    def environment_manager(self):
        """Environment management interface"""
        st.subheader("🧪 Test Environment Manager")
        st.markdown("**Manage ephemeral test and staging environments**")
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Active Environments", "23", "+5")
        with col2:
            st.metric("Total Capacity", "50")
        with col3:
            st.metric("Cost (Monthly)", "$3,456", "-$234")
        with col4:
            st.metric("Avg Lifetime", "4.2 days")
        
        st.markdown("---")
        
        # Active environments
        st.markdown("### 🌍 Active Environments")
        
        environments = pd.DataFrame([
            {
                "Name": "dev-api-v2", 
                "Type": "Development", 
                "Owner": "john.doe", 
                "Status": "🟢 Running",
                "Created": "2 hours ago",
                "Auto-Delete": "In 6 hours",
                "Cost/Day": "$12.50"
            },
            {
                "Name": "staging-frontend", 
                "Type": "Staging", 
                "Owner": "jane.smith", 
                "Status": "🟢 Running",
                "Created": "1 day ago",
                "Auto-Delete": "In 6 days",
                "Cost/Day": "$45.00"
            },
            {
                "Name": "test-integration", 
                "Type": "Testing", 
                "Owner": "bob.jones", 
                "Status": "🟡 Starting",
                "Created": "5 mins ago",
                "Auto-Delete": "In 2 days",
                "Cost/Day": "$8.75"
            },
            {
                "Name": "perf-test-env", 
                "Type": "Performance", 
                "Owner": "alice.wong", 
                "Status": "🟢 Running",
                "Created": "3 days ago",
                "Auto-Delete": "In 4 days",
                "Cost/Day": "$89.00"
            },
        ])
        
        st.dataframe(environments, use_container_width=True, hide_index=True)
        
        # Environment actions
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("➕ Create Environment", use_container_width=True, type="primary"):
                st.info("Opening environment creation wizard...")
        with col2:
            if st.button("🔄 Refresh Status", use_container_width=True):
                st.success("Status refreshed!")
        with col3:
            if st.button("📊 View Costs", use_container_width=True):
                st.info("Opening cost breakdown...")
        with col4:
            if st.button("🗑️ Cleanup Expired", use_container_width=True):
                st.warning("Removing expired environments...")
    
    def developer_metrics(self):
        """Developer productivity metrics and insights"""
        st.subheader("📊 Developer Metrics & Insights")
        st.markdown("**Track developer productivity and platform adoption**")
        
        # KPIs
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Deploy Frequency", "4.2/day", "+0.8")
        with col2:
            st.metric("Lead Time", "2.3 hours", "-0.7h", delta_color="inverse")
        with col3:
            st.metric("MTTR", "18 min", "-5 min", delta_color="inverse")
        with col4:
            st.metric("Change Failure Rate", "3.2%", "-1.1%", delta_color="inverse")
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📈 Deployment Frequency (Last 30 Days)")
            dates = pd.date_range(end=datetime.now(), periods=30)
            deployments = pd.DataFrame({
                'Date': dates,
                'Deployments': [15, 18, 22, 19, 25, 28, 24, 26, 30, 28, 
                               32, 29, 27, 31, 33, 35, 32, 34, 36, 38,
                               35, 37, 40, 38, 36, 39, 41, 42, 40, 43]
            })
            st.line_chart(deployments.set_index('Date'))
        
        with col2:
            st.markdown("#### 🎯 Service Usage by Type")
            usage_data = pd.DataFrame({
                'Service': ['Environments', 'Deployments', 'Databases', 'Caches', 'Queues'],
                'Count': [234, 567, 89, 123, 45]
            })
            st.bar_chart(usage_data.set_index('Service'))
        
        st.markdown("---")
        
        # Top users
        st.markdown("### 👥 Top Platform Users (This Month)")
        top_users = pd.DataFrame([
            {"Developer": "john.doe", "Deployments": 89, "Environments": 23, "Requests": 145, "Score": "⭐⭐⭐⭐⭐"},
            {"Developer": "jane.smith", "Deployments": 76, "Environments": 19, "Requests": 128, "Score": "⭐⭐⭐⭐⭐"},
            {"Developer": "bob.jones", "Deployments": 64, "Environments": 15, "Requests": 98, "Score": "⭐⭐⭐⭐"},
            {"Developer": "alice.wong", "Deployments": 58, "Environments": 12, "Requests": 87, "Score": "⭐⭐⭐⭐"},
            {"Developer": "charlie.brown", "Deployments": 45, "Environments": 10, "Requests": 72, "Score": "⭐⭐⭐"},
        ])
        st.dataframe(top_users, use_container_width=True, hide_index=True)
