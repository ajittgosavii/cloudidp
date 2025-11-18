"""Demo Data Provider - Sample data for Demo Mode"""

from typing import List, Dict, Any

class DemoDataProvider:
    """Provides demo data for all modules"""
    
    @staticmethod
    def get_blueprint_library() -> List[Dict[str, Any]]:
        """Return sample blueprints"""
        return [
            {
                "id": "bp-001",
                "name": "Three-Tier Web Application",
                "category": "Web Application",
                "version": "2.1.0",
                "status": "Active",
                "description": "Standard three-tier architecture with load balancer, app servers, and database",
                "aws_services": ["VPC", "ALB", "EC2", "RDS", "CloudFront", "Route53", "WAF"],
                "environments": ["Development", "Staging", "Production"],
                "estimated_cost": 1250.00,
                "compliance_frameworks": ["PCI DSS", "SOC 2"],
                "author": "Cloud Architecture Team",
                "deployment_count": 23,
                "iac_template": '''resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "three-tier-vpc"
  }
}'''
            },
            {
                "id": "bp-002",
                "name": "Serverless API Backend",
                "category": "Serverless",
                "version": "1.5.0",
                "status": "Active",
                "description": "Event-driven serverless with Lambda, API Gateway, and DynamoDB",
                "aws_services": ["Lambda", "API Gateway", "DynamoDB", "S3", "CloudWatch"],
                "environments": ["Development", "Production"],
                "estimated_cost": 450.00,
                "compliance_frameworks": ["HIPAA", "GDPR"],
                "author": "Serverless Team",
                "deployment_count": 15,
                "iac_template": "# Serverless configuration..."
            },
            {
                "id": "bp-003",
                "name": "Data Lake Analytics",
                "category": "Data Analytics",
                "version": "3.0.0",
                "status": "Active",
                "description": "Scalable data lake with real-time and batch processing",
                "aws_services": ["S3", "Glue", "Athena", "EMR", "Kinesis", "QuickSight"],
                "environments": ["Production"],
                "estimated_cost": 3500.00,
                "compliance_frameworks": ["SOC 2", "ISO 27001"],
                "author": "Data Team",
                "deployment_count": 8,
                "iac_template": "# Data lake configuration..."
            },
            {
                "id": "bp-004",
                "name": "Microservices on EKS",
                "category": "Microservices",
                "version": "2.3.0",
                "status": "Active",
                "description": "EKS-based microservices with service mesh",
                "aws_services": ["EKS", "ECR", "ALB", "Route53", "CloudWatch"],
                "environments": ["Development", "Staging", "Production"],
                "estimated_cost": 2800.00,
                "compliance_frameworks": ["PCI DSS", "SOC 2"],
                "author": "Platform Team",
                "deployment_count": 12,
                "iac_template": "# EKS configuration..."
            }
        ]
    
    @staticmethod
    def get_tag_policies() -> List[Dict[str, Any]]:
        """Return sample tag policies"""
        return [
            {
                "id": "tp-001",
                "name": "Production Resources Tagging",
                "description": "Mandatory tags for all production resources",
                "scope": "Production Accounts",
                "enforcement": "Mandatory",
                "status": "Active",
                "required_tags": [
                    {"key": "Environment", "description": "Environment (prod/dev/stage)"},
                    {"key": "Project", "description": "Project identifier"},
                    {"key": "Owner", "description": "Team or owner"},
                    {"key": "CostCenter", "description": "Cost center code"}
                ]
            }
        ]
    
    @staticmethod
    def get_naming_rules() -> List[Dict[str, Any]]:
        """Return naming rules"""
        return [
            {
                "resource_type": "EC2 Instance",
                "pattern": "{project}-{env}-ec2-{purpose}-{counter}",
                "description": "Standard EC2 naming",
                "enforcement": "Mandatory",
                "example": "myapp-prod-ec2-web-001"
            },
            {
                "resource_type": "S3 Bucket",
                "pattern": "{org}-{project}-{env}-{purpose}",
                "description": "S3 bucket naming",
                "enforcement": "Mandatory",
                "example": "acme-myapp-prod-data"
            }
        ]
    
    @staticmethod
    def get_container_images() -> List[Dict[str, Any]]:
        """Return container images"""
        return [
            {
                "name": "api-service",
                "registry": "ECR",
                "latest_version": "2.3.1",
                "total_versions": 45,
                "last_updated": "2024-11-17",
                "size": "245 MB",
                "security_status": "Clean",
                "vulnerabilities": "0 Critical",
                "deployments": 12
            },
            {
                "name": "web-frontend",
                "registry": "ECR",
                "latest_version": "1.8.5",
                "total_versions": 32,
                "last_updated": "2024-11-16",
                "size": "180 MB",
                "security_status": "Warning",
                "vulnerabilities": "1 High, 3 Medium",
                "deployments": 8
            }
        ]
    
    @staticmethod
    def get_iac_modules() -> List[Dict[str, Any]]:
        """Return IaC modules"""
        return [
            {
                "id": "mod-001",
                "name": "vpc-standard",
                "type": "Terraform",
                "version": "2.1.0",
                "category": "Network",
                "description": "Standard VPC with public/private subnets across 3 AZs",
                "author": "Platform Team",
                "downloads": 245,
                "rating": 5
            },
            {
                "id": "mod-002",
                "name": "rds-postgres",
                "type": "Terraform",
                "version": "1.5.0",
                "category": "Database",
                "description": "PostgreSQL RDS with automated backups",
                "author": "Database Team",
                "downloads": 189,
                "rating": 4
            },
            {
                "id": "mod-003",
                "name": "eks-cluster",
                "type": "Terraform",
                "version": "3.2.0",
                "category": "Compute",
                "description": "Production-ready EKS cluster",
                "author": "Container Team",
                "downloads": 312,
                "rating": 5
            }
        ]
    
    @staticmethod
    def get_validation_dashboard() -> Dict[str, Any]:
        """Return validation dashboard data"""
        return {
            "total_validations": 1543,
            "passed": 1189,
            "failed": 234,
            "warnings": 120,
            "pass_rate": 77,
            "security_checks": [
                {"name": "Encryption at Rest", "passed": True, "score": 95},
                {"name": "IAM Policies", "passed": True, "score": 88},
                {"name": "Network Security", "passed": False, "score": 72}
            ],
            "compliance_checks": [
                {"name": "PCI DSS", "passed": True, "score": 82},
                {"name": "HIPAA", "passed": False, "score": 65},
                {"name": "GDPR", "passed": True, "score": 89}
            ]
        }
