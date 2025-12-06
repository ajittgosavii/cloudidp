"""
ULTRA-SIMPLE TEST - Just shows colored boxes
If you can't see these, something is very wrong with deployment
"""

import streamlit as st

st.set_page_config(
    page_title="SIMPLE TEST",
    page_icon="🧪",
    layout="wide"
)

# Test 1: Pure CSS colors
st.markdown("""
<style>
body {
    background-color: #000000 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background: red; padding: 50px; text-align: center; margin: 20px;">
    <h1 style="color: white; font-size: 60px;">TEST 1: RED BOX</h1>
    <p style="color: white; font-size: 30px;">If you see this, HTML works!</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background: green; padding: 50px; text-align: center; margin: 20px;">
    <h1 style="color: white; font-size: 60px;">TEST 2: GREEN BOX</h1>
    <p style="color: white; font-size: 30px;">If you see this, colors work!</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background: blue; padding: 50px; text-align: center; margin: 20px;">
    <h1 style="color: white; font-size: 60px;">TEST 3: BLUE BOX</h1>
    <p style="color: white; font-size: 30px;">If you see this, deployment works!</p>
</div>
""", unsafe_allow_html=True)

# Metric test
st.markdown("---")
st.markdown("## Metric Card Tests")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="background: white; border: 5px solid black; padding: 30px; border-radius: 10px;">
        <div style="color: black !important; font-size: 16px; font-weight: bold;">LABEL</div>
        <div style="color: black !important; font-size: 60px; font-weight: bold;">123</div>
    </div>
    """, unsafe_allow_html=True)
    st.caption("White card - can you see 123?")

with col2:
    st.markdown("""
    <div style="background: #333333; border: 5px solid orange; padding: 30px; border-radius: 10px;">
        <div style="color: orange !important; font-size: 16px; font-weight: bold;">LABEL</div>
        <div style="color: white !important; font-size: 60px; font-weight: bold;">456</div>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Dark card - can you see 456?")

with col3:
    st.markdown("""
    <div style="background: yellow; border: 5px solid red; padding: 30px; border-radius: 10px;">
        <div style="color: red !important; font-size: 16px; font-weight: bold;">LABEL</div>
        <div style="color: black !important; font-size: 60px; font-weight: bold;">789</div>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Yellow card - can you see 789?")

st.markdown("---")

st.error("🔴 ULTRA-SIMPLE TEST MODE")
st.info("""
**TAKE A SCREENSHOT OF THIS PAGE!**

Answer these questions:
1. Can you see RED BOX at top? (Yes/No)
2. Can you see GREEN BOX? (Yes/No)
3. Can you see BLUE BOX? (Yes/No)
4. Can you see 123 (white card)? (Yes/No)
5. Can you see 456 (dark card)? (Yes/No)
6. Can you see 789 (yellow card)? (Yes/No)

Send screenshot + answers to diagnose!
""")