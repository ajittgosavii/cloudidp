"""
Cloud Infrastructure Development Platform - Enterprise Multi-Account Cloud Management
Clean Light Theme - Dark Text Visible Everywhere
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
# CLEAN LIGHT THEME - DARK TEXT VISIBLE EVERYWHERE
# ==================================================================================
st.markdown("""
<style>
/* ===== CLEAN LIGHT THEME ===== */
:root {
    --primary-color: #2E86DE;
    --secondary-color: #0652DD;
    --background-color: #F5F7FA;
    --text-color: #2C3E50;
    --border-color: #E0E0E0;
}

/* ===== MAIN BACKGROUND - LIGHT GRAY ===== */
.main {
    background-color: #F5F7FA !important;
}

/* ===== ALL TEXT IS DARK (VISIBLE!) ===== */
body, p, span, div, label, h1, h2, h3, h4, h5, h6 {
    color: #2C3E50 !important;
}

/* ===== METRICS - DARK TEXT ON WHITE CARDS ===== */
[data-testid="stMetric"],
[data-testid="stMetricLabel"],
[data-testid="stMetricValue"],
[data-testid="stMetricDelta"] {
    background-color: white !important;
    color: #2C3E50 !important;
}

[data-testid="stMetric"] {
    background-color: white !important;
    border: 1px solid #E0E0E0 !important;
    border-radius: 8px !important;
    padding: 16px !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
}

[data-testid="stMetric"] * {
    color: #2C3E50 !important;
}

/* ===== SIDEBAR - LIGHT ===== */
[data-testid="stSidebar"] {
    background-color: white !important;
    border-right: 1px solid #E0E0E0 !important;
}

[data-testid="stSidebar"] * {
    color: #2C3E50 !important;
}

/* ===== HEADERS - BLUE ===== */
h1 {
    color: #2E86DE !important;
    font-weight: 600 !important;
}

h2 {
    color: #2E86DE !important;
    font-weight: 600 !important;
}

h3 {
    color: #2C3E50 !important;
    font-weight: 600 !important;
}

/* ===== BUTTONS - BLUE ===== */
button[kind="primary"],
button[kind="secondary"],
.stButton button {
    background-color: #2E86DE !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 10px 24px !important;
    font-weight: 500 !important;
    transition: all 0.2s !important;
}

button[kind="primary"]:hover,
button[kind="secondary"]:hover,
.stButton button:hover {
    background-color: #0652DD !important;
    box-shadow: 0 4px 8px rgba(46, 134, 222, 0.3) !important;
}

/* ===== INPUTS & DROPDOWNS - WHITE WITH DARK TEXT ===== */
input, textarea, select {
    background-color: white !important;
    color: #2C3E50 !important;
    border: 1px solid #E0E0E0 !important;
    border-radius: 6px !important;
}

/* Dropdown container */
div[data-baseweb="select"],
div[data-baseweb="popover"] {
    background-color: white !important;
    color: #2C3E50 !important;
}

/* Dropdown options - DARK TEXT */
div[data-baseweb="select"] [role="option"],
div[data-baseweb="select"] li,
[role="option"],
[role="listbox"] li {
    background-color: white !important;
    color: #2C3E50 !important;
}

div[data-baseweb="select"] [role="option"]:hover,
[role="option"]:hover {
    background-color: #F5F7FA !important;
    color: #2E86DE !important;
}

/* Dropdown selected value - DARK TEXT */
div[data-baseweb="select"] > div,
div[data-baseweb="select"] span {
    color: #2C3E50 !important;
    background-color: white !important;
}

/* Input labels */
.stSelectbox label,
.stMultiSelect label,
.stTextInput label,
.stNumberInput label,
.stTextArea label,
.stDateInput label,
.stTimeInput label {
    color: #2C3E50 !important;
    font-weight: 500 !important;
}

/* Multiselect tags */
div[data-baseweb="tag"] {
    background-color: #2E86DE !important;
    border-radius: 4px !important;
}

div[data-baseweb="tag"] span {
    color: white !important;
}

/* ===== TABS - CLEAN ===== */
.stTabs [data-baseweb="tab-list"] {
    background-color: white !important;
    border-bottom: 1px solid #E0E0E0 !important;
}

.stTabs [data-baseweb="tab"] {
    color: #2C3E50 !important;
    padding: 12px 24px !important;
    font-weight: 500 !important;
}

.stTabs [aria-selected="true"] {
    color: #2E86DE !important;
    border-bottom: 3px solid #2E86DE !important;
    background-color: #F5F7FA !important;
}

.stTabs [data-baseweb="tab"]:hover {
    background-color: #F5F7FA !important;
}

/* ===== DATAFRAMES & TABLES ===== */
.stDataFrame,
.dataframe {
    background-color: white !important;
    border: 1px solid #E0E0E0 !important;
    border-radius: 6px !important;
}

table {
    background-color: white !important;
}

thead tr th {
    background-color: #2E86DE !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 12px !important;
}

tbody tr td {
    color: #2C3E50 !important;
    padding: 10px !important;
    border-bottom: 1px solid #E0E0E0 !important;
}

tbody tr:hover {
    background-color: #F5F7FA !important;
}

/* ===== CHARTS - WHITE BACKGROUND ===== */
.stVegaLiteChart,
.stPlotlyChart,
.stDeckGlJsonChart {
    background-color: white !important;
    border: 1px solid #E0E0E0 !important;
    border-radius: 6px !important;
    padding: 16px !important;
}

/* ===== INFO/WARNING/ERROR BOXES ===== */
.stAlert {
    background-color: white !important;
    border-left: 4px solid #2E86DE !important;
    border-radius: 6px !important;
    padding: 16px !important;
    color: #2C3E50 !important;
}

.stSuccess {
    border-left-color: #10B981 !important;
}

.stWarning {
    border-left-color: #F59E0B !important;
}

.stError {
    border-left-color: #EF4444 !important;
}

.stInfo {
    border-left-color: #2E86DE !important;
}

/* ===== EXPANDERS ===== */
.streamlit-expanderHeader {
    background-color: white !important;
    color: #2C3E50 !important;
    border: 1px solid #E0E0E0 !important;
    border-radius: 6px !important;
    font-weight: 500 !important;
}

.streamlit-expanderHeader:hover {
    background-color: #F5F7FA !important;
}

/* ===== RADIO & CHECKBOX ===== */
.stRadio label,
.stCheckbox label {
    color: #2C3E50 !important;
}

/* ===== CODE BLOCKS ===== */
.stCodeBlock,
pre,
code {
    background-color: #F8F9FA !important;
    color: #2C3E50 !important;
    border: 1px solid #E0E0E0 !important;
    border-radius: 6px !important;
}

/* ===== SPINNER ===== */
.stSpinner > div {
    border-top-color: #2E86DE !important;
}

/* ===== PROGRESS BAR ===== */
.stProgress > div > div {
    background-color: #2E86DE !important;
}

/* ===== FILE UPLOADER ===== */
[data-testid="stFileUploader"] {
    background-color: white !important;
    border: 2px dashed #E0E0E0 !important;
    border-radius: 6px !important;
}

[data-testid="stFileUploader"]:hover {
    border-color: #2E86DE !important;
}

/* ===== SLIDER ===== */
.stSlider {
    color: #2C3E50 !important;
}

/* ===== DOWNLOAD BUTTON ===== */
.stDownloadButton button {
    background-color: #10B981 !important;
}

.stDownloadButton button:hover {
    background-color: #059669 !important;
}

/* ===== MARKDOWN ===== */
.stMarkdown {
    color: #2C3E50 !important;
}

/* ===== CAPTIONS ===== */
.caption {
    color: #6B7280 !important;
    font-size: 14px !important;
}

/* ===== LINKS ===== */
a {
    color: #2E86DE !important;
    text-decoration: none !important;
}

a:hover {
    color: #0652DD !important;
    text-decoration: underline !important;
}

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}

::-webkit-scrollbar-track {
    background: #F5F7FA;
}

::-webkit-scrollbar-thumb {
    background: #CBD5E0;
    border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
    background: #2E86DE;
}
</style>
""", unsafe_allow_html=True)
# ==================================================================================
# END CLEAN LIGHT THEME
# ==================================================================================

# Header with gradient
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