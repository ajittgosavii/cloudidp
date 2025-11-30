"""
Auto-Fix Hardcoded Metrics - Make Mode-Aware
This script automatically converts hardcoded st.metric() calls to mode-aware versions

Run: python auto_fix_metrics.py
"""

import re
import os
from pathlib import Path

# Files to fix
FILES_TO_FIX = [
    'module_08_multicloud_hybrid.py',
    'module_09_developer_experience.py',
    'finops_module.py',
    'module_07_abstraction.py',
    'module_10_observability.py',
    'design_planning.py',
    'provisioning_deployment.py',
    'security_compliance.py',
    'policy_guardrails.py',
    'ondemand_operations.py',
    'ondemand_operations_part2.py'
]

def add_get_data_method(content):
    """Add _get_data helper method to class"""
    
    helper_method = '''
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
'''
    
    # Find where to insert (after __init__ method)
    init_pattern = r'(def __init__\(self.*?\):.*?(?=\n    def ))'
    match = re.search(init_pattern, content, re.DOTALL)
    
    if match:
        insert_pos = match.end()
        content = content[:insert_pos] + '\n' + helper_method + '\n' + content[insert_pos:]
    
    return content

def fix_metric_calls(content):
    """Convert hardcoded st.metric() calls to mode-aware versions"""
    
    # Pattern to match st.metric() calls with hardcoded values
    # Matches: st.metric("Name", "Value", "Delta")
    pattern = r'st\.metric\(\s*["\']([^"\']+)["\']\s*,\s*["\']([^"\']+)["\']\s*(?:,\s*["\']([^"\']+)["\']\s*)?\)'
    
    def replace_metric(match):
        metric_name = match.group(1)
        metric_value = match.group(2)
        metric_delta = match.group(3) if match.group(3) else None
        
        # Create a key from metric name
        key = metric_name.lower().replace(' ', '_').replace('/', '_').replace('%', 'pct')
        
        # Generate replacement code
        if metric_delta:
            return f'''# Mode-aware metric
            {key}_value = self._get_data('{key}', "{metric_value}")
            {key}_delta = self._get_data('{key}_delta', "{metric_delta}")
            st.metric("{metric_name}", {key}_value, {key}_delta)'''
        else:
            return f'''# Mode-aware metric
            {key}_value = self._get_data('{key}', "{metric_value}")
            st.metric("{metric_name}", {key}_value)'''
    
    # Replace all matches
    fixed_content = re.sub(pattern, replace_metric, content)
    
    return fixed_content

def add_mode_indicator(content):
    """Add mode indicator to render method"""
    
    mode_indicator = '''
        # Show current mode
        is_demo = st.session_state.get('mode', 'Demo') == 'Demo'
        if is_demo:
            st.info("📊 Demo Mode: Showing sample data")
        else:
            st.success("🔴 Live Mode: Showing real data")
        
'''
    
    # Find render method and add indicator
    render_pattern = r'(def render\(self\):.*?st\.header\([^)]+\))'
    match = re.search(render_pattern, content, re.DOTALL)
    
    if match:
        insert_pos = match.end()
        content = content[:insert_pos] + '\n' + mode_indicator + content[insert_pos:]
    
    return content

def process_file(file_path):
    """Process a single file"""
    
    print(f"\nProcessing: {file_path}")
    print("-" * 60)
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    try:
        # Read file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_size = len(content)
        
        # Count metrics before
        metrics_before = len(re.findall(r'st\.metric\(', content))
        
        # Apply fixes
        print("Adding _get_data method...")
        content = add_get_data_method(content)
        
        print("Converting hardcoded metrics...")
        content = fix_metric_calls(content)
        
        print("Adding mode indicator...")
        content = add_mode_indicator(content)
        
        # Count metrics after
        metrics_after = len(re.findall(r'st\.metric\(', content))
        
        # Save to new file
        output_path = file_path.replace('.py', '_LIVE_ENABLED.py')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Created: {output_path}")
        print(f"   - Original metrics: {metrics_before}")
        print(f"   - Updated metrics: {metrics_after}")
        print(f"   - File size: {original_size} → {len(content)} bytes")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("=" * 80)
    print("CloudIDP Auto-Fix: Convert Hardcoded Metrics to Mode-Aware")
    print("=" * 80)
    print()
    print("This script will:")
    print("1. Add _get_data() helper method to each module")
    print("2. Convert all hardcoded st.metric() calls to mode-aware versions")
    print("3. Add mode indicator to show Demo vs Live")
    print()
    print("Output files will be named: *_LIVE_ENABLED.py")
    print()
    
    input("Press Enter to continue...")
    
    success_count = 0
    fail_count = 0
    
    for file in FILES_TO_FIX:
        if process_file(file):
            success_count += 1
        else:
            fail_count += 1
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"✅ Successfully processed: {success_count}")
    print(f"❌ Failed: {fail_count}")
    print()
    print("Next steps:")
    print("1. Review the *_LIVE_ENABLED.py files")
    print("2. Test one file first")
    print("3. If it works, replace originals:")
    print("   copy module_08_multicloud_hybrid_LIVE_ENABLED.py module_08_multicloud_hybrid.py")
    print()
    print("4. Implement live data fetching in _get_data() method")
    print("   - Replace TODO comments with actual data fetching logic")
    print("   - Connect to your AWS/database services")
    print()

if __name__ == "__main__":
    main()
