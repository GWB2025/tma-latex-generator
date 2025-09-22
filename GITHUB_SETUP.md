# 🚀 Upload TMA Generator to GitHub

## Quick Setup Guide

### 1️⃣ Create GitHub Repository

1. Go to [github.com](https://github.com) and sign in
2. Click **"+"** → **"New repository"**
3. Repository settings:
   - **Name**: `tma-latex-generator` (or your choice)
   - **Description**: `Professional TMA LaTeX Generator for Overleaf - generates structured academic assignment files`
   - **Public** or **Private** (your choice)
   - **Don't initialize** with README/gitignore (we have them)

### 2️⃣ Connect & Upload

**After creating the repository, run these commands in PowerShell:**

```powershell
# Navigate to project directory (if not already there)
cd "Path\To\Your\Project\Directory"

# Add GitHub remote (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Rename branch to main (GitHub standard)
git branch -M main

# Push to GitHub
git push -u origin main
```

### 3️⃣ Authentication Options

**Option A: Personal Access Token**
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with `repo` scope
3. Use token as password when prompted

**Option B: GitHub CLI (Easier)**
```powershell
# Install GitHub CLI, then:
gh auth login
gh repo create tma-latex-generator --public --source=. --remote=origin --push
```

## 🌟 Alternative Hosting Options

### GitLab
- Similar to GitHub
- Go to [gitlab.com](https://gitlab.com)
- Create new project → Import project → Repository by URL

### Bitbucket
- Go to [bitbucket.org](https://bitbucket.org)
- Create repository → Import repository

### Azure DevOps
- Go to [dev.azure.com](https://dev.azure.com)
- Create new project → Repos → Import

## 📋 What Gets Uploaded

✅ **Included:**
- `tma_generator_gui.py` (main application)
- `*.md` (all documentation)
- `*.sty` (LaTeX style files)
- `.gitignore` (project file management)

❌ **Excluded (by .gitignore):**
- Temporary test directories (`junk.*`)
- Python cache files
- Personal config files
- LaTeX auxiliary files

## 🎯 Recommended Repository Settings

**Public Repository Benefits:**
- Showcase your work
- Contribute to open source community
- Easy sharing and collaboration
- GitHub Actions CI/CD available

**Private Repository Benefits:**
- Keep code confidential
- Control access
- Still get full GitHub features

## 🔧 After Upload

1. **Add a README badge**: GitHub will suggest adding repository badges
2. **Enable Issues**: For bug reports and feature requests
3. **Set up GitHub Pages**: For project documentation hosting
4. **Add topics**: Tag with `latex`, `overleaf`, `academic`, `python`, `gui`, `tma`

## 💡 Pro Tips

- **Branch Protection**: Set up branch protection rules for main branch
- **GitHub Actions**: Automate testing and releases
- **Releases**: Create versioned releases for major updates
- **Wiki**: Use GitHub Wiki for extended documentation

## 🆘 Need Help?

If you encounter issues:
1. Check GitHub's [Git Handbook](https://guides.github.com/introduction/git-handbook/)
2. Use `git status` to check repository state
3. Use `git log --oneline` to see commit history
4. GitHub has excellent documentation and community support

**Your project is ready for the world! 🌟**