#!/usr/bin/env python3
"""
Main entry point for the Playlist Importer Backend API
"""

import uvicorn
import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.main import app
from config.settings import API_HOST, API_PORT, DEBUG

if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host=API_HOST,
        port=API_PORT,
        reload=DEBUG,
        log_level="debug" if DEBUG else "info"
    )