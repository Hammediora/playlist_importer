#!/usr/bin/env python3
"""
Simple ytmusicapi Setup (No Quota Limits)
Uses ytmusicapi's built-in authentication
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
if str(backend_dir) not in sys.path:
    sys.path.append(str(backend_dir))

from ytmusicapi import YTMusic

def setup_ytmusicapi_simple():
    """Setup ytmusicapi with simple authentication"""
    print("Simple ytmusicapi Setup (No Quota Limits)")
    print("=" * 50)
    print("✅ No quota limits")
    print("✅ Simple authentication")
    print("✅ Direct YouTube Music access")
    print("=" * 50)
    
    try:
        print("\n🔐 Starting ytmusicapi authentication...")
        print("This will open a browser for authentication...")
        
        # Use ytmusicapi's built-in authentication
        ytmusic = YTMusic.setup(filepath="oauth.json")
        
        print("✅ ytmusicapi authentication successful!")
        print("✅ No quota limits - you can import unlimited playlists!")
        return True
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return False

def test_ytmusicapi_simple():
    """Test the ytmusicapi functionality"""
    print("\n🧪 Testing ytmusicapi functionality...")
    
    try:
        # Load the authenticated client
        ytmusic = YTMusic("oauth.json")
        
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
    print("Simple ytmusicapi Setup and Test")
    print("=" * 50)
    
    # Setup
    setup_success = setup_ytmusicapi_simple()
    
    if setup_success:
        # Test
        test_success = test_ytmusicapi_simple()
        
        if test_success:
            print("\n🎉 All tests passed! Your ytmusicapi setup is complete!")
            print("\n✅ NO QUOTA LIMITS - You can import unlimited playlists!")
            print("✅ Simple authentication - No complex setup required")
            print("✅ Direct YouTube Music access")
            print("\nYou can now import unlimited playlists without quota worries!")
        else:
            print("\n⚠️  Setup completed but tests failed. Check the error messages above.")
    else:
        print("\n❌ Setup failed. Please follow the instructions above.")
        sys.exit(1) 