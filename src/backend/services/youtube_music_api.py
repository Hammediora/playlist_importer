"""
YouTube Music API Client using ytmusicapi
No quota limits - uses YouTube Music web interface directly
"""

import os
import json
from typing import List, Dict, Optional, Tuple
from ytmusicapi import YTMusic

class YouTubeMusicAPIClient:
    """YouTube Music client using ytmusicapi (no quota limits)"""
    
    def __init__(self, auth_headers_file: str = None):
        # Import settings here to avoid circular imports
        import sys
        import os
        from pathlib import Path
        
        # Add the backend directory to Python path
        backend_dir = Path(__file__).parent.parent
        if str(backend_dir) not in sys.path:
            sys.path.append(str(backend_dir))
        
        from config.settings import YOUTUBE_CREDENTIALS_FILE
        
        self.auth_headers_file = auth_headers_file or str(YOUTUBE_CREDENTIALS_FILE).replace('.json', '_headers.json')
        self.ytmusic = None
        self.authenticated = False
        
    def authenticate(self) -> bool:
        """Authenticate with YouTube Music using headers"""
        try:
            if os.path.exists(self.auth_headers_file):
                with open(self.auth_headers_file, 'r') as f:
                    headers = json.load(f)
                
                self.ytmusic = YTMusic(headers=headers)
                self.authenticated = True
                print("✅ YouTube Music authenticated with headers")
                return True
            else:
                print(f"❌ Headers file not found: {self.auth_headers_file}")
                print("Please run the setup script to generate headers")
                return False
                
        except Exception as e:
            print(f"YouTube Music authentication failed: {e}")
            self.authenticated = False
            return False
    
    def search_song(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search for songs on YouTube Music"""
        try:
            if not self.authenticated:
                raise Exception("Not authenticated")
            
            results = self.ytmusic.search(query, filter="songs", limit=max_results)
            
            formatted_results = []
            for item in results:
                if 'videoId' in item:
                    formatted_results.append({
                        'videoId': item['videoId'],
                        'title': item.get('title', 'Unknown'),
                        'artist': item.get('artists', [{}])[0].get('name', 'Unknown') if item.get('artists') else 'Unknown'
                    })
            
            return formatted_results
            
        except Exception as e:
            print(f"Search failed for '{query}': {e}")
            return []
    
    def create_playlist(self, title: str, description: str = "", privacy_status: str = "PRIVATE") -> Optional[str]:
        """Create a new playlist"""
        try:
            if not self.authenticated:
                raise Exception("Not authenticated")
            
            playlist_id = self.ytmusic.create_playlist(title, description, privacy_status)
            print(f"Created playlist: {title} (ID: {playlist_id})")
            return playlist_id
            
        except Exception as e:
            print(f"Failed to create playlist '{title}': {e}")
            return None
    
    def add_songs_to_playlist(self, playlist_id: str, video_ids: List[str]) -> Tuple[List[str], List[str]]:
        """Add songs to a playlist"""
        added_songs = []
        failed_songs = []
        
        try:
            if not self.authenticated:
                raise Exception("Not authenticated")
            
            for video_id in video_ids:
                try:
                    self.ytmusic.add_playlist_items(playlist_id, [video_id])
                    added_songs.append(video_id)
                    print(f"Added video {video_id} to playlist")
                    
                except Exception as e:
                    print(f"Failed to add video {video_id}: {e}")
                    failed_songs.append(video_id)
            
            return added_songs, failed_songs
            
        except Exception as e:
            print(f"Failed to add songs to playlist: {e}")
            return [], video_ids
    
    def get_playlist_url(self, playlist_id: str) -> str:
        """Get the URL for a playlist"""
        return f"https://music.youtube.com/playlist?list={playlist_id}"
    
    def is_authenticated(self) -> bool:
        """Check if client is authenticated"""
        return self.authenticated and self.ytmusic is not None
    
    def get_auth_status(self) -> Dict:
        """Get authentication status"""
        return {
            "authenticated": self.authenticated,
            "service_available": self.ytmusic is not None,
            "headers_file_exists": os.path.exists(self.auth_headers_file)
        } 