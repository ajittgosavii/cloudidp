"""
CloudIDP Backend Infrastructure - Enhanced FastAPI REST API Gateway
Complete REST API with advanced features: API Keys, Rate Limiting, JWT, OAuth2
"""

from fastapi import FastAPI, HTTPException, Depends, Header, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import logging
import secrets
import hashlib
from collections import defaultdict
from enum import Enum

from backend_integration import CloudIDPBackend
from backend_config import BackendConfig
from backend_models import *

logger = logging.getLogger(__name__)

# ==================== Enhanced Authentication & Rate Limiting ====================

class RateLimitTier(str, Enum):
    """Rate limit tier enumeration"""
    FREE = "free"
    BASIC = "basic"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"


RATE_LIMIT_CONFIG = {
    RateLimitTier.FREE: {"requests_per_minute": 10, "requests_per_hour": 100},
    RateLimitTier.BASIC: {"requests_per_minute": 60, "requests_per_hour": 1000},
    RateLimitTier.PREMIUM: {"requests_per_minute": 300, "requests_per_hour": 10000},
    RateLimitTier.ENTERPRISE: {"requests_per_minute": 1000, "requests_per_hour": 50000}
}


class APIKeyManager:
    """Enhanced API Key management with tiers and usage tracking"""
    
    def __init__(self):
        self.keys: Dict[str, Dict[str, Any]] = {}
    
    def generate_api_key(self, user_id: str, tier: RateLimitTier = RateLimitTier.BASIC) -> str:
        """Generate a new API key"""
        api_key = f"cidp_{secrets.token_urlsafe(32)}"
        
        self.keys[api_key] = {
            "api_key": api_key,
            "user_id": user_id,
            "tier": tier,
            "created_at": datetime.utcnow().isoformat(),
            "last_used": None,
            "is_active": True,
            "usage_count": 0,
            "requests_today": 0,
            "last_reset": datetime.utcnow().date().isoformat()
        }
        
        logger.info(f"API key generated for user {user_id} with {tier} tier")
        return api_key
    
    def validate_api_key(self, api_key: str) -> Optional[Dict[str, Any]]:
        """Validate API key and update usage"""
        key_data = self.keys.get(api_key)
        
        if not key_data or not key_data['is_active']:
            return None
        
        # Update usage
        key_data['last_used'] = datetime.utcnow().isoformat()
        key_data['usage_count'] += 1
        
        # Reset daily counter if needed
        today = datetime.utcnow().date().isoformat()
        if key_data['last_reset'] != today:
            key_data['requests_today'] = 0
            key_data['last_reset'] = today
        
        key_data['requests_today'] += 1
        
        return key_data
    
    def revoke_api_key(self, api_key: str) -> bool:
        """Revoke an API key"""
        if api_key in self.keys:
            self.keys[api_key]['is_active'] = False
            logger.info(f"API key revoked")
            return True
        return False
    
    def list_user_keys(self, user_id: str) -> List[Dict[str, Any]]:
        """List all API keys for a user (with masked keys)"""
        return [
            {
                **{k: v for k, v in data.items() if k != 'api_key'},
                'api_key_preview': f"{key[:15]}...{key[-4:]}"
            }
            for key, data in self.keys.items()
            if data['user_id'] == user_id
        ]
    
    def get_tier(self, api_key: str) -> RateLimitTier:
        """Get rate limit tier for API key"""
        key_data = self.keys.get(api_key)
        return key_data['tier'] if key_data else RateLimitTier.FREE


class RateLimiter:
    """Advanced rate limiting with per-user and per-tier limits"""
    
    def __init__(self):
        self.request_history: Dict[str, List[str]] = defaultdict(list)
        self.blocked_until: Dict[str, datetime] = {}
    
    def check_rate_limit(self, identifier: str, tier: RateLimitTier) -> Dict[str, Any]:
        """Check if request is within rate limits"""
        now = datetime.utcnow()
        
        # Check if temporarily blocked
        if identifier in self.blocked_until:
            if now < self.blocked_until[identifier]:
                return {
                    "allowed": False,
                    "reason": "temporarily_blocked",
                    "blocked_until": self.blocked_until[identifier].isoformat()
                }
            else:
                del self.blocked_until[identifier]
        
        limits = RATE_LIMIT_CONFIG[tier]
        
        # Clean old requests (older than 1 hour)
        self.request_history[identifier] = [
            req_time for req_time in self.request_history[identifier]
            if now - datetime.fromisoformat(req_time) < timedelta(hours=1)
        ]
        
        # Count recent requests
        recent_requests = self.request_history[identifier]
        minute_ago = now - timedelta(minutes=1)
        hour_ago = now - timedelta(hours=1)
        
        requests_per_minute = sum(
            1 for req_time in recent_requests
            if datetime.fromisoformat(req_time) > minute_ago
        )
        
        requests_per_hour = sum(
            1 for req_time in recent_requests
            if datetime.fromisoformat(req_time) > hour_ago
        )
        
        # Check limits
        if requests_per_minute >= limits['requests_per_minute']:
            # Block for 1 minute
            self.blocked_until[identifier] = now + timedelta(minutes=1)
            return {
                "allowed": False,
                "reason": "rate_limit_exceeded",
                "limit_type": "per_minute",
                "current": requests_per_minute,
                "limit": limits['requests_per_minute'],
                "reset_at": (now + timedelta(minutes=1)).isoformat(),
                "retry_after": 60
            }
        
        if requests_per_hour >= limits['requests_per_hour']:
            # Block for 1 hour
            self.blocked_until[identifier] = now + timedelta(hours=1)
            return {
                "allowed": False,
                "reason": "rate_limit_exceeded",
                "limit_type": "per_hour",
                "current": requests_per_hour,
                "limit": limits['requests_per_hour'],
                "reset_at": (now + timedelta(hours=1)).isoformat(),
                "retry_after": 3600
            }
        
        # Record this request
        self.request_history[identifier].append(now.isoformat())
        
        return {
            "allowed": True,
            "requests_per_minute": requests_per_minute + 1,
            "limit_per_minute": limits['requests_per_minute'],
            "requests_per_hour": requests_per_hour + 1,
            "limit_per_hour": limits['requests_per_hour'],
            "remaining_minute": limits['requests_per_minute'] - requests_per_minute - 1,
            "remaining_hour": limits['requests_per_hour'] - requests_per_hour - 1
        }


# ==================== FastAPI Application Setup ====================

app = FastAPI(
    title="CloudIDP Backend API",
    description="Enterprise REST API for CloudIDP Infrastructure Development Platform with Advanced Security",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Global instances
backend: Optional[CloudIDPBackend] = None
config: Optional[BackendConfig] = None
api_key_manager = APIKeyManager()
rate_limiter = RateLimiter()
security = HTTPBearer()


# ==================== Middleware ====================

@app.middleware("http")
async def add_rate_limit_headers(request: Request, call_next):
    """Add rate limit information to response headers"""
    response = await call_next(request)
    
    # Add rate limit headers if available
    if hasattr(request.state, "rate_limit_info"):
        info = request.state.rate_limit_info
        if info.get("allowed"):
            response.headers["X-RateLimit-Limit-Minute"] = str(info['limit_per_minute'])
            response.headers["X-RateLimit-Remaining-Minute"] = str(info['remaining_minute'])
            response.headers["X-RateLimit-Limit-Hour"] = str(info['limit_per_hour'])
            response.headers["X-RateLimit-Remaining-Hour"] = str(info['remaining_hour'])
    
    return response


@app.on_event("startup")
async def startup_event():
    """Initialize backend and middleware on startup"""
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
    
    logger.info("CloudIDP Enhanced API Gateway started successfully")


# ==================== Authentication Dependencies ====================

def get_backend() -> CloudIDPBackend:
    """Get backend instance"""
    if backend is None:
        raise HTTPException(status_code=503, detail="Backend not initialized")
    return backend


async def authenticate_request(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    x_api_key: Optional[str] = Header(None)
) -> tuple[User, Dict[str, Any]]:
    """
    Authenticate request using either JWT token or API key
    Also performs rate limiting
    """
    backend = get_backend()
    identifier = None
    tier = RateLimitTier.FREE
    
    # Try API Key authentication first
    if x_api_key:
        key_data = api_key_manager.validate_api_key(x_api_key)
        if not key_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key"
            )
        
        identifier = key_data['user_id']
        tier = key_data['tier']
        
        # Get user from backend
        user = backend.database.get_user(key_data['user_id'])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
    
    # Try JWT authentication
    elif credentials:
        token = credentials.credentials
        user = backend.validate_token(token)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        
        identifier = user.user_id
        # JWT users get BASIC tier by default (can be upgraded)
        tier = RateLimitTier.BASIC
    
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Provide either Bearer token or X-API-Key header",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Rate limiting
    rate_limit_result = rate_limiter.check_rate_limit(identifier, tier)
    request.state.rate_limit_info = rate_limit_result
    
    if not rate_limit_result['allowed']:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded: {rate_limit_result['reason']}",
            headers={
                "Retry-After": str(rate_limit_result.get('retry_after', 60)),
                "X-RateLimit-Reset": rate_limit_result.get('reset_at', '')
            }
        )
    
    return user, rate_limit_result


# ==================== API Key Management Endpoints ====================

@app.post("/api/v1/api-keys/generate", status_code=status.HTTP_201_CREATED)
async def generate_api_key(
    tier: RateLimitTier = RateLimitTier.BASIC,
    auth_data: tuple = Depends(authenticate_request)
):
    """Generate a new API key for the authenticated user"""
    user, _ = auth_data
    
    api_key = api_key_manager.generate_api_key(user.user_id, tier)
    
    return {
        "success": True,
        "api_key": api_key,
        "tier": tier,
        "limits": RATE_LIMIT_CONFIG[tier],
        "message": "Store this API key securely. It will not be shown again."
    }


@app.get("/api/v1/api-keys/list")
async def list_api_keys(auth_data: tuple = Depends(authenticate_request)):
    """List all API keys for the authenticated user"""
    user, _ = auth_data
    
    keys = api_key_manager.list_user_keys(user.user_id)
    return {"success": True, "api_keys": keys}


@app.delete("/api/v1/api-keys/{api_key}")
async def revoke_api_key(
    api_key: str,
    auth_data: tuple = Depends(authenticate_request)
):
    """Revoke an API key"""
    user, _ = auth_data
    
    # Verify the key belongs to the user
    key_data = api_key_manager.keys.get(api_key)
    if not key_data or key_data['user_id'] != user.user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="API key not found")
    
    success = api_key_manager.revoke_api_key(api_key)
    return {"success": success, "message": "API key revoked"}


# ==================== Health & Status ====================

@app.get("/api/v1/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint (no authentication required)"""
    backend = get_backend()
    return backend.health_check()


@app.get("/api/v1/status")
async def get_status(auth_data: tuple = Depends(authenticate_request)):
    """Get detailed backend status"""
    user, rate_info = auth_data
    backend = get_backend()
    
    status_data = backend.get_backend_status()
    status_data['rate_limit'] = {
        'tier': rate_info.get('tier', 'basic'),
        'remaining_minute': rate_info.get('remaining_minute', 0),
        'remaining_hour': rate_info.get('remaining_hour', 0)
    }
    
    return status_data


# ==================== Authentication Endpoints ====================

@app.post("/api/v1/auth/login", response_model=UserToken)
async def login(credentials: UserLogin):
    """Authenticate user and get JWT token (no rate limiting on login)"""
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
async def get_current_user_info(auth_data: tuple = Depends(authenticate_request)):
    """Get current user information"""
    user, _ = auth_data
    return user


# ==================== Account Management ====================

@app.post("/api/v1/accounts", response_model=Account, status_code=status.HTTP_201_CREATED)
async def create_account(
    request: AccountRequest,
    auth_data: tuple = Depends(authenticate_request)
):
    """Create new AWS account"""
    user, _ = auth_data
    backend = get_backend()
    
    try:
        account = backend.create_account(request, user)
        return account
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@app.get("/api/v1/accounts", response_model=List[Account])
async def list_accounts(
    environment: Optional[str] = None,
    status_filter: Optional[AccountStatus] = None,
    auth_data: tuple = Depends(authenticate_request)
):
    """List accounts"""
    user, _ = auth_data
    backend = get_backend()
    
    filters = {}
    if environment:
        filters["environment"] = environment
    if status_filter:
        filters["status"] = status_filter.value
    
    return backend.list_accounts(user, filters)


@app.get("/api/v1/accounts/{account_id}", response_model=Account)
async def get_account(
    account_id: str,
    auth_data: tuple = Depends(authenticate_request)
):
    """Get account by ID"""
    user, _ = auth_data
    backend = get_backend()
    account = backend.get_account(account_id, user)
    
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    
    return account


@app.patch("/api/v1/accounts/{account_id}/status")
async def update_account_status(
    account_id: str,
    new_status: AccountStatus,
    auth_data: tuple = Depends(authenticate_request)
):
    """Update account status"""
    user, _ = auth_data
    backend = get_backend()
    
    try:
        account = backend.update_account_status(account_id, new_status, user)
        if not account:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
        return account
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


# ==================== Deployment Operations ====================

@app.post("/api/v1/deployments", response_model=Deployment, status_code=status.HTTP_201_CREATED)
async def create_deployment(
    request: DeploymentRequest,
    auth_data: tuple = Depends(authenticate_request)
):
    """Create new deployment"""
    user, _ = auth_data
    backend = get_backend()
    
    try:
        return backend.create_deployment(request, user)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@app.get("/api/v1/deployments", response_model=List[Deployment])
async def list_deployments(
    account_id: Optional[str] = None,
    auth_data: tuple = Depends(authenticate_request)
):
    """List deployments"""
    user, _ = auth_data
    backend = get_backend()
    return backend.list_deployments(user, account_id)


@app.get("/api/v1/deployments/{deployment_id}", response_model=Deployment)
async def get_deployment(
    deployment_id: str,
    auth_data: tuple = Depends(authenticate_request)
):
    """Get deployment by ID"""
    user, _ = auth_data
    backend = get_backend()
    deployment = backend.get_deployment(deployment_id, user)
    
    if not deployment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deployment not found")
    
    return deployment


# ==================== Policy Management ====================

@app.post("/api/v1/policies", response_model=Policy, status_code=status.HTTP_201_CREATED)
async def create_policy(
    request: PolicyRequest,
    auth_data: tuple = Depends(authenticate_request)
):
    """Create new policy"""
    user, _ = auth_data
    backend = get_backend()
    
    try:
        return backend.create_policy(request, user)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@app.get("/api/v1/policies", response_model=List[Policy])
async def list_policies(
    policy_type: Optional[PolicyType] = None,
    auth_data: tuple = Depends(authenticate_request)
):
    """List policies"""
    user, _ = auth_data
    backend = get_backend()
    return backend.list_policies(user, policy_type)


@app.get("/api/v1/policies/{policy_id}", response_model=Policy)
async def get_policy(
    policy_id: str,
    auth_data: tuple = Depends(authenticate_request)
):
    """Get policy by ID"""
    user, _ = auth_data
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
    account_ids: Optional[str] = None,
    auth_data: tuple = Depends(authenticate_request)
):
    """Get cost summary for date range"""
    user, _ = auth_data
    backend = get_backend()
    
    try:
        account_id_list = account_ids.split(",") if account_ids else None
        return backend.get_cost_summary(start_date, end_date, user, account_id_list)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


# ==================== Compliance ====================

@app.post("/api/v1/compliance/check/{account_id}", response_model=List[ComplianceCheck])
async def run_compliance_check(
    account_id: str,
    rules: Optional[List[str]] = None,
    auth_data: tuple = Depends(authenticate_request)
):
    """Run compliance checks on account"""
    user, _ = auth_data
    backend = get_backend()
    
    try:
        return backend.run_compliance_check(account_id, user, rules)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


# ==================== User Management ====================

@app.get("/api/v1/users", response_model=List[User])
async def list_users(auth_data: tuple = Depends(authenticate_request)):
    """List all users"""
    user, _ = auth_data
    backend = get_backend()
    return backend.list_users(user)


# ==================== Audit Logs ====================

@app.get("/api/v1/audit-logs", response_model=List[AuditLog])
async def get_audit_logs(
    user_id: Optional[str] = None,
    resource_type: Optional[str] = None,
    auth_data: tuple = Depends(authenticate_request)
):
    """Get audit logs"""
    user, _ = auth_data
    backend = get_backend()
    return backend.get_audit_logs(user, user_id, resource_type)


# ==================== Admin Endpoints ====================

@app.get("/api/v1/admin/rate-limits")
async def get_rate_limit_stats(auth_data: tuple = Depends(authenticate_request)):
    """Get rate limit statistics (admin only)"""
    user, _ = auth_data
    
    if user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    
    stats = {
        "total_identifiers": len(rate_limiter.request_history),
        "blocked_identifiers": len(rate_limiter.blocked_until),
        "rate_limit_tiers": {tier.value: limits for tier, limits in RATE_LIMIT_CONFIG.items()}
    }
    
    return {"success": True, "stats": stats}


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
        },
        headers=exc.headers
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
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
    
    config = BackendConfig.from_environment()
    
    uvicorn.run(
        "api_gateway_enhanced:app",
        host=config.api_host,
        port=config.api_port,
        reload=True,
        log_level=config.log_level.lower()
    )
