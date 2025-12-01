#!/usr/bin/env python3
"""
CloudIDP Refactoring Script
Automatically refactor codebase to:
1. Remove hardcoded AWS account IDs
2. Remove Azure/GCP references
3. Update to use configuration-based approach
"""

import os
import re
import shutil
from pathlib import Path

class CloudIDPRefactorer:
    def __init__(self, source_dir, target_dir):
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        self.stats = {
            'files_processed': 0,
            'hardcoded_ids_replaced': 0,
            'multicloud_refs_removed': 0,
            'files_excluded': 0
        }
        
        # Files to exclude (development/utility files)
        self.exclude_files = {
            'auto_fix_metrics.py',
            'auto_fix_modules.py',
            'check_backups.py',
            'check_syntax.py',
            'diagnostic_modules.py',
            'emergency_fix_finops.py',
            'find_hardcoded_data.py',
            'find_indentation_error.py',
            'fix_all_modules.py',
            'fix_invalid_variables.py',
            'fix_remaining_modules.py',
            'restore_and_add_indicators.py',
            'restore_and_fix.ps1',
            'restore_and_fix.py',
            'verify_setup.py',
            'streamlit_app_COMPLETE.py',
            'module_08_multicloud_hybrid.py',  # Remove multi-cloud module
            'ondemand_operations_part2.py',  # Merged into ondemand_operations.py
        }
        
        # Patterns to remove multi-cloud references
        self.multicloud_patterns = [
            (r'"Azure"', ''),
            (r'"GCP"', ''),
            (r'"Multi-Cloud"', ''),
            (r'Azure', ''),
            (r'GCP', ''),
            (r'azure', ''),
            (r'gcp', ''),
        ]
        
    def should_process_file(self, filename):
        """Check if file should be processed"""
        # Skip backup files
        if filename.endswith('.backup'):
            return False
        # Skip excluded files
        if filename in self.exclude_files:
            return False
        # Skip __pycache__
        if '__pycache__' in str(filename):
            return False
        return True
    
    def replace_hardcoded_accounts(self, content, filename):
        """Replace hardcoded AWS account IDs with config-based approach"""
        replacements = 0
        
        # Pattern for 12-digit account IDs
        account_patterns = [
            r'\b\d{12}\b',  # Any 12-digit number
        ]
        
        # Check if file already imports config
        has_config_import = 'from config import' in content or 'import config' in content
        
        # Add import if needed and file is Python
        if filename.endswith('.py') and not has_config_import:
            # Check if there are hardcoded account IDs first
            if re.search(r'\b\d{12}\b', content):
                # Add import after other imports
                import_line = 'from config import get_aws_account_config\n'
                # Find the last import statement
                lines = content.split('\n')
                import_index = 0
                for i, line in enumerate(lines):
                    if line.startswith('import ') or line.startswith('from '):
                        import_index = i
                if import_index > 0:
                    lines.insert(import_index + 1, import_line)
                    content = '\n'.join(lines)
        
        # Replace specific hardcoded account IDs
        specific_replacements = [
            # Replace direct usage in strings
            (r'"account_id":\s*"123456789012"', '"account_id": get_aws_account_config()[\'account_id\']'),
            (r'"account_id":\s*"111111111111"', '"account_id": get_aws_account_config()[\'account_id\']'),
            (r'"account_id":\s*"222222222222"', '"account_id": get_aws_account_config()[\'account_id\']'),
            (r'"account_id":\s*"333333333333"', '"account_id": get_aws_account_config()[\'account_id\']'),
            
            # Replace in ARNs - use placeholder
            (r'arn:aws:.*?:(\d{12}):', r'arn:aws:REGION:ACCOUNT_ID_PLACEHOLDER:'),
            
            # Replace in variable assignments
            (r'account_id\s*=\s*["\']123456789012["\']', 'account_id = get_aws_account_config()[\'account_id\']'),
            (r'target_account_id\s*=\s*["\']123456789012["\']', 'target_account_id = get_aws_account_config()[\'account_id\']'),
        ]
        
        for pattern, replacement in specific_replacements:
            new_content, count = re.subn(pattern, replacement, content)
            if count > 0:
                content = new_content
                replacements += count
        
        return content, replacements
    
    def remove_multicloud_references(self, content):
        """Remove Azure and GCP references"""
        removals = 0
        
        # Remove from lists
        patterns_to_remove = [
            # Remove Azure/GCP from cloud provider lists
            (r',?\s*"Azure"', ''),
            (r',?\s*"GCP"', ''),
            (r',?\s*"Multi-Cloud"', ''),
            # Remove Azure/GCP data entries
            (r'\{[^}]*"Cloud":\s*"Azure"[^}]*\},?', ''),
            (r'\{[^}]*"Cloud":\s*"GCP"[^}]*\},?', ''),
            (r'\{[^}]*"cloud":\s*"Azure"[^}]*\},?', ''),
            (r'\{[^}]*"cloud":\s*"GCP"[^}]*\},?', ''),
        ]
        
        for pattern, replacement in patterns_to_remove:
            new_content, count = re.subn(pattern, replacement, content)
            if count > 0:
                content = new_content
                removals += count
        
        return content, removals
    
    def process_file(self, source_path, target_path):
        """Process a single file"""
        try:
            with open(source_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            original_content = content
            
            # Replace hardcoded account IDs
            content, account_replacements = self.replace_hardcoded_accounts(content, source_path.name)
            self.stats['hardcoded_ids_replaced'] += account_replacements
            
            # Remove multi-cloud references
            content, multicloud_removals = self.remove_multicloud_references(content)
            self.stats['multicloud_refs_removed'] += multicloud_removals
            
            # Write to target
            target_path.parent.mkdir(parents=True, exist_ok=True)
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.stats['files_processed'] += 1
            
            if content != original_content:
                print(f"✅ Processed: {source_path.name} ({account_replacements} accounts, {multicloud_removals} multicloud refs)")
            else:
                print(f"📄 Copied: {source_path.name}")
                
        except Exception as e:
            print(f"❌ Error processing {source_path}: {e}")
    
    def refactor(self):
        """Main refactoring process"""
        print("🚀 Starting CloudIDP Refactoring...")
        print(f"Source: {self.source_dir}")
        print(f"Target: {self.target_dir}")
        print("-" * 60)
        
        # Create target directory
        self.target_dir.mkdir(parents=True, exist_ok=True)
        
        # Process all Python files
        for source_file in self.source_dir.glob('*.py'):
            if self.should_process_file(source_file.name):
                target_file = self.target_dir / source_file.name
                self.process_file(source_file, target_file)
            else:
                self.stats['files_excluded'] += 1
                print(f"⏭️  Excluded: {source_file.name}")
        
        # Copy non-Python files (except backups)
        for ext in ['*.txt', '*.yaml', '*.yml', '*.md', '*.tf', '*.sh']:
            for source_file in self.source_dir.glob(ext):
                if not source_file.name.endswith('.backup'):
                    target_file = self.target_dir / source_file.name
                    shutil.copy2(source_file, target_file)
                    print(f"📋 Copied: {source_file.name}")
        
        # Copy .gitignore
        gitignore = self.source_dir / '.gitignore'
        if gitignore.exists():
            shutil.copy2(gitignore, self.target_dir / '.gitignore')
            print(f"📋 Copied: .gitignore")
        
        print("-" * 60)
        print("✨ Refactoring Complete!")
        print(f"Files Processed: {self.stats['files_processed']}")
        print(f"Files Excluded: {self.stats['files_excluded']}")
        print(f"Hardcoded IDs Replaced: {self.stats['hardcoded_ids_replaced']}")
        print(f"Multi-cloud References Removed: {self.stats['multicloud_refs_removed']}")
        
        return self.stats

if __name__ == "__main__":
    source = "/home/claude/cloudidp"
    target = "/home/claude/cloudidp_refactored"
    
    refactorer = CloudIDPRefactorer(source, target)
    stats = refactorer.refactor()
