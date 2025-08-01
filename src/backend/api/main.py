from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
import json
import os
import requests
from datetime import datetime, timedelta
import subprocess
import sys
import asyncio

# Import from our organized structure
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import *
from services.youtube_music_api import YouTubeMusicAPIClient
from ytmusicapi import YTMusic
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    # Validate Spotify credentials
    if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
        print("WARNING: Spotify credentials not found in environment variables!")
        print("Please ensure SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET are set in your .env file")
    else:
        print(f"Spotify API configured with Client ID: {SPOTIFY_CLIENT_ID[:8]}...")
    
    print("YouTube Music API ready for authentication")
    
    yield
    
    # Shutdown
    print("Shutting down Playlist Importer API...")

app = FastAPI(title="Playlist Importer API", version="1.0.0", lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class Track(BaseModel):
    name: str
    artist: str
    album: Optional[str] = None
    
    class Config:
        # Allow extra fields to be ignored
        extra = "ignore"

class ImportRequest(BaseModel):
    playlistName: str
    tracks: List[Track]
    
    class Config:
        # Allow extra fields to be ignored
        extra = "ignore"

class ImportResponse(BaseModel):
    playlistUrl: Optional[str] = None
    addedTracks: List[str] = []
    failedTracks: List[str] = []
    message: str

class SpotifyCallbackRequest(BaseModel):
    code: str

class SpotifyPlaylistsRequest(BaseModel):
    access_token: str

class SpotifyTracksRequest(BaseModel):
    access_token: str

class YouTubeMusicSetupRequest(BaseModel):
    credentials: str

# Global YouTube Music clients
ytmusic_api = None

@app.get("/")
async def root():
    return {"message": "Playlist Importer API", "status": "running"}

@app.get("/health")
async def health_check():
    """Simple health check"""
    return {
        "status": "healthy", 
        "youtube_music_ready": ytmusic_api is not None
    }

# Spotify endpoints
@app.get("/auth/spotify")
async def spotify_auth_redirect():
    """Redirect to Spotify OAuth"""
    from fastapi.responses import RedirectResponse
    scope = "playlist-read-private playlist-read-collaborative"
    auth_url = f"https://accounts.spotify.com/authorize?client_id={SPOTIFY_CLIENT_ID}&response_type=code&redirect_uri={SPOTIFY_REDIRECT_URI}&scope={scope}"
    return RedirectResponse(url=auth_url)

@app.get("/spotify/auth-url")
async def get_spotify_auth_url():
    """Get Spotify OAuth URL"""
    scope = "playlist-read-private playlist-read-collaborative"
    auth_url = f"https://accounts.spotify.com/authorize?client_id={SPOTIFY_CLIENT_ID}&response_type=code&redirect_uri={SPOTIFY_REDIRECT_URI}&scope={scope}"
    return {"auth_url": auth_url}

@app.post("/spotify/callback")
async def spotify_callback(request: SpotifyCallbackRequest):
    """Handle Spotify OAuth callback"""
    try:
        # Exchange code for access token
        token_url = "https://accounts.spotify.com/api/token"
        data = {
            "grant_type": "authorization_code",
            "code": request.code,
            "redirect_uri": SPOTIFY_REDIRECT_URI,
            "client_id": SPOTIFY_CLIENT_ID,
            "client_secret": SPOTIFY_CLIENT_SECRET
        }
        
        response = requests.post(token_url, data=data)
        
        if response.status_code == 400:
            error_data = response.json()
            error_message = error_data.get('error_description', 'Unknown error')
            raise HTTPException(status_code=400, detail=f"Spotify authorization failed: {error_message}")
        
        response.raise_for_status()
        
        token_data = response.json()
        return {"access_token": token_data["access_token"]}
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to exchange code for token: {str(e)}")

@app.post("/spotify/playlists")
async def get_spotify_playlists(request: SpotifyPlaylistsRequest):
    """Get user's Spotify playlists"""
    try:
        print(f"Fetching playlists with token: {request.access_token[:20]}...")
        headers = {"Authorization": f"Bearer {request.access_token}"}
        response = requests.get("https://api.spotify.com/v1/me/playlists", headers=headers)
        
        print(f"Spotify API response status: {response.status_code}")
        
        if response.status_code == 401:
            raise HTTPException(status_code=401, detail="Invalid or expired Spotify access token")
        elif response.status_code == 403:
            raise HTTPException(status_code=403, detail="Insufficient permissions to access playlists")
        elif response.status_code != 200:
            print(f"Spotify API error response: {response.text}")
            raise HTTPException(status_code=response.status_code, detail=f"Spotify API error: {response.text}")
        
        response.raise_for_status()
        
        playlists_data = response.json()
        print(f"Found {len(playlists_data.get('items', []))} playlists")
        
        playlists = []
        
        for playlist in playlists_data.get("items", []):
            playlists.append({
                "id": playlist["id"],
                "name": playlist["name"],
                "tracks": {"total": playlist["tracks"]["total"]}
            })
        
        return {"playlists": playlists}
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        print(f"Unexpected error fetching playlists: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Failed to fetch playlists: {str(e)}")

@app.post("/spotify/playlist/{playlist_id}/tracks")
async def get_spotify_playlist_tracks(playlist_id: str, request: SpotifyTracksRequest):
    """Get tracks from a specific Spotify playlist with pagination support"""
    try:
        headers = {"Authorization": f"Bearer {request.access_token}"}
        all_tracks = []
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        
        # Handle pagination to get ALL tracks
        while url:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            tracks_data = response.json()
            
            # Process tracks from this page
            for item in tracks_data.get("items", []):
                track = item["track"]
                if track:  # Some items might be null
                    all_tracks.append({
                        "name": track["name"],
                        "artist": track["artists"][0]["name"] if track["artists"] else "Unknown Artist",
                        "album": track["album"]["name"] if track["album"] else None
                    })
            
            # Get next page URL (None if this is the last page)
            url = tracks_data.get("next")
        
        print(f"Fetched {len(all_tracks)} tracks total for playlist {playlist_id}")
        return {"tracks": all_tracks}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch playlist tracks: {str(e)}")

# YouTube endpoints
@app.post("/youtube/auto-authenticate")
async def auto_authenticate_youtube():
    """Automatically authenticate with YouTube using ytmusicapi"""
    global ytmusic_api
    
    try:
        # Use YouTube Music OAuth instead
        auth_result = await authenticate_youtube_music()
        if auth_result.get("success"):
            return {
                "success": True,
                "message": "✅ YouTube Music OAuth authentication successful!",
                "method": "ytmusicapi_oauth"
            }
        else:
            return {
                "success": False,
                "message": "YouTube Music authentication failed. Please run setup_ytmusic_oauth.py first.",
                "requires_manual_setup": True,
                "instructions": [
                    "1. Run: python setup_ytmusic_oauth.py",
                    "2. Follow the browser header extraction process",
                    "3. Complete the ytmusicapi OAuth setup"
                ]
            }
            
    except Exception as e:
        return {
            "success": False,
            "message": f"YouTube Music authentication error: {str(e)}",
            "requires_manual_setup": True
        }

@app.get("/youtube/auth-status")
async def get_youtube_auth_status():
    """Check YouTube authentication status"""
    global ytmusic_api
    
    # Check YouTube Music API
    if ytmusic_api:
        try:
            # Test with a simple search to verify the connection
            search_results = ytmusic_api.search("test", filter="songs", limit=1)
            return {
                "authenticated": True,
                "method": "ytmusicapi_oauth",
                "message": "YouTube Music is authenticated and ready"
            }
        except Exception as e:
            return {
                "authenticated": False,
                "method": "ytmusicapi_oauth",
                "message": f"Authentication expired or invalid: {str(e)}"
            }
    else:
        return {
            "authenticated": False,
            "message": "YouTube Music not authenticated"
        }

@app.post("/youtube/submit-headers")
async def submit_youtube_headers(request: dict):
    """Process and save YouTube Music headers from cURL or raw format"""
    global ytmusic_api
    
    try:
        headers_input = request.get('headers', '').strip()
        if not headers_input:
            return {
                "success": False,
                "message": "No headers provided"
            }
        
        print(f"Received headers input (first 200 chars): {headers_input[:200]}...")
        
        # Parse headers from different formats
        parsed_headers = {}
        
        if headers_input.startswith('curl'):
            # Clean up Windows CMD-style escaping
            cleaned_curl = headers_input.replace('^"', '"').replace('^', '').replace('\n', ' ')
            
            # Parse cURL format
            import re
            
            # Extract headers from -H parameters
            header_pattern = r'-H\s+"([^:]+):\s*([^"]+)"'
            matches = re.findall(header_pattern, cleaned_curl)
            
            for key, value in matches:
                parsed_headers[key.lower().strip()] = value.strip()
            
            # Extract cookies from -b parameter
            cookie_pattern = r'-b\s+"([^"]+)"'
            cookie_match = re.search(cookie_pattern, cleaned_curl)
            if cookie_match:
                cookie_header = cookie_match.group(1)
                # URL decode the cookies
                import urllib.parse
                cookie_header = urllib.parse.unquote(cookie_header)
                parsed_headers['cookie'] = cookie_header
            
            print(f"Parsed {len(parsed_headers)} headers from cURL command")
        else:
            # Parse raw headers format
            lines = headers_input.split('\n')
            for line in lines:
                line = line.strip()
                if ':' in line and not line.startswith(':'):
                    key, value = line.split(':', 1)
                    parsed_headers[key.strip().lower()] = value.strip()
        
        # Extract required YouTube Music authentication data
        auth_data = {}
        
        # Get cookie values
        cookie_header = parsed_headers.get('cookie', '')
        if cookie_header:
            import re
            # Extract key cookie values
            cookie_patterns = {
                'SAPISID': r'SAPISID=([^;]+)',
                'APISID': r'APISID=([^;]+)', 
                'HSID': r'HSID=([^;]+)',
                'SSID': r'SSID=([^;]+)',
                'SID': r'SID=([^;]+)',
                '__Secure-3PSID': r'__Secure-3PSID=([^;]+)'
            }
            
            for key, pattern in cookie_patterns.items():
                match = re.search(pattern, cookie_header)
                if match:
                    auth_data[key] = match.group(1)
        
        # Get visitor ID
        visitor_id = parsed_headers.get('x-goog-visitor-id', '')
        if visitor_id:
            auth_data['visitor_id'] = visitor_id
            
        # Get user agent
        user_agent = parsed_headers.get('user-agent', '')
        if user_agent:
            auth_data['user_agent'] = user_agent
        
        # Create ytmusicapi headers format
        ytmusic_headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': parsed_headers.get('authorization', ''),
            'content-type': 'application/json',
            'cookie': cookie_header,
            'origin': 'https://music.youtube.com',
            'referer': 'https://music.youtube.com/',
            'user-agent': user_agent,
            'x-goog-authuser': '0',
            'x-goog-visitor-id': visitor_id,
            'x-origin': 'https://music.youtube.com',
            'x-youtube-bootstrap-logged-in': 'true',
            'x-youtube-client-name': '67',
            'x-youtube-client-version': parsed_headers.get('x-youtube-client-version', '1.20250730.03.00')
        }
        
        # Initialize YTMusic with headers
        try:
            from ytmusicapi import YTMusic
            
            # Save headers to file for ytmusicapi
            import json
            headers_file = os.path.join(os.path.dirname(__file__), 'ytmusic_headers.json')
            with open(headers_file, 'w') as f:
                json.dump(ytmusic_headers, f, indent=2)
            
            # Initialize YTMusic
            ytmusic_api = YTMusic(headers_file)
            
            # Test the connection
            test_search = ytmusic_api.search("test", filter="songs", limit=1)
            
            return {
                "success": True,
                "message": "🎵 YouTube Music authentication successful!",
                "headers_saved": True
            }
            
        except Exception as ytmusic_error:
            print(f"YTMusic initialization error: {ytmusic_error}")
            return {
                "success": False,
                "message": f"Failed to initialize YouTube Music: {str(ytmusic_error)}"
            }
            
    except Exception as e:
        print(f"Headers parsing error: {e}")
        return {
            "success": False,
            "message": f"Failed to parse headers: {str(e)}"
        }

# YouTube Music endpoints
@app.post("/youtube-music/authenticate")
async def authenticate_youtube_music():
    """Authenticate with YouTube Music using ytmusicapi OAuth"""
    global ytmusic_api
    
    try:
        import json
        import os
        
        print("🔧 Loading YouTube Music OAuth credentials...")
        
        # Load ytmusic_oauth.json
        oauth_file = os.path.join(os.path.dirname(__file__), '..', 'ytmusic_oauth.json')
        if not os.path.exists(oauth_file):
            oauth_file = 'ytmusic_oauth.json'
        
        print(f"✅ Using ytmusicapi OAuth file: {oauth_file}")
        
        # Initialize YTMusicAPI client directly
        from ytmusicapi import YTMusic
        ytmusic_api = YTMusic(oauth_file)
        
        # Test the connection with a simple search
        try:
            search_results = ytmusic_api.search("test", filter="songs", limit=1)
            print(f"✅ YTMusicAPI authentication test successful! Found {len(search_results)} results")
            
            return {
                "success": True,
                "message": "YouTube Music authentication successful with ytmusicapi OAuth",
                "method": "ytmusicapi_oauth"
            }
        except Exception as e:
            print(f"❌ YTMusicAPI authentication test failed: {e}")
            return {
                "success": False,
                "message": f"YouTube Music OAuth authentication failed: {str(e)}",
                "instructions": [
                    "1. Make sure ytmusic_oauth.json exists in the backend directory",
                    "2. Run setup_ytmusic_oauth.py to generate fresh OAuth credentials",
                    "3. Ensure your browser headers in fresh_raw_headers.txt are recent"
                ]
            }
            
    except Exception as e:
        return {
            "success": False,
            "message": f"YouTube Music authentication error: {str(e)}"
        }

@app.post("/youtube-music/auth-status")
async def get_youtube_music_auth_status():
    """Check YouTube Music authentication status"""
    global ytmusic_api
    
    if ytmusic_api:
        try:
            # Test with a simple search to verify the connection
            search_results = ytmusic_api.search("test", filter="songs", limit=1)
            return {
                "authenticated": True,
                "method": "ytmusicapi_oauth",
                "message": "YouTube Music is authenticated and ready"
            }
        except Exception as e:
            return {
                "authenticated": False,
                "method": "ytmusicapi_oauth",
                "message": f"Authentication expired or invalid: {str(e)}"
            }
    else:
        return {
            "authenticated": False,
            "message": "YouTube Music not authenticated"
        }

@app.post("/youtube-music/setup")
async def setup_youtube_music(request: YouTubeMusicSetupRequest):
    """Setup YouTube Music (currently using ytmusicapi OAuth only)"""
    return {
        "success": False,
        "message": "Manual setup not supported. Use /youtube-music/authenticate with ytmusicapi OAuth.",
        "instructions": [
            "1. Run setup_ytmusic_oauth.py to generate OAuth credentials",
            "2. Use /youtube-music/authenticate endpoint to connect"
        ]
    }

@app.post("/test-youtube-music")
async def test_youtube_music():
    """Test YouTube Music connection without creating playlist"""
    global ytmusic_api
    
    if not ytmusic_api:
        # Try to authenticate first
        auth_result = await authenticate_youtube_music()
        if not auth_result.get("success"):
            return {"success": False, "message": "Authentication failed"}
    
    try:
        # Try a simple search
        search_results = ytmusic_api.search("test", filter="songs", limit=1)
        return {
            "success": True, 
            "message": f"YouTube Music working! Found {len(search_results)} results",
            "results": search_results
        }
    except Exception as e:
        return {"success": False, "message": f"Test failed: {str(e)}"}

@app.post("/test-youtube-music-search")
async def test_youtube_music_search():
    """Test YouTube Music search functionality"""
    global ytmusic_api
    
    if not ytmusic_api:
        # Try to authenticate first
        auth_result = await authenticate_youtube_music()
        if not auth_result.get("success"):
            return {"success": False, "message": "Authentication failed"}
    
    try:
        # Test search with a popular song
        search_results = ytmusic_api.search("300 Violin Orchestra Jorge Quintero", filter="songs", limit=3)
        return {
            "success": True, 
            "message": f"Search test completed! Found {len(search_results)} results",
            "results": search_results
        }
    except Exception as e:
        return {"success": False, "message": f"Search test failed: {str(e)}"}

@app.post("/import-playlist", response_model=ImportResponse)
async def import_playlist_youtube_music(request: ImportRequest):
    """Import a playlist using YouTube Music API"""
    global ytmusic_api
    
    try:
        # Debug: Print the received request
        print(f"Received import request:")
        print(f"  Playlist name: {request.playlistName}")
        print(f"  Number of tracks: {len(request.tracks)}")
        for i, track in enumerate(request.tracks):
            print(f"  Track {i+1}: {track.name} - {track.artist}")
        
        # Validate that we have tracks to import
        if not request.tracks or len(request.tracks) == 0:
            raise HTTPException(status_code=400, detail="No tracks provided for import")
            
    except Exception as validation_error:
        print(f"Request validation error: {validation_error}")
        print(f"Request type: {type(request)}")
        raise HTTPException(status_code=400, detail=f"Invalid request format: {str(validation_error)}")
    
    # Check if YouTube Music authentication is available
    if not ytmusic_api:
        # Try to authenticate
        try:
            ytmusic_result = await authenticate_youtube_music()
            if not ytmusic_result.get("success"):
                raise HTTPException(
                    status_code=401, 
                    detail="YouTube Music authentication failed. Please run 'python setup_ytmusic_oauth.py' or refresh your YouTube Music session."
                )
        except:
            raise HTTPException(
                status_code=401, 
                detail="YouTube Music authentication failed. Please run 'python setup_ytmusic_oauth.py' or refresh your YouTube Music session."
            )
    
    try:
        # Sanitize playlist name and create a fallback if needed
        import re
        from datetime import datetime
        
        # Remove emojis and special characters, keep alphanumeric, spaces, hyphens, underscores
        sanitized_playlist_name = re.sub(r'[^\w\s\-_]', '', request.playlistName).strip()
        
        # If the name is empty or too short after sanitization, create a unique fallback
        if not sanitized_playlist_name or len(sanitized_playlist_name) < 3:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            sanitized_playlist_name = f"Imported_Playlist_{timestamp}"
            print(f"🔧 Original name not usable, using fallback: {sanitized_playlist_name}")
        else:
            print(f"🔧 Using sanitized name: {sanitized_playlist_name}")
        
        # Create playlist using ytmusicapi
        print(f"Creating playlist: {sanitized_playlist_name}")
        
        playlist_id = None
        try:
            print("� Creating playlist with ytmusicapi...")
            playlist_id = ytmusic_api.create_playlist(sanitized_playlist_name, "", "PRIVATE")
            if playlist_id:
                print(f"✅ YTMusicAPI playlist created successfully with ID: {playlist_id}")
            else:
                print("⚠️ YTMusicAPI playlist creation returned no ID")
        except Exception as ytmusic_error:
            print(f"⚠️ YTMusicAPI playlist creation failed: {ytmusic_error}")
            raise HTTPException(status_code=500, detail=f"Failed to create playlist: {str(ytmusic_error)}")
        
        if not playlist_id:
            raise HTTPException(status_code=500, detail="Failed to create playlist")
            raise HTTPException(status_code=500, detail="Failed to create playlist")
        
        print(f"Playlist created successfully with ID: {playlist_id}")
        
        # Process each track
        added_tracks = []
        failed_tracks = []
        video_ids = []
        
        for track in request.tracks:
            try:
                # Try different search strategies
                search_queries = [
                    f"{track.name} {track.artist}",
                    track.name,
                    f"{track.artist} {track.name}"
                ]
                
                video_id = None
                for search_query in search_queries:
                    try:
                        print(f"Searching for: {search_query}")
                        search_results = ytmusic_api.search(search_query, filter="songs", limit=3)
                        
                        if search_results and len(search_results) > 0:
                            # Use the first result
                            video_id = search_results[0].get('videoId')
                            if video_id:
                                break
                    except Exception as search_error:
                        print(f"Search error for '{search_query}': {search_error}")
                        continue
                
                if video_id:
                    video_ids.append(video_id)
                    print(f"Found video for: {track.name} - {track.artist} (video_id: {video_id})")
                else:
                    print(f"Failed to find: {track.name} - {track.artist}")
                    failed_tracks.append(f"{track.name} - {track.artist}")
                    
            except Exception as track_error:
                print(f"Error processing track {track.name}: {track_error}")
                failed_tracks.append(f"{track.name} - {track.artist}")
        
        # Now attempt to add the found videos to the playlist
        if video_ids:
            try:
                print(f"🎵 SEARCH SUCCESS: Found {len(video_ids)} real YouTube Music videos!")
                for i, video_id in enumerate(video_ids):
                    track_name = f"{request.tracks[i].name} - {request.tracks[i].artist}" if i < len(request.tracks) else "Unknown"
                    print(f"   ✅ {track_name} → Video ID: {video_id}")
                
                # Add songs to the playlist using ytmusicapi
                print("🔧 Adding songs to playlist with ytmusicapi...")
                for video_id in video_ids:
                    try:
                        result = ytmusic_api.add_playlist_items(playlist_id, [video_id])
                        if result:
                            added_tracks.append(video_id)
                            print(f"   ✅ Added video {video_id} to playlist")
                        else:
                            failed_tracks.append(video_id)
                            print(f"   ❌ Failed to add video {video_id}")
                    except Exception as add_error:
                        print(f"   ❌ Error adding video {video_id}: {add_error}")
                        failed_tracks.append(video_id)
            except Exception as playlist_add_error:
                print(f"⚠️ Error adding songs to playlist: {playlist_add_error}")
                failed_tracks.extend([f"{track.name} - {track.artist}" for track in request.tracks])
        
        # Create YouTube Music playlist URL
        playlist_url = f"https://music.youtube.com/playlist?list={playlist_id}" if playlist_id else None
        
        return ImportResponse(
            playlistUrl=playlist_url,
            addedTracks=added_tracks,
            failedTracks=failed_tracks,
            message=f"Import completed successfully! {len(added_tracks)} tracks added, {len(failed_tracks)} failed."
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        print(f"Import failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to import playlist: {str(e)}")

@app.post("/import-playlist-stream")
async def import_playlist_with_progress(request: ImportRequest):
    """Import a playlist with real-time progress updates via Server-Sent Events"""
    global ytmusic_api
    
    async def generate_progress():
        try:
            # Validate request
            if not request.tracks or len(request.tracks) == 0:
                yield f"data: {json.dumps({'type': 'error', 'message': 'No tracks provided for import'})}\n\n"
                return
            
            # Check YouTube Music authentication
            if not ytmusic_api:
                try:
                    ytmusic_result = await authenticate_youtube_music()
                    if not ytmusic_result.get("success"):
                        yield f"data: {json.dumps({'type': 'error', 'message': 'YouTube Music authentication failed'})}\n\n"
                        return
                except:
                    yield f"data: {json.dumps({'type': 'error', 'message': 'YouTube Music authentication failed'})}\n\n"
                    return
            
            total_tracks = len(request.tracks)
            yield f"data: {json.dumps({'type': 'start', 'total': total_tracks, 'playlistName': request.playlistName})}\n\n"
            
            # Sanitize playlist name
            import re
            sanitized_playlist_name = re.sub(r'[^\w\s\-_]', '', request.playlistName).strip()
            if not sanitized_playlist_name or len(sanitized_playlist_name) < 3:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                sanitized_playlist_name = f"Imported_Playlist_{timestamp}"
            
            yield f"data: {json.dumps({'type': 'status', 'message': f'Creating playlist: {sanitized_playlist_name}'})}\n\n"
            
            # Create playlist
            try:
                playlist_id = ytmusic_api.create_playlist(sanitized_playlist_name, "", "PRIVATE")
                if not playlist_id:
                    yield f"data: {json.dumps({'type': 'error', 'message': 'Failed to create playlist'})}\n\n"
                    return
                    
                yield f"data: {json.dumps({'type': 'status', 'message': f'Playlist created successfully!'})}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'type': 'error', 'message': f'Failed to create playlist: {str(e)}'})}\n\n"
                return
            
            # Process tracks with progress updates
            added_tracks = []
            failed_tracks = []
            video_ids = []
            
            for i, track in enumerate(request.tracks):
                progress = int((i / total_tracks) * 100)
                yield f"data: {json.dumps({'type': 'progress', 'progress': progress, 'current': i + 1, 'total': total_tracks, 'track': f'{track.name} - {track.artist}'})}\n\n"
                
                try:
                    # Search for the track
                    search_queries = [
                        f"{track.name} {track.artist}",
                        track.name,
                        f"{track.artist} {track.name}"
                    ]
                    
                    video_id = None
                    for search_query in search_queries:
                        try:
                            search_results = ytmusic_api.search(search_query, filter="songs", limit=3)
                            if search_results and len(search_results) > 0:
                                video_id = search_results[0].get('videoId')
                                if video_id and video_id not in video_ids:
                                    break
                        except Exception as search_error:
                            continue
                    
                    if video_id:
                        yield f"data: {json.dumps({'type': 'track_found', 'track': f'{track.name} - {track.artist}', 'videoId': video_id})}\n\n"
                        video_ids.append(video_id)
                        added_tracks.append({
                            "name": track.name,
                            "artist": track.artist,
                            "video_id": video_id
                        })
                    else:
                        yield f"data: {json.dumps({'type': 'track_not_found', 'track': f'{track.name} - {track.artist}'})}\n\n"
                        failed_tracks.append({
                            "name": track.name,
                            "artist": track.artist,
                            "reason": "Not found on YouTube Music"
                        })
                        
                except Exception as track_error:
                    yield f"data: {json.dumps({'type': 'track_error', 'track': f'{track.name} - {track.artist}', 'error': str(track_error)})}\n\n"
                    failed_tracks.append({
                        "name": track.name,
                        "artist": track.artist,
                        "reason": str(track_error)
                    })
                
                # Small delay to prevent rate limiting
                await asyncio.sleep(0.1)
            
            # Add all found tracks to playlist
            if video_ids:
                yield f"data: {json.dumps({'type': 'status', 'message': f'Adding {len(video_ids)} songs to playlist...'})}\n\n"
                
                try:
                    ytmusic_api.add_playlist_items(playlist_id, video_ids)
                    yield f"data: {json.dumps({'type': 'status', 'message': f'Successfully added {len(video_ids)} songs to playlist!'})}\n\n"
                except Exception as add_error:
                    yield f"data: {json.dumps({'type': 'error', 'message': f'Failed to add songs to playlist: {str(add_error)}'})}\n\n"
                    return
            
            # Generate playlist URL
            playlist_url = f"https://music.youtube.com/playlist?list={playlist_id}"
            
            # Send final result
            result = {
                'type': 'complete',
                'progress': 100,
                'playlistUrl': playlist_url,
                'stats': {
                    'total': total_tracks,
                    'successful': len(added_tracks),
                    'failed': len(failed_tracks),
                    'skipped': 0
                },
                'addedTracks': added_tracks,
                'failedTracks': failed_tracks,
                'message': f"Import completed! {len(added_tracks)} tracks added, {len(failed_tracks)} failed."
            }
            
            yield f"data: {json.dumps(result)}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': f'Import failed: {str(e)}'})}\n\n"
    
    return StreamingResponse(
        generate_progress(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "text/event-stream",
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)