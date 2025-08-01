"""
Application configuration settings
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent

# Credentials directory
CREDENTIALS_DIR = PROJECT_ROOT / "credentials"

# Spotify configuration
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:3000/callback")

# YouTube Music configuration (using ytmusicapi - no quota limits)
YOUTUBE_MUSIC_OAUTH_FILE = "ytmusic_oauth.json"

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///playlist_importer.db")

# API configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# CORS configuration
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]