#!/usr/bin/env python3
"""
Travis CI Configuration Setup Script for Project Lexora
Helps configure environment variables and credentials securely
"""

import os
import sys
import json
from pathlib import Path
from getpass import getpass

class TravisSetup:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.travis_file = self.project_root / ".travis.yml"
        self.config = {}
    
    def print_header(self, text):
        """Print formatted header"""
        print(f"\n{'='*60}")
        print(f"  {text}")
        print(f"{'='*60}\n")
    
    def docker_hub_setup(self):
        """Collect Docker Hub credentials"""
        self.print_header("Docker Hub Credentials")
        
        print("You need a Docker Hub Personal Access Token (not your password)")
        print("Get it from: https://hub.docker.com/settings/security\n")
        
        self.config['DOCKER_USERNAME'] = input("Docker Hub Username: ").strip()
        self.config['DOCKER_PASSWORD'] = getpass("Docker Hub Personal Access Token: ")
        self.config['DOCKER_EMAIL'] = input("Docker Hub Email: ").strip()
        
        print("\n✅ Docker Hub credentials collected")
    
    def platform_setup(self):
        """Select and configure deployment platform"""
        self.print_header("Production Deployment Platform")
        
        print("Select your deployment platform:\n")
        print("1. Railway (Recommended) - Easiest, free tier available")
        print("2. Render - Also easy, free tier available")
        print("3. AWS - More complex, pay-as-you-go")
        
        choice = input("\nSelect (1-3): ").strip()
        
        if choice == "1":
            self.railway_setup()
        elif choice == "2":
            self.render_setup()
        elif choice == "3":
            self.aws_setup()
        else:
            print("❌ Invalid selection")
            sys.exit(1)
    
    def railway_setup(self):
        """Configure Railway deployment"""
        print("\n📍 Railway Configuration")
        print("Get your credentials from: https://railway.app\n")
        print("1. Go to Account Settings → API Tokens")
        print("2. Create new token")
        print("3. Copy token (starts with 'eyJ')\n")
        
        self.config['RAILWAY_API_TOKEN'] = getpass("Railway API Token: ")
        self.config['RAILWAY_PROJECT_ID'] = input("Railway Project ID: ").strip()
        self.config['DEPLOYMENT_PLATFORM'] = 'railway'
        
        print("\n✅ Railway configuration complete")
    
    def render_setup(self):
        """Configure Render deployment"""
        print("\n📍 Render Configuration")
        print("Get your credentials from: https://render.com\n")
        print("1. Create/Select your Web Service")
        print("2. Go to Settings → Deploy Hook")
        print("3. Copy the Deploy Hook URL\n")
        
        self.config['RENDER_DEPLOY_HOOK'] = input("Render Deploy Hook URL: ").strip()
        self.config['DEPLOYMENT_PLATFORM'] = 'render'
        
        print("\n✅ Render configuration complete")
    
    def aws_setup(self):
        """Configure AWS deployment"""
        print("\n📍 AWS Configuration")
        print("Get your credentials from AWS IAM\n")
        
        self.config['AWS_REGION'] = input("AWS Region (e.g., us-east-1): ").strip()
        self.config['AWS_ACCOUNT_ID'] = input("AWS Account ID: ").strip()
        self.config['AWS_ACCESS_KEY_ID'] = input("AWS Access Key ID: ").strip()
        self.config['AWS_SECRET_ACCESS_KEY'] = getpass("AWS Secret Access Key: ")
        self.config['DEPLOYMENT_PLATFORM'] = 'aws'
        
        print("\n✅ AWS configuration complete")
    
    def print_instructions(self):
        """Print setup instructions"""
        self.print_header("Next Steps - Important!")
        
        print("You have two options:\n")
        print("OPTION 1: Using Travis CLI (Recommended)")
        print("-" * 60)
        print("1. Install Travis CLI:")
        print("   gem install travis")
        print("   # or: brew install travis (macOS)")
        print("\n2. Login to Travis CI:")
        print("   cd " + str(self.project_root))
        print("   travis login --github")
        print("\n3. Add encrypted environment variables:")
        
        env_vars = [
            ('DOCKER_USERNAME', self.config.get('DOCKER_USERNAME')),
            ('DOCKER_PASSWORD', self.config.get('DOCKER_PASSWORD')),
            ('DOCKER_EMAIL', self.config.get('DOCKER_EMAIL')),
        ]
        
        # Add platform-specific variables
        if self.config.get('DEPLOYMENT_PLATFORM') == 'railway':
            env_vars.extend([
                ('RAILWAY_API_TOKEN', self.config.get('RAILWAY_API_TOKEN')),
                ('RAILWAY_PROJECT_ID', self.config.get('RAILWAY_PROJECT_ID')),
            ])
        elif self.config.get('DEPLOYMENT_PLATFORM') == 'render':
            env_vars.append(('RENDER_DEPLOY_HOOK', self.config.get('RENDER_DEPLOY_HOOK')))
        elif self.config.get('DEPLOYMENT_PLATFORM') == 'aws':
            env_vars.extend([
                ('AWS_REGION', self.config.get('AWS_REGION')),
                ('AWS_ACCOUNT_ID', self.config.get('AWS_ACCOUNT_ID')),
                ('AWS_ACCESS_KEY_ID', self.config.get('AWS_ACCESS_KEY_ID')),
                ('AWS_SECRET_ACCESS_KEY', self.config.get('AWS_SECRET_ACCESS_KEY')),
            ])
        
        for var_name, var_value in env_vars:
            if var_value:
                print(f"   travis encrypt \"{var_name}={var_value}\" --add env.global")
        
        print("\n4. Commit and push:")
        print("   git add .travis.yml")
        print("   git commit -m 'Add Travis CI encrypted credentials'")
        print("   git push origin main")
        
        print("\n\nOPTION 2: Manual Travis CI Dashboard")
        print("-" * 60)
        print("1. Go to: https://www.travis-ci.com")
        print("2. Find your Project-Lexora repository")
        print("3. Click Settings")
        print("4. Add these Environment Variables:\n")
        
        for var_name, var_value in env_vars:
            if var_value:
                # Show only first 10 chars of sensitive data
                display_value = var_value[:10] + "..." if len(var_value) > 10 else var_value
                print(f"   {var_name} = {display_value}")
        
        print("\n5. Save changes")
        print("6. Commit and push any change to trigger first build")
        
        print("\n\n" + "="*60)
        print("Configuration Summary:")
        print("="*60)
        print(json.dumps(
            {k: v[:10] + "..." if len(v) > 10 else v for k, v in self.config.items()},
            indent=2
        ))
    
    def run(self):
        """Run the setup wizard"""
        self.print_header("Travis CI Setup Wizard")
        print(f"Project Root: {self.project_root}\n")
        
        self.docker_hub_setup()
        self.platform_setup()
        self.print_instructions()
        
        print("\n✅ Setup wizard complete! Follow the instructions above.\n")

if __name__ == "__main__":
    try:
        setup = TravisSetup()
        setup.run()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
