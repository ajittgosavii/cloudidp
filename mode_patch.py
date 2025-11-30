# Quick Patch: Make Demo/Live Mode Actually Work
# Add this to the TOP of streamlit_app.py (after imports)

import streamlit as st

# ===== DEMO/LIVE MODE PATCH =====
# This ensures mode switching actually changes data sources

# Initialize mode in session state
if 'mode' not in st.session_state:
    st.session_state.mode = "Demo"
    st.session_state.demo_mode = True

# Helper function for all modules to use
def get_data_source():
    """
    Returns data source type based on current mode
    Returns: 'demo' or 'live'
    """
    return 'demo' if st.session_state.mode == "Demo" else 'live'

def is_demo_mode():
    """
    Check if currently in demo mode
    Returns: True if Demo mode, False if Live mode
    """
    return st.session_state.mode == "Demo"

def get_blueprints():
    """Example: Get blueprints based on mode"""
    if is_demo_mode():
        # Return demo data
        import demo_data
        return demo_data.get_blueprints()
    else:
        # Return live data
        try:
            from database_service import DatabaseService
            db = DatabaseService()
            return db.get_blueprints()
        except Exception as e:
            st.error(f"Error fetching live data: {e}")
            st.info("Falling back to demo data")
            import demo_data
            return demo_data.get_blueprints()

def get_ec2_instances(region='us-east-1'):
    """Example: Get EC2 instances based on mode"""
    if is_demo_mode():
        import demo_data
        return demo_data.get_ec2_instances()
    else:
        try:
            import boto3
            ec2 = boto3.client('ec2', region_name=region)
            response = ec2.describe_instances()
            instances = []
            for reservation in response['Reservations']:
                instances.extend(reservation['Instances'])
            return instances
        except Exception as e:
            st.error(f"Error fetching live EC2 data: {e}")
            st.info("Falling back to demo data")
            import demo_data
            return demo_data.get_ec2_instances()

def get_cost_data(start_date=None, end_date=None):
    """Example: Get cost data based on mode"""
    if is_demo_mode():
        import demo_data
        return demo_data.get_cost_data()
    else:
        try:
            import boto3
            from datetime import datetime, timedelta
            
            ce = boto3.client('ce', region_name='us-east-1')
            
            if not start_date:
                start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            if not end_date:
                end_date = datetime.now().strftime('%Y-%m-%d')
            
            response = ce.get_cost_and_usage(
                TimePeriod={'Start': start_date, 'End': end_date},
                Granularity='MONTHLY',
                Metrics=['UnblendedCost']
            )
            return response
        except Exception as e:
            st.error(f"Error fetching live cost data: {e}")
            st.info("Falling back to demo data")
            import demo_data
            return demo_data.get_cost_data()

# Make these functions available globally
st.session_state.get_data_source = get_data_source
st.session_state.is_demo_mode = is_demo_mode
st.session_state.get_blueprints = get_blueprints
st.session_state.get_ec2_instances = get_ec2_instances
st.session_state.get_cost_data = get_cost_data

# ===== END PATCH =====

# USAGE IN MODULES:
# Instead of:
#   blueprints = demo_data.get_blueprints()
# 
# Use:
#   blueprints = st.session_state.get_blueprints()
#
# Or check mode directly:
#   if st.session_state.is_demo_mode():
#       data = demo_data.get_something()
#   else:
#       data = real_service.get_something()
