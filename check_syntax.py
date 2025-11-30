"""
Check for syntax errors in all Python modules
Run: python check_syntax.py
"""

import py_compile
import sys

files_to_check = [
    'finops_module.py',
    'module_07_abstraction.py',
    'module_08_multicloud_hybrid.py',
    'module_09_developer_experience.py',
    'module_10_observability.py',
    'design_planning.py',
    'provisioning_deployment.py',
    'security_compliance.py',
    'policy_guardrails.py',
    'ondemand_operations.py',
    'ondemand_operations_part2.py',
    'streamlit_app.py'
]

print("=" * 80)
print("CloudIDP Syntax Checker")
print("=" * 80)
print()

errors_found = []
success_count = 0

for filename in files_to_check:
    try:
        py_compile.compile(filename, doraise=True)
        print(f"✅ {filename}")
        success_count += 1
    except py_compile.PyCompileError as e:
        print(f"❌ {filename}")
        print(f"   Error: {e}")
        errors_found.append((filename, str(e)))
    except FileNotFoundError:
        print(f"⚠️  {filename} (not found)")

print()
print("=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"✅ Valid: {success_count}")
print(f"❌ Errors: {len(errors_found)}")

if errors_found:
    print()
    print("Files with syntax errors:")
    for filename, error in errors_found:
        print(f"\n{filename}:")
        print(f"  {error}")
    sys.exit(1)
else:
    print()
    print("🎉 All files have valid syntax!")
    sys.exit(0)
