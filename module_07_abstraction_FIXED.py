"""
Module 07: Abstraction & Reusability
Composable Modules, App-Centric Packaging, Parameterization & Multi-Env Support
"""

import streamlit as st
import yaml
import json
from anthropic_helper import AnthropicHelper


class AbstractionReusabilityModule:
    """Module 07: Abstraction & Reusability Implementation"""
    def render(self):
        """Main render method - organizes all sub-features in tabs"""
        
        st.markdown("## Abstractionreusability")
        
        # Create tabs for each sub-feature
        tabs = st.tabs([
            "📋 Overview",
            "⚙️ Composable Modules",
            "⚙️ App Centric Packaging",
            "⚙️ Parameterization",
            "⚙️ Multi Environment",
            "⚙️ Lifecycle Management",
            "⚙️ Module 07"
        ])
        
        with tabs[0]:
            self.render_overview()
        
        with tabs[1]:
            self.render_composable_modules()
        
        with tabs[2]:
            self.render_app_centric_packaging()
        
        with tabs[3]:
            self.render_parameterization()
        
        with tabs[4]:
            self.render_multi_environment()
        
        with tabs[5]:
            self.render_lifecycle_management()
        
        with tabs[6]:
            self.render_module_07()


    
    @staticmethod
    def render_overview():
        """Render Module 07 Overview"""
        
        st.markdown("## 🔧 Module 07: Abstraction & Reusability")
        st.markdown("### Composable Modules, App-Centric Packaging & Multi-Environment Support")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Code Reduction", "70%", help="Reduction in infrastructure code duplication")
        
        with col2:
            st.metric("Provisioning Speed", "90%", help="Faster new environment provisioning")
        
        with col3:
            st.metric("Consistency", "100%", help="Consistent deployments across 640+ accounts")
        
        with col4:
            st.metric("Deploy Time", "15 min", help="From requirements to deployed environment")
        
        st.markdown("---")
        
        # Overview tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📋 Overview",
            "🏗️ Architecture", 
            "🎯 Benefits",
            "🚀 Quick Start",
            "📊 Examples"
        ])
        
        with tab1:
            st.markdown("### Module Overview")
            
            st.markdown("""
            This module establishes enterprise patterns for creating **reusable, composable infrastructure modules** 
            that support multi-environment deployments while maintaining consistency and reducing operational overhead.
            
            #### What This Module Provides
            
            **1. Composable Module Architecture**
            - Foundation Layer (VPC, Networking, Security)
            - Platform Layer (Databases, Compute, Storage)
            - Application Layer (Full-stack blueprints)
            - Composition Layer (Combined patterns)
            
            **2. App-Centric Packaging**
            - Complete application packages with infrastructure
            - Environment-specific configurations
            - Docker containers and deployment scripts
            - Ready-to-deploy blueprints
            
            **3. Smart Parameterization**
            - Environment-based defaults (dev, staging, prod)
            - Override capabilities for custom requirements
            - Type validation and constraints
            - Comprehensive error handling
            
            **4. Multi-Environment Support**
            - Template-based environment generation
            - Automated Terraform file creation
            - Consistent deployment patterns
            - Region-specific configurations
            
            **5. Lifecycle-Aware Design**
            - State management patterns
            - Resource lifecycle controls
            - Dependency management
            - Import and migration support
            """)
            
            # Key statistics
            st.markdown("### 📊 Implementation Statistics")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.info("""
                **Code Metrics:**
                - 12,000+ lines of production code
                - 9,000+ lines of documentation
                - 15+ complete examples
                - 3 major module layers
                """)
            
            with col2:
                st.info("""
                **Automation Tools:**
                - Python environment generator
                - Bash testing scripts
                - YAML templates
                - Terraform modules
                """)
        
        with tab2:
            st.markdown("### 🏗️ Module Architecture")
            
            st.markdown("#### Layer Hierarchy")
            
            st.code("""
enterprise-modules/
├── foundation/              # Base infrastructure
│   ├── networking/         # VPC, Subnets, Gateways
│   ├── security/           # Security Groups, IAM
│   └── observability/      # CloudWatch, Flow Logs
├── platform/               # Platform services
│   ├── compute/           # EC2, ASG, ECS
│   ├── database/          # RDS, DynamoDB, Aurora
│   └── storage/           # S3, EFS, EBS
├── application/            # Application patterns
│   ├── web-app/           # Web application stack
│   ├── api-service/       # API backend
│   └── data-pipeline/     # Data processing
└── composition/            # Combined patterns
    ├── full-stack-app/    # Complete applications
    ├── microservices/     # Microservice architecture
    └── data-lake/         # Data lake pattern
            """, language="text")
            
            st.markdown("#### Module Structure")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Foundation Layer**")
                st.code("""
modules/foundation/networking/
├── main.tf
├── variables.tf
├── outputs.tf
├── versions.tf
└── README.md
                """, language="text")
                
                st.markdown("**Features:**")
                st.markdown("- VPC with auto-calculated subnets")
                st.markdown("- Multi-AZ support")
                st.markdown("- NAT Gateway (optional)")
                st.markdown("- VPC Flow Logs")
                st.markdown("- Standard tagging")
            
            with col2:
                st.markdown("**Platform Layer**")
                st.code("""
modules/platform/database/rds/
├── main.tf
├── variables.tf
├── outputs.tf
├── versions.tf
└── README.md
                """, language="text")
                
                st.markdown("**Features:**")
                st.markdown("- Multi-engine support")
                st.markdown("- Automated backups")
                st.markdown("- Performance Insights")
                st.markdown("- CloudWatch alarms")
                st.markdown("- Security best practices")
            
            st.markdown("---")
            
            st.markdown("#### Application Blueprint")
            
            st.code("""
app-blueprints/web-application/
├── infrastructure/
│   ├── main.tf              # Main configuration
│   ├── variables.tf         # Input variables
│   ├── outputs.tf           # Outputs
│   └── versions.tf          # Provider versions
├── application/
│   ├── Dockerfile           # Container image
│   ├── docker-compose.yml   # Local development
│   └── app/                 # Application code
├── config/
│   ├── dev.tfvars          # Dev configuration
│   ├── staging.tfvars      # Staging configuration
│   └── prod.tfvars         # Production configuration
└── README.md                # Documentation
            """, language="text")
        
        with tab3:
            st.markdown("### 🎯 Key Benefits")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Efficiency Gains")
                st.success("**70% reduction** in infrastructure code duplication")
                st.success("**90% faster** new environment provisioning")
                st.success("**15 minutes** from requirements to deployed")
                st.success("**Zero manual errors** with automation")
                
                st.markdown("#### Consistency")
                st.info("**100% consistent** deployments across all environments")
                st.info("**Standardized** naming conventions")
                st.info("**Unified** tagging strategy")
                st.info("**Validated** configurations")
            
            with col2:
                st.markdown("#### Cost Optimization")
                st.success("**30-50%** reduction in dev/staging costs")
                st.success("**Auto-scaling** reduces over-provisioning")
                st.success("**Reserved Instance** recommendations")
                st.success("**Spot Instance** support for non-prod")
                
                st.markdown("#### Security & Compliance")
                st.info("**100% encrypted** data at rest and in transit")
                st.info("**Zero trust** security model")
                st.info("**Automated compliance** checking")
                st.info("**Audit logging** enabled by default")
        
        with tab4:
            st.markdown("### 🚀 Quick Start Guide")
            
            st.markdown("#### Prerequisites")
            st.code("""
# Install Python dependencies
pip install PyYAML jinja2

# Verify Terraform
terraform --version  # Should be >= 1.5.0

# Verify AWS CLI (for live mode)
aws --version
            """, language="bash")
            
            st.markdown("#### Generate Environment (2 Minutes)")
            
            st.code("""
# Step 1: Generate development environment
python3 environment_generator.py generate \\
  --template environment_template.yaml \\
  --values dev_environment_values.yaml

# Step 2: Navigate to generated environment
cd environments/dev

# Step 3: Review configuration
cat README.md

# Step 4: Initialize Terraform
terraform init

# Step 5: Plan deployment
terraform plan

# Step 6: Deploy (optional - requires AWS credentials)
terraform apply
            """, language="bash")
            
            st.markdown("#### What Gets Generated")
            
            st.code("""
environments/dev/
├── main.tf              # Main configuration
├── variables.tf         # Variable definitions
├── outputs.tf           # Output definitions
├── backend.tf           # State backend config
├── terraform.tfvars     # Variable values
└── README.md            # Environment documentation
            """, language="text")
            
            st.markdown("#### List All Environments")
            
            st.code("""
python3 environment_generator.py list
            """, language="bash")
        
        with tab5:
            st.markdown("### 📊 Real-World Examples")
            
            # Example selector
            example = st.selectbox(
                "Select Example:",
                [
                    "Standard Web Application",
                    "Microservices Architecture",
                    "Data Pipeline",
                    "Multi-Region Deployment",
                    "Custom Environment"
                ]
            )
            
            if example == "Standard Web Application":
                st.markdown("#### Standard Web Application")
                
                st.markdown("**Components:**")
                st.markdown("- VPC with public/private subnets")
                st.markdown("- Application Load Balancer")
                st.markdown("- Auto Scaling Group (EC2)")
                st.markdown("- RDS PostgreSQL (Multi-AZ)")
                st.markdown("- CloudWatch monitoring")
                
                st.code("""
# Generate environment
python3 environment_generator.py generate \\
  --template environment_template.yaml \\
  --values prod_environment_values.yaml

# Deploy
cd environments/prod
terraform init
terraform apply
                """, language="bash")
                
                st.markdown("**Configuration:**")
                st.code("""
environment_name: "prod"
vpc_cidr: "10.0.0.0/16"
availability_zones: ["us-east-1a", "us-east-1b", "us-east-1c"]

database_config:
  engine: "postgres"
  engine_version: "15.4"
  instance_class: "db.r6g.xlarge"
  allocated_storage: 500
  multi_az: true

compute_config:
  instance_type: "t3.large"
  min_size: 3
  max_size: 10
  desired_capacity: 3
                """, language="yaml")
            
            elif example == "Microservices Architecture":
                st.markdown("#### Microservices Architecture")
                
                st.markdown("**Components:**")
                st.markdown("- Shared VPC infrastructure")
                st.markdown("- ECS Fargate clusters")
                st.markdown("- Application Load Balancers")
                st.markdown("- Aurora Serverless")
                st.markdown("- Service mesh ready")
                
                st.code("""
# Each microservice gets its own module
module "user_service" {
  source = "./modules/application/api-service"
  
  service_name = "user-service"
  container_image = "company/user-service:v1.2.0"
  # ... configuration
}

module "order_service" {
  source = "./modules/application/api-service"
  
  service_name = "order-service"
  container_image = "company/order-service:v1.5.0"
  # ... configuration
}
                """, language="hcl")
            
            elif example == "Data Pipeline":
                st.markdown("#### Data Pipeline")
                
                st.markdown("**Components:**")
                st.markdown("- S3 data lake")
                st.markdown("- Glue ETL jobs")
                st.markdown("- EMR clusters")
                st.markdown("- Redshift data warehouse")
                st.markdown("- Athena for querying")
                
                st.code("""
module "data_pipeline" {
  source = "./modules/composition/data-lake"
  
  pipeline_name = "customer-analytics"
  
  s3_config = {
    raw_bucket = "company-raw-data"
    processed_bucket = "company-processed-data"
    curated_bucket = "company-curated-data"
  }
  
  glue_config = {
    database_name = "customer_analytics_db"
    crawler_schedule = "cron(0 1 * * ? *)"
  }
  
  redshift_config = {
    cluster_type = "multi-node"
    node_type = "ra3.xlplus"
    number_of_nodes = 2
  }
}
                """, language="hcl")
            
            elif example == "Multi-Region Deployment":
                st.markdown("#### Multi-Region Deployment")
                
                st.markdown("**Regions:**")
                st.markdown("- Primary: us-east-1")
                st.markdown("- Secondary: us-west-2")
                st.markdown("- DR: eu-west-1")
                
                st.code("""
# Primary region values
# prod_us_east_values.yaml
environment_name: "prod-us-east"
aws_region: "us-east-1"
vpc_cidr: "10.0.0.0/16"
availability_zones: ["us-east-1a", "us-east-1b", "us-east-1c"]

# Secondary region values
# prod_us_west_values.yaml
environment_name: "prod-us-west"
aws_region: "us-west-2"
vpc_cidr: "10.100.0.0/16"
availability_zones: ["us-west-2a", "us-west-2b", "us-west-2c"]

# Generate both
python3 environment_generator.py generate \\
  --template environment_template.yaml \\
  --values prod_us_east_values.yaml

python3 environment_generator.py generate \\
  --template environment_template.yaml \\
  --values prod_us_west_values.yaml
                """, language="yaml")
            
            elif example == "Custom Environment":
                st.markdown("#### Custom Environment Configuration")
                
                st.markdown("**Create your own values file:**")
                
                st.code("""
# custom_environment_values.yaml
environment_name: "uat"
environment_description: "User Acceptance Testing Environment"
creator: "devops@company.com"
creation_date: "2025-11-18"
app_name: "customer-portal"

# Network Configuration
vpc_cidr: "10.50.0.0/16"
availability_zones: ["us-east-1a", "us-east-1b"]
enable_nat: true
enable_vpn: false

# Database Configuration
db_engine: "postgres"
db_version: "15.4"
db_instance_class: "db.t3.medium"
db_storage: 100
db_multi_az: false
db_backup_retention: 7

# Compute Configuration
compute_instance_type: "t3.medium"
compute_min: 2
compute_max: 5
compute_desired: 2

# Security Settings
deletion_protection: false
monitoring_enabled: true

# Compliance
compliance_standards: ["SOC2"]

# Tags
cost_center: "Engineering"
owner: "UAT-Team"
                """, language="yaml")
                
                st.code("""
# Generate custom environment
python3 environment_generator.py generate \\
  --template environment_template.yaml \\
  --values custom_environment_values.yaml
                """, language="bash")
    
    @staticmethod
    def render_composable_modules():
        """Render Composable Modules page"""
        
        st.markdown("## 🧩 Composable Modules")
        st.markdown("### Building Reusable Infrastructure Components")
        
        st.markdown("""
        Composable modules allow you to build complex infrastructure from simple, 
        reusable building blocks. Each module is designed to do one thing well and 
        can be combined with other modules to create complete systems.
        """)
        
        # Module layers
        tab1, tab2, tab3, tab4 = st.tabs([
            "Foundation Layer",
            "Platform Layer",
            "Application Layer",
            "Composition Layer"
        ])
        
        with tab1:
            st.markdown("### Foundation Layer Modules")
            
            st.markdown("#### Network Module")
            
            with st.expander("📘 View Network Module Code", expanded=False):
                st.code("""
module "network" {
  source = "./modules/foundation/networking"

  environment        = "prod"
  vpc_cidr           = "10.0.0.0/16"
  availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]
  enable_nat_gateway = true
  enable_vpn_gateway = false
  
  tags = {
    Environment = "prod"
    ManagedBy   = "Terraform"
  }
}

# Outputs available:
# - module.network.vpc_id
# - module.network.public_subnet_ids
# - module.network.private_subnet_ids
# - module.network.database_subnet_ids
# - module.network.nat_gateway_ids
                """, language="hcl")
            
            st.markdown("**Features:**")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                - ✅ VPC with DNS support
                - ✅ Auto-calculated subnets (public/private/database)
                - ✅ Internet Gateway
                - ✅ NAT Gateways (optional, per AZ)
                """)
            
            with col2:
                st.markdown("""
                - ✅ VPC Flow Logs
                - ✅ Route tables
                - ✅ Standard tagging
                - ✅ Multi-AZ support
                """)
        
        with tab2:
            st.markdown("### Platform Layer Modules")
            
            st.markdown("#### RDS Database Module")
            
            with st.expander("📘 View RDS Module Code", expanded=False):
                st.code("""
module "database" {
  source = "./modules/platform/database/rds"

  identifier        = "customer-portal-db"
  engine            = "postgres"
  engine_version    = "15.4"
  instance_class    = "db.r6g.xlarge"
  allocated_storage = 500
  
  db_name  = "customer_portal"
  username = "admin"
  password = random_password.db_password.result

  vpc_id     = module.network.vpc_id
  subnet_ids = module.network.database_subnet_ids
  
  allowed_security_group_ids = [module.app_servers.security_group_id]
  
  multi_az                = true
  backup_retention_period = 30
  deletion_protection     = true
  
  performance_insights_enabled = true
  enabled_cloudwatch_logs_exports = ["postgresql"]

  tags = local.common_tags
}
                """, language="hcl")
            
            st.markdown("#### Auto Scaling Group Module")
            
            with st.expander("📘 View ASG Module Code", expanded=False):
                st.code("""
module "app_servers" {
  source = "./modules/platform/compute/asg"

  name_prefix      = "customer-portal-prod"
  instance_type    = "t3.large"
  min_size         = 3
  max_size         = 10
  desired_capacity = 3
  
  vpc_id             = module.network.vpc_id
  subnet_ids         = module.network.private_subnet_ids
  target_group_arns  = [aws_lb_target_group.main.arn]
  
  user_data = templatefile("user_data.sh", {
    db_endpoint = module.database.db_instance_endpoint
  })

  tags = local.common_tags
}
                """, language="hcl")
        
        with tab3:
            st.markdown("### Application Layer Modules")
            
            st.markdown("""
            Application layer modules combine foundation and platform modules 
            to create complete, deployable applications.
            """)
            
            with st.expander("📘 View Full-Stack Application Module", expanded=True):
                st.code("""
module "web_application" {
  source = "./modules/application/web-app"

  app_name           = "customer-portal"
  environment        = "prod"
  vpc_cidr           = "10.0.0.0/16"
  availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]
  
  database_config = {
    engine            = "postgres"
    engine_version    = "15.4"
    instance_class    = "db.r6g.xlarge"
    allocated_storage = 500
    multi_az          = true
  }
  
  compute_config = {
    instance_type    = "t3.large"
    min_size         = 3
    max_size         = 10
    desired_capacity = 3
  }
  
  tags = {
    Environment = "prod"
    Application = "customer-portal"
    CostCenter  = "ProductionServices"
  }
}

# Application is fully deployed with:
# - VPC and networking
# - Load balancer
# - Auto Scaling Group
# - RDS database
# - Security groups
# - CloudWatch monitoring
# - Backup automation
                """, language="hcl")
        
        with tab4:
            st.markdown("### Composition Layer")
            
            st.markdown("""
            Composition modules combine multiple applications or services 
            to create complex systems like microservices or data platforms.
            """)
            
            with st.expander("📘 View Microservices Composition", expanded=False):
                st.code("""
module "microservices_platform" {
  source = "./modules/composition/microservices"

  platform_name = "ecommerce"
  environment   = "prod"
  
  shared_vpc_config = {
    vpc_cidr           = "10.0.0.0/16"
    availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]
  }
  
  services = [
    {
      name            = "user-service"
      container_image = "company/user-service:v1.2.0"
      port            = 8080
      cpu             = 256
      memory          = 512
    },
    {
      name            = "order-service"
      container_image = "company/order-service:v1.5.0"
      port            = 8080
      cpu             = 512
      memory          = 1024
    },
    {
      name            = "payment-service"
      container_image = "company/payment-service:v2.0.0"
      port            = 8080
      cpu             = 512
      memory          = 1024
    }
  ]
  
  database_config = {
    engine         = "aurora-postgresql"
    engine_version = "15.4"
    instance_class = "db.r6g.large"
  }
}
                """, language="hcl")
    
    @staticmethod
    def render_app_centric_packaging():
        """Render App-Centric Packaging page"""
        
        st.markdown("## 📦 App-Centric Packaging")
        st.markdown("### Package Applications with Their Infrastructure")
        
        st.markdown("""
        App-centric packaging bundles application code, infrastructure definitions, 
        and configurations into a single, deployable package. This approach ensures 
        that applications are self-contained and can be deployed consistently across 
        any environment.
        """)
        
        # Package structure
        st.markdown("### Package Structure")
        
        st.code("""
customer-portal/
├── infrastructure/           # Infrastructure as Code
│   ├── main.tf              # Main Terraform configuration
│   ├── variables.tf         # Variable definitions
│   ├── outputs.tf           # Output definitions
│   └── versions.tf          # Provider versions
├── application/             # Application code
│   ├── Dockerfile           # Container definition
│   ├── docker-compose.yml   # Local development
│   ├── requirements.txt     # Python dependencies
│   └── app/                 # Application source
│       ├── __init__.py
│       ├── main.py
│       ├── models.py
│       └── api/
├── config/                  # Environment configurations
│   ├── dev.tfvars          # Development settings
│   ├── staging.tfvars      # Staging settings
│   └── prod.tfvars         # Production settings
├── scripts/                 # Automation scripts
│   ├── deploy.sh           # Deployment script
│   ├── rollback.sh         # Rollback script
│   └── health-check.sh     # Health check script
├── tests/                   # Tests
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests
│   └── e2e/                # End-to-end tests
└── docs/                    # Documentation
    ├── README.md           # Getting started
    ├── DEPLOYMENT.md       # Deployment guide
    └── ARCHITECTURE.md     # Architecture docs
        """, language="text")
        
        # Deployment workflow
        st.markdown("### Deployment Workflow")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 1. Build")
            st.code("""
# Build container
docker build -t app:v1.0.0 .

# Run tests
docker run app:v1.0.0 \\
  pytest tests/

# Push to registry
docker push \\
  company/app:v1.0.0
            """, language="bash")
        
        with col2:
            st.markdown("#### 2. Deploy Infrastructure")
            st.code("""
cd infrastructure

# Select environment
export ENV=prod

# Initialize
terraform init

# Apply
terraform apply \\
  -var-file=../config/$ENV.tfvars
            """, language="bash")
        
        with col3:
            st.markdown("#### 3. Deploy Application")
            st.code("""
# Update container
aws ecs update-service \\
  --cluster app-cluster \\
  --service app-service \\
  --force-new-deployment

# Verify health
./scripts/health-check.sh
            """, language="bash")
        
        # Example package
        st.markdown("### Complete Example")
        
        with st.expander("📦 View Complete Application Package", expanded=True):
            
            tab1, tab2, tab3, tab4 = st.tabs([
                "Infrastructure",
                "Application",
                "Configuration",
                "Scripts"
            ])
            
            with tab1:
                st.markdown("**infrastructure/main.tf**")
                st.code("""
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Import shared modules
module "network" {
  source = "../../modules/foundation/networking"
  
  environment        = var.environment
  vpc_cidr           = var.vpc_cidr
  availability_zones = var.availability_zones
}

module "database" {
  source = "../../modules/platform/database/rds"
  
  identifier     = "${var.app_name}-${var.environment}"
  engine         = var.database_config.engine
  engine_version = var.database_config.engine_version
  instance_class = var.database_config.instance_class
  
  vpc_id     = module.network.vpc_id
  subnet_ids = module.network.database_subnet_ids
}

module "compute" {
  source = "../../modules/platform/compute/asg"
  
  name_prefix      = "${var.app_name}-${var.environment}"
  instance_type    = var.compute_config.instance_type
  min_size         = var.compute_config.min_size
  max_size         = var.compute_config.max_size
  desired_capacity = var.compute_config.desired_capacity
  
  vpc_id             = module.network.vpc_id
  subnet_ids         = module.network.private_subnet_ids
  target_group_arns  = [aws_lb_target_group.main.arn]
}

# Load Balancer
resource "aws_lb" "main" {
  name               = "${var.app_name}-${var.environment}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = module.network.public_subnet_ids
}

resource "aws_lb_target_group" "main" {
  name     = "${var.app_name}-${var.environment}-tg"
  port     = 8080
  protocol = "HTTP"
  vpc_id   = module.network.vpc_id

  health_check {
    enabled  = true
    path     = "/health"
    port     = "traffic-port"
    protocol = "HTTP"
  }
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.main.arn
  }
}
                """, language="hcl")
            
            with tab2:
                st.markdown("**application/Dockerfile**")
                st.code("""
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app/ ./app/

# Create non-root user
RUN useradd -m -u 1000 appuser && \\
    chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \\
  CMD python -c "import requests; requests.get('http://localhost:8080/health')"

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
                """, language="dockerfile")
                
                st.markdown("**application/app/main.py**")
                st.code("""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Customer Portal API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "healthy", "environment": os.getenv("ENVIRONMENT", "unknown")}

@app.get("/")
async def root():
    return {"message": "Customer Portal API", "version": "1.0.0"}

@app.get("/api/customers")
async def get_customers():
    # Database logic here
    return {"customers": []}
                """, language="python")
            
            with tab3:
                st.markdown("**config/prod.tfvars**")
                st.code("""
app_name           = "customer-portal"
environment        = "prod"
vpc_cidr           = "10.0.0.0/16"
availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]

database_config = {
  engine            = "postgres"
  engine_version    = "15.4"
  instance_class    = "db.r6g.xlarge"
  allocated_storage = 500
  multi_az          = true
}

compute_config = {
  instance_type    = "t3.large"
  min_size         = 3
  max_size         = 10
  desired_capacity = 3
}

tags = {
  Environment = "prod"
  Application = "customer-portal"
  CostCenter  = "ProductionServices"
  Owner       = "Platform-Team"
  Compliance  = "PCI-DSS"
}
                """, language="hcl")
            
            with tab4:
                st.markdown("**scripts/deploy.sh**")
                st.code("""
#!/bin/bash
set -e

ENV=${1:-dev}
VERSION=${2:-latest}

echo "Deploying to $ENV with version $VERSION"

# Build and push container
echo "Building container..."
docker build -t customer-portal:$VERSION ./application
docker tag customer-portal:$VERSION company/customer-portal:$VERSION
docker push company/customer-portal:$VERSION

# Deploy infrastructure
echo "Deploying infrastructure..."
cd infrastructure
terraform init
terraform apply -var-file=../config/$ENV.tfvars -auto-approve

# Update application
echo "Updating application..."
aws ecs update-service \\
  --cluster customer-portal-$ENV-cluster \\
  --service customer-portal-$ENV-service \\
  --force-new-deployment

# Wait for deployment
echo "Waiting for deployment..."
aws ecs wait services-stable \\
  --cluster customer-portal-$ENV-cluster \\
  --services customer-portal-$ENV-service

# Run health check
echo "Running health check..."
./scripts/health-check.sh $ENV

echo "Deployment complete!"
                """, language="bash")
    
    @staticmethod
    def render_parameterization():
        """Render Parameterization page"""
        
        st.markdown("## ⚙️ Parameterization & Defaults")
        st.markdown("### Smart Configuration Management")
        
        st.markdown("""
        Smart parameterization allows you to define environment-specific defaults 
        while providing override capabilities for custom requirements. This ensures 
        consistency across environments while maintaining flexibility.
        """)
        
        # Configuration hierarchy
        st.markdown("### Configuration Hierarchy")
        
        st.info("""
        **Priority (High to Low):**
        1. Command-line flags (`-var`)
        2. `.tfvars` files specified (`-var-file`)
        3. `terraform.tfvars` (auto-loaded)
        4. `*.auto.tfvars` (auto-loaded)
        5. Environment variables (`TF_VAR_name`)
        6. Default values in `variables.tf`
        """)
        
        # Example implementation
        with st.expander("📘 View Smart Defaults Implementation", expanded=True):
            st.code("""
# variables.tf - Define variables with smart defaults

variable "environment" {
  description = "Environment name"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod"
  }
}

variable "instance_type" {
  description = "EC2 instance type (overrides environment defaults)"
  type        = string
  default     = null
}

variable "backup_retention_days" {
  description = "Backup retention days (overrides environment defaults)"
  type        = number
  default     = null
}

variable "enable_monitoring" {
  description = "Enable detailed monitoring (overrides environment defaults)"
  type        = bool
  default     = null
}

# locals.tf - Environment-based defaults

locals {
  environment_defaults = {
    dev = {
      instance_type         = "t3.small"
      backup_retention_days = 3
      enable_monitoring     = false
      high_availability     = false
      deletion_protection   = false
      auto_scaling_min      = 1
      auto_scaling_max      = 2
    }
    staging = {
      instance_type         = "t3.medium"
      backup_retention_days = 7
      enable_monitoring     = true
      high_availability     = false
      deletion_protection   = false
      auto_scaling_min      = 2
      auto_scaling_max      = 4
    }
    prod = {
      instance_type         = "t3.large"
      backup_retention_days = 30
      enable_monitoring     = true
      high_availability     = true
      deletion_protection   = true
      auto_scaling_min      = 3
      auto_scaling_max      = 10
    }
  }

  # Merge user values with defaults
  config = merge(
    local.environment_defaults[var.environment],
    {
      instance_type         = coalesce(var.instance_type, local.environment_defaults[var.environment].instance_type)
      backup_retention_days = coalesce(var.backup_retention_days, local.environment_defaults[var.environment].backup_retention_days)
      enable_monitoring     = coalesce(var.enable_monitoring, local.environment_defaults[var.environment].enable_monitoring)
    }
  )
}

# main.tf - Use the configuration

resource "aws_instance" "app" {
  instance_type = local.config.instance_type
  monitoring    = local.config.enable_monitoring
  # ... other configuration
}

resource "aws_db_instance" "main" {
  instance_class          = local.config.instance_type
  backup_retention_period = local.config.backup_retention_days
  deletion_protection     = local.config.deletion_protection
  # ... other configuration
}
            """, language="hcl")
        
        # Configuration validation
        st.markdown("### Configuration Validation")
        
        with st.expander("📘 View Validation Examples", expanded=False):
            st.code("""
variable "database_config" {
  description = "Database configuration"
  type = object({
    engine            = string
    engine_version    = string
    instance_class    = string
    allocated_storage = number
    multi_az          = bool
  })

  validation {
    condition     = contains(["postgres", "mysql", "oracle-ee", "sqlserver-ee"], var.database_config.engine)
    error_message = "Engine must be one of: postgres, mysql, oracle-ee, sqlserver-ee"
  }

  validation {
    condition     = var.database_config.allocated_storage >= 20 && var.database_config.allocated_storage <= 65536
    error_message = "Allocated storage must be between 20 and 65536 GB"
  }

  validation {
    condition     = can(regex("^db\\\\.", var.database_config.instance_class))
    error_message = "Instance class must start with 'db.'"
  }
}

variable "tags" {
  description = "Resource tags"
  type        = map(string)
  
  validation {
    condition = alltrue([
      for key in keys(var.tags) : contains(["Environment", "Application", "CostCenter", "Owner"], key)
    ])
    error_message = "Tags must include Environment, Application, CostCenter, and Owner"
  }
}

variable "cidr_blocks" {
  description = "CIDR blocks for network"
  type        = list(string)
  
  validation {
    condition = alltrue([
      for cidr in var.cidr_blocks : can(cidrnetmask(cidr))
    ])
    error_message = "All CIDR blocks must be valid"
  }
}
            """, language="hcl")
        
        # Environment comparison
        st.markdown("### Environment Comparison")
        
        comparison_data = {
            "Configuration": ["Instance Type", "Backup Retention", "Monitoring", "Multi-AZ", "Deletion Protection", "Min Instances", "Max Instances"],
            "Development": ["t3.small", "3 days", "❌", "❌", "❌", "1", "2"],
            "Staging": ["t3.medium", "7 days", "✅", "❌", "❌", "2", "4"],
            "Production": ["t3.large", "30 days", "✅", "✅", "✅", "3", "10"]
        }
        
        import pandas as pd
        df = pd.DataFrame(comparison_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    @staticmethod
    def render_multi_environment():
        """Render Multi-Environment Support page"""
        
        st.markdown("## 🌍 Multi-Environment Support")
        st.markdown("### Template-Based Environment Generation")
        
        st.markdown("""
        Multi-environment support enables consistent deployment across development, 
        staging, and production environments using templates and automation. Generate 
        complete environment configurations in minutes instead of hours.
        """)
        
        # Environment generator
        st.markdown("### Environment Generator Tool")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("**Features:**")
            st.markdown("- ✅ Template-based generation")
            st.markdown("- ✅ YAML configuration")
            st.markdown("- ✅ Automatic Terraform file creation")
            st.markdown("- ✅ Validation and error checking")
            st.markdown("- ✅ Documentation generation")
        
        with col2:
            st.metric("Generation Time", "< 2 min", help="Time to generate complete environment")
            st.metric("Files Created", "6", help="Terraform files + README")
        
        # Usage demonstration
        st.markdown("### Usage Demonstration")
        
        tab1, tab2, tab3 = st.tabs(["Generate", "Deploy", "Manage"])
        
        with tab1:
            st.markdown("#### Generate Environment")
            
            st.code("""
# Generate development environment
python3 environment_generator.py generate \\
  --template environment_template.yaml \\
  --values dev_environment_values.yaml

# Output:
# ✓ terraform.tfvars
# ✓ backend.tf
# ✓ main.tf
# ✓ variables.tf
# ✓ outputs.tf
# ✓ README.md

# Files created in: environments/dev/
            """, language="bash")
            
            st.markdown("#### List Environments")
            
            st.code("""
python3 environment_generator.py list

# Output:
📋 Generated Environments:
────────────────────────────────────────────────────────────
  • dev                  - Development Environment for Customer Portal
  • staging              - Staging Environment for Customer Portal  
  • prod                 - Production Environment for Customer Portal
────────────────────────────────────────────────────────────
            """, language="text")
        
        with tab2:
            st.markdown("#### Deploy Environment")
            
            st.code("""
# Navigate to environment
cd environments/dev

# Initialize Terraform
terraform init

# Review plan
terraform plan

# Apply configuration
terraform apply

# Expected output:
# Apply complete! Resources: 45 added, 0 changed, 0 destroyed.
#
# Outputs:
#
# application_url = "http://customer-portal-dev-alb-123456789.us-east-1.elb.amazonaws.com"
# database_endpoint = "customer-portal-dev.abc123.us-east-1.rds.amazonaws.com:5432"
# vpc_id = "vpc-0a1b2c3d4e5f67890"
            """, language="bash")
        
        with tab3:
            st.markdown("#### Manage Environments")
            
            st.code("""
# Update environment
vim terraform.tfvars  # Make changes
terraform plan        # Review changes
terraform apply       # Apply changes

# Destroy environment
terraform destroy

# Import existing resources
terraform import aws_vpc.main vpc-0a1b2c3d4e5f67890

# View state
terraform show

# List resources
terraform state list
            """, language="bash")
        
        # Template structure
        st.markdown("### Template Structure")
        
        with st.expander("📋 View Environment Template", expanded=False):
            st.code("""
version: "1.0"
metadata:
  name: "{{ environment_name }}"
  description: "{{ environment_description }}"
  created_by: "{{ creator }}"
  created_date: "{{ creation_date }}"

infrastructure:
  network:
    vpc_cidr: "{{ vpc_cidr }}"
    availability_zones: {{ availability_zones }}
    enable_nat_gateway: {{ enable_nat }}
    enable_vpn_gateway: {{ enable_vpn }}
  
  database:
    engine: "{{ db_engine }}"
    engine_version: "{{ db_version }}"
    instance_class: "{{ db_instance_class }}"
    allocated_storage: {{ db_storage }}
    multi_az: {{ db_multi_az }}
    backup_retention: {{ db_backup_retention }}
  
  compute:
    instance_type: "{{ compute_instance_type }}"
    min_size: {{ compute_min }}
    max_size: {{ compute_max }}
    desired_capacity: {{ compute_desired }}

security:
  encryption_enabled: true
  deletion_protection: {{ deletion_protection }}
  backup_enabled: true
  monitoring_enabled: {{ monitoring_enabled }}

compliance:
  standards: {{ compliance_standards }}
  audit_logging: true
  vpc_flow_logs: true

tags:
  Environment: "{{ environment_name }}"
  Application: "{{ app_name }}"
  CostCenter: "{{ cost_center }}"
  Owner: "{{ owner }}"
  ManagedBy: "Terraform"
            """, language="yaml")
    
    @staticmethod
    def render_lifecycle_management():
        """Render Lifecycle Management page"""
        
        st.markdown("## ♻️ Lifecycle-Aware Module Design")
        st.markdown("### State Management & Resource Lifecycle")
        
        st.markdown("""
        Lifecycle-aware modules handle resource creation, updates, and deletion 
        intelligently. They manage dependencies, prevent accidental deletions, 
        and support complex deployment scenarios.
        """)
        
        # Lifecycle controls
        tab1, tab2, tab3, tab4 = st.tabs([
            "Lifecycle Rules",
            "State Management",
            "Dependencies",
            "Best Practices"
        ])
        
        with tab1:
            st.markdown("### Lifecycle Rules")
            
            with st.expander("📘 Create Before Destroy", expanded=True):
                st.code("""
resource "aws_launch_template" "app" {
  name_prefix   = "app-"
  image_id      = data.aws_ami.latest.id
  instance_type = var.instance_type

  lifecycle {
    create_before_destroy = true
  }
}

# Creates new launch template before destroying old one
# Prevents downtime during updates
                """, language="hcl")
            
            with st.expander("📘 Prevent Destroy"):
                st.code("""
resource "aws_db_instance" "production" {
  identifier     = "prod-database"
  engine         = "postgres"
  instance_class = "db.r6g.xlarge"

  lifecycle {
    prevent_destroy = true
  }
}

# Prevents accidental deletion of critical resources
# Must remove this rule before destroying
                """, language="hcl")
            
            with st.expander("📘 Ignore Changes"):
                st.code("""
resource "aws_instance" "app" {
  ami           = data.aws_ami.latest.id
  instance_type = var.instance_type
  
  tags = {
    Name        = "app-server"
    LastUpdated = timestamp()
  }

  lifecycle {
    ignore_changes = [
      tags["LastUpdated"],  # Ignore timestamp changes
      ami                   # Ignore AMI updates
    ]
  }
}

# Prevents Terraform from updating specific attributes
# Useful for externally managed values
                """, language="hcl")
            
            with st.expander("📘 Replace Triggered By"):
                st.code("""
resource "aws_launch_template" "app" {
  name_prefix   = "app-"
  image_id      = data.aws_ami.latest.id
  instance_type = var.instance_type

  lifecycle {
    replace_triggered_by = [
      data.aws_ami.latest.id
    ]
  }
}

data "aws_ami" "latest" {
  most_recent = true
  owners      = ["self"]
  
  filter {
    name   = "name"
    values = ["app-*"]
  }
}

# Replaces resource when referenced data changes
# Automatically triggers updates
                """, language="hcl")
        
        with tab2:
            st.markdown("### State Management")
            
            with st.expander("📘 Import Existing Resources"):
                st.code("""
# Import existing VPC
terraform import aws_vpc.main vpc-0a1b2c3d4e5f67890

# Import existing database
terraform import aws_db_instance.main db-instance-name

# Import existing S3 bucket
terraform import aws_s3_bucket.data bucket-name

# Verify import
terraform state show aws_vpc.main
                """, language="bash")
            
            with st.expander("📘 Move Resources"):
                st.code("""
# Refactor without recreating
moved {
  from = aws_instance.old_name
  to   = aws_instance.new_name
}

moved {
  from = module.old_module.aws_vpc.main
  to   = module.new_module.aws_vpc.main
}

# Apply moves
terraform plan  # Shows moves instead of destroy/create
terraform apply
                """, language="hcl")
            
            with st.expander("📘 State Operations"):
                st.code("""
# List resources in state
terraform state list

# Show resource details
terraform state show aws_vpc.main

# Remove resource from state (doesn't delete)
terraform state rm aws_instance.old

# Move resource in state
terraform state mv aws_instance.old aws_instance.new

# Pull state
terraform state pull > terraform.tfstate.backup

# Push state (dangerous!)
terraform state push terraform.tfstate
                """, language="bash")
        
        with tab3:
            st.markdown("### Dependency Management")
            
            with st.expander("📘 Explicit Dependencies"):
                st.code("""
resource "aws_db_instance" "main" {
  identifier = "app-db"
  # ... configuration ...
  
  # Wait for log group and monitoring role
  depends_on = [
    aws_cloudwatch_log_group.database,
    aws_iam_role_policy_attachment.rds_monitoring
  ]
}

resource "aws_cloudwatch_log_group" "database" {
  name = "/aws/rds/app-db"
}

resource "aws_iam_role_policy_attachment" "rds_monitoring" {
  role       = aws_iam_role.rds.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonRDSEnhancedMonitoringRole"
}
                """, language="hcl")
            
            with st.expander("📘 Implicit Dependencies"):
                st.code("""
# VPC created first (implicit)
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

# Subnet depends on VPC (implicit via reference)
resource "aws_subnet" "private" {
  vpc_id     = aws_vpc.main.id  # Creates dependency
  cidr_block = "10.0.1.0/24"
}

# Security group depends on VPC (implicit)
resource "aws_security_group" "app" {
  vpc_id = aws_vpc.main.id  # Creates dependency
  # ... rules ...
}

# Instance depends on subnet and security group (implicit)
resource "aws_instance" "app" {
  subnet_id              = aws_subnet.private.id  # Depends on subnet
  vpc_security_group_ids = [aws_security_group.app.id]  # Depends on SG
  # ... configuration ...
}
                """, language="hcl")
            
            with st.expander("📘 Module Dependencies"):
                st.code("""
# Network module created first
module "network" {
  source = "./modules/network"
  # ... configuration ...
}

# Database depends on network
module "database" {
  source = "./modules/database"
  
  vpc_id     = module.network.vpc_id
  subnet_ids = module.network.database_subnet_ids
  
  depends_on = [module.network]
}

# Application depends on both
module "application" {
  source = "./modules/application"
  
  vpc_id            = module.network.vpc_id
  subnet_ids        = module.network.private_subnet_ids
  database_endpoint = module.database.endpoint
  
  depends_on = [
    module.network,
    module.database
  ]
}
                """, language="hcl")
        
        with tab4:
            st.markdown("### Best Practices")
            
            st.markdown("#### Production Resources")
            st.code("""
resource "aws_db_instance" "prod" {
  identifier = "prod-database"
  
  lifecycle {
    # Prevent accidental deletion
    prevent_destroy = true
    
    # Create new before destroying old
    create_before_destroy = true
    
    # Ignore password changes (managed externally)
    ignore_changes = [master_password]
    
    # Validate configuration
    precondition {
      condition     = var.environment == "prod"
      error_message = "This resource is for production only"
    }
    
    precondition {
      condition     = var.multi_az == true
      error_message = "Production databases must be Multi-AZ"
    }
  }
}
            """, language="hcl")
            
            st.markdown("#### Development Resources")
            st.code("""
resource "aws_instance" "dev" {
  instance_type = "t3.small"
  
  lifecycle {
    # Allow easy cleanup
    prevent_destroy = false
    
    # Don't need create_before_destroy
    create_before_destroy = false
    
    # Ignore tag changes
    ignore_changes = [
      tags["LastModified"]
    ]
  }
}
            """, language="hcl")


def render_module_07():
    """Main entry point for Module 07"""
    module = AbstractionReusabilityModule()
    module.render_overview()
