#!/usr/bin/env python3
"""
Auto-Fix Script for CloudIDP Modules
Automatically adds render() methods to modules that are missing them
"""

import re
import sys
from pathlib import Path

def find_render_methods(content):
    """Find all render_* methods in a module"""
    pattern = r'def (render_\w+)\('
    methods = re.findall(pattern, content)
    return [m for m in methods if m != 'render']  # Exclude main render if it exists

def has_render_method(content):
    """Check if module already has a render() method"""
    return bool(re.search(r'def render\(self\):', content))

def get_class_name(content):
    """Extract the class name from the module"""
    match = re.search(r'class (\w+):', content)
    return match.group(1) if match else None

def create_render_method(render_methods, class_name):
    """Generate a render() method that calls all render_* methods"""
    
    # Create friendly tab names from method names
    tab_names = []
    for method in render_methods:
        # Convert render_blueprint_definition to "Blueprints"
        name = method.replace('render_', '').replace('_', ' ').title()
        # Shorten common names
        name = name.replace('Definition', '').replace('Standards', '').strip()
        tab_names.append(name)
    
    # Generate the render method
    render_code = f'''    def render(self):
        """Main render method - organizes all sub-features in tabs"""
        
        st.markdown("## {class_name.replace('Module', '').replace('_', ' ').title()}")
        
        # Create tabs for each sub-feature
        tabs = st.tabs([
'''
    
    # Add tab names
    for i, tab_name in enumerate(tab_names):
        emoji = "📋" if i == 0 else "⚙️"  # Simple emoji
        render_code += f'            "{emoji} {tab_name}",\n'
    
    render_code = render_code.rstrip(',\n') + '\n        ])\n        \n'
    
    # Add tab content
    for i, method in enumerate(render_methods):
        render_code += f'''        with tabs[{i}]:
            self.{method}()
        
'''
    
    return render_code.rstrip() + '\n'

def fix_module(file_path):
    """Add render() method to a module file"""
    
    print(f"\nProcessing {file_path.name}...")
    print("-" * 60)
    
    # Read the file with UTF-8 encoding (fixes Windows encoding issues)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        print("❌ Unicode decode error - trying with error handling")
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            print(f"❌ Could not read file: {e}")
            return False
    
    # Check if it already has render()
    if has_render_method(content):
        print("✅ Already has render() method - skipping")
        return False
    
    # Find all render_* methods
    render_methods = find_render_methods(content)
    
    if not render_methods:
        print("⚠️  No render_* methods found - manual review needed")
        return False
    
    print(f"Found {len(render_methods)} render methods:")
    for method in render_methods:
        print(f"  - {method}()")
    
    # Get class name
    class_name = get_class_name(content)
    if not class_name:
        print("❌ Could not find class definition - manual review needed")
        return False
    
    print(f"Class: {class_name}")
    
    # Generate the render method
    render_method = create_render_method(render_methods, class_name)
    
    # Find where to insert (after class definition, before first method)
    class_pattern = rf'class {class_name}:.*?\n.*?""".*?"""'
    match = re.search(class_pattern, content, re.DOTALL)
    
    if not match:
        # Try simpler pattern
        match = re.search(rf'class {class_name}:.*?\n', content)
    
    if not match:
        print("❌ Could not find insertion point - manual review needed")
        return False
    
    # Insert the render method
    insert_pos = match.end()
    new_content = content[:insert_pos] + '\n' + render_method + '\n' + content[insert_pos:]
    
    # Write the fixed file with UTF-8 encoding
    output_path = file_path.parent / f"{file_path.stem}_FIXED.py"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Created {output_path.name}")
    print(f"   Added render() method with {len(render_methods)} tabs")
    
    return True

def main():
    print("=" * 60)
    print("CloudIDP Module Auto-Fix")
    print("=" * 60)
    print("\nThis script adds render() methods to modules that need them.")
    print()
    
    # Module files to fix
    modules = [
        "design_planning.py",
        "provisioning_deployment.py",
        "ondemand_operations.py",
        "ondemand_operations_part2.py",
        "finops_module.py",
        "security_compliance.py",
        "policy_guardrails.py",
        "module_07_abstraction.py",
        "module_08_multicloud_hybrid.py",
        "module_09_developer_experience.py",
        "module_10_observability.py",
    ]
    
    # Check current directory
    current_dir = Path(".")
    
    fixed_count = 0
    skipped_count = 0
    error_count = 0
    
    for module_name in modules:
        module_path = current_dir / module_name
        
        if not module_path.exists():
            print(f"\n⚠️  {module_name} - File not found, skipping")
            skipped_count += 1
            continue
        
        try:
            result = fix_module(module_path)
            if result:
                fixed_count += 1
            else:
                skipped_count += 1
        except Exception as e:
            print(f"❌ Error processing {module_name}: {e}")
            error_count += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"\n✅ Fixed: {fixed_count}")
    print(f"⚠️  Skipped: {skipped_count}")
    print(f"❌ Errors: {error_count}")
    
    if fixed_count > 0:
        print("\n" + "=" * 60)
        print("NEXT STEPS")
        print("=" * 60)
        print("""
1. Review the *_FIXED.py files to ensure they look correct
2. Replace your original files:
   
   cp design_planning_FIXED.py design_planning.py
   cp provisioning_deployment_FIXED.py provisioning_deployment.py
   # ... etc for all fixed files

3. Run the diagnostic:
   
   python diagnostic_modules.py

4. Deploy:
   
   streamlit run streamlit_app.py

All done!
""")

if __name__ == "__main__":
    main()
