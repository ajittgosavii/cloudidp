# CloudIDP - AWS Infrastructure Development Platform

**Enterprise-Grade AWS Cloud Governance & Automation Framework**

Version 2.0.0 - AWS-Only Edition

---

## 📋 Overview

CloudIDP is a comprehensive AWS infrastructure development and governance platform designed for enterprise-scale cloud operations. It provides end-to-end capabilities for designing, provisioning, operating, and optimizing AWS infrastructure with built-in compliance, security, and cost management.

### Key Features

- **Design & Planning**: Blueprint library, architecture templates, AWS service selection
- **Provisioning & Deployment**: Automated infrastructure provisioning with CloudFormation/Terraform
- **On-Demand Operations**: 14 comprehensive operational capabilities including rightsizing, autoscaling, patch automation, drift detection, and more
- **FinOps**: Cost optimization, budget management, savings recommendations
- **Security & Compliance**: Multi-framework compliance, security scanning, vulnerability management
- **Policy & Guardrails**: Pre-deployment validation, tag policies, naming conventions
- **Abstraction & Reusability**: Infrastructure templates, modules, and patterns
- **Developer Experience**: Self-service portals, API access, automation tools
- **Observability**: Monitoring, logging, alerting integration

---

## 🚀 What's New in Version 2.0.0

### ✅ Enterprise-Grade Refactoring

1. **AWS-Only Focus**: Removed all Azure and GCP references for production clarity
2. **No Hardcoded Data**: All AWS account IDs and sensitive data moved to configuration
3. **Consolidated Features**: Merged duplicate modules into comprehensive units
4. **Clean Codebase**: Removed 30+ development utility files
5. **Enhanced Security**: Configuration-based approach for all AWS resources

### 🔧 Technical Improvements

- **Merged On-Demand Operations**: Combined 14 operational features into single module
- **Configuration Management**: Centralized AWS account configuration with validation
- **Removed Modules**: 
  - module_08_multicloud_hybrid (multi-cloud support - AWS only now)
  - ondemand_operations_part2 (merged into ondemand_operations)
  - All development/utility scripts (20+ files)
  
### 📊 Metrics

- **Files Processed**: 41 core modules
- **Files Removed**: 17 development/utility files  
- **Hardcoded IDs Replaced**: 28 instances
- **Multi-cloud References Removed**: 40 instances

---

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8 or higher
- AWS Account with appropriate permissions
- (Optional) Anthropic API key for AI-powered features

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Configure AWS Credentials

CloudIDP requires AWS configuration. You have two options:

#### Option A: Environment Variables (Recommended for Production)

```bash
export AWS_ACCOUNT_ID="your-12-digit-account-id"
export AWS_ORG_ID="your-organization-id"
export AWS_REGION="us-east-1"
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
```

#### Option B: AWS CLI Configuration

```bash
aws configure
```

Ensure your AWS credentials have the following permissions:
- EC2 (Read/Write)
- RDS (Read)
- S3 (Read/Write)
- CloudFormation (Read/Write)
- Cost Explorer (Read)
- Organizations (Read - if using AWS Organizations)
- Systems Manager (Read/Write)

### Step 3: Update Configuration

Edit `config.py` and update the AWS_CONFIG section:

```python
AWS_CONFIG = {
    "default_region": "us-east-1",
    "account_id_placeholder": "YOUR_AWS_ACCOUNT_ID",  # Replace with your account ID
    "organization_id_placeholder": "YOUR_ORG_ID"      # Replace with your org ID
}
```

### Step 4: Run the Application

```bash
streamlit run streamlit_app.py
```

The application will be available at `http://localhost:8501`

---

## 📖 Usage Guide

### Demo Mode vs Live Mode

CloudIDP supports two operational modes:

#### Demo Mode (Default)
- Uses sample data for demonstration
- No AWS credentials required
- Perfect for testing and learning
- Toggle using the sidebar

#### Live Mode
- Connects to your real AWS account
- Requires proper AWS configuration
- Real-time data from your infrastructure
- Full operational capabilities

**To switch modes**: Use the toggle in the application sidebar

### Module Overview

#### 1. Design & Planning
Create and manage infrastructure blueprints, select AWS services, and plan deployments.

**Key Features**:
- Blueprint library with pre-built templates
- AWS service selector
- Cost estimation
- Architecture diagramming

#### 2. Provisioning & Deployment
Automate infrastructure provisioning using Infrastructure as Code.

**Key Features**:
- CloudFormation/Terraform template deployment
- Environment management (Dev/Staging/Prod)
- Deployment tracking
- Rollback capabilities

#### 3. On-Demand Operations
Comprehensive operational capabilities in one module with 14 tabs:

1. **Overview**: Dashboard with key metrics
2. **Provisioning API**: On-demand resource provisioning
3. **Guardrail Validation**: Pre-deployment policy checks
4. **Deployment Templates**: Pre-built architecture templates
5. **Rightsizing**: Resource optimization recommendations
6. **Storage Tiering**: Intelligent S3 storage class management
7. **Autoscaling**: Auto Scaling group management
8. **Patch Automation**: Automated patch management via Systems Manager
9. **Drift Detection**: Configuration drift monitoring
10. **Backup & Recovery**: AWS Backup management
11. **Lifecycle Hooks**: Resource lifecycle automation
12. **Idle Detection**: Identify and remediate idle resources
13. **Continuous Availability**: Multi-AZ monitoring and SLA tracking
14. **Continuous Deployment**: CI/CD pipeline integration

#### 4. FinOps
Cost optimization and financial management.

**Key Features**:
- Cost analysis and trending
- Budget tracking and alerts
- Savings recommendations
- Resource cost allocation

#### 5. Security & Compliance
Security posture and compliance management.

**Key Features**:
- Compliance framework mapping (PCI DSS, HIPAA, SOC 2, etc.)
- Security scanning
- Vulnerability assessment
- Remediation workflows

#### 6. Policy & Guardrails
Pre-deployment policy validation and governance.

**Key Features**:
- Tag policy enforcement
- Naming convention validation
- Resource limit checks
- Cost threshold validation

#### 7. Abstraction & Reusability
Infrastructure patterns and reusable modules.

**Key Features**:
- Module library
- Pattern catalog
- Template versioning
- Sharing capabilities

#### 8. Developer Experience
Self-service infrastructure provisioning for developers.

**Key Features**:
- Developer portal
- API access
- Documentation
- Request tracking

#### 9. Observability
Monitoring, logging, and alerting integration.

**Key Features**:
- CloudWatch integration
- Log aggregation
- Alert management
- Dashboard creation

---

## 🔐 Security Best Practices

1. **Never commit AWS credentials** to version control
2. **Use IAM roles** instead of access keys when possible
3. **Enable MFA** for AWS accounts
4. **Rotate credentials** regularly
5. **Use least privilege** IAM policies
6. **Enable CloudTrail** for audit logging
7. **Review CloudIDP logs** regularly

---

## 🏗️ Architecture

CloudIDP follows a modular architecture:

```
cloudidp/
├── streamlit_app.py           # Main application entry point
├── config.py                  # Configuration management
├── demo_data.py               # Sample data for demo mode
├── data_provider.py           # Data abstraction layer
│
├── Core Modules:
│   ├── design_planning.py
│   ├── provisioning_deployment.py
│   ├── ondemand_operations.py     # Merged comprehensive module
│   ├── finops_module.py
│   ├── security_compliance.py
│   ├── policy_guardrails.py
│   ├── module_07_abstraction.py
│   ├── module_09_developer_experience.py
│   └── module_10_observability.py
│
├── AWS Integration:
│   ├── aws_backend_services.py
│   ├── aws_integrations_manager.py
│   ├── aws_organizations_integration.py
│   ├── cloudformation_integration.py
│   ├── compute_network_integration.py
│   ├── control_tower_integration.py
│   ├── cost_explorer_integration.py
│   ├── database_integration.py
│   ├── iam_identity_center_integration.py
│   ├── service_catalog_integration.py
│   └── systems_manager_integration.py
│
└── Support Services:
    ├── auth_service.py
    ├── api_gateway.py
    ├── backend_integration.py
    ├── database_service.py
    ├── lambda_orchestrator.py
    ├── message_queue.py
    ├── queue_service.py
    └── worker_services.py
```

---

## 🔧 Configuration Reference

### config.py

Key configuration parameters:

```python
# Application
APP_VERSION = "2.0.0"
APP_NAME = "CloudIDP - AWS Infrastructure Development Platform"

# AWS Configuration
AWS_CONFIG = {
    "default_region": "us-east-1",
    "account_id_placeholder": "YOUR_AWS_ACCOUNT_ID",
    "organization_id_placeholder": "YOUR_ORG_ID"
}

# Available AWS Regions
AWS_REGIONS = [...]  # 22 regions supported

# Compliance Frameworks
COMPLIANCE_FRAMEWORKS = [...]  # 10 frameworks supported

# Cost Thresholds (USD)
COST_THRESHOLDS = {
    "warning": 5000,
    "critical": 10000,
    "alert_enabled": True
}
```

---

## 📊 Troubleshooting

### Common Issues

#### 1. "Module not found" errors

**Solution**: Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

#### 2. AWS authentication errors

**Solution**: Verify AWS credentials are configured:
```bash
aws sts get-caller-identity
```

#### 3. "Invalid AWS Account ID" error

**Solution**: Update `config.py` with your actual 12-digit AWS account ID

#### 4. Slow performance in Live Mode

**Solution**: 
- Check AWS API rate limits
- Verify network connectivity
- Consider using Demo Mode for testing

#### 5. Missing data in Live Mode

**Solution**: Ensure AWS credentials have appropriate read permissions for the services you're querying

---

## 🤝 Support

For issues, questions, or contributions:
1. Review this README thoroughly
2. Check the troubleshooting section
3. Review CloudIDP code comments and docstrings

---

## 📝 License

Enterprise-Grade Internal Tool
Copyright © 2024 - All Rights Reserved

---

## 🎯 Roadmap

### Planned Features
- Enhanced AI-powered cost optimization
- Advanced compliance automation
- Cross-account management improvements
- Enhanced disaster recovery automation
- Advanced analytics and reporting

---

## 📚 Additional Resources

- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [AWS Cost Optimization](https://aws.amazon.com/pricing/cost-optimization/)
- [AWS Security Best Practices](https://aws.amazon.com/security/best-practices/)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

**Built for Enterprise AWS Operations**
*Version 2.0.0 - AWS-Only Edition*
