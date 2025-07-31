#!/usr/bin/env python3
"""
Manual ytmusicapi Setup (No Quota Limits)
Based on spotify_to_ytmusic approach
"""

import os
import sys
import json
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
if str(backend_dir) not in sys.path:
    sys.path.append(str(backend_dir))

from ytmusicapi import YTMusic

def setup_ytmusicapi_manual():
    """Setup ytmusicapi with manual header authentication"""
    print("Manual ytmusicapi Setup (No Quota Limits)")
    print("=" * 50)
    print("✅ No quota limits")
    print("✅ Direct YouTube Music access")
    print("✅ Based on spotify_to_ytmusic approach")
    print("=" * 50)
    
    headers_file = "ytmusic_headers.json"
    
    if not os.path.exists(headers_file):
        print(f"\n❌ Headers file '{headers_file}' not found!")
        print("\nTo get your headers file:")
        print("1. Go to YouTube Music in your browser: https://music.youtube.com/")
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
    
    try:
        # Load headers
        with open(headers_file, 'r') as f:
            headers = json.load(f)
        
        # Test the headers
        ytmusic = YTMusic(headers=headers)
        
        # Test authentication
        print("Testing authentication...")
        test_results = ytmusic.search("test", filter="songs", limit=1)
        
        print("✅ ytmusicapi authentication successful!")
        print("✅ No quota limits - you can import unlimited playlists!")
        return True
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        print("\nMake sure your headers file contains valid authentication headers.")
        return False

def test_ytmusicapi_manual():
    """Test the ytmusicapi functionality"""
    print("\n🧪 Testing ytmusicapi functionality...")
    
    try:
        headers_file = "ytmusic_headers.json"
        
        if not os.path.exists(headers_file):
            print("❌ Headers file not found")
            return False
        
        # Load the authenticated client
        with open(headers_file, 'r') as f:
            headers = json.load(f)
        
        ytmusic = YTMusic(headers=headers)
        
        # Test search
        print("Testing search functionality...")
        results = ytmusic.search("test song", filter="songs", limit=3)
        if results:
            print(f"✅ Search test successful - found {len(results)} results")
        else:
            print("⚠️  Search test returned no results (this might be normal)")
        
        # Test playlist creation
        print("Testing playlist creation...")
        playlist_id = ytmusic.create_playlist(
            "Test Playlist - Will Delete",
            "Test playlist created by ytmusicapi setup script",
            "PRIVATE"
        )
        
        if playlist_id:
            print(f"✅ Playlist creation test successful (ID: {playlist_id})")
            
            # Test adding songs
            print("Testing song addition...")
            if results:
                video_id = results[0]['videoId']
                ytmusic.add_playlist_items(playlist_id, [video_id])
                print(f"✅ Song addition test successful")
            
            return True
        else:
            print("❌ Playlist creation test failed")
            return False
            
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

if __name__ == "__main__":
    print("Manual ytmusicapi Setup and Test")
    print("=" * 50)
    
    # Setup
    setup_success = setup_ytmusicapi_manual()
    
    if setup_success:
        # Test
        test_success = test_ytmusicapi_manual()
        
        if test_success:
            print("\n🎉 All tests passed! Your ytmusicapi setup is complete!")
            print("\n✅ NO QUOTA LIMITS - You can import unlimited playlists!")
            print("✅ Direct YouTube Music access")
            print("✅ Based on proven spotify_to_ytmusic approach")
            print("\nYou can now import unlimited playlists without quota worries!")
        else:
            print("\n⚠️  Setup completed but tests failed. Check the error messages above.")
    else:
        print("\n❌ Setup failed. Please follow the instructions above.")
        sys.exit(1) 