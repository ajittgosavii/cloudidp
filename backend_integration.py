"""
CloudIDP Backend Infrastructure - Main Integration Module
Orchestrates all backend services: Database, Auth, Queue, Lambda
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

from backend_config import BackendConfig
from backend_models import *
from database_service import DatabaseService
from auth_service import AuthenticationService
from queue_service import QueueService
from lambda_orchestrator import LambdaOrchestrator

# Import AWS integrations if available
try:
    from aws_integrations_manager import AWSIntegrationsManager
    AWS_AVAILABLE = True
except ImportError:
    AWS_AVAILABLE = False

logger = logging.getLogger(__name__)


class CloudIDPBackend:
    """
    Main backend orchestration class for CloudIDP platform
    Provides unified interface to all backend services
    """
    
    def __init__(self, config: Optional[BackendConfig] = None, demo_mode: bool = True):
        """
        Initialize CloudIDP Backend
        
        Args:
            config: Backend configuration (uses default if not provided)
            demo_mode: Enable demo mode for testing without AWS infrastructure
        """
        self.config = config or BackendConfig(demo_mode=demo_mode)
        self.demo_mode = self.config.demo_mode
        
        logger.info(f"Initializing CloudIDP Backend (demo_mode={self.demo_mode})")
        
        # Initialize core services
        self.database = DatabaseService(self.config)
        self.auth = AuthenticationService(self.config, self.database)
        self.queue = QueueService(self.config)
        self.lambda_orchestrator = LambdaOrchestrator(self.config)
        
        # Initialize AWS integrations if available
        if AWS_AVAILABLE:
            self.aws = AWSIntegrationsManager(
                demo_mode=self.demo_mode,
                region=self.config.region
            )
        else:
            self.aws = None
            logger.warning("AWS integrations not available")
        
        # Register queue message handlers
        self._register_queue_handlers()
        
        logger.info("CloudIDP Backend initialized successfully")
    
    # ==================== Service Health ====================
    
    def health_check(self) -> HealthCheckResponse:
        """Check health of all backend services"""
        services = {
            "database": "healthy",
            "auth": "healthy",
            "queue": "healthy",
            "lambda": "healthy"
        }
        
        if self.aws:
            services["aws_integrations"] = "healthy"
        else:
            services["aws_integrations"] = "unavailable"
        
        if self.demo_mode:
            services["mode"] = "demo"
        else:
            services["mode"] = "live"
        
        return HealthCheckResponse(
            status="healthy",
            services=services,
            version="1.0.0"
        )
    
    def get_backend_status(self) -> Dict[str, Any]:
        """Get detailed backend status"""
        return {
            "demo_mode": self.demo_mode,
            "environment": self.config.environment.value,
            "region": self.config.region,
            "database_type": self.config.database_type.value,
            "auth_provider": self.config.auth_provider.value,
            "services": {
                "database": "operational",
                "authentication": "operational",
                "queue": "operational",
                "lambda": "operational",
                "aws_integrations": "operational" if self.aws else "unavailable"
            },
            "queue_status": {
                queue_name: self.queue.get_queue_attributes(queue_name)
                for queue_name in ["provisioning", "monitoring", "cost_analysis", "compliance_checks"]
            },
            "lambda_functions": self.lambda_orchestrator.list_functions()
        }
    
    # ==================== Account Operations ====================
    
    def create_account(self, request: AccountRequest, user: User) -> Account:
        """
        Create a new AWS account
        
        Args:
            request: Account creation request
            user: User creating the account
            
        Returns:
            Created Account
        """
        # Create account in database
        account = Account(
            account_id=f"pending-{uuid.uuid4().hex[:12]}",  # Temporary ID
            **request.dict(),
            status=AccountStatus.PENDING,
            created_by=user.user_id
        )
        account = self.database.create_account(account)
        
        # Queue provisioning request
        provisioning_msg = ProvisioningMessage(
            account_request=request,
            requester_id=user.user_id
        )
        self.queue.send_provisioning_request(provisioning_msg)
        
        # Invoke Lambda provisioner (async)
        if not self.demo_mode and self.config.enable_organizations_integration:
            self.lambda_orchestrator.invoke_async("account_provisioner", {
                "account_id": account.account_id,
                "request": request.dict()
            })
        
        # Create audit log
        self._create_audit_log(
            user_id=user.user_id,
            action="create_account",
            resource_type="account",
            resource_id=account.account_id,
            action_details=request.dict()
        )
        
        return account
    
    def get_account(self, account_id: str, user: User) -> Optional[Account]:
        """Get account by ID"""
        # Check permissions
        if not self.auth.check_account_access(user, account_id):
            logger.warning(f"User {user.user_id} denied access to account {account_id}")
            return None
        
        return self.database.get_account(account_id)
    
    def list_accounts(self, user: User, filters: Optional[Dict] = None) -> List[Account]:
        """List accounts accessible to user"""
        accounts = self.database.list_accounts(filters)
        
        # Filter based on user permissions
        if user.role != UserRole.ADMIN:
            accounts = [
                acc for acc in accounts
                if self.auth.check_account_access(user, acc.account_id)
            ]
        
        return accounts
    
    def update_account_status(self, account_id: str, status: AccountStatus, 
                            user: User) -> Optional[Account]:
        """Update account status"""
        if not self.auth.check_permission(user, "account:update"):
            logger.warning(f"User {user.user_id} denied permission to update account")
            return None
        
        account = self.database.update_account_status(account_id, status)
        
        if account:
            self._create_audit_log(
                user_id=user.user_id,
                action="update_account_status",
                resource_type="account",
                resource_id=account_id,
                action_details={"status": status.value}
            )
        
        return account
    
    # ==================== Deployment Operations ====================
    
    def create_deployment(self, request: DeploymentRequest, user: User) -> Deployment:
        """Create a new deployment"""
        # Check permissions
        if not self.auth.check_permission(user, "deployment:create"):
            raise PermissionError("User does not have deployment:create permission")
        
        # Create deployment in database
        deployment = Deployment(
            **request.dict(),
            status=DeploymentStatus.QUEUED,
            created_by=user.user_id
        )
        deployment = self.database.create_deployment(deployment)
        
        # Queue deployment request
        deployment_msg = DeploymentMessage(
            deployment_request=request,
            requester_id=user.user_id
        )
        self.queue.send_deployment_request(deployment_msg)
        
        # Create audit log
        self._create_audit_log(
            user_id=user.user_id,
            action="create_deployment",
            resource_type="deployment",
            resource_id=deployment.deployment_id,
            action_details=request.dict()
        )
        
        return deployment
    
    def get_deployment(self, deployment_id: str, user: User) -> Optional[Deployment]:
        """Get deployment by ID"""
        deployment = self.database.get_deployment(deployment_id)
        
        if deployment and not self.auth.check_account_access(user, deployment.account_id):
            logger.warning(f"User {user.user_id} denied access to deployment")
            return None
        
        return deployment
    
    def list_deployments(self, user: User, account_id: Optional[str] = None) -> List[Deployment]:
        """List deployments"""
        deployments = self.database.list_deployments(account_id)
        
        # Filter based on user permissions
        if user.role != UserRole.ADMIN:
            deployments = [
                dep for dep in deployments
                if self.auth.check_account_access(user, dep.account_id)
            ]
        
        return deployments
    
    # ==================== Policy Operations ====================
    
    def create_policy(self, request: PolicyRequest, user: User) -> Policy:
        """Create a new policy"""
        if not self.auth.check_permission(user, "policy:create"):
            raise PermissionError("User does not have policy:create permission")
        
        policy = Policy(
            **request.dict(),
            created_by=user.user_id
        )
        policy = self.database.create_policy(policy)
        
        # Enforce policy via Lambda
        self.lambda_orchestrator.invoke_async("policy_enforcer", {
            "policy_id": policy.policy_id,
            "target_accounts": policy.target_accounts,
            "target_ous": policy.target_ous
        })
        
        self._create_audit_log(
            user_id=user.user_id,
            action="create_policy",
            resource_type="policy",
            resource_id=policy.policy_id,
            action_details=request.dict()
        )
        
        return policy
    
    def get_policy(self, policy_id: str, user: User) -> Optional[Policy]:
        """Get policy by ID"""
        if not self.auth.check_permission(user, "policy:read"):
            return None
        
        return self.database.get_policy(policy_id)
    
    def list_policies(self, user: User, policy_type: Optional[PolicyType] = None) -> List[Policy]:
        """List policies"""
        if not self.auth.check_permission(user, "policy:read"):
            return []
        
        return self.database.list_policies(policy_type)
    
    # ==================== Cost Operations ====================
    
    def get_cost_summary(self, start_date: str, end_date: str, 
                        user: User, account_ids: Optional[List[str]] = None) -> CostSummary:
        """Get cost summary for date range"""
        if not self.auth.check_permission(user, "cost:read"):
            raise PermissionError("User does not have cost:read permission")
        
        # Get cost data from database
        cost_data = []
        for account_id in (account_ids or [acc.account_id for acc in self.list_accounts(user)]):
            cost_data.extend(self.database.get_cost_data(start_date, account_id))
        
        # Calculate summary
        total_cost = sum(cost.unblended_cost for cost in cost_data)
        
        cost_by_service = {}
        for cost in cost_data:
            cost_by_service[cost.service_name] = cost_by_service.get(cost.service_name, 0) + cost.unblended_cost
        
        cost_by_account = {}
        for cost in cost_data:
            cost_by_account[cost.account_id] = cost_by_account.get(cost.account_id, 0) + cost.unblended_cost
        
        cost_by_environment = {}
        for cost in cost_data:
            if cost.environment:
                cost_by_environment[cost.environment] = cost_by_environment.get(cost.environment, 0) + cost.unblended_cost
        
        # Get savings opportunities from Lambda
        savings_result = self.lambda_orchestrator.analyze_costs(
            date_range={"start": start_date, "end": end_date},
            account_ids=account_ids
        )
        savings_opportunities = savings_result.get("Payload", {}).get("savings_opportunities", [])
        
        return CostSummary(
            total_cost=total_cost,
            cost_by_service=cost_by_service,
            cost_by_account=cost_by_account,
            cost_by_environment=cost_by_environment,
            forecast_next_month=total_cost * 1.05,  # Simple forecast
            savings_opportunities=savings_opportunities
        )
    
    # ==================== Compliance Operations ====================
    
    def run_compliance_check(self, account_id: str, user: User, 
                           rules: Optional[List[str]] = None) -> List[ComplianceCheck]:
        """Run compliance checks on an account"""
        if not self.auth.check_permission(user, "audit:read"):
            raise PermissionError("User does not have audit:read permission")
        
        # Queue compliance check
        self.queue.send_compliance_check({
            "account_id": account_id,
            "rules": rules or [],
            "requester_id": user.user_id
        })
        
        # Invoke Lambda compliance checker
        result = self.lambda_orchestrator.check_compliance(account_id, rules)
        
        # Store compliance check results
        checks = []
        for violation in result.get("Payload", {}).get("violations", []):
            check = ComplianceCheck(
                account_id=account_id,
                rule_name=violation.get("rule"),
                rule_id=violation.get("rule"),
                status=ComplianceStatus.NON_COMPLIANT,
                resource_type=violation.get("resource", "").split("-")[0],
                resource_id=violation.get("resource", ""),
                finding_details=violation.get("finding"),
                severity=violation.get("severity", "medium")
            )
            checks.append(check)
        
        return checks
    
    # ==================== User Management ====================
    
    def authenticate_user(self, login: UserLogin) -> Optional[UserToken]:
        """Authenticate user and return token"""
        return self.auth.authenticate(login)
    
    def register_user(self, username: str, email: str, password: str,
                     full_name: str, role: UserRole = UserRole.DEVELOPER) -> Optional[User]:
        """Register a new user"""
        return self.auth.register_user(username, email, password, full_name, role)
    
    def validate_token(self, token: str) -> Optional[User]:
        """Validate JWT token and return user"""
        return self.auth.validate_token(token)
    
    def list_users(self, requesting_user: User) -> List[User]:
        """List all users"""
        if not self.auth.check_permission(requesting_user, "user:read"):
            return []
        
        return self.database.list_users()
    
    # ==================== Audit Operations ====================
    
    def _create_audit_log(self, user_id: str, action: str, resource_type: str,
                         resource_id: str, action_details: Dict[str, Any],
                         result: str = "success") -> AuditLog:
        """Create audit log entry"""
        log = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            action_details=action_details,
            result=result
        )
        return self.database.create_audit_log(log)
    
    def get_audit_logs(self, user: User, user_id: Optional[str] = None,
                      resource_type: Optional[str] = None) -> List[AuditLog]:
        """Get audit logs"""
        if not self.auth.check_permission(user, "audit:read"):
            return []
        
        return self.database.list_audit_logs(user_id, resource_type)
    
    # ==================== Queue Message Handlers ====================
    
    def _register_queue_handlers(self):
        """Register handlers for queue messages"""
        self.queue.register_handler("provisioning_request", self._handle_provisioning_request)
        self.queue.register_handler("deployment_request", self._handle_deployment_request)
        self.queue.register_handler("monitoring_alert", self._handle_monitoring_alert)
        self.queue.register_handler("cost_analysis", self._handle_cost_analysis)
        self.queue.register_handler("compliance_check", self._handle_compliance_check)
    
    def _handle_provisioning_request(self, message: Dict[str, Any]) -> bool:
        """Handle account provisioning request"""
        try:
            payload = message.get("payload", {})
            account_request = AccountRequest(**payload.get("account_request", {}))
            
            # Invoke Lambda provisioner
            result = self.lambda_orchestrator.provision_account(account_request)
            
            if result.get("StatusCode") == 200:
                logger.info(f"Account provisioned: {result}")
                return True
            
            return False
        except Exception as e:
            logger.error(f"Error handling provisioning request: {e}")
            return False
    
    def _handle_deployment_request(self, message: Dict[str, Any]) -> bool:
        """Handle deployment request"""
        try:
            payload = message.get("payload", {})
            deployment_request = DeploymentRequest(**payload.get("deployment_request", {}))
            
            logger.info(f"Processing deployment: {deployment_request.deployment_name}")
            # TODO: Implement actual deployment logic
            
            return True
        except Exception as e:
            logger.error(f"Error handling deployment request: {e}")
            return False
    
    def _handle_monitoring_alert(self, message: Dict[str, Any]) -> bool:
        """Handle monitoring alert"""
        try:
            payload = message.get("payload", {})
            logger.info(f"Monitoring alert: {payload}")
            
            # Dispatch notification
            self.lambda_orchestrator.send_notification(
                notification_type="alert",
                recipients=["admin@company.com"],
                message=payload.get("message", ""),
                data=payload
            )
            
            return True
        except Exception as e:
            logger.error(f"Error handling monitoring alert: {e}")
            return False
    
    def _handle_cost_analysis(self, message: Dict[str, Any]) -> bool:
        """Handle cost analysis task"""
        try:
            payload = message.get("payload", {})
            logger.info(f"Cost analysis task: {payload}")
            # TODO: Implement cost analysis logic
            return True
        except Exception as e:
            logger.error(f"Error handling cost analysis: {e}")
            return False
    
    def _handle_compliance_check(self, message: Dict[str, Any]) -> bool:
        """Handle compliance check task"""
        try:
            payload = message.get("payload", {})
            account_id = payload.get("account_id")
            rules = payload.get("rules", [])
            
            result = self.lambda_orchestrator.check_compliance(account_id, rules)
            logger.info(f"Compliance check result: {result}")
            
            return True
        except Exception as e:
            logger.error(f"Error handling compliance check: {e}")
            return False
    
    # ==================== Configuration ====================
    
    def get_configuration(self) -> Dict[str, Any]:
        """Get backend configuration"""
        return self.config.to_dict()
    
    def update_demo_mode(self, demo_mode: bool):
        """Update demo mode setting"""
        self.demo_mode = demo_mode
        self.config.demo_mode = demo_mode
        logger.info(f"Demo mode updated to: {demo_mode}")
