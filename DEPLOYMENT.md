# 🚀 Deployment Guide for Streamlit Cloud

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `immobilien-rechner` (or your preferred name)
3. Description: "Real Estate Investment Calculator - Cashflow, Taxes & Opportunity Costs"
4. **Make it PUBLIC** (required for free Streamlit Cloud)
5. **DO NOT** check "Add a README file" or any other initialization options
6. Click "Create repository"

## Step 2: Push Your Code to GitHub

After creating the repo, GitHub will show you a URL like:
`https://github.com/YOUR_USERNAME/immobilien-rechner.git`

Run these commands in your terminal (replace YOUR_USERNAME with your actual GitHub username):

```bash
cd "/Users/mkn501/Library/CloudStorage/GoogleDrive-minkngu@gmail.com/Meine Ablage/VS/RE"

git remote add origin https://github.com/YOUR_USERNAME/immobilien-rechner.git
git branch -M main
git push -u origin main
```

You may be prompted to authenticate with GitHub. Use your GitHub username and a Personal Access Token (not your password).

### Creating a Personal Access Token (if needed):
1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name like "Streamlit Deploy"
4. Check the "repo" scope
5. Click "Generate token"
6. Copy the token and use it as your password when pushing

## Step 3: Deploy to Streamlit Cloud

1. Go to https://share.streamlit.io
2. Sign in with your GitHub account
3. Click "New app"
4. Fill in the form:
   - **Repository:** YOUR_USERNAME/immobilien-rechner
   - **Branch:** main
   - **Main file path:** app.py
5. Click "Deploy!"

## Step 4: Wait for Deployment

Streamlit Cloud will:
- Install dependencies from `requirements.txt`
- Start your app
- Give you a public URL like: `https://YOUR_USERNAME-immobilien-rechner.streamlit.app`

This usually takes 2-3 minutes.

## Step 5: Share Your App! 🎉

Once deployed, you'll get a public URL that you can share with anyone!

## Troubleshooting

### If deployment fails:
1. Check the logs in Streamlit Cloud dashboard
2. Common issues:
   - Missing dependencies in `requirements.txt`
   - Import errors (make sure all files are pushed)
   - Python version issues (Streamlit Cloud uses Python 3.9+)

### If you need to update the app:
```bash
# Make your changes
git add .
git commit -m "Update app"
git push
```
Streamlit Cloud will automatically redeploy when you push to GitHub!

## Current Files Ready for Deployment

✅ `app.py` - Main application
✅ `localization.py` - Text translations (DE/EN)
✅ `pdf_generator.py` - PDF generation logic
✅ `max_re_price.py` - Calculation functions
✅ `requirements.txt` - Dependencies

All files are committed and ready to push!
