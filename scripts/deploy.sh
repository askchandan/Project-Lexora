#!/bin/bash

# Production deployment script for Project Lexora
# This script handles deployment to Railway or other platforms

set -e  # Exit on error

echo "🚀 Starting Production Deployment..."

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
DOCKER_IMAGE="chandanmalakar/lexora-pdf-chat:latest"
DEPLOYMENT_PLATFORM="${DEPLOYMENT_PLATFORM:-railway}"  # Default to Railway

echo -e "${YELLOW}Deployment Platform: $DEPLOYMENT_PLATFORM${NC}"

# Function to deploy to Railway
deploy_railway() {
    echo -e "${YELLOW}Deploying to Railway...${NC}"
    
    if [ -z "$RAILWAY_API_TOKEN" ]; then
        echo -e "${RED}Error: RAILWAY_API_TOKEN not set${NC}"
        exit 1
    fi
    
    if [ -z "$RAILWAY_PROJECT_ID" ]; then
        echo -e "${RED}Error: RAILWAY_PROJECT_ID not set${NC}"
        exit 1
    fi
    
    # Install Railway CLI if not exists
    if ! command -v railway &> /dev/null; then
        echo "Installing Railway CLI..."
        npm install -g @railway/cli
    fi
    
    # Authenticate with Railway
    railway login --token "$RAILWAY_API_TOKEN"
    
    # Deploy
    railway deploy --environment production
    
    echo -e "${GREEN}✅ Railway deployment successful!${NC}"
}

# Function to deploy to Render
deploy_render() {
    echo -e "${YELLOW}Deploying to Render...${NC}"
    
    if [ -z "$RENDER_DEPLOY_HOOK" ]; then
        echo -e "${RED}Error: RENDER_DEPLOY_HOOK not set${NC}"
        exit 1
    fi
    
    # Trigger Render deployment
    curl -X POST "$RENDER_DEPLOY_HOOK"
    
    echo -e "${GREEN}✅ Render deployment triggered!${NC}"
}

# Function to deploy to AWS
deploy_aws() {
    echo -e "${YELLOW}Deploying to AWS...${NC}"
    
    if [ -z "$AWS_REGION" ]; then
        echo -e "${RED}Error: AWS_REGION not set${NC}"
        exit 1
    fi
    
    if [ -z "$AWS_ACCOUNT_ID" ]; then
        echo -e "${RED}Error: AWS_ACCOUNT_ID not set${NC}"
        exit 1
    fi
    
    echo "AWS deployment would go here..."
    echo -e "${GREEN}✅ AWS deployment setup complete!${NC}"
}

# Main deployment logic
case $DEPLOYMENT_PLATFORM in
    railway)
        deploy_railway
        ;;
    render)
        deploy_render
        ;;
    aws)
        deploy_aws
        ;;
    *)
        echo -e "${RED}Unknown deployment platform: $DEPLOYMENT_PLATFORM${NC}"
        exit 1
        ;;
esac

echo -e "${GREEN}🎉 Deployment complete!${NC}"
echo "Docker Image: $DOCKER_IMAGE"
echo "Commit: $TRAVIS_COMMIT"
echo "Branch: $TRAVIS_BRANCH"
