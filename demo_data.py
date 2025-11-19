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
    
    # ============= PROVISIONING & DEPLOYMENT DATA =============
    
    @staticmethod
    def get_provisioning_dashboard() -> Dict[str, Any]:
        """Return provisioning dashboard data"""
        return {
            "total_deployments": 342,
            "deployments_this_month": 45,
            "success_rate": 94.5,
            "success_rate_change": 2.3,
            "active_resources": 1547,
            "resources_growth": 23,
            "avg_deploy_time": "18.5 min",
            "time_improvement": "3.2 min",
            "cloud_distribution": [
                {"Cloud": "AWS", "Deployments": 215, "Resources": 892, "Cost": "$12,450"},
                {"Cloud": "Azure", "Deployments": 87, "Resources": 445, "Cost": "$8,320"},
                {"Cloud": "GCP", "Deployments": 40, "Resources": 210, "Cost": "$4,890"}
            ],
            "recent_deployments": [
                {"Application": "API Gateway", "Environment": "Production", "Status": "✅ Success", "Duration": "15 min"},
                {"Application": "Data Pipeline", "Environment": "Staging", "Status": "🔄 In Progress", "Duration": "8 min"},
                {"Application": "Web Frontend", "Environment": "Production", "Status": "✅ Success", "Duration": "12 min"},
                {"Application": "Analytics Service", "Environment": "Development", "Status": "❌ Failed", "Duration": "22 min"}
            ],
            "deployment_trends": [
                {"date": "2024-11-11", "AWS": 28, "Azure": 12, "GCP": 5},
                {"date": "2024-11-12", "AWS": 32, "Azure": 15, "GCP": 7},
                {"date": "2024-11-13", "AWS": 25, "Azure": 10, "GCP": 6},
                {"date": "2024-11-14", "AWS": 30, "Azure": 13, "GCP": 8},
                {"date": "2024-11-15", "AWS": 35, "Azure": 18, "GCP": 9},
                {"date": "2024-11-16", "AWS": 29, "Azure": 14, "GCP": 7},
                {"date": "2024-11-17", "AWS": 36, "Azure": 19, "GCP": 10}
            ]
        }
    
    @staticmethod
    def get_active_deployments() -> List[Dict[str, Any]]:
        """Return active deployments"""
        return [
            {
                "id": "dep-20241118-001",
                "name": "ecommerce-platform-prod",
                "blueprint": "Three-Tier Web Application",
                "cloud": "AWS",
                "region": "us-east-1",
                "environment": "Production",
                "status": "Running",
                "started_at": "2024-11-18 08:30:00",
                "resources_created": 23,
                "resources_total": 23,
                "progress": 100
            },
            {
                "id": "dep-20241118-002",
                "name": "data-analytics-staging",
                "blueprint": "Data Lake Analytics",
                "cloud": "AWS",
                "region": "us-west-2",
                "environment": "Staging",
                "status": "Provisioning",
                "started_at": "2024-11-18 09:15:00",
                "resources_created": 15,
                "resources_total": 28,
                "progress": 54
            },
            {
                "id": "dep-20241118-003",
                "name": "api-backend-dev",
                "blueprint": "Serverless API Backend",
                "cloud": "Azure",
                "region": "eastus",
                "environment": "Development",
                "status": "Running",
                "started_at": "2024-11-18 07:45:00",
                "resources_created": 12,
                "resources_total": 12,
                "progress": 100
            },
            {
                "id": "dep-20241117-045",
                "name": "microservices-prod",
                "blueprint": "Microservices on EKS",
                "cloud": "AWS",
                "region": "eu-west-1",
                "environment": "Production",
                "status": "Updating",
                "started_at": "2024-11-17 22:30:00",
                "resources_created": 34,
                "resources_total": 36,
                "progress": 94
            },
            {
                "id": "dep-20241117-043",
                "name": "ml-pipeline-test",
                "blueprint": "Data Lake Analytics",
                "cloud": "GCP",
                "region": "us-central1",
                "environment": "Development",
                "status": "Failed",
                "started_at": "2024-11-17 20:15:00",
                "resources_created": 8,
                "resources_total": 18,
                "progress": 44
            }
        ]
    
    @staticmethod
    def get_cloud_comparison() -> List[Dict[str, Any]]:
        """Return cloud provider comparison"""
        return [
            {
                "Metric": "Total Services",
                "AWS": "200+",
                "Azure": "200+",
                "GCP": "100+"
            },
            {
                "Metric": "Compute Cost/Hour",
                "AWS": "$0.096",
                "Azure": "$0.098",
                "GCP": "$0.094"
            },
            {
                "Metric": "Storage Cost/GB",
                "AWS": "$0.023",
                "Azure": "$0.020",
                "GCP": "$0.020"
            },
            {
                "Metric": "Global Regions",
                "AWS": "33",
                "Azure": "60+",
                "GCP": "35"
            },
            {
                "Metric": "Compliance Certifications",
                "AWS": "100+",
                "Azure": "90+",
                "GCP": "70+"
            },
            {
                "Metric": "Free Tier Duration",
                "AWS": "12 months",
                "Azure": "12 months",
                "GCP": "Always free"
            }
        ]
    
    @staticmethod
    def get_promotion_rules() -> List[Dict[str, Any]]:
        """Return promotion rules"""
        return [
            {
                "from_env": "Development",
                "to_env": "Staging",
                "trigger": "Automatic on merge",
                "approvers_required": 0,
                "automated_tests": "Unit + Integration",
                "gates": [
                    "All tests passing",
                    "Code coverage > 80%",
                    "No critical vulnerabilities"
                ],
                "rollback_strategy": "Automatic on failure"
            },
            {
                "from_env": "Staging",
                "to_env": "Production",
                "trigger": "Manual approval",
                "approvers_required": 2,
                "automated_tests": "Full suite + Performance",
                "gates": [
                    "All tests passing",
                    "Security scan clean",
                    "Performance benchmarks met",
                    "Change approval obtained"
                ],
                "rollback_strategy": "Blue-green deployment"
            }
        ]
    
    @staticmethod
    def get_pending_promotions() -> List[Dict[str, Any]]:
        """Return pending promotions"""
        return [
            {
                "id": "PR-20241118-001",
                "application": "Payment Service",
                "version": "v2.3.1",
                "from_env": "Staging",
                "to_env": "Production",
                "status": "Pending Approval",
                "requested_by": "John Doe",
                "created_at": "2024-11-18 09:00:00",
                "approvals": 1,
                "approvals_required": 2,
                "tests_status": "✅ Passed",
                "description": "Performance improvements and bug fixes for payment processing"
            },
            {
                "id": "PR-20241118-002",
                "application": "User Authentication",
                "version": "v1.8.0",
                "from_env": "Staging",
                "to_env": "Production",
                "status": "Ready",
                "requested_by": "Jane Smith",
                "created_at": "2024-11-17 16:30:00",
                "approvals": 2,
                "approvals_required": 2,
                "tests_status": "✅ Passed",
                "description": "OAuth 2.0 integration and MFA enhancements"
            },
            {
                "id": "PR-20241117-045",
                "application": "Analytics Dashboard",
                "version": "v3.1.0",
                "from_env": "Development",
                "to_env": "Staging",
                "status": "Testing",
                "requested_by": "Mike Johnson",
                "created_at": "2024-11-17 14:15:00",
                "approvals": 0,
                "approvals_required": 1,
                "tests_status": "🔄 Running",
                "description": "New real-time analytics features and UI improvements"
            }
        ]
    
    @staticmethod
    def get_approval_workflows() -> List[Dict[str, Any]]:
        """Return approval workflows"""
        return [
            {
                "name": "Production Deployment",
                "environment": "Production",
                "required_approvers": 2,
                "approvers": [
                    "Lead Engineer",
                    "DevOps Manager",
                    "Security Officer"
                ],
                "status": "Active",
                "auto_approve_conditions": [
                    "Hotfix tagged",
                    "Security patch"
                ],
                "notification_channels": [
                    "Slack #deployments",
                    "Email to ops-team@company.com",
                    "PagerDuty"
                ],
                "gates": [
                    "All automated tests passed",
                    "Security scan completed",
                    "Change ticket approved",
                    "Rollback plan documented"
                ]
            },
            {
                "name": "Staging Deployment",
                "environment": "Staging",
                "required_approvers": 1,
                "approvers": [
                    "Team Lead",
                    "Senior Engineer"
                ],
                "status": "Active",
                "auto_approve_conditions": [
                    "Development tests passed"
                ],
                "notification_channels": [
                    "Slack #staging-deploys"
                ],
                "gates": [
                    "Unit tests passed",
                    "Integration tests passed"
                ]
            }
        ]
    
    @staticmethod
    def get_promotion_history() -> List[Dict[str, Any]]:
        """Return promotion history"""
        return [
            {
                "Date": "2024-11-18",
                "Application": "Payment Service",
                "From": "Staging",
                "To": "Production",
                "Version": "v2.3.0",
                "Status": "Success",
                "Duration": "12 min"
            },
            {
                "Date": "2024-11-17",
                "Application": "User Auth",
                "From": "Dev",
                "To": "Staging",
                "Version": "v1.8.0",
                "Status": "Success",
                "Duration": "8 min"
            },
            {
                "Date": "2024-11-17",
                "Application": "Analytics",
                "From": "Staging",
                "To": "Production",
                "Version": "v3.0.5",
                "Status": "Rolled Back",
                "Duration": "15 min"
            },
            {
                "Date": "2024-11-16",
                "Application": "API Gateway",
                "From": "Staging",
                "To": "Production",
                "Version": "v4.2.1",
                "Status": "Success",
                "Duration": "10 min"
            },
            {
                "Date": "2024-11-16",
                "Application": "Data Pipeline",
                "From": "Dev",
                "To": "Staging",
                "Version": "v2.1.0",
                "Status": "Failed",
                "Duration": "5 min"
            }
        ]
    
    @staticmethod
    def get_cicd_connections() -> List[Dict[str, Any]]:
        """Return CI/CD connections"""
        return [
            {
                "id": "cicd-001",
                "name": "Jenkins Production",
                "type": "Jenkins",
                "url": "https://jenkins.company.com",
                "status": "Active",
                "pipelines": 23,
                "last_build": "2024-11-18 09:30:00",
                "connected_at": "2024-01-15"
            },
            {
                "id": "cicd-002",
                "name": "GitHub Actions",
                "type": "GitHub Actions",
                "url": "https://github.com/company",
                "status": "Active",
                "pipelines": 45,
                "last_build": "2024-11-18 09:45:00",
                "connected_at": "2024-02-20"
            },
            {
                "id": "cicd-003",
                "name": "GitLab CI/CD",
                "type": "GitLab CI",
                "url": "https://gitlab.company.com",
                "status": "Active",
                "pipelines": 18,
                "last_build": "2024-11-18 08:15:00",
                "connected_at": "2024-03-10"
            },
            {
                "id": "cicd-004",
                "name": "Azure DevOps",
                "type": "Azure DevOps",
                "url": "https://dev.azure.com/company",
                "status": "Inactive",
                "pipelines": 12,
                "last_build": "2024-11-10 14:20:00",
                "connected_at": "2024-04-05"
            }
        ]
    
    @staticmethod
    def get_pipeline_configurations() -> List[Dict[str, Any]]:
        """Return pipeline configurations"""
        return [
            {
                "id": "pipe-001",
                "name": "Payment Service CI/CD",
                "type": "GitHub Actions",
                "repository": "company/payment-service",
                "branch": "main",
                "trigger": "On push",
                "status": "Active",
                "stages": ["Build", "Test", "Security Scan", "Deploy to Dev", "Deploy to Staging"],
                "deploy_target": "AWS EKS",
                "configuration": """name: Payment Service CI/CD

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build
        run: npm run build
      - name: Test
        run: npm test
      - name: Security Scan
        run: npm audit
      - name: Deploy
        run: kubectl apply -f k8s/"""
            },
            {
                "id": "pipe-002",
                "name": "Analytics Dashboard Build",
                "type": "Jenkins",
                "repository": "company/analytics-dashboard",
                "branch": "develop",
                "trigger": "On merge",
                "status": "Active",
                "stages": ["Compile", "Unit Test", "Integration Test", "Package", "Deploy"],
                "deploy_target": "AWS EC2",
                "configuration": """pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'mvn clean package'
            }
        }
        stage('Test') {
            steps {
                sh 'mvn test'
            }
        }
        stage('Deploy') {
            steps {
                sh './deploy.sh'
            }
        }
    }
}"""
            }
        ]
    
    @staticmethod
    def get_build_status() -> Dict[str, Any]:
        """Return build status data"""
        return {
            "total_builds": 1247,
            "success_rate": 92.3,
            "avg_duration": "8.5 min",
            "failed_builds": 15,
            "recent_builds": [
                {
                    "Pipeline": "Payment Service",
                    "Build": "#1523",
                    "Status": "✅ Success",
                    "Duration": "7.2 min",
                    "Branch": "main",
                    "Started": "2024-11-18 09:45:00"
                },
                {
                    "Pipeline": "User Auth",
                    "Build": "#892",
                    "Status": "✅ Success",
                    "Duration": "5.8 min",
                    "Branch": "main",
                    "Started": "2024-11-18 09:30:00"
                },
                {
                    "Pipeline": "Analytics Dashboard",
                    "Build": "#645",
                    "Status": "🔄 Running",
                    "Duration": "3.1 min",
                    "Branch": "develop",
                    "Started": "2024-11-18 09:40:00"
                },
                {
                    "Pipeline": "Data Pipeline",
                    "Build": "#378",
                    "Status": "❌ Failed",
                    "Duration": "2.5 min",
                    "Branch": "feature/v2",
                    "Started": "2024-11-18 09:15:00"
                }
            ],
            "build_trends": [
                {"date": "2024-11-11", "Success": 45, "Failed": 3},
                {"date": "2024-11-12", "Success": 52, "Failed": 4},
                {"date": "2024-11-13", "Success": 48, "Failed": 2},
                {"date": "2024-11-14", "Success": 55, "Failed": 5},
                {"date": "2024-11-15", "Success": 60, "Failed": 3},
                {"date": "2024-11-16", "Success": 51, "Failed": 4},
                {"date": "2024-11-17", "Success": 58, "Failed": 2}
            ]
        }
    
    @staticmethod
    def get_pipeline_templates() -> List[Dict[str, Any]]:
        """Return pipeline templates"""
        return [
            {
                "id": "tmpl-001",
                "name": "Node.js API Pipeline",
                "type": "GitHub Actions",
                "category": "Backend",
                "language": "Node.js",
                "description": "Standard CI/CD for Node.js REST APIs",
                "use_count": 45,
                "template": """name: Node.js CI/CD

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm test
      - run: npm run build"""
            },
            {
                "id": "tmpl-002",
                "name": "Python Data Pipeline",
                "type": "GitLab CI",
                "category": "Data",
                "language": "Python",
                "description": "Data processing pipeline with pytest",
                "use_count": 23,
                "template": """stages:
  - test
  - deploy

test:
  stage: test
  script:
    - pip install -r requirements.txt
    - pytest tests/
  
deploy:
  stage: deploy
  script:
    - python deploy.py
  only:
    - main"""
            },
            {
                "id": "tmpl-003",
                "name": "React Frontend Pipeline",
                "type": "GitHub Actions",
                "category": "Frontend",
                "language": "JavaScript",
                "description": "Build and deploy React applications",
                "use_count": 67,
                "template": """name: React Build

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install
        run: npm install
      - name: Build
        run: npm run build
      - name: Deploy
        run: aws s3 sync build/ s3://bucket-name/"""
            }
        ]
"""
Add these methods to demo_data.py DemoDataProvider class
Copy and paste into demo_data.py after the existing methods
"""

    # ============= ON-DEMAND PROVISIONING & OPERATIONS DATA =============
    
    @staticmethod
    def get_ondemand_dashboard():
        """Return on-demand provisioning dashboard data"""
        return {
            "total_resources": 1547,
            "resources_optimized": 892,
            "optimization_rate": 57.7,
            "monthly_savings": 18450.00,
            "savings_ytd": 187250.00,
            "active_policies": 45,
            "automated_actions": 2341,
            "avg_response_time": "2.3 min",
            "resource_health": [
                {"category": "Compute", "total": 485, "optimized": 312, "savings": "$8,230"},
                {"category": "Storage", "total": 678, "optimized": 412, "savings": "$5,680"},
                {"category": "Database", "total": 234, "optimized": 145, "savings": "$3,240"},
                {"category": "Network", "total": 150, "optimized": 23, "savings": "$1,300"}
            ],
            "optimization_trends": [
                {"month": "May", "Savings": 14200, "Actions": 189},
                {"month": "Jun", "Savings": 15800, "Actions": 215},
                {"month": "Jul", "Savings": 16500, "Actions": 234},
                {"month": "Aug", "Savings": 17200, "Actions": 267},
                {"month": "Sep", "Savings": 17900, "Actions": 289},
                {"month": "Oct", "Savings": 18100, "Actions": 312},
                {"month": "Nov", "Savings": 18450, "Actions": 341}
            ]
        }
    
    @staticmethod
    def get_provisioning_api_configs():
        """Return provisioning API configurations"""
        return [
            {
                "id": "api-001",
                "name": "EC2 Instance Provisioning",
                "endpoint": "/api/v1/provision/ec2",
                "method": "POST",
                "status": "Active",
                "rate_limit": "100/hour",
                "auth_type": "API Key + IAM",
                "avg_response_time": "3.2s",
                "success_rate": 98.5,
                "last_30_days": 1247,
                "description": "Provision EC2 instances with auto-scaling and right-sizing",
                "sample_request": """{
  "instance_type": "t3.medium",
  "ami_id": "ami-0c55b159cbfafe1f0",
  "count": 3,
  "tags": {
    "Environment": "production",
    "Project": "api-gateway"
  },
  "right_sizing": true,
  "auto_scaling": {
    "min": 2,
    "max": 10,
    "target_cpu": 70
  }
}"""
            },
            {
                "id": "api-002",
                "name": "RDS Database Provisioning",
                "endpoint": "/api/v1/provision/rds",
                "method": "POST",
                "status": "Active",
                "rate_limit": "50/hour",
                "auth_type": "API Key + IAM",
                "avg_response_time": "12.5s",
                "success_rate": 99.2,
                "last_30_days": 342,
                "description": "Provision RDS instances with automated backups and monitoring",
                "sample_request": """{
  "engine": "postgres",
  "version": "14.6",
  "instance_class": "db.t3.medium",
  "storage": 100,
  "multi_az": true,
  "backup_retention": 7,
  "auto_minor_version_upgrade": true
}"""
            },
            {
                "id": "api-003",
                "name": "S3 Bucket Provisioning",
                "endpoint": "/api/v1/provision/s3",
                "method": "POST",
                "status": "Active",
                "rate_limit": "200/hour",
                "auth_type": "API Key + IAM",
                "avg_response_time": "1.8s",
                "success_rate": 99.8,
                "last_30_days": 2156,
                "description": "Provision S3 buckets with lifecycle policies and tiering",
                "sample_request": """{
  "bucket_name": "myapp-prod-data-2024",
  "versioning": true,
  "encryption": "AES256",
  "lifecycle_policies": [
    {
      "name": "archive-old-data",
      "transition": "GLACIER",
      "days": 90
    }
  ],
  "intelligent_tiering": true
}"""
            }
        ]
    
    @staticmethod
    def get_guardrail_validations():
        """Return guardrail validation rules"""
        return [
            {
                "id": "gr-001",
                "name": "Security Group Open Ports",
                "category": "Security",
                "severity": "Critical",
                "status": "Active",
                "description": "Block security groups with 0.0.0.0/0 on sensitive ports",
                "blocked_ports": [22, 3389, 1433, 3306, 5432],
                "action": "Block & Alert",
                "violations_prevented": 234,
                "last_triggered": "2024-11-18 08:30:00"
            },
            {
                "id": "gr-002",
                "name": "Unencrypted Storage",
                "category": "Compliance",
                "severity": "High",
                "status": "Active",
                "description": "Prevent creation of unencrypted EBS volumes and S3 buckets",
                "action": "Block & Alert",
                "violations_prevented": 156,
                "last_triggered": "2024-11-18 07:15:00"
            },
            {
                "id": "gr-003",
                "name": "Public S3 Buckets",
                "category": "Security",
                "severity": "Critical",
                "status": "Active",
                "description": "Block public access to S3 buckets by default",
                "action": "Block & Alert",
                "violations_prevented": 89,
                "last_triggered": "2024-11-17 16:45:00"
            },
            {
                "id": "gr-004",
                "name": "Oversized Instances",
                "category": "Cost",
                "severity": "Medium",
                "status": "Active",
                "description": "Alert on instances larger than t3.xlarge without approval",
                "action": "Alert & Require Approval",
                "violations_prevented": 67,
                "last_triggered": "2024-11-18 09:00:00"
            },
            {
                "id": "gr-005",
                "name": "Missing Required Tags",
                "category": "Governance",
                "severity": "Medium",
                "status": "Active",
                "description": "Require Environment, Project, and Owner tags on all resources",
                "required_tags": ["Environment", "Project", "Owner", "CostCenter"],
                "action": "Block",
                "violations_prevented": 445,
                "last_triggered": "2024-11-18 09:45:00"
            }
        ]
    
    @staticmethod
    def get_deployment_templates():
        """Return deployment templates"""
        return [
            {
                "id": "tmpl-dp-001",
                "name": "Auto-Scaling Web Application",
                "category": "Compute",
                "type": "CloudFormation",
                "version": "2.1.0",
                "description": "Web app with ALB, auto-scaling EC2, and RDS",
                "use_count": 78,
                "last_used": "2024-11-18",
                "estimated_time": "15-20 min",
                "estimated_cost": "$850/month",
                "features": [
                    "Auto-scaling (2-10 instances)",
                    "Application Load Balancer",
                    "RDS PostgreSQL Multi-AZ",
                    "CloudWatch monitoring",
                    "Automated backups"
                ]
            },
            {
                "id": "tmpl-dp-002",
                "name": "Serverless API + DynamoDB",
                "category": "Serverless",
                "type": "SAM Template",
                "version": "1.8.0",
                "description": "Lambda-based REST API with DynamoDB",
                "use_count": 92,
                "last_used": "2024-11-18",
                "estimated_time": "8-12 min",
                "estimated_cost": "$120/month",
                "features": [
                    "Lambda functions with auto-scaling",
                    "API Gateway with throttling",
                    "DynamoDB with on-demand capacity",
                    "CloudWatch Logs",
                    "X-Ray tracing"
                ]
            },
            {
                "id": "tmpl-dp-003",
                "name": "Containerized Microservices",
                "category": "Containers",
                "type": "Terraform",
                "version": "3.0.0",
                "description": "ECS Fargate cluster with service mesh",
                "use_count": 45,
                "last_used": "2024-11-17",
                "estimated_time": "25-30 min",
                "estimated_cost": "$1,450/month",
                "features": [
                    "ECS Fargate cluster",
                    "Application Load Balancer",
                    "ECR repositories",
                    "Service discovery",
                    "Auto-scaling policies"
                ]
            }
        ]
    
    @staticmethod
    def get_rightsizing_recommendations():
        """Return compute right-sizing recommendations"""
        return [
            {
                "resource_id": "i-0abc123def456",
                "resource_name": "web-server-prod-01",
                "current_type": "m5.2xlarge",
                "recommended_type": "m5.xlarge",
                "current_cost": "$280/month",
                "projected_cost": "$140/month",
                "monthly_savings": 140.00,
                "annual_savings": 1680.00,
                "cpu_utilization": "15-25%",
                "memory_utilization": "35%",
                "confidence": "High",
                "recommendation_age": "7 days",
                "action_available": True
            },
            {
                "resource_id": "i-0def789ghi012",
                "resource_name": "api-server-prod-02",
                "current_type": "c5.4xlarge",
                "recommended_type": "c5.2xlarge",
                "current_cost": "$490/month",
                "projected_cost": "$245/month",
                "monthly_savings": 245.00,
                "annual_savings": 2940.00,
                "cpu_utilization": "12-18%",
                "memory_utilization": "28%",
                "confidence": "High",
                "recommendation_age": "14 days",
                "action_available": True
            },
            {
                "resource_id": "i-0ghi345jkl678",
                "resource_name": "batch-processor-01",
                "current_type": "r5.large",
                "recommended_type": "t3.medium",
                "current_cost": "$125/month",
                "projected_cost": "$60/month",
                "monthly_savings": 65.00,
                "annual_savings": 780.00,
                "cpu_utilization": "8-12%",
                "memory_utilization": "42%",
                "confidence": "Medium",
                "recommendation_age": "3 days",
                "action_available": True
            }
        ]
    
    @staticmethod
    def get_storage_tiering_policies():
        """Return storage tiering policies"""
        return [
            {
                "id": "tier-001",
                "name": "Application Logs Archival",
                "bucket": "prod-app-logs",
                "status": "Active",
                "objects_managed": "1.2M",
                "total_size": "850 GB",
                "monthly_savings": "$285",
                "rules": [
                    {"name": "Move to IA", "days": 30, "storage_class": "STANDARD_IA"},
                    {"name": "Move to Glacier", "days": 90, "storage_class": "GLACIER"},
                    {"name": "Deep Archive", "days": 365, "storage_class": "DEEP_ARCHIVE"}
                ]
            },
            {
                "id": "tier-002",
                "name": "Database Backups Lifecycle",
                "bucket": "prod-db-backups",
                "status": "Active",
                "objects_managed": "45K",
                "total_size": "2.4 TB",
                "monthly_savings": "$420",
                "rules": [
                    {"name": "Recent backups", "days": 7, "storage_class": "STANDARD"},
                    {"name": "Archive backups", "days": 30, "storage_class": "GLACIER"},
                    {"name": "Expire old", "days": 90, "action": "DELETE"}
                ]
            },
            {
                "id": "tier-003",
                "name": "Media Assets Optimization",
                "bucket": "prod-media-assets",
                "status": "Active",
                "objects_managed": "3.5M",
                "total_size": "15 TB",
                "monthly_savings": "$1,240",
                "rules": [
                    {"name": "Intelligent Tiering", "days": 0, "storage_class": "INTELLIGENT_TIERING"}
                ]
            }
        ]
    
    @staticmethod
    def get_autoscaling_schedules():
        """Return auto-scaling schedules"""
        return [
            {
                "id": "sched-001",
                "name": "Business Hours Scaling",
                "resource_type": "EC2 Auto Scaling",
                "target": "web-app-asg",
                "status": "Active",
                "schedule_type": "Time-based",
                "schedules": [
                    {"time": "08:00", "days": "Mon-Fri", "min": 4, "max": 10, "desired": 6},
                    {"time": "18:00", "days": "Mon-Fri", "min": 2, "max": 6, "desired": 3},
                    {"time": "00:00", "days": "Sat-Sun", "min": 2, "max": 4, "desired": 2}
                ],
                "monthly_savings": "$850"
            },
            {
                "id": "sched-002",
                "name": "Dev Environment Night Shutdown",
                "resource_type": "EC2 Instances",
                "target": "dev-*",
                "status": "Active",
                "schedule_type": "Stop/Start",
                "schedules": [
                    {"time": "19:00", "days": "Mon-Fri", "action": "Stop"},
                    {"time": "07:00", "days": "Mon-Fri", "action": "Start"},
                    {"time": "19:00", "days": "Fri", "action": "Stop (weekend)"}
                ],
                "monthly_savings": "$1,240"
            },
            {
                "id": "sched-003",
                "name": "RDS Development Instances",
                "resource_type": "RDS",
                "target": "dev-databases",
                "status": "Active",
                "schedule_type": "Stop/Start",
                "schedules": [
                    {"time": "20:00", "days": "Daily", "action": "Stop"},
                    {"time": "06:00", "days": "Mon-Fri", "action": "Start"}
                ],
                "monthly_savings": "$680"
            }
        ]
    
    @staticmethod
    def get_patch_automation_status():
        """Return patch automation status using SSM"""
        return {
            "total_instances": 485,
            "patch_compliant": 412,
            "patch_pending": 58,
            "patch_failed": 15,
            "compliance_rate": 84.9,
            "last_patch_window": "2024-11-15",
            "next_patch_window": "2024-11-22",
            "maintenance_windows": [
                {
                    "name": "Production Patching",
                    "schedule": "Every Friday 02:00 AM",
                    "duration": "4 hours",
                    "target": "Production instances",
                    "patch_baseline": "AmazonLinux2-Default",
                    "last_run": "2024-11-15 02:00",
                    "status": "Success",
                    "instances_patched": 156
                },
                {
                    "name": "Development Patching",
                    "schedule": "Every Tuesday 20:00 PM",
                    "duration": "2 hours",
                    "target": "Development instances",
                    "patch_baseline": "Custom-Dev-Baseline",
                    "last_run": "2024-11-12 20:00",
                    "status": "Success",
                    "instances_patched": 89
                }
            ],
            "recent_patches": [
                {"Instance": "web-prod-01", "Patch": "kernel-5.10.0", "Status": "✅ Installed", "Date": "2024-11-15"},
                {"Instance": "api-prod-02", "Patch": "openssl-1.1.1", "Status": "✅ Installed", "Date": "2024-11-15"},
                {"Instance": "db-prod-01", "Patch": "postgresql-14.6", "Status": "🔄 Pending Reboot", "Date": "2024-11-15"},
                {"Instance": "app-prod-03", "Patch": "nginx-1.22.1", "Status": "❌ Failed", "Date": "2024-11-15"}
            ]
        }
    
    @staticmethod
    def get_drift_detection_results():
        """Return drift detection results"""
        return [
            {
                "stack_name": "production-web-app",
                "stack_id": "stack-prod-001",
                "last_check": "2024-11-18 08:00:00",
                "drift_status": "DRIFTED",
                "drifted_resources": 3,
                "total_resources": 24,
                "drift_details": [
                    {
                        "resource": "WebServerSecurityGroup",
                        "type": "AWS::EC2::SecurityGroup",
                        "property": "IpPermissions",
                        "expected": "Port 443 only",
                        "actual": "Ports 443, 8080, 9000",
                        "severity": "High"
                    },
                    {
                        "resource": "AppLoadBalancer",
                        "type": "AWS::ElasticLoadBalancingV2::LoadBalancer",
                        "property": "Tags",
                        "expected": "Environment=prod",
                        "actual": "Missing tag",
                        "severity": "Low"
                    }
                ],
                "auto_remediate": True
            },
            {
                "stack_name": "staging-data-pipeline",
                "stack_id": "stack-stage-002",
                "last_check": "2024-11-18 07:30:00",
                "drift_status": "IN_SYNC",
                "drifted_resources": 0,
                "total_resources": 18,
                "drift_details": [],
                "auto_remediate": False
            },
            {
                "stack_name": "dev-microservices",
                "stack_id": "stack-dev-003",
                "last_check": "2024-11-18 06:00:00",
                "drift_status": "DRIFTED",
                "drifted_resources": 1,
                "total_resources": 32,
                "drift_details": [
                    {
                        "resource": "ECSTaskDefinition",
                        "type": "AWS::ECS::TaskDefinition",
                        "property": "Memory",
                        "expected": "2048",
                        "actual": "4096",
                        "severity": "Medium"
                    }
                ],
                "auto_remediate": True
            }
        ]
    
    @staticmethod
    def get_backup_recovery_status():
        """Return backup and recovery management status"""
        return {
            "total_protected_resources": 342,
            "backup_plans": 15,
            "total_backup_size": "18.5 TB",
            "monthly_backup_cost": "$1,245",
            "recovery_point_objective": "1 hour",
            "recovery_time_objective": "4 hours",
            "backup_compliance": 96.8,
            "backup_plans_summary": [
                {
                    "name": "Production Databases",
                    "resources": 45,
                    "frequency": "Every 6 hours",
                    "retention": "30 days",
                    "backup_vault": "prod-db-vault",
                    "encrypted": True,
                    "cross_region": True,
                    "last_backup": "2024-11-18 06:00:00",
                    "status": "✅ Healthy"
                },
                {
                    "name": "Application Servers",
                    "resources": 156,
                    "frequency": "Daily at 02:00",
                    "retention": "14 days",
                    "backup_vault": "prod-ec2-vault",
                    "encrypted": True,
                    "cross_region": False,
                    "last_backup": "2024-11-18 02:00:00",
                    "status": "✅ Healthy"
                },
                {
                    "name": "EFS File Systems",
                    "resources": 12,
                    "frequency": "Daily at 01:00",
                    "retention": "7 days",
                    "backup_vault": "prod-efs-vault",
                    "encrypted": True,
                    "cross_region": False,
                    "last_backup": "2024-11-18 01:00:00",
                    "status": "✅ Healthy"
                }
            ],
            "recent_recoveries": [
                {"Resource": "prod-db-primary", "Type": "RDS", "Date": "2024-11-10", "Duration": "35 min", "Status": "✅ Success"},
                {"Resource": "web-server-03", "Type": "EC2", "Date": "2024-11-08", "Duration": "18 min", "Status": "✅ Success"},
                {"Resource": "data-volume-01", "Type": "EBS", "Date": "2024-11-05", "Duration": "12 min", "Status": "✅ Success"}
            ]
        }
    
    @staticmethod
    def get_lifecycle_hooks():
        """Return lifecycle hooks configuration"""
        return [
            {
                "id": "hook-001",
                "name": "Instance Launch Initialization",
                "auto_scaling_group": "web-app-asg",
                "lifecycle_transition": "autoscaling:EC2_INSTANCE_LAUNCHING",
                "default_result": "CONTINUE",
                "heartbeat_timeout": 300,
                "status": "Active",
                "actions": [
                    "Install monitoring agents",
                    "Register with service discovery",
                    "Run health checks",
                    "Update DNS records"
                ],
                "notifications": "SNS: ops-team",
                "executions_30d": 145
            },
            {
                "id": "hook-002",
                "name": "Instance Termination Cleanup",
                "auto_scaling_group": "web-app-asg",
                "lifecycle_transition": "autoscaling:EC2_INSTANCE_TERMINATING",
                "default_result": "CONTINUE",
                "heartbeat_timeout": 300,
                "status": "Active",
                "actions": [
                    "Deregister from load balancer",
                    "Drain active connections",
                    "Upload logs to S3",
                    "Send termination metrics"
                ],
                "notifications": "SNS: ops-team",
                "executions_30d": 132
            },
            {
                "id": "hook-003",
                "name": "Container Task Launch",
                "auto_scaling_group": "ecs-service-asg",
                "lifecycle_transition": "autoscaling:EC2_INSTANCE_LAUNCHING",
                "default_result": "CONTINUE",
                "heartbeat_timeout": 180,
                "status": "Active",
                "actions": [
                    "Pull latest container images",
                    "Initialize ECS agent",
                    "Join ECS cluster"
                ],
                "notifications": "SNS: container-team",
                "executions_30d": 78
            }
        ]
    
    # ==================== FINOPS MODULE DATA ====================
    
    @staticmethod
    def get_finops_overview_data():
        """Return FinOps overview data"""
        return {
            "monthly_spend": 234567,
            "budget_utilization": 78,
            "cost_savings": 45890,
            "anomalies_detected": 3,
            "ri_coverage": 67
        }
    
    @staticmethod
    def get_tag_cost_data():
        """Return tag-based cost tracking data"""
        return {
            "tag_coverage": 94.3,
            "untagged_resources": 23,
            "untagged_cost": 4567,
            "cost_centers": 12
        }
    
    @staticmethod
    def get_budget_policies():
        """Return budget policies"""
        return [
            {
                "name": "Production Infrastructure",
                "period": "Monthly",
                "budget": 150000,
                "actual": 145890,
                "forecast": 148200,
                "status": "Warning"
            },
            {
                "name": "Development Environments",
                "period": "Monthly",
                "budget": 40000,
                "actual": 32450,
                "forecast": 35600,
                "status": "Healthy"
            }
        ]
    
    @staticmethod
    def get_cost_forecast_data():
        """Return cost forecasting data"""
        return {
            "current_month_forecast": 298450,
            "confidence": 87,
            "q4_forecast": 892340,
            "annual_projection": 3200000
        }
    
    @staticmethod
    def get_spot_instance_data():
        """Return spot instance data"""
        return {
            "spot_instances": 234,
            "monthly_savings": 18900,
            "interruption_rate": 2.3,
            "avg_discount": 72,
            "spot_coverage": 45
        }
    
    @staticmethod
    def get_cost_anomalies():
        """Return cost anomalies"""
        return [
            {
                "detected": "2024-11-18 13:45",
                "service": "RDS",
                "resource": "prod-analytics-db",
                "anomaly": "+140% spike",
                "baseline": "$145/day",
                "current": "$348/day",
                "severity": "High"
            }
        ]
    
    @staticmethod
    def get_ri_recommendations():
        """Return RI/SP recommendations"""
        return [
            {
                "type": "EC2 RI",
                "instance_type": "m5.2xlarge",
                "quantity": 12,
                "monthly_savings": 2340,
                "annual_savings": 28080,
                "confidence": "High"
            }
        ]
    
    @staticmethod
    def get_use_cases():
        """Return use case tracking data"""
        return [
            {
                "name": "Mobile App Backend",
                "category": "Customer-Facing",
                "monthly_cost": 34560,
                "resources": 156,
                "business_value": "High"
            }
        ]
    # ===== POLICY & GUARDRAILS MODULE DATA =====
    
    @staticmethod
    def get_policy_activities():
        """Return policy activity log"""
        return [
            {
                "policy": "Production Tagging Policy",
                "resource": "i-abc123def456",
                "action": "Tag validation failed",
                "status": "Non-Compliant",
                "user": "john.doe@company.com",
                "timestamp": "2024-11-18 14:23:45"
            },
            {
                "policy": "EC2 Naming Convention",
                "resource": "prod-web-app-01",
                "action": "Name validated successfully",
                "status": "Compliant",
                "user": "sarah.smith@company.com",
                "timestamp": "2024-11-18 14:15:32"
            },
            {
                "policy": "S3 Encryption Policy",
                "resource": "my-data-bucket-2023",
                "action": "Encryption enabled automatically",
                "status": "Compliant",
                "user": "system",
                "timestamp": "2024-11-18 13:58:12"
            },
            {
                "policy": "VPC Quota Limit",
                "resource": "vpc-12345",
                "action": "Quota threshold warning",
                "status": "Warning",
                "user": "system",
                "timestamp": "2024-11-18 13:45:00"
            },
            {
                "policy": "Cost Budget Policy",
                "resource": "Account: 123456789012",
                "action": "Budget threshold exceeded",
                "status": "Non-Compliant",
                "user": "system",
                "timestamp": "2024-11-18 13:30:21"
            }
        ]
    
    @staticmethod
    def get_policy_as_code():
        """Return policy as code definitions"""
        return [
            {
                "id": "pol-001",
                "name": "Production Tagging Policy",
                "version": "2.1.0",
                "type": "Tag Policy",
                "language": "OPA (Rego)",
                "status": "Active",
                "scope": "Organization",
                "author": "Cloud Governance Team",
                "last_updated": "2024-11-15",
                "resources_affected": "1,234",
                "description": "Enforces mandatory tags for all production resources",
                "policy_code": '''package aws.tagging

deny[msg] {
    input.resource_type == "aws_instance"
    not input.tags.Environment
    msg = "EC2 instances must have Environment tag"
}

deny[msg] {
    input.resource_type == "aws_instance"
    not input.tags.Owner
    msg = "EC2 instances must have Owner tag"
}

deny[msg] {
    input.resource_type == "aws_instance"
    not input.tags.CostCenter
    msg = "EC2 instances must have CostCenter tag"
}'''
            },
            {
                "id": "pol-002",
                "name": "EC2 Naming Convention",
                "version": "1.5.0",
                "type": "Naming Policy",
                "language": "Cedar",
                "status": "Active",
                "scope": "Production OU",
                "author": "Platform Team",
                "last_updated": "2024-11-10",
                "resources_affected": "456",
                "description": "Enforces naming standards for EC2 instances",
                "policy_code": '''permit(
    principal,
    action == CreateInstance,
    resource
) when {
    resource.name matches "^(prod|dev|stage)-[a-z0-9-]+-\\d{2}$"
};'''
            },
            {
                "id": "pol-003",
                "name": "S3 Encryption Enforcement",
                "version": "3.0.0",
                "type": "Security Policy",
                "language": "Python",
                "status": "Active",
                "scope": "All Accounts",
                "author": "Security Team",
                "last_updated": "2024-11-12",
                "resources_affected": "892",
                "description": "Requires encryption for all S3 buckets",
                "policy_code": '''def check_s3_encryption(bucket):
    if not bucket.get('ServerSideEncryptionConfiguration'):
        return {
            'compliant': False,
            'message': 'S3 bucket must have encryption enabled'
        }
    return {'compliant': True}'''
            },
            {
                "id": "pol-004",
                "name": "RDS Multi-AZ Requirement",
                "version": "1.2.0",
                "type": "Compliance Policy",
                "language": "JSON Schema",
                "status": "Active",
                "scope": "Production Accounts",
                "author": "Database Team",
                "last_updated": "2024-11-08",
                "resources_affected": "123",
                "description": "Enforces Multi-AZ for production RDS instances",
                "policy_code": '''{
  "type": "object",
  "properties": {
    "MultiAZ": {
      "type": "boolean",
      "const": true
    }
  },
  "required": ["MultiAZ"]
}'''
            }
        ]
    
    @staticmethod
    def get_policy_versions():
        """Return policy version history"""
        return [
            {
                "version": "2.1.0",
                "commit_message": "Added CostCenter tag requirement",
                "author": "alice.johnson",
                "date": "2024-11-15 10:23:45",
                "branch": "main",
                "changes": "3 files changed, 45 insertions, 12 deletions",
                "status": "Deployed",
                "diff": '''+ deny[msg] {
+     input.resource_type == "aws_instance"
+     not input.tags.CostCenter
+     msg = "EC2 instances must have CostCenter tag"
+ }'''
            },
            {
                "version": "2.0.1",
                "commit_message": "Fixed regex pattern for naming validation",
                "author": "bob.smith",
                "date": "2024-11-12 14:45:20",
                "branch": "main",
                "changes": "1 file changed, 5 insertions, 3 deletions",
                "status": "Deployed",
                "diff": '''- resource.name matches "^(prod|dev)-[a-z0-9-]+$"
+ resource.name matches "^(prod|dev|stage)-[a-z0-9-]+-\\d{2}$"'''
            },
            {
                "version": "2.0.0",
                "commit_message": "Major update: Added multi-cloud support",
                "author": "carol.williams",
                "date": "2024-11-05 09:15:30",
                "branch": "main",
                "changes": "8 files changed, 120 insertions, 45 deletions",
                "status": "Deployed",
                "diff": '''+ # Multi-cloud policy support
+ package multicloud.tagging
+ import data.aws.tagging
+ import data.azure.tagging
+ import data.gcp.tagging'''
            }
        ]
    
    @staticmethod
    def get_cross_cloud_mappings():
        """Return cross-cloud policy mappings"""
        return [
            {
                "policy_name": "Encryption at Rest",
                "description": "Enforce encryption for all storage resources",
                "aws_implementation": '''# AWS - S3 Encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "example" {
  bucket = aws_s3_bucket.example.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}''',
                "azure_implementation": '''# Azure - Storage Account Encryption
resource "azurerm_storage_account" "example" {
  name                     = "storageaccount"
  resource_group_name      = azurerm_resource_group.example.name
  location                 = azurerm_resource_group.example.location
  account_tier             = "Standard"
  account_replication_type = "GRS"
  
  enable_https_traffic_only = true
  min_tls_version          = "TLS1_2"
}''',
                "gcp_implementation": '''# GCP - Cloud Storage Encryption
resource "google_storage_bucket" "example" {
  name     = "example-bucket"
  location = "US"
  
  encryption {
    default_kms_key_name = google_kms_crypto_key.key.id
  }
}''',
                "aws_status": "Synced",
                "azure_status": "Synced",
                "gcp_status": "Synced"
            },
            {
                "policy_name": "Network Segmentation",
                "description": "Enforce network isolation between environments",
                "aws_implementation": '''# AWS - VPC with Private Subnets
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  enable_dns_hostnames = true
  tags = {
    Environment = "production"
  }
}''',
                "azure_implementation": '''# Azure - Virtual Network
resource "azurerm_virtual_network" "main" {
  name                = "production-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
}''',
                "gcp_implementation": '''# GCP - VPC Network
resource "google_compute_network" "main" {
  name                    = "production-vpc"
  auto_create_subnetworks = false
}''',
                "aws_status": "Synced",
                "azure_status": "Synced",
                "gcp_status": "Pending"
            },
            {
                "policy_name": "Mandatory Tagging",
                "description": "Require environment, owner, and cost center tags",
                "aws_implementation": '''# AWS - Tag Policy (SCP)
{
  "tags": {
    "Environment": {"tag_key": {"@@assign": "Environment"}},
    "Owner": {"tag_key": {"@@assign": "Owner"}},
    "CostCenter": {"tag_key": {"@@assign": "CostCenter"}}
  }
}''',
                "azure_implementation": '''# Azure - Policy Assignment
resource "azurerm_resource_group_policy_assignment" "tags" {
  name                 = "mandatory-tags"
  resource_group_id    = azurerm_resource_group.example.id
  policy_definition_id = azurerm_policy_definition.tags.id
}''',
                "gcp_implementation": '''# GCP - Organization Policy
resource "google_organization_policy" "tags" {
  org_id     = var.org_id
  constraint = "constraints/iam.allowedPolicyMemberDomains"
  
  list_policy {
    allow {
      values = ["organization:${var.org_id}"]
    }
  }
}''',
                "aws_status": "Synced",
                "azure_status": "Synced",
                "gcp_status": "Synced"
            }
        ]
    
    @staticmethod
    def get_sync_history():
        """Return policy sync history"""
        return [
            {
                "policy": "Encryption at Rest",
                "clouds": "AWS, Azure, GCP",
                "timestamp": "2024-11-18 14:30:00",
                "duration": "45s",
                "status": "Success",
                "resources_updated": "347"
            },
            {
                "policy": "Network Segmentation",
                "clouds": "AWS, Azure",
                "timestamp": "2024-11-18 13:15:22",
                "duration": "1m 12s",
                "status": "Success",
                "resources_updated": "156"
            },
            {
                "policy": "Mandatory Tagging",
                "clouds": "AWS, Azure, GCP",
                "timestamp": "2024-11-18 12:45:10",
                "duration": "2m 34s",
                "status": "Failed",
                "resources_updated": "0",
                "error": "GCP API rate limit exceeded"
            },
            {
                "policy": "MFA Enforcement",
                "clouds": "AWS, Azure",
                "timestamp": "2024-11-18 11:30:45",
                "duration": "38s",
                "status": "Success",
                "resources_updated": "89"
            },
            {
                "policy": "Backup Policy",
                "clouds": "AWS",
                "timestamp": "2024-11-18 10:20:15",
                "duration": "1m 05s",
                "status": "Success",
                "resources_updated": "234"
            }
        ]
    
    @staticmethod
    def get_tag_enforcement_policies():
        """Return tag enforcement policies"""
        return [
            {
                "name": "Production Resources Tagging",
                "scope": "Production Accounts",
                "enforcement": "Mandatory",
                "status": "Active",
                "resource_types": "EC2, RDS, S3, Lambda",
                "created": "2024-01-15",
                "updated": "2024-11-10",
                "required_tags": [
                    {"key": "Environment", "description": "Environment (prod/dev/stage)", "pattern": "^(prod|production|dev|development|stage|staging)$"},
                    {"key": "Owner", "description": "Team or individual owner", "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"},
                    {"key": "CostCenter", "description": "Cost center code", "pattern": "^CC-[0-9]{4}$"},
                    {"key": "Project", "description": "Project identifier", "pattern": "^[A-Z]{2,4}-[0-9]{3}$"}
                ],
                "optional_tags": [
                    {"key": "Description", "description": "Resource description"},
                    {"key": "Backup", "description": "Backup policy (yes/no)"}
                ]
            },
            {
                "name": "Cost Allocation Tagging",
                "scope": "All Accounts",
                "enforcement": "Mandatory",
                "status": "Active",
                "resource_types": "All",
                "created": "2024-02-01",
                "updated": "2024-10-15",
                "required_tags": [
                    {"key": "CostCenter", "description": "Cost allocation code", "pattern": "^CC-[0-9]{4}$"},
                    {"key": "BusinessUnit", "description": "Business unit", "pattern": "^(Engineering|Sales|Marketing|Finance|Operations)$"},
                    {"key": "Application", "description": "Application name", "pattern": ".*"}
                ],
                "optional_tags": [
                    {"key": "SubProject", "description": "Sub-project identifier"}
                ]
            },
            {
                "name": "Compliance Tagging",
                "scope": "Regulated Accounts",
                "enforcement": "Mandatory",
                "status": "Active",
                "resource_types": "EC2, RDS, S3",
                "created": "2024-03-10",
                "updated": "2024-11-05",
                "required_tags": [
                    {"key": "DataClassification", "description": "Data sensitivity level", "pattern": "^(Public|Internal|Confidential|Restricted)$"},
                    {"key": "Compliance", "description": "Compliance frameworks", "pattern": "^(PCI-DSS|HIPAA|SOC2|GDPR)$"},
                    {"key": "DataRetention", "description": "Retention period in days", "pattern": "^[0-9]{1,4}$"}
                ],
                "optional_tags": []
            }
        ]
    
    @staticmethod
    def get_naming_enforcement_rules():
        """Return naming convention rules"""
        return [
            {
                "resource_type": "EC2 Instance",
                "pattern": "{env}-{app}-{type}-{seq}",
                "example": "prod-web-app-01",
                "enforcement": "Mandatory",
                "status": "Active",
                "scope": "All Accounts",
                "violations": "23",
                "components": [
                    {"part": "{env}", "description": "Environment: prod, dev, stage"},
                    {"part": "{app}", "description": "Application name: 3-20 lowercase alphanumeric"},
                    {"part": "{type}", "description": "Type: web, app, db, cache"},
                    {"part": "{seq}", "description": "Sequence: 01-99"}
                ]
            },
            {
                "resource_type": "S3 Bucket",
                "pattern": "{org}-{env}-{purpose}-{region}",
                "example": "acme-prod-data-us-east-1",
                "enforcement": "Mandatory",
                "status": "Active",
                "scope": "All Accounts",
                "violations": "12",
                "components": [
                    {"part": "{org}", "description": "Organization prefix: 2-10 lowercase"},
                    {"part": "{env}", "description": "Environment: prod, dev, stage"},
                    {"part": "{purpose}", "description": "Purpose: data, logs, backup, static"},
                    {"part": "{region}", "description": "AWS region identifier"}
                ]
            },
            {
                "resource_type": "RDS Instance",
                "pattern": "{env}-{app}-{dbtype}-{role}",
                "example": "prod-api-postgres-primary",
                "enforcement": "Mandatory",
                "status": "Active",
                "scope": "Production Accounts",
                "violations": "5",
                "components": [
                    {"part": "{env}", "description": "Environment: prod, dev, stage"},
                    {"part": "{app}", "description": "Application name"},
                    {"part": "{dbtype}", "description": "Database type: postgres, mysql, oracle"},
                    {"part": "{role}", "description": "Role: primary, replica, standby"}
                ]
            },
            {
                "resource_type": "Lambda Function",
                "pattern": "{env}-{service}-{function}",
                "example": "prod-orders-process-payment",
                "enforcement": "Advisory",
                "status": "Active",
                "scope": "All Accounts",
                "violations": "45",
                "components": [
                    {"part": "{env}", "description": "Environment: prod, dev, stage"},
                    {"part": "{service}", "description": "Service name: 3-20 lowercase"},
                    {"part": "{function}", "description": "Function purpose: descriptive verb-noun"}
                ]
            }
        ]
    
    @staticmethod
    def get_placement_rules():
        """Return resource placement rules"""
        return [
            {
                "name": "Production Workload Placement",
                "description": "Production workloads must be deployed in approved regions with multi-AZ support",
                "resource_type": "EC2, RDS, EKS",
                "environment": "Production",
                "enforcement": "Mandatory",
                "priority": "High",
                "allowed_regions": ["us-east-1", "us-west-2", "eu-west-1"],
                "restrictions": [
                    "Must span at least 2 availability zones",
                    "Database instances require Multi-AZ enabled",
                    "No single points of failure"
                ]
            },
            {
                "name": "Data Residency - EU",
                "description": "EU customer data must remain within EU regions",
                "resource_type": "S3, RDS, DynamoDB",
                "environment": "All",
                "enforcement": "Mandatory",
                "priority": "Critical",
                "allowed_regions": ["eu-west-1", "eu-central-1", "eu-north-1"],
                "restrictions": [
                    "Data replication limited to EU regions only",
                    "Encryption required for data at rest",
                    "GDPR compliance required"
                ]
            },
            {
                "name": "Development Environment Placement",
                "description": "Non-production workloads in cost-optimized regions",
                "resource_type": "All",
                "environment": "Development, Staging",
                "enforcement": "Advisory",
                "priority": "Low",
                "allowed_regions": ["us-east-1", "us-east-2", "ap-south-1"],
                "restrictions": [
                    "Use spot instances where possible",
                    "Single AZ deployment allowed",
                    "Shutdown during off-hours"
                ]
            },
            {
                "name": "PCI-DSS Workload Isolation",
                "description": "PCI-DSS workloads in dedicated accounts and regions",
                "resource_type": "All payment-processing",
                "environment": "Production",
                "enforcement": "Mandatory",
                "priority": "Critical",
                "allowed_regions": ["us-east-1", "eu-west-1"],
                "restrictions": [
                    "Dedicated VPCs with no shared resources",
                    "Network segmentation from non-PCI workloads",
                    "Enhanced logging and monitoring required",
                    "Quarterly compliance audits"
                ]
            }
        ]
    
    @staticmethod
    def get_quota_status():
        """Return service quota status"""
        return [
            {
                "service": "EC2",
                "quota_name": "Running On-Demand Instances",
                "region": "us-east-1",
                "account": "123456789012",
                "current": 945,
                "limit": 1000,
                "growth_rate": "+5%/week",
                "days_to_limit": "18 days"
            },
            {
                "service": "VPC",
                "quota_name": "VPCs per Region",
                "region": "us-east-1",
                "account": "123456789012",
                "current": 4,
                "limit": 5,
                "growth_rate": "+0.5/month",
                "days_to_limit": "45 days"
            },
            {
                "service": "RDS",
                "quota_name": "DB Instances",
                "region": "us-east-1",
                "account": "123456789012",
                "current": 92,
                "limit": 100,
                "growth_rate": "+3%/month",
                "days_to_limit": "62 days"
            },
            {
                "service": "Lambda",
                "quota_name": "Concurrent Executions",
                "region": "us-east-1",
                "account": "123456789012",
                "current": 850,
                "limit": 1000,
                "growth_rate": "+8%/week",
                "days_to_limit": "12 days"
            },
            {
                "service": "EBS",
                "quota_name": "Snapshot Copy Requests",
                "region": "us-east-1",
                "account": "123456789012",
                "current": 3,
                "limit": 5,
                "growth_rate": "+1/month",
                "days_to_limit": "120 days"
            },
            {
                "service": "ELB",
                "quota_name": "Application Load Balancers",
                "region": "us-west-2",
                "account": "123456789012",
                "current": 18,
                "limit": 20,
                "growth_rate": "+2/quarter",
                "days_to_limit": "90 days"
            }
        ]
    
    @staticmethod
    def get_quota_requests():
        """Return quota increase request history"""
        return [
            {
                "service": "EC2",
                "quota": "Running On-Demand Instances",
                "requested": "2000",
                "status": "Approved",
                "requester": "john.doe@company.com",
                "submitted_date": "2024-11-10",
                "approved_date": "2024-11-12",
                "case_id": "AWS-CASE-12345678"
            },
            {
                "service": "VPC",
                "quota": "VPCs per Region",
                "requested": "10",
                "status": "Pending",
                "requester": "sarah.smith@company.com",
                "submitted_date": "2024-11-15",
                "approved_date": "-",
                "case_id": "AWS-CASE-87654321"
            },
            {
                "service": "Lambda",
                "quota": "Concurrent Executions",
                "requested": "3000",
                "status": "Approved",
                "requester": "mike.johnson@company.com",
                "submitted_date": "2024-11-08",
                "approved_date": "2024-11-09",
                "case_id": "AWS-CASE-11223344"
            },
            {
                "service": "RDS",
                "quota": "DB Instances",
                "requested": "150",
                "status": "Rejected",
                "requester": "alice.williams@company.com",
                "submitted_date": "2024-11-05",
                "approved_date": "-",
                "case_id": "AWS-CASE-99887766"
            },
            {
                "service": "S3",
                "quota": "Buckets per Account",
                "requested": "200",
                "status": "Pending",
                "requester": "bob.brown@company.com",
                "submitted_date": "2024-11-17",
                "approved_date": "-",
                "case_id": "AWS-CASE-55443322"
            }
        ]
