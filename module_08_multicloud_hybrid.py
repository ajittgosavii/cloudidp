"""
Module 08: Multi-Cloud & Hybrid Support
Comprehensive multi-cloud and hybrid cloud management
"""

import streamlit as st
import json
from datetime import datetime
from typing import Dict, List, Any

class MultiCloudHybridModule:
    """Multi-Cloud & Hybrid Cloud Support Module"""
    
    def __init__(self):
        self.module_name = "Multi-Cloud & Hybrid Support"
        self.version = "1.0.0"
        

    def _get_data(self, key: str, default_demo_value):
        """
        Get data based on current mode (Demo or Live)
        
        Args:
            key: Data key to fetch
            default_demo_value: Value to return in demo mode
            
        Returns:
            Demo data or Live data based on mode
        """
        is_demo = st.session_state.get('mode', 'Demo') == 'Demo'
        
        if is_demo:
            return default_demo_value
        else:
            try:
                # TODO: Implement live data fetching for this key
                # For now, return demo value in live mode
                # Add your live data logic here
                
                # Example:
                # if key == 'total_cost':
                #     from cost_explorer_integration import CostExplorerIntegration
                #     ce = CostExplorerIntegration()
                #     return ce.get_total_cost()
                
                return default_demo_value
            except Exception as e:
                st.warning(f"Live data fetch failed for {key}: {e}")
                return default_demo_value


    def render(self):
        """Main render method for the module"""
        st.header("☁️ Multi-Cloud & Hybrid Support")

        # Show current mode
        is_demo = st.session_state.get('mode', 'Demo') == 'Demo'
        if is_demo:
            st.info("📊 Demo Mode: Showing sample data")
        else:
            st.success("🔴 Live Mode: Showing real data")
        

        st.markdown("**Enterprise Multi-Cloud Architecture & Hybrid Connectivity Framework**")
        
        # Main navigation tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🌐 Cloud & On-Prem Provisioning",
            "📋 Unified Policy Framework",
            "⚡ Cloud-Specific Optimization",
            "🔗 Private+Public Connectivity",
            "🌍 Global Environment Management"
        ])
        
        with tab1:
            self._render_provisioning()
        with tab2:
            self._render_policy_framework()
        with tab3:
            self._render_optimization()
        with tab4:
            self._render_connectivity()
        with tab5:
            self._render_global_management()
    
    def _render_provisioning(self):
        """Cloud & On-Prem Provisioning Management"""
        st.subheader("🌐 Cloud & On-Premises Provisioning")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### Multi-Cloud Provisioning")
            
            # Cloud provider selection
            providers = st.multiselect(
                "Select Cloud Providers",
                ["AWS", "Azure", "GCP", "Oracle Cloud", "IBM Cloud", "Alibaba Cloud"],
                default=["AWS", "Azure", "GCP"]
            )
            
            # Provisioning strategy
            strategy = st.selectbox(
                "Provisioning Strategy",
                ["Multi-Cloud Active-Active", "Primary-Secondary", "Cloud Bursting", 
                 "Disaster Recovery", "Data Residency Compliance"]
            )
            
            # Workload distribution
            st.markdown("#### Workload Distribution")
            for provider in providers:
                percentage = st.slider(
                    f"{provider} Workload %",
                    0, 100, 33 if len(providers) == 3 else 50,
                    key=f"workload_{provider}"
                )
            
            # Resource provisioning
            st.markdown("#### Resource Provisioning")
            resource_type = st.selectbox(
                "Resource Type",
                ["Compute (VMs/Containers)", "Storage (Block/Object)", "Databases",
                 "Networking", "Serverless Functions", "Analytics"]
            )
            
            # IaC tool selection
            iac_tool = st.selectbox(
                "Infrastructure as Code Tool",
                ["Terraform (Multi-Cloud)", "CloudFormation (AWS)", "ARM Templates (Azure)",
                 "Deployment Manager (GCP)", "Pulumi", "Crossplane"]
            )
            
            if st.button("Generate Provisioning Templates", key="gen_provisioning"):
                st.success("✅ Provisioning templates generated")
                self._show_provisioning_templates(providers, iac_tool)
        
        with col2:
            st.markdown("### On-Premises Integration")
            
            # On-prem environment
            onprem_type = st.selectbox(
                "On-Premises Environment",
                ["VMware vSphere", "Microsoft Hyper-V", "OpenStack",
                 "Bare Metal", "Kubernetes On-Prem", "Mixed Environment"]
            )
            
            # Hybrid connectivity
            st.markdown("#### Hybrid Connectivity Options")
            connectivity = st.multiselect(
                "Connection Methods",
                ["AWS Direct Connect", "Azure ExpressRoute", "GCP Dedicated Interconnect",
                 "VPN Gateway", "SD-WAN", "Private Network Links"],
                default=["AWS Direct Connect", "VPN Gateway"]
            )
            
            # Data synchronization
            st.markdown("#### Data Synchronization")
            sync_method = st.selectbox(
                "Sync Strategy",
                ["Real-time Replication", "Scheduled Sync", "Event-Driven Sync",
                 "Hybrid Backup", "Active-Active", "Active-Passive"]
            )
            
            sync_interval = st.select_slider(
                "Sync Frequency",
                options=["Real-time", "1 min", "5 min", "15 min", "1 hour", "Daily"],
                value="15 min"
            )
            
            # Capacity planning
            st.markdown("#### Capacity Planning")
            onprem_capacity = st.slider("On-Prem Capacity Utilization %", 0, 100, 70)
            cloud_burst = st.checkbox("Enable Cloud Bursting", value=True)
            
            if cloud_burst:
                burst_threshold = st.slider("Cloud Burst Threshold %", 60, 95, 80)
                st.info(f"🔄 Will burst to cloud when on-prem exceeds {burst_threshold}%")
        
        # Provisioning Architecture
        st.markdown("---")
        st.markdown("### 📊 Provisioning Architecture Overview")
        
        col_arch1, col_arch2, col_arch3 = st.columns(3)
        
        with col_arch1:
            # Mode-aware metric
            total_environments_value = self._get_data('total_environments', "12")
            total_environments_delta = self._get_data('total_environments_delta', "+2")
            st.metric("Total Environments", total_environments_value, total_environments_delta)
            st.metric("Active Providers", str(len(providers)))
        
        with col_arch2:
            # Mode-aware metric
            provisioning_time_value = self._get_data('provisioning_time', "15 min")
            provisioning_time_delta = self._get_data('provisioning_time_delta', "-5 min")
            st.metric("Provisioning Time", provisioning_time_value, provisioning_time_delta)
            # Mode-aware metric
            success_rate_value = self._get_data('success_rate', "99.8%")
            success_rate_delta = self._get_data('success_rate_delta', "+0.2%")
            st.metric("Success Rate", success_rate_value, success_rate_delta)
        
        with col_arch3:
            # Mode-aware metric
            active_connections_value = self._get_data('active_connections', "24")
            active_connections_delta = self._get_data('active_connections_delta', "+4")
            st.metric("Active Connections", active_connections_value, active_connections_delta)
            # Mode-aware metric
            sync_lag_value = self._get_data('sync_lag', "< 2s")
            sync_lag_delta = self._get_data('sync_lag_delta', "-0.5s")
            st.metric("Sync Lag", sync_lag_value, sync_lag_delta)
        
        # Provisioning workflow
        if st.checkbox("Show Provisioning Workflow", key="show_prov_workflow"):
            self._show_provisioning_workflow(providers, onprem_type)
    
    def _render_policy_framework(self):
        """Unified Policy Framework"""
        st.subheader("📋 Unified Policy Framework")
        
        # Policy management tabs
        policy_tab1, policy_tab2, policy_tab3, policy_tab4 = st.tabs([
            "Policy Definition", "Compliance Mapping", "Enforcement", "Audit & Reporting"
        ])
        
        with policy_tab1:
            st.markdown("### Policy Definition & Management")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### Create Unified Policy")
                
                policy_name = st.text_input("Policy Name", "Multi-Cloud-Security-Standard-2025")
                
                policy_scope = st.multiselect(
                    "Policy Scope",
                    ["AWS", "Azure", "GCP", "On-Premises", "Edge Locations"],
                    default=["AWS", "Azure", "GCP"]
                )
                
                policy_type = st.selectbox(
                    "Policy Type",
                    ["Security", "Compliance", "Cost Control", "Resource Management",
                     "Data Governance", "Network", "Identity & Access"]
                )
                
                # Policy rules
                st.markdown("#### Policy Rules")
                
                rule_categories = st.multiselect(
                    "Rule Categories",
                    ["Encryption at Rest", "Encryption in Transit", "Access Control",
                     "Network Segmentation", "Logging & Monitoring", "Backup & DR",
                     "Resource Tagging", "Cost Limits", "Data Classification"],
                    default=["Encryption at Rest", "Access Control", "Logging & Monitoring"]
                )
                
                severity = st.select_slider(
                    "Policy Severity",
                    options=["Info", "Low", "Medium", "High", "Critical"],
                    value="High"
                )
                
                enforcement_mode = st.radio(
                    "Enforcement Mode",
                    ["Advisory (Notify Only)", "Soft Enforcement (Warn)", 
                     "Hard Enforcement (Block)", "Audit Only"],
                    index=2
                )
            
            with col2:
                st.markdown("#### Policy Translation Engine")
                
                st.info("🔄 Automatically translate policies to cloud-native formats")
                
                # Show translation targets
                if policy_scope:
                    st.markdown("**Translation Targets:**")
                    for cloud in policy_scope:
                        if cloud == "AWS":
                            st.markdown("- AWS: IAM Policies, SCPs, Config Rules")
                        elif cloud == "Azure":
                            st.markdown("- Azure: RBAC, Azure Policy, Blueprints")
                        elif cloud == "GCP":
                            st.markdown("- GCP: IAM Policies, Organization Policies")
                        elif cloud == "On-Premises":
                            st.markdown("- On-Prem: Active Directory GPOs, Network Policies")
                
                # Policy template
                st.markdown("#### Policy Template")
                policy_template = st.selectbox(
                    "Use Template",
                    ["Custom", "CIS Benchmark", "NIST", "PCI DSS", "HIPAA", "GDPR", "SOC 2"]
                )
                
                if st.button("Generate Policy Definition", key="gen_policy"):
                    st.success("✅ Policy definition generated")
                    self._show_policy_definition(policy_name, policy_scope, rule_categories)
        
        with policy_tab2:
            st.markdown("### Compliance Framework Mapping")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### Select Compliance Frameworks")
                
                frameworks = st.multiselect(
                    "Compliance Standards",
                    ["ISO 27001", "SOC 2 Type II", "PCI DSS 4.0", "HIPAA", 
                     "GDPR", "NIST 800-53", "CIS Controls", "FedRAMP"],
                    default=["ISO 27001", "SOC 2 Type II", "PCI DSS 4.0"]
                )
                
                # Control mapping
                st.markdown("#### Control Mapping")
                for framework in frameworks:
                    with st.expander(f"{framework} Controls"):
                        controls = self._get_framework_controls(framework)
                        for control in controls[:5]:  # Show first 5
                            st.checkbox(
                                f"{control['id']}: {control['name']}", 
                                value=True,
                                key=f"{framework}_{control['id']}"
                            )
            
            with col2:
                st.markdown("#### Compliance Mapping Matrix")
                
                if frameworks:
                    st.dataframe(
                        self._get_compliance_matrix(frameworks),
                        use_container_width=True,
                        height=300
                    )
                
                st.markdown("#### Coverage Analysis")
                if st.button("Analyze Coverage", key="analyze_coverage"):
                    col_cov1, col_cov2, col_cov3 = st.columns(3)
                    with col_cov1:
                        # Mode-aware metric
            overall_coverage_value = self._get_data('overall_coverage', "94%")
            overall_coverage_delta = self._get_data('overall_coverage_delta', "+3%")
            st.metric("Overall Coverage", overall_coverage_value, overall_coverage_delta)
                    with col_cov2:
                        # Mode-aware metric
            automated_controls_value = self._get_data('automated_controls', "156")
            automated_controls_delta = self._get_data('automated_controls_delta', "+12")
            st.metric("Automated Controls", automated_controls_value, automated_controls_delta)
                    with col_cov3:
                        # Mode-aware metric
            manual_reviews_value = self._get_data('manual_reviews', "23")
            manual_reviews_delta = self._get_data('manual_reviews_delta', "-5")
            st.metric("Manual Reviews", manual_reviews_value, manual_reviews_delta)
        
        with policy_tab3:
            st.markdown("### Policy Enforcement")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### Enforcement Configuration")
                
                # Real-time enforcement
                realtime = st.checkbox("Enable Real-time Enforcement", value=True)
                
                if realtime:
                    st.markdown("**Enforcement Actions:**")
                    actions = st.multiselect(
                        "Select Actions",
                        ["Block Non-Compliant Resources", "Auto-Remediate",
                         "Send Notifications", "Create Tickets", "Escalate to Security",
                         "Quarantine Resources", "Generate Audit Log"],
                        default=["Block Non-Compliant Resources", "Send Notifications", "Generate Audit Log"]
                    )
                
                # Enforcement hooks
                st.markdown("#### Enforcement Hooks")
                hooks = st.multiselect(
                    "Integration Points",
                    ["CI/CD Pipeline", "IaC Templates", "Cloud Console",
                     "API Calls", "CLI Commands", "Terraform/ARM"],
                    default=["CI/CD Pipeline", "IaC Templates", "API Calls"]
                )
                
                # Exception management
                st.markdown("#### Exception Management")
                allow_exceptions = st.checkbox("Allow Policy Exceptions", value=True)
                
                if allow_exceptions:
                    approval_required = st.checkbox("Require Approval", value=True)
                    exception_duration = st.selectbox(
                        "Exception Duration",
                        ["1 Hour", "1 Day", "1 Week", "1 Month", "Until Revoked"]
                    )
            
            with col2:
                st.markdown("#### Enforcement Status")
                
                st.markdown("**Live Enforcement Metrics:**")
                
                metrics_col1, metrics_col2 = st.columns(2)
                with metrics_col1:
                    # Mode-aware metric
            policies_active_value = self._get_data('policies_active', "87")
            st.metric("Policies Active", policies_active_value)
                    # Mode-aware metric
            violations_(24h)_value = self._get_data('violations_(24h)', "23")
            violations_(24h)_delta = self._get_data('violations_(24h)_delta', "-12")
            st.metric("Violations (24h)", violations_(24h)_value, violations_(24h)_delta)
                with metrics_col2:
                    # Mode-aware metric
            auto-remediated_value = self._get_data('auto-remediated', "18")
            auto-remediated_delta = self._get_data('auto-remediated_delta', "+5")
            st.metric("Auto-Remediated", auto-remediated_value, auto-remediated_delta)
                    # Mode-aware metric
            manual_review_value = self._get_data('manual_review', "5")
            manual_review_delta = self._get_data('manual_review_delta', "+1")
            st.metric("Manual Review", manual_review_value, manual_review_delta)
                
                # Recent enforcement actions
                st.markdown("#### Recent Enforcement Actions")
                enforcement_data = [
                    {"Time": "10:45 AM", "Action": "Blocked", "Resource": "S3 Bucket", "Reason": "Public Access"},
                    {"Time": "10:30 AM", "Action": "Remediated", "Resource": "EC2 Instance", "Reason": "Missing Tags"},
                    {"Time": "10:15 AM", "Action": "Alert", "Resource": "IAM Role", "Reason": "Excessive Permissions"},
                    {"Time": "10:00 AM", "Action": "Blocked", "Resource": "RDS Instance", "Reason": "No Encryption"},
                ]
                st.dataframe(enforcement_data, use_container_width=True)
        
        with policy_tab4:
            st.markdown("### Audit & Reporting")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### Audit Configuration")
                
                audit_scope = st.multiselect(
                    "Audit Scope",
                    ["All Policies", "Security Policies", "Compliance Policies",
                     "Cost Policies", "Custom Selection"],
                    default=["All Policies"]
                )
                
                audit_period = st.selectbox(
                    "Audit Period",
                    ["Last 24 Hours", "Last 7 Days", "Last 30 Days", 
                     "Last Quarter", "Custom Range"]
                )
                
                report_format = st.multiselect(
                    "Report Format",
                    ["PDF", "Excel", "JSON", "CSV", "HTML Dashboard"],
                    default=["PDF", "Excel"]
                )
                
                include_evidence = st.checkbox("Include Evidence/Screenshots", value=True)
                
                if st.button("Generate Audit Report", key="gen_audit"):
                    st.success("✅ Audit report generated")
                    st.download_button(
                        "📥 Download Report",
                        data="Sample audit report content",
                        file_name=f"audit_report_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf"
                    )
            
            with col2:
                st.markdown("#### Compliance Dashboard")
                
                # Compliance scores
                st.markdown("**Compliance Scores:**")
                compliance_scores = {
                    "ISO 27001": 96,
                    "SOC 2": 94,
                    "PCI DSS": 98,
                    "HIPAA": 91,
                    "GDPR": 93
                }
                
                for framework, score in compliance_scores.items():
                    st.progress(score / 100)
                    st.caption(f"{framework}: {score}%")
                
                st.markdown("---")
                
                # Trend analysis
                st.markdown("**Compliance Trend (30 Days)**")
                st.line_chart({
                    "Day 1": 90, "Day 7": 92, "Day 14": 94,
                    "Day 21": 93, "Day 30": 95
                })
    
    def _render_optimization(self):
        """Cloud-Specific Optimization"""
        st.subheader("⚡ Cloud-Specific Optimization")
        
        # Optimization tabs
        opt_tab1, opt_tab2, opt_tab3, opt_tab4 = st.tabs([
            "Cost Optimization", "Performance Tuning", "Resource Right-Sizing", "Best Practices"
        ])
        
        with opt_tab1:
            st.markdown("### Multi-Cloud Cost Optimization")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### Cost Analysis by Cloud")
                
                cloud_costs = {
                    "AWS": {"current": 145000, "optimized": 112000, "savings": 33000},
                    "Azure": {"current": 98000, "optimized": 79000, "savings": 19000},
                    "GCP": {"current": 67000, "optimized": 54000, "savings": 13000}
                }
                
                for cloud, costs in cloud_costs.items():
                    with st.expander(f"{cloud} Cost Breakdown"):
                        col_cost1, col_cost2, col_cost3 = st.columns(3)
                        with col_cost1:
                            st.metric("Current", f"${costs['current']:,}")
                        with col_cost2:
                            st.metric("Optimized", f"${costs['optimized']:,}")
                        with col_cost3:
                            st.metric("Savings", f"${costs['savings']:,}", 
                                    delta=f"{(costs['savings']/costs['current']*100):.1f}%")
                
                # Optimization recommendations
                st.markdown("#### Optimization Recommendations")
                
                recommendations = [
                    {"Cloud": "AWS", "Action": "Reserved Instances", "Savings": "$22K/mo", "Effort": "Low"},
                    {"Cloud": "AWS", "Action": "S3 Lifecycle Rules", "Savings": "$8K/mo", "Effort": "Low"},
                    {"Cloud": "Azure", "Action": "VM Right-Sizing", "Savings": "$12K/mo", "Effort": "Medium"},
                    {"Cloud": "GCP", "Action": "Committed Use Discounts", "Savings": "$9K/mo", "Effort": "Low"},
                ]
                
                st.dataframe(recommendations, use_container_width=True)
            
            with col2:
                st.markdown("#### Cost Optimization Tools")
                
                # Tool selection
                opt_tools = st.multiselect(
                    "Enable Optimization Tools",
                    ["AWS Cost Explorer", "Azure Cost Management", "GCP Cost Management",
                     "Cloudability", "CloudHealth", "Spot.io", "ProsperOps"],
                    default=["AWS Cost Explorer", "Azure Cost Management", "GCP Cost Management"]
                )
                
                # Automated actions
                st.markdown("#### Automated Cost Actions")
                
                auto_actions = st.multiselect(
                    "Enable Automated Actions",
                    ["Stop idle resources", "Downsize over-provisioned resources",
                     "Delete unused snapshots", "Archive old data to cheaper storage",
                     "Convert to reserved/committed instances", "Enable spot instances"],
                    default=["Stop idle resources", "Delete unused snapshots"]
                )
                
                # Savings goals
                st.markdown("#### Savings Goals")
                
                monthly_target = st.number_input(
                    "Monthly Savings Target ($)", 
                    min_value=0, 
                    value=50000, 
                    step=1000
                )
                
                st.progress(65 / 100)
                st.caption(f"Current Progress: $32,500 of ${monthly_target:,} (65%)")
                
                if st.button("Generate Optimization Plan", key="gen_opt_plan"):
                    st.success("✅ Optimization plan generated")
                    self._show_optimization_plan()
        
        with opt_tab2:
            st.markdown("### Performance Tuning")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### Performance Metrics")
                
                # Select cloud for tuning
                tune_cloud = st.selectbox(
                    "Select Cloud for Tuning",
                    ["AWS", "Azure", "GCP", "Multi-Cloud View"]
                )
                
                # Performance areas
                perf_areas = st.multiselect(
                    "Performance Focus Areas",
                    ["Compute (CPU/Memory)", "Storage (IOPS/Throughput)", 
                     "Network (Latency/Bandwidth)", "Database (Query Performance)",
                     "Application (Response Time)", "API (Throughput)"],
                    default=["Compute (CPU/Memory)", "Network (Latency/Bandwidth)"]
                )
                
                # Current performance
                st.markdown("**Current Performance:**")
                
                metrics = {
                    "Avg Response Time": ("234 ms", "-45 ms"),
                    "P95 Latency": ("890 ms", "-120 ms"),
                    "Throughput": ("12,450 req/s", "+2,300 req/s"),
                    "Error Rate": ("0.12%", "-0.05%")
                }
                
                metric_cols = st.columns(2)
                for idx, (metric, (value, delta)) in enumerate(metrics.items()):
                    with metric_cols[idx % 2]:
                        st.metric(metric, value, delta)
            
            with col2:
                st.markdown("#### Tuning Recommendations")
                
                tuning_recs = [
                    {
                        "Area": "Compute",
                        "Issue": "CPU throttling detected",
                        "Action": "Upgrade to c6i.2xlarge",
                        "Impact": "+40% performance"
                    },
                    {
                        "Area": "Storage",
                        "Issue": "IOPS limit reached",
                        "Action": "Increase provisioned IOPS",
                        "Impact": "+25% throughput"
                    },
                    {
                        "Area": "Network",
                        "Issue": "Cross-region latency",
                        "Action": "Deploy regional caching",
                        "Impact": "-60% latency"
                    }
                ]
                
                for rec in tuning_recs:
                    with st.expander(f"🔧 {rec['Area']}: {rec['Issue']}"):
                        st.markdown(f"**Recommended Action:** {rec['Action']}")
                        st.markdown(f"**Expected Impact:** {rec['Impact']}")
                        st.button(f"Apply Tuning", key=f"apply_{rec['Area']}")
                
                # Auto-tuning
                st.markdown("---")
                st.markdown("#### Auto-Tuning")
                
                enable_auto_tune = st.checkbox("Enable Auto-Tuning", value=False)
                
                if enable_auto_tune:
                    st.warning("⚠️ Auto-tuning will automatically adjust resources based on performance metrics")
                    tune_aggressiveness = st.select_slider(
                        "Tuning Aggressiveness",
                        options=["Conservative", "Moderate", "Aggressive"],
                        value="Moderate"
                    )
        
        with opt_tab3:
            st.markdown("### Resource Right-Sizing")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### Right-Sizing Analysis")
                
                # Resource type
                resource_type = st.selectbox(
                    "Resource Type",
                    ["Compute (VMs/Instances)", "Databases", "Storage Volumes",
                     "Containers", "Kubernetes Clusters", "Serverless Functions"]
                )
                
                # Analysis period
                analysis_period = st.selectbox(
                    "Analysis Period",
                    ["Last 7 Days", "Last 14 Days", "Last 30 Days", "Last 90 Days"]
                )
                
                # Utilization thresholds
                st.markdown("#### Utilization Thresholds")
                
                cpu_threshold = st.slider("CPU Utilization Threshold (%)", 0, 100, 60)
                memory_threshold = st.slider("Memory Utilization Threshold (%)", 0, 100, 70)
                
                if st.button("Analyze Resources", key="analyze_resources"):
                    st.success("✅ Analysis complete")
                    
                    # Show findings
                    st.markdown("**Findings:**")
                    
                    findings = [
                        {"Type": "Over-Provisioned", "Count": 45, "Potential Savings": "$12,400/mo"},
                        {"Type": "Under-Provisioned", "Count": 12, "Performance Risk": "High"},
                        {"Type": "Properly Sized", "Count": 234, "Status": "Optimal"}
                    ]
                    
                    st.dataframe(findings, use_container_width=True)
            
            with col2:
                st.markdown("#### Right-Sizing Recommendations")
                
                sizing_recs = [
                    {
                        "Resource": "prod-web-server-01 (AWS)",
                        "Current": "m5.2xlarge (8 vCPU, 32 GB)",
                        "Recommended": "m5.xlarge (4 vCPU, 16 GB)",
                        "Reason": "Avg CPU: 22%, Avg Memory: 35%",
                        "Savings": "$146/mo"
                    },
                    {
                        "Resource": "prod-db-master (Azure)",
                        "Current": "Standard_D4s_v3 (4 vCPU, 16 GB)",
                        "Recommended": "Standard_D8s_v3 (8 vCPU, 32 GB)",
                        "Reason": "CPU regularly at 85%, OOM events",
                        "Cost": "+$234/mo (Performance Critical)"
                    }
                ]
                
                for idx, rec in enumerate(sizing_recs):
                    with st.expander(f"📊 {rec['Resource']}"):
                        st.markdown(f"**Current:** {rec['Current']}")
                        st.markdown(f"**Recommended:** {rec['Recommended']}")
                        st.markdown(f"**Reason:** {rec['Reason']}")
                        if 'Savings' in rec:
                            st.success(f"💰 {rec['Savings']}")
                        else:
                            st.warning(f"💸 {rec['Cost']}")
                        
                        col_btn1, col_btn2 = st.columns(2)
                        with col_btn1:
                            st.button("Apply", key=f"apply_sizing_{idx}")
                        with col_btn2:
                            st.button("Schedule", key=f"schedule_sizing_{idx}")
        
        with opt_tab4:
            st.markdown("### Cloud-Specific Best Practices")
            
            # Best practices by cloud
            bp_cloud = st.selectbox(
                "Select Cloud Provider",
                ["AWS", "Azure", "GCP", "Oracle Cloud", "IBM Cloud"]
            )
            
            # Categories
            bp_categories = st.multiselect(
                "Best Practice Categories",
                ["Security", "Cost Optimization", "Performance", "Reliability",
                 "Operational Excellence", "Sustainability"],
                default=["Security", "Cost Optimization", "Reliability"]
            )
            
            # Show best practices
            st.markdown(f"### {bp_cloud} Best Practices")
            
            if bp_cloud == "AWS":
                practices = self._get_aws_best_practices(bp_categories)
            elif bp_cloud == "Azure":
                practices = self._get_azure_best_practices(bp_categories)
            elif bp_cloud == "GCP":
                practices = self._get_gcp_best_practices(bp_categories)
            else:
                practices = []
            
            for practice in practices:
                with st.expander(f"✓ {practice['title']}"):
                    st.markdown(f"**Category:** {practice['category']}")
                    st.markdown(f"**Priority:** {practice['priority']}")
                    st.markdown(f"**Description:** {practice['description']}")
                    st.markdown(f"**Implementation:** {practice['implementation']}")
                    
                    compliance_status = st.selectbox(
                        "Compliance Status",
                        ["Not Started", "In Progress", "Compliant", "Not Applicable"],
                        key=f"bp_{practice['title']}"
                    )
    
    def _render_connectivity(self):
        """Private+Public Connectivity Management"""
        st.subheader("🔗 Private + Public Connectivity")
        
        # Connectivity tabs
        conn_tab1, conn_tab2, conn_tab3, conn_tab4 = st.tabs([
            "Network Architecture", "Hybrid Connectivity", "Security Zones", "Traffic Management"
        ])
        
        with conn_tab1:
            st.markdown("### Network Architecture Design")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### Network Topology")
                
                topology = st.selectbox(
                    "Select Topology",
                    ["Hub-and-Spoke", "Mesh Network", "Transit Gateway", 
                     "SD-WAN", "Multi-Region Mesh", "Hybrid Mesh"]
                )
                
                # Network components
                st.markdown("#### Network Components")
                
                components = st.multiselect(
                    "Select Components",
                    ["VPC/VNet", "Subnets (Public/Private)", "Transit Gateway",
                     "VPN Gateway", "Direct Connect", "ExpressRoute",
                     "Cloud Interconnect", "NAT Gateway", "Load Balancers",
                     "API Gateway", "CDN", "DNS"],
                    default=["VPC/VNet", "Subnets (Public/Private)", "Transit Gateway", "Load Balancers"]
                )
                
                # IP addressing
                st.markdown("#### IP Address Management")
                
                ip_strategy = st.selectbox(
                    "IP Allocation Strategy",
                    ["CIDR Block Allocation", "Dynamic Allocation", 
                     "Hybrid (Static + Dynamic)", "IPAM Managed"]
                )
                
                primary_cidr = st.text_input("Primary CIDR Block", "10.0.0.0/16")
                
                # DNS configuration
                st.markdown("#### DNS Configuration")
                
                dns_strategy = st.multiselect(
                    "DNS Services",
                    ["Route 53 (AWS)", "Azure DNS", "Cloud DNS (GCP)",
                     "Private DNS Zones", "Hybrid DNS", "Split-Horizon DNS"],
                    default=["Route 53 (AWS)", "Private DNS Zones"]
                )
            
            with col2:
                st.markdown("#### Network Diagram")
                
                st.info("📊 Network topology visualization")
                
                # Network zones
                st.markdown("**Network Zones:**")
                
                zones = [
                    {"Zone": "Public Zone", "CIDR": "10.0.0.0/20", "Purpose": "Internet-facing resources"},
                    {"Zone": "Private Zone", "CIDR": "10.0.16.0/20", "Purpose": "Internal applications"},
                    {"Zone": "Database Zone", "CIDR": "10.0.32.0/20", "Purpose": "Data tier"},
                    {"Zone": "Management Zone", "CIDR": "10.0.48.0/20", "Purpose": "Admin & monitoring"}
                ]
                
                st.dataframe(zones, use_container_width=True)
                
                # Connectivity matrix
                st.markdown("#### Connectivity Matrix")
                
                st.info("🔗 Shows allowed connections between zones")
                
                # Connection rules
                connections = st.multiselect(
                    "Allowed Connections",
                    ["Public → Private", "Private → Database", 
                     "Management → All Zones", "Internet → Public Only"],
                    default=["Public → Private", "Private → Database", "Management → All Zones"]
                )
                
                if st.button("Generate Network Configuration", key="gen_network_config"):
                    st.success("✅ Network configuration generated")
                    self._show_network_configuration(topology, components)
        
        with conn_tab2:
            st.markdown("### Hybrid Connectivity Setup")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### Connection Types")
                
                # Primary connection
                primary_conn = st.selectbox(
                    "Primary Connection",
                    ["AWS Direct Connect", "Azure ExpressRoute", 
                     "GCP Dedicated Interconnect", "VPN (IPSec)"]
                )
                
                # Connection details
                bandwidth = st.selectbox(
                    "Bandwidth",
                    ["50 Mbps", "100 Mbps", "200 Mbps", "500 Mbps", 
                     "1 Gbps", "10 Gbps", "100 Gbps"]
                )
                
                # Redundancy
                st.markdown("#### Redundancy Configuration")
                
                enable_redundancy = st.checkbox("Enable Redundant Connection", value=True)
                
                if enable_redundancy:
                    secondary_conn = st.selectbox(
                        "Secondary Connection",
                        ["AWS Direct Connect (Secondary)", "Azure ExpressRoute (Secondary)",
                         "VPN (Backup)", "SD-WAN", "Internet Backup"]
                    )
                    
                    failover_mode = st.selectbox(
                        "Failover Mode",
                        ["Active-Active", "Active-Passive", "Active-Standby"]
                    )
                
                # Routing
                st.markdown("#### Routing Configuration")
                
                routing_protocol = st.selectbox(
                    "Routing Protocol",
                    ["BGP", "Static Routes", "OSPF", "EIGRP"]
                )
                
                bgp_asn = st.text_input("BGP ASN", "65000") if routing_protocol == "BGP" else None
            
            with col2:
                st.markdown("#### Connection Status")
                
                # Status metrics
                st.markdown("**Live Connection Metrics:**")
                
                status_col1, status_col2 = st.columns(2)
                
                with status_col1:
                    st.metric("Primary Link", "Active", delta="99.99% uptime")
                    st.metric("Latency", "5.2 ms", delta="-0.3 ms")
                
                with status_col2:
                    # Mode-aware metric
            secondary_link_value = self._get_data('secondary_link', "Standby")
            st.metric("Secondary Link", secondary_link_value)
                    st.metric("Throughput", "890 Mbps", delta="+120 Mbps")
                
                # Connection health
                st.markdown("#### Connection Health")
                
                health_checks = [
                    {"Check": "Link Status", "Status": "✅ Healthy", "Last Check": "30s ago"},
                    {"Check": "Routing", "Status": "✅ Healthy", "Last Check": "1m ago"},
                    {"Check": "Bandwidth", "Status": "✅ Normal", "Last Check": "45s ago"},
                    {"Check": "Packet Loss", "Status": "✅ < 0.01%", "Last Check": "30s ago"}
                ]
                
                st.dataframe(health_checks, use_container_width=True, hide_index=True)
                
                # Traffic statistics
                st.markdown("#### Traffic Statistics (24h)")
                
                st.line_chart({
                    "00:00": 450, "06:00": 780, "12:00": 920,
                    "18:00": 850, "24:00": 620
                })
        
        with conn_tab3:
            st.markdown("### Security Zones & Segmentation")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### Security Zone Definition")
                
                # Zone configuration
                zone_name = st.text_input("Zone Name", "DMZ-Public-Web")
                
                zone_type = st.selectbox(
                    "Zone Type",
                    ["Public DMZ", "Private Application", "Database Tier",
                     "Management", "Development", "Production"]
                )
                
                trust_level = st.select_slider(
                    "Trust Level",
                    options=["Untrusted", "Low", "Medium", "High", "Trusted"],
                    value="Low"
                )
                
                # Segmentation strategy
                st.markdown("#### Segmentation Strategy")
                
                segmentation = st.multiselect(
                    "Segmentation Methods",
                    ["Network ACLs", "Security Groups", "NSGs (Azure)",
                     "VPC Peering Controls", "Microsegmentation", "Zero Trust"],
                    default=["Network ACLs", "Security Groups"]
                )
                
                # Access controls
                st.markdown("#### Access Controls")
                
                inbound_rules = st.text_area(
                    "Inbound Rules (one per line)",
                    "HTTPS from 0.0.0.0/0\nSSH from 10.0.48.0/20 (Mgmt)"
                )
                
                outbound_rules = st.text_area(
                    "Outbound Rules (one per line)",
                    "HTTPS to 0.0.0.0/0\nMySQL to 10.0.32.0/20 (DB)"
                )
            
            with col2:
                st.markdown("#### Zone Map")
                
                st.info("🗺️ Security zone visualization")
                
                # Zone summary
                zones_summary = [
                    {"Zone": "Public DMZ", "Trust": "Untrusted", "Resources": 45, "Threats": "High"},
                    {"Zone": "Private App", "Trust": "Medium", "Resources": 234, "Threats": "Medium"},
                    {"Zone": "Database", "Trust": "High", "Resources": 67, "Threats": "Low"},
                    {"Zone": "Management", "Trust": "Trusted", "Resources": 12, "Threats": "Low"}
                ]
                
                st.dataframe(zones_summary, use_container_width=True)
                
                # Security posture
                st.markdown("#### Security Posture")
                
                posture_col1, posture_col2 = st.columns(2)
                
                with posture_col1:
                    # Mode-aware metric
            zones_configured_value = self._get_data('zones_configured', "4")
            st.metric("Zones Configured", zones_configured_value)
                    # Mode-aware metric
            active_rules_value = self._get_data('active_rules', "156")
            st.metric("Active Rules", active_rules_value)
                
                with posture_col2:
                    # Mode-aware metric
            blocked_attempts_(24h)_value = self._get_data('blocked_attempts_(24h)', "1,234")
            st.metric("Blocked Attempts (24h)", blocked_attempts_(24h)_value)
                    # Mode-aware metric
            security_score_value = self._get_data('security_score', "94/100")
            security_score_delta = self._get_data('security_score_delta', "+3")
            st.metric("Security Score", security_score_value, security_score_delta)
                
                # Threat detection
                st.markdown("#### Threat Detection")
                
                enable_ids = st.checkbox("Enable IDS/IPS", value=True)
                enable_waf = st.checkbox("Enable WAF", value=True)
                enable_ddos = st.checkbox("Enable DDoS Protection", value=True)
        
        with conn_tab4:
            st.markdown("### Traffic Management & Optimization")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### Traffic Routing")
                
                # Load balancing
                lb_strategy = st.selectbox(
                    "Load Balancing Strategy",
                    ["Round Robin", "Least Connections", "Weighted",
                     "IP Hash", "Geographic", "Latency-Based"]
                )
                
                # Traffic distribution
                st.markdown("#### Traffic Distribution")
                
                distribution = st.multiselect(
                    "Distribution Methods",
                    ["Geographic Routing", "Latency-Based Routing",
                     "Weighted Routing", "Failover Routing", "Multivalue Answer"],
                    default=["Geographic Routing", "Latency-Based Routing"]
                )
                
                # QoS
                st.markdown("#### Quality of Service (QoS)")
                
                enable_qos = st.checkbox("Enable QoS", value=True)
                
                if enable_qos:
                    priority_traffic = st.multiselect(
                        "Priority Traffic Types",
                        ["Real-time Video", "Voice (VoIP)", "Interactive Apps",
                         "Streaming Media", "File Transfer", "Backup"],
                        default=["Real-time Video", "Voice (VoIP)"]
                    )
                
                # Traffic shaping
                st.markdown("#### Traffic Shaping")
                
                enable_shaping = st.checkbox("Enable Traffic Shaping", value=False)
                
                if enable_shaping:
                    rate_limit = st.number_input("Rate Limit (Mbps)", min_value=1, value=100)
                    burst_size = st.number_input("Burst Size (MB)", min_value=1, value=10)
            
            with col2:
                st.markdown("#### Traffic Analytics")
                
                # Real-time metrics
                st.markdown("**Real-Time Traffic:**")
                
                traffic_col1, traffic_col2 = st.columns(2)
                
                with traffic_col1:
                    # Mode-aware metric
            current_traffic_value = self._get_data('current_traffic', "890 Mbps")
            st.metric("Current Traffic", current_traffic_value)
                    # Mode-aware metric
            active_connections_value = self._get_data('active_connections', "12,456")
            st.metric("Active Connections", active_connections_value)
                
                with traffic_col2:
                    # Mode-aware metric
            peak_traffic_value = self._get_data('peak_traffic', "1,234 Mbps")
            st.metric("Peak Traffic", peak_traffic_value)
                    # Mode-aware metric
            avg_latency_value = self._get_data('avg_latency', "45 ms")
            st.metric("Avg Latency", avg_latency_value)
                
                # Traffic breakdown
                st.markdown("#### Traffic Breakdown (24h)")
                
                traffic_data = {
                    "HTTP/HTTPS": 65,
                    "Database": 20,
                    "Storage": 10,
                    "Other": 5
                }
                
                for traffic_type, percentage in traffic_data.items():
                    st.progress(percentage / 100)
                    st.caption(f"{traffic_type}: {percentage}%")
                
                # Top talkers
                st.markdown("#### Top Talkers")
                
                talkers = [
                    {"Source": "10.0.1.45", "Destination": "10.0.32.10", "Traffic": "145 Mbps"},
                    {"Source": "10.0.2.78", "Destination": "0.0.0.0/0", "Traffic": "98 Mbps"},
                    {"Source": "10.0.1.23", "Destination": "10.0.32.15", "Traffic": "67 Mbps"}
                ]
                
                st.dataframe(talkers, use_container_width=True, hide_index=True)
    
    def _render_global_management(self):
        """Global Environment Management"""
        st.subheader("🌍 Global Environment Management")
        
        # Global management tabs
        global_tab1, global_tab2, global_tab3, global_tab4 = st.tabs([
            "Multi-Region Architecture", "Global Load Balancing", "Data Residency", "Disaster Recovery"
        ])
        
        with global_tab1:
            st.markdown("### Multi-Region Architecture")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### Region Configuration")
                
                # Primary regions
                primary_regions = st.multiselect(
                    "Primary Regions",
                    ["us-east-1 (N. Virginia)", "us-west-2 (Oregon)", 
                     "eu-west-1 (Ireland)", "eu-central-1 (Frankfurt)",
                     "ap-southeast-1 (Singapore)", "ap-northeast-1 (Tokyo)",
                     "ap-south-1 (Mumbai)", "sa-east-1 (São Paulo)"],
                    default=["us-east-1 (N. Virginia)", "eu-west-1 (Ireland)", "ap-southeast-1 (Singapore)"]
                )
                
                # Secondary regions (DR)
                secondary_regions = st.multiselect(
                    "Secondary Regions (DR)",
                    ["us-west-1 (California)", "eu-west-2 (London)",
                     "ap-southeast-2 (Sydney)", "ca-central-1 (Canada)"],
                    default=["us-west-1 (California)", "eu-west-2 (London)"]
                )
                
                # Deployment strategy
                st.markdown("#### Deployment Strategy")
                
                strategy = st.selectbox(
                    "Multi-Region Strategy",
                    ["Active-Active (All Regions)", "Active-Passive (Failover)",
                     "Active-Active-Passive", "Geographic Distribution",
                     "Latency-Based Routing", "Pilot Light"]
                )
                
                # Replication
                st.markdown("#### Data Replication")
                
                replication_mode = st.selectbox(
                    "Replication Mode",
                    ["Synchronous", "Asynchronous", "Hybrid (Critical=Sync)"]
                )
                
                rpo = st.selectbox("RPO (Recovery Point Objective)", 
                                  ["0 (Sync)", "< 1 min", "< 5 min", "< 15 min", "< 1 hour"])
                rto = st.selectbox("RTO (Recovery Time Objective)",
                                  ["< 1 min", "< 5 min", "< 15 min", "< 1 hour", "< 4 hours"])
            
            with col2:
                st.markdown("#### Region Status Dashboard")
                
                # Region health
                st.markdown("**Region Health Status:**")
                
                for region in primary_regions:
                    region_name = region.split(" ")[0]
                    with st.expander(f"🌐 {region}", expanded=False):
                        col_r1, col_r2, col_r3 = st.columns(3)
                        with col_r1:
                            # Mode-aware metric
            status_value = self._get_data('status', "✅ Active")
            st.metric("Status", status_value)
                        with col_r2:
                            # Mode-aware metric
            resources_value = self._get_data('resources', "234")
            st.metric("Resources", resources_value)
                        with col_r3:
                            # Mode-aware metric
            latency_value = self._get_data('latency', "45 ms")
            st.metric("Latency", latency_value)
                
                # Global traffic distribution
                st.markdown("#### Global Traffic Distribution")
                
                st.info("📊 Traffic distribution across regions")
                
                traffic_dist = {
                    "us-east-1": 45,
                    "eu-west-1": 35,
                    "ap-southeast-1": 20
                }
                
                for region, percentage in traffic_dist.items():
                    st.progress(percentage / 100)
                    st.caption(f"{region}: {percentage}%")
                
                # Cost by region
                st.markdown("#### Cost by Region (Monthly)")
                
                costs = {
                    "us-east-1": "$78,500",
                    "eu-west-1": "$54,200",
                    "ap-southeast-1": "$32,800"
                }
                
                for region, cost in costs.items():
                    st.text(f"{region}: {cost}")
        
        with global_tab2:
            st.markdown("### Global Load Balancing")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### Load Balancing Configuration")
                
                # Global LB type
                glb_type = st.selectbox(
                    "Global Load Balancer Type",
                    ["AWS Global Accelerator", "Azure Traffic Manager", 
                     "GCP Cloud Load Balancing", "CloudFlare Load Balancing",
                     "Multi-Cloud DNS-Based LB"]
                )
                
                # Routing policies
                st.markdown("#### Routing Policies")
                
                routing_policies = st.multiselect(
                    "Select Routing Policies",
                    ["Geolocation", "Latency-Based", "Weighted", 
                     "Failover", "Geoproximity", "Multivalue"],
                    default=["Geolocation", "Latency-Based", "Failover"]
                )
                
                # Health checks
                st.markdown("#### Health Check Configuration")
                
                enable_health = st.checkbox("Enable Health Checks", value=True)
                
                if enable_health:
                    health_protocol = st.selectbox("Protocol", ["HTTPS", "HTTP", "TCP", "ICMP"])
                    health_interval = st.selectbox("Check Interval", ["10s", "30s", "60s"], index=1)
                    health_timeout = st.selectbox("Timeout", ["5s", "10s", "30s"], index=0)
                    failure_threshold = st.slider("Failure Threshold", 1, 10, 3)
                
                # Traffic weighting
                st.markdown("#### Traffic Weighting")
                
                for region in ["us-east-1", "eu-west-1", "ap-southeast-1"]:
                    weight = st.slider(f"{region} Weight", 0, 100, 33, 
                                      key=f"weight_{region}")
            
            with col2:
                st.markdown("#### Load Balancing Status")
                
                # Global metrics
                st.markdown("**Global Metrics:**")
                
                glb_col1, glb_col2 = st.columns(2)
                
                with glb_col1:
                    # Mode-aware metric
            total_requests_value = self._get_data('total_requests', "1.2M/hour")
            st.metric("Total Requests", total_requests_value)
                    # Mode-aware metric
            global_latency_value = self._get_data('global_latency', "67 ms")
            global_latency_delta = self._get_data('global_latency_delta', "-12 ms")
            st.metric("Global Latency", global_latency_value, global_latency_delta)
                
                with glb_col2:
                    # Mode-aware metric
            success_rate_value = self._get_data('success_rate', "99.97%")
            success_rate_delta = self._get_data('success_rate_delta', "+0.02%")
            st.metric("Success Rate", success_rate_value, success_rate_delta)
                    # Mode-aware metric
            failed_health_checks_value = self._get_data('failed_health_checks', "2")
            failed_health_checks_delta = self._get_data('failed_health_checks_delta', "-5")
            st.metric("Failed Health Checks", failed_health_checks_value, failed_health_checks_delta)
                
                # Endpoint status
                st.markdown("#### Endpoint Status")
                
                endpoints = [
                    {"Region": "us-east-1", "Status": "✅ Healthy", "Latency": "45 ms", "Load": "45%"},
                    {"Region": "eu-west-1", "Status": "✅ Healthy", "Latency": "52 ms", "Load": "35%"},
                    {"Region": "ap-southeast-1", "Status": "✅ Healthy", "Latency": "78 ms", "Load": "20%"},
                    {"Region": "us-west-1", "Status": "⚠️ Degraded", "Latency": "125 ms", "Load": "0%"}
                ]
                
                st.dataframe(endpoints, use_container_width=True, hide_index=True)
                
                # Traffic flow
                st.markdown("#### Traffic Flow (Last Hour)")
                
                st.line_chart({
                    "00:00": 800, "00:15": 950, "00:30": 1100,
                    "00:45": 1200, "01:00": 1050
                })
        
        with global_tab3:
            st.markdown("### Data Residency & Compliance")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### Data Residency Requirements")
                
                # Regulatory frameworks
                regulations = st.multiselect(
                    "Applicable Regulations",
                    ["GDPR (EU)", "CCPA (California)", "LGPD (Brazil)",
                     "PIPEDA (Canada)", "APPI (Japan)", "PDPA (Singapore)",
                     "Data Protection Act (UK)", "Schrems II"],
                    default=["GDPR (EU)", "CCPA (California)"]
                )
                
                # Data classification
                st.markdown("#### Data Classification")
                
                data_types = st.multiselect(
                    "Data Types to Manage",
                    ["Personal Identifiable Information (PII)", "Protected Health Information (PHI)",
                     "Financial Data", "Intellectual Property", "Government Data",
                     "Customer Data", "Employee Data", "Transactional Data"],
                    default=["Personal Identifiable Information (PII)", "Customer Data"]
                )
                
                # Residency rules
                st.markdown("#### Residency Rules")
                
                for regulation in regulations:
                    with st.expander(f"📍 {regulation} Requirements"):
                        if regulation == "GDPR (EU)":
                            st.markdown("**Data Storage:** Must remain in EU or adequate countries")
                            st.markdown("**Transfer Mechanism:** Standard Contractual Clauses (SCCs)")
                            allowed_regions = st.multiselect(
                                "Allowed Regions",
                                ["eu-west-1", "eu-central-1", "eu-west-2", "eu-north-1"],
                                default=["eu-west-1", "eu-central-1"],
                                key="gdpr_regions"
                            )
                        elif regulation == "CCPA (California)":
                            st.markdown("**Data Storage:** No specific location requirement")
                            st.markdown("**Transfer Mechanism:** Consumer consent required")
                            st.checkbox("Obtain explicit consent for transfers", value=True, key="ccpa_consent")
            
            with col2:
                st.markdown("#### Compliance Status")
                
                # Compliance dashboard
                st.markdown("**Data Residency Compliance:**")
                
                compliance_status = [
                    {"Regulation": "GDPR", "Status": "✅ Compliant", "Coverage": "100%"},
                    {"Regulation": "CCPA", "Status": "✅ Compliant", "Coverage": "100%"},
                    {"Regulation": "LGPD", "Status": "⚠️ Partial", "Coverage": "85%"},
                    {"Regulation": "PIPEDA", "Status": "✅ Compliant", "Coverage": "100%"}
                ]
                
                st.dataframe(compliance_status, use_container_width=True, hide_index=True)
                
                # Data location map
                st.markdown("#### Data Location Map")
                
                st.info("🗺️ Visualization of data storage locations")
                
                locations = [
                    {"Region": "EU (GDPR)", "Storage": "eu-west-1, eu-central-1", "Data": "PII, Customer"},
                    {"Region": "US (CCPA)", "Storage": "us-west-2", "Data": "Customer, Transaction"},
                    {"Region": "APAC", "Storage": "ap-southeast-1", "Data": "Customer, Analytics"}
                ]
                
                st.dataframe(locations, use_container_width=True, hide_index=True)
                
                # Violation alerts
                st.markdown("#### Compliance Alerts")
                
                st.warning("⚠️ 1 potential violation detected:")
                st.markdown("- Brazilian customer data found in us-east-1 (requires LGPD compliance)")
                
                if st.button("Auto-Remediate", key="remediate_violation"):
                    st.success("✅ Initiated data migration to sa-east-1")
        
        with global_tab4:
            st.markdown("### Global Disaster Recovery")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### DR Strategy")
                
                # DR approach
                dr_approach = st.selectbox(
                    "DR Approach",
                    ["Backup & Restore", "Pilot Light", "Warm Standby",
                     "Multi-Site Active-Active", "Hot Standby"]
                )
                
                # DR objectives
                st.markdown("#### DR Objectives")
                
                rpo_target = st.selectbox(
                    "RPO Target",
                    ["0 (Continuous)", "< 1 minute", "< 5 minutes", 
                     "< 15 minutes", "< 1 hour", "< 4 hours"],
                    index=2
                )
                
                rto_target = st.selectbox(
                    "RTO Target",
                    ["< 1 minute", "< 5 minutes", "< 15 minutes",
                     "< 1 hour", "< 4 hours", "< 24 hours"],
                    index=3
                )
                
                # DR regions
                st.markdown("#### DR Region Pairing")
                
                primary_dr = st.selectbox("Primary Region", 
                                         ["us-east-1", "eu-west-1", "ap-southeast-1"])
                
                dr_region = st.selectbox("DR Region",
                                        ["us-west-2", "eu-central-1", "ap-northeast-1"])
                
                # Replication
                st.markdown("#### Replication Configuration")
                
                replication_services = st.multiselect(
                    "Services to Replicate",
                    ["Compute (EC2/VMs)", "Databases (RDS/Azure SQL)", 
                     "Storage (S3/Blob)", "Kubernetes Clusters",
                     "Networking Config", "Security Policies", "IAM/RBAC"],
                    default=["Compute (EC2/VMs)", "Databases (RDS/Azure SQL)", "Storage (S3/Blob)"]
                )
                
                replication_freq = st.selectbox(
                    "Replication Frequency",
                    ["Continuous", "Every 5 minutes", "Every 15 minutes", 
                     "Hourly", "Daily", "On-Demand"]
                )
            
            with col2:
                st.markdown("#### DR Status & Testing")
                
                # DR health
                st.markdown("**DR Environment Health:**")
                
                dr_col1, dr_col2 = st.columns(2)
                
                with dr_col1:
                    # Mode-aware metric
            dr_status_value = self._get_data('dr_status', "✅ Ready")
            st.metric("DR Status", dr_status_value)
                    # Mode-aware metric
            last_test_value = self._get_data('last_test', "7 days ago")
            st.metric("Last Test", last_test_value)
                
                with dr_col2:
                    # Mode-aware metric
            replication_lag_value = self._get_data('replication_lag', "45 seconds")
            st.metric("Replication Lag", replication_lag_value)
                    # Mode-aware metric
            data_synced_value = self._get_data('data_synced', "98.7%")
            st.metric("Data Synced", data_synced_value)
                
                # DR testing
                st.markdown("#### DR Testing Schedule")
                
                test_frequency = st.selectbox(
                    "Test Frequency",
                    ["Weekly", "Monthly", "Quarterly", "Annually"]
                )
                
                next_test = st.date_input("Next Scheduled Test")
                
                if st.button("Initiate DR Test", key="dr_test"):
                    st.warning("⚠️ DR test initiated - switching to DR region")
                    st.info("🔄 Monitoring failover process...")
                
                # Failover history
                st.markdown("#### Recent DR Events")
                
                dr_events = [
                    {"Date": "2025-11-10", "Type": "Scheduled Test", "Duration": "45 min", "Result": "✅ Success"},
                    {"Date": "2025-10-15", "Type": "Scheduled Test", "Duration": "52 min", "Result": "✅ Success"},
                    {"Date": "2025-09-20", "Type": "Unplanned Failover", "Duration": "12 min", "Result": "✅ Success"}
                ]
                
                st.dataframe(dr_events, use_container_width=True, hide_index=True)
                
                # Runbook
                st.markdown("#### DR Runbook")
                
                if st.button("View DR Runbook", key="view_runbook"):
                    st.success("📖 DR Runbook opened")
                    st.markdown("""
                    **Quick Reference:**
                    1. Initiate failover from primary console
                    2. Verify DR region health
                    3. Update DNS records (automated)
                    4. Monitor application health
                    5. Notify stakeholders
                    """)
    
    # Helper methods
    
    def _show_provisioning_templates(self, providers, iac_tool):
        """Show provisioning templates"""
        st.markdown("#### Generated Templates")
        
        with st.expander("View Terraform Configuration"):
            st.code(f"""
# Multi-Cloud Provisioning - {iac_tool}
# Providers: {', '.join(providers)}

terraform {{
  required_providers {{
    aws = {{
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }}
    azurerm = {{
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }}
    google = {{
      source  = "hashicorp/google"
      version = "~> 5.0"
    }}
  }}
}}

# AWS Configuration
provider "aws" {{
  region = "us-east-1"
}}

# Azure Configuration
provider "azurerm" {{
  features {{}}
}}

# GCP Configuration
provider "google" {{
  project = "my-project-id"
  region  = "us-central1"
}}

# Resources will be provisioned here
            """, language="hcl")
    
    def _show_provisioning_workflow(self, providers, onprem_type):
        """Show provisioning workflow"""
        st.markdown("#### Provisioning Workflow")
        
        workflow = f"""
        1. **Planning Phase**
           - Validate requirements across {', '.join(providers)}
           - Check resource quotas and limits
           - Verify network connectivity
        
        2. **Pre-Provisioning**
           - Initialize {onprem_type} integration
           - Set up hybrid connectivity
           - Configure identity federation
        
        3. **Provisioning**
           - Deploy infrastructure in parallel
           - Configure cross-cloud networking
           - Set up monitoring and logging
        
        4. **Validation**
           - Run connectivity tests
           - Verify data synchronization
           - Check compliance status
        
        5. **Post-Provisioning**
           - Update CMDB
           - Configure backup policies
           - Enable monitoring alerts
        """
        
        st.markdown(workflow)
    
    def _show_policy_definition(self, name, scope, rules):
        """Show generated policy definition"""
        with st.expander("View Generated Policy"):
            st.code(f"""
{{
  "policyName": "{name}",
  "version": "1.0",
  "scope": {json.dumps(scope)},
  "rules": {json.dumps(rules)},
  "enforcement": "hard",
  "createdAt": "{datetime.now().isoformat()}",
  "cloudTranslations": {{
    "aws": {{
      "type": "ServiceControlPolicy",
      "actions": ["Deny"],
      "resources": ["*"]
    }},
    "azure": {{
      "type": "AzurePolicy",
      "effect": "Deny"
    }},
    "gcp": {{
      "type": "OrganizationPolicy",
      "constraint": "constraints/custom"
    }}
  }}
}}
            """, language="json")
    
    def _get_framework_controls(self, framework):
        """Get compliance framework controls"""
        controls_map = {
            "ISO 27001": [
                {"id": "A.5.1", "name": "Information Security Policies"},
                {"id": "A.6.1", "name": "Internal Organization"},
                {"id": "A.7.1", "name": "Prior to Employment"},
                {"id": "A.8.1", "name": "Responsibility for Assets"},
                {"id": "A.9.1", "name": "Business Requirements"}
            ],
            "SOC 2 Type II": [
                {"id": "CC1.1", "name": "Control Environment"},
                {"id": "CC2.1", "name": "Communication & Information"},
                {"id": "CC3.1", "name": "Risk Assessment"},
                {"id": "CC4.1", "name": "Monitoring Activities"},
                {"id": "CC5.1", "name": "Control Activities"}
            ],
            "PCI DSS 4.0": [
                {"id": "1.1", "name": "Network Security Controls"},
                {"id": "2.1", "name": "Secure Configurations"},
                {"id": "3.1", "name": "Stored Account Data Protection"},
                {"id": "4.1", "name": "Transmission Protection"},
                {"id": "5.1", "name": "Malware Protection"}
            ]
        }
        
        return controls_map.get(framework, [])
    
    def _get_compliance_matrix(self, frameworks):
        """Get compliance mapping matrix"""
        return {
            "Control": ["Access Control", "Encryption", "Logging", "Network Security", "Backup"],
            "ISO 27001": ["✅ A.9.1", "✅ A.10.1", "✅ A.12.4", "✅ A.13.1", "✅ A.12.3"],
            "SOC 2": ["✅ CC6.1", "✅ CC6.7", "✅ CC7.2", "✅ CC6.6", "✅ CC7.5"],
            "PCI DSS": ["✅ Req 7", "✅ Req 4", "✅ Req 10", "✅ Req 1", "✅ Req 9"]
        }
    
    def _show_optimization_plan(self):
        """Show optimization plan"""
        with st.expander("View Optimization Plan"):
            st.markdown("""
            ### Cost Optimization Plan
            
            **Phase 1: Quick Wins (Week 1-2)**
            - Implement Reserved Instances for predictable workloads
            - Enable S3 lifecycle policies
            - Remove unused snapshots and volumes
            - **Expected Savings:** $15,000/month
            
            **Phase 2: Right-Sizing (Week 3-4)**
            - Downsize over-provisioned instances
            - Optimize database configurations
            - Implement auto-scaling policies
            - **Expected Savings:** $18,000/month
            
            **Phase 3: Advanced Optimization (Month 2)**
            - Implement spot instances for non-critical workloads
            - Optimize data transfer costs
            - Consolidate underutilized resources
            - **Expected Savings:** $12,000/month
            
            **Total Expected Savings:** $45,000/month (65% of target)
            """)
    
    def _get_aws_best_practices(self, categories):
        """Get AWS best practices"""
        practices = []
        
        if "Security" in categories:
            practices.extend([
                {
                    "title": "Enable MFA for Root Account",
                    "category": "Security",
                    "priority": "Critical",
                    "description": "Always enable multi-factor authentication for AWS root account",
                    "implementation": "IAM Console → Root User → Enable MFA → Follow setup wizard"
                },
                {
                    "title": "Use IAM Roles Instead of Access Keys",
                    "category": "Security",
                    "priority": "High",
                    "description": "Prefer IAM roles over long-term access keys for EC2 and Lambda",
                    "implementation": "Create IAM role → Attach to EC2/Lambda → Remove access keys"
                }
            ])
        
        if "Cost Optimization" in categories:
            practices.extend([
                {
                    "title": "Implement S3 Lifecycle Policies",
                    "category": "Cost Optimization",
                    "priority": "Medium",
                    "description": "Automatically transition objects to cheaper storage classes",
                    "implementation": "S3 → Bucket → Management → Lifecycle Rules → Add transitions"
                },
                {
                    "title": "Use Reserved Instances for Steady Workloads",
                    "category": "Cost Optimization",
                    "priority": "High",
                    "description": "Purchase RIs for predictable workloads to save up to 75%",
                    "implementation": "EC2 → Reserved Instances → Purchase → Select term & payment"
                }
            ])
        
        if "Reliability" in categories:
            practices.extend([
                {
                    "title": "Design for Failure",
                    "category": "Reliability",
                    "priority": "Critical",
                    "description": "Deploy across multiple AZs and use Auto Scaling",
                    "implementation": "Use Multi-AZ deployments → Enable Auto Scaling → Test failover"
                }
            ])
        
        return practices
    
    def _get_azure_best_practices(self, categories):
        """Get Azure best practices"""
        practices = []
        
        if "Security" in categories:
            practices.append({
                "title": "Enable Azure AD Conditional Access",
                "category": "Security",
                "priority": "High",
                "description": "Implement conditional access policies for enhanced security",
                "implementation": "Azure AD → Security → Conditional Access → New Policy"
            })
        
        if "Cost Optimization" in categories:
            practices.append({
                "title": "Use Azure Hybrid Benefit",
                "category": "Cost Optimization",
                "priority": "High",
                "description": "Save on Windows VMs by using existing licenses",
                "implementation": "VM → Configuration → Licensing → Enable Hybrid Benefit"
            })
        
        return practices
    
    def _get_gcp_best_practices(self, categories):
        """Get GCP best practices"""
        practices = []
        
        if "Security" in categories:
            practices.append({
                "title": "Use Organization Policies",
                "category": "Security",
                "priority": "High",
                "description": "Enforce security controls across all projects",
                "implementation": "IAM & Admin → Organization Policies → Create Policy"
            })
        
        if "Cost Optimization" in categories:
            practices.append({
                "title": "Enable Committed Use Discounts",
                "category": "Cost Optimization",
                "priority": "Medium",
                "description": "Purchase 1 or 3-year commitments for predictable savings",
                "implementation": "Billing → Commitments → Purchase → Select resources"
            })
        
        return practices
    
    def _show_network_configuration(self, topology, components):
        """Show network configuration"""
        with st.expander("View Network Configuration"):
            st.code(f"""
# Network Configuration
# Topology: {topology}
# Components: {', '.join(components)}

network:
  topology: {topology}
  
  vpc:
    cidr: 10.0.0.0/16
    
  subnets:
    public:
      - name: public-subnet-1
        cidr: 10.0.0.0/20
        az: us-east-1a
    private:
      - name: private-subnet-1
        cidr: 10.0.16.0/20
        az: us-east-1a
    database:
      - name: db-subnet-1
        cidr: 10.0.32.0/20
        az: us-east-1a
  
  routing:
    transit_gateway: enabled
    route_tables:
      - name: public-rt
        routes:
          - destination: 0.0.0.0/0
            target: internet-gateway
      - name: private-rt
        routes:
          - destination: 0.0.0.0/0
            target: nat-gateway
            """, language="yaml")

# Demo data if needed
def get_demo_data():
    """Return demo data for the module"""
    return {
        "clouds": ["AWS", "Azure", "GCP"],
        "regions": ["us-east-1", "eu-west-1", "ap-southeast-1"],
        "policies": 87,
        "compliance_score": 94
    }
