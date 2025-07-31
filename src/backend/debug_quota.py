#!/usr/bin/env python3
"""
Debug YouTube Data API v3 quota issues
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
if str(backend_dir) not in sys.path:
    sys.path.append(str(backend_dir))

from services.youtube_api import YouTubeAPIClient

def debug_quota():
    """Debug quota issues"""
    print("YouTube Data API v3 Quota Debug")
    print("=" * 40)
    
    try:
        client = YouTubeAPIClient()
        
        if not client.authenticate():
            print("❌ Authentication failed")
            return
        
        print("✅ Authentication successful")
        print("\nPossible issues:")
        print("1. **Low quota allocation** - Your project might have a very low quota")
        print("2. **Different quota limits** - Some operations cost more quota units")
        print("3. **Project configuration** - API might not be properly enabled")
        
        print("\nNext steps:")
        print("1. Go to Google Cloud Console: https://console.cloud.google.com/")
        print("2. Select your project: youtubemusic-467617")
        print("3. Go to 'APIs & Services' > 'Quotas'")
        print("4. Look for 'YouTube Data API v3' quotas")
        print("5. Check if you have a very low daily quota (like 100-1000 units)")
        
        print("\nCommon quota costs:")
        print("- Search requests: 100 units each")
        print("- Playlist insertions: 50 units each")
        print("- Channel info: 1 unit each")
        
        print("\nWith 209 requests:")
        print("- If each search costs 100 units: 209 * 100 = 20,900 units")
        print("- This would easily exceed a 10,000 unit daily limit")
        
        print("\nSolutions:")
        print("1. **Request quota increase** in Google Cloud Console")
        print("2. **Enable billing** to get higher quotas")
        print("3. **Wait for quota reset** (daily at midnight PT)")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    debug_quota() 