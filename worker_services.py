"""
Worker Services for Async Job Processing
Handles Celery workers, Lambda functions, Terraform execution, and provisioning jobs
"""

import boto3
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from enum import Enum
import uuid
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JobStatus(Enum):
    """Job status enumeration"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class JobType(Enum):
    """Job type enumeration"""
    TERRAFORM_APPLY = "terraform_apply"
    TERRAFORM_DESTROY = "terraform_destroy"
    TERRAFORM_PLAN = "terraform_plan"
    ACCOUNT_PROVISION = "account_provision"
    RESOURCE_SCAN = "resource_scan"
    COMPLIANCE_CHECK = "compliance_check"
    COST_ANALYSIS = "cost_analysis"
    BACKUP_RESTORE = "backup_restore"


class TerraformExecutor:
    """Terraform execution engine for IaC provisioning"""
    
    def __init__(self):
        """Initialize Terraform executor"""
        self.working_dir = "/tmp/terraform"
        os.makedirs(self.working_dir, exist_ok=True)
    
    def execute_plan(self, job_id: str, terraform_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute Terraform plan
        
        Args:
            job_id: Unique job identifier
            terraform_config: Terraform configuration including:
                - modules: List of modules to apply
                - variables: Terraform variables
                - backend_config: Backend configuration
                - workspace: Terraform workspace
                
        Returns:
            Dict with plan execution results
        """
        logger.info(f"Executing Terraform plan for job {job_id}")
        
        try:
            # In real implementation, this would:
            # 1. Clone/copy Terraform modules
            # 2. Initialize Terraform
            # 3. Select/create workspace
            # 4. Run terraform plan
            # 5. Upload plan file to S3
            # 6. Return plan details
            
            result = {
                "status": "success",
                "job_id": job_id,
                "plan_id": f"plan-{uuid.uuid4()}",
                "resources_to_add": 15,
                "resources_to_change": 3,
                "resources_to_destroy": 0,
                "estimated_cost": "$127.50/month",
                "plan_file_s3": f"s3://terraform-plans/{job_id}/tfplan",
                "execution_time": "45s",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            logger.info(f"Terraform plan completed: {result['plan_id']}")
            return result
            
        except Exception as e:
            logger.error(f"Terraform plan failed: {e}")
            return {
                "status": "failed",
                "job_id": job_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def execute_apply(self, job_id: str, plan_id: str, 
                     auto_approve: bool = False) -> Dict[str, Any]:
        """
        Execute Terraform apply
        
        Args:
            job_id: Unique job identifier
            plan_id: Plan ID from previous plan execution
            auto_approve: Whether to auto-approve the apply
            
        Returns:
            Dict with apply execution results
        """
        logger.info(f"Executing Terraform apply for job {job_id}, plan {plan_id}")
        
        try:
            # In real implementation, this would:
            # 1. Download plan file from S3
            # 2. Execute terraform apply
            # 3. Stream logs to CloudWatch
            # 4. Update state in backend
            # 5. Return apply results
            
            result = {
                "status": "success",
                "job_id": job_id,
                "plan_id": plan_id,
                "resources_created": 15,
                "resources_modified": 3,
                "resources_destroyed": 0,
                "state_file_s3": f"s3://terraform-states/{job_id}/terraform.tfstate",
                "outputs": {
                    "vpc_id": "vpc-abc123",
                    "subnet_ids": ["subnet-xyz", "subnet-123"],
                    "security_group_id": "sg-456789"
                },
                "execution_time": "4m 23s",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            logger.info(f"Terraform apply completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Terraform apply failed: {e}")
            return {
                "status": "failed",
                "job_id": job_id,
                "plan_id": plan_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def execute_destroy(self, job_id: str, workspace: str) -> Dict[str, Any]:
        """Execute Terraform destroy"""
        logger.info(f"Executing Terraform destroy for job {job_id}")
        
        try:
            result = {
                "status": "success",
                "job_id": job_id,
                "workspace": workspace,
                "resources_destroyed": 18,
                "execution_time": "3m 15s",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            logger.info(f"Terraform destroy completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Terraform destroy failed: {e}")
            return {
                "status": "failed",
                "job_id": job_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }


class LambdaWorker:
    """AWS Lambda worker for serverless job execution"""
    
    def __init__(self, region: str = 'us-east-1'):
        """Initialize Lambda client"""
        self.region = region
        try:
            self.client = boto3.client('lambda', region_name=region)
        except Exception as e:
            logger.error(f"Failed to initialize Lambda client: {e}")
            self.client = None
    
    def invoke_async(self, function_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Invoke Lambda function asynchronously
        
        Args:
            function_name: Name of the Lambda function
            payload: Payload to send to Lambda
            
        Returns:
            Dict with invocation status
        """
        if not self.client:
            return {"status": "error", "message": "Lambda client not initialized"}
        
        try:
            response = self.client.invoke(
                FunctionName=function_name,
                InvocationType='Event',  # Async invocation
                Payload=json.dumps(payload)
            )
            
            return {
                "status": "success",
                "status_code": response['StatusCode'],
                "request_id": response['ResponseMetadata']['RequestId'],
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Lambda invocation failed: {e}")
            return {"status": "failed", "error": str(e)}
    
    def invoke_sync(self, function_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Invoke Lambda function synchronously
        
        Args:
            function_name: Name of the Lambda function
            payload: Payload to send to Lambda
            
        Returns:
            Dict with invocation result and response
        """
        if not self.client:
            return {"status": "error", "message": "Lambda client not initialized"}
        
        try:
            response = self.client.invoke(
                FunctionName=function_name,
                InvocationType='RequestResponse',  # Sync invocation
                Payload=json.dumps(payload)
            )
            
            result_payload = json.loads(response['Payload'].read())
            
            return {
                "status": "success",
                "status_code": response['StatusCode'],
                "result": result_payload,
                "request_id": response['ResponseMetadata']['RequestId'],
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Lambda invocation failed: {e}")
            return {"status": "failed", "error": str(e)}


class CeleryWorker:
    """Celery worker for long-running background jobs"""
    
    def __init__(self, broker_url: str = 'redis://localhost:6379/0',
                 backend_url: str = 'redis://localhost:6379/1'):
        """
        Initialize Celery worker
        
        Args:
            broker_url: Message broker URL (Redis, RabbitMQ, SQS)
            backend_url: Result backend URL
        """
        self.broker_url = broker_url
        self.backend_url = backend_url
        self.jobs = {}  # In-memory job store for demo
    
    def submit_job(self, job_type: JobType, job_config: Dict[str, Any]) -> str:
        """
        Submit a new job to Celery queue
        
        Args:
            job_type: Type of job to execute
            job_config: Job configuration parameters
            
        Returns:
            Job ID for tracking
        """
        job_id = str(uuid.uuid4())
        
        job = {
            "job_id": job_id,
            "job_type": job_type.value,
            "status": JobStatus.PENDING.value,
            "config": job_config,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "started_at": None,
            "completed_at": None,
            "result": None,
            "error": None
        }
        
        self.jobs[job_id] = job
        
        logger.info(f"Job {job_id} submitted to queue: {job_type.value}")
        
        # In real implementation, this would publish to Celery broker
        # celery_app.send_task(job_type.value, args=[job_config], task_id=job_id)
        
        return job_id
    
    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """Get status of a job"""
        job = self.jobs.get(job_id)
        
        if not job:
            return {
                "status": "not_found",
                "message": f"Job {job_id} not found"
            }
        
        return {
            "status": "success",
            "job": job
        }
    
    def cancel_job(self, job_id: str) -> Dict[str, Any]:
        """Cancel a running job"""
        job = self.jobs.get(job_id)
        
        if not job:
            return {"status": "not_found"}
        
        if job["status"] in [JobStatus.COMPLETED.value, JobStatus.FAILED.value]:
            return {
                "status": "error",
                "message": "Cannot cancel completed or failed job"
            }
        
        job["status"] = JobStatus.CANCELLED.value
        job["updated_at"] = datetime.utcnow().isoformat()
        
        logger.info(f"Job {job_id} cancelled")
        
        return {
            "status": "success",
            "message": f"Job {job_id} cancelled"
        }


class ProvisioningJobManager:
    """Manager for coordinating provisioning jobs across workers"""
    
    def __init__(self, region: str = 'us-east-1'):
        """Initialize job manager"""
        self.region = region
        self.terraform = TerraformExecutor()
        self.lambda_worker = LambdaWorker(region)
        self.celery_worker = CeleryWorker()
    
    def create_infrastructure_job(self, infrastructure_config: Dict[str, Any]) -> str:
        """
        Create a new infrastructure provisioning job
        
        Args:
            infrastructure_config: Configuration for infrastructure
                - name: Infrastructure name
                - environment: Environment (dev, staging, prod)
                - modules: List of Terraform modules
                - variables: Terraform variables
                - auto_approve: Auto-approve apply
                
        Returns:
            Job ID for tracking
        """
        # Submit Terraform plan job
        job_config = {
            "operation": "terraform_plan",
            "infrastructure_name": infrastructure_config['name'],
            "environment": infrastructure_config['environment'],
            "terraform_config": {
                "modules": infrastructure_config.get('modules', []),
                "variables": infrastructure_config.get('variables', {}),
                "workspace": f"{infrastructure_config['name']}-{infrastructure_config['environment']}"
            }
        }
        
        job_id = self.celery_worker.submit_job(JobType.TERRAFORM_PLAN, job_config)
        
        logger.info(f"Infrastructure provisioning job created: {job_id}")
        
        return job_id
    
    def execute_compliance_scan(self, account_id: str, scan_config: Dict[str, Any]) -> str:
        """
        Execute compliance scanning job
        
        Args:
            account_id: AWS account ID to scan
            scan_config: Scan configuration
                - frameworks: List of compliance frameworks (PCI-DSS, HIPAA, etc.)
                - resources: Resource types to scan
                - severity: Minimum severity level
                
        Returns:
            Job ID for tracking
        """
        job_config = {
            "account_id": account_id,
            "frameworks": scan_config.get('frameworks', ['CIS-AWS']),
            "resources": scan_config.get('resources', ['all']),
            "severity": scan_config.get('severity', 'MEDIUM')
        }
        
        job_id = self.celery_worker.submit_job(JobType.COMPLIANCE_CHECK, job_config)
        
        logger.info(f"Compliance scan job created: {job_id}")
        
        return job_id
    
    def execute_cost_analysis(self, account_ids: List[str], 
                            analysis_config: Dict[str, Any]) -> str:
        """
        Execute cost analysis job
        
        Args:
            account_ids: List of AWS account IDs
            analysis_config: Analysis configuration
                - period: Analysis period (7d, 30d, 90d)
                - granularity: Data granularity (DAILY, MONTHLY)
                - group_by: Grouping dimensions
                
        Returns:
            Job ID for tracking
        """
        job_config = {
            "account_ids": account_ids,
            "period": analysis_config.get('period', '30d'),
            "granularity": analysis_config.get('granularity', 'DAILY'),
            "group_by": analysis_config.get('group_by', ['SERVICE', 'USAGE_TYPE'])
        }
        
        job_id = self.celery_worker.submit_job(JobType.COST_ANALYSIS, job_config)
        
        logger.info(f"Cost analysis job created: {job_id}")
        
        return job_id
    
    def get_job_logs(self, job_id: str, max_lines: int = 100) -> Dict[str, Any]:
        """
        Retrieve logs for a job
        
        Args:
            job_id: Job ID
            max_lines: Maximum number of log lines to return
            
        Returns:
            Dict with job logs
        """
        # In real implementation, this would fetch from CloudWatch Logs
        return {
            "status": "success",
            "job_id": job_id,
            "log_stream": f"/aws/lambda/provisioning-worker/{job_id}",
            "logs": [
                {"timestamp": "2025-11-19T10:00:00Z", "message": "Job started"},
                {"timestamp": "2025-11-19T10:00:15Z", "message": "Initializing Terraform"},
                {"timestamp": "2025-11-19T10:00:45Z", "message": "Terraform initialized successfully"},
                {"timestamp": "2025-11-19T10:01:30Z", "message": "Running terraform plan"},
                {"timestamp": "2025-11-19T10:02:15Z", "message": "Plan completed: 15 to add, 3 to change, 0 to destroy"}
            ]
        }
    
    def list_active_jobs(self, job_type: Optional[JobType] = None) -> Dict[str, Any]:
        """
        List all active jobs
        
        Args:
            job_type: Optional filter by job type
            
        Returns:
            Dict with list of active jobs
        """
        active_jobs = []
        
        for job_id, job in self.celery_worker.jobs.items():
            if job['status'] in [JobStatus.PENDING.value, JobStatus.RUNNING.value]:
                if job_type is None or job['job_type'] == job_type.value:
                    active_jobs.append(job)
        
        return {
            "status": "success",
            "count": len(active_jobs),
            "jobs": active_jobs
        }


# Mock implementations for demo mode
class MockProvisioningJobManager:
    """Mock job manager for demo mode"""
    
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.jobs = {}
    
    def create_infrastructure_job(self, infrastructure_config: Dict[str, Any]) -> str:
        """Mock infrastructure provisioning job"""
        job_id = str(uuid.uuid4())
        
        self.jobs[job_id] = {
            "job_id": job_id,
            "job_type": "terraform_plan",
            "status": "running",
            "infrastructure_name": infrastructure_config['name'],
            "environment": infrastructure_config['environment'],
            "progress": 45,
            "created_at": datetime.utcnow().isoformat(),
            "estimated_completion": (datetime.utcnow() + timedelta(minutes=5)).isoformat()
        }
        
        return job_id
    
    def execute_compliance_scan(self, account_id: str, scan_config: Dict[str, Any]) -> str:
        """Mock compliance scan job"""
        job_id = str(uuid.uuid4())
        
        self.jobs[job_id] = {
            "job_id": job_id,
            "job_type": "compliance_check",
            "status": "running",
            "account_id": account_id,
            "frameworks": scan_config.get('frameworks', ['CIS-AWS']),
            "progress": 67,
            "findings": {"critical": 2, "high": 8, "medium": 15, "low": 23},
            "created_at": datetime.utcnow().isoformat()
        }
        
        return job_id
    
    def execute_cost_analysis(self, account_ids: List[str], analysis_config: Dict[str, Any]) -> str:
        """Mock cost analysis job"""
        job_id = str(uuid.uuid4())
        
        self.jobs[job_id] = {
            "job_id": job_id,
            "job_type": "cost_analysis",
            "status": "completed",
            "account_count": len(account_ids),
            "total_cost": "$12,456.78",
            "savings_opportunities": "$1,234.56",
            "created_at": datetime.utcnow().isoformat()
        }
        
        return job_id
    
    def get_job_logs(self, job_id: str, max_lines: int = 100) -> Dict[str, Any]:
        """Mock job logs"""
        return {
            "status": "success",
            "job_id": job_id,
            "logs": [
                {"timestamp": datetime.utcnow().isoformat(), "message": "Job started (DEMO MODE)"},
                {"timestamp": datetime.utcnow().isoformat(), "message": "Processing resources..."},
                {"timestamp": datetime.utcnow().isoformat(), "message": "Analysis complete"}
            ]
        }
    
    def list_active_jobs(self, job_type: Optional[JobType] = None) -> Dict[str, Any]:
        """Mock active jobs list"""
        active_jobs = [
            {
                "job_id": "job-demo-001",
                "job_type": "terraform_plan",
                "status": "running",
                "progress": 75,
                "infrastructure_name": "prod-vpc",
                "created_at": datetime.utcnow().isoformat()
            },
            {
                "job_id": "job-demo-002",
                "job_type": "compliance_check",
                "status": "running",
                "progress": 45,
                "account_id": "123456789012",
                "created_at": datetime.utcnow().isoformat()
            }
        ]
        
        return {
            "status": "success",
            "count": len(active_jobs),
            "jobs": active_jobs
        }
