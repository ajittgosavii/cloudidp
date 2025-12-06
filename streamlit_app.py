"""
Cloud Infrastructure Development Platform - Enterprise Multi-Account Cloud Management
Simple Blue Theme - Clean & Professional
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
# SIMPLE BLUE THEME - CLEAN & PROFESSIONAL
# ==================================================================================
st.markdown("""
<style>
/* ===== GLOBAL THEME ===== */
:root {
    --primary-color: #2E86DE;
    --secondary-color: #0652DD;
    --background-color: #FFFFFF;
    --text-color: #000000;
    --border-color: #E0E0E0;
}

/* Main app background - WHITE */
.main {
    background-color: white !important;
}

/* All text - BLACK (except metrics which will be handled separately) */
body {
    color: black !important;
}

/* Most text elements - BLACK */
p:not([data-testid*="stMetric"] *),
span:not([data-testid*="stMetric"] *),
div:not([data-testid*="stMetric"] *):not([style*="background"]),
label:not([data-testid*="stMetric"] *) {
    color: black !important;
}

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] {
    background-color: #F5F7FA !important;
}

[data-testid="stSidebar"] * {
    color: black !important;
}

/* ===== HEADERS ===== */
h1, h2, h3 {
    color: #2E86DE !important;
}

/* ===== BUTTONS ===== */
button {
    background-color: #2E86DE !important;
    color: white !important;
    border: none !important;
    border-radius: 4px !important;
    padding: 8px 16px !important;
    font-weight: 500 !important;
}

button:hover {
    background-color: #0652DD !important;
    color: white !important;
}

/* ===== DROPDOWNS & SELECTS ===== */
/* Dropdown labels */
.stSelectbox label,
.stMultiSelect label,
.stTextInput label,
.stNumberInput label,
.stTextArea label {
    color: black !important;
    font-weight: 500 !important;
}

/* Dropdown options text - BLACK */
div[data-baseweb="select"] [role="option"],
div[data-baseweb="select"] li,
[role="option"] {
    color: black !important;
    background-color: white !important;
}

/* Dropdown selected value - BLACK */
div[data-baseweb="select"] > div {
    color: black !important;
    background-color: white !important;
}

/* Multiselect tags */
div[data-baseweb="tag"] {
    background-color: #2E86DE !important;
}

div[data-baseweb="tag"] span {
    color: white !important;
}

/* ===== INPUT FIELDS ===== */
input, textarea {
    background-color: white !important;
    color: black !important;
    border: 1px solid #E0E0E0 !important;
}

/* ===== TABS ===== */
.stTabs [data-baseweb="tab-list"] {
    background-color: white !important;
}

.stTabs [data-baseweb="tab"] {
    color: black !important;
}

.stTabs [aria-selected="true"] {
    color: #2E86DE !important;
    border-bottom: 2px solid #2E86DE !important;
}

/* ===== METRICS - FORCE WHITE TEXT IN DARK BOXES ===== */

/* Metric labels - MAXIMUM SPECIFICITY */
[data-testid="stMetricLabel"],
[data-testid="stMetric"] [data-testid="stMetricLabel"],
div[data-testid="stMetric"] label,
div[data-testid="stMetric"] [data-testid="stMetricLabel"],
[data-testid="metric-container"] label {
    color: white !important;
    font-weight: 500 !important;
}

/* Metric values - MAXIMUM SPECIFICITY */
[data-testid="stMetricValue"],
[data-testid="stMetric"] [data-testid="stMetricValue"],
div[data-testid="stMetric"] > div > div,
div[data-testid="stMetric"] [data-testid="stMetricValue"],
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: white !important;
    font-weight: 600 !important;
}

/* Metric deltas */
[data-testid="stMetricDelta"],
[data-testid="stMetric"] [data-testid="stMetricDelta"] {
    color: #B0B0B0 !important;
}

/* ALL elements inside metrics - WHITE */
[data-testid="stMetric"] *,
[data-testid="stMetric"] p,
[data-testid="stMetric"] span,
[data-testid="stMetric"] div,
[data-testid="stMetric"] label,
div[data-testid="stMetric"] > div > div > *,
div[data-testid="metric-container"] *,
div[data-testid="metric-container"] p,
div[data-testid="metric-container"] span,
div[data-testid="metric-container"] div,
div[data-testid="metric-container"] label {
    color: white !important;
}

/* Columns containing metrics */
div[data-testid="column"] [data-testid="stMetric"] *,
div[data-testid="column"] [data-testid="stMetric"] p,
div[data-testid="column"] [data-testid="stMetric"] span,
div[data-testid="column"] [data-testid="stMetric"] div,
div[data-testid="column"] [data-testid="stMetric"] label {
    color: white !important;
}

/* Metric containers */
.stMetric,
div[data-testid="stMetric"] {
    background-color: transparent !important;
}

/* For any container with a dark background - force white text */
div[style*="background-color: rgb(33"],
div[style*="background-color: rgb(44"],
div[style*="background-color: rgb(55"],
div[style*="background-color: #1"],
div[style*="background-color: #2"],
div[style*="background-color: #3"] {
    color: white !important;
}

div[style*="background-color: rgb(33"] *,
div[style*="background-color: rgb(44"] *,
div[style*="background-color: rgb(55"] *,
div[style*="background-color: #1"] *,
div[style*="background-color: #2"] *,
div[style*="background-color: #3"] * {
    color: white !important;
}

/* ===== INFO/WARNING/ERROR BOXES ===== */
.stAlert {
    background-color: white !important;
    border-left: 4px solid #2E86DE !important;
}

/* ===== DATAFRAMES ===== */
.stDataFrame {
    background-color: white !important;
}

table {
    background-color: white !important;
}

th {
    background-color: #2E86DE !important;
    color: white !important;
}

td {
    color: black !important;
}

/* ===== EXPANDERS ===== */
.streamlit-expanderHeader {
    background-color: #F5F7FA !important;
    color: black !important;
}

/* ===== RADIO & CHECKBOX ===== */
.stRadio label,
.stCheckbox label {
    color: black !important;
}

/* ===== CLEAN BORDERS ===== */
.stSelectbox > div,
.stMultiSelect > div,
.stTextInput > div,
.stNumberInput > div {
    border-radius: 4px !important;
}
</style>
""", unsafe_allow_html=True)
# ==================================================================================
# END SIMPLE BLUE THEME
# ==================================================================================

# Simple header - centered
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
    
    # Simple footer
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
