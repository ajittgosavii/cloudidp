# 🚀 Streamlit Cloud Deployment Guide

Deploy your AWS Design & Planning Platform to Streamlit Cloud in 5 minutes!

## 📋 Prerequisites

- GitHub account
- Streamlit Cloud account (free at https://share.streamlit.io/)
- This repository forked to your GitHub

## 🎯 Step-by-Step Deployment

### Step 1: Prepare Repository

1. **Fork this repository** to your GitHub account
   - Click "Fork" button on GitHub
   - Choose your account

2. **Clone your fork** (optional, for local testing)
   ```bash
   git clone https://github.com/YOUR-USERNAME/aws-design-platform
   cd aws-design-platform
   ```

### Step 2: Deploy to Streamlit Cloud

1. **Go to** [Streamlit Cloud](https://share.streamlit.io/)

2. **Sign in** with GitHub

3. **Click "New app"** button

4. **Configure deployment:**
   - **Repository**: Select `YOUR-USERNAME/aws-design-platform`
   - **Branch**: `main` (or `master`)
   - **Main file path**: `streamlit_app.py`

5. **Advanced settings** (optional):
   - Python version: 3.11 (recommended)
   - Click "Advanced settings" if you need to customize

6. **Click "Deploy!"**

### Step 3: Wait for Deployment

- Streamlit Cloud will:
  - Install dependencies from `requirements.txt`
  - Build the application
  - Start the server
  
- **Duration**: 2-3 minutes for first deployment

### Step 4: Access Your App

Your app will be live at:
```
https://YOUR-APP-NAME.streamlit.app
```

## 🔑 Configure Secrets (Optional)

For AI features, add your Anthropic API key:

1. **Go to app dashboard** on Streamlit Cloud

2. **Click ⚙️ Settings**

3. **Select "Secrets"**

4. **Add secrets** in TOML format:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-your-actual-key-here"
   ```

5. **Click "Save"**

6. **App will restart** automatically

## 🎨 Custom Domain (Optional)

### Free Subdomain

Your app gets a free subdomain:
- `https://your-app-name.streamlit.app`

### Custom Domain

1. **Go to App Settings** → General

2. **Add Custom Domain**

3. **Update your DNS**:
   ```
   CNAME record: yourdomain.com → your-app.streamlit.app
   ```

4. **Wait for SSL** (automatic, ~5 minutes)

## 🔄 Update Your App

### Auto-Deploy (Recommended)

Changes to your GitHub repo automatically deploy:

1. Make changes locally
2. Commit and push:
   ```bash
   git add .
   git commit -m "Update feature"
   git push origin main
   ```
3. Streamlit Cloud auto-deploys (1-2 minutes)

### Manual Deploy

In Streamlit Cloud dashboard:
1. Click "⋮" menu
2. Select "Reboot app"

## 🐛 Troubleshooting

### Deployment Failed

**Check:**
- ✅ `requirements.txt` exists
- ✅ `streamlit_app.py` exists
- ✅ No syntax errors in Python files
- ✅ All imports are available

**View logs:**
- Click "Manage app" → "Logs"

### App Crashes

**Common issues:**
1. **Missing dependency** - Add to `requirements.txt`
2. **Import error** - Check file names match imports
3. **Memory limit** - Optimize data loading

### Can't Find Main File

**Solution:**
- Ensure `streamlit_app.py` is in repository root
- Check file name spelling
- Verify it's not in a subdirectory

### Secrets Not Working

**Check:**
- ✅ TOML syntax is correct
- ✅ No quotes around key names
- ✅ App restarted after adding secrets

## 📊 Monitor Your App

### View Analytics

Streamlit Cloud provides:
- **Viewer count** - Current active users
- **Total views** - Historical usage
- **Logs** - Application output
- **Resources** - CPU/Memory usage

### Access Logs

```
App Dashboard → Manage app → Logs
```

## 🔒 Security Best Practices

### DO:
- ✅ Use Streamlit Secrets for API keys
- ✅ Add `.gitignore` to exclude secrets
- ✅ Use environment-specific configs
- ✅ Enable HTTPS (automatic)

### DON'T:
- ❌ Commit API keys to Git
- ❌ Store secrets in code
- ❌ Push `.env` files
- ❌ Share secret URLs publicly

## 💡 Optimization Tips

### Faster Load Times

1. **Cache data:**
   ```python
   @st.cache_data
   def load_data():
       # Your data loading
   ```

2. **Minimize imports** in main file

3. **Lazy load** heavy libraries

### Reduce Memory

1. **Use demo mode** by default
2. **Clear unused session state**
3. **Optimize data structures**

## 🔧 Advanced Configuration

### Custom Python Version

In Streamlit Cloud settings:
- Advanced settings → Python version
- Choose 3.8, 3.9, 3.10, or 3.11

### Environment Variables

In secrets, add:
```toml
[general]
LOG_LEVEL = "INFO"
DEBUG_MODE = false

[aws]
DEFAULT_REGION = "us-east-1"
```

Access in code:
```python
import streamlit as st
log_level = st.secrets["general"]["LOG_LEVEL"]
```

## 📱 Share Your App

### Public App

- Anyone with link can access
- No authentication required
- Use demo mode for security

### Private App

Streamlit Cloud Community (free tier):
- Apps are public by default

Streamlit Cloud Teams (paid):
- Private apps
- Authentication
- Team workspaces

## 🎯 Success Checklist

After deployment, verify:

- [ ] App loads without errors
- [ ] Demo mode shows sample data
- [ ] All 6 modules are accessible
- [ ] Navigation works correctly
- [ ] Live/Demo toggle functions
- [ ] AI Assistant works (if API key added)

## 🆘 Get Help

### Streamlit Community

- **Forum**: https://discuss.streamlit.io/
- **Docs**: https://docs.streamlit.io/
- **GitHub**: https://github.com/streamlit/streamlit

### App-Specific Issues

- **Create issue** in your repository
- **Check logs** in Streamlit Cloud
- **Test locally** first

## 🚀 Next Steps

After successful deployment:

1. **Test all features** in demo mode
2. **Add API keys** for AI features
3. **Customize** demo data for your org
4. **Share** with your team
5. **Monitor** usage and performance

## 📈 Scaling

### Free Tier Limits

- **1 app** per account
- **1 GB RAM**
- **1 CPU core**
- Public apps only

### Upgrade Options

For production use:
- **Streamlit Cloud Teams**
- **Self-hosted** on AWS/GCP/Azure
- **Docker** deployment

## 🎉 You're Live!

Your AWS Design & Planning Platform is now accessible worldwide!

**Share your app:**
```
https://your-app-name.streamlit.app
```

---

**Questions?** Check the [README.md](README.md) or create an issue.

**Happy Deploying!** 🚀
