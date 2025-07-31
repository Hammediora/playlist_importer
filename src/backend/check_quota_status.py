#!/usr/bin/env python3
"""
Check YouTube Data API v3 Quota Status
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
if str(backend_dir) not in sys.path:
    sys.path.append(str(backend_dir))

from services.youtube_oauth_api import YouTubeOAuthAPIClient

def check_quota_status():
    """Check current quota status"""
    print("YouTube Data API v3 Quota Status Check")
    print("=" * 50)
    
    try:
        # Initialize client
        client = YouTubeOAuthAPIClient()
        
        # Try to authenticate (this will fail if quota exceeded)
        print("Testing authentication...")
        
        try:
            if client.authenticate():
                print("✅ Authentication successful!")
                quota_info = client.get_quota_info()
                print(f"📊 Quota used: {quota_info['quota_used']} units")
                print(f"📊 Quota remaining: {quota_info['quota_remaining']} units")
                print(f"📊 Quota percentage: {quota_info['quota_percentage']:.1f}%")
                
                if quota_info['quota_remaining'] > 1000:
                    print("✅ Plenty of quota remaining!")
                else:
                    print("⚠️  Low quota remaining")
                    
            else:
                print("❌ Authentication failed")
                
        except Exception as e:
            if "quotaExceeded" in str(e):
                print("❌ QUOTA EXCEEDED")
                print("\nSolutions:")
                print("1. Wait until tomorrow (quota resets daily at midnight PT)")
                print("2. Add billing account to Google Cloud Console")
                print("3. Request quota increase in Google Cloud Console")
                print("\nTo add billing:")
                print("- Go to: https://console.cloud.google.com/billing")
                print("- Select project: youtubemusic-467617")
                print("- Link or create a billing account")
                print("- This will increase your quota to 100,000+ units")
                
            else:
                print(f"❌ Other error: {e}")
                
    except Exception as e:
        print(f"❌ Error checking quota: {e}")

if __name__ == "__main__":
    check_quota_status() 