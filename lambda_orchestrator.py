"""
CloudIDP Backend Infrastructure - Lambda Orchestrator
Manages and invokes AWS Lambda functions for backend processing
"""

import boto3
import json
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
import base64
import zipfile
import io
from backend_config import BackendConfig, LAMBDA_FUNCTIONS
from backend_models import *
import logging
from config import get_aws_account_config


logger = logging.getLogger(__name__)


class LambdaOrchestrator:
    """
    Lambda Function Orchestrator
    Manages Lambda function deployment and invocation
    Supports demo mode for testing without AWS infrastructure
    """
    
    def __init__(self, config: BackendConfig):
        self.config = config
        self.demo_mode = config.demo_mode
        
        if not self.demo_mode:
            self.lambda_client = boto3.client('lambda', region_name=config.region)
            self.iam_client = boto3.client('iam', region_name=config.region)
            self.function_arns: Dict[str, str] = {}
            self._init_lambda_functions()
        else:
            # Demo mode: register local handlers
            self._demo_handlers: Dict[str, Callable] = {}
            self._demo_invocations: List[Dict] = []
            self._register_demo_handlers()
    
    # ==================== Lambda Initialization ====================
    
    def _init_lambda_functions(self):
        """Initialize Lambda functions - check if they exist"""
        try:
            for function_name in LAMBDA_FUNCTIONS.keys():
                full_function_name = self.config.get_lambda_name(function_name)
                
                try:
                    response = self.lambda_client.get_function(
                        FunctionName=full_function_name
                    )
                    self.function_arns[function_name] = response['Configuration']['FunctionArn']
                    logger.info(f"Lambda function {full_function_name} found")
                except self.lambda_client.exceptions.ResourceNotFoundException:
                    logger.warning(f"Lambda function {full_function_name} not found")
        except Exception as e:
            logger.error(f"Error initializing Lambda functions: {e}")
    
    def _register_demo_handlers(self):
        """Register demo handlers for testing"""
        self._demo_handlers = {
            "account_provisioner": self._demo_account_provisioner,
            "policy_enforcer": self._demo_policy_enforcer,
            "cost_analyzer": self._demo_cost_analyzer,
            "compliance_checker": self._demo_compliance_checker,
            "notification_dispatcher": self._demo_notification_dispatcher
        }
    
    # ==================== Lambda Function Deployment ====================
    
    def create_lambda_function(self, function_name: str, 
                              code_path: str,
                              role_arn: str,
                              environment_vars: Optional[Dict[str, str]] = None) -> bool:
        """
        Create or update a Lambda function
        
        Args:
            function_name: Name of the Lambda function
            code_path: Path to the deployment package (zip file)
            role_arn: IAM role ARN for Lambda execution
            environment_vars: Environment variables
            
        Returns:
            True if successful, False otherwise
        """
        if self.demo_mode:
            logger.info(f"Demo: Would create Lambda function {function_name}")
            return True
        
        full_function_name = self.config.get_lambda_name(function_name)
        function_config = LAMBDA_FUNCTIONS.get(function_name, {})
        
        try:
            # Read deployment package
            with open(code_path, 'rb') as f:
                zip_content = f.read()
            
            # Check if function exists
            try:
                self.lambda_client.get_function(FunctionName=full_function_name)
                # Function exists, update it
                response = self.lambda_client.update_function_code(
                    FunctionName=full_function_name,
                    ZipFile=zip_content
                )
                logger.info(f"Updated Lambda function {full_function_name}")
                
            except self.lambda_client.exceptions.ResourceNotFoundException:
                # Function doesn't exist, create it
                response = self.lambda_client.create_function(
                    FunctionName=full_function_name,
                    Runtime=self.config.lambda_runtime,
                    Role=role_arn,
                    Handler=function_config.get('handler', 'index.handler'),
                    Code={'ZipFile': zip_content},
                    Description=function_config.get('description', ''),
                    Timeout=self.config.lambda_timeout,
                    MemorySize=self.config.lambda_memory_size,
                    Environment={
                        'Variables': environment_vars or {}
                    }
                )
                logger.info(f"Created Lambda function {full_function_name}")
            
            self.function_arns[function_name] = response['FunctionArn']
            return True
            
        except Exception as e:
            logger.error(f"Error creating Lambda function {function_name}: {e}")
            return False
    
    def delete_lambda_function(self, function_name: str) -> bool:
        """Delete a Lambda function"""
        if self.demo_mode:
            logger.info(f"Demo: Would delete Lambda function {function_name}")
            return True
        
        full_function_name = self.config.get_lambda_name(function_name)
        
        try:
            self.lambda_client.delete_function(FunctionName=full_function_name)
            logger.info(f"Deleted Lambda function {full_function_name}")
            return True
        except Exception as e:
            logger.error(f"Error deleting Lambda function {function_name}: {e}")
            return False
    
    # ==================== Lambda Function Invocation ====================
    
    def invoke_function(self, function_name: str, payload: Dict[str, Any],
                       invocation_type: str = "RequestResponse") -> Dict[str, Any]:
        """
        Invoke a Lambda function
        
        Args:
            function_name: Name of the Lambda function
            payload: Input payload for the function
            invocation_type: "RequestResponse" (synchronous) or "Event" (asynchronous)
            
        Returns:
            Response from Lambda function
        """
        if self.demo_mode:
            return self._invoke_demo_handler(function_name, payload)
        
        full_function_name = self.config.get_lambda_name(function_name)
        
        try:
            response = self.lambda_client.invoke(
                FunctionName=full_function_name,
                InvocationType=invocation_type,
                Payload=json.dumps(payload)
            )
            
            result = {
                "StatusCode": response['StatusCode'],
                "ExecutedVersion": response.get('ExecutedVersion', '$LATEST')
            }
            
            if invocation_type == "RequestResponse":
                payload_response = json.loads(response['Payload'].read())
                result["Payload"] = payload_response
            
            logger.info(f"Invoked Lambda function {full_function_name}")
            return result
            
        except Exception as e:
            logger.error(f"Error invoking Lambda function {function_name}: {e}")
            return {"StatusCode": 500, "Error": str(e)}
    
    def invoke_async(self, function_name: str, payload: Dict[str, Any]) -> bool:
        """Invoke Lambda function asynchronously"""
        result = self.invoke_function(function_name, payload, "Event")
        return result.get("StatusCode") == 202
    
    # ==================== Demo Mode Handlers ====================
    
    def _invoke_demo_handler(self, function_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke demo handler"""
        handler = self._demo_handlers.get(function_name)
        
        # Log invocation
        self._demo_invocations.append({
            "function_name": function_name,
            "payload": payload,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        if not handler:
            logger.warning(f"No demo handler for {function_name}")
            return {
                "StatusCode": 404,
                "Error": f"Handler not found: {function_name}"
            }
        
        try:
            result = handler(payload)
            return {
                "StatusCode": 200,
                "Payload": result
            }
        except Exception as e:
            logger.error(f"Demo handler error: {e}")
            return {
                "StatusCode": 500,
                "Error": str(e)
            }
    
    def _demo_account_provisioner(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Demo handler for account provisioning"""
        logger.info(f"Demo: Provisioning account {payload.get('account_name')}")
        
        return {
            "success": True,
            "account_id": get_aws_account_config()['account_id'],
            "status": "active",
            "message": "Account provisioned successfully (demo)",
            "provisioning_time_seconds": 120
        }
    
    def _demo_policy_enforcer(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Demo handler for policy enforcement"""
        logger.info(f"Demo: Enforcing policy {payload.get('policy_name')}")
        
        return {
            "success": True,
            "policies_enforced": 5,
            "accounts_affected": 3,
            "violations_found": 0,
            "message": "Policies enforced successfully (demo)"
        }
    
    def _demo_cost_analyzer(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Demo handler for cost analysis"""
        logger.info(f"Demo: Analyzing costs for {payload.get('date_range')}")
        
        return {
            "success": True,
            "total_cost": 15234.56,
            "cost_by_service": {
                "EC2": 8500.00,
                "RDS": 3200.00,
                "S3": 1534.56,
                "Lambda": 1000.00,
                "Other": 1000.00
            },
            "savings_opportunities": [
                {
                    "service": "EC2",
                    "recommendation": "Right-size underutilized instances",
                    "potential_savings": 2400.00
                },
                {
                    "service": "RDS",
                    "recommendation": "Use Reserved Instances",
                    "potential_savings": 1200.00
                }
            ],
            "message": "Cost analysis completed (demo)"
        }
    
    def _demo_compliance_checker(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Demo handler for compliance checking"""
        logger.info(f"Demo: Checking compliance for {payload.get('account_id')}")
        
        return {
            "success": True,
            "checks_performed": 45,
            "compliant": 42,
            "non_compliant": 3,
            "violations": [
                {
                    "rule": "S3-001",
                    "resource": "bucket-prod-data",
                    "severity": "high",
                    "finding": "Bucket has public access enabled"
                },
                {
                    "rule": "EC2-003",
                    "resource": "i-1234567890abcdef0",
                    "severity": "medium",
                    "finding": "Instance missing required tags"
                },
                {
                    "rule": "RDS-002",
                    "resource": "db-production",
                    "severity": "medium",
                    "finding": "Database not encrypted at rest"
                }
            ],
            "message": "Compliance check completed (demo)"
        }
    
    def _demo_notification_dispatcher(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Demo handler for notification dispatch"""
        logger.info(f"Demo: Dispatching notification {payload.get('notification_type')}")
        
        return {
            "success": True,
            "notifications_sent": 3,
            "channels": ["email", "slack", "sns"],
            "message": "Notifications dispatched successfully (demo)"
        }
    
    # ==================== Specialized Invocations ====================
    
    def provision_account(self, account_request: AccountRequest) -> Dict[str, Any]:
        """Invoke account provisioner Lambda"""
        payload = {
            "action": "provision_account",
            "account_request": account_request.dict()
        }
        return self.invoke_function("account_provisioner", payload)
    
    def enforce_policies(self, policy_ids: List[str], target_accounts: List[str]) -> Dict[str, Any]:
        """Invoke policy enforcer Lambda"""
        payload = {
            "action": "enforce_policies",
            "policy_ids": policy_ids,
            "target_accounts": target_accounts
        }
        return self.invoke_function("policy_enforcer", payload)
    
    def analyze_costs(self, date_range: Dict[str, str], account_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """Invoke cost analyzer Lambda"""
        payload = {
            "action": "analyze_costs",
            "date_range": date_range,
            "account_ids": account_ids or []
        }
        return self.invoke_function("cost_analyzer", payload)
    
    def check_compliance(self, account_id: str, rules: Optional[List[str]] = None) -> Dict[str, Any]:
        """Invoke compliance checker Lambda"""
        payload = {
            "action": "check_compliance",
            "account_id": account_id,
            "rules": rules or []
        }
        return self.invoke_function("compliance_checker", payload)
    
    def send_notification(self, notification_type: str, recipients: List[str], 
                         message: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Invoke notification dispatcher Lambda"""
        payload = {
            "action": "send_notification",
            "notification_type": notification_type,
            "recipients": recipients,
            "message": message,
            "data": data or {}
        }
        return self.invoke_function("notification_dispatcher", payload)
    
    # ==================== Function Management ====================
    
    def get_function_configuration(self, function_name: str) -> Dict[str, Any]:
        """Get Lambda function configuration"""
        if self.demo_mode:
            return {
                "FunctionName": function_name,
                "Runtime": self.config.lambda_runtime,
                "Timeout": self.config.lambda_timeout,
                "MemorySize": self.config.lambda_memory_size,
                "Description": LAMBDA_FUNCTIONS.get(function_name, {}).get('description', '')
            }
        
        full_function_name = self.config.get_lambda_name(function_name)
        
        try:
            response = self.lambda_client.get_function_configuration(
                FunctionName=full_function_name
            )
            return response
        except Exception as e:
            logger.error(f"Error getting function configuration: {e}")
            return {}
    
    def update_function_configuration(self, function_name: str, 
                                     timeout: Optional[int] = None,
                                     memory: Optional[int] = None,
                                     environment: Optional[Dict[str, str]] = None) -> bool:
        """Update Lambda function configuration"""
        if self.demo_mode:
            logger.info(f"Demo: Would update {function_name} configuration")
            return True
        
        full_function_name = self.config.get_lambda_name(function_name)
        
        try:
            update_params = {'FunctionName': full_function_name}
            
            if timeout:
                update_params['Timeout'] = timeout
            if memory:
                update_params['MemorySize'] = memory
            if environment:
                update_params['Environment'] = {'Variables': environment}
            
            self.lambda_client.update_function_configuration(**update_params)
            logger.info(f"Updated configuration for {full_function_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating function configuration: {e}")
            return False
    
    def list_functions(self) -> List[Dict[str, Any]]:
        """List all Lambda functions"""
        if self.demo_mode:
            return [
                {
                    "FunctionName": name,
                    "Description": config.get('description', ''),
                    "Runtime": self.config.lambda_runtime
                }
                for name, config in LAMBDA_FUNCTIONS.items()
            ]
        
        try:
            response = self.lambda_client.list_functions()
            # Filter to only CloudIDP functions
            prefix = self.config.lambda_function_prefix
            return [
                func for func in response.get('Functions', [])
                if func['FunctionName'].startswith(prefix)
            ]
        except Exception as e:
            logger.error(f"Error listing functions: {e}")
            return []
    
    # ==================== Monitoring ====================
    
    def get_invocation_history(self) -> List[Dict[str, Any]]:
        """Get invocation history (demo mode only)"""
        if self.demo_mode:
            return self._demo_invocations
        return []
