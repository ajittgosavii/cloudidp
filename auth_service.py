"""
CloudIDP Backend Infrastructure - Authentication Service
Handles JWT tokens, AWS Cognito, and SSO authentication
"""

import boto3
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import jwt
import hashlib
import secrets
from backend_config import BackendConfig, AuthProvider
from backend_models import User, UserLogin, UserToken, UserRole
from database_service import DatabaseService
import logging

logger = logging.getLogger(__name__)


class AuthenticationService:
    """
    Authentication and authorization service
    Supports AWS Cognito, SAML SSO, and demo mode
    """
    
    def __init__(self, config: BackendConfig, database: DatabaseService):
        self.config = config
        self.database = database
        self.demo_mode = config.demo_mode
        
        if not self.demo_mode:
            if config.auth_provider == AuthProvider.COGNITO:
                self.cognito_client = boto3.client(
                    'cognito-idp',
                    region_name=config.cognito_region or config.region
                )
            # Add other auth providers as needed
        
        # Demo credentials for testing
        self._demo_users = {
            "admin": {
                "password": self._hash_password("admin123"),
                "user_id": "user-001",
                "role": UserRole.ADMIN
            },
            "architect": {
                "password": self._hash_password("architect123"),
                "user_id": "user-002",
                "role": UserRole.ARCHITECT
            },
            "developer": {
                "password": self._hash_password("developer123"),
                "user_id": "user-003",
                "role": UserRole.DEVELOPER
            }
        }
    
    # ==================== Password Hashing ====================
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return self._hash_password(password) == hashed
    
    # ==================== JWT Token Management ====================
    
    def _create_jwt_token(self, user: User) -> UserToken:
        """Create JWT access token"""
        expires_in = self.config.jwt_expiration_minutes * 60
        expiration = datetime.utcnow() + timedelta(seconds=expires_in)
        
        payload = {
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "role": user.role.value,
            "permissions": user.permissions,
            "exp": expiration,
            "iat": datetime.utcnow(),
            "iss": "cloudidp-backend"
        }
        
        token = jwt.encode(
            payload,
            self.config.jwt_secret_key,
            algorithm=self.config.jwt_algorithm
        )
        
        return UserToken(
            access_token=token,
            expires_in=expires_in,
            user_id=user.user_id,
            role=user.role
        )
    
    def verify_jwt_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(
                token,
                self.config.jwt_secret_key,
                algorithms=[self.config.jwt_algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {e}")
            return None
    
    # ==================== Demo Mode Authentication ====================
    
    def _authenticate_demo(self, login: UserLogin) -> Optional[User]:
        """Authenticate using demo credentials"""
        demo_user = self._demo_users.get(login.username)
        if not demo_user:
            return None
        
        if not self._verify_password(login.password, demo_user["password"]):
            return None
        
        # Get or create user in database
        user = self.database.get_user(demo_user["user_id"])
        if not user:
            user = User(
                user_id=demo_user["user_id"],
                username=login.username,
                email=f"{login.username}@demo.cloudidp.com",
                full_name=f"{login.username.title()} User",
                role=demo_user["role"],
                is_active=True,
                permissions=self._get_default_permissions(demo_user["role"])
            )
            user = self.database.create_user(user)
        
        return user
    
    # ==================== AWS Cognito Authentication ====================
    
    def _authenticate_cognito(self, login: UserLogin) -> Optional[User]:
        """Authenticate using AWS Cognito"""
        try:
            response = self.cognito_client.initiate_auth(
                ClientId=self.config.cognito_client_id,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': login.username,
                    'PASSWORD': login.password
                }
            )
            
            # Get user attributes from Cognito
            user_info = self.cognito_client.get_user(
                AccessToken=response['AuthenticationResult']['AccessToken']
            )
            
            # Extract user attributes
            attributes = {attr['Name']: attr['Value'] for attr in user_info['UserAttributes']}
            
            # Get or create user in database
            cognito_user_id = user_info['Username']
            user = self.database.get_user(cognito_user_id)
            
            if not user:
                user = User(
                    user_id=cognito_user_id,
                    username=login.username,
                    email=attributes.get('email'),
                    full_name=attributes.get('name', login.username),
                    role=UserRole(attributes.get('custom:role', 'developer')),
                    cognito_user_id=cognito_user_id,
                    is_active=True
                )
                user = self.database.create_user(user)
            
            return user
            
        except self.cognito_client.exceptions.NotAuthorizedException:
            logger.warning(f"Authentication failed for user: {login.username}")
            return None
        except Exception as e:
            logger.error(f"Cognito authentication error: {e}")
            return None
    
    # ==================== SSO Authentication ====================
    
    def _authenticate_sso(self, saml_response: str) -> Optional[User]:
        """Authenticate using SAML SSO response"""
        # TODO: Implement SAML assertion validation
        logger.warning("SSO authentication not yet implemented")
        return None
    
    # ==================== Public Authentication Methods ====================
    
    def authenticate(self, login: UserLogin) -> Optional[UserToken]:
        """
        Authenticate user and return JWT token
        
        Args:
            login: UserLogin credentials
            
        Returns:
            UserToken if authentication successful, None otherwise
        """
        user = None
        
        if self.demo_mode or self.config.auth_provider == AuthProvider.DEMO:
            user = self._authenticate_demo(login)
        elif self.config.auth_provider == AuthProvider.COGNITO:
            user = self._authenticate_cognito(login)
        else:
            logger.error(f"Unsupported auth provider: {self.config.auth_provider}")
            return None
        
        if user:
            return self._create_jwt_token(user)
        
        return None
    
    def validate_token(self, token: str) -> Optional[User]:
        """
        Validate JWT token and return user
        
        Args:
            token: JWT access token
            
        Returns:
            User if token is valid, None otherwise
        """
        payload = self.verify_jwt_token(token)
        if not payload:
            return None
        
        user = self.database.get_user(payload['user_id'])
        if not user or not user.is_active:
            return None
        
        return user
    
    # ==================== User Registration ====================
    
    def register_user(self, username: str, email: str, password: str, 
                     full_name: str, role: UserRole = UserRole.DEVELOPER) -> Optional[User]:
        """
        Register a new user
        
        Args:
            username: Username
            email: Email address
            password: Password
            full_name: Full name
            role: User role
            
        Returns:
            Created User or None if registration fails
        """
        # Check if user already exists
        existing_user = self.database.get_user_by_email(email)
        if existing_user:
            logger.warning(f"User with email {email} already exists")
            return None
        
        if self.demo_mode or self.config.auth_provider == AuthProvider.DEMO:
            # Create user directly in database
            user = User(
                username=username,
                email=email,
                full_name=full_name,
                role=role,
                is_active=True,
                permissions=self._get_default_permissions(role)
            )
            return self.database.create_user(user)
        
        elif self.config.auth_provider == AuthProvider.COGNITO:
            try:
                # Create user in Cognito
                response = self.cognito_client.sign_up(
                    ClientId=self.config.cognito_client_id,
                    Username=username,
                    Password=password,
                    UserAttributes=[
                        {'Name': 'email', 'Value': email},
                        {'Name': 'name', 'Value': full_name},
                        {'Name': 'custom:role', 'Value': role.value}
                    ]
                )
                
                # Create user in database
                user = User(
                    user_id=response['UserSub'],
                    username=username,
                    email=email,
                    full_name=full_name,
                    role=role,
                    cognito_user_id=response['UserSub'],
                    is_active=False  # Pending confirmation
                )
                return self.database.create_user(user)
                
            except Exception as e:
                logger.error(f"Error registering user in Cognito: {e}")
                return None
        
        return None
    
    def confirm_user(self, username: str, confirmation_code: str) -> bool:
        """Confirm user registration (Cognito)"""
        if self.demo_mode or self.config.auth_provider != AuthProvider.COGNITO:
            return True
        
        try:
            self.cognito_client.confirm_sign_up(
                ClientId=self.config.cognito_client_id,
                Username=username,
                ConfirmationCode=confirmation_code
            )
            
            # Activate user in database
            user = self.database.get_user_by_email(f"{username}@*")  # Find by username pattern
            if user:
                self.database.update("users", {"user_id": user.user_id}, {"is_active": True})
            
            return True
        except Exception as e:
            logger.error(f"Error confirming user: {e}")
            return False
    
    # ==================== Authorization ====================
    
    def check_permission(self, user: User, permission: str) -> bool:
        """Check if user has specific permission"""
        if user.role == UserRole.ADMIN:
            return True  # Admin has all permissions
        
        return permission in user.permissions
    
    def check_account_access(self, user: User, account_id: str) -> bool:
        """Check if user has access to specific account"""
        if user.role == UserRole.ADMIN:
            return True
        
        return account_id in user.account_access
    
    def _get_default_permissions(self, role: UserRole) -> List[str]:
        """Get default permissions for role"""
        permissions = {
            UserRole.ADMIN: [
                "account:create", "account:read", "account:update", "account:delete",
                "user:create", "user:read", "user:update", "user:delete",
                "deployment:create", "deployment:read", "deployment:update", "deployment:delete",
                "policy:create", "policy:read", "policy:update", "policy:delete",
                "audit:read", "cost:read"
            ],
            UserRole.ARCHITECT: [
                "account:read", "account:update",
                "deployment:create", "deployment:read", "deployment:update",
                "policy:create", "policy:read", "policy:update",
                "audit:read", "cost:read"
            ],
            UserRole.DEVELOPER: [
                "account:read",
                "deployment:create", "deployment:read",
                "policy:read",
                "cost:read"
            ],
            UserRole.VIEWER: [
                "account:read",
                "deployment:read",
                "policy:read",
                "cost:read"
            ],
            UserRole.AUDITOR: [
                "account:read",
                "deployment:read",
                "policy:read",
                "audit:read",
                "cost:read"
            ]
        }
        
        return permissions.get(role, [])
    
    # ==================== Password Management ====================
    
    def reset_password_request(self, email: str) -> bool:
        """Request password reset"""
        if self.demo_mode:
            logger.info(f"Password reset requested for {email} (demo mode)")
            return True
        
        if self.config.auth_provider == AuthProvider.COGNITO:
            try:
                user = self.database.get_user_by_email(email)
                if not user:
                    return False
                
                self.cognito_client.forgot_password(
                    ClientId=self.config.cognito_client_id,
                    Username=user.username
                )
                return True
            except Exception as e:
                logger.error(f"Error requesting password reset: {e}")
                return False
        
        return False
    
    def reset_password_confirm(self, username: str, code: str, new_password: str) -> bool:
        """Confirm password reset with code"""
        if self.demo_mode:
            return True
        
        if self.config.auth_provider == AuthProvider.COGNITO:
            try:
                self.cognito_client.confirm_forgot_password(
                    ClientId=self.config.cognito_client_id,
                    Username=username,
                    ConfirmationCode=code,
                    Password=new_password
                )
                return True
            except Exception as e:
                logger.error(f"Error confirming password reset: {e}")
                return False
        
        return False
    
    # ==================== Session Management ====================
    
    def refresh_token(self, refresh_token: str) -> Optional[UserToken]:
        """Refresh access token using refresh token"""
        if self.demo_mode:
            # In demo mode, decode the current token and issue a new one
            payload = self.verify_jwt_token(refresh_token)
            if payload:
                user = self.database.get_user(payload['user_id'])
                if user:
                    return self._create_jwt_token(user)
        
        # TODO: Implement refresh token logic for Cognito
        return None
    
    def logout(self, token: str) -> bool:
        """Logout user (revoke token)"""
        # In demo mode, tokens are stateless so no action needed
        if self.demo_mode:
            return True
        
        # TODO: Implement token revocation for Cognito
        return True
