"""
Optimized YouTube Data API v3 Client
Reduces quota usage through batching and intelligent delays
"""

import os
import json
import pickle
import time
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

class OptimizedYouTubeAPIClient:
    """Optimized YouTube Data API v3 client with reduced quota usage"""
    
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
        self.search_cache = {}  # Cache search results to avoid duplicate searches
        self.last_request_time = 0
        self.min_delay = 0.1  # Minimum delay between requests (100ms)
        
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
    
    def _rate_limit(self):
        """Implement rate limiting to avoid quota issues"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_delay:
            sleep_time = self.min_delay - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def search_song(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search for songs on YouTube Music with caching"""
        # Check cache first
        cache_key = f"{query}_{max_results}"
        if cache_key in self.search_cache:
            print(f"Using cached result for: {query}")
            return self.search_cache[cache_key]
        
        try:
            if not self.authenticated:
                raise Exception("Not authenticated")
            
            self._rate_limit()
            
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
            
            # Cache the result
            self.search_cache[cache_key] = results
            return results
            
        except Exception as e:
            print(f"Search failed for '{query}': {e}")
            return []
    
    def search_songs_batch(self, queries: List[str], max_results: int = 5) -> Dict[str, List[Dict]]:
        """Search for multiple songs with intelligent batching"""
        results = {}
        
        for i, query in enumerate(queries):
            print(f"Searching {i+1}/{len(queries)}: {query}")
            results[query] = self.search_song(query, max_results)
            
            # Add delay between searches to be gentle on quota
            if i < len(queries) - 1:  # Don't delay after last search
                time.sleep(0.2)  # 200ms delay between searches
        
        return results
    
    def create_playlist(self, title: str, description: str = "", privacy_status: str = "private") -> Optional[str]:
        """Create a new playlist"""
        try:
            if not self.authenticated:
                raise Exception("Not authenticated")
            
            self._rate_limit()
            
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
    
    def add_songs_to_playlist_batch(self, playlist_id: str, video_ids: List[str], batch_size: int = 10) -> Tuple[List[str], List[str]]:
        """Add songs to a playlist in batches to reduce quota usage"""
        added_songs = []
        failed_songs = []
        
        try:
            if not self.authenticated:
                raise Exception("Not authenticated")
            
            # Process in batches
            for i in range(0, len(video_ids), batch_size):
                batch = video_ids[i:i + batch_size]
                print(f"Adding batch {i//batch_size + 1}/{(len(video_ids) + batch_size - 1)//batch_size}")
                
                for video_id in batch:
                    try:
                        self._rate_limit()
                        
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
                
                # Delay between batches
                if i + batch_size < len(video_ids):
                    time.sleep(0.5)  # 500ms delay between batches
            
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
            "token_file_exists": os.path.exists(self.token_file),
            "cache_size": len(self.search_cache)
        } 