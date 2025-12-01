"""
INTEGRATION GUIDE: How to Add Backend Services to streamlit_app.py

This file shows the EXACT changes you need to make to integrate the backend modules.
"""

# ============================================================================
# STEP 1: Add imports at the top of streamlit_app.py
# ============================================================================

# Add this after your existing imports (around line 19):

from backend_integration import CloudIDPBackend

# ============================================================================
# STEP 2: Initialize backend in config.py or streamlit_app.py
# ============================================================================

# In your config.py file, add to initialize_session_state():

def initialize_session_state():
    """Initialize session state variables"""
    
    # Existing code...
    if 'demo_mode' not in st.session_state:
        st.session_state.demo_mode = True
    
    # ADD THIS NEW CODE:
    if 'backend' not in st.session_state:
        st.session_state.backend = CloudIDPBackend(
            demo_mode=st.session_state.demo_mode,
            region='us-east-1'
        )
    
    # Rest of existing code...

# ============================================================================
# STEP 3: Update mode toggle to reinitialize backend
# ============================================================================

# In your main() function where you have the mode toggle (around line 113-121):

# REPLACE THIS:
st.session_state.demo_mode = (mode == "Demo Mode")

# WITH THIS:
old_demo_mode = st.session_state.get('demo_mode', True)
st.session_state.demo_mode = (mode == "Demo Mode")

# Reinitialize backend if mode changed
if old_demo_mode != st.session_state.demo_mode:
    st.session_state.backend = CloudIDPBackend(
        demo_mode=st.session_state.demo_mode,
        region='us-east-1'
    )

# ============================================================================
# STEP 4: Add backend status indicator in sidebar
# ============================================================================

# Add this after the mode indicator (around line 137):

# Display backend status
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🔧 Backend Status")
    
    try:
        health = st.session_state.backend.get_platform_health()
        
        if health['overall_status'] == 'healthy':
            st.success("✅ All systems operational")
        else:
            st.warning(f"⚠️ {len(health['unhealthy_services'])} services degraded")
        
        with st.expander("View Service Details"):
            for service, status in health['services'].items():
                status_icon = "✅" if status.get('status') == 'healthy' else "❌"
                st.write(f"{status_icon} {service}")
    except Exception as e:
        st.error(f"Backend error: {str(e)}")

# ============================================================================
# STEP 5: Example - Using backend in provisioning_deployment.py
# ============================================================================

# In your provisioning_deployment.py file, add this method:

def provision_with_backend(self):
    """Provision infrastructure using backend services"""
    
    st.markdown("## 🚀 Infrastructure Provisioning")
    
    col1, col2 = st.columns(2)
    
    with col1:
        env_name = st.text_input("Infrastructure Name", value="web-app")
        environment = st.selectbox("Environment", ["dev", "staging", "prod"])
    
    with col2:
        modules = st.multiselect(
            "Select Modules",
            ["vpc", "ec2", "rds", "alb", "s3", "cloudfront"],
            default=["vpc", "ec2"]
        )
    
    if st.button("Provision Infrastructure"):
        with st.spinner("Submitting provisioning job..."):
            try:
                # Use the backend!
                backend = st.session_state.backend
                
                result = backend.provision_infrastructure({
                    "name": env_name,
                    "environment": environment,
                    "modules": modules,
                    "variables": {
                        "vpc_cidr": "10.0.0.0/16",
                        "instance_type": "t3.medium"
                    },
                    "created_by": st.session_state.get('user_email', 'user@example.com')
                })
                
                if result['status'] == 'success':
                    st.success(f"✅ Infrastructure job created!")
                    
                    st.info(f"""
                    **Job Details:**
                    - Job ID: `{result['job_id']}`
                    - Terraform Job: `{result['terraform_job_id']}`
                    - Status: In Progress
                    
                    You can track this job in the Job Management section.
                    """)
                else:
                    st.error(f"❌ Failed: {result.get('message')}")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ============================================================================
# STEP 6: Example - Using backend in security_compliance.py
# ============================================================================

# In your security_compliance.py file, add this method:

def run_compliance_scan_with_backend(self):
    """Run compliance scan using backend services"""
    
    st.markdown("## 🔍 Compliance Scanning")
    
    col1, col2 = st.columns(2)
    
    with col1:
        account_id = st.text_input("AWS Account ID", value="123456789012")
        frameworks = st.multiselect(
            "Compliance Frameworks",
            ["CIS-AWS", "PCI-DSS", "HIPAA", "SOC 2", "GDPR"],
            default=["CIS-AWS"]
        )
    
    with col2:
        resources = st.multiselect(
            "Resource Types",
            ["ec2", "s3", "rds", "iam", "vpc", "lambda", "all"],
            default=["all"]
        )
        severity = st.selectbox("Minimum Severity", ["LOW", "MEDIUM", "HIGH", "CRITICAL"])
    
    if st.button("Start Scan"):
        with st.spinner("Initiating compliance scan..."):
            try:
                # Use the backend!
                backend = st.session_state.backend
                
                result = backend.run_compliance_scan({
                    "account_id": account_id,
                    "frameworks": frameworks,
                    "resources": resources,
                    "severity": severity
                })
                
                if result['status'] == 'success':
                    st.success(f"✅ Compliance scan started!")
                    
                    st.info(f"""
                    **Scan Details:**
                    - Scan ID: `{result['scan_id']}`
                    - Job ID: `{result['job_id']}`
                    - Account: {account_id}
                    - Frameworks: {', '.join(frameworks)}
                    
                    Results will be available in 5-10 minutes.
                    """)
                else:
                    st.error(f"❌ Failed: {result.get('message')}")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ============================================================================
# STEP 7: Example - Job monitoring dashboard
# ============================================================================

# Create a new function in streamlit_app.py for job monitoring:

def show_job_monitoring():
    """Show job monitoring dashboard"""
    
    st.markdown("## 📊 Job Monitoring Dashboard")
    
    backend = st.session_state.backend
    
    # Get active jobs
    try:
        jobs = backend.job_manager.list_active_jobs()
        
        if jobs['count'] > 0:
            st.success(f"Found {jobs['count']} active jobs")
            
            for job in jobs['jobs']:
                with st.expander(f"Job {job['job_id']} - {job['job_type']}"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Status", job['status'])
                    with col2:
                        st.metric("Progress", f"{job.get('progress', 0)}%")
                    with col3:
                        st.write(f"Created: {job['created_at']}")
                    
                    # Job details
                    st.json(job)
                    
                    # Action buttons
                    if job['status'] == 'running':
                        if st.button(f"Cancel Job {job['job_id'][:8]}"):
                            # Cancel job
                            st.warning("Job cancellation initiated")
        else:
            st.info("No active jobs at the moment")
            
    except Exception as e:
        st.error(f"Error loading jobs: {str(e)}")
    
    # Queue statistics
    st.markdown("### 📬 Message Queue Status")
    
    try:
        queue_stats = backend.message_queue.get_queue_stats()
        
        cols = st.columns(len(queue_stats['queues']))
        
        for idx, (queue_name, stats) in enumerate(queue_stats['queues'].items()):
            with cols[idx]:
                st.metric(
                    queue_name,
                    stats['messages'],
                    delta=f"{stats['in_flight']} in flight"
                )
    except Exception as e:
        st.error(f"Error loading queue stats: {str(e)}")

# ============================================================================
# STEP 8: Add job monitoring to navigation
# ============================================================================

# In your navigation selectbox (around line 141), add:

page = st.selectbox(
    "Select Module:",
    [
        "Home",
        # ... existing options ...
        "─────── JOB MANAGEMENT ───────",
        "Job Monitoring Dashboard",
        "Active Jobs",
        "Job History",
        # ... rest of options ...
    ]
)

# And in your page routing section, add:

elif page == "Job Monitoring Dashboard":
    show_job_monitoring()

# ============================================================================
# COMPLETE EXAMPLE: Updated streamlit_app.py structure
# ============================================================================

"""
Your updated streamlit_app.py should look like this:

import streamlit as st
from design_planning import DesignPlanningModule
from provisioning_deployment import ProvisioningDeploymentModule
# ... other imports ...

# NEW: Add backend import
from backend_integration import CloudIDPBackend
from config import get_aws_account_config


# Page configuration
st.set_page_config(...)

def main():
    # Initialize session state (with backend!)
    initialize_session_state()
    
    # Header
    st.markdown(...)
    
    # Sidebar
    with st.sidebar:
        # Logo
        st.markdown(...)
        
        # Mode toggle (with backend reinitialization)
        mode = st.radio(...)
        old_demo_mode = st.session_state.get('demo_mode', True)
        st.session_state.demo_mode = (mode == "Demo Mode")
        
        if old_demo_mode != st.session_state.demo_mode:
            st.session_state.backend = CloudIDPBackend(
                demo_mode=st.session_state.demo_mode
            )
        
        # Backend status indicator
        st.markdown("### 🔧 Backend Status")
        health = st.session_state.backend.get_platform_health()
        st.success("✅ All systems operational")
        
        # Navigation
        page = st.selectbox(...)
    
    # Page routing
    if page == "Home":
        show_home()
    elif page == "Job Monitoring Dashboard":
        show_job_monitoring()
    # ... etc ...

if __name__ == "__main__":
    main()
"""

# ============================================================================
# THAT'S IT! You're done!
# ============================================================================

"""
Summary of changes:

1. Import backend_integration module
2. Initialize backend in session state
3. Reinitialize when demo mode changes
4. Add backend status indicator in sidebar
5. Use backend in your existing modules
6. Add job monitoring dashboard
7. Update navigation

The backend will automatically use demo data when demo_mode=True,
and connect to real AWS services when demo_mode=False.

All your existing UI code works the same, but now it's connected to
a real backend infrastructure!
"""
