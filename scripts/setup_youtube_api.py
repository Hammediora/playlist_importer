#!/usr/bin/env python3
"""
Setup script for YouTube Data API v3 authentication
"""

import os
import sys
from youtube_api import YouTubeAPIClient

def setup_youtube_api():
    """Setup YouTube Data API v3 authentication"""
    print("YouTube Data API v3 Setup")
    print("=" * 50)
    
    # Check if credentials file exists
    credentials_file = "youtube_credentials.json"
    
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
        print("6. Place it in the backend directory")
        print("\nAfter downloading the credentials file, run this script again.")
        return False
    
    print(f"✅ Found credentials file: {credentials_file}")
    
    # Initialize YouTube API client
    try:
        client = YouTubeAPIClient()
        print("\n🔐 Starting authentication...")
        
        # Authenticate
        if client.authenticate():
            print("✅ YouTube API authentication successful!")
            print("✅ Your playlist importer is now ready to use!")
            return True
        else:
            print("❌ Authentication failed!")
            return False
            
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return False

def test_youtube_api():
    """Test the YouTube API functionality"""
    print("\n🧪 Testing YouTube API functionality...")
    
    try:
        client = YouTubeAPIClient()
        
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
            "private"
        )
        
        if test_playlist_id:
            print(f"✅ Playlist creation test successful (ID: {test_playlist_id})")
            
            # Clean up test playlist
            try:
                # Note: We don't have a delete method in our client yet
                # The test playlist will remain but that's okay for testing
                print("ℹ️  Test playlist created successfully (not deleted)")
            except:
                print("ℹ️  Test playlist created successfully")
            
            return True
        else:
            print("❌ Playlist creation test failed")
            return False
            
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

if __name__ == "__main__":
    print("YouTube Data API v3 Setup and Test")
    print("=" * 50)
    
    # Setup
    setup_success = setup_youtube_api()
    
    if setup_success:
        # Test
        test_success = test_youtube_api()
        
        if test_success:
            print("\n🎉 All tests passed! Your YouTube API setup is complete!")
            print("\nYou can now use the playlist importer with official YouTube API authentication.")
        else:
            print("\n⚠️  Setup completed but tests failed. Check the error messages above.")
    else:
        print("\n❌ Setup failed. Please follow the instructions above.")
        sys.exit(1) 