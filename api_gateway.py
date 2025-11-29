"""
CloudIDP Backend Infrastructure - FastAPI REST API Gateway
Provides REST API endpoints for all backend services
"""

from fastapi import FastAPI, HTTPException, Depends, Header, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional, List
from datetime import datetime
import logging

from backend_integration import CloudIDPBackend
from backend_config import BackendConfig
from backend_models import *

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="CloudIDP Backend API",
    description="REST API for CloudIDP Infrastructure Development Platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Initialize backend
backend = None
config = None


def get_backend() -> CloudIDPBackend:
    """Get backend instance"""
    global backend
    if backend is None:
        raise HTTPException(status_code=503, detail="Backend not initialized")
    return backend


async def get_current_user(authorization: Optional[str] = Header(None)) -> User:
    """Get current user from JWT token"""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header required",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    try:
        # Extract token from "Bearer <token>"
        token = authorization.replace("Bearer ", "")
        backend = get_backend()
        user = backend.validate_token(token)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        
        return user
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )


# Configure CORS
@app.on_event("startup")
async def startup_event():
    """Initialize backend on startup"""
    global backend, config
    
    config = BackendConfig.from_environment()
    backend = CloudIDPBackend(config)
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    logger.info("CloudIDP API Gateway started successfully")


# ==================== Health & Status ====================

@app.get("/api/v1/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint"""
    backend = get_backend()
    return backend.health_check()


@app.get("/api/v1/status")
async def get_status(user: User = Depends(get_current_user)):
    """Get detailed backend status"""
    backend = get_backend()
    return backend.get_backend_status()


# ==================== Authentication ====================

@app.post("/api/v1/auth/login", response_model=UserToken)
async def login(credentials: UserLogin):
    """Authenticate user and get JWT token"""
    backend = get_backend()
    token = backend.authenticate_user(credentials)
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    return token


@app.post("/api/v1/auth/register", response_model=User)
async def register(
    username: str,
    email: str,
    password: str,
    full_name: str,
    role: UserRole = UserRole.DEVELOPER
):
    """Register new user"""
    backend = get_backend()
    user = backend.register_user(username, email, password, full_name, role)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User registration failed"
        )
    
    return user


@app.get("/api/v1/auth/me", response_model=User)
async def get_current_user_info(user: User = Depends(get_current_user)):
    """Get current user information"""
    return user


@app.post("/api/v1/auth/reset-password")
async def reset_password(email: str):
    """Request password reset"""
    backend = get_backend()
    success = backend.auth.reset_password_request(email)
    
    return {"success": success, "message": "Password reset email sent"}


# ==================== Account Management ====================

@app.post("/api/v1/accounts", response_model=Account, status_code=status.HTTP_201_CREATED)
async def create_account(
    request: AccountRequest,
    user: User = Depends(get_current_user)
):
    """Create new AWS account"""
    backend = get_backend()
    
    try:
        account = backend.create_account(request, user)
        return account
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating account: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/api/v1/accounts", response_model=List[Account])
async def list_accounts(
    environment: Optional[str] = None,
    status: Optional[AccountStatus] = None,
    user: User = Depends(get_current_user)
):
    """List accounts"""
    backend = get_backend()
    
    filters = {}
    if environment:
        filters["environment"] = environment
    if status:
        filters["status"] = status.value
    
    accounts = backend.list_accounts(user, filters)
    return accounts


@app.get("/api/v1/accounts/{account_id}", response_model=Account)
async def get_account(
    account_id: str,
    user: User = Depends(get_current_user)
):
    """Get account by ID"""
    backend = get_backend()
    account = backend.get_account(account_id, user)
    
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    
    return account


@app.patch("/api/v1/accounts/{account_id}/status")
async def update_account_status(
    account_id: str,
    new_status: AccountStatus,
    user: User = Depends(get_current_user)
):
    """Update account status"""
    backend = get_backend()
    
    try:
        account = backend.update_account_status(account_id, new_status, user)
        if not account:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
        return account
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


# ==================== Deployments ====================

@app.post("/api/v1/deployments", response_model=Deployment, status_code=status.HTTP_201_CREATED)
async def create_deployment(
    request: DeploymentRequest,
    user: User = Depends(get_current_user)
):
    """Create new deployment"""
    backend = get_backend()
    
    try:
        deployment = backend.create_deployment(request, user)
        return deployment
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating deployment: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/api/v1/deployments", response_model=List[Deployment])
async def list_deployments(
    account_id: Optional[str] = None,
    user: User = Depends(get_current_user)
):
    """List deployments"""
    backend = get_backend()
    deployments = backend.list_deployments(user, account_id)
    return deployments


@app.get("/api/v1/deployments/{deployment_id}", response_model=Deployment)
async def get_deployment(
    deployment_id: str,
    user: User = Depends(get_current_user)
):
    """Get deployment by ID"""
    backend = get_backend()
    deployment = backend.get_deployment(deployment_id, user)
    
    if not deployment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deployment not found")
    
    return deployment


# ==================== Policies ====================

@app.post("/api/v1/policies", response_model=Policy, status_code=status.HTTP_201_CREATED)
async def create_policy(
    request: PolicyRequest,
    user: User = Depends(get_current_user)
):
    """Create new policy"""
    backend = get_backend()
    
    try:
        policy = backend.create_policy(request, user)
        return policy
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating policy: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/api/v1/policies", response_model=List[Policy])
async def list_policies(
    policy_type: Optional[PolicyType] = None,
    user: User = Depends(get_current_user)
):
    """List policies"""
    backend = get_backend()
    policies = backend.list_policies(user, policy_type)
    return policies


@app.get("/api/v1/policies/{policy_id}", response_model=Policy)
async def get_policy(
    policy_id: str,
    user: User = Depends(get_current_user)
):
    """Get policy by ID"""
    backend = get_backend()
    policy = backend.get_policy(policy_id, user)
    
    if not policy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found")
    
    return policy


# ==================== Cost Management ====================

@app.get("/api/v1/costs/summary", response_model=CostSummary)
async def get_cost_summary(
    start_date: str,
    end_date: str,
    account_ids: Optional[str] = None,  # Comma-separated list
    user: User = Depends(get_current_user)
):
    """Get cost summary for date range"""
    backend = get_backend()
    
    try:
        account_id_list = account_ids.split(",") if account_ids else None
        summary = backend.get_cost_summary(start_date, end_date, user, account_id_list)
        return summary
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting cost summary: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# ==================== Compliance ====================

@app.post("/api/v1/compliance/check/{account_id}", response_model=List[ComplianceCheck])
async def run_compliance_check(
    account_id: str,
    rules: Optional[List[str]] = None,
    user: User = Depends(get_current_user)
):
    """Run compliance checks on account"""
    backend = get_backend()
    
    try:
        checks = backend.run_compliance_check(account_id, user, rules)
        return checks
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        logger.error(f"Error running compliance check: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# ==================== Users ====================

@app.get("/api/v1/users", response_model=List[User])
async def list_users(user: User = Depends(get_current_user)):
    """List all users"""
    backend = get_backend()
    users = backend.list_users(user)
    return users


# ==================== Audit Logs ====================

@app.get("/api/v1/audit-logs", response_model=List[AuditLog])
async def get_audit_logs(
    user_id: Optional[str] = None,
    resource_type: Optional[str] = None,
    user: User = Depends(get_current_user)
):
    """Get audit logs"""
    backend = get_backend()
    logs = backend.get_audit_logs(user, user_id, resource_type)
    return logs


# ==================== Queue Management ====================

@app.get("/api/v1/queues/{queue_name}/status")
async def get_queue_status(
    queue_name: str,
    user: User = Depends(get_current_user)
):
    """Get queue status"""
    if user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    
    backend = get_backend()
    attributes = backend.queue.get_queue_attributes(queue_name)
    return attributes


@app.post("/api/v1/queues/{queue_name}/purge")
async def purge_queue(
    queue_name: str,
    user: User = Depends(get_current_user)
):
    """Purge queue (admin only)"""
    if user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    
    backend = get_backend()
    success = backend.queue.purge_queue(queue_name)
    return {"success": success, "message": f"Queue {queue_name} purged"}


# ==================== Lambda Functions ====================

@app.get("/api/v1/lambda/functions")
async def list_lambda_functions(user: User = Depends(get_current_user)):
    """List Lambda functions"""
    if user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    
    backend = get_backend()
    functions = backend.lambda_orchestrator.list_functions()
    return functions


@app.post("/api/v1/lambda/invoke/{function_name}")
async def invoke_lambda_function(
    function_name: str,
    payload: Dict[str, Any],
    user: User = Depends(get_current_user)
):
    """Invoke Lambda function"""
    if user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    
    backend = get_backend()
    result = backend.lambda_orchestrator.invoke_function(function_name, payload)
    return result


# ==================== Error Handlers ====================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "timestamp": datetime.utcnow().isoformat()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "Internal server error",
            "timestamp": datetime.utcnow().isoformat()
        }
    )


# ==================== Main ====================

if __name__ == "__main__":
    import uvicorn
    
    # Get configuration
    config = BackendConfig.from_environment()
    
    # Run server
    uvicorn.run(
        "api_gateway:app",
        host=config.api_host,
        port=config.api_port,
        reload=True,
        log_level=config.log_level.lower()
    )
