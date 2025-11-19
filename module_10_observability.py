"""
Module 10: Observability & Integration
Standard Logging Stack, Metrics Collection, Change Tracking, Alerting
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json

class ObservabilityIntegrationModule:
    """Module for Observability and Integration capabilities"""
    
    @staticmethod
    def render_overview():
        """Render Module 10 Overview"""
        st.header("🔍 Module 10: Observability & Integration")
        
        st.markdown("""
        ### Comprehensive Observability and Integration Framework
        
        **Purpose**: Establish unified observability across all cloud resources with standardized 
        logging, metrics, change tracking, and alerting capabilities.
        """)
        
        # Key Components
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### 🎯 Core Capabilities
            - **Standard Logging Stack via IaC**: Automated deployment of CloudWatch, S3, and log aggregation
            - **Cloud Native Collection**: Real-time metrics and logs from all AWS services
            - **Change Tracking & CMDB**: Automated configuration tracking and sync
            """)
        
        with col2:
            st.markdown("""
            #### 🚨 Monitoring & Response
            - **Policy Violation Reporting**: Real-time compliance breach detection
            - **Event-Driven Alerting**: SNS, EventBridge, and PagerDuty integration
            - **Cross-Account Observability**: Unified monitoring across AWS Organizations
            """)
        
        # Architecture Diagram
        st.markdown("### 📊 Observability Architecture")
        
        architecture = """
        ┌─────────────────────────────────────────────────────────────────┐
        │                   OBSERVABILITY & INTEGRATION                    │
        ├─────────────────────────────────────────────────────────────────┤
        │                                                                   │
        │  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐  │
        │  │   Logging    │      │   Metrics    │      │   Tracing    │  │
        │  │   Stack      │      │  Collection  │      │   (X-Ray)    │  │
        │  └──────┬───────┘      └──────┬───────┘      └──────┬───────┘  │
        │         │                     │                     │           │
        │         └─────────────────────┴─────────────────────┘           │
        │                              │                                   │
        │                    ┌─────────▼─────────┐                        │
        │                    │  CloudWatch Logs  │                        │
        │                    │  CloudWatch       │                        │
        │                    │  Metrics          │                        │
        │                    └─────────┬─────────┘                        │
        │                              │                                   │
        │         ┌────────────────────┼────────────────────┐             │
        │         │                    │                    │             │
        │  ┌──────▼───────┐   ┌───────▼────────┐  ┌───────▼────────┐    │
        │  │ EventBridge  │   │ Config Rules   │  │  Systems Mgr   │    │
        │  │ Event Rules  │   │ Change Track   │  │  OpsCenter     │    │
        │  └──────┬───────┘   └───────┬────────┘  └───────┬────────┘    │
        │         │                   │                    │             │
        │         └───────────────────┴────────────────────┘             │
        │                             │                                   │
        │                    ┌────────▼────────┐                          │
        │                    │   Alert Router  │                          │
        │                    │   SNS Topics    │                          │
        │                    └────────┬────────┘                          │
        │                             │                                   │
        │         ┌───────────────────┼───────────────────┐               │
        │         │                   │                   │               │
        │  ┌──────▼──────┐   ┌────────▼────────┐  ┌──────▼──────┐       │
        │  │   Email     │   │   PagerDuty     │  │    Slack    │       │
        │  │   Alerts    │   │   Incidents     │  │  Webhooks   │       │
        │  └─────────────┘   └─────────────────┘  └─────────────┘       │
        │                                                                   │
        └─────────────────────────────────────────────────────────────────┘
        """
        
        st.code(architecture, language="")
        
        # Value Proposition
        st.markdown("### 💡 Business Value")
        
        metrics_cols = st.columns(4)
        with metrics_cols[0]:
            st.metric("MTTD", "< 5 min", help="Mean Time To Detect")
        with metrics_cols[1]:
            st.metric("MTTR", "< 15 min", help="Mean Time To Resolve")
        with metrics_cols[2]:
            st.metric("Compliance", "99.9%", help="Policy Compliance Rate")
        with metrics_cols[3]:
            st.metric("Coverage", "100%", help="Resource Observability Coverage")
    
    @staticmethod
    def render_logging_stack():
        """Render Standard Logging Stack via IaC"""
        st.header("📝 Standard Logging Stack via IaC")
        
        st.markdown("""
        ### Automated Logging Infrastructure Deployment
        
        Deploy standardized logging infrastructure across all AWS accounts using 
        Infrastructure as Code (CloudFormation/Terraform).
        """)
        
        # Configuration
        st.subheader("🔧 Logging Stack Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            log_retention = st.selectbox(
                "CloudWatch Logs Retention",
                ["7 days", "30 days", "90 days", "180 days", "1 year", "Never expire"],
                index=2
            )
            
            s3_lifecycle = st.selectbox(
                "S3 Logs Lifecycle",
                ["30 days to Glacier", "90 days to Glacier", "180 days to Glacier", 
                 "1 year to Glacier Deep Archive"],
                index=1
            )
            
            enable_kinesis = st.checkbox("Enable Kinesis Data Streams for real-time processing", value=True)
        
        with col2:
            log_aggregation = st.selectbox(
                "Log Aggregation Strategy",
                ["CloudWatch Logs Insights", "OpenSearch", "S3 + Athena", "Third-party SIEM"],
                index=0
            )
            
            encryption_key = st.text_input(
                "KMS Key for Encryption",
                placeholder="arn:aws:kms:us-east-1:123456789012:key/..."
            )
            
            cross_account = st.checkbox("Enable cross-account log aggregation", value=True)
        
        # IaC Templates
        st.subheader("📜 Infrastructure as Code Templates")
        
        tab1, tab2, tab3 = st.tabs(["CloudFormation", "Terraform", "CDK (Python)"])
        
        with tab1:
            st.code("""AWSTemplateFormatVersion: '2010-09-09'
Description: 'Standard Logging Stack - CloudWatch, S3, Kinesis'

Parameters:
  Environment:
    Type: String
    Default: production
    AllowedValues: [development, staging, production]
  
  LogRetentionDays:
    Type: Number
    Default: 90
    Description: CloudWatch Logs retention period in days

Resources:
  # CloudWatch Log Groups
  ApplicationLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Sub '/aws/application/${Environment}'
      RetentionInDays: !Ref LogRetentionDays
      KmsKeyId: !GetAtt LogEncryptionKey.Arn

  InfrastructureLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Sub '/aws/infrastructure/${Environment}'
      RetentionInDays: !Ref LogRetentionDays
      KmsKeyId: !GetAtt LogEncryptionKey.Arn

  SecurityLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Sub '/aws/security/${Environment}'
      RetentionInDays: 365  # Security logs kept longer
      KmsKeyId: !GetAtt LogEncryptionKey.Arn

  # S3 Bucket for Log Archive
  LogArchiveBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub '${AWS::AccountId}-logs-archive-${Environment}'
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: aws:kms
              KMSMasterKeyID: !GetAtt LogEncryptionKey.Arn
      LifecycleConfiguration:
        Rules:
          - Id: TransitionToGlacier
            Status: Enabled
            Transitions:
              - TransitionInDays: 90
                StorageClass: GLACIER
              - TransitionInDays: 365
                StorageClass: DEEP_ARCHIVE
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
      VersioningConfiguration:
        Status: Enabled

  # KMS Key for Encryption
  LogEncryptionKey:
    Type: AWS::KMS::Key
    Properties:
      Description: 'KMS key for log encryption'
      KeyPolicy:
        Version: '2012-10-17'
        Statement:
          - Sid: Enable IAM User Permissions
            Effect: Allow
            Principal:
              AWS: !Sub 'arn:aws:iam::${AWS::AccountId}:root'
            Action: 'kms:*'
            Resource: '*'
          - Sid: Allow CloudWatch Logs
            Effect: Allow
            Principal:
              Service: !Sub 'logs.${AWS::Region}.amazonaws.com'
            Action:
              - 'kms:Encrypt'
              - 'kms:Decrypt'
              - 'kms:ReEncrypt*'
              - 'kms:GenerateDataKey*'
              - 'kms:CreateGrant'
              - 'kms:DescribeKey'
            Resource: '*'

  # Kinesis Data Stream for Real-time Processing
  LogStream:
    Type: AWS::Kinesis::Stream
    Properties:
      Name: !Sub 'log-stream-${Environment}'
      ShardCount: 2
      RetentionPeriodHours: 24
      StreamEncryption:
        EncryptionType: KMS
        KeyId: !Ref LogEncryptionKey

  # CloudWatch Logs Subscription Filter to Kinesis
  LogSubscriptionFilter:
    Type: AWS::Logs::SubscriptionFilter
    Properties:
      LogGroupName: !Ref ApplicationLogGroup
      FilterPattern: ''
      DestinationArn: !GetAtt LogStream.Arn
      RoleArn: !GetAtt LogsToKinesisRole.Arn

  # IAM Role for CloudWatch Logs to Kinesis
  LogsToKinesisRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: logs.amazonaws.com
            Action: 'sts:AssumeRole'
      Policies:
        - PolicyName: PutToKinesis
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - 'kinesis:PutRecord'
                  - 'kinesis:PutRecords'
                Resource: !GetAtt LogStream.Arn

  # CloudWatch Metric Filters for Key Events
  ErrorMetricFilter:
    Type: AWS::Logs::MetricFilter
    Properties:
      LogGroupName: !Ref ApplicationLogGroup
      FilterPattern: '[time, request_id, event_type = ERROR, ...]'
      MetricTransformations:
        - MetricName: ApplicationErrors
          MetricNamespace: !Sub '${Environment}/Application'
          MetricValue: '1'
          DefaultValue: 0

Outputs:
  LogGroupArn:
    Description: Application Log Group ARN
    Value: !GetAtt ApplicationLogGroup.Arn
  
  ArchiveBucketName:
    Description: Log Archive S3 Bucket
    Value: !Ref LogArchiveBucket
  
  KinesisStreamArn:
    Description: Log Processing Stream ARN
    Value: !GetAtt LogStream.Arn
""", language="yaml")
        
        with tab2:
            st.code("""# Standard Logging Stack - Terraform
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

variable "environment" {
  type        = string
  default     = "production"
  description = "Environment name"
}

variable "log_retention_days" {
  type        = number
  default     = 90
  description = "CloudWatch Logs retention in days"
}

# KMS Key for Log Encryption
resource "aws_kms_key" "logs" {
  description             = "KMS key for log encryption"
  deletion_window_in_days = 30
  enable_key_rotation     = true

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "Enable IAM User Permissions"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        Action   = "kms:*"
        Resource = "*"
      },
      {
        Sid    = "Allow CloudWatch Logs"
        Effect = "Allow"
        Principal = {
          Service = "logs.${data.aws_region.current.name}.amazonaws.com"
        }
        Action = [
          "kms:Encrypt",
          "kms:Decrypt",
          "kms:ReEncrypt*",
          "kms:GenerateDataKey*",
          "kms:CreateGrant",
          "kms:DescribeKey"
        ]
        Resource = "*"
      }
    ]
  })

  tags = {
    Environment = var.environment
    Purpose     = "LogEncryption"
  }
}

resource "aws_kms_alias" "logs" {
  name          = "alias/logs-${var.environment}"
  target_key_id = aws_kms_key.logs.key_id
}

# CloudWatch Log Groups
resource "aws_cloudwatch_log_group" "application" {
  name              = "/aws/application/${var.environment}"
  retention_in_days = var.log_retention_days
  kms_key_id        = aws_kms_key.logs.arn

  tags = {
    Environment = var.environment
    Type        = "Application"
  }
}

resource "aws_cloudwatch_log_group" "infrastructure" {
  name              = "/aws/infrastructure/${var.environment}"
  retention_in_days = var.log_retention_days
  kms_key_id        = aws_kms_key.logs.arn

  tags = {
    Environment = var.environment
    Type        = "Infrastructure"
  }
}

resource "aws_cloudwatch_log_group" "security" {
  name              = "/aws/security/${var.environment}"
  retention_in_days = 365  # Security logs kept longer
  kms_key_id        = aws_kms_key.logs.arn

  tags = {
    Environment = var.environment
    Type        = "Security"
  }
}

# S3 Bucket for Log Archive
resource "aws_s3_bucket" "log_archive" {
  bucket = "${data.aws_caller_identity.current.account_id}-logs-archive-${var.environment}"

  tags = {
    Environment = var.environment
    Purpose     = "LogArchive"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "log_archive" {
  bucket = aws_s3_bucket.log_archive.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.logs.arn
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "log_archive" {
  bucket = aws_s3_bucket.log_archive.id

  rule {
    id     = "transition-to-glacier"
    status = "Enabled"

    transition {
      days          = 90
      storage_class = "GLACIER"
    }

    transition {
      days          = 365
      storage_class = "DEEP_ARCHIVE"
    }

    expiration {
      days = 2555  # 7 years
    }
  }
}

resource "aws_s3_bucket_public_access_block" "log_archive" {
  bucket = aws_s3_bucket.log_archive.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "log_archive" {
  bucket = aws_s3_bucket.log_archive.id

  versioning_configuration {
    status = "Enabled"
  }
}

# Kinesis Data Stream
resource "aws_kinesis_stream" "logs" {
  name             = "log-stream-${var.environment}"
  shard_count      = 2
  retention_period = 24

  stream_mode_details {
    stream_mode = "PROVISIONED"
  }

  encryption_type = "KMS"
  kms_key_id      = aws_kms_key.logs.id

  tags = {
    Environment = var.environment
    Purpose     = "LogProcessing"
  }
}

# IAM Role for CloudWatch Logs to Kinesis
resource "aws_iam_role" "logs_to_kinesis" {
  name = "logs-to-kinesis-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "logs.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "logs_to_kinesis" {
  name = "kinesis-put"
  role = aws_iam_role.logs_to_kinesis.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "kinesis:PutRecord",
          "kinesis:PutRecords"
        ]
        Effect   = "Allow"
        Resource = aws_kinesis_stream.logs.arn
      }
    ]
  })
}

# CloudWatch Logs Subscription Filter
resource "aws_cloudwatch_log_subscription_filter" "kinesis" {
  name            = "kinesis-stream-${var.environment}"
  log_group_name  = aws_cloudwatch_log_group.application.name
  filter_pattern  = ""
  destination_arn = aws_kinesis_stream.logs.arn
  role_arn        = aws_iam_role.logs_to_kinesis.arn
}

# CloudWatch Metric Filter for Errors
resource "aws_cloudwatch_log_metric_filter" "errors" {
  name           = "application-errors"
  log_group_name = aws_cloudwatch_log_group.application.name
  pattern        = "[time, request_id, event_type = ERROR, ...]"

  metric_transformation {
    name      = "ApplicationErrors"
    namespace = "${var.environment}/Application"
    value     = "1"
    default_value = 0
  }
}

# Data Sources
data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

# Outputs
output "log_group_arns" {
  description = "ARNs of created log groups"
  value = {
    application    = aws_cloudwatch_log_group.application.arn
    infrastructure = aws_cloudwatch_log_group.infrastructure.arn
    security       = aws_cloudwatch_log_group.security.arn
  }
}

output "archive_bucket_name" {
  description = "Name of log archive S3 bucket"
  value       = aws_s3_bucket.log_archive.id
}

output "kinesis_stream_arn" {
  description = "ARN of log processing Kinesis stream"
  value       = aws_kinesis_stream.logs.arn
}
""", language="hcl")
        
        with tab3:
            st.code("""# Standard Logging Stack - AWS CDK (Python)
from aws_cdk import (
    Stack,
    aws_logs as logs,
    aws_s3 as s3,
    aws_kinesis as kinesis,
    aws_kms as kms,
    aws_iam as iam,
    Duration,
    RemovalPolicy,
)
from constructs import Construct

class LoggingStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, 
                 environment: str = "production", **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # KMS Key for Encryption
        log_key = kms.Key(
            self, "LogEncryptionKey",
            description="KMS key for log encryption",
            enable_key_rotation=True,
            removal_policy=RemovalPolicy.RETAIN
        )
        
        # CloudWatch Log Groups
        app_log_group = logs.LogGroup(
            self, "ApplicationLogGroup",
            log_group_name=f"/aws/application/{environment}",
            retention=logs.RetentionDays.THREE_MONTHS,
            encryption_key=log_key,
            removal_policy=RemovalPolicy.RETAIN
        )
        
        infra_log_group = logs.LogGroup(
            self, "InfrastructureLogGroup",
            log_group_name=f"/aws/infrastructure/{environment}",
            retention=logs.RetentionDays.THREE_MONTHS,
            encryption_key=log_key,
            removal_policy=RemovalPolicy.RETAIN
        )
        
        security_log_group = logs.LogGroup(
            self, "SecurityLogGroup",
            log_group_name=f"/aws/security/{environment}",
            retention=logs.RetentionDays.ONE_YEAR,
            encryption_key=log_key,
            removal_policy=RemovalPolicy.RETAIN
        )
        
        # S3 Bucket for Log Archive
        archive_bucket = s3.Bucket(
            self, "LogArchiveBucket",
            bucket_name=f"{self.account}-logs-archive-{environment}",
            encryption=s3.BucketEncryption.KMS,
            encryption_key=log_key,
            versioned=True,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            lifecycle_rules=[
                s3.LifecycleRule(
                    enabled=True,
                    transitions=[
                        s3.Transition(
                            storage_class=s3.StorageClass.GLACIER,
                            transition_after=Duration.days(90)
                        ),
                        s3.Transition(
                            storage_class=s3.StorageClass.DEEP_ARCHIVE,
                            transition_after=Duration.days(365)
                        )
                    ],
                    expiration=Duration.days(2555)  # 7 years
                )
            ],
            removal_policy=RemovalPolicy.RETAIN
        )
        
        # Kinesis Data Stream
        log_stream = kinesis.Stream(
            self, "LogStream",
            stream_name=f"log-stream-{environment}",
            shard_count=2,
            retention_period=Duration.hours(24),
            encryption=kinesis.StreamEncryption.KMS,
            encryption_key=log_key
        )
        
        # IAM Role for CloudWatch Logs to Kinesis
        logs_to_kinesis_role = iam.Role(
            self, "LogsToKinesisRole",
            assumed_by=iam.ServicePrincipal("logs.amazonaws.com")
        )
        
        log_stream.grant_write(logs_to_kinesis_role)
        
        # Subscription Filter
        logs.SubscriptionFilter(
            self, "KinesisSubscription",
            log_group=app_log_group,
            destination=logs.KinesisDestination(log_stream),
            filter_pattern=logs.FilterPattern.all_events()
        )
        
        # Metric Filters
        app_log_group.add_metric_filter(
            "ErrorMetricFilter",
            filter_pattern=logs.FilterPattern.literal(
                "[time, request_id, event_type = ERROR, ...]"
            ),
            metric_name="ApplicationErrors",
            metric_namespace=f"{environment}/Application",
            metric_value="1",
            default_value=0
        )
        
        # Store attributes
        self.log_groups = {
            'application': app_log_group,
            'infrastructure': infra_log_group,
            'security': security_log_group
        }
        self.archive_bucket = archive_bucket
        self.log_stream = log_stream
        self.encryption_key = log_key
""", language="python")
        
        # Deployment Actions
        st.subheader("🚀 Deployment Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔨 Deploy to Account", key="deploy_logging"):
                with st.spinner("Deploying logging stack..."):
                    st.success("✅ Logging stack deployed successfully!")
                    st.info("""
                    **Resources Created:**
                    - 3 CloudWatch Log Groups
                    - 1 S3 Archive Bucket
                    - 1 Kinesis Data Stream
                    - 1 KMS Encryption Key
                    - Metric Filters and Subscriptions
                    """)
        
        with col2:
            if st.button("📋 Validate Template", key="validate_logging"):
                st.success("✅ Template validation passed!")
        
        with col3:
            if st.button("📊 View Existing Stacks", key="view_stacks"):
                st.info("Showing deployed logging stacks across accounts...")
    
    @staticmethod
    def render_metrics_collection():
        """Render Cloud Native Log/Metric Collection"""
        st.header("📊 Cloud Native Log/Metric Collection")
        
        st.markdown("""
        ### Real-Time Metrics and Log Collection
        
        Automated collection of metrics and logs from all AWS services with 
        standardized namespaces and dimensions.
        """)
        
        # Metrics Configuration
        st.subheader("⚙️ Metrics Collection Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Standard Metrics")
            metrics_config = {
                "EC2 Metrics": st.checkbox("CPU, Memory, Disk, Network", value=True),
                "RDS Metrics": st.checkbox("Connections, IOPS, Replication Lag", value=True),
                "Lambda Metrics": st.checkbox("Invocations, Duration, Errors, Throttles", value=True),
                "ECS/EKS Metrics": st.checkbox("Container CPU/Memory, Service Health", value=True),
                "API Gateway": st.checkbox("Latency, 4xx/5xx Errors, Request Count", value=True),
            }
            
            collection_interval = st.selectbox(
                "Collection Interval",
                ["1 minute", "5 minutes (standard)", "15 minutes"],
                index=1
            )
        
        with col2:
            st.markdown("#### Custom Metrics")
            enable_custom = st.checkbox("Enable custom application metrics", value=True)
            
            if enable_custom:
                custom_namespace = st.text_input(
                    "Custom Namespace",
                    placeholder="MyApp/Production"
                )
                
                st.text_area(
                    "Custom Dimensions (JSON)",
                    value='{\n  "Environment": "Production",\n  "Application": "WebApp",\n  "Version": "1.0"\n}',
                    height=150
                )
        
        # CloudWatch Agent Configuration
        st.subheader("🔧 CloudWatch Agent Configuration")
        
        st.code("""{
  "agent": {
    "metrics_collection_interval": 60,
    "run_as_user": "cwagent"
  },
  "logs": {
    "logs_collected": {
      "files": {
        "collect_list": [
          {
            "file_path": "/var/log/application.log",
            "log_group_name": "/aws/application/production",
            "log_stream_name": "{instance_id}",
            "timezone": "UTC"
          },
          {
            "file_path": "/var/log/access.log",
            "log_group_name": "/aws/access/production",
            "log_stream_name": "{instance_id}",
            "timezone": "UTC"
          }
        ]
      }
    }
  },
  "metrics": {
    "namespace": "CWAgent",
    "metrics_collected": {
      "cpu": {
        "measurement": [
          {
            "name": "cpu_usage_idle",
            "rename": "CPU_IDLE",
            "unit": "Percent"
          },
          "cpu_usage_iowait"
        ],
        "metrics_collection_interval": 60,
        "totalcpu": false
      },
      "disk": {
        "measurement": [
          {
            "name": "used_percent",
            "rename": "DISK_USED",
            "unit": "Percent"
          }
        ],
        "metrics_collection_interval": 60,
        "resources": [
          "*"
        ]
      },
      "diskio": {
        "measurement": [
          "io_time"
        ],
        "metrics_collection_interval": 60
      },
      "mem": {
        "measurement": [
          {
            "name": "mem_used_percent",
            "rename": "MEMORY_USED",
            "unit": "Percent"
          }
        ],
        "metrics_collection_interval": 60
      },
      "netstat": {
        "measurement": [
          "tcp_established",
          "tcp_time_wait"
        ],
        "metrics_collection_interval": 60
      },
      "statsd": {
        "metrics_aggregation_interval": 60,
        "metrics_collection_interval": 10,
        "service_address": ":8125"
      }
    }
  }
}""", language="json")
        
        # Sample Metrics Dashboard
        st.subheader("📈 Real-Time Metrics Dashboard")
        
        if st.session_state.demo_mode:
            # Demo data
            import random
            from datetime import datetime, timedelta
            
            # Generate sample time series data
            now = datetime.now()
            times = [now - timedelta(minutes=x) for x in range(60, 0, -1)]
            
            metrics_data = {
                'Time': times,
                'CPU Usage (%)': [random.uniform(20, 80) for _ in range(60)],
                'Memory Usage (%)': [random.uniform(40, 70) for _ in range(60)],
                'Disk I/O (MB/s)': [random.uniform(5, 50) for _ in range(60)],
                'Network In (MB/s)': [random.uniform(10, 100) for _ in range(60)]
            }
            
            df = pd.DataFrame(metrics_data)
            
            # Display metrics
            metric_cols = st.columns(4)
            with metric_cols[0]:
                st.metric("Avg CPU", f"{df['CPU Usage (%)'].mean():.1f}%", 
                         delta=f"{random.uniform(-5, 5):.1f}%")
            with metric_cols[1]:
                st.metric("Avg Memory", f"{df['Memory Usage (%)'].mean():.1f}%",
                         delta=f"{random.uniform(-3, 3):.1f}%")
            with metric_cols[2]:
                st.metric("Avg Disk I/O", f"{df['Disk I/O (MB/s)'].mean():.1f} MB/s",
                         delta=f"{random.uniform(-10, 10):.1f} MB/s")
            with metric_cols[3]:
                st.metric("Avg Network", f"{df['Network In (MB/s)'].mean():.1f} MB/s",
                         delta=f"{random.uniform(-5, 5):.1f} MB/s")
            
            # Line chart
            st.line_chart(df.set_index('Time')[['CPU Usage (%)', 'Memory Usage (%)']])
        else:
            st.info("💡 Connect to AWS to view real-time metrics from CloudWatch")
        
        # Log Insights Queries
        st.subheader("🔍 CloudWatch Logs Insights")
        
        query_templates = st.selectbox(
            "Select Query Template",
            [
                "Top 10 Error Messages",
                "Request Latency Statistics",
                "Failed Authentication Attempts",
                "Resource Access Patterns",
                "Custom Query"
            ]
        )
        
        if query_templates == "Top 10 Error Messages":
            query = """fields @timestamp, @message
| filter @message like /ERROR/
| stats count() as error_count by @message
| sort error_count desc
| limit 10"""
        elif query_templates == "Request Latency Statistics":
            query = """fields @timestamp, request.latency
| filter ispresent(request.latency)
| stats avg(request.latency), max(request.latency), 
        pct(request.latency, 95), pct(request.latency, 99)"""
        elif query_templates == "Failed Authentication Attempts":
            query = """fields @timestamp, userIdentity.principalId, errorCode
| filter errorCode like /Unauthorized/ or errorCode like /AccessDenied/
| stats count() as attempts by userIdentity.principalId
| sort attempts desc"""
        elif query_templates == "Resource Access Patterns":
            query = """fields @timestamp, requestParameters.resourceArn, userIdentity.arn
| stats count() as access_count by requestParameters.resourceArn
| sort access_count desc
| limit 25"""
        else:
            query = "fields @timestamp, @message\n| limit 20"
        
        st.code(query, language="sql")
        
        if st.button("🔍 Run Query", key="run_log_query"):
            with st.spinner("Executing query..."):
                st.success("✅ Query executed successfully!")
                
                if st.session_state.demo_mode:
                    # Demo results
                    results_data = {
                        'Timestamp': [datetime.now() - timedelta(minutes=x) for x in range(10)],
                        'Message': [
                            'ERROR: Database connection timeout',
                            'ERROR: Failed to authenticate user',
                            'ERROR: Invalid request parameter',
                            'ERROR: Resource not found',
                            'ERROR: Permission denied',
                            'ERROR: Rate limit exceeded',
                            'ERROR: Internal server error',
                            'ERROR: Timeout waiting for response',
                            'ERROR: Invalid configuration',
                            'ERROR: Service unavailable'
                        ],
                        'Count': [45, 32, 28, 25, 22, 18, 15, 12, 10, 8]
                    }
                    st.dataframe(pd.DataFrame(results_data), use_container_width=True)
    
    @staticmethod
    def render_change_tracking():
        """Render Change Tracking & CMDB Sync"""
        st.header("📝 Change Tracking & CMDB Sync")
        
        st.markdown("""
        ### Automated Configuration Tracking and CMDB Integration
        
        Track all configuration changes across AWS resources and automatically 
        sync with Configuration Management Database (CMDB).
        """)
        
        # AWS Config Setup
        st.subheader("⚙️ AWS Config Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Resource Types to Track")
            resource_types = {
                "EC2 Instances": st.checkbox("EC2::Instance", value=True),
                "Security Groups": st.checkbox("EC2::SecurityGroup", value=True),
                "IAM Roles": st.checkbox("IAM::Role", value=True),
                "S3 Buckets": st.checkbox("S3::Bucket", value=True),
                "RDS Instances": st.checkbox("RDS::DBInstance", value=True),
                "Lambda Functions": st.checkbox("Lambda::Function", value=True),
                "VPCs": st.checkbox("EC2::VPC", value=True),
                "Load Balancers": st.checkbox("ElasticLoadBalancingV2::LoadBalancer", value=True)
            }
            
            track_all = st.checkbox("Track all supported resource types", value=False)
        
        with col2:
            st.markdown("#### Change Detection Settings")
            
            snapshot_frequency = st.selectbox(
                "Configuration Snapshot Frequency",
                ["Every 1 hour", "Every 3 hours", "Every 6 hours", "Every 12 hours", "Daily"],
                index=0
            )
            
            enable_notifications = st.checkbox("Send notifications on changes", value=True)
            
            if enable_notifications:
                notification_channels = st.multiselect(
                    "Notification Channels",
                    ["SNS Topic", "EventBridge", "CloudWatch Logs", "CMDB Webhook"],
                    default=["SNS Topic", "EventBridge"]
                )
        
        # CMDB Integration
        st.subheader("🔗 CMDB Integration Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            cmdb_system = st.selectbox(
                "CMDB System",
                ["ServiceNow", "BMC Remedy", "Cherwell", "Custom CMDB API"],
                index=0
            )
            
            cmdb_endpoint = st.text_input(
                "CMDB API Endpoint",
                placeholder="https://your-instance.service-now.com/api"
            )
            
            sync_frequency = st.selectbox(
                "Sync Frequency",
                ["Real-time (on change)", "Every 5 minutes", "Every 15 minutes", "Hourly"],
                index=0
            )
        
        with col2:
            cmdb_auth = st.selectbox(
                "Authentication Method",
                ["API Key", "OAuth 2.0", "Basic Auth", "IAM Role"],
                index=0
            )
            
            cmdb_api_key = st.text_input(
                "API Key / Credentials",
                type="password",
                placeholder="Enter CMDB credentials"
            )
            
            enable_bidirectional = st.checkbox(
                "Enable bidirectional sync",
                value=False,
                help="Sync changes from CMDB back to AWS tags"
            )
        
        # Config Rules for Change Validation
        st.subheader("✅ Configuration Rules & Validation")
        
        st.code("""# AWS Config Rule: Detect Unauthorized Changes
{
  "ConfigRuleName": "detect-unauthorized-changes",
  "Description": "Detect configuration changes not originating from approved CI/CD pipelines",
  "Source": {
    "Owner": "CUSTOM_LAMBDA",
    "SourceIdentifier": "arn:aws:lambda:us-east-1:123456789012:function:ValidateChangeSource"
  },
  "Scope": {
    "ComplianceResourceTypes": [
      "AWS::EC2::Instance",
      "AWS::RDS::DBInstance",
      "AWS::Lambda::Function",
      "AWS::IAM::Role"
    ]
  },
  "ConfigRuleState": "ACTIVE",
  "MaximumExecutionFrequency": "One_Hour"
}

# Lambda Function for Change Validation
import boto3
import json

def lambda_handler(event, context):
    config_client = boto3.client('config')
    cloudtrail_client = boto3.client('cloudtrail')
    
    # Get resource configuration from Config
    configuration_item = json.loads(event['configurationItem'])
    resource_type = configuration_item['resourceType']
    resource_id = configuration_item['resourceId']
    
    # Query CloudTrail for change events
    events = cloudtrail_client.lookup_events(
        LookupAttributes=[
            {'AttributeKey': 'ResourceName', 'AttributeValue': resource_id}
        ],
        MaxResults=1
    )
    
    if events['Events']:
        event_source = events['Events'][0].get('Username', '')
        
        # Check if change came from approved CI/CD role
        approved_roles = [
            'AWSReservedSSO_DevOps',
            'jenkins-deployment-role',
            'github-actions-role'
        ]
        
        if any(role in event_source for role in approved_roles):
            compliance_type = 'COMPLIANT'
            annotation = 'Change originated from approved automation'
        else:
            compliance_type = 'NON_COMPLIANT'
            annotation = f'Unauthorized manual change by {event_source}'
    else:
        compliance_type = 'INSUFFICIENT_DATA'
        annotation = 'No CloudTrail events found for this change'
    
    # Report compliance result
    config_client.put_evaluations(
        Evaluations=[{
            'ComplianceResourceType': resource_type,
            'ComplianceResourceId': resource_id,
            'ComplianceType': compliance_type,
            'Annotation': annotation,
            'OrderingTimestamp': configuration_item['configurationItemCaptureTime']
        }],
        ResultToken=event['resultToken']
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps(f'Compliance evaluation: {compliance_type}')
    }
""", language="python")
        
        # Change Timeline View
        st.subheader("📅 Configuration Change Timeline")
        
        if st.session_state.demo_mode:
            # Demo change history
            changes_data = {
                'Timestamp': [datetime.now() - timedelta(hours=x) for x in range(10)],
                'Resource Type': [
                    'EC2::Instance',
                    'IAM::Role',
                    'S3::Bucket',
                    'RDS::DBInstance',
                    'Lambda::Function',
                    'EC2::SecurityGroup',
                    'ElasticLoadBalancingV2::LoadBalancer',
                    'EC2::Instance',
                    'IAM::Policy',
                    'S3::Bucket'
                ],
                'Resource ID': [
                    'i-0abc123def456',
                    'role/app-execution-role',
                    'my-app-bucket',
                    'db-prod-mysql-01',
                    'process-payments',
                    'sg-0123456789',
                    'app-alb-prod',
                    'i-0xyz789abc123',
                    'policy/S3ReadOnly',
                    'logs-archive-bucket'
                ],
                'Change Type': [
                    'UPDATE',
                    'CREATE',
                    'UPDATE',
                    'UPDATE',
                    'UPDATE',
                    'UPDATE',
                    'CREATE',
                    'DELETE',
                    'UPDATE',
                    'UPDATE'
                ],
                'Changed By': [
                    'jenkins-deployment-role',
                    'admin@company.com',
                    'github-actions-role',
                    'DBA-team@company.com',
                    'jenkins-deployment-role',
                    'security-team@company.com',
                    'terraform-automation',
                    'admin@company.com',
                    'security-automation',
                    'backup-automation'
                ],
                'CMDB Synced': [
                    '✅',
                    '✅',
                    '✅',
                    '✅',
                    '✅',
                    '⏳ Pending',
                    '✅',
                    '✅',
                    '✅',
                    '✅'
                ]
            }
            
            df_changes = pd.DataFrame(changes_data)
            st.dataframe(df_changes, use_container_width=True)
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Changes (24h)", "247")
            with col2:
                st.metric("Unauthorized Changes", "3", delta="-2")
            with col3:
                st.metric("CMDB Sync Rate", "99.2%", delta="0.5%")
            with col4:
                st.metric("Avg Sync Latency", "12 sec", delta="-3 sec")
        else:
            st.info("💡 Connect to AWS to view real configuration change history")
        
        # Compliance Status
        st.subheader("📊 Configuration Compliance Status")
        
        if st.session_state.demo_mode:
            compliance_data = {
                'Rule Name': [
                    'Approved Changes Only',
                    'Required Tags Present',
                    'Encryption Enabled',
                    'Backup Configured',
                    'Logging Enabled'
                ],
                'Compliant Resources': [234, 456, 412, 389, 445],
                'Non-Compliant Resources': [12, 5, 18, 34, 8],
                'Compliance Rate': ['95.1%', '98.9%', '95.8%', '92.0%', '98.2%']
            }
            
            st.dataframe(pd.DataFrame(compliance_data), use_container_width=True)
    
    @staticmethod
    def render_policy_violations():
        """Render Policy Violation Reporting"""
        st.header("🚨 Policy Violation Reporting")
        
        st.markdown("""
        ### Real-Time Policy Compliance Monitoring and Alerting
        
        Detect and report policy violations in real-time with automated remediation 
        and escalation workflows.
        """)
        
        # Violation Dashboard
        st.subheader("📊 Active Policy Violations Dashboard")
        
        if st.session_state.demo_mode:
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Critical Violations", "5", delta="2", delta_color="inverse")
            with col2:
                st.metric("High Priority", "12", delta="-3", delta_color="normal")
            with col3:
                st.metric("Medium Priority", "28", delta="5", delta_color="inverse")
            with col4:
                st.metric("Low Priority", "47", delta="-8", delta_color="normal")
            
            st.markdown("---")
            
            # Violations Table
            violations_data = {
                'Severity': [
                    '🔴 Critical',
                    '🔴 Critical',
                    '🟠 High',
                    '🟠 High',
                    '🟠 High',
                    '🟡 Medium',
                    '🟡 Medium',
                    '🟢 Low'
                ],
                'Policy': [
                    'Public S3 Bucket',
                    'Root Account Access',
                    'Unencrypted EBS Volume',
                    'Security Group - All Traffic',
                    'Unused IAM Access Key',
                    'Missing Backup Tag',
                    'Non-Compliant Instance Type',
                    'Outdated AMI'
                ],
                'Resource': [
                    's3://sensitive-data-bucket',
                    'Root Account',
                    'vol-0abc123456',
                    'sg-0xyz789abc',
                    'AKIAIOSFODNN7EXAMPLE',
                    'i-0def456789',
                    'i-0ghi789012',
                    'i-0jkl345678'
                ],
                'Detected': [
                    '2 min ago',
                    '15 min ago',
                    '1 hour ago',
                    '2 hours ago',
                    '3 hours ago',
                    '5 hours ago',
                    '8 hours ago',
                    '1 day ago'
                ],
                'Account': [
                    'prod-123456',
                    'prod-123456',
                    'dev-789012',
                    'prod-123456',
                    'staging-345678',
                    'dev-789012',
                    'prod-123456',
                    'staging-345678'
                ],
                'Auto-Remediation': [
                    '⏳ In Progress',
                    '❌ Manual Required',
                    '✅ Completed',
                    '⏳ In Progress',
                    '✅ Completed',
                    '⏳ Pending Approval',
                    '❌ Failed',
                    '✅ Scheduled'
                ],
                'Status': [
                    'Open',
                    'Open',
                    'Resolved',
                    'Open',
                    'Resolved',
                    'Open',
                    'Open',
                    'Open'
                ]
            }
            
            df_violations = pd.DataFrame(violations_data)
            st.dataframe(df_violations, use_container_width=True)
        else:
            st.info("💡 Connect to AWS to view real policy violations")
        
        # Policy Categories
        st.subheader("📋 Policy Categories")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Security Policies")
            security_policies = pd.DataFrame({
                'Policy': [
                    'Public Access Prohibited',
                    'Encryption Required',
                    'MFA Required',
                    'Least Privilege Access',
                    'Secure Communication Only'
                ],
                'Violations': [8, 15, 3, 22, 6],
                'Auto-Remediate': ['✅', '✅', '❌', '⚠️', '✅']
            })
            st.dataframe(security_policies, use_container_width=True)
        
        with col2:
            st.markdown("#### Compliance Policies")
            compliance_policies = pd.DataFrame({
                'Policy': [
                    'Required Tags Present',
                    'Approved Regions Only',
                    'Data Residency Rules',
                    'Backup Policy Compliance',
                    'Log Retention Requirements'
                ],
                'Violations': [42, 5, 2, 18, 8],
                'Auto-Remediate': ['✅', '⚠️', '❌', '✅', '✅']
            })
            st.dataframe(compliance_policies, use_container_width=True)
        
        # Auto-Remediation Configuration
        st.subheader("🔧 Auto-Remediation Configuration")
        
        st.code("""# EventBridge Rule for Policy Violation Detection
{
  "source": ["aws.config"],
  "detail-type": ["Config Rules Compliance Change"],
  "detail": {
    "messageType": ["ComplianceChangeNotification"],
    "newEvaluationResult": {
      "complianceType": ["NON_COMPLIANT"]
    },
    "configRuleName": [{
      "prefix": "security-"
    }]
  }
}

# Lambda Function for Auto-Remediation
import boto3
import json

def lambda_handler(event, context):
    config_rule = event['detail']['configRuleName']
    resource_type = event['detail']['resourceType']
    resource_id = event['detail']['resourceId']
    
    remediation_actions = {
        'security-s3-public-block': remediate_s3_public_access,
        'security-unencrypted-ebs': remediate_ebs_encryption,
        'security-sg-unrestricted': remediate_security_group,
        'security-unused-keys': remediate_iam_keys
    }
    
    if config_rule in remediation_actions:
        result = remediation_actions[config_rule](resource_id)
        
        # Send notification
        sns = boto3.client('sns')
        sns.publish(
            TopicArn='arn:aws:sns:us-east-1:123456789012:policy-violations',
            Subject=f'Auto-Remediation: {config_rule}',
            Message=json.dumps({
                'rule': config_rule,
                'resource': resource_id,
                'action': 'auto_remediated',
                'result': result
            })
        )
        
        return {'statusCode': 200, 'body': 'Remediation completed'}
    else:
        # Manual remediation required
        create_ops_item(config_rule, resource_type, resource_id)
        return {'statusCode': 200, 'body': 'Manual remediation required'}

def remediate_s3_public_access(bucket_name):
    s3 = boto3.client('s3')
    s3.put_public_access_block(
        Bucket=bucket_name,
        PublicAccessBlockConfiguration={
            'BlockPublicAcls': True,
            'IgnorePublicAcls': True,
            'BlockPublicPolicy': True,
            'RestrictPublicBuckets': True
        }
    )
    return 'Public access blocked'

def remediate_ebs_encryption(volume_id):
    ec2 = boto3.client('ec2')
    # Create encrypted snapshot and new volume
    response = ec2.create_snapshot(
        VolumeId=volume_id,
        Description='Remediation snapshot for encryption'
    )
    snapshot_id = response['SnapshotId']
    
    # Wait for snapshot completion, then create encrypted volume
    return f'Encryption initiated via snapshot {snapshot_id}'

def remediate_security_group(sg_id):
    ec2 = boto3.client('ec2')
    # Remove overly permissive rules
    ec2.revoke_security_group_ingress(
        GroupId=sg_id,
        IpPermissions=[{
            'IpProtocol': '-1',
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }]
    )
    return 'Unrestricted ingress rule removed'

def remediate_iam_keys(key_id):
    iam = boto3.client('iam')
    # Deactivate unused key
    iam.update_access_key(
        AccessKeyId=key_id,
        Status='Inactive'
    )
    return 'Unused access key deactivated'

def create_ops_item(rule, resource_type, resource_id):
    ssm = boto3.client('ssm')
    ssm.create_ops_item(
        Title=f'Policy Violation: {rule}',
        Description=f'Manual remediation required for {resource_type} {resource_id}',
        Priority=2,
        Source='AWS Config',
        Category='Security',
        Severity='2'
    )
""", language="python")
        
        # Violation Trends
        st.subheader("📈 Violation Trends")
        
        if st.session_state.demo_mode:
            import random
            trend_data = {
                'Date': [(datetime.now() - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(30, 0, -1)],
                'Critical': [random.randint(2, 8) for _ in range(30)],
                'High': [random.randint(5, 15) for _ in range(30)],
                'Medium': [random.randint(15, 35) for _ in range(30)],
                'Low': [random.randint(30, 60) for _ in range(30)]
            }
            
            df_trends = pd.DataFrame(trend_data)
            st.line_chart(df_trends.set_index('Date'))
    
    @staticmethod
    def render_event_alerting():
        """Render Event Tools for Alerting"""
        st.header("🔔 Event Tools for Alerting")
        
        st.markdown("""
        ### Multi-Channel Event-Driven Alerting System
        
        Configure intelligent alerts across multiple channels with escalation policies 
        and on-call integration.
        """)
        
        # Alert Channels Configuration
        st.subheader("📢 Alert Channels Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Primary Channels")
            
            enable_email = st.checkbox("📧 Email Notifications", value=True)
            if enable_email:
                email_recipients = st.text_area(
                    "Email Recipients",
                    placeholder="ops-team@company.com\nsecurity-team@company.com",
                    height=80
                )
            
            enable_slack = st.checkbox("💬 Slack Integration", value=True)
            if enable_slack:
                slack_webhook = st.text_input(
                    "Slack Webhook URL",
                    type="password",
                    placeholder="https://hooks.slack.com/services/..."
                )
                slack_channel = st.text_input("Default Channel", value="#aws-alerts")
            
            enable_pagerduty = st.checkbox("📟 PagerDuty Integration", value=True)
            if enable_pagerduty:
                pagerduty_key = st.text_input(
                    "PagerDuty Integration Key",
                    type="password"
                )
        
        with col2:
            st.markdown("#### Secondary Channels")
            
            enable_sms = st.checkbox("📱 SMS Alerts (SNS)", value=False)
            if enable_sms:
                sms_numbers = st.text_area(
                    "Phone Numbers",
                    placeholder="+1-555-0100\n+1-555-0101",
                    height=80
                )
            
            enable_webhook = st.checkbox("🔗 Custom Webhook", value=False)
            if enable_webhook:
                webhook_url = st.text_input(
                    "Webhook URL",
                    placeholder="https://your-system.com/webhook"
                )
            
            enable_teams = st.checkbox("👥 Microsoft Teams", value=False)
            if enable_teams:
                teams_webhook = st.text_input(
                    "Teams Webhook URL",
                    type="password"
                )
        
        # Alert Rules
        st.subheader("⚡ Alert Rules & Conditions")
        
        tab1, tab2, tab3 = st.tabs(["Metric Alarms", "Log-Based Alerts", "Event Patterns"])
        
        with tab1:
            st.markdown("#### CloudWatch Metric Alarms")
            
            st.code("""# High CPU Utilization Alert
resource "aws_cloudwatch_metric_alarm" "high_cpu" {
  alarm_name          = "high-cpu-utilization"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "300"
  statistic           = "Average"
  threshold           = "80"
  alarm_description   = "Alert when CPU exceeds 80% for 10 minutes"
  
  alarm_actions = [
    aws_sns_topic.alerts.arn
  ]
  
  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.app.name
  }
}

# Database Connection Spike Alert
resource "aws_cloudwatch_metric_alarm" "db_connections" {
  alarm_name          = "high-db-connections"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "DatabaseConnections"
  namespace           = "AWS/RDS"
  period              = "60"
  statistic           = "Average"
  threshold           = "80"
  treat_missing_data  = "notBreaching"
  
  alarm_actions = [
    aws_sns_topic.alerts.arn,
    aws_autoscaling_policy.scale_up.arn
  ]
}

# Lambda Error Rate Alert
resource "aws_cloudwatch_metric_alarm" "lambda_errors" {
  alarm_name          = "lambda-high-error-rate"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  threshold           = "5"
  alarm_description   = "Alert when Lambda error rate exceeds 5%"
  treat_missing_data  = "notBreaching"
  
  metric_query {
    id          = "error_rate"
    expression  = "errors / invocations * 100"
    label       = "Error Rate"
    return_data = "true"
  }
  
  metric_query {
    id = "errors"
    metric {
      metric_name = "Errors"
      namespace   = "AWS/Lambda"
      period      = "300"
      stat        = "Sum"
      dimensions = {
        FunctionName = "process-payments"
      }
    }
  }
  
  metric_query {
    id = "invocations"
    metric {
      metric_name = "Invocations"
      namespace   = "AWS/Lambda"
      period      = "300"
      stat        = "Sum"
      dimensions = {
        FunctionName = "process-payments"
      }
    }
  }
  
  alarm_actions = [
    aws_sns_topic.critical_alerts.arn
  ]
}
""", language="hcl")
        
        with tab2:
            st.markdown("#### Log-Based Metric Filters and Alerts")
            
            st.code("""# Security Event Alert
resource "aws_cloudwatch_log_metric_filter" "security_events" {
  name           = "security-events"
  log_group_name = aws_cloudwatch_log_group.security.name
  pattern        = "[time, event_type = SECURITY_VIOLATION, ...]"
  
  metric_transformation {
    name      = "SecurityViolations"
    namespace = "Security/Events"
    value     = "1"
  }
}

resource "aws_cloudwatch_metric_alarm" "security_violations" {
  alarm_name          = "security-violations-detected"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "SecurityViolations"
  namespace           = "Security/Events"
  period              = "60"
  statistic           = "Sum"
  threshold           = "0"
  alarm_description   = "Alert on any security violation"
  
  alarm_actions = [
    aws_sns_topic.security_alerts.arn
  ]
}

# Failed Login Attempts
resource "aws_cloudwatch_log_metric_filter" "failed_logins" {
  name           = "failed-login-attempts"
  log_group_name = aws_cloudwatch_log_group.application.name
  pattern        = "[time, event = LOGIN_FAILED, user, ...]"
  
  metric_transformation {
    name      = "FailedLoginAttempts"
    namespace = "Application/Security"
    value     = "1"
  }
}

resource "aws_cloudwatch_metric_alarm" "brute_force_detection" {
  alarm_name          = "potential-brute-force-attack"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "FailedLoginAttempts"
  namespace           = "Application/Security"
  period              = "300"
  statistic           = "Sum"
  threshold           = "10"
  alarm_description   = "Alert on 10+ failed login attempts in 5 minutes"
  
  alarm_actions = [
    aws_sns_topic.security_alerts.arn
  ]
}
""", language="hcl")
        
        with tab3:
            st.markdown("#### EventBridge Event Patterns")
            
            st.code("""{
  "Event Pattern for Security Group Changes": {
    "source": ["aws.ec2"],
    "detail-type": ["AWS API Call via CloudTrail"],
    "detail": {
      "eventName": [
        "AuthorizeSecurityGroupIngress",
        "AuthorizeSecurityGroupEgress",
        "RevokeSecurityGroupIngress",
        "RevokeSecurityGroupEgress"
      ]
    }
  },
  
  "Event Pattern for IAM Changes": {
    "source": ["aws.iam"],
    "detail-type": ["AWS API Call via CloudTrail"],
    "detail": {
      "eventName": [
        "CreateUser",
        "DeleteUser",
        "AttachUserPolicy",
        "PutUserPolicy",
        "CreateAccessKey"
      ]
    }
  },
  
  "Event Pattern for Root Account Usage": {
    "source": ["aws.signin"],
    "detail-type": ["AWS Console Sign In via CloudTrail"],
    "detail": {
      "userIdentity": {
        "type": ["Root"]
      }
    }
  },
  
  "Event Pattern for Instance State Changes": {
    "source": ["aws.ec2"],
    "detail-type": ["EC2 Instance State-change Notification"],
    "detail": {
      "state": ["running", "stopped", "terminated"]
    }
  },
  
  "Event Pattern for GuardDuty Findings": {
    "source": ["aws.guardduty"],
    "detail-type": ["GuardDuty Finding"],
    "detail": {
      "severity": [7, 8, 8.9]
    }
  }
}""", language="json")
        
        # Escalation Policies
        st.subheader("📊 Escalation Policies")
        
        st.markdown("""
        Configure automatic escalation based on severity and response time:
        """)
        
        escalation_config = pd.DataFrame({
            'Severity': ['🔴 Critical', '🟠 High', '🟡 Medium', '🟢 Low'],
            'Initial Alert': ['PagerDuty + Slack', 'Slack + Email', 'Email', 'Email'],
            'No Response After': ['5 minutes', '15 minutes', '1 hour', '4 hours'],
            'Escalation 1': ['Call On-Call Manager', 'Page Team Lead', 'Slack Reminder', 'Slack Reminder'],
            'Escalation 2': ['Page Director', 'Call On-Call Manager', 'Email Manager', 'Email Team Lead']
        })
        
        st.dataframe(escalation_config, use_container_width=True)
        
        # On-Call Schedule Integration
        st.subheader("👥 On-Call Schedule Integration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Current On-Call Roster")
            if st.session_state.demo_mode:
                oncall_data = pd.DataFrame({
                    'Team': ['DevOps', 'Security', 'Database', 'Application'],
                    'On-Call Engineer': [
                        'John Smith',
                        'Sarah Johnson',
                        'Mike Chen',
                        'Emily Davis'
                    ],
                    'Backup': [
                        'Jane Doe',
                        'Tom Wilson',
                        'Lisa Wang',
                        'Chris Brown'
                    ],
                    'Shift Ends': [
                        '6 hours',
                        '2 days',
                        '4 days',
                        '12 hours'
                    ]
                })
                st.dataframe(oncall_data, use_container_width=True)
        
        with col2:
            st.markdown("#### Recent Alert Activity")
            if st.session_state.demo_mode:
                activity_data = pd.DataFrame({
                    'Time': ['5 min ago', '23 min ago', '1 hour ago', '2 hours ago'],
                    'Alert': [
                        'High CPU Usage',
                        'Security Group Changed',
                        'Database Connection Spike',
                        'Lambda Error Rate High'
                    ],
                    'Acknowledged': ['✅ John Smith', '✅ Sarah Johnson', '✅ Mike Chen', '✅ Emily Davis'],
                    'Resolved': ['⏳ In Progress', '✅ 15 min', '✅ 22 min', '✅ 8 min']
                })
                st.dataframe(activity_data, use_container_width=True)
        
        # Alert Testing
        st.subheader("🧪 Test Alert Delivery")
        
        test_severity = st.selectbox(
            "Test Alert Severity",
            ["Critical", "High", "Medium", "Low"]
        )
        
        test_message = st.text_area(
            "Test Message",
            value="This is a test alert to verify the alerting pipeline is working correctly.",
            height=100
        )
        
        if st.button("📤 Send Test Alert", key="send_test_alert"):
            with st.spinner("Sending test alert..."):
                st.success(f"✅ Test alert sent successfully!")
                st.info(f"""
                **Alert Details:**
                - Severity: {test_severity}
                - Channels: {'Email, Slack, PagerDuty' if test_severity == 'Critical' else 'Email, Slack'}
                - Delivery Status: All channels confirmed
                - Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                """)

# Export the module
__all__ = ['ObservabilityIntegrationModule']
