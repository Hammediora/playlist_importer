#!/usr/bin/env python3
"""
Check YouTube Data API v3 quota usage
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
if str(backend_dir) not in sys.path:
    sys.path.append(str(backend_dir))

from services.youtube_api import YouTubeAPIClient

def check_quota():
    """Check current quota usage"""
    print("YouTube Data API v3 Quota Check")
    print("=" * 40)
    
    try:
        client = YouTubeAPIClient()
        
        if not client.authenticate():
            print("❌ Authentication failed")
            return
        
        # Get quota usage by making a simple request
        print("Checking quota usage...")
        
        # Try a simple search to see if we get quota error
        try:
            results = client.search_song("test", max_results=1)
            if results:
                print("✅ Quota available - search successful")
                print(f"Found {len(results)} results")
            else:
                print("⚠️  Search returned no results (quota might be low)")
        except Exception as e:
            if "quotaExceeded" in str(e):
                print("❌ Quota exceeded!")
                print("You've used up your daily API quota.")
                print("\nSolutions:")
                print("1. Wait until tomorrow (quota resets daily)")
                print("2. Upgrade to a paid Google Cloud account")
                print("3. Request quota increase from Google")
            else:
                print(f"❌ Other error: {e}")
        
    except Exception as e:
        print(f"❌ Error checking quota: {e}")

if __name__ == "__main__":
    check_quota() 