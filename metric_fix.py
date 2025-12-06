"""
PYTHON FIX - Bypass CSS entirely!
This creates custom metric functions that force white text directly in HTML
"""

import streamlit as st
from typing import Optional

def metric_with_white_text(
    label: str,
    value: str,
    delta: Optional[str] = None,
    delta_color: str = "normal",
    help: Optional[str] = None,
    label_visibility: str = "visible"
):
    """
    Custom metric that forces WHITE text - bypasses all CSS issues!
    
    Use this instead of st.metric() to guarantee visible text in dark boxes.
    
    Args:
        label: The metric label (e.g., "Connected Accounts")
        value: The metric value (e.g., "1" or "$0.00")
        delta: Optional delta value
        delta_color: "normal", "inverse", or "off"
        help: Optional help text
        label_visibility: "visible", "hidden", or "collapsed"
    
    Example:
        metric_with_white_text("Connected Accounts", "1")
    """
    
    # Create HTML with forced white text
    delta_html = ""
    if delta:
        delta_color_style = "#B0B0B0"  # Light gray for delta
        if delta_color == "inverse":
            # Inverse the typical red/green
            delta_color_style = "#FF6B6B" if delta.startswith("-") else "#4ECDC4"
        elif delta_color == "normal":
            # Normal green for positive, red for negative
            delta_color_style = "#4ECDC4" if delta.startswith("+") or not delta.startswith("-") else "#FF6B6B"
        
        delta_html = f"""
        <div style="color: {delta_color_style} !important; 
                    font-size: 14px !important; 
                    margin-top: 4px !important;
                    font-weight: 400 !important;">
            {delta}
        </div>
        """
    
    help_html = ""
    if help:
        help_html = f'title="{help}"'
    
    visibility_style = ""
    if label_visibility == "hidden":
        visibility_style = "visibility: hidden;"
    elif label_visibility == "collapsed":
        visibility_style = "display: none;"
    
    # Complete metric HTML with FORCED white text
    metric_html = f"""
    <div style="
        background-color: transparent !important;
        padding: 0 !important;
        margin: 0 !important;
    " {help_html}>
        <div style="
            color: white !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            margin-bottom: 4px !important;
            {visibility_style}
        ">
            {label}
        </div>
        <div style="
            color: white !important;
            font-size: 36px !important;
            font-weight: 600 !important;
            line-height: 1 !important;
            margin: 0 !important;
        ">
            {value}
        </div>
        {delta_html}
    </div>
    """
    
    st.markdown(metric_html, unsafe_allow_html=True)


# ========================================
# HOW TO USE IN YOUR DASHBOARD
# ========================================

# BEFORE (invisible text):
# st.metric("Connected Accounts", "1")
# st.metric("Total Resources", "N/A")
# st.metric("Last Monthly Cost", "$0.00")
# st.metric("Compliance Score", "N/A")

# AFTER (visible white text):
# metric_with_white_text("Connected Accounts", "1")
# metric_with_white_text("Total Resources", "N/A")
# metric_with_white_text("Last Monthly Cost", "$0.00")
# metric_with_white_text("Compliance Score", "N/A")

# With delta:
# metric_with_white_text("Active Users", "1,234", delta="+5%", delta_color="normal")

# ========================================
# STREAMLIT CLOUD DEPLOYMENT
# ========================================

"""
For Streamlit Cloud:

1. Add this file to your repository:
   - Save as: src/metric_fix.py
   OR
   - Add the function directly to your dashboard file

2. Import in your main file or dashboard:
   from metric_fix import metric_with_white_text

3. Replace all st.metric() calls with metric_with_white_text()

4. Commit and push:
   git add src/metric_fix.py
   git commit -m "Fix metric text visibility"
   git push origin main

5. Streamlit Cloud will auto-deploy!

That's it! No CSS changes needed!
"""

# ========================================
# ALTERNATIVE: ONE-LINE FIX
# ========================================

# If you want a quick one-line replacement, add this to your dashboard file:

def m(label, value, delta=None):
    """Ultra-short metric with white text"""
    st.markdown(f"""
    <div>
        <div style="color:white !important; font-size:14px; font-weight:500; margin-bottom:4px;">{label}</div>
        <div style="color:white !important; font-size:36px; font-weight:600;">{value}</div>
        {f'<div style="color:#B0B0B0 !important; font-size:14px; margin-top:4px;">{delta}</div>' if delta else ''}
    </div>
    """, unsafe_allow_html=True)

# Then use:
# m("Connected Accounts", "1")
# m("Total Resources", "N/A")
# m("Last Monthly Cost", "$0.00", delta="↑ Active")
