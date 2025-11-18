# AWS Design & Planning Platform

🏗️ **Enterprise Cloud Architecture & Governance Framework**

A comprehensive Streamlit application for AWS architecture design, planning, and governance powered by Anthropic Claude AI.

[![Streamlit](https://img.shields.io/badge/Streamlit-1.29.0-FF4B4B.svg)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![AWS](https://img.shields.io/badge/AWS-Ready-orange.svg)](https://aws.amazon.com)

## 🌟 Features

### Design & Planning Modules

✅ **Blueprint Definition** - Define reusable architecture blueprints  
✅ **Tagging Standards** - Enforce consistent tagging policies  
✅ **Naming Conventions** - Standardize resource naming  
✅ **Artifact Versioning** - Manage container images and versions  
✅ **IaC Module Registry** - Centralized Infrastructure as Code repository  
✅ **Design-Time Validation** - Pre-deployment compliance checking  

### AI-Powered Features

🤖 **Claude AI Assistant** - AWS architecture guidance  
📄 **Documentation Generation** - Automated technical docs  
🔍 **Code Review** - IaC template analysis  
💰 **Cost Estimation** - Architecture cost analysis  

### Operation Modes

📋 **Demo Mode** (Default) - Explore with sample data, no credentials needed  
🟢 **Live Mode** - Connect to real AWS services  

## 🚀 Quick Start

### Deploy to Streamlit Cloud (Recommended)

1. **Fork this repository** to your GitHub account

2. **Go to** [Streamlit Cloud](https://share.streamlit.io/)

3. **Click "New app"**

4. **Select:**
   - Repository: `your-username/aws-design-platform`
   - Branch: `main`
   - Main file: `streamlit_app.py`

5. **Click "Deploy"** ✨

Your app will be live in 2-3 minutes!

### Local Development

```bash
# Clone repository
git clone <your-repo-url>
cd aws-design-platform

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run streamlit_app.py
```

Access at: http://localhost:8501

## 📁 File Structure

```
aws-design-platform/
├── streamlit_app.py          # Main application (entry point)
├── design_planning.py         # All 6 Design & Planning modules
├── config.py                  # Configuration management
├── anthropic_helper.py        # Claude AI integration
├── demo_data.py              # Demo data provider
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

**Flat structure optimized for Streamlit Cloud and GitHub!**

## 🎯 Usage

### Demo Mode (No Setup Required)

1. App starts in Demo Mode by default
2. Explore all features with sample data
3. No AWS credentials needed
4. No API keys required

### Live Mode

1. **Toggle to Live Mode** in sidebar
2. **Configure AWS credentials** (optional)
3. **Add Anthropic API key** for AI features (optional)

### Get Anthropic API Key

1. Visit: https://console.anthropic.com/
2. Sign up or log in
3. Go to "API Keys"
4. Create new key
5. Paste in sidebar under "Claude AI Configuration"

## 📊 Demo Data Included

- ✅ 4 Architecture Blueprints
- ✅ Tag Policies & Validation Results
- ✅ Naming Convention Rules
- ✅ Container Images & Versions  
- ✅ 87+ IaC Modules (Terraform, CloudFormation, CDK)
- ✅ Security Scan Results
- ✅ Validation Rules & Issues

## 🔧 Configuration

### Streamlit Cloud Secrets

For AI features, add to Streamlit Cloud secrets:

```toml
ANTHROPIC_API_KEY = "sk-ant-your-key-here"
```

Go to: App settings → Secrets → Add above

### Environment Variables (Local)

Create `.env` file:

```bash
ANTHROPIC_API_KEY=sk-ant-your-key-here
AWS_DEFAULT_REGION=us-east-1
```

## 🎨 Customization

### Modify Demo Data

Edit `demo_data.py` to customize sample data for your organization.

### Add Custom Modules

Add new functions to `design_planning.py` following existing patterns.

### Extend AI Features

Modify `anthropic_helper.py` to add new AI-powered capabilities.

## 🔒 Security

- API keys stored in session state only
- Never commit credentials to git
- Use Streamlit Cloud secrets for production
- Follow AWS IAM best practices

## 📖 Module Guide

### 1. Blueprint Definition

Create and manage reusable architecture templates:
- Infrastructure patterns
- Security baselines
- Compliance mappings
- IaC templates

### 2. Tagging Standards

Enforce consistent tagging:
- Define mandatory tags
- Validation rules
- Compliance reporting
- Auto-remediation

### 3. Naming Conventions

Standardize resource naming:
- Pattern definitions
- Validation engine
- Component specifications
- Examples library

### 4. Image/Artifact Versioning

Manage container images:
- Registry management
- Version tracking
- Lifecycle policies
- Security scanning

### 5. IaC Module Registry

Centralized IaC repository:
- 87+ sample modules
- Multi-framework support
- Usage analytics
- Documentation

### 6. Design-Time Validation

Pre-deployment validation:
- Security checks
- Compliance validation
- Cost estimation
- Auto-remediation

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 License

MIT License - see LICENSE file for details

## 🆘 Support

- **Issues**: Create an issue in GitHub
- **Questions**: Use GitHub Discussions
- **Demo Mode**: Try features without setup

## 🎓 Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Anthropic Claude API](https://docs.anthropic.com/)
- [AWS Well-Architected](https://aws.amazon.com/architecture/well-architected/)

## ⭐ Star History

If you find this useful, please star the repository!

---

**Built with ❤️ for AWS Enterprise Architecture**

**Version**: 1.0.0  
**Status**: Production Ready  
**Deploy**: Streamlit Cloud Compatible  
