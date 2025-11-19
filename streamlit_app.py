"""
CloudIDP - Cloud Infrastructure Development Platform
Multi-Cloud Architecture & Governance Framework
"""

import streamlit as st
from design_planning import DesignPlanningModule
from provisioning_deployment import ProvisioningDeploymentModule
from ondemand_operations import OnDemandOperationsModule
from ondemand_operations_part2 import OnDemandOperationsModule2
from finops_module import FinOpsModule
from security_compliance import SecurityComplianceModule
from policy_guardrails import PolicyGuardrailsModule
from module_07_abstraction import AbstractionReusabilityModule
from module_08_multicloud_hybrid import MultiCloudHybridModule
from module_09_developer_experience import DeveloperExperienceModule
from module_10_observability import ObservabilityIntegrationModule
from config import initialize_session_state
from anthropic_helper import AnthropicHelper

# Page configuration
st.set_page_config(
    page_title="CloudIDP - Cloud Infrastructure Development Platform",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF9900;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #232F3E;
        text-align: center;
        padding-bottom: 2rem;
    }
    .mode-indicator {
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .live-mode {
        background-color: #28a745;
        color: white;
    }
    .demo-mode {
        background-color: #ffc107;
        color: #000;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    """Main application entry point"""
    
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.markdown('<div class="main-header">☁️ CloudIDP</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Cloud Infrastructure Development Platform | Enterprise Architecture & Governance</div>', unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        # AWS-Style CloudIDP Logo
        st.markdown("""
            <div style="text-align: center; padding: 20px 0;">
                <div style="
                    background: linear-gradient(180deg, #232F3E 0%, #1a252f 100%);
                    border-radius: 8px;
                    padding: 25px 20px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                    margin-bottom: 10px;
                    border: 2px solid #FF9900;
                ">
                    <div style="
                        color: #FF9900;
                        font-size: 36px;
                        font-weight: bold;
                        letter-spacing: 3px;
                        margin-bottom: 8px;
                    ">CloudIDP</div>
                    <div style="
                        color: #FFFFFF;
                        font-size: 10px;
                        letter-spacing: 1.5px;
                        font-weight: 500;
                    ">INFRASTRUCTURE DEVELOPMENT PLATFORM</div>
                    <div style="
                        width: 60px;
                        height: 3px;
                        background: #FF9900;
                        margin: 12px auto 0 auto;
                        border-radius: 2px;
                    "></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        
        # ============= LIVE/DEMO MODE TOGGLE =============
        st.markdown("### 🔄 Operation Mode")
        mode = st.radio(
            "Select Mode:",
            ["Demo Mode", "Live Mode"],
            index=0,  # Demo Mode is default
            help="Demo Mode: Use sample data (no cloud credentials)\nLive Mode: Connect to real cloud services (AWS, Azure, GCP)"
        )
        
        # Update session state based on selection
        st.session_state.demo_mode = (mode == "Demo Mode")
        
        # Display mode indicator with clear visual feedback
        if st.session_state.demo_mode:
            st.markdown(
                '<div class="mode-indicator demo-mode">📋 DEMO MODE ACTIVE</div>',
                unsafe_allow_html=True
            )
            st.info("✓ Using sample data\n\n✓ No cloud credentials needed\n\n✓ Safe to explore all features")
        else:
            st.markdown(
                '<div class="mode-indicator live-mode">🟢 LIVE MODE ACTIVE</div>',
                unsafe_allow_html=True
            )
            st.warning("⚠️ Connected to Cloud Services\n\n⚠️ Real data will be used\n\n⚠️ Actions may affect resources")
        
        st.markdown("---")
        
        # Navigation
        st.markdown("### 📋 Navigation")
        page = st.selectbox(
            "Select Module:",
            [
                "Home",
                "─────── DESIGN & PLANNING ───────",
                "Design & Planning Overview",
                "Blueprint Definition",
                "Tagging Standards",
                "Naming Conventions",
                "Image/Artifact Versioning",
                "IaC Module Registry",
                "Design-Time Validation",
                "─────── PROVISIONING & DEPLOYMENT ───────",
                "Provisioning & Deployment Overview",
                "Multi-Cloud Provisioning",
                "Environment Promotion",
                "CI/CD Pipeline Integration",
                "─────── ON-DEMAND OPERATIONS ───────",
                "On-Demand Operations Overview",
                "Provisioning API",
                "Guardrail Validation",
                "Deployment Templates",
                "Compute Right-Sizing",
                "Storage Re-Tiering",
                "Auto-Scaling & Scheduling",
                "Patch Automation (SSM)",
                "Drift Detection",
                "Backup & Recovery",
                "Lifecycle Hooks",
                "Idle Resource Detection",
                "Continuous Availability",
                "Continuous Deployment",
                "─────── FINOPS ───────",
                "FinOps Overview",
                "Tag-Based Cost Tracking",
                "Budget Policy Enforcement",
                "Forecasting & Chargebacks",
                "Scheduled Infrastructure",
                "Spot Instance Orchestration",
                "Cost Anomaly Detection",
                "Reporting & Dashboards",
                "PMO vs FMO",
                "RI Recommendations",
                "Use Case Tracking",
                "─────── SECURITY & COMPLIANCE ───────",
                "Security & Compliance Overview",
                "─────── MODULE 07: ABSTRACTION & REUSABILITY ───────",
                "Module 07 Overview",
                "Composable Modules",
                "App-Centric Packaging",
                "Parameterization & Defaults",
                "Multi-Environment Support",
                "Lifecycle Management",
                "─────── MODULE 08: MULTI-CLOUD & HYBRID ───────",
                "Module 08 Overview",
                "Cloud & On-Prem Provisioning",
                "Unified Policy Framework",
                "Cloud-Specific Optimization",
                "Private+Public Connectivity",
                "Global Environment Management",
                "─────── MODULE 09: DEVELOPER EXPERIENCE ───────",
                "Module 09 Overview",
                "Governed Self-Service Portals",
                "GitOps Integration",
                "Drift Notification & Feedback Loop",
                "Documentation & Examples",
                "InfraSecOps",
                "User Community",
                "─────── MODULE 10: OBSERVABILITY & INTEGRATION ───────",
                "Module 10 Overview",
                "Standard Logging Stack via IaC",
                "Cloud Native Log/Metric Collection",
                "Change Tracking & CMDB Sync",
                "Policy Violation Reporting",
                "Event Tools for Alerting",
                "─────── POLICY & GUARDRAILS ───────",
                "Policy & Guardrails Overview",
                "Policy as Code Engine",
                "Cross-Cloud Policy Consistency",
                "Tag Policy Enforcement",
                "Naming & Placement Enforcement",
                "Quota Guardrails",
                "─────── AI ASSISTANT ───────",
                "AI Assistant"
            ]
        )
        
        st.markdown("---")
        
        # Cloud Provider Configuration (Live Mode Only)
        if not st.session_state.demo_mode:
            st.markdown("### ☁️ Cloud Provider Configuration")
            with st.expander("Cloud Settings", expanded=False):
                cloud_provider = st.selectbox(
                    "Cloud Provider:",
                    ["AWS", "Azure", "Google Cloud", "Multi-Cloud"],
                    index=0
                )
                st.session_state.cloud_provider = cloud_provider
                
                if cloud_provider == "AWS":
                    aws_region = st.selectbox(
                        "AWS Region:",
                        ["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1"],
                        index=0
                    )
                    st.session_state.aws_region = aws_region
                    
                    aws_account = st.text_input(
                        "AWS Account ID:",
                        placeholder="123456789012"
                    )
                    st.session_state.aws_account = aws_account
                    
                    if aws_account:
                        st.success("✅ AWS configured")
                
                elif cloud_provider == "Azure":
                    azure_subscription = st.text_input(
                        "Azure Subscription ID:",
                        placeholder="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
                    )
                    st.session_state.azure_subscription = azure_subscription
                    if azure_subscription:
                        st.success("✅ Azure configured")
                
                elif cloud_provider == "Google Cloud":
                    gcp_project = st.text_input(
                        "GCP Project ID:",
                        placeholder="my-project-id"
                    )
                    st.session_state.gcp_project = gcp_project
                    if gcp_project:
                        st.success("✅ GCP configured")
        
        # Anthropic API Configuration (from secrets)
        st.markdown("### 🤖 Claude AI")
        
        # Try to read API key from secrets
        api_key_found = False
        error_message = None
        
        try:
            # Check if secrets exist
            if hasattr(st, 'secrets'):
                # Check if anthropic section exists
                if 'anthropic' in st.secrets:
                    # Check if api_key exists in anthropic section
                    if 'api_key' in st.secrets['anthropic']:
                        api_key = st.secrets['anthropic']['api_key']
                        if api_key and len(api_key) > 0:
                            st.session_state.anthropic_api_key = api_key
                            api_key_found = True
                            st.success("✅ Claude AI connected")
                        else:
                            error_message = "API key is empty"
                    else:
                        error_message = "Key 'api_key' not found in [anthropic] section"
                else:
                    error_message = "Section [anthropic] not found in secrets"
            else:
                error_message = "Secrets not available (running locally without secrets.toml?)"
        except Exception as e:
            error_message = f"Error reading secrets: {str(e)}"
        
        # Show status
        if not api_key_found:
            st.session_state.anthropic_api_key = None
            st.warning(f"⚠️ API key not configured")
            if error_message:
                with st.expander("🔍 Debug Info", expanded=False):
                    st.code(error_message)
            st.caption("""Add to Streamlit Cloud secrets:
[anthropic]
api_key = "sk-ant-your-key"

Then REBOOT the app!""")
        
        st.markdown("---")
        st.caption("v1.0.0 | CloudIDP - Multi-Cloud Infrastructure Platform")
    
    # Main content area - Route to appropriate page
    if page == "Home":
        show_home_page()
    elif page.startswith("───────"):
        # Skip separator entries
        st.info("Please select a specific page from the navigation menu.")
    elif page == "Design & Planning Overview":
        show_design_planning_overview()
    elif page == "Blueprint Definition":
        DesignPlanningModule.render_blueprint_definition()
    elif page == "Tagging Standards":
        DesignPlanningModule.render_tagging_standards()
    elif page == "Naming Conventions":
        DesignPlanningModule.render_naming_conventions()
    elif page == "Image/Artifact Versioning":
        DesignPlanningModule.render_artifact_versioning()
    elif page == "IaC Module Registry":
        DesignPlanningModule.render_iac_registry()
    elif page == "Design-Time Validation":
        DesignPlanningModule.render_design_validation()
    elif page == "Provisioning & Deployment Overview":
        show_provisioning_deployment_overview()
    elif page == "Multi-Cloud Provisioning":
        ProvisioningDeploymentModule.render_multi_cloud_provisioning()
    elif page == "Environment Promotion":
        ProvisioningDeploymentModule.render_environment_promotion()
    elif page == "CI/CD Pipeline Integration":
        ProvisioningDeploymentModule.render_cicd_integration()
    elif page == "On-Demand Operations Overview":
        show_ondemand_operations_overview()
    elif page == "Provisioning API":
        OnDemandOperationsModule.render_provisioning_api()
    elif page == "Guardrail Validation":
        OnDemandOperationsModule.render_guardrail_validation()
    elif page == "Deployment Templates":
        OnDemandOperationsModule.render_deployment_templates()
    elif page == "Compute Right-Sizing":
        OnDemandOperationsModule.render_rightsizing()
    elif page == "Storage Re-Tiering":
        OnDemandOperationsModule.render_storage_tiering()
    elif page == "Auto-Scaling & Scheduling":
        OnDemandOperationsModule.render_autoscaling()
    elif page == "Patch Automation (SSM)":
        OnDemandOperationsModule2.render_patch_automation()
    elif page == "Drift Detection":
        OnDemandOperationsModule2.render_drift_detection()
    elif page == "Backup & Recovery":
        OnDemandOperationsModule2.render_backup_recovery()
    elif page == "Lifecycle Hooks":
        OnDemandOperationsModule2.render_lifecycle_hooks()
    elif page == "Idle Resource Detection":
        OnDemandOperationsModule2.render_idle_detection()
    elif page == "Continuous Availability":
        OnDemandOperationsModule2.render_continuous_availability()
    elif page == "Continuous Deployment":
        OnDemandOperationsModule2.render_continuous_deployment()
    elif page == "FinOps Overview":
        FinOpsModule.render_finops_overview()
    elif page == "Tag-Based Cost Tracking":
        FinOpsModule.render_tag_based_cost_tracking()
    elif page == "Budget Policy Enforcement":
        FinOpsModule.render_budget_policy_enforcement()
    elif page == "Forecasting & Chargebacks":
        FinOpsModule.render_forecasting_chargebacks()
    elif page == "Scheduled Infrastructure":
        FinOpsModule.render_scheduled_infrastructure_policies()
    elif page == "Spot Instance Orchestration":
        FinOpsModule.render_spot_instance_orchestration()
    elif page == "Cost Anomaly Detection":
        FinOpsModule.render_cost_anomaly_detection()
    elif page == "Reporting & Dashboards":
        FinOpsModule.render_reporting_dashboards()
    elif page == "PMO vs FMO":
        FinOpsModule.render_pmo_vs_fmo()
    elif page == "RI Recommendations":
        FinOpsModule.render_ri_recommendations()
    elif page == "Use Case Tracking":
        FinOpsModule.render_use_case_tracking()
    elif page == "Security & Compliance Overview":
        security_module = SecurityComplianceModule(demo_mode=st.session_state.demo_mode)
        security_module.render()
    elif page == "Module 07 Overview":
        AbstractionReusabilityModule.render_overview()
    elif page == "Composable Modules":
        AbstractionReusabilityModule.render_composable_modules()
    elif page == "App-Centric Packaging":
        AbstractionReusabilityModule.render_app_centric_packaging()
    elif page == "Parameterization & Defaults":
        AbstractionReusabilityModule.render_parameterization()
    elif page == "Multi-Environment Support":
        AbstractionReusabilityModule.render_multi_environment()
    elif page == "Lifecycle Management":
        AbstractionReusabilityModule.render_lifecycle_management()
    elif page == "Module 08 Overview":
        show_module_08_overview()
    elif page == "Cloud & On-Prem Provisioning":
        module = MultiCloudHybridModule()
        module._render_provisioning()
    elif page == "Unified Policy Framework":
        module = MultiCloudHybridModule()
        module._render_policy_framework()
    elif page == "Cloud-Specific Optimization":
        module = MultiCloudHybridModule()
        module._render_optimization()
    elif page == "Private+Public Connectivity":
        module = MultiCloudHybridModule()
        module._render_connectivity()
    elif page == "Global Environment Management":
        module = MultiCloudHybridModule()
        module._render_global_management()
    elif page == "Module 09 Overview":
        DeveloperExperienceModule.render_overview()
    elif page == "Governed Self-Service Portals":
        DeveloperExperienceModule.render_self_service_portals()
    elif page == "GitOps Integration":
        DeveloperExperienceModule.render_gitops_integration()
    elif page == "Drift Notification & Feedback Loop":
        DeveloperExperienceModule.render_drift_notification()
    elif page == "Documentation & Examples":
        DeveloperExperienceModule.render_documentation_examples()
    elif page == "InfraSecOps":
        DeveloperExperienceModule.render_infrasecops()
    elif page == "User Community":
        DeveloperExperienceModule.render_user_community()
    elif page == "Module 10 Overview":
        ObservabilityIntegrationModule.render_overview()
    elif page == "Standard Logging Stack via IaC":
        ObservabilityIntegrationModule.render_logging_stack()
    elif page == "Cloud Native Log/Metric Collection":
        ObservabilityIntegrationModule.render_metrics_collection()
    elif page == "Change Tracking & CMDB Sync":
        ObservabilityIntegrationModule.render_change_tracking()
    elif page == "Policy Violation Reporting":
        ObservabilityIntegrationModule.render_policy_violations()
    elif page == "Event Tools for Alerting":
        ObservabilityIntegrationModule.render_event_alerting()
    elif page == "Policy & Guardrails Overview":
        show_policy_guardrails_overview()
    elif page == "Policy as Code Engine":
        show_policy_as_code()
    elif page == "Cross-Cloud Policy Consistency":
        show_cross_cloud_policy()
    elif page == "Tag Policy Enforcement":
        show_tag_enforcement()
    elif page == "Naming & Placement Enforcement":
        show_naming_enforcement()
    elif page == "Quota Guardrails":
        show_quota_guardrails()
    elif page == "AI Assistant":
        show_ai_assistant()

def show_home_page():
    """Display home page"""
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📐 Design & Planning")
        st.markdown("""
        - Blueprint Definition
        - Tagging Standards
        - Naming Conventions
        - Artifact Versioning
        - IaC Module Registry
        - Design Validation
        """)
    
    with col2:
        st.markdown("### 🚀 Provisioning & Deployment")
        st.markdown("""
        - Multi-Cloud Provisioning
        - Environment Promotion
        - CI/CD Integration
        - Build Monitoring
        - Deployment Tracking
        - Pipeline Templates
        """)
    
    with col3:
        st.markdown("### ⚡ On-Demand Operations")
        st.markdown("""
        - API Provisioning
        - Guardrail Validation
        - Right-Sizing
        - Storage Tiering
        - Auto-Scaling
        - Patch Automation
        - Drift Detection
        - Backup Management
        - Lifecycle Hooks
        - Continuous Deployment
        """)
    
    st.markdown("---")
    
    # Second row of modules
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 💰 FinOps")
        st.markdown("""
        - Cost Tracking
        - Budget Enforcement
        - Forecasting
        - Chargebacks
        - Spot Orchestration
        - Anomaly Detection
        - RI Recommendations
        """)
    
    with col2:
        st.markdown("### 🔒 Security & Compliance")
        st.markdown("""
        - RBAC & Identity
        - Network Segmentation
        - Encryption Management
        - Secrets Management
        - Certificate Management
        - Audit Logging
        - Vulnerability Scanning
        """)
    
    with col3:
        st.markdown("### 🤖 AI Assistant")
        st.markdown("""
        - Architecture Review
        - Best Practices
        - Cost Optimization
        - Security Guidance
        - Troubleshooting
        - Documentation
        """)
    
    st.markdown("---")
    
    # Quick Stats
    st.markdown("### 📊 Platform Capabilities")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Cloud Services", "450+")
    with col2:
        st.metric("Active Deployments", "342")
    with col3:
        st.metric("IaC Templates", "500+")
    with col4:
        st.metric("Managed Resources", "1,547")
    
    st.markdown("---")
    
    # Current Mode Info
    st.markdown("### 🚀 Getting Started")
    
    if st.session_state.demo_mode:
        st.success("""
        **✅ Demo Mode Active** - You're exploring with sample data
        
        - All features available for testing
        - No cloud credentials required
        - Sample data represents real scenarios
        - Switch to Live Mode when ready to connect
        """)
        
        st.markdown("#### Try These Features:")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("📋 Browse 4 architecture blueprints")
            st.info("🏷️ View tagging policies")
            st.info("📛 Check naming conventions")
            st.info("☁️ Multi-cloud provisioning")
        with col2:
            st.info("🔄 Environment promotion workflow")
            st.info("🔧 CI/CD pipeline integration")
            st.info("📊 Build status monitoring")
            st.info("🤖 Chat with AI Assistant")
        with col3:
            st.info("⚡ On-demand provisioning API")
            st.info("📉 Right-sizing recommendations")
            st.info("💾 Storage re-tiering policies")
            st.info("🔍 Drift detection & remediation")
    else:
        st.warning("""
        **🟢 Live Mode Active** - Connected to cloud services
        
        - Configure cloud credentials in sidebar
        - All operations affect real resources
        - Review changes before applying
        - Audit logs are enabled
        """)

def show_design_planning_overview():
    """Display Design & Planning module overview"""
    
    st.markdown("## 📐 Design & Planning Framework")
    
    st.markdown("""
    Comprehensive tools for multi-cloud architecture design and planning. Ensure consistency,
    compliance, and best practices across AWS, Azure, GCP, and hybrid environments.
    """)
    
    st.markdown("---")
    
    # Module cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📋 Blueprint Definition")
        st.markdown("Define reusable architecture blueprints")
        st.markdown("- Infrastructure patterns")
        st.markdown("- Security baselines")
        st.markdown("- Network topologies")
        
        st.markdown("#### 🏷️ Tagging Standards")
        st.markdown("Establish tagging policies")
        st.markdown("- Mandatory tags")
        st.markdown("- Validation rules")
        st.markdown("- Cost allocation")
        
        st.markdown("#### 📛 Naming Conventions")
        st.markdown("Define naming standards")
        st.markdown("- Resource patterns")
        st.markdown("- Prefix/suffix rules")
        st.markdown("- Environment indicators")
    
    with col2:
        st.markdown("#### 📦 Image/Artifact Versioning")
        st.markdown("Manage container versions")
        st.markdown("- Registry management")
        st.markdown("- Version tracking")
        st.markdown("- Security scanning")
        
        st.markdown("#### 📚 IaC Module Registry")
        st.markdown("Centralized IaC modules")
        st.markdown("- Terraform modules")
        st.markdown("- CloudFormation templates")
        st.markdown("- Module versioning")
        
        st.markdown("#### ✅ Design-Time Validation")
        st.markdown("Validate before deployment")
        st.markdown("- Policy compliance")
        st.markdown("- Security checks")
        st.markdown("- Cost estimates")

def show_provisioning_deployment_overview():
    """Display Provisioning & Deployment module overview"""
    
    st.markdown("## 🚀 Provisioning & Deployment Framework")
    
    st.markdown("""
    End-to-end infrastructure provisioning and deployment management across multiple cloud providers.
    Automate deployments, manage environment promotions, and integrate with CI/CD pipelines.
    """)
    
    st.markdown("---")
    
    # Module cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ☁️ Multi-Cloud Provisioning")
        st.markdown("Deploy across cloud providers")
        st.markdown("- AWS, Azure, GCP support")
        st.markdown("- Unified deployment interface")
        st.markdown("- Cross-cloud governance")
        st.markdown("- Cost comparison tools")
        
        st.markdown("#### 🔄 Environment Promotion")
        st.markdown("Structured deployment pipeline")
        st.markdown("- Dev → Staging → Production")
        st.markdown("- Approval workflows")
        st.markdown("- Automated testing gates")
        st.markdown("- Rollback capabilities")
    
    with col2:
        st.markdown("#### 🔧 CI/CD Pipeline Integration")
        st.markdown("Connect with your CI/CD tools")
        st.markdown("- Jenkins integration")
        st.markdown("- GitHub Actions support")
        st.markdown("- GitLab CI/CD")
        st.markdown("- Azure DevOps")
        st.markdown("- Build monitoring")
        st.markdown("- Pipeline templates")
    
    st.markdown("---")
    
    # Key features
    st.markdown("### 🎯 Key Capabilities")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Automated Deployment**")
        st.markdown("""
        - One-click provisioning
        - Blueprint-based deployment
        - Infrastructure automation
        - Configuration management
        """)
    
    with col2:
        st.markdown("**Governance & Control**")
        st.markdown("""
        - Approval workflows
        - Policy enforcement
        - Audit trails
        - Change management
        """)
    
    with col3:
        st.markdown("**Monitoring & Insights**")
        st.markdown("""
        - Real-time status
        - Build analytics
        - Cost tracking
        - Performance metrics
        """)

def show_ondemand_operations_overview():
    """Display On-Demand Operations module overview"""
    
    st.markdown("## ⚡ On-Demand Provisioning & Operations Framework")
    
    st.markdown("""
    Intelligent resource management and automation platform. Optimize costs, ensure compliance,
    and maintain operational excellence through automated provisioning, right-sizing, and lifecycle management.
    """)
    
    st.markdown("---")
    
    # Module cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔌 On-Demand Provisioning API")
        st.markdown("Self-service infrastructure provisioning")
        st.markdown("- RESTful API endpoints")
        st.markdown("- Built-in guardrails")
        st.markdown("- Automatic validation")
        st.markdown("- Rate limiting & auth")
        
        st.markdown("#### 🛡️ Guardrail Validation")
        st.markdown("Pre-deployment policy enforcement")
        st.markdown("- Security checks")
        st.markdown("- Compliance validation")
        st.markdown("- Cost controls")
        st.markdown("- Tagging requirements")
        
        st.markdown("#### 📦 Deployment Templates")
        st.markdown("Pre-configured infrastructure patterns")
        st.markdown("- CloudFormation templates")
        st.markdown("- Terraform modules")
        st.markdown("- Right-sizing built-in")
        st.markdown("- Auto-scaling enabled")
        
        st.markdown("#### 📉 Compute Right-Sizing")
        st.markdown("AI-powered instance optimization")
        st.markdown("- Usage analysis")
        st.markdown("- Cost savings recommendations")
        st.markdown("- Automated resizing")
        st.markdown("- Performance monitoring")
        
        st.markdown("#### 💾 Storage Re-Tiering")
        st.markdown("Automated S3 lifecycle management")
        st.markdown("- Cost optimization")
        st.markdown("- Lifecycle policies")
        st.markdown("- Intelligent tiering")
        st.markdown("- Archive automation")
        
        st.markdown("#### ⏰ Auto-Scaling & Scheduling")
        st.markdown("Time-based resource management")
        st.markdown("- Business hours scaling")
        st.markdown("- Dev environment shutdown")
        st.markdown("- Cost optimization")
        st.markdown("- Demand-based scaling")
        
        st.markdown("#### 🔧 Patch Automation (SSM)")
        st.markdown("Automated patch management")
        st.markdown("- Maintenance windows")
        st.markdown("- Compliance tracking")
        st.markdown("- Automated updates")
        st.markdown("- Rollback capabilities")
    
    with col2:
        st.markdown("#### 🔍 Drift Detection & Remediation")
        st.markdown("Configuration compliance monitoring")
        st.markdown("- CloudFormation drift detection")
        st.markdown("- Automatic remediation")
        st.markdown("- Change tracking")
        st.markdown("- Compliance reporting")
        
        st.markdown("#### 💾 Backup & Recovery Management")
        st.markdown("Centralized backup orchestration")
        st.markdown("- Cloud backup integration (AWS Backup, Azure Backup, GCP backups)")
        st.markdown("- Cross-region replication")
        st.markdown("- RPO/RTO management")
        st.markdown("- Recovery testing")
        
        st.markdown("#### 🪝 Lifecycle Hooks")
        st.markdown("Automated lifecycle actions")
        st.markdown("- Launch initialization")
        st.markdown("- Termination cleanup")
        st.markdown("- Custom workflows")
        st.markdown("- Event-driven automation")
        
        st.markdown("#### 💤 Idle Resource Detection")
        st.markdown("Cost optimization through usage analysis")
        st.markdown("- Underutilized resources")
        st.markdown("- Idle detection")
        st.markdown("- Automatic termination")
        st.markdown("- Savings opportunities")
        
        st.markdown("#### 🔄 Continuous Availability")
        st.markdown("High availability monitoring")
        st.markdown("- Multi-AZ deployments")
        st.markdown("- Health checks")
        st.markdown("- Automatic failover")
        st.markdown("- SLA monitoring")
        
        st.markdown("#### 🚀 Continuous Deployment")
        st.markdown("Progressive delivery strategies")
        st.markdown("- Blue/green deployments")
        st.markdown("- Canary releases")
        st.markdown("- Automatic rollback")
        st.markdown("- Deployment gates")
    
    st.markdown("---")
    
    # Key capabilities
    st.markdown("### 🎯 Key Capabilities")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Cost Optimization**")
        st.markdown("""
        - Right-sizing recommendations
        - Storage tiering
        - Idle resource detection
        - Scheduled scaling
        - Savings tracking
        """)
    
    with col2:
        st.markdown("**Operational Excellence**")
        st.markdown("""
        - Automated patching
        - Drift remediation
        - Backup management
        - Lifecycle automation
        - Continuous monitoring
        """)
    
    with col3:
        st.markdown("**Security & Compliance**")
        st.markdown("""
        - Guardrail validation
        - Policy enforcement
        - Configuration compliance
        - Audit trails
        - Automated remediation
        """)
    
    # Call the actual overview rendering
    OnDemandOperationsModule.render_ondemand_overview()

def show_module_08_overview():
    """Display Module 08: Multi-Cloud & Hybrid Support overview"""
    
    st.markdown("## ☁️ Module 08: Multi-Cloud & Hybrid Support")
    
    st.markdown("""
    Comprehensive multi-cloud and hybrid cloud management platform. Unify policies across clouds,
    optimize workloads for each provider, and seamlessly connect on-premises to cloud environments.
    """)
    
    st.markdown("---")
    
    # Module cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🌐 Cloud & On-Prem Provisioning")
        st.markdown("Multi-cloud and hybrid provisioning")
        st.markdown("- AWS, Azure, GCP, Oracle, IBM support")
        st.markdown("- On-premises integration (VMware, Hyper-V)")
        st.markdown("- Hybrid connectivity (Direct Connect, ExpressRoute)")
        st.markdown("- Cloud bursting capabilities")
        st.markdown("- Unified IaC (Terraform, CloudFormation)")
        
        st.markdown("#### 📋 Unified Policy Framework")
        st.markdown("Cross-cloud policy management")
        st.markdown("- Policy translation engine")
        st.markdown("- Compliance mapping (ISO, SOC 2, PCI DSS, GDPR)")
        st.markdown("- Real-time enforcement")
        st.markdown("- Auto-remediation")
        st.markdown("- Comprehensive audit trails")
        
        st.markdown("#### ⚡ Cloud-Specific Optimization")
        st.markdown("Tailored optimization per cloud")
        st.markdown("- Multi-cloud cost analysis")
        st.markdown("- Performance tuning recommendations")
        st.markdown("- Resource right-sizing")
        st.markdown("- Cloud-native best practices")
        st.markdown("- Savings opportunity tracking")
    
    with col2:
        st.markdown("#### 🔗 Private + Public Connectivity")
        st.markdown("Secure hybrid networking")
        st.markdown("- Network topology design (Hub-Spoke, Mesh)")
        st.markdown("- Direct Connect / ExpressRoute / VPN")
        st.markdown("- Security zones & microsegmentation")
        st.markdown("- Global load balancing")
        st.markdown("- Traffic management & QoS")
        
        st.markdown("#### 🌍 Global Environment Management")
        st.markdown("Worldwide deployment orchestration")
        st.markdown("- Multi-region active-active/passive")
        st.markdown("- Global traffic distribution")
        st.markdown("- Data residency compliance")
        st.markdown("- Disaster recovery automation")
        st.markdown("- Latency-based routing")
    
    st.markdown("---")
    
    # Key capabilities
    st.markdown("### 🎯 Key Capabilities")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Multi-Cloud Strategy**")
        st.markdown("""
        - Unified provisioning
        - Cross-cloud policies
        - Cost comparison
        - Workload distribution
        - Vendor flexibility
        """)
    
    with col2:
        st.markdown("**Hybrid Integration**")
        st.markdown("""
        - On-premises connectivity
        - Data synchronization
        - Hybrid governance
        - Cloud bursting
        - Seamless migration
        """)
    
    with col3:
        st.markdown("**Global Scale**")
        st.markdown("""
        - Multi-region deployments
        - Data residency compliance
        - Global load balancing
        - DR automation
        - Latency optimization
        """)
    
    st.markdown("---")
    
    # Stats
    st.markdown("### 📊 Platform Coverage")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Cloud Providers", "6+", "+2")
    with col2:
        st.metric("Global Regions", "35+", "+5")
    with col3:
        st.metric("Unified Policies", "87", "+12")
    with col4:
        st.metric("Compliance Frameworks", "8", "+2")

def show_ai_assistant():
    """Display AI Assistant"""
    
    st.markdown("## 🤖 Claude AI Assistant")
    
    if not st.session_state.get('anthropic_api_key'):
        st.warning("⚠️ Anthropic API key not configured in Streamlit secrets.")
        st.info("""
        **Configure API key in Streamlit Cloud:**
        1. Go to your app settings
        2. Navigate to "Secrets" section
        3. Add the following:
        ```
        [anthropic]
        api_key = "your-api-key-here"
        ```
        4. Save and reboot the app
        
        Get your API key at: https://console.anthropic.com/
        """)
        return
    
    st.markdown("Ask Claude about multi-cloud architecture, best practices, and design patterns for AWS, Azure, and GCP.")
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about cloud architecture, AWS, Azure, GCP..."):
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Claude is thinking..."):
                try:
                    helper = AnthropicHelper(st.session_state.anthropic_api_key)
                    
                    context = f"""You are a multi-cloud architecture expert with deep knowledge of AWS, Azure, and Google Cloud Platform. 
                    Current mode: {'Demo Mode' if st.session_state.demo_mode else 'Live Mode'}
                    
                    User question: {prompt}
                    
                    Provide detailed, practical cloud architecture advice. Consider best practices across different cloud providers when relevant."""
                    
                    response = helper.get_completion(context)
                    st.markdown(response)
                    
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.info("Check your API key and try again.")
    
    # Clear chat
    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()

def show_policy_guardrails_overview():
    """Show Policy & Guardrails Overview"""
    module = PolicyGuardrailsModule()
    module.render_overview()

def show_policy_as_code():
    """Show Policy as Code Engine"""
    module = PolicyGuardrailsModule()
    module.render_policy_as_code()

def show_cross_cloud_policy():
    """Show Cross-Cloud Policy Consistency"""
    module = PolicyGuardrailsModule()
    module.render_cross_cloud_policy()

def show_tag_enforcement():
    """Show Tag Policy Enforcement"""
    module = PolicyGuardrailsModule()
    module.render_tag_enforcement()

def show_naming_enforcement():
    """Show Naming & Placement Enforcement"""
    module = PolicyGuardrailsModule()
    module.render_naming_enforcement()

def show_quota_guardrails():
    """Show Quota Guardrails"""
    module = PolicyGuardrailsModule()
    module.render_quota_guardrails()

if __name__ == "__main__":
    main()