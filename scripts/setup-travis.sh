#!/bin/bash

# Quick setup script for Travis CI configuration
# This script helps you generate encrypted environment variables

echo "🚀 Travis CI Setup Assistant for Project Lexora"
echo "=================================================="
echo ""

# Check if travis CLI is installed
if ! command -v travis &> /dev/null; then
    echo "⚠️  Travis CLI not found. Installing..."
    gem install travis
fi

echo "Step 1: Docker Hub Credentials"
echo "==============================="
read -p "Enter your Docker Hub username: " DOCKER_USERNAME
read -sp "Enter your Docker Hub Personal Access Token (not password): " DOCKER_PASSWORD
echo ""
read -p "Enter your Docker Hub email: " DOCKER_EMAIL

echo ""
echo "Step 2: Production Platform Selection"
echo "======================================"
echo "1. Railway (Recommended)"
echo "2. Render"
echo "3. AWS"
read -p "Select deployment platform (1-3): " PLATFORM_CHOICE

case $PLATFORM_CHOICE in
    1)
        echo "Setting up Railway..."
        read -p "Enter your Railway API Token: " RAILWAY_API_TOKEN
        read -p "Enter your Railway Project ID: " RAILWAY_PROJECT_ID
        DEPLOYMENT_PLATFORM="railway"
        ;;
    2)
        echo "Setting up Render..."
        read -p "Enter your Render Deploy Hook URL: " RENDER_DEPLOY_HOOK
        DEPLOYMENT_PLATFORM="render"
        ;;
    3)
        echo "Setting up AWS..."
        read -p "Enter AWS Region (e.g., us-east-1): " AWS_REGION
        read -p "Enter AWS Account ID: " AWS_ACCOUNT_ID
        read -p "Enter AWS Access Key ID: " AWS_ACCESS_KEY_ID
        read -sp "Enter AWS Secret Access Key: " AWS_SECRET_ACCESS_KEY
        DEPLOYMENT_PLATFORM="aws"
        ;;
    *)
        echo "Invalid selection"
        exit 1
        ;;
esac

echo ""
echo "Step 3: Encrypting Credentials"
echo "==============================="
echo ""

# Create a temporary environment file
temp_file=$(mktemp)

cat > "$temp_file" << EOF
DOCKER_USERNAME=$DOCKER_USERNAME
DOCKER_PASSWORD=$DOCKER_PASSWORD
DOCKER_EMAIL=$DOCKER_EMAIL
DEPLOYMENT_PLATFORM=$DEPLOYMENT_PLATFORM
EOF

case $DEPLOYMENT_PLATFORM in
    railway)
        echo "RAILWAY_API_TOKEN=$RAILWAY_API_TOKEN" >> "$temp_file"
        echo "RAILWAY_PROJECT_ID=$RAILWAY_PROJECT_ID" >> "$temp_file"
        ;;
    render)
        echo "RENDER_DEPLOY_HOOK=$RENDER_DEPLOY_HOOK" >> "$temp_file"
        ;;
    aws)
        echo "AWS_REGION=$AWS_REGION" >> "$temp_file"
        echo "AWS_ACCOUNT_ID=$AWS_ACCOUNT_ID" >> "$temp_file"
        echo "AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID" >> "$temp_file"
        echo "AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY" >> "$temp_file"
        ;;
esac

echo "Encrypting credentials..."
echo ""
echo "⚠️  Important: The following commands need to be run in your project directory"
echo "Command to run in your terminal:"
echo ""
echo "travis login --github"
echo ""
echo "Then run each of these commands:"
echo ""

# Generate travis encrypt commands
while IFS= read -r line; do
    if [ ! -z "$line" ]; then
        echo "travis encrypt \"$line\" --add env.global"
    fi
done < "$temp_file"

echo ""
echo "✅ After running above commands, your .travis.yml will be automatically updated!"
echo ""
echo "Then run:"
echo "git add .travis.yml"
echo "git commit -m 'Add Travis CI environment variables'"
echo "git push origin main"
echo ""

rm "$temp_file"

echo "Setup Complete! 🎉"
