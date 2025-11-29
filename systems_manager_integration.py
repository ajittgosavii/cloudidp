"""
CloudIDP - AWS Systems Manager Integration Module
Automation, patch management, and parameter store operations
"""

import boto3
from typing import Dict, List, Optional, Any
from botocore.exceptions import ClientError


class SystemsManagerIntegration:
    """AWS Systems Manager integration for CloudIDP"""
    
    def __init__(self, demo_mode: bool = True, region: str = 'us-east-1'):
        self.demo_mode = demo_mode
        self.region = region
        
        if not demo_mode:
            try:
                self.ssm_client = boto3.client('ssm', region_name=region)
            except Exception as e:
                print(f"Warning: {e}")
                self.demo_mode = True
    
    def execute_automation(self, document_name: str, 
                          parameters: Optional[Dict[str, List[str]]] = None) -> Dict[str, Any]:
        """Execute an SSM automation document"""
        if self.demo_mode:
            return {
                'success': True,
                'automation_execution_id': f'exec-{str(hash(document_name))[-12:]}',
                'status': 'InProgress',
                'demo_mode': True
            }
        
        try:
            response = self.ssm_client.start_automation_execution(
                DocumentName=document_name,
                Parameters=parameters or {}
            )
            return {
                'success': True,
                'execution_id': response['AutomationExecutionId']
            }
        except ClientError as e:
            return {'success': False, 'error': str(e)}
    
    def get_parameter(self, name: str, with_decryption: bool = False) -> Dict[str, Any]:
        """Get a parameter from Parameter Store"""
        if self.demo_mode:
            return {
                'success': True,
                'name': name,
                'value': 'demo-parameter-value',
                'type': 'String',
                'demo_mode': True
            }
        
        try:
            response = self.ssm_client.get_parameter(
                Name=name,
                WithDecryption=with_decryption
            )
            return {
                'success': True,
                'parameter': response['Parameter']
            }
        except ClientError as e:
            return {'success': False, 'error': str(e)}
    
    def put_parameter(self, name: str, value: str, 
                     parameter_type: str = 'String',
                     description: str = '') -> Dict[str, Any]:
        """Create or update a parameter"""
        if self.demo_mode:
            return {
                'success': True,
                'name': name,
                'version': 1,
                'demo_mode': True
            }
        
        try:
            response = self.ssm_client.put_parameter(
                Name=name,
                Value=value,
                Type=parameter_type,
                Description=description,
                Overwrite=True
            )
            return {
                'success': True,
                'version': response['Version']
            }
        except ClientError as e:
            return {'success': False, 'error': str(e)}
    
    def create_patch_baseline(self, name: str, 
                             operating_system: str = 'AMAZON_LINUX_2') -> Dict[str, Any]:
        """Create a patch baseline"""
        if self.demo_mode:
            return {
                'success': True,
                'baseline_id': f'pb-{str(hash(name))[-8:]}',
                'demo_mode': True
            }
        
        try:
            response = self.ssm_client.create_patch_baseline(
                Name=name,
                OperatingSystem=operating_system,
                ApprovalRules={
                    'PatchRules': [{
                        'ApproveAfterDays': 7,
                        'ComplianceLevel': 'CRITICAL'
                    }]
                }
            )
            return {
                'success': True,
                'baseline_id': response['BaselineId']
            }
        except ClientError as e:
            return {'success': False, 'error': str(e)}


if __name__ == "__main__":
    print("Systems Manager Integration Demo")
    ssm = SystemsManagerIntegration(demo_mode=True)
    param = ssm.get_parameter('/cloudidp/config/demo')
    print(f"Parameter value: {param['value']}")
    print("✅ Demo completed!")
