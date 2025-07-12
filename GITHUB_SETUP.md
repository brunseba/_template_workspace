# GitHub Integration Setup Guide

This guide helps you enable GitHub-dependent plugins when you move from the template to a real GitHub repository.

## Overview

The MkDocs templates have GitHub-dependent plugins commented out by default to avoid authentication issues when used as templates. Once you have a real GitHub repository, you can enable these plugins for enhanced functionality.

## Plugins to Enable

### 1. Git Revision Date Localized Plugin

Shows when pages were last updated based on git commits.

**Enable in your `mkdocs.yml`:**
```yaml
plugins:
  - git-revision-date-localized:
      enable_creation_date: true
      type: date
      timezone: UTC
      locale: en
      fallback_to_build_date: true
```

### 2. Git Committers Plugin

Shows contributors for each page based on git history.

**Enable in your `mkdocs.yml`:**
```yaml
plugins:
  - git-committers:
      repository: yourusername/your-repository
      branch: main
      token: !ENV [MKDOCS_GIT_COMMITTERS_APIKEY, GITHUB_TOKEN]
```

## Setup Steps

### Step 1: Create GitHub Repository

1. Create a new repository on GitHub
2. Push your documentation to the repository:
   ```bash
   git remote add origin https://github.com/yourusername/your-repository.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Configure GitHub Token (for git-committers)

1. **Create a GitHub Personal Access Token:**
   - Go to GitHub Settings > Developer settings > Personal access tokens
   - Click "Generate new token (classic)"
   - Select scopes: `public_repo` (for public repos) or `repo` (for private repos)
   - Copy the generated token

2. **Set environment variable:**
   ```bash
   # Option 1: Export in your shell
   export GITHUB_TOKEN="your_token_here"
   
   # Option 2: Create .env file (add to .gitignore!)
   echo "GITHUB_TOKEN=your_token_here" >> .env
   
   # Option 3: Set in CI/CD environment variables
   ```

### Step 3: Update mkdocs.yml

1. **Update repository information:**
   ```yaml
   site_name: Your Project Name
   site_url: https://yourusername.github.io/your-repository
   repo_name: yourusername/your-repository
   repo_url: https://github.com/yourusername/your-repository
   ```

2. **Uncomment and configure git plugins:**
   ```yaml
   plugins:
     - search
     - git-revision-date-localized:
         enable_creation_date: true
         type: date
         timezone: UTC
         locale: en
         fallback_to_build_date: true
     - git-committers:
         repository: yourusername/your-repository
         branch: main
         token: !ENV [GITHUB_TOKEN]
   ```

### Step 4: Update Metadata

Update `.metadata.yaml` with your project information:
```yaml
project:
  name: "Your Project Name"
  repository: "https://github.com/yourusername/your-repository"
  documentation: "https://yourusername.github.io/your-repository/"
```

### Step 5: Test Configuration

```bash
# Test locally
task serve

# Build and validate
task validate

# Deploy to GitHub Pages
task deploy-gh-pages
```

## GitHub Pages Deployment

### Automatic Deployment with GitHub Actions

Create `.github/workflows/docs.yml`:
```yaml
name: Deploy Documentation

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      
      - name: Install dependencies
        run: |
          pip install mkdocs mkdocs-material
          pip install -r requirements.txt
      
      - name: Deploy to GitHub Pages
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: mkdocs gh-deploy --force
```

### Manual Deployment

```bash
# Deploy to GitHub Pages
task deploy-gh-pages
```

## Troubleshooting

### Common Issues

1. **Bad Credentials Error**
   - Ensure your GitHub token has correct permissions
   - Check token is not expired
   - Verify environment variable is set correctly

2. **Repository Not Found**
   - Verify repository name in `mkdocs.yml`
   - Check repository is public or token has access to private repos

3. **Git History Issues**
   - Ensure repository has commit history
   - Check branch name is correct (main vs master)

### Environment Variables

You can use different environment variable names:
```yaml
plugins:
  - git-committers:
      token: !ENV [MKDOCS_GIT_COMMITTERS_APIKEY, GITHUB_TOKEN, GH_TOKEN]
```

## Security Best Practices

1. **Never commit tokens to version control**
2. **Use environment variables or secrets management**
3. **Limit token permissions to minimum required**
4. **Regularly rotate tokens**
5. **Use different tokens for different environments**

## Plugin Options

### Git Revision Date Localized

```yaml
plugins:
  - git-revision-date-localized:
      enable_creation_date: true
      type: timeago           # date, datetime, iso_date, iso_datetime, timeago
      timezone: Europe/Paris  # or UTC
      locale: en             # language for timeago
      fallback_to_build_date: true
      exclude:
        - index.md
```

### Git Committers

```yaml
plugins:
  - git-committers:
      repository: owner/repo
      branch: main
      docs_path: docs/
      cache_dir: .git-committers-cache
      enabled: !ENV [CI, false]  # Only enable in CI
```

## Testing Your Setup

1. **Local testing:**
   ```bash
   task serve
   # Check that git information appears on pages
   ```

2. **Build testing:**
   ```bash
   task build-strict
   # Should build without errors
   ```

3. **Deployment testing:**
   ```bash
   task deploy-gh-pages
   # Should deploy successfully to GitHub Pages
   ```

---

For more information, see:
- [MkDocs Material Documentation](https://squidfunk.github.io/mkdocs-material/)
- [Git Revision Date Plugin](https://github.com/timvink/mkdocs-git-revision-date-localized-plugin)
- [Git Committers Plugin](https://github.com/byrnereese/mkdocs-git-committers-plugin)
