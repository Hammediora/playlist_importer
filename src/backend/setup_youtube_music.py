#!/usr/bin/env python3
"""
Setup script for YouTube Music authentication using ytmusicapi
No quota limits - uses YouTube Music web interface directly
"""

import os
import sys
import json
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
if str(backend_dir) not in sys.path:
    sys.path.append(str(backend_dir))

from services.youtube_music_api import YouTubeMusicAPIClient
from config.settings import YOUTUBE_CREDENTIALS_FILE

def setup_youtube_music():
    """Setup YouTube Music authentication using ytmusicapi"""
    print("YouTube Music Setup (No Quota Limits)")
    print("=" * 50)
    
    try:
        # Check if headers file exists
        headers_file = str(YOUTUBE_CREDENTIALS_FILE).replace('.json', '_headers.json')
        
        if not os.path.exists(headers_file):
            print(f"\n❌ Headers file '{headers_file}' not found!")
            print("\nTo get your headers file:")
            print("1. Go to YouTube Music in your browser")
            print("2. Open Developer Tools (F12)")
            print("3. Go to Network tab")
            print("4. Make any request (like search for a song)")
            print("5. Find a request to 'music.youtube.com'")
            print("6. Copy the 'Authorization' header value")
            print("7. Create a JSON file with your headers")
            print("\nExample headers.json:")
            print('''{
  "Authorization": "SAPISIDHASH your_auth_token_here",
  "Cookie": "your_cookies_here",
  "X-Goog-AuthUser": "0"
}''')
            print(f"\nSave this as '{headers_file}' and run this script again.")
            return False
        
        print(f"✅ Found headers file: {headers_file}")
        
        # Test the headers
        client = YouTubeMusicAPIClient()
        if client.authenticate():
            print("✅ YouTube Music authentication successful!")
            print("✅ No quota limits - you can import unlimited playlists!")
            return True
        else:
            print("❌ Authentication failed!")
            return False
            
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return False

def test_youtube_music():
    """Test the YouTube Music functionality"""
    print("\n🧪 Testing YouTube Music functionality...")
    
    try:
        client = YouTubeMusicAPIClient()
        
        if not client.authenticate():
            print("❌ Authentication failed during testing")
            return False
        
        # Test search
        print("Testing search functionality...")
        results = client.search_song("test song", max_results=3)
        if results:
            print(f"✅ Search test successful - found {len(results)} results")
        else:
            print("⚠️  Search test returned no results (this might be normal)")
        
        # Test playlist creation
        print("Testing playlist creation...")
        test_playlist_id = client.create_playlist(
            "Test Playlist - Will Delete",
            "Test playlist created by setup script",
            "PRIVATE"
        )
        
        if test_playlist_id:
            print(f"✅ Playlist creation test successful (ID: {test_playlist_id})")
            return True
        else:
            print("❌ Playlist creation test failed")
            return False
            
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

if __name__ == "__main__":
    print("YouTube Music Setup and Test (No Quota Limits)")
    print("=" * 50)
    
    # Setup
    setup_success = setup_youtube_music()
    
    if setup_success:
        # Test
        test_success = test_youtube_music()
        
        if test_success:
            print("\n🎉 All tests passed! Your YouTube Music setup is complete!")
            print("\n✅ NO QUOTA LIMITS - You can import unlimited playlists!")
        else:
            print("\n⚠️  Setup completed but tests failed. Check the error messages above.")
    else:
        print("\n❌ Setup failed. Please follow the instructions above.")
        sys.exit(1) 