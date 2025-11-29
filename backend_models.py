"""
CloudIDP Backend Infrastructure - Data Models
Pydantic models for database entities and API contracts
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import uuid


class AccountStatus(str, Enum):
    """AWS Account status"""
    PENDING = "pending"
    CREATING = "creating"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    CLOSED = "closed"
    FAILED = "failed"


class DeploymentStatus(str, Enum):
    """Deployment status"""
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


class PolicyType(str, Enum):
    """Policy types"""
    SCP = "service_control_policy"
    IAM = "iam_policy"
    RESOURCE = "resource_policy"
    GUARDRAIL = "guardrail_policy"
    TAG = "tag_policy"


class ComplianceStatus(str, Enum):
    """Compliance status"""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    NOT_APPLICABLE = "not_applicable"
    PENDING_REVIEW = "pending_review"


# ==================== Base Models ====================

class BaseEntity(BaseModel):
    """Base model for all entities"""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    tags: Dict[str, str] = Field(default_factory=dict)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


# ==================== Account Models ====================

class Account(BaseEntity):
    """AWS Account entity"""
    account_id: str = Field(..., description="AWS Account ID")
    account_name: str = Field(..., description="Account name")
    account_email: str = Field(..., description="Root email")
    org_id: str = Field(..., description="Organization ID")
    ou_id: Optional[str] = Field(None, description="Organizational Unit ID")
    status: AccountStatus = Field(AccountStatus.PENDING)
    environment: str = Field(..., description="dev, staging, prod")
    cost_center: Optional[str] = None
    owner: str = Field(..., description="Account owner")
    description: Optional[str] = None
    
    # Metadata
    aws_organization_arn: Optional[str] = None
    control_tower_enabled: bool = False
    sso_enabled: bool = False
    
    @validator("account_id")
    def validate_account_id(cls, v):
        if not v.isdigit() or len(v) != 12:
            raise ValueError("Account ID must be 12 digits")
        return v


class AccountRequest(BaseModel):
    """Request to create new account"""
    account_name: str
    account_email: str
    org_id: str
    ou_id: Optional[str] = None
    environment: str
    cost_center: Optional[str] = None
    owner: str
    description: Optional[str] = None
    tags: Dict[str, str] = Field(default_factory=dict)


# ==================== User Models ====================

class UserRole(str, Enum):
    """User roles"""
    ADMIN = "admin"
    ARCHITECT = "architect"
    DEVELOPER = "developer"
    VIEWER = "viewer"
    AUDITOR = "auditor"


class User(BaseEntity):
    """User entity"""
    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str = Field(..., description="Username")
    email: str = Field(..., description="Email address")
    full_name: str = Field(..., description="Full name")
    role: UserRole = Field(UserRole.DEVELOPER)
    is_active: bool = True
    
    # Authentication
    cognito_user_id: Optional[str] = None
    sso_provider: Optional[str] = None
    
    # Permissions
    permissions: List[str] = Field(default_factory=list)
    account_access: List[str] = Field(default_factory=list)
    
    @validator("email")
    def validate_email(cls, v):
        if "@" not in v:
            raise ValueError("Invalid email address")
        return v.lower()


class UserLogin(BaseModel):
    """User login request"""
    username: str
    password: str


class UserToken(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user_id: str
    role: UserRole


# ==================== Deployment Models ====================

class Deployment(BaseEntity):
    """Infrastructure deployment entity"""
    deployment_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    account_id: str = Field(..., description="Target account")
    deployment_name: str = Field(..., description="Deployment name")
    deployment_type: str = Field(..., description="terraform, cloudformation, cdk")
    status: DeploymentStatus = Field(DeploymentStatus.QUEUED)
    
    # Configuration
    template_url: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)
    stack_id: Optional[str] = None
    
    # Execution details
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    
    # Resources
    resources_created: List[str] = Field(default_factory=list)
    outputs: Dict[str, Any] = Field(default_factory=dict)


class DeploymentRequest(BaseModel):
    """Request to create deployment"""
    account_id: str
    deployment_name: str
    deployment_type: str
    template_url: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)
    tags: Dict[str, str] = Field(default_factory=dict)


# ==================== Policy Models ====================

class Policy(BaseEntity):
    """Governance policy entity"""
    policy_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    policy_name: str = Field(..., description="Policy name")
    policy_type: PolicyType = Field(..., description="Policy type")
    version: str = Field("1.0", description="Policy version")
    
    # Policy content
    policy_document: Dict[str, Any] = Field(..., description="Policy JSON")
    description: Optional[str] = None
    
    # Scope
    target_accounts: List[str] = Field(default_factory=list)
    target_ous: List[str] = Field(default_factory=list)
    
    # Status
    is_active: bool = True
    enforcement_level: str = Field("enforce", description="enforce, monitor, audit")


class PolicyRequest(BaseModel):
    """Request to create/update policy"""
    policy_name: str
    policy_type: PolicyType
    policy_document: Dict[str, Any]
    description: Optional[str] = None
    target_accounts: List[str] = Field(default_factory=list)
    target_ous: List[str] = Field(default_factory=list)
    enforcement_level: str = "enforce"


# ==================== Compliance Models ====================

class ComplianceCheck(BaseEntity):
    """Compliance check result"""
    check_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    account_id: str = Field(..., description="Account checked")
    rule_name: str = Field(..., description="Compliance rule")
    rule_id: str = Field(..., description="Rule identifier")
    status: ComplianceStatus = Field(..., description="Check status")
    
    # Details
    resource_type: str = Field(..., description="AWS resource type")
    resource_id: str = Field(..., description="Resource identifier")
    finding_details: Optional[str] = None
    remediation_steps: Optional[List[str]] = None
    
    # Severity
    severity: str = Field("medium", description="critical, high, medium, low")
    risk_score: int = Field(5, ge=0, le=10)


# ==================== Cost Models ====================

class CostData(BaseEntity):
    """Cost tracking entity"""
    cost_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    date: str = Field(..., description="Date YYYY-MM-DD")
    account_id: str = Field(..., description="AWS Account")
    service_name: str = Field(..., description="AWS Service")
    
    # Cost breakdown
    unblended_cost: float = Field(0.0, ge=0)
    blended_cost: float = Field(0.0, ge=0)
    usage_quantity: float = Field(0.0, ge=0)
    usage_unit: str = Field("", description="GB, Hours, Requests")
    
    # Metadata
    region: Optional[str] = None
    cost_center: Optional[str] = None
    environment: Optional[str] = None


class CostSummary(BaseModel):
    """Cost summary response"""
    total_cost: float
    cost_by_service: Dict[str, float]
    cost_by_account: Dict[str, float]
    cost_by_environment: Dict[str, float]
    forecast_next_month: float
    savings_opportunities: List[Dict[str, Any]]


# ==================== Audit Models ====================

class AuditLog(BaseEntity):
    """Audit log entry"""
    log_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_id: str = Field(..., description="User who performed action")
    action: str = Field(..., description="Action performed")
    resource_type: str = Field(..., description="Resource type")
    resource_id: str = Field(..., description="Resource ID")
    
    # Details
    action_details: Dict[str, Any] = Field(default_factory=dict)
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    result: str = Field("success", description="success, failure")
    error_message: Optional[str] = None


# ==================== Queue Message Models ====================

class QueueMessage(BaseModel):
    """SQS message wrapper"""
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    message_type: str = Field(..., description="Message type")
    payload: Dict[str, Any] = Field(..., description="Message payload")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    priority: int = Field(5, ge=1, le=10)
    retry_count: int = 0


class ProvisioningMessage(BaseModel):
    """Account provisioning message"""
    account_request: AccountRequest
    requester_id: str
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))


class DeploymentMessage(BaseModel):
    """Deployment message"""
    deployment_request: DeploymentRequest
    requester_id: str
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))


# ==================== Response Models ====================

class ApiResponse(BaseModel):
    """Standard API response"""
    success: bool
    message: str
    data: Optional[Any] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class PaginatedResponse(BaseModel):
    """Paginated response"""
    items: List[Any]
    total: int
    page: int
    page_size: int
    has_next: bool
    has_previous: bool


class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str = "healthy"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str = "1.0.0"
    services: Dict[str, str] = Field(default_factory=dict)


# ==================== Demo Data Models ====================

class DemoDataConfig(BaseModel):
    """Configuration for demo data generation"""
    num_accounts: int = 10
    num_users: int = 20
    num_deployments: int = 50
    num_policies: int = 15
    date_range_days: int = 90
