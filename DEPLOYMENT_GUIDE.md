# CloudIDP Enterprise Deployment Guide

## 🎯 Deployment Checklist

### Pre-Deployment

- [ ] Python 3.8+ installed
- [ ] AWS CLI configured
- [ ] AWS account with appropriate permissions
- [ ] Network access to AWS APIs
- [ ] (Optional) Anthropic API key for AI features

### Configuration

- [ ] Updated `config.py` with actual AWS account ID
- [ ] Set environment variables for AWS credentials
- [ ] Configured AWS region preferences
- [ ] Updated cost thresholds if needed
- [ ] Reviewed required tags configuration

### Security

- [ ] AWS credentials secured (never in code)
- [ ] IAM policies follow least privilege
- [ ] MFA enabled on AWS account
- [ ] CloudTrail enabled for audit
- [ ] Security group rules reviewed

### Testing

- [ ] Application starts successfully
- [ ] Demo mode works correctly
- [ ] Live mode connects to AWS
- [ ] All 9 core modules load without errors
- [ ] AWS API calls return expected data

---

## 🔒 IAM Policy Requirements

### Minimum Required Permissions

Create an IAM policy with these permissions for CloudIDP:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "CloudIDPReadAccess",
      "Effect": "Allow",
      "Action": [
        "ec2:Describe*",
        "rds:Describe*",
        "s3:ListBucket",
        "s3:GetObject",
        "cloudformation:Describe*",
        "cloudformation:List*",
        "ce:GetCostAndUsage",
        "ce:GetCostForecast",
        "cloudwatch:GetMetricStatistics",
        "cloudwatch:ListMetrics",
        "iam:GetAccountSummary",
        "iam:ListUsers",
        "iam:ListRoles",
        "organizations:Describe*",
        "organizations:List*",
        "ssm:Describe*",
        "ssm:ListDocuments",
        "backup:List*",
        "backup:Describe*"
      ],
      "Resource": "*"
    },
    {
      "Sid": "CloudIDPWriteAccess",
      "Effect": "Allow",
      "Action": [
        "cloudformation:CreateStack",
        "cloudformation:UpdateStack",
        "cloudformation:DeleteStack",
        "ec2:RunInstances",
        "ec2:StopInstances",
        "ec2:StartInstances",
        "s3:PutObject",
        "ssm:SendCommand",
        "ssm:StartAutomationExecution"
      ],
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "aws:RequestedRegion": ["us-east-1", "us-west-2"]
        }
      }
    }
  ]
}
```

### Create IAM User for CloudIDP

```bash
# Create IAM user
aws iam create-user --user-name cloudidp-service-user

# Attach policy
aws iam attach-user-policy \
  --user-name cloudidp-service-user \
  --policy-arn arn:aws:iam::aws:policy/ReadOnlyAccess

# Create access key
aws iam create-access-key --user-name cloudidp-service-user
```

---

## 🚀 Deployment Methods

### Method 1: Local Development

```bash
# Clone repository
cd cloudidp_refactored

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export AWS_ACCOUNT_ID="123456789012"
export AWS_REGION="us-east-1"

# Run application
streamlit run streamlit_app.py --server.port 8501
```

### Method 2: Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:

```bash
docker build -t cloudidp:2.0.0 .
docker run -p 8501:8501 \
  -e AWS_ACCOUNT_ID=$AWS_ACCOUNT_ID \
  -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
  -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
  -e AWS_REGION=us-east-1 \
  cloudidp:2.0.0
```

### Method 3: EC2 Deployment

```bash
# Launch EC2 instance (t3.medium recommended)
# Amazon Linux 2 or Ubuntu 20.04

# Install Python
sudo yum install python3 -y  # Amazon Linux
# or
sudo apt-get install python3 python3-pip -y  # Ubuntu

# Install CloudIDP
cd /opt
git clone <cloudidp-repo>
cd cloudidp_refactored
pip3 install -r requirements.txt

# Configure as systemd service
sudo cat > /etc/systemd/system/cloudidp.service <<EOF
[Unit]
Description=CloudIDP Service
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/opt/cloudidp_refactored
Environment="AWS_ACCOUNT_ID=123456789012"
Environment="AWS_REGION=us-east-1"
ExecStart=/usr/bin/streamlit run streamlit_app.py --server.port 8501
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Start service
sudo systemctl daemon-reload
sudo systemctl start cloudidp
sudo systemctl enable cloudidp
```

### Method 4: ECS Deployment

Create `task-definition.json`:

```json
{
  "family": "cloudidp",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "containerDefinitions": [
    {
      "name": "cloudidp",
      "image": "your-registry/cloudidp:2.0.0",
      "portMappings": [
        {
          "containerPort": 8501,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "AWS_REGION",
          "value": "us-east-1"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/cloudidp",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

---

## 🔧 Configuration Management

### Environment-Specific Configuration

Create separate configuration files for each environment:

**dev_config.py**:
```python
from config import *

AWS_CONFIG['account_id_placeholder'] = "111111111111"
COST_THRESHOLDS['warning'] = 1000
COST_THRESHOLDS['critical'] = 5000
```

**prod_config.py**:
```python
from config import *

AWS_CONFIG['account_id_placeholder'] = "999999999999"
COST_THRESHOLDS['warning'] = 10000
COST_THRESHOLDS['critical'] = 50000
```

### Secrets Management

Use AWS Secrets Manager for sensitive data:

```python
import boto3
import json

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

# In config.py
try:
    secrets = get_secret('cloudidp/production')
    AWS_CONFIG['account_id_placeholder'] = secrets['account_id']
except:
    # Fall back to environment variables
    pass
```

---

## 📊 Monitoring & Logging

### Application Monitoring

Monitor CloudIDP health:

```python
# Add to streamlit_app.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cloudidp.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('cloudidp')
```

### AWS CloudWatch Integration

Send metrics to CloudWatch:

```python
import boto3

cloudwatch = boto3.client('cloudwatch')

def send_metric(metric_name, value):
    cloudwatch.put_metric_data(
        Namespace='CloudIDP',
        MetricData=[
            {
                'MetricName': metric_name,
                'Value': value,
                'Unit': 'Count'
            }
        ]
    )
```

---

## 🔄 Maintenance

### Regular Tasks

**Daily**:
- [ ] Review application logs
- [ ] Check AWS API usage
- [ ] Monitor cost metrics

**Weekly**:
- [ ] Review security alerts
- [ ] Update demo data if needed
- [ ] Check for AWS service updates

**Monthly**:
- [ ] Update dependencies
- [ ] Review IAM policies
- [ ] Audit user access
- [ ] Performance optimization

### Backup Strategy

**What to Backup**:
1. Configuration files
2. Custom blueprints
3. User data (if stored)
4. Application logs

**Backup Commands**:
```bash
# Backup configuration
tar -czf cloudidp-config-$(date +%Y%m%d).tar.gz config.py *.yaml

# Upload to S3
aws s3 cp cloudidp-config-*.tar.gz s3://your-backup-bucket/cloudidp/
```

---

## 🚨 Troubleshooting Guide

### Issue: Application won't start

**Check**:
1. Python version: `python --version`
2. Dependencies: `pip list`
3. Port availability: `netstat -an | grep 8501`

**Solution**:
```bash
pip install --upgrade -r requirements.txt
streamlit run streamlit_app.py --server.port 8502  # Try different port
```

### Issue: AWS API errors

**Check**:
1. Credentials: `aws sts get-caller-identity`
2. Permissions: Review IAM policies
3. Rate limits: Check AWS Service Quotas

**Solution**:
```bash
# Refresh credentials
aws configure
# Or
export AWS_ACCESS_KEY_ID=new_key
export AWS_SECRET_ACCESS_KEY=new_secret
```

### Issue: High memory usage

**Check**:
1. Number of concurrent users
2. Demo data size
3. AWS API response caching

**Solution**:
- Increase container memory
- Implement data pagination
- Add response caching

---

## 📈 Performance Optimization

### Caching Strategy

Implement caching for AWS API calls:

```python
from functools import lru_cache
import time

@lru_cache(maxsize=128)
def get_ec2_instances_cached(region, timestamp):
    # timestamp forces cache refresh every 5 minutes
    ec2 = boto3.client('ec2', region_name=region)
    return ec2.describe_instances()

# Usage
current_5min = int(time.time() / 300)
instances = get_ec2_instances_cached('us-east-1', current_5min)
```

### Database Optimization

If using database_service.py:
- Enable connection pooling
- Add indexes on frequently queried fields
- Implement query result caching

---

## 🎓 Training & Documentation

### User Training Checklist

- [ ] Overview of CloudIDP capabilities
- [ ] Demo mode vs Live mode
- [ ] Module-by-module walkthrough
- [ ] Best practices for AWS operations
- [ ] Security and compliance considerations
- [ ] Troubleshooting common issues

### Documentation to Maintain

1. **User Guide**: How to use each module
2. **API Documentation**: For programmatic access
3. **Runbook**: Operational procedures
4. **Change Log**: Version history and updates

---

## 🔐 Security Hardening

### Production Security Checklist

- [ ] Enable HTTPS (use reverse proxy like nginx)
- [ ] Implement authentication (Cognito, OAuth)
- [ ] Add rate limiting
- [ ] Enable audit logging
- [ ] Implement role-based access control
- [ ] Regular security scanning
- [ ] Keep dependencies updated
- [ ] Enable AWS CloudTrail
- [ ] Configure VPC endpoints for AWS services
- [ ] Use AWS PrivateLink where possible

### Example: Add Basic Authentication

```python
import streamlit as st

def check_password():
    """Returns `True` if user enters correct password."""
    def password_entered():
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("😕 Password incorrect")
        return False
    else:
        return True

if check_password():
    # Main application code
    st.title("CloudIDP")
```

---

## 📞 Support & Escalation

### Support Tiers

**Tier 1**: Application issues, basic configuration
**Tier 2**: AWS integration issues, performance problems
**Tier 3**: Architecture changes, security incidents

### Incident Response

1. **Identify**: What is the issue?
2. **Assess**: What is the impact?
3. **Escalate**: Who needs to know?
4. **Resolve**: Fix the issue
5. **Document**: Record in runbook

---

**Enterprise Deployment Complete!**

For questions or issues, refer to the main README.md or contact your system administrator.
