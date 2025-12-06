"""
Cloud Infrastructure Development Platform - Enterprise Multi-Account Cloud Management
Minimal Light Theme - Maximum Compatibility
"""

import streamlit as st
from datetime import datetime
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from config_settings import AppConfig
from core_session_manager import SessionManager
from components_navigation import Navigation
from components_sidebar import GlobalSidebar

# Page configuration
st.set_page_config(
    page_title="Cloud Infrastructure Development Platform",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================================================
# MINIMAL LIGHT THEME - MAXIMUM COMPATIBILITY
# ==================================================================================
st.markdown("""
<style>
/* ===== MINIMAL CLEAN THEME ===== */

/* Main background - light */
.main {
    background-color: #F5F7FA !important;
}

/* All text dark by default */
body, p, span, div, label {
    color: #2C3E50 !important;
}

/* Headers */
h1, h2, h3, h4, h5, h6 {
    color: #2E86DE !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #FFFFFF !important;
}

/* Buttons */
.stButton button {
    background-color: #2E86DE !important;
    color: white !important;
    border-radius: 6px !important;
    padding: 10px 24px !important;
}

.stButton button:hover {
    background-color: #0652DD !important;
}

/* Inputs and Dropdowns - WHITE with DARK text */
input, textarea, select {
    background-color: white !important;
    color: #2C3E50 !important;
    border: 1px solid #E0E0E0 !important;
}

/* Dropdown options */
div[data-baseweb="select"],
div[role="listbox"],
[role="option"] {
    background-color: white !important;
    color: #2C3E50 !important;
}

/* Tables */
table {
    background-color: white !important;
}

thead tr th {
    background-color: #2E86DE !important;
    color: white !important;
}

tbody tr td {
    color: #2C3E50 !important;
}

/* Tabs */
.stTabs [data-baseweb="tab"] {
    color: #2C3E50 !important;
}

.stTabs [aria-selected="true"] {
    color: #2E86DE !important;
    border-bottom: 3px solid #2E86DE !important;
}

/* Metrics - let custom components handle their own styling */
[data-testid="stMetric"] {
    background-color: transparent !important;
}
</style>
""", unsafe_allow_html=True)
# ==================================================================================
# END MINIMAL THEME
# ==================================================================================

# Header
st.markdown("""
<div style="background: linear-gradient(135deg, #2E86DE 0%, #0652DD 100%); padding: 20px; border-radius: 10px; margin-bottom: 20px; text-align: center;">
    <h1 style="color: white !important; margin: 0; font-weight: 600;">☁️ Cloud Infrastructure Development Platform</h1>
    <p style="color: white !important; margin: 5px 0 0 0; font-size: 16px;">Enterprise Multi-Account Cloud Management</p>
</div>
""", unsafe_allow_html=True)

def main():
    """Main application entry point"""
    
    # Initialize session
    SessionManager.initialize()
    
    # Render global sidebar
    GlobalSidebar.render()
    
    # Render main navigation
    Navigation.render()
    
    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    with col2:
        st.caption(f"🔗 Connected Accounts: {SessionManager.get_active_account_count()}")
    with col3:
        st.caption("☁️ Cloud Infrastructure Development Platform")

if __name__ == "__main__":
    main()