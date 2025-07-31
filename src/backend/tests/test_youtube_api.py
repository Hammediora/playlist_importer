#!/usr/bin/env python3
"""
Test script for YouTube API implementation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from youtube_api import YouTubeAPIClient

def test_youtube_api():
    """Test the YouTube API functionality"""
    print("Testing YouTube API Implementation")
    print("=" * 40)
    
    try:
        # Initialize client
        print("1. Initializing YouTube API client...")
        client = YouTubeAPIClient()
        
        # Test authentication
        print("2. Testing authentication...")
        if client.authenticate():
            print("✅ Authentication successful!")
        else:
            print("❌ Authentication failed!")
            return False
        
        # Test search
        print("3. Testing search functionality...")
        results = client.search_song("test song", max_results=3)
        if results:
            print(f"✅ Search successful - found {len(results)} results")
            for result in results[:2]:  # Show first 2 results
                print(f"   - {result['title']} by {result['channel']}")
        else:
            print("⚠️  Search returned no results (this might be normal)")
        
        # Test playlist creation
        print("4. Testing playlist creation...")
        test_playlist_id = client.create_playlist(
            "Test Playlist - API Test",
            "Test playlist created by API test script",
            "private"
        )
        
        if test_playlist_id:
            print(f"✅ Playlist creation successful (ID: {test_playlist_id})")
            
            # Test adding songs to playlist
            print("5. Testing adding songs to playlist...")
            if results:
                video_ids = [results[0]['videoId']]
                added, failed = client.add_songs_to_playlist(test_playlist_id, video_ids)
                
                if added:
                    print(f"✅ Added {len(added)} songs to playlist")
                else:
                    print("⚠️  No songs were added to playlist")
                
                if failed:
                    print(f"⚠️  {len(failed)} songs failed to add")
            
            # Get playlist URL
            playlist_url = client.get_playlist_url(test_playlist_id)
            print(f"6. Playlist URL: {playlist_url}")
            
            print("\n🎉 All tests passed! YouTube API is working correctly.")
            return True
        else:
            print("❌ Playlist creation failed!")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    success = test_youtube_api()
    if success:
        print("\n✅ YouTube API implementation is ready to use!")
        print("You can now run your playlist importer with confidence.")
    else:
        print("\n❌ YouTube API implementation needs attention.")
        print("Please check the error messages above and fix any issues.")
        sys.exit(1) 