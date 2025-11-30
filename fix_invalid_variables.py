"""
Fix Invalid Variable Names in Auto-Fixed Files
Replaces invalid Python variable names with valid ones

Run: python fix_invalid_variables.py
"""

import re
import os

# Files that need fixing
FILES_TO_FIX = [
    'finops_module.py',
    'module_08_multicloud_hybrid.py',
    'module_09_developer_experience.py',
    'module_10_observability.py',
    'policy_guardrails.py',
    'security_compliance.py'
]

def fix_variable_names(content):
    """Fix invalid variable names"""
    
    # Pattern 1: Fix (24h) -> _24h
    # anomalies_(24h)_value -> anomalies_24h_value
    content = re.sub(r'_\(24h\)', '_24h', content)
    
    # Pattern 2: Fix (>80pct) -> _gt80pct
    # at_risk_(>80pct)_value -> at_risk_gt80pct_value
    content = re.sub(r'_\(>(\d+)pct\)', r'_gt\1pct', content)
    
    # Pattern 3: Fix (<value) -> _lt{value}
    content = re.sub(r'_\(<(\d+)\)', r'_lt\1', content)
    
    # Pattern 4: Fix any remaining parentheses
    content = re.sub(r'_\(([^)]+)\)', r'_\1', content)
    
    # Pattern 5: Remove any remaining invalid characters from variable names
    # This is more aggressive - finds variable_name = and cleans it
    def clean_var_name(match):
        var_name = match.group(1)
        # Remove invalid characters
        var_name = var_name.replace('(', '').replace(')', '')
        var_name = var_name.replace('>', 'gt')
        var_name = var_name.replace('<', 'lt')
        var_name = var_name.replace('%', 'pct')
        var_name = var_name.replace('/', '_')
        var_name = var_name.replace('-', '_')
        var_name = var_name.replace(' ', '_')
        return var_name + ' ='
    
    # Fix variable assignments
    content = re.sub(r'([a-zA-Z_][a-zA-Z0-9_()<>%/\-]*)\s*=', clean_var_name, content)
    
    return content

def fix_indentation(content):
    """Fix indentation issues"""
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        # Check if line starts with unexpected spaces after a def or class
        if i > 0 and line.strip() and not line[0].isspace():
            prev_line = lines[i-1].strip()
            if prev_line.endswith(':'):
                # This line should be indented
                line = '    ' + line
        
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def process_file(filepath):
    """Process a single file"""
    
    print(f"\nProcessing: {filepath}")
    print("-" * 60)
    
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return False
    
    try:
        # Read file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix variable names
        print("Fixing invalid variable names...")
        content = fix_variable_names(content)
        
        # Fix indentation (only for security_compliance.py)
        if 'security_compliance' in filepath:
            print("Fixing indentation...")
            content = fix_indentation(content)
        
        # Check if anything changed
        if content == original_content:
            print("⚠️  No changes needed")
            return True
        
        # Save fixed version
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Fixed: {filepath}")
        
        # Verify syntax
        import py_compile
        try:
            py_compile.compile(filepath, doraise=True)
            print(f"✅ Syntax valid!")
            return True
        except Exception as e:
            print(f"⚠️  Warning: Still has syntax issues: {e}")
            return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("=" * 80)
    print("Fix Invalid Variable Names")
    print("=" * 80)
    print()
    print("This will fix:")
    print("  - anomalies_(24h) → anomalies_24h")
    print("  - violations_(24h) → violations_24h")
    print("  - at_risk_(>80pct) → at_risk_gt80pct")
    print("  - Indentation issues")
    print()
    
    success = 0
    failed = 0
    
    for filepath in FILES_TO_FIX:
        if process_file(filepath):
            success += 1
        else:
            failed += 1
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"✅ Successfully fixed: {success}")
    print(f"❌ Failed: {failed}")
    
    if success > 0:
        print("\n🎉 Files fixed! Run check_syntax.py to verify.")

if __name__ == "__main__":
    main()
