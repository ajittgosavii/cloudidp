"""
CloudIDP - AWS Database Services Integration Module
RDS, DynamoDB, and database management operations
"""

import streamlit as st
import boto3
from typing import Dict, List, Optional, Any
from botocore.exceptions import ClientError


class DatabaseIntegration:
    """AWS Database services integration for CloudIDP"""
    
    def __init__(self, demo_mode: bool = True, region: str = 'us-east-1'):
        self.demo_mode = demo_mode
        self.region = region
        
        if not demo_mode:
            try:
                # Try to read from Streamlit secrets first
                if hasattr(st, 'secrets') and 'aws' in st.secrets:
                    self.rds_client = boto3.client(
                        'rds',
                        aws_access_key_id=st.secrets["aws"]["access_key"],
                        aws_secret_access_key=st.secrets["aws"]["secret_access_key"],
                        region_name=st.secrets["aws"].get("region", region)
                    )
                    self.dynamodb_client = boto3.client(
                        'dynamodb',
                        aws_access_key_id=st.secrets["aws"]["access_key"],
                        aws_secret_access_key=st.secrets["aws"]["secret_access_key"],
                        region_name=st.secrets["aws"].get("region", region)
                    )
                    self.dynamodb_resource = boto3.resource(
                        'dynamodb',
                        aws_access_key_id=st.secrets["aws"]["access_key"],
                        aws_secret_access_key=st.secrets["aws"]["secret_access_key"],
                        region_name=st.secrets["aws"].get("region", region)
                    )
                else:
                    # Fallback to default credentials (IAM role, env vars, etc.)
                    self.rds_client = boto3.client('rds', region_name=region)
                    self.dynamodb_client = boto3.client('dynamodb', region_name=region)
                    self.dynamodb_resource = boto3.resource('dynamodb', region_name=region)
            except Exception as e:
                print(f"Warning: {e}")
                self.demo_mode = True
    
    # ============= RDS OPERATIONS =============
    
    def create_db_instance(self, db_instance_identifier: str,
                          db_instance_class: str, engine: str,
                          master_username: str, master_password: str,
                          allocated_storage: int = 20,
                          multi_az: bool = False) -> Dict[str, Any]:
        """Create an RDS database instance"""
        if self.demo_mode:
            return {
                'success': True,
                'db_instance_identifier': db_instance_identifier,
                'endpoint': f'{db_instance_identifier}.demo.us-east-1.rds.amazonaws.com',
                'status': 'creating',
                'demo_mode': True
            }
        
        try:
            response = self.rds_client.create_db_instance(
                DBInstanceIdentifier=db_instance_identifier,
                DBInstanceClass=db_instance_class,
                Engine=engine,
                MasterUsername=master_username,
                MasterUserPassword=master_password,
                AllocatedStorage=allocated_storage,
                MultiAZ=multi_az
            )
            
            return {
                'success': True,
                'db_instance_identifier': db_instance_identifier,
                'status': response['DBInstance']['DBInstanceStatus']
            }
        except ClientError as e:
            return {'success': False, 'error': str(e)}
    
    def list_db_instances(self) -> Dict[str, Any]:
        """List all RDS instances"""
        if self.demo_mode:
            return {
                'success': True,
                'count': 3,
                'db_instances': [
                    {
                        'DBInstanceIdentifier': 'prod-mysql-01',
                        'Engine': 'mysql',
                        'DBInstanceClass': 'db.r5.large',
                        'DBInstanceStatus': 'available',
                        'AllocatedStorage': 100,
                        'MultiAZ': True
                    },
                    {
                        'DBInstanceIdentifier': 'prod-postgres-01',
                        'Engine': 'postgres',
                        'DBInstanceClass': 'db.r5.xlarge',
                        'DBInstanceStatus': 'available',
                        'AllocatedStorage': 500,
                        'MultiAZ': True
                    },
                    {
                        'DBInstanceIdentifier': 'dev-mysql-01',
                        'Engine': 'mysql',
                        'DBInstanceClass': 'db.t3.medium',
                        'DBInstanceStatus': 'stopped',
                        'AllocatedStorage': 20,
                        'MultiAZ': False
                    }
                ],
                'demo_mode': True
            }
        
        try:
            response = self.rds_client.describe_db_instances()
            return {
                'success': True,
                'count': len(response['DBInstances']),
                'db_instances': response['DBInstances']
            }
        except ClientError as e:
            return {'success': False, 'error': str(e)}
    
    def create_db_snapshot(self, db_instance_identifier: str,
                          snapshot_identifier: str) -> Dict[str, Any]:
        """Create a database snapshot"""
        if self.demo_mode:
            return {
                'success': True,
                'snapshot_identifier': snapshot_identifier,
                'status': 'creating',
                'demo_mode': True
            }
        
        try:
            response = self.rds_client.create_db_snapshot(
                DBSnapshotIdentifier=snapshot_identifier,
                DBInstanceIdentifier=db_instance_identifier
            )
            return {
                'success': True,
                'snapshot_identifier': snapshot_identifier,
                'status': response['DBSnapshot']['Status']
            }
        except ClientError as e:
            return {'success': False, 'error': str(e)}
    
    # ============= DYNAMODB OPERATIONS =============
    
    def create_dynamodb_table(self, table_name: str,
                             partition_key: str,
                             partition_key_type: str = 'S',
                             sort_key: Optional[str] = None,
                             sort_key_type: str = 'S',
                             billing_mode: str = 'PAY_PER_REQUEST') -> Dict[str, Any]:
        """Create a DynamoDB table"""
        if self.demo_mode:
            return {
                'success': True,
                'table_name': table_name,
                'status': 'CREATING',
                'demo_mode': True
            }
        
        try:
            key_schema = [
                {'AttributeName': partition_key, 'KeyType': 'HASH'}
            ]
            attribute_definitions = [
                {'AttributeName': partition_key, 'AttributeType': partition_key_type}
            ]
            
            if sort_key:
                key_schema.append({'AttributeName': sort_key, 'KeyType': 'RANGE'})
                attribute_definitions.append({'AttributeName': sort_key, 'AttributeType': sort_key_type})
            
            response = self.dynamodb_client.create_table(
                TableName=table_name,
                KeySchema=key_schema,
                AttributeDefinitions=attribute_definitions,
                BillingMode=billing_mode
            )
            
            return {
                'success': True,
                'table_name': table_name,
                'status': response['TableDescription']['TableStatus']
            }
        except ClientError as e:
            return {'success': False, 'error': str(e)}
    
    def list_dynamodb_tables(self) -> Dict[str, Any]:
        """List all DynamoDB tables"""
        if self.demo_mode:
            return {
                'success': True,
                'count': 4,
                'tables': [
                    'cloudidp-users',
                    'cloudidp-accounts',
                    'cloudidp-resources',
                    'cloudidp-audit-logs'
                ],
                'demo_mode': True
            }
        
        try:
            response = self.dynamodb_client.list_tables()
            return {
                'success': True,
                'count': len(response['TableNames']),
                'tables': response['TableNames']
            }
        except ClientError as e:
            return {'success': False, 'error': str(e)}
    
    def put_item(self, table_name: str, item: Dict[str, Any]) -> Dict[str, Any]:
        """Put an item in DynamoDB table"""
        if self.demo_mode:
            return {
                'success': True,
                'table_name': table_name,
                'demo_mode': True
            }
        
        try:
            table = self.dynamodb_resource.Table(table_name)
            table.put_item(Item=item)
            return {'success': True, 'table_name': table_name}
        except ClientError as e:
            return {'success': False, 'error': str(e)}
    
    def query_table(self, table_name: str,
                   key_condition_expression: str,
                   expression_attribute_values: Dict[str, Any]) -> Dict[str, Any]:
        """Query a DynamoDB table"""
        if self.demo_mode:
            return {
                'success': True,
                'count': 2,
                'items': [
                    {'id': '1', 'name': 'Demo Item 1'},
                    {'id': '2', 'name': 'Demo Item 2'}
                ],
                'demo_mode': True
            }
        
        try:
            table = self.dynamodb_resource.Table(table_name)
            response = table.query(
                KeyConditionExpression=key_condition_expression,
                ExpressionAttributeValues=expression_attribute_values
            )
            return {
                'success': True,
                'count': response['Count'],
                'items': response['Items']
            }
        except ClientError as e:
            return {'success': False, 'error': str(e)}


if __name__ == "__main__":
    print("Database Integration Demo")
    db = DatabaseIntegration(demo_mode=True)
    
    # Test RDS listing
    rds_instances = db.list_db_instances()
    print(f"RDS Instances: {rds_instances['count']}")
    for inst in rds_instances['db_instances'][:2]:
        print(f"  - {inst['DBInstanceIdentifier']} ({inst['Engine']}): {inst['DBInstanceStatus']}")
    
    # Test DynamoDB listing
    print(f"\nDynamoDB Tables: {db.list_dynamodb_tables()['count']}")
    
    print("\n✅ Demo completed!")