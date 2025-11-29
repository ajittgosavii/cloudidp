"""
CloudIDP API Gateway - Streamlit Integration Module
Standalone version of API Key Management and Rate Limiting for Streamlit UI
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import secrets
import logging
from collections import defaultdict
from enum import Enum

logger = logging.getLogger(__name__)

# ==================== Rate Limiting Configuration ====================

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


# ==================== API Key Manager ====================

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


# ==================== Rate Limiter ====================

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
