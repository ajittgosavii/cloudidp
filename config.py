"""Configuration and Session State Management"""

import streamlit as st

def initialize_session_state():
    """Initialize all session state variables"""
    
    # Core application state
    if 'demo_mode' not in st.session_state:
        st.session_state.demo_mode = True  # Default to Demo Mode
    
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"
    
    # AWS Configuration
    if 'aws_region' not in st.session_state:
        st.session_state.aws_region = "us-east-1"
    
    if 'aws_account' not in st.session_state:
        st.session_state.aws_account = ""
    
    # Anthropic API
    if 'anthropic_api_key' not in st.session_state:
        st.session_state.anthropic_api_key = ""
    
    # Chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
