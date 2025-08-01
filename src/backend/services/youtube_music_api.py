"""
YouTube Music API Client using ytmusicapi (linsomniac approach)
No quota limits - uses YouTube Music web interface directly with OAuth authentication
"""

import os
import json
from typing import List, Dict, Optional, Tuple
from ytmusicapi import YTMusic
from pathlib import Path

class YouTubeMusicAPIClient:
    """YouTube Music client using ytmusicapi (no quota limits)"""
    
    def __init__(self, oauth_file: str = None):
        """Initialize YouTube Music client with OAuth file (like linsomniac approach)"""
        self.oauth_file = oauth_file or "ytmusic_oauth.json"
        self.ytmusic = None
        self.authenticated = False
        
    def authenticate(self) -> bool:
        """Authenticate with YouTube Music using OAuth file (linsomniac approach)"""
        try:
            if not os.path.exists(self.oauth_file):
                print(f"❌ OAuth file not found: {self.oauth_file}")
                print("Please run setup_ytmusic_oauth.py to create the OAuth file")
                return False
            
            # Initialize YTMusic with OAuth file (like linsomniac does)
            self.ytmusic = YTMusic(self.oauth_file)
            self.authenticated = True
            print(f"✅ YouTube Music authenticated with OAuth file: {self.oauth_file}")
            return True
                
        except Exception as e:
            print(f"YouTube Music authentication failed: {e}")
            print("Try running setup_ytmusic_oauth.py to create a fresh OAuth file")
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
            "oauth_file_exists": os.path.exists(self.oauth_file),
            "oauth_file_path": self.oauth_file
        } 