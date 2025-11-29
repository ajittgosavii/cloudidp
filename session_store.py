"""
Session Store and Caching Layer
Redis/ElastiCache integration for user sessions, cache management, and temporary storage
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import json
import hashlib
import pickle

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RedisSessionStore:
    """Redis-based session store"""
    
    def __init__(self, host: str = 'localhost', port: int = 6379, 
                 db: int = 0, password: Optional[str] = None):
        """
        Initialize Redis session store
        
        Args:
            host: Redis host
            port: Redis port
            db: Redis database number
            password: Redis password (if required)
        """
        self.host = host
        self.port = port
        self.db = db
        
        # In real implementation, use redis-py
        # import redis
        # self.client = redis.Redis(
        #     host=host, port=port, db=db, 
        #     password=password, decode_responses=True
        # )
        
        self.client = None  # Mock for demo
        self._mock_storage = {}  # In-memory storage for demo
        
        logger.info(f"Redis session store initialized (mock mode)")
    
    def create_session(self, user_id: str, session_data: Dict[str, Any],
                      ttl: int = 3600) -> str:
        """
        Create a new user session
        
        Args:
            user_id: User identifier
            session_data: Session data to store
            ttl: Time to live in seconds (default 1 hour)
            
        Returns:
            Session ID
        """
        # Generate session ID
        session_id = hashlib.sha256(
            f"{user_id}:{datetime.utcnow().isoformat()}".encode()
        ).hexdigest()
        
        session = {
            "session_id": session_id,
            "user_id": user_id,
            "data": session_data,
            "created_at": datetime.utcnow().isoformat(),
            "expires_at": (datetime.utcnow() + timedelta(seconds=ttl)).isoformat()
        }
        
        # In real implementation:
        # self.client.setex(
        #     f"session:{session_id}",
        #     ttl,
        #     json.dumps(session)
        # )
        
        self._mock_storage[f"session:{session_id}"] = session
        
        logger.info(f"Session created for user {user_id}: {session_id[:16]}...")
        
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve session data
        
        Args:
            session_id: Session ID
            
        Returns:
            Session data or None if not found/expired
        """
        # In real implementation:
        # session_data = self.client.get(f"session:{session_id}")
        # if session_data:
        #     return json.loads(session_data)
        
        session = self._mock_storage.get(f"session:{session_id}")
        
        if session:
            # Check expiration
            expires_at = datetime.fromisoformat(session['expires_at'])
            if datetime.utcnow() > expires_at:
                self.delete_session(session_id)
                return None
            
            return session
        
        return None
    
    def update_session(self, session_id: str, updates: Dict[str, Any],
                      extend_ttl: bool = True, ttl: int = 3600) -> bool:
        """
        Update session data
        
        Args:
            session_id: Session ID
            updates: Data to update
            extend_ttl: Whether to extend TTL
            ttl: New TTL if extending
            
        Returns:
            Success status
        """
        session = self.get_session(session_id)
        
        if not session:
            return False
        
        # Update data
        session['data'].update(updates)
        session['updated_at'] = datetime.utcnow().isoformat()
        
        if extend_ttl:
            session['expires_at'] = (datetime.utcnow() + timedelta(seconds=ttl)).isoformat()
        
        # In real implementation:
        # self.client.setex(
        #     f"session:{session_id}",
        #     ttl if extend_ttl else self.client.ttl(f"session:{session_id}"),
        #     json.dumps(session)
        # )
        
        self._mock_storage[f"session:{session_id}"] = session
        
        return True
    
    def delete_session(self, session_id: str) -> bool:
        """Delete session"""
        # In real implementation:
        # return bool(self.client.delete(f"session:{session_id}"))
        
        if f"session:{session_id}" in self._mock_storage:
            del self._mock_storage[f"session:{session_id}"]
            logger.info(f"Session deleted: {session_id[:16]}...")
            return True
        
        return False
    
    def get_user_sessions(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all active sessions for a user"""
        sessions = []
        
        # In real implementation:
        # for key in self.client.scan_iter(match="session:*"):
        #     session_data = self.client.get(key)
        #     session = json.loads(session_data)
        #     if session['user_id'] == user_id:
        #         sessions.append(session)
        
        for key, session in self._mock_storage.items():
            if key.startswith("session:") and session['user_id'] == user_id:
                sessions.append(session)
        
        return sessions
    
    def delete_user_sessions(self, user_id: str) -> int:
        """Delete all sessions for a user"""
        count = 0
        
        sessions = self.get_user_sessions(user_id)
        for session in sessions:
            if self.delete_session(session['session_id']):
                count += 1
        
        logger.info(f"Deleted {count} sessions for user {user_id}")
        
        return count


class CacheManager:
    """Cache manager for application data"""
    
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 1):
        """Initialize cache manager"""
        self.host = host
        self.port = port
        self.db = db
        
        # In real implementation: use redis-py
        self.client = None
        self._mock_cache = {}
        
        logger.info("Cache manager initialized (mock mode)")
    
    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """
        Set cache value
        
        Args:
            key: Cache key
            value: Value to cache (will be JSON serialized)
            ttl: Time to live in seconds
            
        Returns:
            Success status
        """
        cache_entry = {
            "value": value,
            "created_at": datetime.utcnow().isoformat(),
            "expires_at": (datetime.utcnow() + timedelta(seconds=ttl)).isoformat()
        }
        
        # In real implementation:
        # self.client.setex(key, ttl, json.dumps(value))
        
        self._mock_cache[key] = cache_entry
        
        logger.debug(f"Cache set: {key}")
        
        return True
    
    def get(self, key: str) -> Optional[Any]:
        """Get cache value"""
        # In real implementation:
        # cached = self.client.get(key)
        # return json.loads(cached) if cached else None
        
        cache_entry = self._mock_cache.get(key)
        
        if cache_entry:
            # Check expiration
            expires_at = datetime.fromisoformat(cache_entry['expires_at'])
            if datetime.utcnow() > expires_at:
                self.delete(key)
                return None
            
            return cache_entry['value']
        
        return None
    
    def delete(self, key: str) -> bool:
        """Delete cache entry"""
        # In real implementation:
        # return bool(self.client.delete(key))
        
        if key in self._mock_cache:
            del self._mock_cache[key]
            return True
        
        return False
    
    def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        return self.get(key) is not None
    
    def cache_resource_list(self, resource_type: str, resources: List[Dict[str, Any]],
                          ttl: int = 300) -> bool:
        """Cache resource list"""
        key = f"resources:{resource_type}"
        return self.set(key, resources, ttl)
    
    def get_cached_resource_list(self, resource_type: str) -> Optional[List[Dict[str, Any]]]:
        """Get cached resource list"""
        key = f"resources:{resource_type}"
        return self.get(key)
    
    def cache_job_status(self, job_id: str, status: Dict[str, Any], ttl: int = 600) -> bool:
        """Cache job status"""
        key = f"job:{job_id}"
        return self.set(key, status, ttl)
    
    def get_cached_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get cached job status"""
        key = f"job:{job_id}"
        return self.get(key)
    
    def cache_compliance_results(self, account_id: str, results: Dict[str, Any],
                                ttl: int = 1800) -> bool:
        """Cache compliance scan results"""
        key = f"compliance:{account_id}"
        return self.set(key, results, ttl)
    
    def get_cached_compliance_results(self, account_id: str) -> Optional[Dict[str, Any]]:
        """Get cached compliance results"""
        key = f"compliance:{account_id}"
        return self.get(key)
    
    def cache_cost_data(self, account_id: str, period: str, 
                       cost_data: Dict[str, Any], ttl: int = 3600) -> bool:
        """Cache cost analysis data"""
        key = f"costs:{account_id}:{period}"
        return self.set(key, cost_data, ttl)
    
    def get_cached_cost_data(self, account_id: str, period: str) -> Optional[Dict[str, Any]]:
        """Get cached cost data"""
        key = f"costs:{account_id}:{period}"
        return self.get(key)
    
    def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate all keys matching pattern"""
        count = 0
        
        # In real implementation:
        # for key in self.client.scan_iter(match=pattern):
        #     self.client.delete(key)
        #     count += 1
        
        keys_to_delete = [key for key in self._mock_cache.keys() if pattern in key]
        for key in keys_to_delete:
            self.delete(key)
            count += 1
        
        logger.info(f"Invalidated {count} cache entries matching pattern: {pattern}")
        
        return count
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        # In real implementation:
        # info = self.client.info('stats')
        
        return {
            "total_keys": len(self._mock_cache),
            "mode": "demo",
            "timestamp": datetime.utcnow().isoformat()
        }


class TemporaryDataStore:
    """Temporary data storage for large objects"""
    
    def __init__(self, redis_client=None):
        """Initialize temporary data store"""
        self.cache_manager = redis_client or CacheManager()
        self._temp_storage = {}
    
    def store_terraform_plan(self, plan_id: str, plan_data: Dict[str, Any],
                           ttl: int = 86400) -> bool:
        """
        Store Terraform plan temporarily
        
        Args:
            plan_id: Plan identifier
            plan_data: Plan data
            ttl: Time to live (default 24 hours)
            
        Returns:
            Success status
        """
        key = f"terraform:plan:{plan_id}"
        return self.cache_manager.set(key, plan_data, ttl)
    
    def get_terraform_plan(self, plan_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve stored Terraform plan"""
        key = f"terraform:plan:{plan_id}"
        return self.cache_manager.get(key)
    
    def store_scan_results(self, scan_id: str, results: Dict[str, Any],
                          ttl: int = 604800) -> bool:
        """
        Store compliance scan results
        
        Args:
            scan_id: Scan identifier
            results: Scan results
            ttl: Time to live (default 7 days)
            
        Returns:
            Success status
        """
        key = f"scan:results:{scan_id}"
        return self.cache_manager.set(key, results, ttl)
    
    def get_scan_results(self, scan_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve scan results"""
        key = f"scan:results:{scan_id}"
        return self.cache_manager.get(key)


# Mock implementations for demo
class MockRedisSessionStore:
    """Mock session store for demo"""
    
    def __init__(self):
        self.sessions = {}
    
    def create_session(self, user_id: str, session_data: Dict[str, Any],
                      ttl: int = 3600) -> str:
        """Mock create session"""
        session_id = hashlib.sha256(
            f"{user_id}:{datetime.utcnow().isoformat()}".encode()
        ).hexdigest()
        
        self.sessions[session_id] = {
            "session_id": session_id,
            "user_id": user_id,
            "data": session_data,
            "created_at": datetime.utcnow().isoformat()
        }
        
        logger.info(f"[DEMO] Session created: {session_id[:16]}...")
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Mock get session"""
        return self.sessions.get(session_id)
    
    def update_session(self, session_id: str, updates: Dict[str, Any],
                      extend_ttl: bool = True, ttl: int = 3600) -> bool:
        """Mock update session"""
        if session_id in self.sessions:
            self.sessions[session_id]['data'].update(updates)
            return True
        return False
    
    def delete_session(self, session_id: str) -> bool:
        """Mock delete session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False


class MockCacheManager:
    """Mock cache manager for demo"""
    
    def __init__(self):
        self.cache = {}
    
    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Mock set"""
        self.cache[key] = value
        logger.debug(f"[DEMO] Cache set: {key}")
        return True
    
    def get(self, key: str) -> Optional[Any]:
        """Mock get"""
        return self.cache.get(key)
    
    def delete(self, key: str) -> bool:
        """Mock delete"""
        if key in self.cache:
            del self.cache[key]
            return True
        return False
    
    def exists(self, key: str) -> bool:
        """Mock exists"""
        return key in self.cache
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Mock stats"""
        return {
            "total_keys": len(self.cache),
            "mode": "demo",
            "timestamp": datetime.utcnow().isoformat()
        }
