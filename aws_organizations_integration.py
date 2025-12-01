"""
CloudIDP - AWS Organizations Integration Module
Provides account provisioning, management, and organizational structure operations

This module integrates with AWS Organizations to enable:
- Automated account creation and provisioning
- Organizational Unit (OU) management
- Service Control Policy (SCP) management
- Account tagging and governance
- Billing and cost allocation
"""

import boto3
import time
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from botocore.exceptions import ClientError
from config import get_aws_account_config



class AWSOrganizationsIntegration:
    """
    AWS Organizations integration for CloudIDP platform
    
    Capabilities:
    - Account lifecycle management (create, close, invite)
    - OU structure management
    - SCP policy management and enforcement
    - Tag-based governance
    - Delegated administrator setup
    """
    
    def __init__(self, demo_mode: bool = True, region: str = 'us-east-1'):
        """
        Initialize AWS Organizations integration
        
        Args:
            demo_mode: If True, returns mock data. If False, connects to real AWS.
            region: AWS region for API calls (Organizations is global but needs region)
        """
        self.demo_mode = demo_mode
        self.region = region
        
        if not demo_mode:
            try:
                self.org_client = boto3.client('organizations', region_name=region)
                self.sts_client = boto3.client('sts', region_name=region)
                self._verify_organization_access()
            except Exception as e:
                print(f"Warning: Could not initialize AWS Organizations client: {e}")
                self.demo_mode = True
    
    def _verify_organization_access(self):
        """Verify access to AWS Organizations"""
        try:
            self.org_client.describe_organization()
        except ClientError as e:
            if e.response['Error']['Code'] == 'AWSOrganizationsNotInUseException':
                raise Exception("AWS Organizations is not enabled for this account")
            raise
    
    # ============================================================================
    # ACCOUNT PROVISIONING
    # ============================================================================
    
    def create_account(
        self,
        account_name: str,
        email: str,
        account_type: str = 'MEMBER',
        ou_id: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        iam_user_access: bool = False,
        role_name: str = 'OrganizationAccountAccessRole'
    ) -> Dict[str, Any]:
        """
        Create a new AWS account within the organization
        
        Args:
            account_name: Name for the new account
            email: Unique email address for the account
            account_type: 'MEMBER' or 'MANAGEMENT'
            ou_id: Optional OU ID to place the account
            tags: Dictionary of tags to apply
            iam_user_access: Whether to allow IAM users to access billing
            role_name: Name of cross-account access role
            
        Returns:
            Dict containing account creation details and status
        """
        if self.demo_mode:
            return self._mock_create_account(account_name, email, ou_id, tags)
        
        try:
            # Create account request
            response = self.org_client.create_account(
                Email=email,
                AccountName=account_name,
                RoleName=role_name,
                IamUserAccessToBilling='ALLOW' if iam_user_access else 'DENY'
            )
            
            request_id = response['CreateAccountStatus']['Id']
            
            # Poll for completion
            account_info = self._wait_for_account_creation(request_id)
            
            # Tag the account if tags provided
            if tags and account_info.get('account_id'):
                self._tag_account(account_info['account_id'], tags)
            
            # Move to OU if specified
            if ou_id and account_info.get('account_id'):
                self._move_account_to_ou(account_info['account_id'], ou_id)
            
            return {
                'success': True,
                'account_id': account_info.get('account_id'),
                'account_name': account_name,
                'email': email,
                'request_id': request_id,
                'status': account_info.get('status'),
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except ClientError as e:
            return {
                'success': False,
                'error': str(e),
                'error_code': e.response['Error']['Code'],
                'timestamp': datetime.utcnow().isoformat()
            }
    
    def _wait_for_account_creation(
        self,
        request_id: str,
        max_wait_time: int = 300,
        poll_interval: int = 10
    ) -> Dict[str, Any]:
        """
        Wait for account creation to complete
        
        Args:
            request_id: Account creation request ID
            max_wait_time: Maximum time to wait in seconds
            poll_interval: Time between status checks
            
        Returns:
            Dict with account creation details
        """
        start_time = time.time()
        
        while (time.time() - start_time) < max_wait_time:
            response = self.org_client.describe_create_account_status(
                CreateAccountRequestId=request_id
            )
            
            status = response['CreateAccountStatus']
            state = status['State']
            
            if state == 'SUCCEEDED':
                return {
                    'account_id': status['AccountId'],
                    'status': 'SUCCEEDED',
                    'account_name': status.get('AccountName')
                }
            elif state == 'FAILED':
                return {
                    'status': 'FAILED',
                    'failure_reason': status.get('FailureReason', 'Unknown error')
                }
            
            time.sleep(poll_interval)
        
        return {
            'status': 'TIMEOUT',
            'failure_reason': 'Account creation timed out'
        }
    
    def _tag_account(self, account_id: str, tags: Dict[str, str]):
        """Apply tags to an account"""
        try:
            tag_list = [{'Key': k, 'Value': v} for k, v in tags.items()]
            self.org_client.tag_resource(
                ResourceId=account_id,
                Tags=tag_list
            )
        except ClientError as e:
            print(f"Warning: Could not tag account {account_id}: {e}")
    
    def _move_account_to_ou(self, account_id: str, ou_id: str):
        """Move account to specified OU"""
        try:
            # Get current parent (root or OU)
            parents = self.org_client.list_parents(ChildId=account_id)
            current_parent_id = parents['Parents'][0]['Id']
            
            # Move account
            self.org_client.move_account(
                AccountId=account_id,
                SourceParentId=current_parent_id,
                DestinationParentId=ou_id
            )
        except ClientError as e:
            print(f"Warning: Could not move account to OU: {e}")
    
    def close_account(self, account_id: str) -> Dict[str, Any]:
        """
        Close an AWS account
        
        Args:
            account_id: The account ID to close
            
        Returns:
            Dict with operation status
        """
        if self.demo_mode:
            return {
                'success': True,
                'account_id': account_id,
                'status': 'CLOSED',
                'message': 'Account closure initiated (Demo)',
                'timestamp': datetime.utcnow().isoformat()
            }
        
        try:
            self.org_client.close_account(AccountId=account_id)
            return {
                'success': True,
                'account_id': account_id,
                'status': 'CLOSED',
                'timestamp': datetime.utcnow().isoformat()
            }
        except ClientError as e:
            return {
                'success': False,
                'error': str(e),
                'error_code': e.response['Error']['Code']
            }
    
    # ============================================================================
    # ORGANIZATIONAL UNIT (OU) MANAGEMENT
    # ============================================================================
    
    def create_organizational_unit(
        self,
        parent_id: str,
        name: str,
        tags: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Create a new Organizational Unit
        
        Args:
            parent_id: Parent OU or root ID
            name: Name for the new OU
            tags: Optional tags
            
        Returns:
            Dict with OU details
        """
        if self.demo_mode:
            return self._mock_create_ou(parent_id, name)
        
        try:
            response = self.org_client.create_organizational_unit(
                ParentId=parent_id,
                Name=name
            )
            
            ou_id = response['OrganizationalUnit']['Id']
            
            # Apply tags if provided
            if tags:
                self._tag_account(ou_id, tags)
            
            return {
                'success': True,
                'ou_id': ou_id,
                'name': name,
                'parent_id': parent_id,
                'arn': response['OrganizationalUnit']['Arn']
            }
        except ClientError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def list_organizational_units(self, parent_id: Optional[str] = None) -> Dict[str, Any]:
        """
        List all OUs in the organization or under a parent
        
        Args:
            parent_id: Optional parent ID to list children
            
        Returns:
            Dict with list of OUs
        """
        if self.demo_mode:
            return self._mock_list_ous()
        
        try:
            if not parent_id:
                # Get root first
                roots = self.org_client.list_roots()
                parent_id = roots['Roots'][0]['Id']
            
            ous = []
            paginator = self.org_client.get_paginator('list_organizational_units_for_parent')
            
            for page in paginator.paginate(ParentId=parent_id):
                ous.extend(page['OrganizationalUnits'])
            
            return {
                'success': True,
                'count': len(ous),
                'organizational_units': ous
            }
        except ClientError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_ou_hierarchy(self) -> Dict[str, Any]:
        """
        Get complete OU hierarchy structure
        
        Returns:
            Dict with hierarchical OU structure
        """
        if self.demo_mode:
            return self._mock_ou_hierarchy()
        
        try:
            roots = self.org_client.list_roots()
            root_id = roots['Roots'][0]['Id']
            
            hierarchy = self._build_ou_tree(root_id)
            
            return {
                'success': True,
                'root_id': root_id,
                'hierarchy': hierarchy
            }
        except ClientError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _build_ou_tree(self, parent_id: str) -> Dict[str, Any]:
        """Recursively build OU tree structure"""
        try:
            # Get OUs under this parent
            ous = self.org_client.list_organizational_units_for_parent(
                ParentId=parent_id
            )
            
            # Get accounts under this parent
            accounts = self.org_client.list_accounts_for_parent(
                ParentId=parent_id
            )
            
            result = {
                'id': parent_id,
                'organizational_units': [],
                'accounts': accounts.get('Accounts', [])
            }
            
            # Recursively get children
            for ou in ous.get('OrganizationalUnits', []):
                ou_data = self._build_ou_tree(ou['Id'])
                ou_data['name'] = ou['Name']
                ou_data['arn'] = ou['Arn']
                result['organizational_units'].append(ou_data)
            
            return result
            
        except ClientError:
            return {'id': parent_id, 'error': 'Failed to retrieve children'}
    
    # ============================================================================
    # SERVICE CONTROL POLICIES (SCP)
    # ============================================================================
    
    def create_policy(
        self,
        name: str,
        description: str,
        content: Dict[str, Any],
        policy_type: str = 'SERVICE_CONTROL_POLICY'
    ) -> Dict[str, Any]:
        """
        Create a Service Control Policy
        
        Args:
            name: Policy name
            description: Policy description
            content: Policy document (JSON dict)
            policy_type: Type of policy
            
        Returns:
            Dict with policy details
        """
        if self.demo_mode:
            return self._mock_create_policy(name, description)
        
        try:
            response = self.org_client.create_policy(
                Content=json.dumps(content),
                Description=description,
                Name=name,
                Type=policy_type
            )
            
            return {
                'success': True,
                'policy_id': response['Policy']['PolicySummary']['Id'],
                'policy_arn': response['Policy']['PolicySummary']['Arn'],
                'name': name
            }
        except ClientError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def attach_policy(self, policy_id: str, target_id: str) -> Dict[str, Any]:
        """
        Attach a policy to an account or OU
        
        Args:
            policy_id: Policy ID to attach
            target_id: Account or OU ID
            
        Returns:
            Dict with operation status
        """
        if self.demo_mode:
            return {
                'success': True,
                'policy_id': policy_id,
                'target_id': target_id,
                'message': 'Policy attached (Demo)'
            }
        
        try:
            self.org_client.attach_policy(
                PolicyId=policy_id,
                TargetId=target_id
            )
            return {
                'success': True,
                'policy_id': policy_id,
                'target_id': target_id
            }
        except ClientError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def list_policies(self, filter_type: str = 'SERVICE_CONTROL_POLICY') -> Dict[str, Any]:
        """
        List all policies of a specific type
        
        Args:
            filter_type: Type of policies to list
            
        Returns:
            Dict with list of policies
        """
        if self.demo_mode:
            return self._mock_list_policies()
        
        try:
            policies = []
            paginator = self.org_client.get_paginator('list_policies')
            
            for page in paginator.paginate(Filter=filter_type):
                policies.extend(page['Policies'])
            
            return {
                'success': True,
                'count': len(policies),
                'policies': policies
            }
        except ClientError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    # ============================================================================
    # ACCOUNT OPERATIONS
    # ============================================================================
    
    def list_accounts(self) -> Dict[str, Any]:
        """
        List all accounts in the organization
        
        Returns:
            Dict with list of accounts
        """
        if self.demo_mode:
            return self._mock_list_accounts()
        
        try:
            accounts = []
            paginator = self.org_client.get_paginator('list_accounts')
            
            for page in paginator.paginate():
                accounts.extend(page['Accounts'])
            
            return {
                'success': True,
                'count': len(accounts),
                'accounts': accounts
            }
        except ClientError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_account_details(self, account_id: str) -> Dict[str, Any]:
        """
        Get detailed information about an account
        
        Args:
            account_id: Account ID
            
        Returns:
            Dict with account details
        """
        if self.demo_mode:
            return self._mock_account_details(account_id)
        
        try:
            response = self.org_client.describe_account(AccountId=account_id)
            account = response['Account']
            
            # Get tags
            tags = self.org_client.list_tags_for_resource(ResourceId=account_id)
            
            # Get parent OU
            parents = self.org_client.list_parents(ChildId=account_id)
            
            return {
                'success': True,
                'account': account,
                'tags': tags.get('Tags', []),
                'parent': parents['Parents'][0] if parents['Parents'] else None
            }
        except ClientError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    # ============================================================================
    # DELEGATED ADMINISTRATOR
    # ============================================================================
    
    def register_delegated_administrator(
        self,
        account_id: str,
        service_principal: str
    ) -> Dict[str, Any]:
        """
        Register an account as a delegated administrator for a service
        
        Args:
            account_id: Account to register
            service_principal: AWS service principal (e.g., 'config.amazonaws.com')
            
        Returns:
            Dict with operation status
        """
        if self.demo_mode:
            return {
                'success': True,
                'account_id': account_id,
                'service': service_principal,
                'message': 'Delegated admin registered (Demo)'
            }
        
        try:
            self.org_client.register_delegated_administrator(
                AccountId=account_id,
                ServicePrincipal=service_principal
            )
            return {
                'success': True,
                'account_id': account_id,
                'service_principal': service_principal
            }
        except ClientError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    # ============================================================================
    # DEMO DATA METHODS
    # ============================================================================
    
    def _mock_create_account(
        self,
        account_name: str,
        email: str,
        ou_id: Optional[str],
        tags: Optional[Dict[str, str]]
    ) -> Dict[str, Any]:
        """Generate mock account creation response"""
        account_id = f"123456{str(hash(email))[-6:]}"
        return {
            'success': True,
            'account_id': account_id,
            'account_name': account_name,
            'email': email,
            'ou_id': ou_id,
            'tags': tags or {},
            'request_id': f'car-{str(hash(email))[-8:]}',
            'status': 'SUCCEEDED',
            'timestamp': datetime.utcnow().isoformat(),
            'demo_mode': True
        }
    
    def _mock_create_ou(self, parent_id: str, name: str) -> Dict[str, Any]:
        """Generate mock OU creation response"""
        return {
            'success': True,
            'ou_id': f'ou-{str(hash(name))[-8:]}',
            'name': name,
            'parent_id': parent_id,
            'arn': f'arn:aws:REGION:ACCOUNT_ID_PLACEHOLDER:ou/o-exampleorgid/ou-{str(hash(name))[-8:]}',
            'demo_mode': True
        }
    
    def _mock_list_ous(self) -> Dict[str, Any]:
        """Generate mock OU list"""
        return {
            'success': True,
            'count': 5,
            'organizational_units': [
                {
                    'Id': 'ou-prod-001',
                    'Arn': 'arn:aws:REGION:ACCOUNT_ID_PLACEHOLDER:ou/o-exampleorgid/ou-prod-001',
                    'Name': 'Production'
                },
                {
                    'Id': 'ou-dev-001',
                    'Arn': 'arn:aws:REGION:ACCOUNT_ID_PLACEHOLDER:ou/o-exampleorgid/ou-dev-001',
                    'Name': 'Development'
                },
                {
                    'Id': 'ou-staging-001',
                    'Arn': 'arn:aws:REGION:ACCOUNT_ID_PLACEHOLDER:ou/o-exampleorgid/ou-staging-001',
                    'Name': 'Staging'
                },
                {
                    'Id': 'ou-sandbox-001',
                    'Arn': 'arn:aws:REGION:ACCOUNT_ID_PLACEHOLDER:ou/o-exampleorgid/ou-sandbox-001',
                    'Name': 'Sandbox'
                },
                {
                    'Id': 'ou-shared-001',
                    'Arn': 'arn:aws:REGION:ACCOUNT_ID_PLACEHOLDER:ou/o-exampleorgid/ou-shared-001',
                    'Name': 'Shared Services'
                }
            ],
            'demo_mode': True
        }
    
    def _mock_ou_hierarchy(self) -> Dict[str, Any]:
        """Generate mock OU hierarchy"""
        return {
            'success': True,
            'root_id': 'r-root',
            'hierarchy': {
                'id': 'r-root',
                'organizational_units': [
                    {
                        'id': 'ou-prod-001',
                        'name': 'Production',
                        'accounts': [
                            {'Id': '111111111111', 'Name': 'Prod-App-1', 'Email': 'prod-app-1@example.com'}
                        ],
                        'organizational_units': []
                    },
                    {
                        'id': 'ou-dev-001',
                        'name': 'Development',
                        'accounts': [
                            {'Id': '222222222222', 'Name': 'Dev-App-1', 'Email': 'dev-app-1@example.com'}
                        ],
                        'organizational_units': []
                    }
                ],
                'accounts': [
                    {'Id': '123456789012', 'Name': 'Management', 'Email': 'management@example.com'}
                ]
            },
            'demo_mode': True
        }
    
    def _mock_create_policy(self, name: str, description: str) -> Dict[str, Any]:
        """Generate mock policy creation response"""
        return {
            'success': True,
            'policy_id': f'p-{str(hash(name))[-8:]}',
            'policy_arn': f'arn:aws:REGION:ACCOUNT_ID_PLACEHOLDER:policy/o-exampleorgid/service_control_policy/p-{str(hash(name))[-8:]}',
            'name': name,
            'description': description,
            'demo_mode': True
        }
    
    def _mock_list_policies(self) -> Dict[str, Any]:
        """Generate mock policy list"""
        return {
            'success': True,
            'count': 3,
            'policies': [
                {
                    'Id': 'p-FullAWSAccess',
                    'Arn': 'arn:aws:organizations::aws:policy/service_control_policy/p-FullAWSAccess',
                    'Name': 'FullAWSAccess',
                    'Description': 'Allows access to all AWS services',
                    'Type': 'SERVICE_CONTROL_POLICY',
                    'AwsManaged': True
                },
                {
                    'Id': 'p-deny-s3-public',
                    'Arn': 'arn:aws:REGION:ACCOUNT_ID_PLACEHOLDER:policy/o-exampleorgid/service_control_policy/p-deny-s3-public',
                    'Name': 'DenyS3PublicAccess',
                    'Description': 'Prevents public S3 buckets',
                    'Type': 'SERVICE_CONTROL_POLICY',
                    'AwsManaged': False
                },
                {
                    'Id': 'p-require-mfa',
                    'Arn': 'arn:aws:REGION:ACCOUNT_ID_PLACEHOLDER:policy/o-exampleorgid/service_control_policy/p-require-mfa',
                    'Name': 'RequireMFA',
                    'Description': 'Requires MFA for console access',
                    'Type': 'SERVICE_CONTROL_POLICY',
                    'AwsManaged': False
                }
            ],
            'demo_mode': True
        }
    
    def _mock_list_accounts(self) -> Dict[str, Any]:
        """Generate mock account list"""
        return {
            'success': True,
            'count': 6,
            'accounts': [
                {
                    'Id': '123456789012',
                    'Arn': 'arn:aws:REGION:ACCOUNT_ID_PLACEHOLDER:account/o-exampleorgid/123456789012',
                    'Email': 'management@example.com',
                    'Name': 'Management',
                    'Status': 'ACTIVE',
                    'JoinedMethod': 'CREATED'
                },
                {
                    'Id': '111111111111',
                    'Arn': 'arn:aws:REGION:ACCOUNT_ID_PLACEHOLDER:account/o-exampleorgid/111111111111',
                    'Email': 'prod-app-1@example.com',
                    'Name': 'Production-App-1',
                    'Status': 'ACTIVE',
                    'JoinedMethod': 'CREATED'
                },
                {
                    'Id': '222222222222',
                    'Arn': 'arn:aws:REGION:ACCOUNT_ID_PLACEHOLDER:account/o-exampleorgid/222222222222',
                    'Email': 'dev-app-1@example.com',
                    'Name': 'Development-App-1',
                    'Status': 'ACTIVE',
                    'JoinedMethod': 'CREATED'
                },
                {
                    'Id': '333333333333',
                    'Arn': 'arn:aws:REGION:ACCOUNT_ID_PLACEHOLDER:account/o-exampleorgid/333333333333',
                    'Email': 'staging@example.com',
                    'Name': 'Staging',
                    'Status': 'ACTIVE',
                    'JoinedMethod': 'CREATED'
                },
                {
                    'Id': '444444444444',
                    'Arn': 'arn:aws:REGION:ACCOUNT_ID_PLACEHOLDER:account/o-exampleorgid/444444444444',
                    'Email': 'sandbox@example.com',
                    'Name': 'Sandbox',
                    'Status': 'ACTIVE',
                    'JoinedMethod': 'CREATED'
                },
                {
                    'Id': '555555555555',
                    'Arn': 'arn:aws:REGION:ACCOUNT_ID_PLACEHOLDER:account/o-exampleorgid/555555555555',
                    'Email': 'shared-services@example.com',
                    'Name': 'Shared-Services',
                    'Status': 'ACTIVE',
                    'JoinedMethod': 'CREATED'
                }
            ],
            'demo_mode': True
        }
    
    def _mock_account_details(self, account_id: str) -> Dict[str, Any]:
        """Generate mock account details"""
        return {
            'success': True,
            'account': {
                'Id': account_id,
                'Arn': f'arn:aws:REGION:ACCOUNT_ID_PLACEHOLDER:account/o-exampleorgid/{account_id}',
                'Email': f'account-{account_id}@example.com',
                'Name': f'Account-{account_id}',
                'Status': 'ACTIVE',
                'JoinedMethod': 'CREATED',
                'JoinedTimestamp': datetime.utcnow().isoformat()
            },
            'tags': [
                {'Key': 'Environment', 'Value': 'Production'},
                {'Key': 'CostCenter', 'Value': 'Engineering'},
                {'Key': 'Owner', 'Value': 'platform-team'}
            ],
            'parent': {
                'Id': 'ou-prod-001',
                'Type': 'ORGANIZATIONAL_UNIT'
            },
            'demo_mode': True
        }


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("CloudIDP - AWS Organizations Integration Demo\n")
    
    # Initialize in demo mode
    org = AWSOrganizationsIntegration(demo_mode=True)
    
    # Test account creation
    print("1. Creating new AWS account...")
    result = org.create_account(
        account_name="Test-Application-Account",
        email="test-app@example.com",
        ou_id="ou-prod-001",
        tags={'Environment': 'Production', 'App': 'WebApp'}
    )
    print(f"   Account Created: {result['account_id']}")
    
    # Test OU creation
    print("\n2. Creating Organizational Unit...")
    ou_result = org.create_organizational_unit(
        parent_id="r-root",
        name="Security"
    )
    print(f"   OU Created: {ou_result['ou_id']}")
    
    # List accounts
    print("\n3. Listing all accounts...")
    accounts = org.list_accounts()
    print(f"   Total Accounts: {accounts['count']}")
    for acc in accounts['accounts'][:3]:
        print(f"   - {acc['Name']} ({acc['Id']})")
    
    # Get OU hierarchy
    print("\n4. Getting OU hierarchy...")
    hierarchy = org.get_ou_hierarchy()
    print(f"   Root ID: {hierarchy['root_id']}")
    print(f"   Top-level OUs: {len(hierarchy['hierarchy']['organizational_units'])}")
    
    print("\n✅ Demo completed successfully!")
