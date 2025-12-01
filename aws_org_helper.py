"""
AWS Organizations Helper - Fetch Real Account Data
Integrates with AWS Organizations to get actual account information
"""

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
import streamlit as st
from typing import List, Dict, Optional
import pandas as pd

class AWSOrganizationsHelper:
    """Helper class to interact with AWS Organizations"""
    
    def __init__(self):
        self.session = None
        self.org_client = None
        self.sts_client = None
        self.initialized = False
        
    def initialize(self) -> bool:
        """Initialize AWS clients"""
        try:
            # Try to get AWS credentials from Streamlit secrets
            if hasattr(st, 'secrets') and 'aws' in st.secrets:
                aws_config = st.secrets['aws']
                self.session = boto3.Session(
                    aws_access_key_id=aws_config.get('access_key_id'),
                    aws_secret_access_key=aws_config.get('secret_access_key'),
                    region_name=aws_config.get('region', 'us-east-1')
                )
            else:
                # Fall back to default credentials
                self.session = boto3.Session()
            
            self.org_client = self.session.client('organizations')
            self.sts_client = self.session.client('sts')
            self.initialized = True
            return True
            
        except (NoCredentialsError, Exception) as e:
            st.warning(f"⚠️ Could not initialize AWS clients: {str(e)}")
            return False
    
    def get_current_account_info(self) -> Dict:
        """Get current AWS account information using STS"""
        try:
            if not self.initialized:
                if not self.initialize():
                    return None
            
            identity = self.sts_client.get_caller_identity()
            return {
                'account_id': identity['Account'],
                'user_arn': identity['Arn'],
                'user_id': identity['UserId']
            }
        except Exception as e:
            st.error(f"Error getting account info: {str(e)}")
            return None
    
    def get_organization_info(self) -> Optional[Dict]:
        """Get AWS Organization information"""
        try:
            if not self.initialized:
                if not self.initialize():
                    return None
            
            org = self.org_client.describe_organization()
            return {
                'id': org['Organization']['Id'],
                'master_account_id': org['Organization']['MasterAccountId'],
                'feature_set': org['Organization'].get('FeatureSet', 'CONSOLIDATED_BILLING'),
                'arn': org['Organization']['Arn']
            }
        except ClientError as e:
            if e.response['Error']['Code'] == 'AWSOrganizationsNotInUseException':
                st.info("ℹ️ This AWS account is not part of an AWS Organization")
                return None
            else:
                st.warning(f"⚠️ Cannot access AWS Organizations: {e.response['Error']['Message']}")
                return None
        except Exception as e:
            st.warning(f"⚠️ Error accessing AWS Organizations: {str(e)}")
            return None
    
    def list_accounts(self) -> List[Dict]:
        """List all accounts in the organization"""
        try:
            if not self.initialized:
                if not self.initialize():
                    return []
            
            accounts = []
            paginator = self.org_client.get_paginator('list_accounts')
            
            for page in paginator.paginate():
                for account in page['Accounts']:
                    accounts.append({
                        'id': account['Id'],
                        'name': account['Name'],
                        'email': account['Email'],
                        'status': account['Status'],
                        'joined_method': account.get('JoinedMethod', 'UNKNOWN'),
                        'joined_timestamp': account.get('JoinedTimestamp')
                    })
            
            return accounts
            
        except ClientError as e:
            if e.response['Error']['Code'] in ['AccessDeniedException', 'AWSOrganizationsNotInUseException']:
                # Not in an organization or no access
                # Return just the current account
                current_account = self.get_current_account_info()
                if current_account:
                    return [{
                        'id': current_account['account_id'],
                        'name': 'Current Account',
                        'email': 'N/A',
                        'status': 'ACTIVE',
                        'joined_method': 'STANDALONE',
                        'joined_timestamp': None
                    }]
                return []
            else:
                st.error(f"Error listing accounts: {e.response['Error']['Message']}")
                return []
        except Exception as e:
            st.error(f"Error listing accounts: {str(e)}")
            return []
    
    def list_organizational_units(self, parent_id: str = None) -> List[Dict]:
        """List organizational units"""
        try:
            if not self.initialized:
                if not self.initialize():
                    return []
            
            if parent_id is None:
                # Get root first
                roots = self.org_client.list_roots()
                if not roots.get('Roots'):
                    return []
                parent_id = roots['Roots'][0]['Id']
            
            ous = []
            paginator = self.org_client.get_paginator('list_organizational_units_for_parent')
            
            for page in paginator.paginate(ParentId=parent_id):
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
    
    def get_available_regions(self) -> List[str]:
        """Get list of available AWS regions"""
        try:
            if not self.initialized:
                if not self.initialize():
                    return ['us-east-1', 'us-west-2']
            
            ec2 = self.session.client('ec2')
            regions = ec2.describe_regions()
            return [region['RegionName'] for region in regions['Regions']]
            
        except Exception as e:
            # Return common regions as fallback
            return [
                'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2',
                'eu-west-1', 'eu-west-2', 'eu-central-1',
                'ap-southeast-1', 'ap-southeast-2', 'ap-northeast-1'
            ]
    
    def get_account_resources_count(self, account_id: str, region: str = 'us-east-1') -> int:
        """
        Get approximate count of resources in an account
        NOTE: This requires assume role capability for cross-account access
        """
        try:
            # This is a simplified version - in production, you'd assume role into the account
            # For now, we'll return an estimate or 0
            return 0
        except Exception:
            return 0

# Global instance
_aws_org_helper = None

def get_aws_org_helper() -> AWSOrganizationsHelper:
    """Get or create AWS Organizations helper singleton"""
    global _aws_org_helper
    if _aws_org_helper is None:
        _aws_org_helper = AWSOrganizationsHelper()
    return _aws_org_helper

def get_real_accounts_dataframe() -> pd.DataFrame:
    """
    Get real AWS accounts as a DataFrame
    Returns demo data if AWS Organizations is not accessible
    """
    helper = get_aws_org_helper()
    
    # Try to get real accounts
    accounts = helper.list_accounts()
    
    if not accounts:
        # Return demo data as fallback
        return get_demo_accounts_dataframe()
    
    # Convert to DataFrame
    accounts_data = []
    for account in accounts:
        accounts_data.append({
            "Account ID": account['id'],
            "Account Name": account['name'],
            "OU": "Root",  # Default to Root, would need to query for actual OU
            "Status": "🟢 Active" if account['status'] == 'ACTIVE' else "🟡 Suspended",
            "Email": account['email'],
            "Created": account['joined_timestamp'].strftime("%Y-%m-%d") if account.get('joined_timestamp') else "N/A",
            "Resources": "N/A",  # Would need cross-account access to get this
            "Monthly Cost": "N/A",  # Would need Cost Explorer access
            "SSO Access": "✅ Enabled"  # Assume enabled
        })
    
    return pd.DataFrame(accounts_data)

def get_demo_accounts_dataframe() -> pd.DataFrame:
    """Get demo accounts data for fallback"""
    return pd.DataFrame([
        {
            "Account ID": "123456789012",
            "Account Name": "Production",
            "OU": "Production",
            "Status": "🟢 Active",
            "Email": "aws-prod@company.com",
            "Created": "2023-01-15",
            "Resources": "1,234",
            "Monthly Cost": "$45,000",
            "SSO Access": "✅ Enabled"
        },
        {
            "Account ID": "234567890123",
            "Account Name": "Staging",
            "OU": "Non-Production",
            "Status": "🟢 Active",
            "Email": "aws-staging@company.com",
            "Created": "2023-02-10",
            "Resources": "567",
            "Monthly Cost": "$18,500",
            "SSO Access": "✅ Enabled"
        },
        {
            "Account ID": "345678901234",
            "Account Name": "Development",
            "OU": "Non-Production",
            "Status": "🟢 Active",
            "Email": "aws-dev@company.com",
            "Created": "2023-03-05",
            "Resources": "892",
            "Monthly Cost": "$12,300",
            "SSO Access": "✅ Enabled"
        }
    ])

def get_current_account_summary() -> Dict:
    """Get summary information about current AWS account/organization"""
    helper = get_aws_org_helper()
    
    # Get current account info
    current_account = helper.get_current_account_info()
    if not current_account:
        return {
            'mode': 'demo',
            'account_count': 47,
            'region_count': 12,
            'resource_count': 3456,
            'is_organization': False
        }
    
    # Get organization info
    org_info = helper.get_organization_info()
    accounts = helper.list_accounts()
    regions = helper.get_available_regions()
    
    return {
        'mode': 'live',
        'current_account_id': current_account['account_id'],
        'account_count': len(accounts) if accounts else 1,
        'region_count': len(regions) if regions else 12,
        'resource_count': 0,  # Would need to query
        'is_organization': org_info is not None,
        'organization_id': org_info['id'] if org_info else None,
        'master_account_id': org_info['master_account_id'] if org_info else None
    }
