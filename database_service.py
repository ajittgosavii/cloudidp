"""
CloudIDP Backend Infrastructure - Database Service
Handles DynamoDB and RDS database operations with demo mode support
"""

import boto3
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
from backend_config import BackendConfig, DatabaseType, DYNAMODB_TABLES
from backend_models import *
import logging
from config import get_aws_account_config


logger = logging.getLogger(__name__)


class DatabaseService:
    """
    Unified database service supporting both DynamoDB and RDS
    Provides demo mode for testing without AWS infrastructure
    """
    
    def __init__(self, config: BackendConfig):
        self.config = config
        self.demo_mode = config.demo_mode
        
        if not self.demo_mode:
            if config.database_type == DatabaseType.DYNAMODB:
                self.dynamodb = boto3.resource('dynamodb', region_name=config.region)
                self.dynamodb_client = boto3.client('dynamodb', region_name=config.region)
                self._init_dynamodb()
            else:
                self._init_rds()
        else:
            # Demo mode: use in-memory storage
            self._demo_data: Dict[str, List[Dict]] = {
                "accounts": [],
                "users": [],
                "deployments": [],
                "policies": [],
                "audit_logs": [],
                "cost_data": []
            }
            self._init_demo_data()
    
    # ==================== Initialization ====================
    
    def _init_dynamodb(self):
        """Initialize DynamoDB tables if they don't exist"""
        try:
            for table_name, schema in DYNAMODB_TABLES.items():
                full_table_name = self.config.get_table_name(table_name)
                
                try:
                    self.dynamodb_client.describe_table(TableName=full_table_name)
                    logger.info(f"Table {full_table_name} already exists")
                except self.dynamodb_client.exceptions.ResourceNotFoundException:
                    self._create_dynamodb_table(full_table_name, schema)
        except Exception as e:
            logger.error(f"Error initializing DynamoDB: {e}")
    
    def _create_dynamodb_table(self, table_name: str, schema: Dict):
        """Create a DynamoDB table"""
        try:
            key_schema = [
                {'AttributeName': schema['partition_key'], 'KeyType': 'HASH'}
            ]
            attribute_definitions = [
                {'AttributeName': schema['partition_key'], 'AttributeType': 'S'}
            ]
            
            if schema.get('sort_key'):
                key_schema.append({'AttributeName': schema['sort_key'], 'KeyType': 'RANGE'})
                attribute_definitions.append({'AttributeName': schema['sort_key'], 'AttributeType': 'S'})
            
            # Add GSI attributes
            for gsi in schema.get('gsi', []):
                if not any(attr['AttributeName'] == gsi['partition_key'] for attr in attribute_definitions):
                    attribute_definitions.append({
                        'AttributeName': gsi['partition_key'],
                        'AttributeType': 'S'
                    })
            
            # Build GSI configuration
            global_secondary_indexes = []
            for gsi in schema.get('gsi', []):
                global_secondary_indexes.append({
                    'IndexName': gsi['index_name'],
                    'KeySchema': [
                        {'AttributeName': gsi['partition_key'], 'KeyType': 'HASH'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                })
            
            table_params = {
                'TableName': table_name,
                'KeySchema': key_schema,
                'AttributeDefinitions': attribute_definitions,
                'BillingMode': 'PAY_PER_REQUEST'
            }
            
            if global_secondary_indexes:
                table_params['GlobalSecondaryIndexes'] = global_secondary_indexes
                table_params['BillingMode'] = 'PROVISIONED'
                table_params['ProvisionedThroughput'] = {
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            
            self.dynamodb_client.create_table(**table_params)
            logger.info(f"Created table {table_name}")
            
        except Exception as e:
            logger.error(f"Error creating table {table_name}: {e}")
    
    def _init_rds(self):
        """Initialize RDS connection (PostgreSQL/MySQL)"""
        # TODO: Implement RDS connection logic
        logger.info("RDS initialization not yet implemented")
    
    def _init_demo_data(self):
        """Initialize demo data for testing"""
        # Add demo accounts
        demo_accounts = [
            {
                "account_id": get_aws_account_config()['account_id'],
                "account_name": "Production Account",
                "account_email": "prod@company.com",
                "org_id": "o-123456",
                "status": "active",
                "environment": "production",
                "owner": "Platform Team",
                "created_at": datetime.utcnow().isoformat()
            },
            {
                "account_id": "234567890123",
                "account_name": "Staging Account",
                "account_email": "staging@company.com",
                "org_id": "o-123456",
                "status": "active",
                "environment": "staging",
                "owner": "Platform Team",
                "created_at": datetime.utcnow().isoformat()
            },
            {
                "account_id": "345678901234",
                "account_name": "Development Account",
                "account_email": "dev@company.com",
                "org_id": "o-123456",
                "status": "active",
                "environment": "development",
                "owner": "Dev Team",
                "created_at": datetime.utcnow().isoformat()
            }
        ]
        self._demo_data["accounts"] = demo_accounts
        
        # Add demo users
        demo_users = [
            {
                "user_id": "user-001",
                "username": "admin",
                "email": "admin@company.com",
                "full_name": "Admin User",
                "role": "admin",
                "is_active": True,
                "created_at": datetime.utcnow().isoformat()
            },
            {
                "user_id": "user-002",
                "username": "architect",
                "email": "architect@company.com",
                "full_name": "Cloud Architect",
                "role": "architect",
                "is_active": True,
                "created_at": datetime.utcnow().isoformat()
            }
        ]
        self._demo_data["users"] = demo_users
    
    # ==================== Generic CRUD Operations ====================
    
    def create(self, table_name: str, item: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new item"""
        if self.demo_mode:
            item['id'] = item.get('id', str(uuid.uuid4()))
            item['created_at'] = datetime.utcnow().isoformat()
            self._demo_data[table_name].append(item)
            return item
        
        full_table_name = self.config.get_table_name(table_name)
        table = self.dynamodb.Table(full_table_name)
        table.put_item(Item=item)
        return item
    
    def get(self, table_name: str, key: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get an item by key"""
        if self.demo_mode:
            for item in self._demo_data[table_name]:
                if all(item.get(k) == v for k, v in key.items()):
                    return item
            return None
        
        full_table_name = self.config.get_table_name(table_name)
        table = self.dynamodb.Table(full_table_name)
        response = table.get_item(Key=key)
        return response.get('Item')
    
    def update(self, table_name: str, key: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update an item"""
        if self.demo_mode:
            for item in self._demo_data[table_name]:
                if all(item.get(k) == v for k, v in key.items()):
                    item.update(updates)
                    item['updated_at'] = datetime.utcnow().isoformat()
                    return item
            return None
        
        full_table_name = self.config.get_table_name(table_name)
        table = self.dynamodb.Table(full_table_name)
        
        update_expr = "SET " + ", ".join([f"#{k} = :{k}" for k in updates.keys()])
        expr_attr_names = {f"#{k}": k for k in updates.keys()}
        expr_attr_values = {f":{k}": v for k, v in updates.items()}
        
        response = table.update_item(
            Key=key,
            UpdateExpression=update_expr,
            ExpressionAttributeNames=expr_attr_names,
            ExpressionAttributeValues=expr_attr_values,
            ReturnValues="ALL_NEW"
        )
        return response.get('Attributes')
    
    def delete(self, table_name: str, key: Dict[str, Any]) -> bool:
        """Delete an item"""
        if self.demo_mode:
            original_len = len(self._demo_data[table_name])
            self._demo_data[table_name] = [
                item for item in self._demo_data[table_name]
                if not all(item.get(k) == v for k, v in key.items())
            ]
            return len(self._demo_data[table_name]) < original_len
        
        full_table_name = self.config.get_table_name(table_name)
        table = self.dynamodb.Table(full_table_name)
        table.delete_item(Key=key)
        return True
    
    def query(self, table_name: str, key_condition: Dict[str, Any], 
              filter_condition: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Query items"""
        if self.demo_mode:
            results = self._demo_data[table_name]
            
            # Apply key condition
            for key, value in key_condition.items():
                results = [item for item in results if item.get(key) == value]
            
            # Apply filter condition
            if filter_condition:
                for key, value in filter_condition.items():
                    results = [item for item in results if item.get(key) == value]
            
            return results
        
        full_table_name = self.config.get_table_name(table_name)
        table = self.dynamodb.Table(full_table_name)
        
        # Build query parameters
        key_expr = " AND ".join([f"#{k} = :{k}" for k in key_condition.keys()])
        expr_attr_names = {f"#{k}": k for k in key_condition.keys()}
        expr_attr_values = {f":{k}": v for k, v in key_condition.items()}
        
        query_params = {
            'KeyConditionExpression': key_expr,
            'ExpressionAttributeNames': expr_attr_names,
            'ExpressionAttributeValues': expr_attr_values
        }
        
        if filter_condition:
            filter_expr = " AND ".join([f"#{k} = :{k}" for k in filter_condition.keys()])
            query_params['FilterExpression'] = filter_expr
            query_params['ExpressionAttributeNames'].update({f"#{k}": k for k in filter_condition.keys()})
            query_params['ExpressionAttributeValues'].update({f":{k}": v for k, v in filter_condition.items()})
        
        response = table.query(**query_params)
        return response.get('Items', [])
    
    def scan(self, table_name: str, filter_condition: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Scan all items (expensive operation)"""
        if self.demo_mode:
            results = self._demo_data[table_name]
            if filter_condition:
                for key, value in filter_condition.items():
                    results = [item for item in results if item.get(key) == value]
            return results
        
        full_table_name = self.config.get_table_name(table_name)
        table = self.dynamodb.Table(full_table_name)
        
        scan_params = {}
        if filter_condition:
            filter_expr = " AND ".join([f"#{k} = :{k}" for k in filter_condition.keys()])
            scan_params['FilterExpression'] = filter_expr
            scan_params['ExpressionAttributeNames'] = {f"#{k}": k for k in filter_condition.keys()}
            scan_params['ExpressionAttributeValues'] = {f":{k}": v for k, v in filter_condition.items()}
        
        response = table.scan(**scan_params)
        return response.get('Items', [])
    
    # ==================== Account Operations ====================
    
    def create_account(self, account: Account) -> Account:
        """Create a new account"""
        item = account.dict()
        self.create("accounts", item)
        return account
    
    def get_account(self, account_id: str) -> Optional[Account]:
        """Get account by ID"""
        item = self.get("accounts", {"account_id": account_id})
        return Account(**item) if item else None
    
    def list_accounts(self, filters: Optional[Dict] = None) -> List[Account]:
        """List all accounts"""
        items = self.scan("accounts", filters)
        return [Account(**item) for item in items]
    
    def update_account_status(self, account_id: str, status: AccountStatus) -> Account:
        """Update account status"""
        item = self.update("accounts", {"account_id": account_id}, {"status": status.value})
        return Account(**item) if item else None
    
    # ==================== User Operations ====================
    
    def create_user(self, user: User) -> User:
        """Create a new user"""
        item = user.dict()
        self.create("users", item)
        return user
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        item = self.get("users", {"user_id": user_id})
        return User(**item) if item else None
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        items = self.query("users", {"email": email})
        return User(**items[0]) if items else None
    
    def list_users(self) -> List[User]:
        """List all users"""
        items = self.scan("users")
        return [User(**item) for item in items]
    
    # ==================== Deployment Operations ====================
    
    def create_deployment(self, deployment: Deployment) -> Deployment:
        """Create a new deployment"""
        item = deployment.dict()
        self.create("deployments", item)
        return deployment
    
    def get_deployment(self, deployment_id: str) -> Optional[Deployment]:
        """Get deployment by ID"""
        item = self.get("deployments", {"deployment_id": deployment_id})
        return Deployment(**item) if item else None
    
    def list_deployments(self, account_id: Optional[str] = None) -> List[Deployment]:
        """List deployments"""
        filters = {"account_id": account_id} if account_id else None
        items = self.scan("deployments", filters)
        return [Deployment(**item) for item in items]
    
    def update_deployment_status(self, deployment_id: str, status: DeploymentStatus, 
                                error_message: Optional[str] = None) -> Deployment:
        """Update deployment status"""
        updates = {"status": status.value}
        if status == DeploymentStatus.COMPLETED:
            updates["completed_at"] = datetime.utcnow().isoformat()
        if error_message:
            updates["error_message"] = error_message
        
        item = self.update("deployments", {"deployment_id": deployment_id}, updates)
        return Deployment(**item) if item else None
    
    # ==================== Policy Operations ====================
    
    def create_policy(self, policy: Policy) -> Policy:
        """Create a new policy"""
        item = policy.dict()
        self.create("policies", item)
        return policy
    
    def get_policy(self, policy_id: str) -> Optional[Policy]:
        """Get policy by ID"""
        item = self.get("policies", {"policy_id": policy_id})
        return Policy(**item) if item else None
    
    def list_policies(self, policy_type: Optional[PolicyType] = None) -> List[Policy]:
        """List policies"""
        filters = {"policy_type": policy_type.value} if policy_type else None
        items = self.scan("policies", filters)
        return [Policy(**item) for item in items]
    
    # ==================== Audit Log Operations ====================
    
    def create_audit_log(self, log: AuditLog) -> AuditLog:
        """Create audit log entry"""
        item = log.dict()
        self.create("audit_logs", item)
        return log
    
    def list_audit_logs(self, user_id: Optional[str] = None, 
                       resource_type: Optional[str] = None) -> List[AuditLog]:
        """List audit logs"""
        filters = {}
        if user_id:
            filters["user_id"] = user_id
        if resource_type:
            filters["resource_type"] = resource_type
        
        items = self.scan("audit_logs", filters if filters else None)
        return [AuditLog(**item) for item in items]
    
    # ==================== Cost Data Operations ====================
    
    def create_cost_data(self, cost: CostData) -> CostData:
        """Create cost data entry"""
        item = cost.dict()
        self.create("cost_data", item)
        return cost
    
    def get_cost_data(self, date: str, account_id: Optional[str] = None) -> List[CostData]:
        """Get cost data for a date"""
        filters = {"date": date}
        if account_id:
            filters["account_id"] = account_id
        
        items = self.scan("cost_data", filters)
        return [CostData(**item) for item in items]
