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

/* ===== CRITICAL: NO GLOBAL BLACK RULE ===== */
/* We do NOT set a global black color rule because it conflicts with metrics */
/* Instead, we set black on specific elements only */

/* Set black on non-metric elements */
.main > div:not([data-testid="stMetric"]),
.main > div:not([data-testid="stMetric"]) > div:not([data-testid="stMetric"]),
.main > div:not([data-testid="stMetric"]) > div:not([data-testid="stMetric"]) > p:not([data-testid*="stMetric"]),
.main > div:not([data-testid="stMetric"]) > div:not([data-testid="stMetric"]) > span:not([data-testid*="stMetric"]) {
    color: black;
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

/* ================================
   NUCLEAR OPTION - ULTRA AGGRESSIVE METRICS CSS
   Uses EVERY possible selector with maximum !important
   ================================ */

/* Global override - metrics get white text NO MATTER WHAT */
[data-testid="stMetric"],
[data-testid="stMetric"] *,
[data-testid="stMetric"] > *,
[data-testid="stMetric"] > * > *,
[data-testid="stMetric"] > * > * > *,
[data-testid="stMetric"] > * > * > * > *,
[data-testid="stMetric"] div,
[data-testid="stMetric"] p,
[data-testid="stMetric"] span,
[data-testid="stMetric"] label,
[data-testid="stMetric"] h1,
[data-testid="stMetric"] h2,
[data-testid="stMetric"] h3,
[data-testid="stMetric"] h4,
[data-testid="stMetric"] h5,
[data-testid="stMetric"] h6,
div[data-testid="stMetric"],
div[data-testid="stMetric"] *,
div[data-testid="stMetric"] > *,
div[data-testid="stMetric"] > * > *,
div[data-testid="stMetric"] > * > * > *,
div[data-testid="stMetric"] div,
div[data-testid="stMetric"] p,
div[data-testid="stMetric"] span,
div[data-testid="stMetric"] label {
    color: white !important;
    fill: white !important;
}

/* Metric labels - EVERY possible selector */
[data-testid="stMetricLabel"],
div[data-testid="stMetricLabel"],
[data-testid="stMetric"] [data-testid="stMetricLabel"],
div[data-testid="stMetric"] [data-testid="stMetricLabel"],
div[data-testid="stMetric"] div[data-testid="stMetricLabel"],
[data-testid="metric-container"] [data-testid="stMetricLabel"],
.stMetric [data-testid="stMetricLabel"],
[class*="stMetric"] [data-testid="stMetricLabel"] {
    color: white !important;
    fill: white !important;
}

/* Metric values - EVERY possible selector */
[data-testid="stMetricValue"],
div[data-testid="stMetricValue"],
[data-testid="stMetric"] [data-testid="stMetricValue"],
div[data-testid="stMetric"] [data-testid="stMetricValue"],
div[data-testid="stMetric"] div[data-testid="stMetricValue"],
[data-testid="metric-container"] [data-testid="stMetricValue"],
.stMetric [data-testid="stMetricValue"],
[class*="stMetric"] [data-testid="stMetricValue"] {
    color: white !important;
    fill: white !important;
    font-weight: 600 !important;
}

/* Metric deltas */
[data-testid="stMetricDelta"],
div[data-testid="stMetricDelta"],
[data-testid="stMetric"] [data-testid="stMetricDelta"],
div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
    color: #B0B0B0 !important;
    fill: #B0B0B0 !important;
}

/* Column containers with metrics */
div[data-testid="column"] [data-testid="stMetric"],
div[data-testid="column"] [data-testid="stMetric"] *,
div[data-testid="column"] div[data-testid="stMetric"],
div[data-testid="column"] div[data-testid="stMetric"] * {
    color: white !important;
    fill: white !important;
}

/* Vertical blocks with metrics */
div[data-testid="stVerticalBlock"] [data-testid="stMetric"],
div[data-testid="stVerticalBlock"] [data-testid="stMetric"] *,
div[data-testid="stVerticalBlock"] div[data-testid="stMetric"],
div[data-testid="stVerticalBlock"] div[data-testid="stMetric"] * {
    color: white !important;
    fill: white !important;
}

/* Horizontal blocks with metrics */
div[data-testid="stHorizontalBlock"] [data-testid="stMetric"],
div[data-testid="stHorizontalBlock"] [data-testid="stMetric"] *,
div[data-testid="stHorizontalBlock"] div[data-testid="stMetric"],
div[data-testid="stHorizontalBlock"] div[data-testid="stMetric"] * {
    color: white !important;
    fill: white !important;
}

/* Element containers with metrics */
div[class*="element-container"] [data-testid="stMetric"],
div[class*="element-container"] [data-testid="stMetric"] *,
div[class*="element-container"] div[data-testid="stMetric"],
div[class*="element-container"] div[data-testid="stMetric"] * {
    color: white !important;
    fill: white !important;
}

/* Any div with style attribute containing background */
div[style*="background"] [data-testid="stMetric"],
div[style*="background"] [data-testid="stMetric"] *,
div[style*="background"] div[data-testid="stMetric"],
div[style*="background"] div[data-testid="stMetric"] * {
    color: white !important;
    fill: white !important;
}

/* Dark background colors - comprehensive list */
div[style*="background-color: rgb(0"],
div[style*="background-color: rgb(1"],
div[style*="background-color: rgb(2"],
div[style*="background-color: rgb(3"],
div[style*="background-color: rgb(4"],
div[style*="background-color: rgb(5"],
div[style*="background-color: #0"],
div[style*="background-color: #1"],
div[style*="background-color: #2"],
div[style*="background-color: #3"],
div[style*="background: rgb(0"],
div[style*="background: rgb(1"],
div[style*="background: rgb(2"],
div[style*="background: rgb(3"],
div[style*="background: rgb(4"],
div[style*="background: rgb(5"],
div[style*="background: #0"],
div[style*="background: #1"],
div[style*="background: #2"],
div[style*="background: #3"] {
    color: white !important;
}

div[style*="background-color: rgb(0"] *,
div[style*="background-color: rgb(1"] *,
div[style*="background-color: rgb(2"] *,
div[style*="background-color: rgb(3"] *,
div[style*="background-color: rgb(4"] *,
div[style*="background-color: rgb(5"] *,
div[style*="background-color: #0"] *,
div[style*="background-color: #1"] *,
div[style*="background-color: #2"] *,
div[style*="background-color: #3"] *,
div[style*="background: rgb(0"] *,
div[style*="background: rgb(1"] *,
div[style*="background: rgb(2"] *,
div[style*="background: rgb(3"] *,
div[style*="background: rgb(4"] *,
div[style*="background: rgb(5"] *,
div[style*="background: #0"] *,
div[style*="background: #1"] *,
div[style*="background: #2"] *,
div[style*="background: #3"] * {
    color: white !important;
    fill: white !important;
}

/* Override ANY computed black color */
[style*="color: rgb(0, 0, 0)"][data-testid*="stMetric"],
[style*="color: rgb(0,0,0)"][data-testid*="stMetric"],
[style*="color: black"][data-testid*="stMetric"],
[style*="color: #000"][data-testid*="stMetric"],
[style*="color:#000"][data-testid*="stMetric"] {
    color: white !important;
}

/* Force white on common class patterns */
.stMetric,
.stMetric *,
div.stMetric,
div.stMetric *,
[class*="Metric"],
[class*="Metric"] *,
[class*="metric"],
[class*="metric"] * {
    color: white !important;
    fill: white !important;
}

/* Streamlit's CSS modules - target them directly */
div[class^="st-"] [data-testid="stMetric"],
div[class^="st-"] [data-testid="stMetric"] *,
div[class*="st-"] [data-testid="stMetric"],
div[class*="st-"] [data-testid="stMetric"] * {
    color: white !important;
    fill: white !important;
}

/* Last resort - target by position in DOM */
div > div > div > [data-testid="stMetric"],
div > div > div > [data-testid="stMetric"] *,
div > div > div > div > [data-testid="stMetric"],
div > div > div > div > [data-testid="stMetric"] * {
    color: white !important;
    fill: white !important;
}

/* ULTIMATE NUCLEAR OPTION - if nothing else works */
* [data-testid="stMetric"],
* [data-testid="stMetric"] *,
* div[data-testid="stMetric"],
* div[data-testid="stMetric"] * {
    color: white !important;
    fill: white !important;
}

/* ===== END NUCLEAR METRICS CSS ===== */

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
