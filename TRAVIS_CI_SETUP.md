# Travis CI/CD Setup Guide for Project Lexora

## Overview

This guide explains how to set up Travis CI/CD for automatic testing, Docker image building, and production deployment.

## Prerequisites

1. **GitHub Account** - Your repo is on GitHub
2. **Travis CI Account** - https://www.travis-ci.com
3. **Docker Hub Account** - For storing Docker images
4. **Production Platform Account** - Railway, Render, or AWS

## Step 1: Connect Travis CI to Your Repository

### 1.1 Sign Up and Connect
```bash
# Go to https://www.travis-ci.com
# Sign in with GitHub
# Find your Project-Lexora repository
# Click "Activate" to enable Travis CI
```

### 1.2 Sync Repository
```bash
# In Travis CI dashboard:
# Settings → Repository → Sync account
```

## Step 2: Add Environment Variables to Travis CI

### 2.1 Docker Hub Credentials

```bash
# In Travis CI Dashboard:
# Go to: Project Settings → Environment Variables

# Add these variables:
DOCKER_USERNAME=your_docker_username
DOCKER_PASSWORD=your_docker_password  # Use Personal Access Token, not password
DOCKER_EMAIL=your_docker_email
```

**Important:** Use Docker Personal Access Token instead of password:
1. Go to Docker Hub → Account Settings → Security
2. Create new Personal Access Token
3. Use this token as `DOCKER_PASSWORD`

### 2.2 Production Deployment Credentials

Choose your deployment platform:

#### For Railway:
```
RAILWAY_API_TOKEN=your_railway_api_token
RAILWAY_PROJECT_ID=your_project_id
DEPLOYMENT_PLATFORM=railway
```

#### For Render:
```
RENDER_DEPLOY_HOOK=https://api.render.com/deploy/srv-...
DEPLOYMENT_PLATFORM=render
```

#### For AWS:
```
AWS_REGION=us-east-1
AWS_ACCOUNT_ID=your_account_id
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
DEPLOYMENT_PLATFORM=aws
```

### 2.3 Optional: Slack Notifications

```bash
# Encrypt Slack webhook for notifications
travis encrypt "https://hooks.slack.com/services/YOUR/WEBHOOK/URL" --add notifications.slack
```

## Step 3: Understanding the Travis CI Pipeline

### What Happens on Every Push to `main`:

```
1. Install Python 3.11 & dependencies
   └─ Install requirements.txt
   └─ Install testing tools (pytest, coverage)

2. Run Tests
   └─ Execute tests/ directory
   └─ Generate code coverage report

3. Build Docker Image
   └─ Build from Dockerfile
   └─ Tag with commit SHA and 'latest'

4. Push to Docker Hub
   └─ Log into Docker Hub
   └─ Push image with both tags

5. Deploy to Production (if tests pass)
   └─ Run deploy.sh script
   └─ Deploy to Railway/Render/AWS
```

## Step 4: Configure Production Deployment

### Option A: Deploy to Railway (Recommended)

**Why Railway?**
- Easiest setup
- Direct Docker support
- Built-in database support
- Free tier available

#### Setup Railway:

```bash
# 1. Create Railway account at https://railway.app
# 2. Create new project
# 3. Connect to GitHub repo
# 4. Add environment variables:
#    - OPENAI_API_KEY
#    - Other config from .env.example

# 5. Get Railway API token:
# - Account → API Tokens
# - Create new token
# - Copy token

# 6. Add to Travis CI environment variables:
# - RAILWAY_API_TOKEN
# - RAILWAY_PROJECT_ID
```

**Dockerfile for Railway:**
Your existing Dockerfile is already compatible!

### Option B: Deploy to Render

```bash
# 1. Create Render account at https://render.com
# 2. Create Web Service
# 3. Connect GitHub repo
# 4. Get deploy hook URL from service settings
# 5. Add RENDER_DEPLOY_HOOK to Travis CI
```

### Option C: Deploy to AWS

```bash
# 1. Set up ECR (Elastic Container Registry)
# 2. Configure ECS (Elastic Container Service)
# 3. Add AWS credentials to Travis CI
# 4. Update deploy.sh with AWS deployment logic
```

## Step 5: Local Testing

### Test Locally Before Pushing

```bash
# Install test dependencies
pip install pytest pytest-cov python-dotenv

# Run tests
python -m pytest tests/ -v

# Generate coverage report
python -m pytest tests/ --cov=src --cov-report=html
```

### Test Docker Build Locally

```bash
# Build image
docker build -t lexora-test .

# Run container
docker run -p 5000:5000 lexora-test

# Test it
curl http://localhost:5000/status
```

## Step 6: Monitoring CI/CD

### Check Build Status

```bash
# In Travis CI Dashboard:
# - View recent builds
# - Click on a build to see logs
# - Check for failures in test/build stage
```

### Read Build Logs

```
# Log sections:
1. "before_install" - Setup phase
2. "install" - Dependency installation
3. "before_script" - Test environment setup
4. "script" - Test execution
5. "after_success" - Docker build and push
6. "deploy" - Production deployment
```

## Step 7: Troubleshooting

### Tests Fail on Travis but Pass Locally

```bash
# Check differences:
# 1. Python version (Travis uses 3.11)
# 2. Environment variables (may not be set)
# 3. Database state (use test fixtures)
```

### Docker Push Fails

```bash
# Verify credentials:
# 1. Check DOCKER_USERNAME and DOCKER_PASSWORD
# 2. Ensure Docker Hub token is valid
# 3. Check if image name is correct
```

### Deployment Doesn't Trigger

```bash
# Check:
# 1. All tests passed (build status green)
# 2. Branch is 'main'
# 3. Deployment API tokens are valid
# 4. Deploy script has execute permissions
```

## Step 8: File Permissions

Make deploy.sh executable:

```bash
# On your local machine:
chmod +x scripts/deploy.sh

# Commit and push
git add scripts/deploy.sh
git commit -m "Make deploy script executable"
git push origin main
```

## Step 9: Complete CI/CD Workflow

### For Developers:

```bash
# 1. Make changes locally
git add .
git commit -m "Feature: Add new capability"

# 2. Run local tests
pytest tests/ -v

# 3. Push to GitHub
git push origin main

# 4. Watch Travis CI build (https://www.travis-ci.com)
# - Tests run automatically
# - Docker image builds
# - Deploys to production

# 5. Check deployment
# - Visit production URL
# - Verify everything works
```

## Available Environment Variables in Travis CI

Your scripts can access:
- `$TRAVIS_COMMIT` - Current commit SHA
- `$TRAVIS_BRANCH` - Current branch name
- `$TRAVIS_BUILD_NUMBER` - Build number
- `$DOCKER_IMAGE_NAME` - Docker image name
- `$DOCKER_IMAGE_TAG` - Docker image tag

## Next Steps

1. ✅ Create `.travis.yml` file (already done)
2. ✅ Create `scripts/deploy.sh` file (already done)
3. ⏭️ Add environment variables in Travis CI dashboard
4. ⏭️ Push to GitHub (this triggers first build)
5. ⏭️ Monitor build progress
6. ⏭️ Verify deployment on production

## Quick Start Checklist

- [ ] Travis CI account created
- [ ] Repository connected to Travis CI
- [ ] `.travis.yml` committed and pushed
- [ ] `scripts/deploy.sh` committed and pushed
- [ ] Docker Hub credentials added to Travis CI
- [ ] Production platform selected (Railway/Render/AWS)
- [ ] Production credentials added to Travis CI
- [ ] First build triggered
- [ ] Tests passing
- [ ] Docker image building
- [ ] Deployment successful
- [ ] Production app accessible

## Support

For issues:
1. Check Travis CI build logs
2. Review this guide
3. Consult platform documentation (Railway/Render/AWS)
4. Check GitHub Issues

---

**Status**: Ready for deployment! 🚀
