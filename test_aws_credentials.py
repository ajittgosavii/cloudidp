"""
AWS Credentials Diagnostic Test
Run this to verify your AWS credentials are configured correctly
"""

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
import streamlit as st

def test_aws_credentials():
    """Test AWS credentials and connectivity"""
    
    st.header("🔍 AWS Credentials Diagnostic")
    
    results = {
        "credentials_found": False,
        "sts_works": False,
        "account_id": None,
        "region": None,
        "organizations_access": False,
        "iam_identity_center": False
    }
    
    # Test 1: Check if credentials exist
    st.subheader("Test 1: Checking for AWS Credentials")
    try:
        session = boto3.Session()
        credentials = session.get_credentials()
        if credentials:
            st.success("✅ AWS credentials found!")
            results["credentials_found"] = True
            
            # Show credential type (without exposing keys)
            if credentials.method:
                st.info(f"📋 Credential method: {credentials.method}")
        else:
            st.error("❌ No AWS credentials found")
            st.warning("Configure credentials in Streamlit Cloud Secrets")
            return results
    except Exception as e:
        st.error(f"❌ Error checking credentials: {str(e)}")
        return results
    
    # Test 2: Test STS (who am I?)
    st.subheader("Test 2: Testing AWS STS (Security Token Service)")
    try:
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        
        results["sts_works"] = True
        results["account_id"] = identity['Account']
        
        st.success("✅ Successfully connected to AWS!")
        st.json({
            "Account ID": identity['Account'],
            "User ARN": identity['Arn'],
            "User ID": identity['UserId']
        })
    except NoCredentialsError:
        st.error("❌ No credentials configured")
        return results
    except ClientError as e:
        st.error(f"❌ AWS API Error: {e.response['Error']['Message']}")
        return results
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return results
    
    # Test 3: Check current region
    st.subheader("Test 3: Checking AWS Region")
    try:
        session = boto3.Session()
        results["region"] = session.region_name or "Not set"
        st.success(f"✅ Region: {results['region']}")
    except Exception as e:
        st.warning(f"⚠️ Could not determine region: {str(e)}")
    
    # Test 4: Test AWS Organizations access
    st.subheader("Test 4: Testing AWS Organizations Access")
    try:
        org = boto3.client('organizations')
        org_info = org.describe_organization()
        
        results["organizations_access"] = True
        st.success("✅ AWS Organizations access confirmed!")
        st.json({
            "Organization ID": org_info['Organization']['Id'],
            "Master Account": org_info['Organization']['MasterAccountId'],
            "Feature Set": org_info['Organization'].get('FeatureSet', 'Unknown')
        })
        
        # Try to list accounts
        try:
            accounts_response = org.list_accounts(MaxResults=10)
            account_count = len(accounts_response.get('Accounts', []))
            st.info(f"📊 Found {account_count} AWS accounts in organization")
            
            # Show first few accounts
            if accounts_response.get('Accounts'):
                st.write("**Sample Accounts:**")
                for account in accounts_response['Accounts'][:5]:
                    st.write(f"- {account['Name']} ({account['Id']}) - {account['Status']}")
        except Exception as e:
            st.warning(f"⚠️ Could not list accounts: {str(e)}")
            
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'AccessDeniedException':
            st.warning("⚠️ No access to AWS Organizations (requires management account)")
        else:
            st.warning(f"⚠️ AWS Organizations error: {e.response['Error']['Message']}")
    except Exception as e:
        st.warning(f"⚠️ Could not access AWS Organizations: {str(e)}")
    
    # Test 5: Test IAM Identity Center (SSO)
    st.subheader("Test 5: Testing IAM Identity Center (SSO)")
    try:
        sso = boto3.client('sso-admin')
        instances = sso.list_instances()
        
        if instances.get('Instances'):
            results["iam_identity_center"] = True
            st.success("✅ IAM Identity Center (SSO) access confirmed!")
            for instance in instances['Instances']:
                st.info(f"📋 SSO Instance ARN: {instance['InstanceArn']}")
        else:
            st.warning("⚠️ No SSO instances found")
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'AccessDeniedException':
            st.warning("⚠️ No access to IAM Identity Center")
        else:
            st.warning(f"⚠️ IAM Identity Center error: {e.response['Error']['Message']}")
    except Exception as e:
        st.warning(f"⚠️ Could not access IAM Identity Center: {str(e)}")
    
    # Summary
    st.subheader("📊 Summary")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if results["credentials_found"]:
            st.metric("Credentials", "✅ Found")
        else:
            st.metric("Credentials", "❌ Missing")
    
    with col2:
        if results["sts_works"]:
            st.metric("AWS Access", "✅ Working")
        else:
            st.metric("AWS Access", "❌ Failed")
    
    with col3:
        if results["organizations_access"]:
            st.metric("Organizations", "✅ Access")
        else:
            st.metric("Organizations", "⚠️ Limited")
    
    # Recommendations
    st.subheader("💡 Recommendations")
    
    if not results["credentials_found"]:
        st.error("**Action Required:** Configure AWS credentials in Streamlit Cloud Secrets")
        st.code("""
# Add to Streamlit Cloud Secrets:
[aws]
access_key_id = "YOUR_ACCESS_KEY"
secret_access_key = "YOUR_SECRET_KEY"
region = "us-east-1"
        """)
    elif not results["sts_works"]:
        st.error("**Action Required:** Verify your AWS credentials are valid")
    elif results["organizations_access"]:
        st.success("**Great!** You have full AWS Organizations access. You can use all multi-account features!")
    else:
        st.info("**Note:** Limited to single account. For multi-account features, use credentials from the management account.")
    
    return results

if __name__ == "__main__":
    st.set_page_config(page_title="AWS Credentials Test", page_icon="🔍")
    test_aws_credentials()
