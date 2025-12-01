"""
Configuration module for AWS Design & Planning Platform
"""

import streamlit as st

def initialize_session_state():
    """Initialize all session state variables"""
    
    # Core settings
    if 'demo_mode' not in st.session_state:
        st.session_state.demo_mode = True  # Default to demo mode
    
    if 'aws_region' not in st.session_state:
        st.session_state.aws_region = 'us-east-1'
    
    if 'aws_account' not in st.session_state:
        st.session_state.aws_account = ''
    
    if 'anthropic_api_key' not in st.session_state:
        st.session_state.anthropic_api_key = ''
    
    # Module-specific states
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'selected_blueprint' not in st.session_state:
        st.session_state.selected_blueprint = None
    
    if 'deployment_status' not in st.session_state:
        st.session_state.deployment_status = {}
    
    if 'promotion_queue' not in st.session_state:
        st.session_state.promotion_queue = []

# Application constants
APP_VERSION = "1.0.0"
APP_NAME = "AWS Design & Planning Platform"

# AWS Regions
AWS_REGIONS = [
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2",
    "eu-west-1",
    "eu-west-2",
    "eu-central-1",
    "ap-southeast-1",
    "ap-southeast-2",
    "ap-northeast-1"
]

# Compliance Frameworks
COMPLIANCE_FRAMEWORKS = [
    "PCI DSS",
    "HIPAA",
    "GDPR",
    "SOC 2",
    "ISO 27001",
    "FedRAMP",
    "NIST",
    "CIS"
]

# Cloud Providers
CLOUD_PROVIDERS = [
    "AWS"
]

# Environments
ENVIRONMENTS = [
    "Development",
    "Staging",
    "Production",
    "DR"
]
