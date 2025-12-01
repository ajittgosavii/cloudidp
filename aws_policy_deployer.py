"""
AWS Policy Deployment Engine
Apply CloudIDP policies directly to AWS Organizations, Config, and SCPs
"""

import boto3
from botocore.exceptions import ClientError
import streamlit as st
from typing import Dict, List, Optional
import json
from datetime import datetime

class AWSPolicyDeployer:
    """Deploy CloudIDP policies to AWS"""
    
    def __init__(self):
        self.session = None
        self.org_client = None
        self.config_client = None
        self.initialized = False
        
    def initialize(self) -> bool:
        """Initialize AWS clients"""
        try:
            if hasattr(st, 'secrets') and 'aws' in st.secrets:
                aws_config = st.secrets['aws']
                self.session = boto3.Session(
                    aws_access_key_id=aws_config.get('access_key_id'),
                    aws_secret_access_key=aws_config.get('secret_access_key'),
                    region_name=aws_config.get('region', 'us-east-1')
                )
            else:
                self.session = boto3.Session()
            
            self.org_client = self.session.client('organizations')
            self.config_client = self.session.client('config')
            self.initialized = True
            return True
            
        except Exception as e:
            st.error(f"Failed to initialize AWS clients: {str(e)}")
            return False
    
    def create_tag_policy(self, policy_name: str, required_tags: List[Dict], scope: str = "Production") -> Optional[str]:
        """
        Create AWS Organizations Tag Policy
        
        Args:
            policy_name: Name of the policy
            required_tags: List of required tags with their configurations
            scope: Scope of the policy (Production, Non-Production, etc.)
        
        Returns:
            Policy ID if successful, None otherwise
        """
        if not self.initialized:
            if not self.initialize():
                return None
        
        try:
            # Build tag policy content
            policy_content = {
                "tags": {}
            }
            
            for tag in required_tags:
                tag_key = tag['key']
                tag_values = tag.get('values', [])
                resources = tag.get('resources', ['*'])
                
                policy_content['tags'][tag_key] = {
                    "tag_key": {
                        "@@assign": tag_key
                    }
                }
                
                if tag_values:
                    policy_content['tags'][tag_key]["tag_value"] = {
                        "@@assign": tag_values
                    }
                
                if resources and resources != ['*']:
                    policy_content['tags'][tag_key]["enforced_for"] = {
                        "@@assign": resources
                    }
            
            # Create the policy
            response = self.org_client.create_policy(
                Content=json.dumps(policy_content),
                Description=f"Tag policy for {scope} - Created by CloudIDP",
                Name=policy_name,
                Type='TAG_POLICY'
            )
            
            policy_id = response['Policy']['PolicySummary']['Id']
            st.success(f"✅ Tag Policy created successfully! Policy ID: {policy_id}")
            return policy_id
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'DuplicatePolicyException':
                st.warning(f"⚠️ Policy '{policy_name}' already exists. Use update instead.")
            elif error_code == 'PolicyTypeNotEnabledException':
                st.error("❌ Tag Policies not enabled in AWS Organizations. Enable them first.")
                st.info("Run: `aws organizations enable-policy-type --root-id r-xxxx --policy-type TAG_POLICY`")
            else:
                st.error(f"❌ Error creating tag policy: {e.response['Error']['Message']}")
            return None
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")
            return None
    
    def attach_policy_to_ou(self, policy_id: str, ou_id: str) -> bool:
        """Attach policy to Organizational Unit"""
        if not self.initialized:
            if not self.initialize():
                return False
        
        try:
            self.org_client.attach_policy(
                PolicyId=policy_id,
                TargetId=ou_id
            )
            st.success(f"✅ Policy attached to OU: {ou_id}")
            return True
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'DuplicatePolicyAttachmentException':
                st.info(f"ℹ️ Policy already attached to this OU")
                return True
            else:
                st.error(f"❌ Error attaching policy: {e.response['Error']['Message']}")
            return False
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")
            return False
    
    def create_config_rule_for_tags(self, rule_name: str, required_tags: List[str], resource_types: List[str]) -> bool:
        """
        Create AWS Config Rule for tag compliance
        
        Args:
            rule_name: Name of the Config rule
            required_tags: List of required tag keys
            resource_types: List of AWS resource types to check
        
        Returns:
            True if successful, False otherwise
        """
        if not self.initialized:
            if not self.initialize():
                return False
        
        try:
            # Map CloudIDP resource types to AWS Config resource types
            resource_type_mapping = {
                "ec2:instance": "AWS::EC2::Instance",
                "s3:bucket": "AWS::S3::Bucket",
                "rds:db": "AWS::RDS::DBInstance",
                "lambda:function": "AWS::Lambda::Function",
                "dynamodb:table": "AWS::DynamoDB::Table"
            }
            
            config_resource_types = [
                resource_type_mapping.get(rt, rt) 
                for rt in resource_types
            ]
            
            # Create Config rule using AWS managed rule "required-tags"
            self.config_client.put_config_rule(
                ConfigRule={
                    'ConfigRuleName': rule_name,
                    'Description': f'Requires tags: {", ".join(required_tags)} - Created by CloudIDP',
                    'Scope': {
                        'ComplianceResourceTypes': config_resource_types
                    },
                    'Source': {
                        'Owner': 'AWS',
                        'SourceIdentifier': 'REQUIRED_TAGS'
                    },
                    'InputParameters': json.dumps({
                        f'tag{i+1}Key': tag
                        for i, tag in enumerate(required_tags[:6])  # AWS Config supports up to 6 tags
                    })
                }
            )
            
            st.success(f"✅ AWS Config Rule '{rule_name}' created successfully!")
            return True
            
        except ClientError as e:
            st.error(f"❌ Error creating Config rule: {e.response['Error']['Message']}")
            return False
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")
            return False
    
    def create_scp_for_tags(self, scp_name: str, required_tags: List[str], actions: List[str]) -> Optional[str]:
        """
        Create Service Control Policy (SCP) to enforce tags
        
        Args:
            scp_name: Name of the SCP
            required_tags: List of required tag keys
            actions: List of AWS actions to restrict
        
        Returns:
            Policy ID if successful, None otherwise
        """
        if not self.initialized:
            if not self.initialize():
                return None
        
        try:
            # Build SCP content - deny actions if tags are missing
            statements = []
            
            # Deny if any required tag is missing
            for tag_key in required_tags:
                statements.append({
                    "Sid": f"DenyWithout{tag_key.replace(':', '')}",
                    "Effect": "Deny",
                    "Action": actions,
                    "Resource": "*",
                    "Condition": {
                        "Null": {
                            f"aws:RequestTag/{tag_key}": "true"
                        }
                    }
                })
            
            scp_content = {
                "Version": "2012-10-17",
                "Statement": statements
            }
            
            # Create the SCP
            response = self.org_client.create_policy(
                Content=json.dumps(scp_content),
                Description=f"Enforce required tags - Created by CloudIDP",
                Name=scp_name,
                Type='SERVICE_CONTROL_POLICY'
            )
            
            policy_id = response['Policy']['PolicySummary']['Id']
            st.success(f"✅ Service Control Policy created! Policy ID: {policy_id}")
            return policy_id
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'DuplicatePolicyException':
                st.warning(f"⚠️ SCP '{scp_name}' already exists")
            else:
                st.error(f"❌ Error creating SCP: {e.response['Error']['Message']}")
            return None
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")
            return None
    
    def list_organizational_units(self) -> List[Dict]:
        """List all OUs to allow user to select deployment target"""
        if not self.initialized:
            if not self.initialize():
                return []
        
        try:
            # Get root first
            roots = self.org_client.list_roots()
            if not roots.get('Roots'):
                return []
            
            root_id = roots['Roots'][0]['Id']
            
            # List OUs under root
            ous = []
            paginator = self.org_client.get_paginator('list_organizational_units_for_parent')
            
            for page in paginator.paginate(ParentId=root_id):
                for ou in page['OrganizationalUnits']:
                    ous.append({
                        'id': ou['Id'],
                        'name': ou['Name'],
                        'arn': ou['Arn']
                    })
            
            return ous
            
        except Exception as e:
            st.warning(f"Could not list OUs: {str(e)}")
            return []
    
    def get_policy_status(self, policy_id: str) -> Dict:
        """Get status of a deployed policy"""
        if not self.initialized:
            if not self.initialize():
                return {'status': 'unknown'}
        
        try:
            policy = self.org_client.describe_policy(PolicyId=policy_id)
            
            # Get attachments
            targets = self.org_client.list_targets_for_policy(PolicyId=policy_id)
            
            return {
                'status': 'active',
                'name': policy['Policy']['PolicySummary']['Name'],
                'type': policy['Policy']['PolicySummary']['Type'],
                'attached_to': len(targets.get('Targets', [])),
                'last_updated': policy['Policy']['PolicySummary'].get('LastUpdatedTimestamp')
            }
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

# Global instance
_policy_deployer = None

def get_policy_deployer() -> AWSPolicyDeployer:
    """Get or create policy deployer singleton"""
    global _policy_deployer
    if _policy_deployer is None:
        _policy_deployer = AWSPolicyDeployer()
    return _policy_deployer

def deploy_tag_policy_to_aws(
    policy_name: str,
    required_tags: List[Dict],
    scope: str,
    deployment_targets: List[str],
    create_config_rule: bool = True,
    create_scp: bool = False
) -> Dict:
    """
    Complete deployment workflow for tag policy
    
    Args:
        policy_name: Name of the policy
        required_tags: List of tag configurations
        scope: Scope (Production, Non-Production, etc.)
        deployment_targets: List of OU IDs to attach policy to
        create_config_rule: Whether to create AWS Config rule
        create_scp: Whether to create SCP for enforcement
    
    Returns:
        Dict with deployment results
    """
    deployer = get_policy_deployer()
    results = {
        'tag_policy_id': None,
        'config_rule_created': False,
        'scp_id': None,
        'attachments': [],
        'status': 'pending'
    }
    
    with st.spinner("🚀 Deploying tag policy to AWS..."):
        # Step 1: Create Tag Policy
        st.info("📝 Creating AWS Organizations Tag Policy...")
        tag_policy_id = deployer.create_tag_policy(policy_name, required_tags, scope)
        
        if not tag_policy_id:
            results['status'] = 'failed'
            return results
        
        results['tag_policy_id'] = tag_policy_id
        
        # Step 2: Attach to OUs
        if deployment_targets:
            st.info(f"🔗 Attaching policy to {len(deployment_targets)} organizational unit(s)...")
            for ou_id in deployment_targets:
                if deployer.attach_policy_to_ou(tag_policy_id, ou_id):
                    results['attachments'].append(ou_id)
        
        # Step 3: Create Config Rule (optional)
        if create_config_rule:
            st.info("⚙️ Creating AWS Config Rule for compliance monitoring...")
            tag_keys = [tag['key'] for tag in required_tags]
            resource_types = list(set([
                res 
                for tag in required_tags 
                for res in tag.get('resources', ['ec2:instance'])
            ]))
            
            config_rule_name = f"CloudIDP-{policy_name.replace(' ', '-')}-TagCompliance"
            if deployer.create_config_rule_for_tags(config_rule_name, tag_keys, resource_types):
                results['config_rule_created'] = True
        
        # Step 4: Create SCP (optional)
        if create_scp:
            st.info("🛡️ Creating Service Control Policy for enforcement...")
            tag_keys = [tag['key'] for tag in required_tags]
            actions = [
                "ec2:RunInstances",
                "s3:CreateBucket",
                "rds:CreateDBInstance",
                "dynamodb:CreateTable",
                "lambda:CreateFunction"
            ]
            
            scp_name = f"CloudIDP-{policy_name.replace(' ', '-')}-Enforce"
            scp_id = deployer.create_scp_for_tags(scp_name, tag_keys, actions)
            if scp_id:
                results['scp_id'] = scp_id
    
    results['status'] = 'success'
    return results
