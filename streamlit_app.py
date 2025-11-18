"""
AWS Design & Planning Platform
Streamlit Cloud Compatible - Flat File Structure
"""

import streamlit as st
from design_planning import DesignPlanningModule
from config import initialize_session_state
from anthropic_helper import AnthropicHelper

# Page configuration
st.set_page_config(
    page_title="AWS Design & Planning Platform",
    page_icon="🏗️",
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
    st.markdown('<div class="main-header">🏗️ AWS Design & Planning Platform</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Enterprise Cloud Architecture & Governance Framework</div>', unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.image("https://a0.awsstatic.com/libra-css/images/logos/aws_logo_smile_1200x630.png", width=200)
        st.markdown("---")
        
        # ============= LIVE/DEMO MODE TOGGLE =============
        st.markdown("### 🔄 Operation Mode")
        mode = st.radio(
            "Select Mode:",
            ["Demo Mode", "Live Mode"],
            index=0,  # Demo Mode is default
            help="Demo Mode: Use sample data (no AWS credentials)\nLive Mode: Connect to real AWS services"
        )
        
        # Update session state based on selection
        st.session_state.demo_mode = (mode == "Demo Mode")
        
        # Display mode indicator with clear visual feedback
        if st.session_state.demo_mode:
            st.markdown(
                '<div class="mode-indicator demo-mode">📋 DEMO MODE ACTIVE</div>',
                unsafe_allow_html=True
            )
            st.info("✓ Using sample data\n\n✓ No AWS credentials needed\n\n✓ Safe to explore all features")
        else:
            st.markdown(
                '<div class="mode-indicator live-mode">🟢 LIVE MODE ACTIVE</div>',
                unsafe_allow_html=True
            )
            st.warning("⚠️ Connected to AWS\n\n⚠️ Real data will be used\n\n⚠️ Actions may affect resources")
        
        st.markdown("---")
        
        # Navigation
        st.markdown("### 📋 Navigation")
        page = st.selectbox(
            "Select Module:",
            [
                "Home",
                "Design & Planning Overview",
                "Blueprint Definition",
                "Tagging Standards",
                "Naming Conventions",
                "Image/Artifact Versioning",
                "IaC Module Registry",
                "Design-Time Validation",
                "AI Assistant"
            ]
        )
        
        st.markdown("---")
        
        # AWS Configuration (Live Mode Only)
        if not st.session_state.demo_mode:
            st.markdown("### ⚙️ AWS Configuration")
            with st.expander("AWS Settings", expanded=False):
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
                    st.success("✅ AWS Account configured")
        
        # Anthropic API Configuration
        st.markdown("### 🤖 Claude AI Configuration")
        with st.expander("API Settings", expanded=False):
            api_key = st.text_input(
                "Anthropic API Key:",
                type="password",
                help="Get your API key from https://console.anthropic.com/"
            )
            if api_key:
                st.session_state.anthropic_api_key = api_key
                st.success("✅ API Key configured")
            else:
                st.info("ℹ️ API key needed for AI features")
        
        st.markdown("---")
        st.caption("v1.0.0 | Built for AWS Enterprise Architecture")
    
    # Main content area - Route to appropriate page
    if page == "Home":
        show_home_page()
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
        st.markdown("### 🔒 Compliance & Security")
        st.markdown("""
        - PCI DSS Compliance
        - HIPAA Requirements
        - GDPR Controls
        - Security Baselines
        - Audit Trails
        - Risk Assessment
        """)
    
    with col3:
        st.markdown("### 🤖 AI-Powered")
        st.markdown("""
        - Claude AI Assistant
        - Automated Reviews
        - Documentation Gen
        - Best Practices
        - Architecture Help
        - Code Analysis
        """)
    
    st.markdown("---")
    
    # Quick Stats
    st.markdown("### 📊 Platform Capabilities")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("AWS Services", "150+")
    with col2:
        st.metric("Compliance Frameworks", "12+")
    with col3:
        st.metric("IaC Templates", "500+")
    with col4:
        st.metric("Validation Rules", "1000+")
    
    st.markdown("---")
    
    # Current Mode Info
    st.markdown("### 🚀 Getting Started")
    
    if st.session_state.demo_mode:
        st.success("""
        **✅ Demo Mode Active** - You're exploring with sample data
        
        - All features available for testing
        - No AWS credentials required
        - Sample data represents real scenarios
        - Switch to Live Mode when ready to connect
        """)
        
        st.markdown("#### Try These Features:")
        col1, col2 = st.columns(2)
        with col1:
            st.info("📋 Browse 4 architecture blueprints")
            st.info("🏷️ View tagging policies")
            st.info("📛 Check naming conventions")
        with col2:
            st.info("📦 Explore 87+ IaC modules")
            st.info("✅ Run design validation")
            st.info("🤖 Chat with AI Assistant")
    else:
        st.warning("""
        **🟢 Live Mode Active** - Connected to AWS services
        
        - Configure AWS credentials in sidebar
        - All operations affect real resources
        - Review changes before applying
        - Audit logs are enabled
        """)

def show_design_planning_overview():
    """Display Design & Planning module overview"""
    
    st.markdown("## 📐 Design & Planning Framework")
    
    st.markdown("""
    Comprehensive tools for AWS architecture design and planning. Ensure consistency,
    compliance, and best practices across your cloud environment.
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

def show_ai_assistant():
    """Display AI Assistant"""
    
    st.markdown("## 🤖 Claude AI Assistant")
    
    if not st.session_state.get('anthropic_api_key'):
        st.warning("⚠️ Configure your Anthropic API key in the sidebar to use AI features.")
        st.info("""
        **Get your API key:**
        1. Visit https://console.anthropic.com/
        2. Sign up or log in
        3. Go to API Keys section
        4. Create a new key
        5. Enter it in the sidebar
        """)
        return
    
    st.markdown("Ask Claude about AWS architecture, best practices, and design patterns.")
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about AWS architecture..."):
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Claude is thinking..."):
                try:
                    helper = AnthropicHelper(st.session_state.anthropic_api_key)
                    
                    context = f"""You are an AWS architecture expert. 
                    Current mode: {'Demo Mode' if st.session_state.demo_mode else 'Live Mode'}
                    
                    User question: {prompt}
                    
                    Provide detailed, practical AWS advice."""
                    
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

if __name__ == "__main__":
    main()
