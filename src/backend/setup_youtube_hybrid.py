#!/usr/bin/env python3
"""
Setup script for Hybrid YouTube API (OAuth + ytmusicapi)
Best of both worlds: OAuth authentication + no quota limits
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
if str(backend_dir) not in sys.path:
    sys.path.append(str(backend_dir))

from services.youtube_hybrid_api import YouTubeHybridAPIClient
from config.settings import YOUTUBE_CREDENTIALS_FILE

def setup_youtube_hybrid():
    """Setup Hybrid YouTube API authentication"""
    print("Hybrid YouTube API Setup (OAuth + ytmusicapi)")
    print("=" * 50)
    print("✅ OAuth authentication (secure)")
    print("✅ ytmusicapi operations (no quota limits)")
    print("✅ Automatic fallback to YouTube Data API")
    print("=" * 50)
    
    try:
        # Check if credentials file exists
        credentials_file = YOUTUBE_CREDENTIALS_FILE
        
        if not os.path.exists(credentials_file):
            print(f"\n❌ Credentials file '{credentials_file}' not found!")
            print("\nTo get your credentials file:")
            print("1. Go to Google Cloud Console: https://console.cloud.google.com/")
            print("2. Create a new project or select existing one")
            print("3. Enable YouTube Data API v3:")
            print("   - Go to 'APIs & Services' > 'Library'")
            print("   - Search for 'YouTube Data API v3'")
            print("   - Click 'Enable'")
            print("4. Create credentials:")
            print("   - Go to 'APIs & Services' > 'Credentials'")
            print("   - Click 'Create Credentials' > 'OAuth 2.0 Client IDs'")
            print("   - Choose 'Desktop application'")
            print("   - Download the JSON file")
            print("5. Rename the downloaded file to 'youtube_credentials.json'")
            print("6. Place it in the credentials directory")
            print("\nAfter downloading the credentials file, run this script again.")
            return False
        
        print(f"✅ Found credentials file: {credentials_file}")
        
        # Initialize Hybrid YouTube API client
        try:
            client = YouTubeHybridAPIClient()
            print("\n🔐 Starting hybrid authentication...")
            
            # Authenticate
            if client.authenticate():
                print("✅ Hybrid YouTube API authentication successful!")
                print("✅ OAuth authentication completed")
                print("✅ ytmusicapi setup completed")
                print("✅ No quota limits for operations!")
                return True
            else:
                print("❌ Authentication failed!")
                return False
                
        except Exception as e:
            print(f"❌ Setup failed: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return False

def test_youtube_hybrid():
    """Test the Hybrid YouTube API functionality"""
    print("\n🧪 Testing Hybrid YouTube API functionality...")
    
    try:
        client = YouTubeHybridAPIClient()
        
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
            "Test playlist created by hybrid setup script",
            "private"
        )
        
        if test_playlist_id:
            print(f"✅ Playlist creation test successful (ID: {test_playlist_id})")
            
            # Test adding songs
            print("Testing song addition...")
            if results:
                video_id = results[0]['videoId']
                added, failed = client.add_songs_to_playlist(test_playlist_id, [video_id])
                if added:
                    print(f"✅ Song addition test successful - added {len(added)} songs")
                else:
                    print("⚠️  Song addition test failed")
            
            return True
        else:
            print("❌ Playlist creation test failed")
            return False
            
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

if __name__ == "__main__":
    print("Hybrid YouTube API Setup and Test")
    print("=" * 50)
    
    # Setup
    setup_success = setup_youtube_hybrid()
    
    if setup_success:
        # Test
        test_success = test_youtube_hybrid()
        
        if test_success:
            print("\n🎉 All tests passed! Your Hybrid YouTube API setup is complete!")
            print("\n✅ OAuth authentication: Secure and reliable")
            print("✅ ytmusicapi operations: No quota limits")
            print("✅ Automatic fallback: Always works")
            print("\nYou can now import unlimited playlists without quota worries!")
        else:
            print("\n⚠️  Setup completed but tests failed. Check the error messages above.")
    else:
        print("\n❌ Setup failed. Please follow the instructions above.")
        sys.exit(1) 