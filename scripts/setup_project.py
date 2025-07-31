#!/usr/bin/env python3
"""
Project setup script
Sets up the entire project for development
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and handle errors"""
    print(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def setup_backend():
    """Setup backend dependencies"""
    print("\n🐍 Setting up backend...")
    backend_dir = Path(__file__).parent.parent / "src" / "backend"
    
    # Install Python dependencies
    success, output = run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], cwd=backend_dir)
    if not success:
        print(f"❌ Failed to install Python dependencies: {output}")
        return False
    
    print("✅ Backend setup complete!")
    return True

def setup_frontend():
    """Setup frontend dependencies"""
    print("\n📦 Setting up frontend...")
    frontend_dir = Path(__file__).parent.parent / "src" / "frontend"
    
    if not frontend_dir.exists():
        print("⚠️  Frontend directory not found, skipping...")
        return True
    
    # Install Node dependencies
    success, output = run_command(["npm", "install"], cwd=frontend_dir)
    if not success:
        print(f"❌ Failed to install Node dependencies: {output}")
        return False
    
    print("✅ Frontend setup complete!")
    return True

def check_credentials():
    """Check if credential files exist"""
    print("\n🔑 Checking credentials...")
    
    credentials_dir = Path(__file__).parent.parent / "credentials"
    youtube_creds = credentials_dir / "youtube_credentials.json"
    env_file = Path(__file__).parent.parent / ".env"
    
    if not youtube_creds.exists():
        print("⚠️  YouTube credentials not found!")
        print("   Please add youtube_credentials.json to credentials/ directory")
        print("   See README.md for instructions")
    else:
        print("✅ YouTube credentials found!")
    
    if not env_file.exists():
        print("⚠️  .env file not found!")
        print("   Please copy .env.example to .env and fill in your values")
    else:
        print("✅ Environment file found!")

def main():
    print("🎵 Playlist Importer - Project Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required!")
        return 1
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Setup backend
    if not setup_backend():
        return 1
    
    # Setup frontend  
    if not setup_frontend():
        return 1
    
    # Check credentials
    check_credentials()
    
    print("\n🎉 Setup complete!")
    print("Next steps:")
    print("1. Set up your .env file with Spotify credentials")
    print("2. Add youtube_credentials.json to credentials/ directory")
    print("3. Run: python scripts/start_dev.py")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())