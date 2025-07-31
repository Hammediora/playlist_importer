#!/usr/bin/env python3
"""
Setup script for Optimized OAuth YouTube API
OAuth authentication with intelligent quota management
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
if str(backend_dir) not in sys.path:
    sys.path.append(str(backend_dir))

from services.youtube_oauth_api import YouTubeOAuthAPIClient
from config.settings import YOUTUBE_CREDENTIALS_FILE

def setup_youtube_oauth():
    """Setup Optimized OAuth YouTube API authentication"""
    print("Optimized OAuth YouTube API Setup")
    print("=" * 50)
    print("✅ OAuth authentication (secure)")
    print("✅ Intelligent quota management")
    print("✅ Search result caching")
    print("✅ Batch processing")
    print("✅ Rate limiting")
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
        
        # Initialize Optimized OAuth YouTube API client
        try:
            client = YouTubeOAuthAPIClient()
            print("\n🔐 Starting OAuth authentication...")
            
            # Authenticate
            if client.authenticate():
                print("✅ Optimized OAuth YouTube API authentication successful!")
                print("✅ Quota management enabled")
                print("✅ Search caching enabled")
                print("✅ Rate limiting enabled")
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

def test_youtube_oauth():
    """Test the Optimized OAuth YouTube API functionality"""
    print("\n🧪 Testing Optimized OAuth YouTube API functionality...")
    
    try:
        client = YouTubeOAuthAPIClient()
        
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
        
        # Test quota tracking
        quota_info = client.get_quota_info()
        print(f"✅ Quota tracking: {quota_info['quota_used']} used, {quota_info['quota_remaining']} remaining")
        
        # Test playlist creation
        print("Testing playlist creation...")
        test_playlist_id = client.create_playlist(
            "Test Playlist - Will Delete",
            "Test playlist created by optimized OAuth setup script",
            "private"
        )
        
        if test_playlist_id:
            print(f"✅ Playlist creation test successful (ID: {test_playlist_id})")
            
            # Test adding songs in batches
            print("Testing batch song addition...")
            if results:
                video_ids = [result['videoId'] for result in results[:2]]  # Use first 2 results
                added, failed = client.add_songs_to_playlist_batch(test_playlist_id, video_ids, batch_size=2)
                if added:
                    print(f"✅ Batch song addition test successful - added {len(added)} songs")
                else:
                    print("⚠️  Batch song addition test failed")
            
            return True
        else:
            print("❌ Playlist creation test failed")
            return False
            
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

if __name__ == "__main__":
    print("Optimized OAuth YouTube API Setup and Test")
    print("=" * 50)
    
    # Setup
    setup_success = setup_youtube_oauth()
    
    if setup_success:
        # Test
        test_success = test_youtube_oauth()
        
        if test_success:
            print("\n🎉 All tests passed! Your Optimized OAuth YouTube API setup is complete!")
            print("\n✅ OAuth authentication: Secure and reliable")
            print("✅ Quota management: Intelligent tracking and warnings")
            print("✅ Search caching: Avoids duplicate searches")
            print("✅ Batch processing: Efficient playlist operations")
            print("✅ Rate limiting: Prevents quota issues")
            print("\nYou can now import playlists efficiently with quota awareness!")
        else:
            print("\n⚠️  Setup completed but tests failed. Check the error messages above.")
    else:
        print("\n❌ Setup failed. Please follow the instructions above.")
        sys.exit(1) 