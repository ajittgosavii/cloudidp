"""
CloudIDP Backend Infrastructure - Configuration Management
Centralized configuration for all backend services
"""

import os
from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum


class Environment(str, Enum):
    """Deployment environments"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    DEMO = "demo"


class DatabaseType(str, Enum):
    """Database backend types"""
    DYNAMODB = "dynamodb"
    RDS_POSTGRES = "rds_postgres"
    RDS_MYSQL = "rds_mysql"


class AuthProvider(str, Enum):
    """Authentication providers"""
    COGNITO = "cognito"
    OKTA = "okta"
    AZURE_AD = "azure_ad"
    AUTH0 = "auth0"
    DEMO = "demo"


@dataclass
class BackendConfig:
    """Backend infrastructure configuration"""
    
    # Environment
    environment: Environment = Environment.DEMO
    demo_mode: bool = True
    region: str = "us-east-1"
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_base_path: str = "/api/v1"
    cors_origins: list = None
    
    # Database Configuration
    database_type: DatabaseType = DatabaseType.DYNAMODB
    dynamodb_table_prefix: str = "cloudidp"
    rds_host: Optional[str] = None
    rds_port: int = 5432
    rds_database: str = "cloudidp"
    rds_username: Optional[str] = None
    rds_password: Optional[str] = None
    
    # Authentication Configuration
    auth_provider: AuthProvider = AuthProvider.DEMO
    cognito_user_pool_id: Optional[str] = None
    cognito_client_id: Optional[str] = None
    cognito_region: Optional[str] = None
    jwt_secret_key: str = "demo-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 1440  # 24 hours
    
    # Queue Configuration
    sqs_queue_prefix: str = "cloudidp"
    sqs_visibility_timeout: int = 300  # 5 minutes
    sqs_message_retention: int = 345600  # 4 days
    sqs_max_receive_count: int = 3
    
    # Lambda Configuration
    lambda_function_prefix: str = "cloudidp"
    lambda_timeout: int = 900  # 15 minutes
    lambda_memory_size: int = 512  # MB
    lambda_runtime: str = "python3.11"
    
    # Cache Configuration
    enable_caching: bool = True
    cache_ttl_seconds: int = 300  # 5 minutes
    redis_host: Optional[str] = None
    redis_port: int = 6379
    
    # Monitoring Configuration
    enable_cloudwatch: bool = True
    enable_xray: bool = False
    log_level: str = "INFO"
    
    # Security Configuration
    enable_encryption: bool = True
    kms_key_id: Optional[str] = None
    enable_waf: bool = False
    
    # Rate Limiting
    rate_limit_per_minute: int = 100
    rate_limit_burst: int = 200
    
    # Feature Flags
    enable_organizations_integration: bool = True
    enable_identity_center_integration: bool = True
    enable_service_catalog_integration: bool = True
    enable_control_tower_integration: bool = True
    enable_cloudformation_integration: bool = True
    enable_cost_explorer_integration: bool = True
    enable_systems_manager_integration: bool = True
    enable_compute_network_integration: bool = True
    enable_database_integration: bool = True
    
    def __post_init__(self):
        """Initialize derived configurations"""
        if self.cors_origins is None:
            self.cors_origins = ["http://localhost:8501", "http://localhost:3000"]
        
        # Auto-configure based on environment
        if self.environment == Environment.PRODUCTION:
            self.demo_mode = False
            self.enable_encryption = True
            self.enable_waf = True
            self.enable_xray = True
            self.log_level = "WARNING"
        
        elif self.environment == Environment.STAGING:
            self.demo_mode = False
            self.enable_encryption = True
            self.log_level = "INFO"
        
        elif self.environment == Environment.DEMO:
            self.demo_mode = True
            self.auth_provider = AuthProvider.DEMO
            self.enable_encryption = False
            self.log_level = "DEBUG"
    
    @classmethod
    def from_environment(cls) -> "BackendConfig":
        """Load configuration from environment variables"""
        return cls(
            environment=Environment(os.getenv("CLOUDIDP_ENV", "demo")),
            demo_mode=os.getenv("DEMO_MODE", "true").lower() == "true",
            region=os.getenv("AWS_REGION", "us-east-1"),
            
            # API
            api_host=os.getenv("API_HOST", "0.0.0.0"),
            api_port=int(os.getenv("API_PORT", "8000")),
            
            # Database
            database_type=DatabaseType(os.getenv("DATABASE_TYPE", "dynamodb")),
            rds_host=os.getenv("RDS_HOST"),
            rds_username=os.getenv("RDS_USERNAME"),
            rds_password=os.getenv("RDS_PASSWORD"),
            
            # Auth
            auth_provider=AuthProvider(os.getenv("AUTH_PROVIDER", "demo")),
            cognito_user_pool_id=os.getenv("COGNITO_USER_POOL_ID"),
            cognito_client_id=os.getenv("COGNITO_CLIENT_ID"),
            jwt_secret_key=os.getenv("JWT_SECRET_KEY", "demo-secret-key-change-in-production"),
            
            # Cache
            redis_host=os.getenv("REDIS_HOST"),
        )
    
    def get_table_name(self, table_suffix: str) -> str:
        """Generate DynamoDB table name with prefix"""
        return f"{self.dynamodb_table_prefix}_{self.environment.value}_{table_suffix}"
    
    def get_queue_name(self, queue_suffix: str) -> str:
        """Generate SQS queue name with prefix"""
        return f"{self.sqs_queue_prefix}_{self.environment.value}_{queue_suffix}"
    
    def get_lambda_name(self, function_suffix: str) -> str:
        """Generate Lambda function name with prefix"""
        return f"{self.lambda_function_prefix}_{self.environment.value}_{function_suffix}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            "environment": self.environment.value,
            "demo_mode": self.demo_mode,
            "region": self.region,
            "api_base_path": self.api_base_path,
            "database_type": self.database_type.value,
            "auth_provider": self.auth_provider.value,
            "enable_caching": self.enable_caching,
            "enable_encryption": self.enable_encryption,
        }


# Table definitions for DynamoDB
DYNAMODB_TABLES = {
    "accounts": {
        "partition_key": "account_id",
        "sort_key": "timestamp",
        "gsi": [
            {"index_name": "org_id_index", "partition_key": "org_id"},
            {"index_name": "status_index", "partition_key": "status"}
        ]
    },
    "users": {
        "partition_key": "user_id",
        "sort_key": None,
        "gsi": [
            {"index_name": "email_index", "partition_key": "email"}
        ]
    },
    "deployments": {
        "partition_key": "deployment_id",
        "sort_key": "timestamp",
        "gsi": [
            {"index_name": "account_id_index", "partition_key": "account_id"},
            {"index_name": "status_index", "partition_key": "status"}
        ]
    },
    "policies": {
        "partition_key": "policy_id",
        "sort_key": "version",
        "gsi": [
            {"index_name": "type_index", "partition_key": "policy_type"}
        ]
    },
    "audit_logs": {
        "partition_key": "log_id",
        "sort_key": "timestamp",
        "gsi": [
            {"index_name": "user_id_index", "partition_key": "user_id"},
            {"index_name": "resource_index", "partition_key": "resource_type"}
        ]
    },
    "cost_data": {
        "partition_key": "date",
        "sort_key": "account_id",
        "gsi": [
            {"index_name": "service_index", "partition_key": "service_name"}
        ]
    }
}


# Queue definitions for SQS
SQS_QUEUES = {
    "provisioning": {
        "description": "Account provisioning and infrastructure deployment",
        "fifo": False
    },
    "monitoring": {
        "description": "Monitoring and alerting events",
        "fifo": False
    },
    "cost_analysis": {
        "description": "Cost analysis and optimization tasks",
        "fifo": False
    },
    "compliance_checks": {
        "description": "Compliance and policy validation",
        "fifo": False
    },
    "dlq": {
        "description": "Dead letter queue for failed messages",
        "fifo": False
    }
}


# Lambda function definitions
LAMBDA_FUNCTIONS = {
    "account_provisioner": {
        "description": "Provisions new AWS accounts",
        "handler": "lambda_handlers.account_provisioner.handler",
        "layers": ["boto3", "requests"]
    },
    "policy_enforcer": {
        "description": "Enforces governance policies",
        "handler": "lambda_handlers.policy_enforcer.handler",
        "layers": ["boto3"]
    },
    "cost_analyzer": {
        "description": "Analyzes and optimizes costs",
        "handler": "lambda_handlers.cost_analyzer.handler",
        "layers": ["boto3", "pandas"]
    },
    "compliance_checker": {
        "description": "Validates compliance rules",
        "handler": "lambda_handlers.compliance_checker.handler",
        "layers": ["boto3"]
    },
    "notification_dispatcher": {
        "description": "Dispatches notifications and alerts",
        "handler": "lambda_handlers.notification_dispatcher.handler",
        "layers": ["boto3", "requests"]
    }
}


# Default configuration instance
default_config = BackendConfig()
