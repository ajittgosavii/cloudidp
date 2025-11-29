"""
Module 09: Developer Experience & Self-Service
Governed Self-Service Portals, GitOps Integration, Drift Notification, Documentation, InfraSecOps, User Community
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

class DeveloperExperienceModule:
    """Developer Experience & Self-Service Module"""
    def render(self):
        """Main render method - organizes all sub-features in tabs"""
        
        st.markdown("## Developerexperience")
        
        # Create tabs for each sub-feature
        tabs = st.tabs([
            "📋 Overview",
            "⚙️ Self Service Portals",
            "⚙️ Gitops Integration",
            "⚙️ Drift Notification",
            "⚙️ Documentation Examples",
            "⚙️ Infrasecops",
            "⚙️ User Community"
        ])
        
        with tabs[0]:
            self.render_overview()
        
        with tabs[1]:
            self.render_self_service_portals()
        
        with tabs[2]:
            self.render_gitops_integration()
        
        with tabs[3]:
            self.render_drift_notification()
        
        with tabs[4]:
            self.render_documentation_examples()
        
        with tabs[5]:
            self.render_infrasecops()
        
        with tabs[6]:
            self.render_user_community()


    
    def __init__(self):
        self.module_name = "Developer Experience & Self-Service"
    
    @staticmethod
    def render_overview():
        """Render Module 09 Overview"""
        st.markdown("## 👨‍💻 Module 09: Developer Experience & Self-Service")
        
        st.markdown("""
        Empower developers with self-service capabilities while maintaining governance and compliance.
        Streamline workflows through GitOps, automation, and comprehensive documentation.
        """)
        
        st.markdown("---")
        
        # Key Components
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🌐 Governed Self-Service Portals")
            st.markdown("Developer-friendly infrastructure provisioning")
            st.markdown("- Service catalog with pre-approved templates")
            st.markdown("- Role-based access control (RBAC)")
            st.markdown("- Automated approval workflows")
            st.markdown("- Resource quota management")
            st.markdown("- Cost estimation before deployment")
            
            st.markdown("#### 🔄 GitOps Integration")
            st.markdown("Git-based infrastructure automation")
            st.markdown("- Infrastructure as Code repository management")
            st.markdown("- Automated CI/CD pipelines")
            st.markdown("- Pull request reviews & approvals")
            st.markdown("- Environment synchronization")
            st.markdown("- Rollback capabilities")
            
            st.markdown("#### 🔔 Drift Notification & Feedback Loop")
            st.markdown("Real-time configuration monitoring")
            st.markdown("- Continuous drift detection")
            st.markdown("- Automated notifications (Slack, Email, Teams)")
            st.markdown("- Root cause analysis")
            st.markdown("- Auto-remediation options")
            st.markdown("- Drift history & trends")
        
        with col2:
            st.markdown("#### 📚 Documentation & Examples")
            st.markdown("Comprehensive developer resources")
            st.markdown("- Interactive API documentation")
            st.markdown("- IaC code examples & templates")
            st.markdown("- Architecture patterns library")
            st.markdown("- Troubleshooting guides")
            st.markdown("- Video tutorials & workshops")
            
            st.markdown("#### 🔒 InfraSecOps")
            st.markdown("Security integrated into development")
            st.markdown("- Security scanning in CI/CD")
            st.markdown("- Policy-as-code validation")
            st.markdown("- Secrets management (Vault, Secrets Manager)")
            st.markdown("- Vulnerability remediation tracking")
            st.markdown("- Compliance gates")
            
            st.markdown("#### 👥 User Community")
            st.markdown("Collaboration and knowledge sharing")
            st.markdown("- Internal forums & Q&A")
            st.markdown("- Best practices sharing")
            st.markdown("- Feature request tracking")
            st.markdown("- Usage analytics & insights")
            st.markdown("- Community-driven improvements")
        
        st.markdown("---")
        
        # Key Capabilities
        st.markdown("### 🎯 Key Capabilities")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Self-Service**")
            st.markdown("""
            - Pre-approved templates
            - Automated provisioning
            - Cost transparency
            - Quota management
            - Fast deployment
            """)
        
        with col2:
            st.markdown("**Automation**")
            st.markdown("""
            - GitOps workflows
            - CI/CD integration
            - Drift remediation
            - Policy enforcement
            - Continuous monitoring
            """)
        
        with col3:
            st.markdown("**Developer Focus**")
            st.markdown("""
            - Rich documentation
            - Community support
            - Training resources
            - Feedback loops
            - Continuous improvement
            """)
        
        st.markdown("---")
        
        # Metrics
        st.markdown("### 📊 Platform Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Active Developers", "847", "+156")
        with col2:
            st.metric("Self-Service Requests", "12.4K", "+2.3K")
        with col3:
            st.metric("Avg Deployment Time", "8 min", "-12 min")
        with col4:
            st.metric("Developer Satisfaction", "4.6/5", "+0.3")
    
    @staticmethod
    def render_self_service_portals():
        """Render Governed Self-Service Portals"""
        st.markdown("## 🌐 Governed Self-Service Portals")
        
        st.markdown("""
        Enable developers to provision infrastructure independently while maintaining organizational 
        governance, compliance, and cost controls.
        """)
        
        st.markdown("---")
        
        # Demo Mode Toggle Check
        demo_mode = st.session_state.get('demo_mode', True)
        
        # Service Catalog
        st.markdown("### 📦 Service Catalog")
        
        catalog_items = [
            {
                "service": "Web Application Stack",
                "type": "Application",
                "resources": "ALB, EC2 Auto Scaling, RDS, S3",
                "approval": "Auto-approved",
                "cost_estimate": "$450/month",
                "deployment_time": "12 minutes",
                "compliance": "✅ PCI DSS, SOC 2"
            },
            {
                "service": "Kubernetes Cluster",
                "type": "Container Platform",
                "resources": "EKS, VPC, NAT Gateway, Load Balancer",
                "approval": "Manager approval",
                "cost_estimate": "$850/month",
                "deployment_time": "18 minutes",
                "compliance": "✅ HIPAA, ISO 27001"
            },
            {
                "service": "Data Pipeline",
                "type": "Analytics",
                "resources": "Glue, S3, Redshift, Lambda",
                "approval": "Auto-approved",
                "cost_estimate": "$320/month",
                "deployment_time": "9 minutes",
                "compliance": "✅ GDPR, CCPA"
            },
            {
                "service": "Serverless API",
                "type": "API",
                "resources": "API Gateway, Lambda, DynamoDB",
                "approval": "Auto-approved",
                "cost_estimate": "$85/month",
                "deployment_time": "5 minutes",
                "compliance": "✅ All frameworks"
            },
            {
                "service": "ML Training Environment",
                "type": "Machine Learning",
                "resources": "SageMaker, S3, EC2 GPU instances",
                "approval": "Director approval",
                "cost_estimate": "$2,400/month",
                "deployment_time": "15 minutes",
                "compliance": "✅ SOC 2, ISO 27001"
            }
        ]
        
        df_catalog = pd.DataFrame(catalog_items)
        st.dataframe(df_catalog, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Request Provisioning
        st.markdown("### 🚀 Request New Service")
        
        col1, col2 = st.columns(2)
        
        with col1:
            service_type = st.selectbox(
                "Select Service Template:",
                ["Web Application Stack", "Kubernetes Cluster", "Data Pipeline", 
                 "Serverless API", "ML Training Environment"]
            )
            
            environment = st.selectbox(
                "Target Environment:",
                ["Development", "QA", "Staging", "Production"]
            )
            
            project_code = st.text_input(
                "Project Code:",
                placeholder="PRJ-2025-XXX"
            )
            
            cost_center = st.text_input(
                "Cost Center:",
                placeholder="CC-ENGINEERING-001"
            )
        
        with col2:
            region = st.selectbox(
                "AWS Region:",
                ["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1"]
            )
            
            instance_size = st.selectbox(
                "Instance Size:",
                ["Small (t3.small)", "Medium (t3.medium)", "Large (t3.large)", 
                 "X-Large (t3.xlarge)"]
            )
            
            high_availability = st.checkbox("Enable High Availability", value=True)
            
            auto_scaling = st.checkbox("Enable Auto-Scaling", value=True)
        
        st.markdown("---")
        
        # Cost Estimation
        st.markdown("### 💰 Cost Estimation")
        
        base_cost = 450 if "Web" in service_type else 320
        if "Kubernetes" in service_type:
            base_cost = 850
        elif "ML" in service_type:
            base_cost = 2400
        elif "Serverless" in service_type:
            base_cost = 85
        
        # Adjustments
        size_multiplier = {"Small": 1.0, "Medium": 1.5, "Large": 2.0, "X-Large": 2.5}
        multiplier = size_multiplier.get(instance_size.split("(")[0].strip(), 1.0)
        ha_cost = base_cost * 0.3 if high_availability else 0
        
        total_monthly_cost = (base_cost * multiplier) + ha_cost
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Base Cost", f"${base_cost:.0f}/mo")
        with col2:
            st.metric("Size Adjustment", f"${(base_cost * multiplier - base_cost):.0f}/mo")
        with col3:
            st.metric("HA Cost", f"${ha_cost:.0f}/mo")
        with col4:
            st.metric("Total Estimated", f"${total_monthly_cost:.0f}/mo", 
                     help="Monthly cost estimate")
        
        st.markdown("---")
        
        # Governance Checks
        st.markdown("### ✅ Governance Validation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Automated Checks:**")
            st.success("✅ Tagging policy compliant")
            st.success("✅ Naming convention valid")
            st.success("✅ Security group rules approved")
            st.success("✅ Encryption enabled")
        
        with col2:
            st.markdown("**Quota Verification:**")
            st.info("✅ VPC quota available (85/100)")
            st.info("✅ EC2 instance quota available (42/100)")
            st.info("✅ S3 bucket quota available (156/500)")
            st.info("✅ Budget allocation confirmed")
        
        st.markdown("---")
        
        # Submit Request
        if st.button("🚀 Submit Provisioning Request", type="primary", use_container_width=True):
            with st.spinner("Validating request and initiating provisioning..."):
                import time
                time.sleep(2)
                st.success("✅ Request submitted successfully!")
                st.info(f"""
                **Request ID:** REQ-{datetime.now().strftime('%Y%m%d-%H%M%S')}
                
                **Status:** Approved (Auto-approved template)
                
                **Estimated Completion:** 12 minutes
                
                **Next Steps:**
                1. Infrastructure provisioning initiated
                2. Security configurations applied
                3. Monitoring enabled
                4. Notification sent to {project_code} team
                
                Track your request in the **Dashboard** section.
                """)
        
        st.markdown("---")
        
        # Recent Requests
        st.markdown("### 📋 Your Recent Requests")
        
        recent_requests = [
            {
                "request_id": "REQ-20250115-143022",
                "service": "Web Application Stack",
                "environment": "Development",
                "status": "✅ Completed",
                "submitted": "2 hours ago",
                "cost": "$450/mo"
            },
            {
                "request_id": "REQ-20250114-091534",
                "service": "Serverless API",
                "environment": "QA",
                "status": "🟢 Running",
                "submitted": "1 day ago",
                "cost": "$85/mo"
            },
            {
                "request_id": "REQ-20250112-165432",
                "service": "Data Pipeline",
                "environment": "Production",
                "status": "⏸️ Pending Approval",
                "submitted": "3 days ago",
                "cost": "$320/mo"
            }
        ]
        
        df_requests = pd.DataFrame(recent_requests)
        st.dataframe(df_requests, use_container_width=True, hide_index=True)
    
    @staticmethod
    def render_gitops_integration():
        """Render GitOps Integration"""
        st.markdown("## 🔄 GitOps Integration")
        
        st.markdown("""
        Implement Infrastructure as Code (IaC) workflows with Git as the single source of truth.
        Automate deployments, enable rollbacks, and maintain audit trails through Git history.
        """)
        
        st.markdown("---")
        
        # GitOps Architecture
        st.markdown("### 🏗️ GitOps Architecture")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Git Repository Structure:**")
            st.code("""
├── infrastructure/
│   ├── base/
│   │   ├── networking.tf
│   │   ├── security.tf
│   │   └── monitoring.tf
│   ├── environments/
│   │   ├── dev/
│   │   ├── qa/
│   │   ├── staging/
│   │   └── production/
│   └── modules/
│       ├── compute/
│       ├── database/
│       └── storage/
├── policies/
│   ├── security-policies/
│   ├── cost-policies/
│   └── compliance-policies/
└── workflows/
    ├── ci-cd/
    └── automation/
            """, language="text")
        
        with col2:
            st.markdown("**GitOps Workflow:**")
            st.markdown("""
            1. **Developer commits** IaC changes to Git
            2. **CI/CD pipeline triggers** automatically
            3. **Automated validation** runs:
               - Syntax checking
               - Security scanning
               - Policy validation
               - Cost estimation
            4. **Pull Request (PR)** created for review
            5. **Peer review** and approval process
            6. **Merge to main** branch
            7. **Automated deployment** to target environment
            8. **State verification** and drift detection
            9. **Notifications** sent to team
            """)
        
        st.markdown("---")
        
        # Repository Configuration
        st.markdown("### ⚙️ Repository Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            repo_url = st.text_input(
                "Git Repository URL:",
                value="https://github.com/org/infrastructure-platform.git",
                disabled=st.session_state.get('demo_mode', True)
            )
            
            branch_strategy = st.selectbox(
                "Branching Strategy:",
                ["GitFlow", "Trunk-Based", "GitHub Flow", "GitLab Flow"]
            )
            
            auto_sync = st.checkbox("Enable Auto-Sync", value=True,
                                   help="Automatically sync repo changes to infrastructure")
        
        with col2:
            sync_interval = st.selectbox(
                "Sync Interval:",
                ["Manual", "Every 5 minutes", "Every 15 minutes", 
                 "Every 30 minutes", "Every hour"]
            )
            
            deployment_strategy = st.selectbox(
                "Deployment Strategy:",
                ["Rolling Update", "Blue-Green", "Canary", "Recreate"]
            )
            
            auto_rollback = st.checkbox("Auto-Rollback on Failure", value=True)
        
        st.markdown("---")
        
        # CI/CD Pipeline Status
        st.markdown("### 🔄 CI/CD Pipeline Status")
        
        pipelines = [
            {
                "pipeline": "Infrastructure-Dev",
                "branch": "feature/add-eks-cluster",
                "status": "🟢 Running",
                "stage": "Security Scan",
                "progress": "60%",
                "duration": "3m 42s",
                "triggered_by": "john.doe@company.com"
            },
            {
                "pipeline": "Infrastructure-QA",
                "branch": "release/v2.3.0",
                "status": "✅ Success",
                "stage": "Completed",
                "progress": "100%",
                "duration": "8m 15s",
                "triggered_by": "jane.smith@company.com"
            },
            {
                "pipeline": "Infrastructure-Prod",
                "branch": "main",
                "status": "⏸️ Waiting Approval",
                "stage": "Manual Approval",
                "progress": "50%",
                "duration": "15m 30s",
                "triggered_by": "deploy-bot"
            },
            {
                "pipeline": "Infrastructure-Staging",
                "branch": "hotfix/security-patch",
                "status": "❌ Failed",
                "stage": "Policy Validation",
                "progress": "35%",
                "duration": "2m 18s",
                "triggered_by": "security-team@company.com"
            }
        ]
        
        df_pipelines = pd.DataFrame(pipelines)
        st.dataframe(df_pipelines, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Recent Deployments
        st.markdown("### 📦 Recent Deployments")
        
        deployments = [
            {
                "timestamp": "2025-01-15 14:32:00",
                "environment": "Production",
                "commit": "a3f45b2",
                "author": "jane.smith",
                "changes": "Added EKS cluster, updated security groups",
                "status": "✅ Deployed",
                "rollback": "Available"
            },
            {
                "timestamp": "2025-01-15 11:15:00",
                "environment": "Staging",
                "commit": "c7d92e1",
                "author": "john.doe",
                "changes": "Database migration, RDS parameter updates",
                "status": "✅ Deployed",
                "rollback": "Available"
            },
            {
                "timestamp": "2025-01-14 16:45:00",
                "environment": "QA",
                "commit": "f2a83c9",
                "author": "alice.wang",
                "changes": "Lambda function updates, API Gateway changes",
                "status": "✅ Deployed",
                "rollback": "Available"
            },
            {
                "timestamp": "2025-01-14 09:20:00",
                "environment": "Development",
                "commit": "b9e41d3",
                "author": "bob.chen",
                "changes": "S3 bucket policies, CloudFront distribution",
                "status": "⏮️ Rolled Back",
                "rollback": "N/A"
            }
        ]
        
        df_deployments = pd.DataFrame(deployments)
        st.dataframe(df_deployments, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Manual Deployment
        st.markdown("### 🚀 Manual Deployment Trigger")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            target_env = st.selectbox(
                "Target Environment:",
                ["Development", "QA", "Staging", "Production"]
            )
        
        with col2:
            git_branch = st.text_input(
                "Git Branch/Tag:",
                value="main"
            )
        
        with col3:
            deployment_type = st.selectbox(
                "Deployment Type:",
                ["Standard", "Blue-Green", "Canary"]
            )
        
        if st.button("🚀 Trigger Deployment", type="primary"):
            with st.spinner(f"Deploying to {target_env}..."):
                import time
                time.sleep(2)
                st.success(f"✅ Deployment to {target_env} initiated successfully!")
                st.info(f"""
                **Deployment ID:** DEP-{datetime.now().strftime('%Y%m%d-%H%M%S')}
                
                **Branch:** {git_branch}
                **Type:** {deployment_type}
                **Estimated Time:** 8-12 minutes
                
                Track progress in CI/CD Pipeline Status above.
                """)
        
        st.markdown("---")
        
        # GitOps Metrics
        st.markdown("### 📊 GitOps Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Deployments Today", "18", "+6")
        with col2:
            st.metric("Success Rate", "96.4%", "+2.1%")
        with col3:
            st.metric("Avg Deploy Time", "7.2 min", "-1.8 min")
        with col4:
            st.metric("Rollbacks (24h)", "1", "-2")
    
    @staticmethod
    def render_drift_notification():
        """Render Drift Notification & Feedback Loop"""
        st.markdown("## 🔔 Drift Notification & Feedback Loop")
        
        st.markdown("""
        Detect, notify, and remediate infrastructure drift in real-time. Maintain alignment 
        between declared state (IaC) and actual infrastructure state.
        """)
        
        st.markdown("---")
        
        # Drift Detection Overview
        st.markdown("### 📊 Drift Detection Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Resources Monitored", "2,847", "+124")
        with col2:
            st.metric("Drifts Detected (24h)", "23", "+8")
        with col3:
            st.metric("Auto-Remediated", "18", "+5")
        with col4:
            st.metric("Manual Review Needed", "5", "+3")
        
        st.markdown("---")
        
        # Active Drift Alerts
        st.markdown("### ⚠️ Active Drift Alerts")
        
        drift_alerts = [
            {
                "severity": "🔴 Critical",
                "resource": "sg-0a3b5c7d9e (SecurityGroup)",
                "account": "Production-US-East",
                "drift_type": "Ingress rule added manually",
                "detected": "15 minutes ago",
                "status": "Pending Review",
                "action": "Notify + Block"
            },
            {
                "severity": "🟠 High",
                "resource": "i-0f8e7d6c5b4a (EC2)",
                "account": "Production-EU-West",
                "drift_type": "Instance type changed",
                "detected": "1 hour ago",
                "status": "Auto-Remediation Failed",
                "action": "Manual Intervention"
            },
            {
                "severity": "🟡 Medium",
                "resource": "db-prod-mysql-01 (RDS)",
                "account": "Production-US-West",
                "drift_type": "Parameter group modified",
                "detected": "2 hours ago",
                "status": "Awaiting Approval",
                "action": "Review + Approve"
            },
            {
                "severity": "🟢 Low",
                "resource": "bucket-logs-2025 (S3)",
                "account": "Logging-US-East",
                "drift_type": "Lifecycle policy updated",
                "detected": "4 hours ago",
                "status": "Auto-Remediated",
                "action": "Completed"
            },
            {
                "severity": "🟠 High",
                "resource": "lambda-api-handler (Lambda)",
                "account": "Development-AP-SE",
                "drift_type": "Environment variables changed",
                "detected": "6 hours ago",
                "status": "Investigating",
                "action": "In Progress"
            }
        ]
        
        df_drift_alerts = pd.DataFrame(drift_alerts)
        st.dataframe(df_drift_alerts, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Drift Details
        st.markdown("### 🔍 Drift Detail View")
        
        selected_drift = st.selectbox(
            "Select Drift Alert to View:",
            ["sg-0a3b5c7d9e (SecurityGroup) - Critical",
             "i-0f8e7d6c5b4a (EC2) - High",
             "db-prod-mysql-01 (RDS) - Medium"]
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Expected State (IaC):**")
            st.code("""
# Security Group Configuration
resource "aws_security_group" "web" {
  name        = "web-sg"
  description = "Web tier security group"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/8"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
            """, language="hcl")
        
        with col2:
            st.markdown("**Actual State (AWS):**")
            st.code("""
# Security Group Configuration
resource "aws_security_group" "web" {
  name        = "web-sg"
  description = "Web tier security group"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/8"]
  }

  # ⚠️ DRIFT: Manually added rule
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # ❌ Public SSH
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
            """, language="hcl")
        
        st.markdown("---")
        
        # Drift Analysis
        st.markdown("### 🔬 Drift Analysis")
        
        st.error("**Security Risk Identified:**")
        st.markdown("""
        - ❌ **Unauthorized SSH access** from Internet (0.0.0.0/0)
        - ⚠️ **Violates security policy** SEC-POL-001
        - 🔴 **Compliance impact**: PCI DSS, SOC 2
        - 👤 **Changed by**: john.doe@company.com (Manual console change)
        - ⏰ **Changed at**: 2025-01-15 14:15:32 UTC
        """)
        
        st.markdown("---")
        
        # Remediation Options
        st.markdown("### 🛠️ Remediation Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Auto-Remediate", type="primary", use_container_width=True):
                with st.spinner("Remediating drift..."):
                    import time
                    time.sleep(2)
                    st.success("✅ Drift remediated successfully!")
                    st.info("Security group reverted to IaC-defined state.")
        
        with col2:
            if st.button("✅ Accept Change", use_container_width=True):
                st.warning("⚠️ This will update IaC to match actual state.")
                st.info("Requires approval from Security Team.")
        
        with col3:
            if st.button("📝 Create Ticket", use_container_width=True):
                st.info("Ticket created: JIRA-SEC-1234")
                st.success("Assigned to: Security Operations Team")
        
        st.markdown("---")
        
        # Notification Configuration
        st.markdown("### 📢 Notification Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Notification Channels:**")
            notify_slack = st.checkbox("Slack (#infrastructure-alerts)", value=True)
            notify_email = st.checkbox("Email (ops-team@company.com)", value=True)
            notify_teams = st.checkbox("Microsoft Teams", value=False)
            notify_pagerduty = st.checkbox("PagerDuty (Critical only)", value=True)
        
        with col2:
            st.markdown("**Severity Thresholds:**")
            critical_notify = st.checkbox("Critical - Immediate notification", value=True)
            high_notify = st.checkbox("High - Within 15 minutes", value=True)
            medium_notify = st.checkbox("Medium - Within 1 hour", value=True)
            low_notify = st.checkbox("Low - Daily digest", value=False)
        
        if st.button("💾 Save Notification Settings", use_container_width=True):
            st.success("✅ Notification settings saved successfully!")
        
        st.markdown("---")
        
        # Drift Trends
        st.markdown("### 📈 Drift Trends")
        
        trend_data = pd.DataFrame({
            'Date': pd.date_range(start='2025-01-08', end='2025-01-15', freq='D'),
            'Critical': [2, 1, 3, 2, 4, 1, 5, 3],
            'High': [5, 7, 6, 8, 7, 9, 6, 10],
            'Medium': [12, 15, 14, 11, 13, 16, 14, 12],
            'Low': [8, 10, 9, 11, 10, 12, 11, 9]
        })
        
        st.line_chart(trend_data.set_index('Date'))
        
        st.markdown("---")
        
        # Drift History
        st.markdown("### 📜 Drift History (Last 7 Days)")
        
        history = [
            {
                "timestamp": "2025-01-15 14:15:32",
                "resource": "sg-0a3b5c7d9e",
                "type": "SecurityGroup ingress rule",
                "action": "Pending Review",
                "remediation": "Not yet remediated"
            },
            {
                "timestamp": "2025-01-15 10:42:18",
                "resource": "i-0f8e7d6c5b4a",
                "type": "EC2 instance type change",
                "action": "Auto-remediation failed",
                "remediation": "Manual intervention required"
            },
            {
                "timestamp": "2025-01-14 16:30:45",
                "resource": "db-prod-mysql-01",
                "type": "RDS parameter group",
                "action": "Awaiting approval",
                "remediation": "Under review"
            },
            {
                "timestamp": "2025-01-14 11:20:12",
                "resource": "bucket-logs-2025",
                "type": "S3 lifecycle policy",
                "action": "Auto-remediated",
                "remediation": "✅ Completed"
            },
            {
                "timestamp": "2025-01-13 09:15:33",
                "resource": "lambda-api-handler",
                "type": "Lambda env variables",
                "action": "Auto-remediated",
                "remediation": "✅ Completed"
            }
        ]
        
        df_history = pd.DataFrame(history)
        st.dataframe(df_history, use_container_width=True, hide_index=True)
    
    @staticmethod
    def render_documentation_examples():
        """Render Documentation & Examples"""
        st.markdown("## 📚 Documentation & Examples")
        
        st.markdown("""
        Comprehensive developer resources including API documentation, IaC templates, 
        architecture patterns, and troubleshooting guides.
        """)
        
        st.markdown("---")
        
        # Documentation Categories
        tab1, tab2, tab3, tab4 = st.tabs([
            "📖 Getting Started",
            "💻 Code Examples",
            "🏗️ Architecture Patterns",
            "🔧 Troubleshooting"
        ])
        
        with tab1:
            st.markdown("### 🚀 Quick Start Guide")
            
            st.markdown("#### Prerequisites")
            st.code("""
# Install required tools
brew install terraform
brew install aws-cli
brew install kubectl

# Configure AWS credentials
aws configure

# Clone infrastructure repository
git clone https://github.com/org/infrastructure-platform.git
cd infrastructure-platform
            """, language="bash")
            
            st.markdown("#### Your First Deployment")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**1. Choose a Template**")
                st.code("""
cd templates/web-application
ls -la

# Files:
# - main.tf
# - variables.tf
# - outputs.tf
# - README.md
                """, language="bash")
                
                st.markdown("**2. Customize Variables**")
                st.code("""
# Edit terraform.tfvars
environment = "development"
project_name = "my-web-app"
instance_type = "t3.small"
enable_ha = false
                """, language="hcl")
            
            with col2:
                st.markdown("**3. Deploy Infrastructure**")
                st.code("""
# Initialize Terraform
terraform init

# Plan deployment
terraform plan

# Apply changes
terraform apply
                """, language="bash")
                
                st.markdown("**4. Verify Deployment**")
                st.code("""
# Check resources
terraform show

# Get outputs
terraform output

# Test application
curl https://my-web-app.example.com
                """, language="bash")
            
            st.markdown("---")
            
            st.markdown("#### Key Concepts")
            
            with st.expander("🏷️ Tagging Standards"):
                st.markdown("""
                All resources must include these tags:
                - **Environment**: dev, qa, staging, prod
                - **Project**: Project code (e.g., PRJ-2025-001)
                - **CostCenter**: Cost center code
                - **Owner**: Team email
                - **ManagedBy**: terraform
                """)
                
                st.code("""
tags = {
  Environment = "production"
  Project     = "PRJ-2025-001"
  CostCenter  = "CC-ENG-001"
  Owner       = "platform-team@company.com"
  ManagedBy   = "terraform"
}
                """, language="hcl")
            
            with st.expander("📝 Naming Conventions"):
                st.markdown("""
                Resource naming pattern: `{env}-{project}-{resource}-{id}`
                
                Examples:
                - EC2: `prod-webapp-ec2-01`
                - RDS: `prod-webapp-rds-mysql`
                - S3: `prod-webapp-logs-bucket`
                - VPC: `prod-network-vpc-main`
                """)
            
            with st.expander("🔒 Security Best Practices"):
                st.markdown("""
                - Enable encryption at rest for all data stores
                - Use AWS Secrets Manager for credentials
                - Implement least privilege IAM policies
                - Enable MFA for privileged accounts
                - Use private subnets for application layers
                - Enable VPC Flow Logs
                - Implement WAF for public endpoints
                """)
        
        with tab2:
            st.markdown("### 💻 Infrastructure as Code Examples")
            
            example_category = st.selectbox(
                "Select Example Category:",
                ["Web Application", "Serverless", "Kubernetes", "Data Pipeline", 
                 "Machine Learning", "Networking"]
            )
            
            if example_category == "Web Application":
                st.markdown("#### 3-Tier Web Application")
                
                st.code(r"""
# main.tf - 3-Tier Web Application

# VPC Configuration
module "vpc" {
  source = "../../modules/networking/vpc"
  
  name = "\${var.environment}-\${var.project_name}-vpc"
  cidr = "10.0.0.0/16"
  
  azs             = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
  
  enable_nat_gateway = true
  enable_vpn_gateway = false
  
  tags = local.common_tags
}

# Application Load Balancer
module "alb" {
  source = "../../modules/compute/alb"
  
  name               = "\${var.environment}-\${var.project_name}-alb"
  vpc_id             = module.vpc.vpc_id
  subnets            = module.vpc.public_subnets
  security_group_ids = [module.alb_sg.security_group_id]
  
  certificate_arn = var.ssl_certificate_arn
  
  target_groups = [{
    name     = "web-servers"
    port     = 80
    protocol = "HTTP"
  }]
  
  tags = local.common_tags
}

# Auto Scaling Group
module "asg" {
  source = "../../modules/compute/asg"
  
  name                 = "\${var.environment}-\${var.project_name}-asg"
  vpc_zone_identifier  = module.vpc.private_subnets
  target_group_arns    = [module.alb.target_group_arns[0]]
  
  min_size         = var.asg_min_size
  max_size         = var.asg_max_size
  desired_capacity = var.asg_desired_capacity
  
  launch_template = {
    name          = "\${var.environment}-\${var.project_name}-lt"
    image_id      = data.aws_ami.amazon_linux_2.id
    instance_type = var.instance_type
    user_data     = base64encode(file("user-data.sh"))
  }
  
  tags = local.common_tags
}

# RDS Database
module "rds" {
  source = "../../modules/database/rds"
  
  identifier = "\${var.environment}-\${var.project_name}-mysql"
  
  engine         = "mysql"
  engine_version = "8.0"
  instance_class = var.db_instance_class
  
  allocated_storage     = 100
  max_allocated_storage = 500
  storage_encrypted     = true
  
  db_name  = var.db_name
  username = var.db_username
  password = data.aws_secretsmanager_secret_version.db_password.secret_string
  
  multi_az               = var.enable_ha
  vpc_security_group_ids = [module.rds_sg.security_group_id]
  db_subnet_group_name   = module.vpc.database_subnet_group
  
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  tags = local.common_tags
}

# S3 Buckets
module "s3_static_assets" {
  source = "../../modules/storage/s3"
  
  bucket = "\${var.environment}-\${var.project_name}-static-assets"
  
  versioning = {
    enabled = true
  }
  
  server_side_encryption_configuration = {
    rule = {
      apply_server_side_encryption_by_default = {
        sse_algorithm = "AES256"
      }
    }
  }
  
  lifecycle_rule = [{
    id      = "transition-old-versions"
    enabled = true
    
    noncurrent_version_transition = [{
      days          = 30
      storage_class = "STANDARD_IA"
    }]
  }]
  
  tags = local.common_tags
}

# CloudWatch Alarms
module "cloudwatch_alarms" {
  source = "../../modules/monitoring/cloudwatch"
  
  alb_name = module.alb.name
  asg_name = module.asg.name
  rds_name = module.rds.identifier
  
  sns_topic_arn = var.alert_sns_topic_arn
  
  tags = local.common_tags
}

# Outputs
output "alb_dns_name" {
  description = "DNS name of the load balancer"
  value       = module.alb.dns_name
}

output "rds_endpoint" {
  description = "RDS database endpoint"
  value       = module.rds.endpoint
  sensitive   = true
}

output "static_assets_bucket" {
  description = "S3 bucket for static assets"
  value       = module.s3_static_assets.bucket_name
}
                """, language="hcl")
            
            elif example_category == "Serverless":
                st.markdown("#### Serverless REST API")
                
                st.code(r"""
# main.tf - Serverless REST API with Lambda & API Gateway

# Lambda Function
resource "aws_lambda_function" "api" {
  filename         = "lambda.zip"
  function_name    = "\${var.environment}-\${var.project_name}-api"
  role            = aws_iam_role.lambda_exec.arn
  handler         = "index.handler"
  source_code_hash = filebase64sha256("lambda.zip")
  runtime         = "nodejs18.x"
  timeout         = 30
  memory_size     = 512
  
  environment {
    variables = {
      DYNAMODB_TABLE = aws_dynamodb_table.main.name
      STAGE          = var.environment
    }
  }
  
  vpc_config {
    subnet_ids         = var.private_subnet_ids
    security_group_ids = [aws_security_group.lambda.id]
  }
  
  tags = local.common_tags
}

# API Gateway REST API
resource "aws_apigatewayv2_api" "main" {
  name          = "\${var.environment}-\${var.project_name}-api"
  protocol_type = "HTTP"
  
  cors_configuration {
    allow_origins = ["https://app.example.com"]
    allow_methods = ["GET", "POST", "PUT", "DELETE"]
    allow_headers = ["content-type", "authorization"]
    max_age       = 300
  }
  
  tags = local.common_tags
}

# API Gateway Integration
resource "aws_apigatewayv2_integration" "lambda" {
  api_id = aws_apigatewayv2_api.main.id
  
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.api.invoke_arn
  
  payload_format_version = "2.0"
}

# API Gateway Routes
resource "aws_apigatewayv2_route" "get_items" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "GET /items"
  target    = "integrations/\${aws_apigatewayv2_integration.lambda.id}"
  
  authorization_type = "JWT"
  authorizer_id      = aws_apigatewayv2_authorizer.cognito.id
}

# DynamoDB Table
resource "aws_dynamodb_table" "main" {
  name           = "\${var.environment}-\${var.project_name}-data"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "id"
  range_key      = "timestamp"
  
  attribute {
    name = "id"
    type = "S"
  }
  
  attribute {
    name = "timestamp"
    type = "N"
  }
  
  ttl {
    attribute_name = "expires_at"
    enabled        = true
  }
  
  point_in_time_recovery {
    enabled = true
  }
  
  server_side_encryption {
    enabled = true
  }
  
  tags = local.common_tags
}

# Lambda Permission for API Gateway
resource "aws_lambda_permission" "apigw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.api.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "\${aws_apigatewayv2_api.main.execution_arn}/*/*"
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/\${aws_lambda_function.api.function_name}"
  retention_in_days = 7
  
  tags = local.common_tags
}

# Outputs
output "api_endpoint" {
  description = "API Gateway endpoint URL"
  value       = aws_apigatewayv2_api.main.api_endpoint
}

output "dynamodb_table_name" {
  description = "DynamoDB table name"
  value       = aws_dynamodb_table.main.name
}
                """, language="hcl")
            
            st.markdown("---")
            st.info("💡 **Tip**: Copy the code above and modify it for your use case. All examples follow best practices.")
        
        with tab3:
            st.markdown("### 🏗️ Reference Architectures")
            
            architecture_type = st.selectbox(
                "Select Architecture Pattern:",
                ["High Availability Web App", "Microservices on EKS", 
                 "Data Lake & Analytics", "IoT Platform"]
            )
            
            if architecture_type == "High Availability Web App":
                st.markdown("#### High Availability Web Application")
                
                st.markdown("""
                **Architecture Components:**
                - Multi-AZ Application Load Balancer
                - Auto Scaling Group across 3 Availability Zones
                - Multi-AZ RDS with Read Replicas
                - ElastiCache for session management
                - S3 + CloudFront for static assets
                - Route 53 for DNS with health checks
                - CloudWatch for monitoring
                - AWS WAF for security
                
                **Design Principles:**
                - 99.99% availability target
                - Automatic failover capabilities
                - Zero-downtime deployments
                - Scalability from 10 to 10,000+ users
                """)
                
                st.image("https://d1.awsstatic.com/architecture-diagrams/ArchitectureDiagrams/web-app-hosting-scalable-ra.5c92c17891c1baebea7bd8ca8e738c066a8eb01c.png",
                        caption="High Availability Web Application Architecture")
            
            elif architecture_type == "Microservices on EKS":
                st.markdown("#### Microservices on Amazon EKS")
                
                st.markdown("""
                **Architecture Components:**
                - Amazon EKS cluster with managed node groups
                - Application Load Balancer Ingress Controller
                - AWS App Mesh for service mesh
                - Amazon RDS and DynamoDB for data persistence
                - Amazon ECR for container registry
                - AWS X-Ray for distributed tracing
                - Prometheus & Grafana for monitoring
                - Fluentd for log aggregation
                
                **Design Principles:**
                - Loose coupling between services
                - Independent deployment & scaling
                - Service discovery & load balancing
                - Observability & tracing
                """)
            
            st.markdown("---")
            
            st.markdown("#### Key Design Patterns")
            
            with st.expander("🔄 Blue-Green Deployment"):
                st.markdown("""
                Zero-downtime deployment strategy:
                1. Deploy new version (Green) alongside existing (Blue)
                2. Test Green environment thoroughly
                3. Switch traffic from Blue to Green
                4. Keep Blue as rollback option
                5. Decommission Blue after validation
                
                **Benefits:**
                - Zero downtime
                - Easy rollback
                - Testing in production environment
                """)
            
            with st.expander("🎯 Circuit Breaker"):
                st.markdown("""
                Prevent cascading failures:
                - Monitor service health
                - Open circuit when failures exceed threshold
                - Fail fast instead of waiting for timeout
                - Periodically retry (half-open state)
                - Close circuit when service recovers
                
                **Implementation**: AWS App Mesh, API Gateway throttling
                """)
            
            with st.expander("💾 CQRS (Command Query Responsibility Segregation)"):
                st.markdown("""
                Separate read and write operations:
                - Write operations use transactional database (RDS)
                - Read operations use optimized read replicas
                - Event sourcing with DynamoDB Streams
                - Cache frequently accessed data (ElastiCache)
                
                **Benefits:**
                - Optimized performance for reads and writes
                - Scalability
                - Flexibility in data models
                """)
        
        with tab4:
            st.markdown("### 🔧 Troubleshooting Guide")
            
            issue_category = st.selectbox(
                "Select Issue Category:",
                ["Deployment Failures", "Performance Issues", "Security Alerts", 
                 "Cost Anomalies", "Networking Problems"]
            )
            
            if issue_category == "Deployment Failures":
                st.markdown("#### Common Deployment Issues")
                
                with st.expander("❌ Terraform Apply Failed"):
                    st.markdown("""
                    **Symptoms:**
                    ```
                    Error: Error creating EC2 instance: InsufficientInstanceCapacity
                    ```
                    
                    **Causes:**
                    - AWS capacity issues in specific AZ
                    - Instance type not available
                    - Account limits reached
                    
                    **Solutions:**
                    1. Change to different instance type
                    2. Deploy to different Availability Zone
                    3. Request limit increase
                    4. Use mixed instance types in Auto Scaling
                    
                    **Prevention:**
                    - Use multiple instance types
                    - Spread across multiple AZs
                    - Monitor capacity trends
                    """)
                
                with st.expander("⚠️ Security Group Dependency Error"):
                    st.markdown("""
                    **Symptoms:**
                    ```
                    Error: Error deleting security group: DependencyViolation
                    ```
                    
                    **Causes:**
                    - Security group still attached to resources
                    - Circular dependencies
                    - Cross-account references
                    
                    **Solutions:**
                    1. Check dependencies: `terraform state list`
                    2. Remove resources using the security group
                    3. Use `terraform taint` to force recreation
                    4. Delete manually from AWS Console
                    
                    **Prevention:**
                    - Proper resource dependencies in Terraform
                    - Use `depends_on` meta-argument
                    - Clean up resources in correct order
                    """)
                
                with st.expander("🔒 IAM Permission Denied"):
                    st.markdown("""
                    **Symptoms:**
                    ```
                    Error: AccessDenied: User is not authorized to perform: iam:CreateRole
                    ```
                    
                    **Causes:**
                    - Insufficient IAM permissions
                    - Service Control Policies (SCPs)
                    - Permission boundaries
                    
                    **Solutions:**
                    1. Check IAM user/role permissions
                    2. Verify SCPs at organization level
                    3. Review permission boundaries
                    4. Request elevated access
                    
                    **Prevention:**
                    - Use least privilege principle
                    - Regular permission audits
                    - Document required permissions
                    """)
            
            elif issue_category == "Performance Issues":
                st.markdown("#### Performance Troubleshooting")
                
                with st.expander("🐌 Slow Application Response"):
                    st.markdown("""
                    **Investigation Steps:**
                    
                    1. **Check Application Metrics**
                    ```bash
                    # View CloudWatch metrics
                    aws cloudwatch get-metric-statistics \\
                      --namespace AWS/ApplicationELB \\
                      --metric-name TargetResponseTime \\
                      --dimensions Name=LoadBalancer,Value=app/my-alb/abc123 \\
                      --start-time 2025-01-15T00:00:00Z \\
                      --end-time 2025-01-15T23:59:59Z \\
                      --period 3600 \\
                      --statistics Average
                    ```
                    
                    2. **Check Database Performance**
                    - Review RDS Performance Insights
                    - Check for slow queries
                    - Monitor CPU and memory utilization
                    
                    3. **Network Latency**
                    - VPC Flow Logs
                    - Check cross-AZ traffic
                    - Review NAT Gateway metrics
                    
                    **Common Fixes:**
                    - Add read replicas for read-heavy workloads
                    - Implement caching (ElastiCache)
                    - Optimize database queries
                    - Scale EC2 instances
                    - Use CloudFront for static content
                    """)
            
            st.markdown("---")
            
            st.markdown("#### Quick Reference Commands")
            
            st.code("""
# Terraform Commands
terraform init          # Initialize working directory
terraform plan          # Preview changes
terraform apply         # Apply changes
terraform destroy       # Destroy infrastructure
terraform state list    # List resources in state
terraform taint         # Mark resource for recreation
terraform import        # Import existing resources

# AWS CLI Commands
aws ec2 describe-instances                    # List EC2 instances
aws rds describe-db-instances                 # List RDS instances
aws s3 ls                                     # List S3 buckets
aws logs tail /aws/lambda/function-name       # View Lambda logs
aws cloudformation describe-stacks            # List CloudFormation stacks

# Kubernetes Commands (EKS)
kubectl get pods                              # List pods
kubectl describe pod <pod-name>               # Pod details
kubectl logs <pod-name>                       # View logs
kubectl exec -it <pod-name> -- /bin/bash     # Access pod shell
kubectl get events --sort-by='.lastTimestamp' # Recent events
            """, language="bash")
        
        st.markdown("---")
        
        # Additional Resources
        st.markdown("### 🔗 Additional Resources")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Internal Links:**")
            st.markdown("- [Wiki Documentation](https://wiki.company.com/infrastructure)")
            st.markdown("- [Video Tutorials](https://videos.company.com/infrastructure)")
            st.markdown("- [Slack Channel: #infrastructure](slack://channel?id=infra)")
            st.markdown("- [Office Hours: Tuesdays 2-3 PM](https://meet.company.com)")
        
        with col2:
            st.markdown("**External Resources:**")
            st.markdown("- [AWS Documentation](https://docs.aws.amazon.com)")
            st.markdown("- [Terraform Registry](https://registry.terraform.io)")
            st.markdown("- [AWS Well-Architected](https://aws.amazon.com/architecture/well-architected)")
            st.markdown("- [AWS Solutions Library](https://aws.amazon.com/solutions)")
        
        with col3:
            st.markdown("**Support:**")
            st.markdown("- 📧 Email: platform-team@company.com")
            st.markdown("- 💬 Slack: #infrastructure-help")
            st.markdown("- 🎫 JIRA: Create ticket")
            st.markdown("- 📞 On-Call: +1-800-PLATFORM")
    
    @staticmethod
    def render_infrasecops():
        """Render InfraSecOps"""
        st.markdown("## 🔒 InfraSecOps - Security Integrated Development")
        
        st.markdown("""
        Embed security throughout the infrastructure development lifecycle. Shift security left 
        with automated scanning, policy validation, and continuous monitoring.
        """)
        
        st.markdown("---")
        
        # Security Pipeline Overview
        st.markdown("### 🛡️ Security Pipeline Overview")
        
        st.markdown("""
        **Shift-Left Security Approach:**
        1. **Code Commit** → Static code analysis (SAST)
        2. **Build** → Dependency scanning & license check
        3. **Test** → Dynamic application testing (DAST)
        4. **Deploy** → Policy validation & compliance check
        5. **Runtime** → Continuous monitoring & threat detection
        """)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Security Scans (24h)", "342", "+28")
        with col2:
            st.metric("Vulnerabilities Found", "47", "+12")
        with col3:
            st.metric("Auto-Remediated", "39", "+10")
        with col4:
            st.metric("Critical Issues", "2", "-1")
        
        st.markdown("---")
        
        # Security Scanning Results
        st.markdown("### 🔍 Security Scanning Results")
        
        scan_results = [
            {
                "scan_id": "SCAN-20250115-143022",
                "repository": "infrastructure-platform",
                "branch": "feature/eks-cluster",
                "severity": "🔴 Critical",
                "findings": "2 Critical, 8 High, 15 Medium",
                "status": "❌ Failed",
                "scanned": "2 hours ago"
            },
            {
                "scan_id": "SCAN-20250115-120145",
                "repository": "web-application",
                "branch": "main",
                "severity": "🟡 Medium",
                "findings": "0 Critical, 0 High, 5 Medium",
                "status": "⚠️ Warning",
                "scanned": "4 hours ago"
            },
            {
                "scan_id": "SCAN-20250115-095032",
                "repository": "serverless-api",
                "branch": "develop",
                "severity": "🟢 Low",
                "findings": "0 Critical, 0 High, 0 Medium",
                "status": "✅ Passed",
                "scanned": "7 hours ago"
            },
            {
                "scan_id": "SCAN-20250114-163421",
                "repository": "data-pipeline",
                "branch": "hotfix/security-patch",
                "severity": "🟠 High",
                "findings": "1 Critical, 12 High, 8 Medium",
                "status": "🔄 Remediation",
                "scanned": "1 day ago"
            }
        ]
        
        df_scans = pd.DataFrame(scan_results)
        st.dataframe(df_scans, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Vulnerability Details
        st.markdown("### 🐛 Vulnerability Details")
        
        selected_scan = st.selectbox(
            "Select Scan to Review:",
            ["SCAN-20250115-143022 (Critical)",
             "SCAN-20250115-120145 (Medium)",
             "SCAN-20250114-163421 (High)"]
        )
        
        vulnerabilities = [
            {
                "cve": "CVE-2024-12345",
                "severity": "🔴 Critical (9.8)",
                "component": "terraform-provider-aws v5.21.0",
                "description": "Arbitrary code execution vulnerability",
                "recommendation": "Upgrade to v5.22.0 or later",
                "status": "🔄 In Progress"
            },
            {
                "cve": "CVE-2024-67890",
                "severity": "🔴 Critical (9.1)",
                "component": "kubectl v1.27.3",
                "description": "Privilege escalation in Kubernetes",
                "recommendation": "Upgrade to v1.28.0 or apply security patch",
                "status": "⏰ Pending"
            },
            {
                "cve": "N/A (Policy Violation)",
                "severity": "🟠 High",
                "component": "Security Group: sg-0a3b5c7d",
                "description": "Unrestricted SSH access from 0.0.0.0/0",
                "recommendation": "Restrict SSH to bastion host or VPN",
                "status": "❌ Open"
            },
            {
                "cve": "N/A (Compliance)",
                "severity": "🟠 High",
                "component": "S3 Bucket: prod-data-bucket",
                "description": "Encryption at rest not enabled",
                "recommendation": "Enable SSE-S3 or SSE-KMS encryption",
                "status": "✅ Remediated"
            }
        ]
        
        df_vulns = pd.DataFrame(vulnerabilities)
        st.dataframe(df_vulns, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Security Policy Checks
        st.markdown("### 📋 Security Policy Validation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**PASSED Policies:**")
            st.success("✅ SEC-001: Encryption at rest required")
            st.success("✅ SEC-002: MFA enabled for privileged accounts")
            st.success("✅ SEC-003: IAM password policy enforced")
            st.success("✅ SEC-004: CloudTrail logging enabled")
            st.success("✅ SEC-005: VPC Flow Logs enabled")
        
        with col2:
            st.markdown("**FAILED Policies:**")
            st.error("❌ SEC-006: Public S3 buckets detected")
            st.error("❌ SEC-007: Unrestricted security group rules")
            st.error("❌ SEC-008: Root account activity detected")
            st.warning("⚠️ SEC-009: Missing backup configuration")
            st.warning("⚠️ SEC-010: GuardDuty not enabled")
        
        st.markdown("---")
        
        # Secrets Management
        st.markdown("### 🔐 Secrets Management")
        
        st.markdown("""
        **Secrets Scanning Results:**
        - AWS Access Keys: ✅ None detected
        - Database Passwords: ✅ None detected
        - API Keys: ⚠️ 2 potential matches (false positives)
        - Private Keys: ✅ None detected
        - Certificates: ✅ Properly stored in ACM
        """)
        
        st.info("""
        **Best Practices:**
        - Store secrets in AWS Secrets Manager or Parameter Store
        - Rotate secrets automatically (every 90 days)
        - Use IAM roles instead of access keys
        - Enable secret encryption with KMS
        - Audit secret access with CloudTrail
        """)
        
        st.markdown("---")
        
        # Compliance Checks
        st.markdown("### 🏆 Compliance Framework Checks")
        
        compliance_results = [
            {
                "framework": "PCI DSS 4.0",
                "status": "✅ Compliant",
                "score": "98%",
                "findings": "2 minor issues",
                "last_audit": "2025-01-10"
            },
            {
                "framework": "SOC 2 Type II",
                "status": "✅ Compliant",
                "score": "97%",
                "findings": "3 observations",
                "last_audit": "2025-01-08"
            },
            {
                "framework": "HIPAA",
                "status": "⚠️ Partial",
                "score": "89%",
                "findings": "8 items to address",
                "last_audit": "2025-01-05"
            },
            {
                "framework": "GDPR",
                "status": "✅ Compliant",
                "score": "95%",
                "findings": "4 recommendations",
                "last_audit": "2025-01-12"
            },
            {
                "framework": "ISO 27001",
                "status": "⚠️ Partial",
                "score": "91%",
                "findings": "6 controls pending",
                "last_audit": "2025-01-07"
            }
        ]
        
        df_compliance = pd.DataFrame(compliance_results)
        st.dataframe(df_compliance, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Remediation Actions
        st.markdown("### 🛠️ Automated Remediation")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Auto-Remediate All", type="primary", use_container_width=True):
                with st.spinner("Running automated remediation..."):
                    import time
                    time.sleep(3)
                    st.success("✅ Automated remediation completed!")
                    st.info("""
                    **Actions Taken:**
                    - Upgraded 4 vulnerable dependencies
                    - Enabled encryption on 2 S3 buckets
                    - Restricted 3 security group rules
                    - Rotated 1 exposed credential
                    """)
        
        with col2:
            if st.button("📝 Generate Report", use_container_width=True):
                st.info("Security report generated: SEC-RPT-20250115.pdf")
                st.success("Report sent to security-team@company.com")
        
        with col3:
            if st.button("🎫 Create Jira Tickets", use_container_width=True):
                st.success("Created 8 Jira tickets for manual review items")
                st.info("Tickets assigned to Security Team")
        
        st.markdown("---")
        
        # Security Metrics
        st.markdown("### 📊 Security Metrics & Trends")
        
        metrics_data = pd.DataFrame({
            'Date': pd.date_range(start='2025-01-08', end='2025-01-15', freq='D'),
            'Critical': [5, 4, 6, 3, 5, 2, 4, 2],
            'High': [15, 18, 16, 14, 17, 12, 15, 13],
            'Medium': [32, 28, 35, 30, 33, 25, 31, 27],
            'Low': [48, 45, 52, 47, 50, 44, 49, 46]
        })
        
        st.line_chart(metrics_data.set_index('Date'))
        
        st.markdown("---")
        
        # Security Tools Integration
        st.markdown("### 🔧 Integrated Security Tools")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**SAST Tools:**")
            st.markdown("- ✅ Checkov (IaC scanning)")
            st.markdown("- ✅ tfsec (Terraform security)")
            st.markdown("- ✅ Semgrep (Code patterns)")
            st.markdown("- ✅ SonarQube (Code quality)")
        
        with col2:
            st.markdown("**Dependency Scanning:**")
            st.markdown("- ✅ Snyk (Vulnerabilities)")
            st.markdown("- ✅ Dependabot (Updates)")
            st.markdown("- ✅ OWASP Dependency Check")
            st.markdown("- ✅ Trivy (Container scanning)")
        
        with col3:
            st.markdown("**Runtime Security:**")
            st.markdown("- ✅ AWS GuardDuty")
            st.markdown("- ✅ AWS Security Hub")
            st.markdown("- ✅ AWS Inspector")
            st.markdown("- ✅ Falco (Runtime detection)")
    
    @staticmethod
    def render_user_community():
        """Render User Community"""
        st.markdown("## 👥 User Community & Collaboration")
        
        st.markdown("""
        Foster a collaborative environment where developers share knowledge, best practices, 
        and contribute to platform improvements.
        """)
        
        st.markdown("---")
        
        # Community Stats
        st.markdown("### 📊 Community Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Active Users", "847", "+156 this month")
        with col2:
            st.metric("Total Posts", "2,341", "+248")
        with col3:
            st.metric("Resolved Questions", "1,876", "+198")
        with col4:
            st.metric("Satisfaction Score", "4.7/5", "+0.2")
        
        st.markdown("---")
        
        # Community Tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "💬 Discussion Forum",
            "💡 Feature Requests",
            "🏆 Leaderboard",
            "📈 Usage Analytics"
        ])
        
        with tab1:
            st.markdown("### 💬 Community Forum")
            
            # Recent Discussions
            discussions = [
                {
                    "title": "Best practices for EKS cluster auto-scaling?",
                    "author": "john.doe",
                    "category": "Kubernetes",
                    "replies": "12",
                    "views": "247",
                    "status": "✅ Answered",
                    "posted": "2 hours ago"
                },
                {
                    "title": "How to implement blue-green deployment with Terraform?",
                    "author": "jane.smith",
                    "category": "CI/CD",
                    "replies": "8",
                    "views": "189",
                    "status": "💬 Active",
                    "posted": "5 hours ago"
                },
                {
                    "title": "RDS connection pooling recommendations",
                    "author": "alice.wang",
                    "category": "Database",
                    "replies": "15",
                    "views": "312",
                    "status": "✅ Answered",
                    "posted": "1 day ago"
                },
                {
                    "title": "Cost optimization strategies for S3 storage",
                    "author": "bob.chen",
                    "category": "FinOps",
                    "replies": "23",
                    "views": "456",
                    "status": "✅ Answered",
                    "posted": "1 day ago"
                },
                {
                    "title": "Lambda cold start mitigation techniques",
                    "author": "charlie.brown",
                    "category": "Serverless",
                    "replies": "18",
                    "views": "378",
                    "status": "💬 Active",
                    "posted": "2 days ago"
                }
            ]
            
            df_discussions = pd.DataFrame(discussions)
            st.dataframe(df_discussions, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            
            # New Discussion
            st.markdown("#### 📝 Start New Discussion")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                discussion_title = st.text_input("Title:", placeholder="What's your question?")
                discussion_category = st.selectbox(
                    "Category:",
                    ["General", "Kubernetes", "CI/CD", "Database", "Security", 
                     "FinOps", "Networking", "Serverless"]
                )
            
            with col2:
                discussion_tags = st.multiselect(
                    "Tags:",
                    ["aws", "terraform", "eks", "rds", "lambda", "s3", "vpc", 
                     "security", "cost", "performance"]
                )
            
            discussion_content = st.text_area(
                "Question Details:",
                placeholder="Provide detailed context, what you've tried, and what you're trying to achieve...",
                height=150
            )
            
            if st.button("📤 Post Question", type="primary"):
                st.success("✅ Question posted successfully!")
                st.info("Community members will be notified. Expect responses within 1-2 hours.")
        
        with tab2:
            st.markdown("### 💡 Feature Requests & Roadmap")
            
            # Feature Request Status
            feature_status = st.selectbox(
                "Filter by Status:",
                ["All", "🟢 Planned", "🔵 Under Review", "🟡 In Progress", 
                 "✅ Completed", "❌ Declined"]
            )
            
            feature_requests = [
                {
                    "feature": "Terraform module for AWS Backup automation",
                    "requested_by": "Platform Team",
                    "votes": "87 👍",
                    "status": "🟡 In Progress",
                    "priority": "High",
                    "eta": "Q1 2025"
                },
                {
                    "feature": "Cost anomaly detection with ML",
                    "requested_by": "FinOps Team",
                    "votes": "142 👍",
                    "status": "🟢 Planned",
                    "priority": "High",
                    "eta": "Q2 2025"
                },
                {
                    "feature": "Multi-account governance dashboard",
                    "requested_by": "Security Team",
                    "votes": "201 👍",
                    "status": "🟡 In Progress",
                    "priority": "Critical",
                    "eta": "Q1 2025"
                },
                {
                    "feature": "Kubernetes cluster templates for different workloads",
                    "requested_by": "Dev Team",
                    "votes": "156 👍",
                    "status": "✅ Completed",
                    "priority": "High",
                    "eta": "Released"
                },
                {
                    "feature": "Auto-scaling policies based on custom metrics",
                    "requested_by": "SRE Team",
                    "votes": "98 👍",
                    "status": "🔵 Under Review",
                    "priority": "Medium",
                    "eta": "TBD"
                }
            ]
            
            df_features = pd.DataFrame(feature_requests)
            st.dataframe(df_features, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            
            # Submit Feature Request
            st.markdown("#### ✨ Submit New Feature Request")
            
            feature_title = st.text_input("Feature Title:", placeholder="Brief description of the feature")
            
            col1, col2 = st.columns(2)
            
            with col1:
                feature_category = st.selectbox(
                    "Category:",
                    ["Infrastructure", "Security", "Cost Optimization", "Monitoring", 
                     "Automation", "Documentation", "Developer Experience"]
                )
            
            with col2:
                business_impact = st.selectbox(
                    "Business Impact:",
                    ["Critical", "High", "Medium", "Low"]
                )
            
            feature_description = st.text_area(
                "Detailed Description:",
                placeholder="Explain the feature, use case, and expected benefits...",
                height=120
            )
            
            feature_justification = st.text_area(
                "Business Justification:",
                placeholder="Why is this feature needed? What problem does it solve?",
                height=80
            )
            
            if st.button("📤 Submit Feature Request", type="primary"):
                st.success("✅ Feature request submitted!")
                st.info("""
                **Next Steps:**
                1. Product team will review within 5 business days
                2. Community can vote on your request
                3. High-voted features get prioritized
                4. You'll receive updates on progress
                """)
        
        with tab3:
            st.markdown("### 🏆 Community Leaderboard")
            
            # Time period selector
            period = st.selectbox(
                "Period:",
                ["This Month", "Last Month", "This Quarter", "All Time"]
            )
            
            # Leaderboard categories
            leaderboard_category = st.radio(
                "Category:",
                ["🌟 Top Contributors", "💬 Most Helpful", "🚀 Most Active", "📚 Best Answers"],
                horizontal=True
            )
            
            if leaderboard_category == "🌟 Top Contributors":
                leaders = [
                    {
                        "rank": "🥇",
                        "user": "alice.wang",
                        "team": "Platform Engineering",
                        "contributions": "142",
                        "points": "1,847",
                        "badges": "5 🏆"
                    },
                    {
                        "rank": "🥈",
                        "user": "bob.chen",
                        "team": "SRE",
                        "contributions": "128",
                        "points": "1,632",
                        "badges": "4 🏆"
                    },
                    {
                        "rank": "🥉",
                        "user": "charlie.brown",
                        "team": "Security",
                        "contributions": "115",
                        "points": "1,489",
                        "badges": "4 🏆"
                    },
                    {
                        "rank": "4",
                        "user": "diana.prince",
                        "team": "DevOps",
                        "contributions": "98",
                        "points": "1,234",
                        "badges": "3 🏆"
                    },
                    {
                        "rank": "5",
                        "user": "edward.stark",
                        "team": "Cloud Architecture",
                        "contributions": "87",
                        "points": "1,156",
                        "badges": "3 🏆"
                    }
                ]
                
                df_leaders = pd.DataFrame(leaders)
                st.dataframe(df_leaders, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            
            # Achievement Badges
            st.markdown("### 🏅 Achievement Badges")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown("**🌟 First Contribution**")
                st.caption("Make your first post")
                st.progress(100)
            
            with col2:
                st.markdown("**💬 Helpful Member**")
                st.caption("10+ helpful answers")
                st.progress(100)
            
            with col3:
                st.markdown("**🚀 Super Contributor**")
                st.caption("50+ contributions")
                st.progress(75)
            
            with col4:
                st.markdown("**🏆 Platform Expert**")
                st.caption("100+ contributions")
                st.progress(45)
        
        with tab4:
            st.markdown("### 📈 Platform Usage Analytics")
            
            # Time period
            analytics_period = st.selectbox(
                "Select Period:",
                ["Last 7 Days", "Last 30 Days", "Last Quarter", "Last Year"]
            )
            
            # Usage Metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Deployments", "1,847", "+234")
            with col2:
                st.metric("Infrastructure Requests", "923", "+145")
            with col3:
                st.metric("Active Projects", "127", "+18")
            with col4:
                st.metric("Avg Response Time", "14 min", "-8 min")
            
            st.markdown("---")
            
            # Usage Trends
            st.markdown("#### Daily Usage Trends")
            
            usage_data = pd.DataFrame({
                'Date': pd.date_range(start='2025-01-08', end='2025-01-15', freq='D'),
                'Deployments': [42, 38, 51, 47, 56, 44, 52, 48],
                'Service Requests': [28, 32, 27, 35, 31, 38, 29, 33],
                'Forum Posts': [15, 18, 16, 22, 19, 25, 20, 24]
            })
            
            st.line_chart(usage_data.set_index('Date'))
            
            st.markdown("---")
            
            # Most Used Services
            st.markdown("#### Most Requested Services")
            
            services = [
                {"service": "Web Application Stack", "requests": "342", "satisfaction": "4.8/5"},
                {"service": "Kubernetes Cluster", "requests": "287", "satisfaction": "4.6/5"},
                {"service": "Serverless API", "requests": "256", "satisfaction": "4.7/5"},
                {"service": "Data Pipeline", "requests": "198", "satisfaction": "4.5/5"},
                {"service": "ML Training Environment", "requests": "142", "satisfaction": "4.9/5"}
            ]
            
            df_services = pd.DataFrame(services)
            st.dataframe(df_services, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            
            # User Feedback
            st.markdown("#### Recent Feedback")
            
            feedback = [
                {
                    "user": "john.doe",
                    "rating": "⭐⭐⭐⭐⭐",
                    "comment": "Self-service portal is amazing! Deployed in 10 minutes.",
                    "date": "2025-01-15"
                },
                {
                    "user": "jane.smith",
                    "rating": "⭐⭐⭐⭐",
                    "comment": "Great documentation. Would love more video tutorials.",
                    "date": "2025-01-14"
                },
                {
                    "user": "alice.wang",
                    "rating": "⭐⭐⭐⭐⭐",
                    "comment": "GitOps integration streamlined our workflow significantly.",
                    "date": "2025-01-13"
                }
            ]
            
            df_feedback = pd.DataFrame(feedback)
            st.dataframe(df_feedback, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Community Guidelines
        with st.expander("📜 Community Guidelines"):
            st.markdown("""
            **Our Community Values:**
            
            1. **Be Respectful**: Treat all members with respect and professionalism
            2. **Be Helpful**: Share knowledge and help others learn
            3. **Be Constructive**: Provide actionable feedback and solutions
            4. **Be Collaborative**: Work together to solve problems
            5. **Be Inclusive**: Welcome developers of all skill levels
            
            **Posting Guidelines:**
            - Search before posting to avoid duplicates
            - Provide context and relevant details
            - Use clear, descriptive titles
            - Tag posts appropriately
            - Follow up on your questions
            
            **Code of Conduct:**
            - No spam or self-promotion
            - No harassment or discrimination
            - No sharing of sensitive information
            - Respect intellectual property
            - Follow company policies
            """)