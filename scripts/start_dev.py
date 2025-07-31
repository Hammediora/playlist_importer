#!/usr/bin/env python3
"""
Development startup script
Starts both backend and frontend in development mode
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def start_backend():
    """Start the backend development server"""
    backend_dir = Path(__file__).parent.parent / "src" / "backend"
    os.chdir(backend_dir)
    
    print("🚀 Starting backend server...")
    return subprocess.Popen([
        sys.executable, "main.py"
    ], env={**os.environ, "DEBUG": "True"})

def start_frontend():
    """Start the frontend development server"""
    frontend_dir = Path(__file__).parent.parent / "src" / "frontend"
    os.chdir(frontend_dir)
    
    print("🚀 Starting frontend server...")
    return subprocess.Popen(["npm", "start"])

def main():
    print("🎵 Playlist Importer - Development Mode")
    print("=" * 50)
    
    try:
        # Start backend
        backend_process = start_backend()
        time.sleep(2)  # Give backend time to start
        
        # Start frontend
        frontend_process = start_frontend()
        
        print("\n✅ Both servers started!")
        print("📡 Backend: http://localhost:8000")
        print("🌐 Frontend: http://localhost:3000")
        print("📖 API Docs: http://localhost:8000/docs")
        print("\nPress Ctrl+C to stop both servers...")
        
        # Wait for user to stop
        try:
            backend_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping servers...")
            backend_process.terminate()
            frontend_process.terminate()
            
    except Exception as e:
        print(f"❌ Error starting servers: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())