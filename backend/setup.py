#!/usr/bin/env python3
"""
Setup script for Spotify → YouTube Music Playlist Importer
"""

import os
import sys
import subprocess
import json

def run_command(command, cwd=None):
    """Run a command and return the result"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True, cwd=cwd)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def check_node_version():
    """Check if Node.js is installed"""
    success, output = run_command("node --version")
    if success:
        print(f"✅ Node.js {output.strip()} is installed")
        return True
    else:
        print("❌ Node.js is not installed. Please install Node.js v16 or higher")
        return False

def setup_frontend():
    """Setup the React frontend"""
    print("\n🔧 Setting up React frontend...")
    
    # Install npm dependencies
    success, output = run_command("npm install")
    if success:
        print("✅ Frontend dependencies installed")
    else:
        print("❌ Failed to install frontend dependencies")
        print(output)
        return False
    
    return True

def setup_backend():
    """Setup the FastAPI backend"""
    print("\n🔧 Setting up FastAPI backend...")
    
    # Create backend directory if it doesn't exist
    if not os.path.exists("backend"):
        os.makedirs("backend")
    
    # Change to backend directory
    os.chdir("backend")
    
    # Create virtual environment
    success, output = run_command("python -m venv venv")
    if success:
        print("✅ Virtual environment created")
    else:
        print("❌ Failed to create virtual environment")
        print(output)
        return False
    
    # Install Python dependencies
    if os.name == 'nt':  # Windows
        pip_cmd = "venv\\Scripts\\pip install -r requirements.txt"
    else:  # Unix/Linux/Mac
        pip_cmd = "venv/bin/pip install -r requirements.txt"
    
    success, output = run_command(pip_cmd)
    if success:
        print("✅ Backend dependencies installed")
    else:
        print("❌ Failed to install backend dependencies")
        print(output)
        return False
    
    return True

def create_env_file():
    """Create a .env file template"""
    env_content = """# Spotify OAuth Configuration
# Replace with your actual Spotify Client ID
SPOTIFY_CLIENT_ID=your_spotify_client_id_here

# Backend Configuration
BACKEND_URL=http://localhost:8000

# Frontend Configuration
REACT_APP_BACKEND_URL=http://localhost:8000
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    print("✅ Created .env template file")

def main():
    """Main setup function"""
    print("🚀 Setting up Spotify → YouTube Music Playlist Importer")
    print("=" * 50)
    
    # Check prerequisites
    if not check_python_version():
        return False
    
    if not check_node_version():
        return False
    
    # Setup frontend
    if not setup_frontend():
        return False
    
    # Setup backend
    if not setup_backend():
        return False
    
    # Create environment file
    create_env_file()
    
    print("\n" + "=" * 50)
    print("✅ Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Get your Spotify Client ID from https://developer.spotify.com/dashboard")
    print("2. Update the clientId in src/App.js")
    print("3. Run 'cd backend && python -c \"import ytmusicapi; ytmusicapi.setup(filepath='auth_headers.json')\"'")
    print("4. Start the backend: 'cd backend && python main.py'")
    print("5. Start the frontend: 'npm start'")
    print("6. Open http://localhost:3000 in your browser")
    print("\n📖 See README.md for detailed instructions")

if __name__ == "__main__":
    main() 