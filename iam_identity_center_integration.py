"""
CloudIDP - IAM Identity Center (AWS SSO) Integration Module
Provides SSO, SCIM, permission set, and identity management operations

This module integrates with AWS IAM Identity Center to enable:
- Single Sign-On (SSO) configuration
- SCIM user/group provisioning
- Permission set management
- Account assignments
- Multi-account access management
"""

import boto3
import time
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from botocore.exceptions import ClientError
from config import get_aws_account_config



class IAMIdentityCenterIntegration:
    """
    IAM Identity Center integration for CloudIDP platform
    
    Capabilities:
    - SSO instance management
    - Permission set creation and management
    - User and group provisioning (SCIM)
    - Account assignment automation
    - Access portal configuration
    """
    
    def __init__(self, demo_mode: bool = True, region: str = 'us-east-1'):
        """
        Initialize IAM Identity Center integration
        
        Args:
            demo_mode: If True, returns mock data. If False, connects to real AWS.
            region: AWS region for IAM Identity Center instance
        """
        self.demo_mode = demo_mode
        self.region = region
        
        if not demo_mode:
            try:
                self.sso_admin_client = boto3.client('sso-admin', region_name=region)
                self.identitystore_client = boto3.client('identitystore', region_name=region)
                self.organizations_client = boto3.client('organizations', region_name=region)
                self._get_instance_details()
            except Exception as e:
                print(f"Warning: Could not initialize IAM Identity Center client: {e}")
                self.demo_mode = True
        else:
            # Mock instance details for demo mode
            self.instance_arn = "arn:aws:sso:::instance/ssoins-demo123456789"
            self.identity_store_id = "d-demo123456"
    
    def _get_instance_details(self):
        """Get IAM Identity Center instance details"""
        try:
            response = self.sso_admin_client.list_instances()
            if response['Instances']:
                instance = response['Instances'][0]
                self.instance_arn = instance['InstanceArn']
                self.identity_store_id = instance['IdentityStoreId']
            else:
                raise Exception("No IAM Identity Center instance found")
        except ClientError as e:
            raise Exception(f"Failed to get IAM Identity Center instance: {e}")
    
    # ============================================================================
    # PERMISSION SET MANAGEMENT
    # ============================================================================
    
    def create_permission_set(
        self,
        name: str,
        description: str,
        session_duration: str = 'PT8H',
        managed_policies: Optional[List[str]] = None,
        inline_policy: Optional[Dict[str, Any]] = None,
        tags: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Create a permission set
        
        Args:
            name: Permission set name
            description: Description
            session_duration: Session duration (ISO 8601, e.g., 'PT8H' for 8 hours)
            managed_policies: List of AWS managed policy ARNs
            inline_policy: Inline policy document
            tags: Tags to apply
            
        Returns:
            Dict with permission set details
        """
        if self.demo_mode:
            return self._mock_create_permission_set(name, description)
        
        try:
            # Create permission set
            response = self.sso_admin_client.create_permission_set(
                Name=name,
                Description=description,
                InstanceArn=self.instance_arn,
                SessionDuration=session_duration
            )
            
            permission_set_arn = response['PermissionSet']['PermissionSetArn']
            
            # Attach managed policies
            if managed_policies:
                for policy_arn in managed_policies:
                    self.sso_admin_client.attach_managed_policy_to_permission_set(
                        InstanceArn=self.instance_arn,
                        PermissionSetArn=permission_set_arn,
                        ManagedPolicyArn=policy_arn
                    )
            
            # Add inline policy
            if inline_policy:
                self.sso_admin_client.put_inline_policy_to_permission_set(
                    InstanceArn=self.instance_arn,
                    PermissionSetArn=permission_set_arn,
                    InlinePolicy=json.dumps(inline_policy)
                )
            
            # Tag permission set
            if tags:
                tag_list = [{'Key': k, 'Value': v} for k, v in tags.items()]
                self.sso_admin_client.tag_resource(
                    InstanceArn=self.instance_arn,
                    ResourceArn=permission_set_arn,
                    Tags=tag_list
                )
            
            return {
                'success': True,
                'permission_set_arn': permission_set_arn,
                'name': name,
                'session_duration': session_duration
            }
            
        except ClientError as e:
            return {
                'success': False,
                'error': str(e),
                'error_code': e.response['Error']['Code']
            }
    
    def update_permission_set(
        self,
        permission_set_arn: str,
        description: Optional[str] = None,
        session_duration: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update an existing permission set
        
        Args:
            permission_set_arn: ARN of permission set to update
            description: New description
            session_duration: New session duration
            
        Returns:
            Dict with operation status
        """
        if self.demo_mode:
            return {
                'success': True,
                'permission_set_arn': permission_set_arn,
                'message': 'Permission set updated (Demo)'
            }
        
        try:
            update_params = {
                'InstanceArn': self.instance_arn,
                'PermissionSetArn': permission_set_arn
            }
            
            if description:
                update_params['Description'] = description
            if session_duration:
                update_params['SessionDuration'] = session_duration
            
            self.sso_admin_client.update_permission_set(**update_params)
            
            return {
                'success': True,
                'permission_set_arn': permission_set_arn
            }
        except ClientError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def list_permission_sets(self) -> Dict[str, Any]:
        """
        List all permission sets
        
        Returns:
            Dict with list of permission sets
        """
        if self.demo_mode:
            return self._mock_list_permission_sets()
        
        try:
            permission_sets = []
            paginator = self.sso_admin_client.get_paginator('list_permission_sets')
            
            for page in paginator.paginate(InstanceArn=self.instance_arn):
                permission_sets.extend(page['PermissionSets'])
            
            # Get details for each permission set
            detailed_sets = []
            for ps_arn in permission_sets:
                details = self.sso_admin_client.describe_permission_set(
                    InstanceArn=self.instance_arn,
                    PermissionSetArn=ps_arn
                )
                detailed_sets.append(details['PermissionSet'])
            
            return {
                'success': True,
                'count': len(detailed_sets),
                'permission_sets': detailed_sets
            }
        except ClientError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def delete_permission_set(self, permission_set_arn: str) -> Dict[str, Any]:
        """
        Delete a permission set
        
        Args:
            permission_set_arn: ARN of permission set to delete
            
        Returns:
            Dict with operation status
        """
        if self.demo_mode:
            return {
                'success': True,
                'permission_set_arn': permission_set_arn,
                'message': 'Permission set deleted (Demo)'
            }
        
        try:
            self.sso_admin_client.delete_permission_set(
                InstanceArn=self.instance_arn,
                PermissionSetArn=permission_set_arn
            )
            return {
                'success': True,
                'permission_set_arn': permission_set_arn
            }
        except ClientError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    # ============================================================================
    # ACCOUNT ASSIGNMENTS
    # ============================================================================
    
    def create_account_assignment(
        self,
        permission_set_arn: str,
        principal_id: str,
        principal_type: str,  # 'USER' or 'GROUP'
        target_account_id: str
    ) -> Dict[str, Any]:
        """
        Assign a permission set to a principal (user/group) for an account
        
        Args:
            permission_set_arn: Permission set ARN
            principal_id: User or group ID
            principal_type: 'USER' or 'GROUP'
            target_account_id: AWS account ID
            
        Returns:
            Dict with assignment details
        """
        if self.demo_mode:
            return self._mock_create_assignment(
                permission_set_arn, principal_id, principal_type, target_account_id
            )
        
        try:
            response = self.sso_admin_client.create_account_assignment(
                InstanceArn=self.instance_arn,
                TargetId=target_account_id,
                TargetType='AWS_ACCOUNT',
                PermissionSetArn=permission_set_arn,
                PrincipalType=principal_type,
                PrincipalId=principal_id
            )
            
            # Wait for assignment to complete
            request_id = response['AccountAssignmentCreationStatus']['RequestId']
            status = self._wait_for_assignment(request_id)
            
            return {
                'success': status == 'SUCCEEDED',
                'request_id': request_id,
                'status': status,
                'permission_set_arn': permission_set_arn,
                'principal_id': principal_id,
                'account_id': target_account_id
            }
            
        except ClientError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def delete_account_assignment(
        self,
        permission_set_arn: str,
        principal_id: str,
        principal_type: str,
        target_account_id: str
    ) -> Dict[str, Any]:
        """
        Remove a permission set assignment
        
        Args:
            permission_set_arn: Permission set ARN
            principal_id: User or group ID
            principal_type: 'USER' or 'GROUP'
            target_account_id: AWS account ID
            
        Returns:
            Dict with operation status
        """
        if self.demo_mode:
            return {
                'success': True,
                'message': 'Assignment deleted (Demo)'
            }
        
        try:
            response = self.sso_admin_client.delete_account_assignment(
                InstanceArn=self.instance_arn,
                TargetId=target_account_id,
                TargetType='AWS_ACCOUNT',
                PermissionSetArn=permission_set_arn,
                PrincipalType=principal_type,
                PrincipalId=principal_id
            )
            
            request_id = response['AccountAssignmentDeletionStatus']['RequestId']
            status = self._wait_for_assignment_deletion(request_id)
            
            return {
                'success': status == 'SUCCEEDED',
                'request_id': request_id,
                'status': status
            }
        except ClientError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def list_account_assignments(
        self,
        account_id: str,
        permission_set_arn: str
    ) -> Dict[str, Any]:
        """
        List all assignments for a permission set in an account
        
        Args:
            account_id: AWS account ID
            permission_set_arn: Permission set ARN
            
        Returns:
            Dict with list of assignments
        """
        if self.demo_mode:
            return self._mock_list_assignments()
        
        try:
            assignments = []
            paginator = self.sso_admin_client.get_paginator('list_account_assignments')
            
            for page in paginator.paginate(
                InstanceArn=self.instance_arn,
                AccountId=account_id,
                PermissionSetArn=permission_set_arn
            ):
                assignments.extend(page['AccountAssignments'])
            
            return {
                'success': True,
                'count': len(assignments),
                'assignments': assignments
            }
        except ClientError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _wait_for_assignment(
        self,
        request_id: str,
        max_wait_time: int = 120
    ) -> str:
        """Wait for account assignment to complete"""
        start_time = time.time()
        
        while (time.time() - start_time) < max_wait_time:
            response = self.sso_admin_client.describe_account_assignment_creation_status(
                InstanceArn=self.instance_arn,
                AccountAssignmentCreationRequestId=request_id
            )
            
            status = response['AccountAssignmentCreationStatus']['Status']
            
            if status in ['SUCCEEDED', 'FAILED']:
                return status
            
            time.sleep(2)
        
        return 'TIMEOUT'
    
    def _wait_for_assignment_deletion(
        self,
        request_id: str,
        max_wait_time: int = 120
    ) -> str:
        """Wait for account assignment deletion to complete"""
        start_time = time.time()
        
        while (time.time() - start_time) < max_wait_time:
            response = self.sso_admin_client.describe_account_assignment_deletion_status(
                InstanceArn=self.instance_arn,
                AccountAssignmentDeletionRequestId=request_id
            )
            
            status = response['AccountAssignmentDeletionStatus']['Status']
            
            if status in ['SUCCEEDED', 'FAILED']:
                return status
            
            time.sleep(2)
        
        return 'TIMEOUT'
    
    # ============================================================================
    # USER MANAGEMENT (SCIM)
    # ============================================================================
    
    def create_user(
        self,
        username: str,
        given_name: str,
        family_name: str,
        email: str,
        display_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a user in Identity Store
        
        Args:
            username: Username
            given_name: First name
            family_name: Last name
            email: Email address
            display_name: Optional display name
            
        Returns:
            Dict with user details
        """
        if self.demo_mode:
            return self._mock_create_user(username, email)
        
        try:
            response = self.identitystore_client.create_user(
                IdentityStoreId=self.identity_store_id,
                UserName=username,
                Name={
                    'GivenName': given_name,
                    'FamilyName': family_name
                },
                DisplayName=display_name or f"{given_name} {family_name}",
                Emails=[{
                    'Value': email,
                    'Type': 'Work',
                    'Primary': True
                }]
            )
            
            return {
                'success': True,
                'user_id': response['UserId'],
                'username': username,
                'email': email
            }
        except ClientError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_user(self, user_id: str) -> Dict[str, Any]:
        """
        Get user details
        
        Args:
            user_id: User ID
            
        Returns:
            Dict with user details
        """
        if self.demo_mode:
            return self._mock_get_user(user_id)
        
        try:
            response = self.identitystore_client.describe_user(
                IdentityStoreId=self.identity_store_id,
                UserId=user_id
            )
            return {
                'success': True,
                'user': response
            }
        except ClientError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def list_users(self) -> Dict[str, Any]:
        """
        List all users in Identity Store
        
        Returns:
            Dict with list of users
        """
        if self.demo_mode:
            return self._mock_list_users()
        
        try:
            users = []
            paginator = self.identitystore_client.get_paginator('list_users')
            
            for page in paginator.paginate(IdentityStoreId=self.identity_store_id):
                users.extend(page['Users'])
            
            return {
                'success': True,
                'count': len(users),
                'users': users
            }
        except ClientError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    # ============================================================================
    # GROUP MANAGEMENT
    # ============================================================================
    
    def create_group(
        self,
        display_name: str,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a group in Identity Store
        
        Args:
            display_name: Group name
            description: Group description
            
        Returns:
            Dict with group details
        """
        if self.demo_mode:
            return self._mock_create_group(display_name)
        
        try:
            response = self.identitystore_client.create_group(
                IdentityStoreId=self.identity_store_id,
                DisplayName=display_name,
                Description=description or f"Group: {display_name}"
            )
            
            return {
                'success': True,
                'group_id': response['GroupId'],
                'display_name': display_name
            }
        except ClientError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def add_user_to_group(self, user_id: str, group_id: str) -> Dict[str, Any]:
        """
        Add a user to a group
        
        Args:
            user_id: User ID
            group_id: Group ID
            
        Returns:
            Dict with operation status
        """
        if self.demo_mode:
            return {
                'success': True,
                'user_id': user_id,
                'group_id': group_id,
                'message': 'User added to group (Demo)'
            }
        
        try:
            response = self.identitystore_client.create_group_membership(
                IdentityStoreId=self.identity_store_id,
                GroupId=group_id,
                MemberId={'UserId': user_id}
            )
            
            return {
                'success': True,
                'membership_id': response['MembershipId'],
                'user_id': user_id,
                'group_id': group_id
            }
        except ClientError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def list_groups(self) -> Dict[str, Any]:
        """
        List all groups in Identity Store
        
        Returns:
            Dict with list of groups
        """
        if self.demo_mode:
            return self._mock_list_groups()
        
        try:
            groups = []
            paginator = self.identitystore_client.get_paginator('list_groups')
            
            for page in paginator.paginate(IdentityStoreId=self.identity_store_id):
                groups.extend(page['Groups'])
            
            return {
                'success': True,
                'count': len(groups),
                'groups': groups
            }
        except ClientError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    # ============================================================================
    # DEMO DATA METHODS
    # ============================================================================
    
    def _mock_create_permission_set(self, name: str, description: str) -> Dict[str, Any]:
        """Generate mock permission set creation response"""
        return {
            'success': True,
            'permission_set_arn': f'arn:aws:sso:::permissionSet/ssoins-demo/{str(hash(name))[-12:]}',
            'name': name,
            'description': description,
            'session_duration': 'PT8H',
            'demo_mode': True
        }
    
    def _mock_list_permission_sets(self) -> Dict[str, Any]:
        """Generate mock permission set list"""
        return {
            'success': True,
            'count': 5,
            'permission_sets': [
                {
                    'Name': 'AdministratorAccess',
                    'PermissionSetArn': 'arn:aws:sso:::permissionSet/ssoins-demo/ps-admin',
                    'Description': 'Full administrator access',
                    'SessionDuration': 'PT8H'
                },
                {
                    'Name': 'PowerUserAccess',
                    'PermissionSetArn': 'arn:aws:sso:::permissionSet/ssoins-demo/ps-power',
                    'Description': 'Power user access',
                    'SessionDuration': 'PT8H'
                },
                {
                    'Name': 'ReadOnlyAccess',
                    'PermissionSetArn': 'arn:aws:sso:::permissionSet/ssoins-demo/ps-readonly',
                    'Description': 'Read-only access to all services',
                    'SessionDuration': 'PT4H'
                },
                {
                    'Name': 'DeveloperAccess',
                    'PermissionSetArn': 'arn:aws:sso:::permissionSet/ssoins-demo/ps-dev',
                    'Description': 'Developer access with limited permissions',
                    'SessionDuration': 'PT8H'
                },
                {
                    'Name': 'SecurityAuditor',
                    'PermissionSetArn': 'arn:aws:sso:::permissionSet/ssoins-demo/ps-audit',
                    'Description': 'Security auditor access',
                    'SessionDuration': 'PT4H'
                }
            ],
            'demo_mode': True
        }
    
    def _mock_create_assignment(
        self, ps_arn: str, principal_id: str, principal_type: str, account_id: str
    ) -> Dict[str, Any]:
        """Generate mock assignment response"""
        return {
            'success': True,
            'request_id': f'req-{str(hash(principal_id))[-8:]}',
            'status': 'SUCCEEDED',
            'permission_set_arn': ps_arn,
            'principal_id': principal_id,
            'principal_type': principal_type,
            'account_id': account_id,
            'demo_mode': True
        }
    
    def _mock_list_assignments(self) -> Dict[str, Any]:
        """Generate mock assignment list"""
        return {
            'success': True,
            'count': 3,
            'assignments': [
                {
                    'PrincipalId': 'user-12345',
                    'PrincipalType': 'USER',
                    'PermissionSetArn': 'arn:aws:sso:::permissionSet/ssoins-demo/ps-admin'
                },
                {
                    'PrincipalId': 'group-67890',
                    'PrincipalType': 'GROUP',
                    'PermissionSetArn': 'arn:aws:sso:::permissionSet/ssoins-demo/ps-dev'
                },
                {
                    'PrincipalId': 'user-54321',
                    'PrincipalType': 'USER',
                    'PermissionSetArn': 'arn:aws:sso:::permissionSet/ssoins-demo/ps-readonly'
                }
            ],
            'demo_mode': True
        }
    
    def _mock_create_user(self, username: str, email: str) -> Dict[str, Any]:
        """Generate mock user creation response"""
        return {
            'success': True,
            'user_id': f'user-{str(hash(username))[-8:]}',
            'username': username,
            'email': email,
            'demo_mode': True
        }
    
    def _mock_get_user(self, user_id: str) -> Dict[str, Any]:
        """Generate mock user details"""
        return {
            'success': True,
            'user': {
                'UserId': user_id,
                'UserName': f'user{user_id[-4:]}',
                'DisplayName': 'Demo User',
                'Name': {
                    'GivenName': 'Demo',
                    'FamilyName': 'User'
                },
                'Emails': [{'Value': f'user{user_id[-4:]}@example.com', 'Primary': True}]
            },
            'demo_mode': True
        }
    
    def _mock_list_users(self) -> Dict[str, Any]:
        """Generate mock user list"""
        return {
            'success': True,
            'count': 4,
            'users': [
                {
                    'UserId': 'user-admin',
                    'UserName': 'admin',
                    'DisplayName': 'System Administrator',
                    'Emails': [{'Value': 'admin@example.com'}]
                },
                {
                    'UserId': 'user-dev1',
                    'UserName': 'developer1',
                    'DisplayName': 'Developer One',
                    'Emails': [{'Value': 'dev1@example.com'}]
                },
                {
                    'UserId': 'user-dev2',
                    'UserName': 'developer2',
                    'DisplayName': 'Developer Two',
                    'Emails': [{'Value': 'dev2@example.com'}]
                },
                {
                    'UserId': 'user-auditor',
                    'UserName': 'auditor',
                    'DisplayName': 'Security Auditor',
                    'Emails': [{'Value': 'auditor@example.com'}]
                }
            ],
            'demo_mode': True
        }
    
    def _mock_create_group(self, display_name: str) -> Dict[str, Any]:
        """Generate mock group creation response"""
        return {
            'success': True,
            'group_id': f'group-{str(hash(display_name))[-8:]}',
            'display_name': display_name,
            'demo_mode': True
        }
    
    def _mock_list_groups(self) -> Dict[str, Any]:
        """Generate mock group list"""
        return {
            'success': True,
            'count': 3,
            'groups': [
                {
                    'GroupId': 'group-admins',
                    'DisplayName': 'Administrators',
                    'Description': 'System administrators group'
                },
                {
                    'GroupId': 'group-developers',
                    'DisplayName': 'Developers',
                    'Description': 'Development team group'
                },
                {
                    'GroupId': 'group-auditors',
                    'DisplayName': 'Security Auditors',
                    'Description': 'Security and compliance team'
                }
            ],
            'demo_mode': True
        }


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("CloudIDP - IAM Identity Center Integration Demo\n")
    
    # Initialize in demo mode
    sso = IAMIdentityCenterIntegration(demo_mode=True)
    
    # Test permission set creation
    print("1. Creating permission set...")
    ps_result = sso.create_permission_set(
        name="CloudIDP-Developer",
        description="Developer access for CloudIDP platform",
        managed_policies=["arn:aws:iam::aws:policy/PowerUserAccess"]
    )
    print(f"   Permission Set ARN: {ps_result['permission_set_arn']}")
    
    # List permission sets
    print("\n2. Listing permission sets...")
    ps_list = sso.list_permission_sets()
    print(f"   Total Permission Sets: {ps_list['count']}")
    for ps in ps_list['permission_sets'][:3]:
        print(f"   - {ps['Name']}")
    
    # Create user
    print("\n3. Creating user...")
    user_result = sso.create_user(
        username="jdoe",
        given_name="John",
        family_name="Doe",
        email="jdoe@example.com"
    )
    print(f"   User ID: {user_result['user_id']}")
    
    # Create account assignment
    print("\n4. Creating account assignment...")
    assignment = sso.create_account_assignment(
        permission_set_arn=ps_result['permission_set_arn'],
        principal_id=user_result['user_id'],
        principal_type='USER',
        target_account_id = get_aws_account_config()['account_id']
    )
    print(f"   Assignment Status: {assignment['status']}")
    
    print("\n✅ Demo completed successfully!")
