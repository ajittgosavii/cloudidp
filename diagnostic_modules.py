"""
CloudIDP Module Diagnostic Script
Run this to check if all modules are properly configured

This script checks for common display methods:
- render(), show(), display(), run(), execute(), main()

Your modules can use ANY of these method names!
"""

import sys
import importlib

def check_module(module_name, class_name):
    """Check if a module can be imported and has a display method"""
    try:
        # Try to import the module
        module = importlib.import_module(module_name)
        print(f"✅ {module_name}: Import successful")
        
        # Try to get the class
        if hasattr(module, class_name):
            cls = getattr(module, class_name)
            print(f"   ✅ Class '{class_name}' found")
            
            # Try to instantiate
            try:
                instance = cls()
                print(f"   ✅ Instantiation successful")
                
                # Check for common display methods
                method_names = ['render', 'show', 'display', 'run', 'execute', 'main']
                found_methods = []
                
                for method_name in method_names:
                    if hasattr(instance, method_name) and callable(getattr(instance, method_name)):
                        found_methods.append(method_name)
                
                if found_methods:
                    print(f"   ✅ Display method(s) found: {', '.join(found_methods)}")
                    print(f"   ℹ️  Will use: {found_methods[0]}()")
                    return True
                else:
                    print(f"   ❌ No display method found")
                    available = [m for m in dir(instance) if not m.startswith('_') and callable(getattr(instance, m))]
                    print(f"   ℹ️  Available methods: {', '.join(available)}")
                    return False
                    
            except Exception as e:
                print(f"   ❌ Instantiation failed: {e}")
                return False
        else:
            print(f"   ❌ Class '{class_name}' NOT FOUND")
            print(f"   ℹ️  Available classes: {[item for item in dir(module) if not item.startswith('_')]}")
            return False
            
    except ImportError as e:
        print(f"❌ {module_name}: Import failed - {e}")
        return False
    except Exception as e:
        print(f"❌ {module_name}: Unexpected error - {e}")
        return False

def main():
    print("=" * 60)
    print("CloudIDP Module Diagnostic")
    print("=" * 60)
    print()
    
    modules_to_check = [
        ("design_planning", "DesignPlanningModule"),
        ("provisioning_deployment", "ProvisioningDeploymentModule"),
        ("ondemand_operations", "OnDemandOperationsModule"),
        ("ondemand_operations_part2", "OnDemandOperationsModule2"),
        ("finops_module", "FinOpsModule"),
        ("security_compliance", "SecurityComplianceModule"),
        ("policy_guardrails", "PolicyGuardrailsModule"),
        ("module_07_abstraction", "AbstractionReusabilityModule"),
        ("module_08_multicloud_hybrid", "MultiCloudHybridModule"),
        ("module_09_developer_experience", "DeveloperExperienceModule"),
        ("module_10_observability", "ObservabilityIntegrationModule"),
        ("config", "initialize_session_state"),
        ("anthropic_helper", "AnthropicHelper"),
    ]
    
    results = {}
    
    for module_name, class_name in modules_to_check:
        print(f"\nChecking {module_name}...")
        print("-" * 60)
        results[module_name] = check_module(module_name, class_name)
        print()
    
    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"\nPassed: {passed}/{total}")
    print()
    
    if passed == total:
        print("✅ All modules are properly configured!")
        print("   The tab-based navigation should work correctly.")
        print("   Modules can use: render(), show(), display(), run(), execute(), or main()")
    else:
        print("⚠️  Some modules have issues:")
        print()
        for module_name, passed in results.items():
            if not passed:
                print(f"   ❌ {module_name}")
        print()
        print("RECOMMENDATIONS:")
        print("1. Check that all module files are in the same directory")
        print("2. Verify that each module class has a render() method")
        print("3. Check the module file structure matches the original")
        print("4. Look at the detailed error messages above")
    
    print()
    print("=" * 60)

if __name__ == "__main__":
    main()
