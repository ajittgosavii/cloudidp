"""
Find Hardcoded Data in CloudIDP Modules
Run: python find_hardcoded_data.py
"""
import os
import re

# Module files to check
module_files = [
    'design_planning.py',
    'provisioning_deployment.py',
    'finops_module.py',
    'security_compliance.py',
    'policy_guardrails.py',
    'ondemand_operations.py',
    'ondemand_operations_part2.py',
    'module_07_abstraction.py',
    'module_08_multicloud_hybrid.py',
    'module_09_developer_experience.py',
    'module_10_observability.py',
    'streamlit_app.py',
    'api_gateway.py',
    'api_gateway_enhanced.py',
    'api_gateway_streamlit.py'
]

results = []

print("=" * 80)
print("CloudIDP Hardcoded Data Finder")
print("=" * 80)
print("\nSearching for hardcoded data in module files...\n")

for file in module_files:
    if not os.path.exists(file):
        continue
    
    try:
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')
        
        issues = {
            'demo_data_calls': [],
            'hardcoded_numbers': [],
            'hardcoded_dicts': [],
            'hardcoded_lists': []
        }
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Skip comments
            if stripped.startswith('#'):
                continue
            
            # Find demo_data calls
            if 'demo_data.' in line:
                issues['demo_data_calls'].append((i, stripped[:100]))
            
            # Find hardcoded metric values
            if re.search(r'st\.metric\([^,]+,\s*["\']?\d+', line):
                issues['hardcoded_numbers'].append((i, stripped[:100]))
            
            # Find hardcoded assignments with numbers
            if re.search(r'\w+\s*=\s*\d+\.?\d*\s*(?:#|$)', line):
                issues['hardcoded_numbers'].append((i, stripped[:100]))
            
            # Find hardcoded dicts
            if re.search(r'\w+\s*=\s*\{', line) and '{' in line:
                issues['hardcoded_dicts'].append((i, stripped[:100]))
            
            # Find hardcoded lists  
            if re.search(r'\w+\s*=\s*\[', line) and '[' in line:
                issues['hardcoded_lists'].append((i, stripped[:100]))
        
        total_issues = (
            len(issues['demo_data_calls']) + 
            len(issues['hardcoded_numbers']) + 
            len(issues['hardcoded_dicts']) + 
            len(issues['hardcoded_lists'])
        )
        
        if total_issues > 0:
            results.append({
                'file': file,
                'total': total_issues,
                'issues': issues
            })
    
    except Exception as e:
        print(f"Error processing {file}: {e}")

# Sort by total issues
results.sort(key=lambda x: x['total'], reverse=True)

# Print summary
print("\n" + "=" * 80)
print("SUMMARY - Files Ranked by Number of Issues")
print("=" * 80)

for i, result in enumerate(results, 1):
    file = result['file']
    total = result['total']
    issues = result['issues']
    
    demo_calls = len(issues['demo_data_calls'])
    numbers = len(issues['hardcoded_numbers'])
    dicts = len(issues['hardcoded_dicts'])
    lists = len(issues['hardcoded_lists'])
    
    print(f"\n{i}. {file} - {total} issues")
    print(f"   └─ demo_data calls: {demo_calls}")
    print(f"   └─ hardcoded numbers: {numbers}")
    print(f"   └─ hardcoded dicts: {dicts}")
    print(f"   └─ hardcoded lists: {lists}")

# Print detailed findings for top 3
print("\n" + "=" * 80)
print("DETAILED VIEW - Top 3 Files with Most Issues")
print("=" * 80)

for result in results[:3]:
    file = result['file']
    issues = result['issues']
    
    print(f"\n{'=' * 80}")
    print(f"FILE: {file}")
    print('=' * 80)
    
    if issues['demo_data_calls']:
        print("\nDemo Data Calls:")
        for line_num, line in issues['demo_data_calls'][:10]:
            print(f"  Line {line_num}: {line}")
        if len(issues['demo_data_calls']) > 10:
            print(f"  ... and {len(issues['demo_data_calls']) - 10} more")
    
    if issues['hardcoded_numbers']:
        print("\nHardcoded Numbers:")
        for line_num, line in issues['hardcoded_numbers'][:5]:
            print(f"  Line {line_num}: {line}")
        if len(issues['hardcoded_numbers']) > 5:
            print(f"  ... and {len(issues['hardcoded_numbers']) - 5} more")

# Print recommendations
print("\n" + "=" * 80)
print("RECOMMENDATIONS")
print("=" * 80)

if results:
    print("\n📋 Fix Priority Order:")
    for i, result in enumerate(results[:5], 1):
        print(f"  {i}. {result['file']} ({result['total']} issues)")
    
    print("\n💡 What to do:")
    print("  1. Start with the files that have the most issues")
    print("  2. For each file, replace:")
    print("     - demo_data.get_*() with mode-aware logic")
    print("     - Hardcoded numbers with real data fetches")
    print("     - Hardcoded lists/dicts with database queries")
    print("\n  3. Pattern to use:")
    print("     if st.session_state.get('mode') == 'Demo':")
    print("         data = demo_data.get_something()")
    print("     else:")
    print("         data = real_service.get_something()")
else:
    print("\n✅ No hardcoded data found! (or files don't exist)")

print("\n" + "=" * 80)
