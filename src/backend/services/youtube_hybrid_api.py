"""
Hybrid YouTube API Client
Uses OAuth for authentication, then ytmusicapi for operations (no quota limits)
"""

import os
import json
import pickle
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from ytmusicapi import YTMusic

# YouTube Data API v3 scopes
SCOPES = [
    'https://www.googleapis.com/auth/youtube.force-ssl',
    'https://www.googleapis.com/auth/youtube'
]

class YouTubeHybridAPIClient:
    """Hybrid YouTube client: OAuth auth + ytmusicapi operations"""
    
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
        self.ytmusic = None
        self.authenticated = False
        self.oauth_creds = None
        
    def authenticate(self) -> bool:
        """Authenticate with OAuth and setup ytmusicapi"""
        try:
            # Step 1: OAuth authentication
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
            
            self.oauth_creds = creds
            
            # Step 2: Build YouTube service for testing
            self.service = build('youtube', 'v3', credentials=creds)
            
            # Step 3: Extract headers for ytmusicapi
            headers = self._extract_headers_from_oauth(creds)
            
            # Step 4: Setup ytmusicapi with extracted headers
            # ytmusicapi doesn't accept headers in constructor, we'll use it differently
            self.ytmusic = YTMusic()
            # Store headers for later use
            self.ytmusic_headers = headers
            
            # Step 5: Test authentication
            self._test_authentication()
            
            self.authenticated = True
            return True
            
        except Exception as e:
            print(f"YouTube Hybrid API authentication failed: {e}")
            self.authenticated = False
            return False
    
    def _extract_headers_from_oauth(self, creds: Credentials) -> Dict[str, str]:
        """Extract headers from OAuth credentials for ytmusicapi"""
        try:
            # Get the access token
            access_token = creds.token
            
            # Create headers that ytmusicapi expects
            headers = {
                "Authorization": f"Bearer {access_token}",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin"
            }
            
            # Test the headers by making a request to YouTube Music
            test_url = "https://music.youtube.com/youtubei/v1/guide"
            response = requests.get(test_url, headers=headers)
            
            if response.status_code == 200:
                print("✅ Successfully extracted headers from OAuth")
                return headers
            else:
                # Fallback: try to get cookies from a YouTube session
                print("⚠️  OAuth headers test failed, trying alternative method...")
                return self._get_headers_from_youtube_session(creds)
                
        except Exception as e:
            print(f"Failed to extract headers from OAuth: {e}")
            return self._get_headers_from_youtube_session(creds)
    
    def _get_headers_from_youtube_session(self, creds: Credentials) -> Dict[str, str]:
        """Alternative method to get headers from YouTube session"""
        try:
            # Create a session and get cookies from YouTube
            session = requests.Session()
            
            # First, authenticate with OAuth
            session.headers.update({
                "Authorization": f"Bearer {creds.token}",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })
            
            # Get cookies from YouTube
            youtube_response = session.get("https://www.youtube.com/")
            
            # Now try to get YouTube Music cookies
            music_response = session.get("https://music.youtube.com/")
            
            # Extract cookies
            cookies = session.cookies.get_dict()
            cookie_string = "; ".join([f"{k}={v}" for k, v in cookies.items()])
            
            headers = {
                "Authorization": f"Bearer {creds.token}",
                "Cookie": cookie_string,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive"
            }
            
            print("✅ Successfully created headers from YouTube session")
            return headers
            
        except Exception as e:
            print(f"Failed to get headers from YouTube session: {e}")
            # Return basic headers as fallback
            return {
                "Authorization": f"Bearer {creds.token}",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
    
    def _test_authentication(self):
        """Test authentication by getting user's channel info"""
        try:
            # Test with YouTube Data API
            request = self.service.channels().list(
                part="snippet",
                mine=True
            )
            response = request.execute()
            
            if not response.get('items'):
                raise Exception("No channel found - authentication may have failed")
                
            print(f"Successfully authenticated as: {response['items'][0]['snippet']['title']}")
            
            # Test with ytmusicapi
            if self.ytmusic:
                try:
                    # Try a simple search to test ytmusicapi
                    test_results = self.ytmusic.search("test", filter="songs", limit=1)
                    print("✅ ytmusicapi authentication successful")
                except Exception as e:
                    print(f"⚠️  ytmusicapi test failed: {e}")
                    print("Will use YouTube Data API for operations")
                    self.ytmusic = None
            
        except Exception as e:
            raise Exception(f"Authentication test failed: {e}")
    
    def search_song(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search for songs using ytmusicapi (no quota) or fallback to YouTube API"""
        try:
            if not self.authenticated:
                raise Exception("Not authenticated")
            
            # Try ytmusicapi first (no quota)
            if self.ytmusic:
                try:
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
                    print(f"ytmusicapi search failed, falling back to YouTube API: {e}")
            
            # Fallback to YouTube Data API
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
    
    def create_playlist(self, title: str, description: str = "", privacy_status: str = "private") -> Optional[str]:
        """Create a new playlist using ytmusicapi (no quota) or fallback"""
        try:
            if not self.authenticated:
                raise Exception("Not authenticated")
            
            # Try ytmusicapi first (no quota)
            if self.ytmusic:
                try:
                    playlist_id = self.ytmusic.create_playlist(title, description, privacy_status.upper())
                    print(f"Created playlist: {title} (ID: {playlist_id})")
                    return playlist_id
                except Exception as e:
                    print(f"ytmusicapi playlist creation failed, falling back to YouTube API: {e}")
            
            # Fallback to YouTube Data API
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
        """Add songs to a playlist using ytmusicapi (no quota) or fallback"""
        added_songs = []
        failed_songs = []
        
        try:
            if not self.authenticated:
                raise Exception("Not authenticated")
            
            # Try ytmusicapi first (no quota)
            if self.ytmusic:
                try:
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
                    print(f"ytmusicapi add songs failed, falling back to YouTube API: {e}")
            
            # Fallback to YouTube Data API
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
        return self.authenticated and (self.service is not None or self.ytmusic is not None)
    
    def get_auth_status(self) -> Dict:
        """Get authentication status"""
        return {
            "authenticated": self.authenticated,
            "oauth_service_available": self.service is not None,
            "ytmusicapi_available": self.ytmusic is not None,
            "credentials_file_exists": os.path.exists(self.credentials_file),
            "token_file_exists": os.path.exists(self.token_file)
        } 