"""On-Demand Provisioning & Operations Module"""

import streamlit as st
from demo_data import DemoDataProvider
import pandas as pd

class OnDemandOperationsModule:
    """On-Demand Provisioning & Operations functionality"""
    
    @staticmethod
    def render_ondemand_overview():
        """Render on-demand provisioning overview"""
        st.markdown("## ⚡ On-Demand Provisioning & Operations")
        
        demo_mode = st.session_state.get('demo_mode', True)
        
        if demo_mode:
            data = DemoDataProvider.get_ondemand_dashboard()
        else:
            st.info("Live mode: Connect to AWS for real-time data")
            return
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Resources", f"{data['total_resources']:,}", 
                     delta=f"{data['resources_optimized']} optimized")
        with col2:
            st.metric("Monthly Savings", f"${data['monthly_savings']:,.0f}",
                     delta=f"{data['optimization_rate']:.1f}% rate")
        with col3:
            st.metric("Automated Actions", f"{data['automated_actions']:,}",
                     delta=f"{data['active_policies']} policies")
        with col4:
            st.metric("Avg Response Time", data['avg_response_time'],
                     delta="98.5% success")
        
        st.markdown("---")
        
        # Resource health and optimization
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Resource Optimization Status")
            df = pd.DataFrame(data['resource_health'])
            st.dataframe(df, hide_index=True, use_container_width=True)
        
        with col2:
            st.markdown("### 📈 Optimization Trends")
            trends_df = pd.DataFrame(data['optimization_trends'])
            st.line_chart(trends_df.set_index('month'))
    
    @staticmethod
    def render_provisioning_api():
        """Render Provisioning API interface"""
        st.markdown("## 🔌 On-Demand Provisioning API")
        
        st.markdown("""
        Self-service API for provisioning AWS resources with built-in guardrails, 
        right-sizing, and compliance validation.
        """)
        
        demo_mode = st.session_state.get('demo_mode', True)
        
        if demo_mode:
            configs = DemoDataProvider.get_provisioning_api_configs()
        else:
            st.info("Live mode: Connect to AWS for real-time data")
            return
        
        # API endpoints overview
        st.markdown("### 📡 Available API Endpoints")
        
        for config in configs:
            with st.expander(f"**{config['name']}** - {config['endpoint']}", expanded=False):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"**Method:** `{config['method']}`")
                    st.markdown(f"**Rate Limit:** {config['rate_limit']}")
                    st.markdown(f"**Auth:** {config['auth_type']}")
                
                with col2:
                    st.metric("Success Rate", f"{config['success_rate']}%")
                    st.metric("Avg Response", config['avg_response_time'])
                
                with col3:
                    st.metric("Last 30 Days", f"{config['last_30_days']:,} requests")
                    st.markdown(f"**Status:** {'🟢' if config['status'] == 'Active' else '🔴'} {config['status']}")
                
                st.markdown(f"**Description:** {config['description']}")
                
                st.markdown("**Sample Request:**")
                st.code(config['sample_request'], language='json')
                
                if st.button(f"Test API - {config['name']}", key=f"test_{config['id']}"):
                    st.success(f"✅ API test successful for {config['name']}")
    
    @staticmethod
    def render_guardrail_validation():
        """Render Guardrail Validation interface"""
        st.markdown("## 🛡️ Guardrail Validation (Pre-Deploy)")
        
        st.markdown("""
        Automated policy enforcement to prevent non-compliant resources from being deployed.
        Guardrails validate security, compliance, and cost policies before provisioning.
        """)
        
        demo_mode = st.session_state.get('demo_mode', True)
        
        if demo_mode:
            validations = DemoDataProvider.get_guardrail_validations()
        else:
            st.info("Live mode: Connect to AWS for real-time data")
            return
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        critical = sum(1 for v in validations if v['severity'] == 'Critical')
        high = sum(1 for v in validations if v['severity'] == 'High')
        total_prevented = sum(v['violations_prevented'] for v in validations)
        active = sum(1 for v in validations if v['status'] == 'Active')
        
        with col1:
            st.metric("Active Guardrails", active)
        with col2:
            st.metric("Critical Rules", critical, delta="High priority")
        with col3:
            st.metric("Violations Prevented", f"{total_prevented:,}")
        with col4:
            st.metric("High Severity", high)
        
        st.markdown("---")
        
        # Guardrail rules
        st.markdown("### 🔒 Active Guardrail Rules")
        
        for rule in validations:
            severity_icon = "🔴" if rule['severity'] == 'Critical' else "🟠" if rule['severity'] == 'High' else "🟡"
            
            with st.expander(f"{severity_icon} **{rule['name']}** - {rule['category']}", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Description:** {rule['description']}")
                    st.markdown(f"**Action:** {rule['action']}")
                    
                    if 'blocked_ports' in rule:
                        st.markdown(f"**Blocked Ports:** {', '.join(map(str, rule['blocked_ports']))}")
                    
                    if 'required_tags' in rule:
                        st.markdown(f"**Required Tags:** {', '.join(rule['required_tags'])}")
                
                with col2:
                    st.metric("Violations Prevented", f"{rule['violations_prevented']:,}")
                    st.markdown(f"**Severity:** {rule['severity']}")
                    st.markdown(f"**Status:** {'🟢' if rule['status'] == 'Active' else '🔴'} {rule['status']}")
                    st.caption(f"Last triggered: {rule['last_triggered']}")
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("Edit Rule", key=f"edit_{rule['id']}"):
                        st.info(f"Editing rule: {rule['name']}")
                with col2:
                    if st.button("View Logs", key=f"logs_{rule['id']}"):
                        st.info(f"Viewing logs for: {rule['name']}")
                with col3:
                    status = "Disable" if rule['status'] == 'Active' else "Enable"
                    if st.button(status, key=f"toggle_{rule['id']}"):
                        st.success(f"Rule {status.lower()}d")
    
    @staticmethod
    def render_deployment_templates():
        """Render Deployment Templates interface"""
        st.markdown("## 📦 Deployment Templates")
        
        st.markdown("""
        Pre-configured deployment templates with right-sizing, auto-scaling, 
        and optimization built-in.
        """)
        
        demo_mode = st.session_state.get('demo_mode', True)
        
        if demo_mode:
            templates = DemoDataProvider.get_deployment_templates()
        else:
            st.info("Live mode: Connect to AWS for real-time data")
            return
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            category_filter = st.selectbox("Category", ["All", "Compute", "Serverless", "Containers"])
        with col2:
            type_filter = st.selectbox("Type", ["All", "CloudFormation", "Terraform", "SAM Template"])
        with col3:
            sort_by = st.selectbox("Sort by", ["Most Used", "Recently Used", "Name"])
        
        st.markdown("---")
        
        # Display templates
        for template in templates:
            with st.expander(f"**{template['name']}** - {template['category']}", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Description:** {template['description']}")
                    st.markdown(f"**Type:** {template['type']} | **Version:** {template['version']}")
                    
                    st.markdown("**Features:**")
                    for feature in template['features']:
                        st.markdown(f"- {feature}")
                
                with col2:
                    st.metric("Times Used", template['use_count'])
                    st.markdown(f"**Est. Time:** {template['estimated_time']}")
                    st.markdown(f"**Est. Cost:** {template['estimated_cost']}")
                    st.caption(f"Last used: {template['last_used']}")
                
                # Deployment button
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("Deploy", key=f"deploy_{template['id']}", type="primary"):
                        st.success(f"✅ Deploying {template['name']}...")
                with col2:
                    if st.button("Preview", key=f"preview_{template['id']}"):
                        st.info(f"Previewing template: {template['name']}")
                with col3:
                    if st.button("Customize", key=f"custom_{template['id']}"):
                        st.info(f"Customizing: {template['name']}")
    
    @staticmethod
    def render_rightsizing():
        """Render Compute Right-Sizing interface"""
        st.markdown("## 📉 Compute Right-Sizing")
        
        st.markdown("""
        AI-powered recommendations to optimize instance sizes based on actual usage patterns.
        Reduce costs while maintaining performance.
        """)
        
        demo_mode = st.session_state.get('demo_mode', True)
        
        if demo_mode:
            recommendations = DemoDataProvider.get_rightsizing_recommendations()
        else:
            st.info("Live mode: Connect to AWS for real-time data")
            return
        
        # Summary metrics
        total_monthly_savings = sum(r['monthly_savings'] for r in recommendations)
        total_annual_savings = sum(r['annual_savings'] for r in recommendations)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Recommendations", len(recommendations))
        with col2:
            st.metric("Monthly Savings", f"${total_monthly_savings:,.0f}")
        with col3:
            st.metric("Annual Savings", f"${total_annual_savings:,.0f}")
        with col4:
            st.metric("High Confidence", sum(1 for r in recommendations if r['confidence'] == 'High'))
        
        st.markdown("---")
        
        # Recommendations table
        st.markdown("### 💡 Right-Sizing Recommendations")
        
        for rec in recommendations:
            confidence_color = "🟢" if rec['confidence'] == 'High' else "🟡"
            
            with st.expander(f"{confidence_color} **{rec['resource_name']}** - Save ${rec['monthly_savings']:.0f}/month", expanded=False):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"**Resource ID:** {rec['resource_id']}")
                    st.markdown(f"**Current Type:** `{rec['current_type']}`")
                    st.markdown(f"**Recommended:** `{rec['recommended_type']}`")
                
                with col2:
                    st.metric("Monthly Savings", f"${rec['monthly_savings']:.0f}")
                    st.metric("Annual Savings", f"${rec['annual_savings']:.0f}")
                    st.markdown(f"**Confidence:** {rec['confidence']}")
                
                with col3:
                    st.markdown(f"**CPU Utilization:** {rec['cpu_utilization']}")
                    st.markdown(f"**Memory Utilization:** {rec['memory_utilization']}")
                    st.caption(f"Recommendation age: {rec['recommendation_age']}")
                
                # Cost comparison
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Current Cost:**")
                    st.info(rec['current_cost'])
                with col2:
                    st.markdown("**Projected Cost:**")
                    st.success(rec['projected_cost'])
                
                # Actions
                if rec['action_available']:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("Apply Now", key=f"apply_{rec['resource_id']}", type="primary"):
                            st.success(f"✅ Resizing {rec['resource_name']} to {rec['recommended_type']}")
                    with col2:
                        if st.button("Schedule", key=f"schedule_{rec['resource_id']}"):
                            st.info("Scheduled for next maintenance window")
                    with col3:
                        if st.button("Dismiss", key=f"dismiss_{rec['resource_id']}"):
                            st.warning("Recommendation dismissed")
    
    @staticmethod
    def render_storage_tiering():
        """Render Storage Re-Tiering interface"""
        st.markdown("## 💾 Storage Re-Tiering")
        
        st.markdown("""
        Automated S3 lifecycle policies to move data to cost-effective storage classes.
        Optimize storage costs without sacrificing accessibility.
        """)
        
        demo_mode = st.session_state.get('demo_mode', True)
        
        if demo_mode:
            policies = DemoDataProvider.get_storage_tiering_policies()
        else:
            st.info("Live mode: Connect to AWS for real-time data")
            return
        
        # Summary metrics
        total_savings = sum(float(p['monthly_savings'].replace('$', '').replace(',', '')) for p in policies)
        total_objects = sum(float(p['objects_managed'].replace('M', '').replace('K', '')) * 
                          (1000000 if 'M' in p['objects_managed'] else 1000) for p in policies)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Active Policies", len(policies))
        with col2:
            st.metric("Objects Managed", f"{total_objects/1000000:.1f}M")
        with col3:
            st.metric("Monthly Savings", f"${total_savings:,.0f}")
        with col4:
            st.metric("Annual Savings", f"${total_savings*12:,.0f}")
        
        st.markdown("---")
        
        # Tiering policies
        st.markdown("### 🗄️ Active Tiering Policies")
        
        for policy in policies:
            with st.expander(f"**{policy['name']}** - {policy['bucket']}", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Bucket:** `{policy['bucket']}`")
                    st.markdown(f"**Status:** {'🟢' if policy['status'] == 'Active' else '🔴'} {policy['status']}")
                    
                    st.markdown("**Lifecycle Rules:**")
                    for rule in policy['rules']:
                        if 'storage_class' in rule:
                            st.markdown(f"- **{rule['name']}:** After {rule['days']} days → `{rule['storage_class']}`")
                        elif 'action' in rule:
                            st.markdown(f"- **{rule['name']}:** After {rule['days']} days → `{rule['action']}`")
                
                with col2:
                    st.metric("Objects Managed", policy['objects_managed'])
                    st.metric("Total Size", policy['total_size'])
                    st.metric("Monthly Savings", policy['monthly_savings'])
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("Edit Policy", key=f"edit_tier_{policy['id']}"):
                        st.info(f"Editing policy: {policy['name']}")
                with col2:
                    if st.button("View Metrics", key=f"metrics_{policy['id']}"):
                        st.info(f"Viewing metrics for: {policy['name']}")
                with col3:
                    if st.button("Pause", key=f"pause_{policy['id']}"):
                        st.warning("Policy paused")
    
    @staticmethod
    def render_autoscaling():
        """Render Auto-Scaling & Scheduling interface"""
        st.markdown("## ⏰ Auto-Scaling & Scheduling")
        
        st.markdown("""
        Intelligent scheduling to automatically scale resources based on time and demand.
        Reduce costs during off-hours while maintaining performance during peak times.
        """)
        
        demo_mode = st.session_state.get('demo_mode', True)
        
        if demo_mode:
            schedules = DemoDataProvider.get_autoscaling_schedules()
        else:
            st.info("Live mode: Connect to AWS for real-time data")
            return
        
        # Summary metrics
        total_savings = sum(float(s['monthly_savings'].replace('$', '').replace(',', '')) for s in schedules)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Active Schedules", len(schedules))
        with col2:
            st.metric("Monthly Savings", f"${total_savings:,.0f}")
        with col3:
            st.metric("Annual Savings", f"${total_savings*12:,.0f}")
        with col4:
            st.metric("Resource Types", len(set(s['resource_type'] for s in schedules)))
        
        st.markdown("---")
        
        # Schedules
        st.markdown("### 📅 Scaling Schedules")
        
        for schedule in schedules:
            with st.expander(f"**{schedule['name']}** - {schedule['resource_type']}", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Target:** `{schedule['target']}`")
                    st.markdown(f"**Type:** {schedule['schedule_type']}")
                    st.markdown(f"**Status:** {'🟢' if schedule['status'] == 'Active' else '🔴'} {schedule['status']}")
                    
                    st.markdown("**Schedules:**")
                    for sched in schedule['schedules']:
                        if 'min' in sched:
                            st.markdown(f"- {sched['time']} ({sched['days']}): Min={sched['min']}, Max={sched['max']}, Desired={sched['desired']}")
                        elif 'action' in sched:
                            st.markdown(f"- {sched['time']} ({sched['days']}): {sched['action']}")
                
                with col2:
                    st.metric("Monthly Savings", schedule['monthly_savings'])
                    st.markdown(f"**Resource Type:** {schedule['resource_type']}")
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("Edit Schedule", key=f"edit_sched_{schedule['id']}"):
                        st.info(f"Editing schedule: {schedule['name']}")
                with col2:
                    if st.button("View History", key=f"history_{schedule['id']}"):
                        st.info("Viewing execution history")
                with col3:
                    status = "Disable" if schedule['status'] == 'Active' else "Enable"
                    if st.button(status, key=f"toggle_sched_{schedule['id']}"):
                        st.success(f"Schedule {status.lower()}d")
