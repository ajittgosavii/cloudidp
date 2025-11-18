# ⚡ QUICK SETUP GUIDE

## 🎯 For GitHub + Streamlit Cloud Deployment

### 📁 Files Included (Flat Structure - Streamlit Cloud Ready!)

```
aws_platform_streamlit/
├── streamlit_app.py          ← Main app (START HERE)
├── design_planning.py         ← All 6 modules
├── config.py                  ← Configuration
├── anthropic_helper.py        ← Claude AI
├── demo_data.py              ← Sample data
├── requirements.txt          ← Dependencies
├── README.md                 ← Full docs
├── STREAMLIT_DEPLOY.md       ← Deploy guide
└── .gitignore                ← Git exclusions
```

**✅ FLAT FILE STRUCTURE - No nested folders!**  
**✅ Perfect for GitHub and Streamlit Cloud!**

---

## 🚀 3-Step Deployment

### Step 1: Push to GitHub

```bash
cd aws_platform_streamlit
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR-USERNAME/aws-design-platform.git
git push -u origin main
```

### Step 2: Deploy to Streamlit Cloud

1. Go to: https://share.streamlit.io/
2. Click "New app"
3. Select your repository
4. Main file: `streamlit_app.py`
5. Click "Deploy"

### Step 3: Done! 🎉

Your app is live at:
```
https://your-app-name.streamlit.app
```

---

## 💻 Local Testing (Optional)

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Open: http://localhost:8501

---

## 🔑 Add API Key (Optional)

For AI features:

1. Get key: https://console.anthropic.com/
2. In Streamlit Cloud: Settings → Secrets
3. Add:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-your-key"
   ```

---

## ✨ Features Available

### Demo Mode (Default - No Setup!)
- ✅ 4 Architecture Blueprints
- ✅ Tagging Standards & Validation
- ✅ Naming Conventions
- ✅ Container Images & Versions
- ✅ 87+ IaC Modules
- ✅ Design-Time Validation

### Live Mode (AWS Connection)
- 🟢 Connect to real AWS services
- 🟢 Toggle in sidebar
- 🟢 Requires AWS credentials

### AI Assistant (Optional)
- 🤖 AWS architecture guidance
- 🤖 IaC template generation
- 🤖 Code review
- 🤖 Requires Anthropic API key

---

## 🎮 First-Time Usage

1. **App opens in Demo Mode** ← No setup needed!
2. **Browse Home** to see overview
3. **Click "Blueprint Definition"** to see 4 sample blueprints
4. **Try "Tagging Standards"** to explore policies
5. **Check "IaC Module Registry"** for 87+ modules
6. **Toggle to Live Mode** when ready for AWS

---

## 📊 Module Navigation

| Module | Description |
|--------|-------------|
| 📋 Blueprint Definition | Architecture templates |
| 🏷️ Tagging Standards | Tag policies & validation |
| 📛 Naming Conventions | Resource naming rules |
| 📦 Artifact Versioning | Container image management |
| 📚 IaC Module Registry | 87+ IaC templates |
| ✅ Design Validation | Pre-deployment checks |
| 🤖 AI Assistant | Claude AI integration |

---

## 🐛 Troubleshooting

### Streamlit Cloud Issues

**App won't start:**
- Check `requirements.txt` exists
- Verify `streamlit_app.py` is in root
- View logs in Streamlit Cloud

**Import errors:**
- All imports are relative (no nested modules)
- Files are in root directory
- No folder structure needed

**Demo data not showing:**
- Should work immediately
- Check you're in Demo Mode
- Look at sidebar for mode indicator

### Local Issues

**Module not found:**
```bash
pip install -r requirements.txt --upgrade
```

**Port in use:**
```bash
streamlit run streamlit_app.py --server.port=8502
```

---

## 🎨 Customization

### Change Demo Data
Edit `demo_data.py`:
```python
class DemoDataProvider:
    @staticmethod
    def get_blueprint_library():
        # Add your blueprints here
```

### Add Features
Edit `design_planning.py`:
```python
class DesignPlanningModule:
    @staticmethod
    def render_your_module():
        # Your module code
```

### Modify UI
Edit `streamlit_app.py`:
- Update navigation
- Change colors
- Add pages

---

## 📖 Documentation

| File | Purpose |
|------|---------|
| README.md | Complete documentation |
| STREAMLIT_DEPLOY.md | Detailed deploy guide |
| This file | Quick reference |

---

## ✅ Verification Checklist

After deployment:

- [ ] App loads without errors
- [ ] Demo mode active by default
- [ ] Can see 4 blueprints
- [ ] Navigation works
- [ ] All 6 modules accessible
- [ ] Live/Demo toggle works
- [ ] No hardcoded demo data in live mode

---

## 🎯 Why This Structure?

✅ **Flat structure** - Streamlit Cloud compatible  
✅ **No nested folders** - GitHub friendly  
✅ **All files in root** - Easy imports  
✅ **Relative imports** - No path issues  
✅ **Single entry point** - streamlit_app.py  

---

## 💡 Pro Tips

1. **Always test in Demo Mode first** - No credentials needed
2. **Push to GitHub regularly** - Auto-deploys to Streamlit
3. **Use secrets for API keys** - Never commit to Git
4. **Check Streamlit logs** - For debugging
5. **Start simple** - Add features incrementally

---

## 🆘 Need Help?

- **Deployment issues**: See STREAMLIT_DEPLOY.md
- **Feature questions**: See README.md
- **Code issues**: Check inline comments
- **Community**: https://discuss.streamlit.io/

---

## 🚦 Status Check

Run this locally to verify:
```bash
python -c "import streamlit; import pandas; import requests; print('✅ All dependencies OK')"
```

---

## 🎉 You're Ready!

1. ✅ Files are flat structure
2. ✅ GitHub push ready
3. ✅ Streamlit Cloud compatible
4. ✅ Demo mode works out of box
5. ✅ All 6 modules implemented

**Now deploy and enjoy! 🚀**

---

**File Structure**: FLAT (Streamlit Cloud optimized)  
**Dependencies**: Minimal (3 packages)  
**Setup Time**: 5 minutes  
**Demo Data**: Included  
**Documentation**: Complete  

**Ready to deploy!** 🎯
