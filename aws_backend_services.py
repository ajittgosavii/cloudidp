"""
AWS Backend Services Integration
Handles AWS Organizations, Control Tower, Service Catalog, and IAM Identity Center
"""

import boto3
from botocore.exceptions import ClientError, BotoCoreError
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime
import json
from config import get_aws_account_config


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AWSOrganizationsService:
    """AWS Organizations API Integration for Account Management"""
    
    def __init__(self, region: str = 'us-east-1'):
        """Initialize AWS Organizations client"""
        self.region = region
        try:
            self.client = boto3.client('organizations', region_name=region)
            self.sts_client = boto3.client('sts', region_name=region)
        except Exception as e:
            logger.error(f"Failed to initialize AWS Organizations client: {e}")
            self.client = None
            self.sts_client = None
    
    def create_account(self, account_name: str, email: str, 
                       iam_user_access: str = 'ALLOW',
                       role_name: str = 'OrganizationAccountAccessRole',
                       tags: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        """
        Create a new AWS account in the organization
        
        Args:
            account_name: Name for the new account
            email: Email address for the account
            iam_user_access: Allow or deny IAM user access
            role_name: Name of the IAM role for cross-account access
            tags: List of tags to apply to the account
            
        Returns:
            Dict containing account creation status and request ID
        """
        if not self.client:
            return {"status": "error", "message": "AWS Organizations client not initialized"}
        
        try:
            params = {
                'Email': email,
                'AccountName': account_name,
                'IamUserAccessToBilling': iam_user_access,
                'RoleName': role_name
            }
            
            if tags:
                params['Tags'] = tags
            
            response = self.client.create_account(**params)
            
            return {
                "status": "success",
                "request_id": response['CreateAccountStatus']['Id'],
                "state": response['CreateAccountStatus']['State'],
                "account_name": account_name,
                "email": email,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except ClientError as e:
            logger.error(f"Failed to create account: {e}")
            return {
                "status": "error",
                "error_code": e.response['Error']['Code'],
                "message": e.response['Error']['Message']
            }
    
    def get_account_creation_status(self, request_id: str) -> Dict[str, Any]:
        """Check the status of account creation request"""
        if not self.client:
            return {"status": "error", "message": "Client not initialized"}
        
        try:
            response = self.client.describe_create_account_status(
                CreateAccountRequestId=request_id
            )
            
            status = response['CreateAccountStatus']
            return {
                "status": "success",
                "state": status['State'],
                "account_id": status.get('AccountId'),
                "account_name": status.get('AccountName'),
                "completed_timestamp": status.get('CompletedTimestamp'),
                "failure_reason": status.get('FailureReason')
            }
            
        except ClientError as e:
            logger.error(f"Failed to get account status: {e}")
            return {"status": "error", "message": str(e)}
    
    def list_accounts(self) -> Dict[str, Any]:
        """List all accounts in the organization"""
        if not self.client:
            return {"status": "error", "accounts": []}
        
        try:
            accounts = []
            paginator = self.client.get_paginator('list_accounts')
            
            for page in paginator.paginate():
                accounts.extend(page['Accounts'])
            
            return {
                "status": "success",
                "count": len(accounts),
                "accounts": accounts
            }
            
        except ClientError as e:
            logger.error(f"Failed to list accounts: {e}")
            return {"status": "error", "accounts": [], "message": str(e)}
    
    def move_account(self, account_id: str, source_ou_id: str, 
                     destination_ou_id: str) -> Dict[str, Any]:
        """Move an account between organizational units"""
        if not self.client:
            return {"status": "error", "message": "Client not initialized"}
        
        try:
            self.client.move_account(
                AccountId=account_id,
                SourceParentId=source_ou_id,
                DestinationParentId=destination_ou_id
            )
            
            return {
                "status": "success",
                "message": f"Account {account_id} moved successfully",
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except ClientError as e:
            logger.error(f"Failed to move account: {e}")
            return {"status": "error", "message": str(e)}
    
    def create_organizational_unit(self, parent_id: str, name: str,
                                   tags: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        """Create a new organizational unit"""
        if not self.client:
            return {"status": "error", "message": "Client not initialized"}
        
        try:
            params = {
                'ParentId': parent_id,
                'Name': name
            }
            
            if tags:
                params['Tags'] = tags
            
            response = self.client.create_organizational_unit(**params)
            
            return {
                "status": "success",
                "ou_id": response['OrganizationalUnit']['Id'],
                "ou_name": name,
                "ou_arn": response['OrganizationalUnit']['Arn']
            }
            
        except ClientError as e:
            logger.error(f"Failed to create OU: {e}")
            return {"status": "error", "message": str(e)}
    
    def tag_account(self, account_id: str, tags: List[Dict[str, str]]) -> Dict[str, Any]:
        """Apply tags to an AWS account"""
        if not self.client:
            return {"status": "error", "message": "Client not initialized"}
        
        try:
            self.client.tag_resource(
                ResourceId=account_id,
                Tags=tags
            )
            
            return {
                "status": "success",
                "message": f"Tags applied to account {account_id}",
                "tags": tags
            }
            
        except ClientError as e:
            logger.error(f"Failed to tag account: {e}")
            return {"status": "error", "message": str(e)}


class AWSControlTowerService:
    """AWS Control Tower Integration for Landing Zone Management"""
    
    def __init__(self, region: str = 'us-east-1'):
        """Initialize Control Tower client"""
        self.region = region
        try:
            self.client = boto3.client('controltower', region_name=region)
            self.org_client = boto3.client('organizations', region_name=region)
        except Exception as e:
            logger.error(f"Failed to initialize Control Tower client: {e}")
            self.client = None
            self.org_client = None
    
    def get_landing_zone_status(self) -> Dict[str, Any]:
        """Get the status of Control Tower landing zone"""
        if not self.client:
            return {"status": "error", "message": "Client not initialized"}
        
        try:
            # Note: This is a simplified version. Real implementation would check
            # Control Tower landing zone status through CloudFormation stacks
            response = self.client.get_landing_zone(
                landingZoneIdentifier='default'
            )
            
            return {
                "status": "success",
                "landing_zone_status": response.get('status', 'UNKNOWN'),
                "version": response.get('version'),
                "drift_status": response.get('driftStatus')
            }
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                return {
                    "status": "not_deployed",
                    "message": "Control Tower landing zone not found"
                }
            logger.error(f"Failed to get landing zone status: {e}")
            return {"status": "error", "message": str(e)}
    
    def enable_guardrail(self, guardrail_identifier: str, target_identifier: str) -> Dict[str, Any]:
        """Enable a Control Tower guardrail on a target OU"""
        if not self.client:
            return {"status": "error", "message": "Client not initialized"}
        
        try:
            response = self.client.enable_control(
                controlIdentifier=guardrail_identifier,
                targetIdentifier=target_identifier
            )
            
            return {
                "status": "success",
                "operation_identifier": response.get('operationIdentifier'),
                "message": "Guardrail enablement initiated"
            }
            
        except ClientError as e:
            logger.error(f"Failed to enable guardrail: {e}")
            return {"status": "error", "message": str(e)}
    
    def list_enabled_controls(self, target_identifier: str) -> Dict[str, Any]:
        """List all enabled controls for a target OU"""
        if not self.client:
            return {"status": "error", "controls": []}
        
        try:
            controls = []
            paginator = self.client.get_paginator('list_enabled_controls')
            
            for page in paginator.paginate(targetIdentifier=target_identifier):
                controls.extend(page.get('enabledControls', []))
            
            return {
                "status": "success",
                "count": len(controls),
                "controls": controls
            }
            
        except ClientError as e:
            logger.error(f"Failed to list controls: {e}")
            return {"status": "error", "controls": [], "message": str(e)}


class AWSServiceCatalogService:
    """AWS Service Catalog Integration for Product Management"""
    
    def __init__(self, region: str = 'us-east-1'):
        """Initialize Service Catalog client"""
        self.region = region
        try:
            self.client = boto3.client('servicecatalog', region_name=region)
        except Exception as e:
            logger.error(f"Failed to initialize Service Catalog client: {e}")
            self.client = None
    
    def create_portfolio(self, display_name: str, provider_name: str,
                        description: str, tags: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        """Create a new Service Catalog portfolio"""
        if not self.client:
            return {"status": "error", "message": "Client not initialized"}
        
        try:
            params = {
                'DisplayName': display_name,
                'ProviderName': provider_name,
                'Description': description
            }
            
            if tags:
                params['Tags'] = tags
            
            response = self.client.create_portfolio(**params)
            
            return {
                "status": "success",
                "portfolio_id": response['PortfolioDetail']['Id'],
                "portfolio_arn": response['PortfolioDetail']['ARN'],
                "display_name": display_name
            }
            
        except ClientError as e:
            logger.error(f"Failed to create portfolio: {e}")
            return {"status": "error", "message": str(e)}
    
    def create_product(self, name: str, owner: str, product_type: str,
                       provisioning_artifact_parameters: Dict[str, Any],
                       tags: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        """Create a new Service Catalog product"""
        if not self.client:
            return {"status": "error", "message": "Client not initialized"}
        
        try:
            params = {
                'Name': name,
                'Owner': owner,
                'ProductType': product_type,
                'ProvisioningArtifactParameters': provisioning_artifact_parameters
            }
            
            if tags:
                params['Tags'] = tags
            
            response = self.client.create_product(**params)
            
            return {
                "status": "success",
                "product_id": response['ProductViewDetail']['ProductViewSummary']['ProductId'],
                "product_arn": response['ProductViewDetail']['ProductARN'],
                "name": name
            }
            
        except ClientError as e:
            logger.error(f"Failed to create product: {e}")
            return {"status": "error", "message": str(e)}
    
    def provision_product(self, product_id: str, provisioning_artifact_id: str,
                         provisioned_product_name: str,
                         provisioning_parameters: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        """Provision a Service Catalog product"""
        if not self.client:
            return {"status": "error", "message": "Client not initialized"}
        
        try:
            params = {
                'ProductId': product_id,
                'ProvisioningArtifactId': provisioning_artifact_id,
                'ProvisionedProductName': provisioned_product_name,
                'ProvisionToken': f"token-{datetime.utcnow().timestamp()}"
            }
            
            if provisioning_parameters:
                params['ProvisioningParameters'] = provisioning_parameters
            
            response = self.client.provision_product(**params)
            
            return {
                "status": "success",
                "record_id": response['RecordDetail']['RecordId'],
                "provisioned_product_id": response['RecordDetail'].get('ProvisionedProductId'),
                "status": response['RecordDetail']['Status']
            }
            
        except ClientError as e:
            logger.error(f"Failed to provision product: {e}")
            return {"status": "error", "message": str(e)}
    
    def list_portfolios(self) -> Dict[str, Any]:
        """List all Service Catalog portfolios"""
        if not self.client:
            return {"status": "error", "portfolios": []}
        
        try:
            portfolios = []
            paginator = self.client.get_paginator('list_portfolios')
            
            for page in paginator.paginate():
                portfolios.extend(page.get('PortfolioDetails', []))
            
            return {
                "status": "success",
                "count": len(portfolios),
                "portfolios": portfolios
            }
            
        except ClientError as e:
            logger.error(f"Failed to list portfolios: {e}")
            return {"status": "error", "portfolios": [], "message": str(e)}


class IAMIdentityCenterService:
    """AWS IAM Identity Center (SSO) Integration"""
    
    def __init__(self, region: str = 'us-east-1'):
        """Initialize IAM Identity Center client"""
        self.region = region
        try:
            self.client = boto3.client('sso-admin', region_name=region)
            self.identity_store = boto3.client('identitystore', region_name=region)
        except Exception as e:
            logger.error(f"Failed to initialize IAM Identity Center client: {e}")
            self.client = None
            self.identity_store = None
    
    def list_instances(self) -> Dict[str, Any]:
        """List IAM Identity Center instances"""
        if not self.client:
            return {"status": "error", "instances": []}
        
        try:
            response = self.client.list_instances()
            
            return {
                "status": "success",
                "count": len(response.get('Instances', [])),
                "instances": response.get('Instances', [])
            }
            
        except ClientError as e:
            logger.error(f"Failed to list instances: {e}")
            return {"status": "error", "instances": [], "message": str(e)}
    
    def create_permission_set(self, instance_arn: str, name: str, 
                             description: str, session_duration: str = 'PT1H') -> Dict[str, Any]:
        """Create a new permission set"""
        if not self.client:
            return {"status": "error", "message": "Client not initialized"}
        
        try:
            response = self.client.create_permission_set(
                InstanceArn=instance_arn,
                Name=name,
                Description=description,
                SessionDuration=session_duration
            )
            
            return {
                "status": "success",
                "permission_set_arn": response['PermissionSet']['PermissionSetArn'],
                "name": name
            }
            
        except ClientError as e:
            logger.error(f"Failed to create permission set: {e}")
            return {"status": "error", "message": str(e)}
    
    def create_account_assignment(self, instance_arn: str, permission_set_arn: str,
                                 principal_id: str, principal_type: str,
                                 target_id: str, target_type: str = 'AWS_ACCOUNT') -> Dict[str, Any]:
        """Assign a permission set to a principal for an AWS account"""
        if not self.client:
            return {"status": "error", "message": "Client not initialized"}
        
        try:
            response = self.client.create_account_assignment(
                InstanceArn=instance_arn,
                PermissionSetArn=permission_set_arn,
                PrincipalId=principal_id,
                PrincipalType=principal_type,
                TargetId=target_id,
                TargetType=target_type
            )
            
            return {
                "status": "success",
                "request_id": response['AccountAssignmentCreationStatus']['RequestId'],
                "status_message": response['AccountAssignmentCreationStatus']['Status']
            }
            
        except ClientError as e:
            logger.error(f"Failed to create account assignment: {e}")
            return {"status": "error", "message": str(e)}
    
    def create_user(self, identity_store_id: str, user_name: str,
                   display_name: str, email: str,
                   given_name: str, family_name: str) -> Dict[str, Any]:
        """Create a new user in Identity Store"""
        if not self.identity_store:
            return {"status": "error", "message": "Identity Store client not initialized"}
        
        try:
            response = self.identity_store.create_user(
                IdentityStoreId=identity_store_id,
                UserName=user_name,
                DisplayName=display_name,
                Emails=[{'Value': email, 'Type': 'Work', 'Primary': True}],
                Name={'GivenName': given_name, 'FamilyName': family_name}
            )
            
            return {
                "status": "success",
                "user_id": response['UserId'],
                "user_name": user_name
            }
            
        except ClientError as e:
            logger.error(f"Failed to create user: {e}")
            return {"status": "error", "message": str(e)}


class AWSBackendOrchestrator:
    """
    Orchestrator for all AWS backend services
    Provides unified interface for account provisioning workflow
    """
    
    def __init__(self, region: str = 'us-east-1'):
        """Initialize all backend services"""
        self.region = region
        self.organizations = AWSOrganizationsService(region)
        self.control_tower = AWSControlTowerService(region)
        self.service_catalog = AWSServiceCatalogService(region)
        self.iam_identity_center = IAMIdentityCenterService(region)
    
    def provision_account_workflow(self, account_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Complete account provisioning workflow
        
        Args:
            account_config: Dictionary containing:
                - account_name: Name of the account
                - email: Email for the account
                - ou_id: Target organizational unit
                - tags: Tags to apply
                - guardrails: List of guardrails to enable
                - permission_sets: Permission sets to create
                
        Returns:
            Dictionary with workflow status and details
        """
        workflow_result = {
            "status": "in_progress",
            "steps": [],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Step 1: Create AWS Account
        account_result = self.organizations.create_account(
            account_name=account_config['account_name'],
            email=account_config['email'],
            tags=account_config.get('tags', [])
        )
        workflow_result['steps'].append({
            "step": "create_account",
            "result": account_result
        })
        
        if account_result['status'] != 'success':
            workflow_result['status'] = 'failed'
            return workflow_result
        
        # Step 2: Move to target OU (if specified)
        if account_config.get('ou_id'):
            # Wait for account creation to complete
            # In real implementation, this would poll until complete
            move_result = {"status": "pending", "message": "Waiting for account creation"}
            workflow_result['steps'].append({
                "step": "move_to_ou",
                "result": move_result
            })
        
        # Step 3: Enable guardrails (if specified)
        if account_config.get('guardrails'):
            for guardrail in account_config['guardrails']:
                guardrail_result = self.control_tower.enable_guardrail(
                    guardrail_identifier=guardrail['identifier'],
                    target_identifier=account_config.get('ou_id', '')
                )
                workflow_result['steps'].append({
                    "step": f"enable_guardrail_{guardrail['identifier']}",
                    "result": guardrail_result
                })
        
        # Step 4: Create permission sets (if specified)
        if account_config.get('permission_sets'):
            for perm_set in account_config['permission_sets']:
                perm_result = self.iam_identity_center.create_permission_set(
                    instance_arn=perm_set['instance_arn'],
                    name=perm_set['name'],
                    description=perm_set.get('description', '')
                )
                workflow_result['steps'].append({
                    "step": f"create_permission_set_{perm_set['name']}",
                    "result": perm_result
                })
        
        workflow_result['status'] = 'completed'
        return workflow_result
    
    def get_platform_health(self) -> Dict[str, Any]:
        """Get overall health status of AWS backend services"""
        health = {
            "timestamp": datetime.utcnow().isoformat(),
            "services": {}
        }
        
        # Check Organizations
        try:
            orgs_status = self.organizations.list_accounts()
            health['services']['organizations'] = {
                "status": "healthy" if orgs_status['status'] == 'success' else "degraded",
                "account_count": orgs_status.get('count', 0)
            }
        except Exception as e:
            health['services']['organizations'] = {"status": "unhealthy", "error": str(e)}
        
        # Check Control Tower
        try:
            ct_status = self.control_tower.get_landing_zone_status()
            health['services']['control_tower'] = {
                "status": "healthy" if ct_status['status'] in ['success', 'not_deployed'] else "degraded",
                "landing_zone": ct_status.get('landing_zone_status', 'unknown')
            }
        except Exception as e:
            health['services']['control_tower'] = {"status": "unhealthy", "error": str(e)}
        
        # Check Service Catalog
        try:
            sc_status = self.service_catalog.list_portfolios()
            health['services']['service_catalog'] = {
                "status": "healthy" if sc_status['status'] == 'success' else "degraded",
                "portfolio_count": sc_status.get('count', 0)
            }
        except Exception as e:
            health['services']['service_catalog'] = {"status": "unhealthy", "error": str(e)}
        
        # Check IAM Identity Center
        try:
            idc_status = self.iam_identity_center.list_instances()
            health['services']['iam_identity_center'] = {
                "status": "healthy" if idc_status['status'] == 'success' else "degraded",
                "instance_count": idc_status.get('count', 0)
            }
        except Exception as e:
            health['services']['iam_identity_center'] = {"status": "unhealthy", "error": str(e)}
        
        return health


# Demo/Mock implementations for testing without AWS credentials
class MockAWSBackendOrchestrator:
    """Mock version for demo mode"""
    
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
    
    def provision_account_workflow(self, account_config: Dict[str, Any]) -> Dict[str, Any]:
        """Mock account provisioning"""
        return {
            "status": "completed",
            "steps": [
                {
                    "step": "create_account",
                    "result": {
                        "status": "success",
                        "request_id": "req-demo-12345",
                        "state": "SUCCEEDED",
                        "account_name": account_config['account_name'],
                        "account_id": get_aws_account_config()['account_id']
                    }
                },
                {
                    "step": "move_to_ou",
                    "result": {"status": "success", "message": "Account moved to OU"}
                },
                {
                    "step": "enable_guardrails",
                    "result": {"status": "success", "guardrails_enabled": 5}
                }
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def get_platform_health(self) -> Dict[str, Any]:
        """Mock health check"""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "mode": "demo",
            "services": {
                "organizations": {"status": "healthy", "account_count": 45},
                "control_tower": {"status": "healthy", "landing_zone": "ACTIVE"},
                "service_catalog": {"status": "healthy", "portfolio_count": 12},
                "iam_identity_center": {"status": "healthy", "instance_count": 1}
            }
        }
