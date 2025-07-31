"""
YouTube Data API v3 Client for Playlist Management
Uses official Google API client with OAuth 2.0 authentication
"""

import os
import json
import pickle
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# YouTube Data API v3 scopes
SCOPES = [
    'https://www.googleapis.com/auth/youtube.force-ssl',
    'https://www.googleapis.com/auth/youtube'
]

class YouTubeAPIClient:
    """Official YouTube Data API v3 client for playlist operations"""
    
    def __init__(self, credentials_file: str = None, token_file: str = None):
        # Import settings here to avoid circular imports
        import sys
        import os
        from pathlib import Path
        
        # Add the backend directory to Python path
        backend_dir = Path(__file__).parent.parent
        if str(backend_dir) not in sys.path:
            sys.path.append(str(backend_dir))
        
        from config.settings import YOUTUBE_CREDENTIALS_FILE, YOUTUBE_TOKEN_FILE
        
        self.credentials_file = credentials_file or str(YOUTUBE_CREDENTIALS_FILE)
        self.token_file = token_file or str(YOUTUBE_TOKEN_FILE)
        self.service = None
        self.authenticated = False
        
    def authenticate(self) -> bool:
        """Authenticate with YouTube Data API using OAuth 2.0"""
        try:
            creds = None
            
            # Load existing token if available
            if os.path.exists(self.token_file):
                with open(self.token_file, 'rb') as token:
                    creds = pickle.load(token)
            
            # If no valid credentials available, let user log in
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    if not os.path.exists(self.credentials_file):
                        raise FileNotFoundError(
                            f"Credentials file '{self.credentials_file}' not found. "
                            "Please download it from Google Cloud Console."
                        )
                    
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_file, SCOPES)
                    creds = flow.run_local_server(port=0)
                
                # Save the credentials for the next run
                with open(self.token_file, 'wb') as token:
                    pickle.dump(creds, token)
            
            # Build the YouTube service
            self.service = build('youtube', 'v3', credentials=creds)
            self.authenticated = True
            
            # Test authentication
            self._test_authentication()
            
            return True
            
        except Exception as e:
            print(f"YouTube API authentication failed: {e}")
            self.authenticated = False
            return False
    
    def _test_authentication(self):
        """Test authentication by getting user's channel info"""
        try:
            request = self.service.channels().list(
                part="snippet",
                mine=True
            )
            response = request.execute()
            
            if not response.get('items'):
                raise Exception("No channel found - authentication may have failed")
                
            print(f"Successfully authenticated as: {response['items'][0]['snippet']['title']}")
            
        except Exception as e:
            raise Exception(f"Authentication test failed: {e}")
    
    def search_song(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search for songs on YouTube Music"""
        try:
            if not self.authenticated:
                raise Exception("Not authenticated")
            
            # Search for music videos
            request = self.service.search().list(
                part="snippet",
                q=query,
                type="video",
                videoCategoryId="10",  # Music category
                maxResults=max_results,
                fields="items(id/videoId,snippet/title,snippet/channelTitle)"
            )
            
            response = request.execute()
            
            results = []
            for item in response.get('items', []):
                results.append({
                    'videoId': item['id']['videoId'],
                    'title': item['snippet']['title'],
                    'channel': item['snippet']['channelTitle']
                })
            
            return results
            
        except Exception as e:
            print(f"Search failed for '{query}': {e}")
            return []
    
    def search_song_batch(self, queries: List[str], max_results: int = 5) -> Dict[str, List[Dict]]:
        """Search for multiple songs in one batch to reduce quota usage"""
        results = {}
        
        try:
            if not self.authenticated:
                raise Exception("Not authenticated")
            
            for query in queries:
                try:
                    # Search for music videos
                    request = self.service.search().list(
                        part="snippet",
                        q=query,
                        type="video",
                        videoCategoryId="10",  # Music category
                        maxResults=max_results,
                        fields="items(id/videoId,snippet/title,snippet/channelTitle)"
                    )
                    
                    response = request.execute()
                    
                    song_results = []
                    for item in response.get('items', []):
                        song_results.append({
                            'videoId': item['id']['videoId'],
                            'title': item['snippet']['title'],
                            'channel': item['snippet']['channelTitle']
                        })
                    
                    results[query] = song_results
                    
                except Exception as e:
                    print(f"Search failed for '{query}': {e}")
                    results[query] = []
            
            return results
            
        except Exception as e:
            print(f"Batch search failed: {e}")
            return {query: [] for query in queries}
    
    def create_playlist(self, title: str, description: str = "", privacy_status: str = "private") -> Optional[str]:
        """Create a new playlist"""
        try:
            if not self.authenticated:
                raise Exception("Not authenticated")
            
            # Create playlist
            request = self.service.playlists().insert(
                part="snippet,status",
                body={
                    "snippet": {
                        "title": title,
                        "description": description
                    },
                    "status": {
                        "privacyStatus": privacy_status
                    }
                }
            )
            
            response = request.execute()
            playlist_id = response['id']
            
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
                    request = self.service.playlistItems().insert(
                        part="snippet",
                        body={
                            "snippet": {
                                "playlistId": playlist_id,
                                "resourceId": {
                                    "kind": "youtube#video",
                                    "videoId": video_id
                                }
                            }
                        }
                    )
                    
                    response = request.execute()
                    added_songs.append(video_id)
                    print(f"Added video {video_id} to playlist")
                    
                except HttpError as e:
                    if e.resp.status == 409:  # Already in playlist
                        print(f"Video {video_id} already in playlist")
                        added_songs.append(video_id)
                    else:
                        print(f"Failed to add video {video_id}: {e}")
                        failed_songs.append(video_id)
                        
                except Exception as e:
                    print(f"Failed to add video {video_id}: {e}")
                    failed_songs.append(video_id)
            
            return added_songs, failed_songs
            
        except Exception as e:
            print(f"Failed to add songs to playlist: {e}")
            return [], video_ids
    
    def get_playlist_url(self, playlist_id: str) -> str:
        """Get the URL for a playlist"""
        return f"https://www.youtube.com/playlist?list={playlist_id}"
    
    def is_authenticated(self) -> bool:
        """Check if client is authenticated"""
        return self.authenticated and self.service is not None
    
    def get_auth_status(self) -> Dict:
        """Get authentication status"""
        return {
            "authenticated": self.authenticated,
            "service_available": self.service is not None,
            "credentials_file_exists": os.path.exists(self.credentials_file),
            "token_file_exists": os.path.exists(self.token_file)
        } 