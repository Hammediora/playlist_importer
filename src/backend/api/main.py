from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
import os
import requests
from datetime import datetime, timedelta
import subprocess
import sys

# Import from our organized structure
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import *
from services.youtube_api import YouTubeAPIClient
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
    
    # Don't initialize YouTube client on startup - wait for user action
    print("YouTube API will be initialized when user connects")
    
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

# Configuration is now imported from settings

# Pydantic models
class Track(BaseModel):
    name: str
    artist: str
    album: Optional[str] = None

class ImportRequest(BaseModel):
    playlistName: str
    tracks: List[Track]

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

class YouTubeAuthRequest(BaseModel):
    auth_headers: str

# Global YouTube API client
youtube_client = None

def initialize_youtube_client():
    """Initialize YouTube API client with OAuth 2.0 authentication"""
    global youtube_client
    
    try:
        youtube_client = YouTubeAPIClient()
        # Don't authenticate immediately - wait for user action
        print("YouTube API client created (authentication pending)")
        return True
    except Exception as e:
        print(f"Failed to initialize YouTube API client: {e}")
        return False

def is_youtube_client_working():
    """Test if the current YouTube client is working"""
    global youtube_client
    
    if not youtube_client:
        return False, "No YouTube client initialized"
    
    try:
        # Try a simple search to test authentication
        test_search = youtube_client.search_song("test", max_results=1)
        if test_search and len(test_search) > 0:
            return True, "YouTube client is working"
        else:
            return False, "Search returned no results"
    except Exception as e:
        return False, f"YouTube client test failed: {str(e)}"

def setup_youtube_api():
    """Setup YouTube API authentication using OAuth 2.0"""
    try:
        import sys
        import os
        from pathlib import Path
        
        # Add the backend directory to Python path
        backend_dir = Path(__file__).parent.parent
        sys.path.append(str(backend_dir))
        
        from setup_youtube_api import setup_youtube_api as setup_api
        success = setup_api()
        if success:
            return True, "YouTube API setup completed successfully"
        else:
            return False, "YouTube API setup failed"
    except Exception as e:
        return False, f"Error setting up YouTube API: {str(e)}"

@app.get("/")
async def root():
    return {"message": "Playlist Importer API", "status": "running"}

@app.get("/health")
async def health_check():
    """Enhanced health check including YouTube API status"""
    youtube_status = await get_youtube_auth_status()
    return {
        "status": "healthy", 
        "youtube_initialized": youtube_client is not None,
        "youtube_authenticated": youtube_status["authenticated"],
        "youtube_requires_setup": youtube_status["requires_setup"]
    }

# Spotify endpoints
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
    """Get tracks from a specific Spotify playlist"""
    try:
        headers = {"Authorization": f"Bearer {request.access_token}"}
        response = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", headers=headers)
        response.raise_for_status()
        
        tracks_data = response.json()
        tracks = []
        
        for item in tracks_data.get("items", []):
            track = item["track"]
            if track:  # Some items might be null
                tracks.append({
                    "name": track["name"],
                    "artist": track["artists"][0]["name"] if track["artists"] else "Unknown Artist",
                    "album": track["album"]["name"] if track["album"] else None
                })
        
        return {"tracks": tracks}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch playlist tracks: {str(e)}")

# YouTube API endpoints
@app.get("/youtube/auth-status")
async def get_youtube_auth_status():
    """Check YouTube API authentication status"""
    try:
        global youtube_client
        
        # Check if client exists and is authenticated
        if youtube_client and youtube_client.is_authenticated():
            return {
                "authenticated": True,
                "client_working": True,
                "message": "YouTube API is authenticated and ready",
                "requires_setup": False
            }
        else:
            return {
                "authenticated": False,
                "client_working": False,
                "message": "YouTube API not authenticated - click 'Connect YouTube' to authenticate",
                "requires_setup": True
            }
        
    except Exception as e:
        return {
            "authenticated": False,
            "client_working": False,
            "message": f"Error checking auth status: {str(e)}",
            "requires_setup": True
        }

@app.post("/youtube/auto-authenticate")
async def auto_authenticate_youtube():
    """Authenticate with YouTube API using OAuth 2.0"""
    try:
        global youtube_client
        
        # Initialize client if not already done
        if not youtube_client:
            initialize_youtube_client()
        
        # Try to authenticate
        if youtube_client and youtube_client.authenticate():
            return {
                "success": True,
                "message": "YouTube API authentication successful",
                "action": "authenticated"
            }
        else:
            return {
                "success": False,
                "message": "YouTube API authentication failed",
                "action": "setup_required",
                "requires_manual_setup": True,
                "instructions": [
                    "1. Make sure you have youtube_credentials.json in the backend directory",
                    "2. Click 'Connect YouTube' again to retry authentication",
                    "3. Follow the OAuth 2.0 authentication process in your browser"
                ]
            }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Authentication failed: {str(e)}",
            "action": "error"
        }

@app.post("/youtube/authenticate")
async def authenticate_youtube_api():
    """Authenticate with YouTube API using OAuth 2.0"""
    try:
        # Try to initialize and authenticate
        if initialize_youtube_client():
            client_working, client_msg = is_youtube_client_working()
            if client_working:
                return {"message": "YouTube API authentication successful"}
            else:
                raise HTTPException(status_code=400, detail=f"Authentication failed: {client_msg}")
        else:
            raise HTTPException(status_code=400, detail="Failed to initialize YouTube API client")
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to authenticate with YouTube API: {str(e)}")

@app.post("/import-playlist", response_model=ImportResponse)
async def import_playlist(request: ImportRequest):
    """Import a playlist from Spotify to YouTube"""
    
    if not youtube_client:
        # Try to reinitialize
        if not initialize_youtube_client():
            raise HTTPException(status_code=500, detail="YouTube API client not initialized. Please authenticate first.")
    
    # Check if client is working
    client_working, client_msg = is_youtube_client_working()
    if not client_working:
        raise HTTPException(status_code=401, detail=f"YouTube API authentication not working: {client_msg}")
    
    try:
        # Create the playlist
        try:
            print(f"Creating playlist: {request.playlistName}")
            playlist_id = youtube_client.create_playlist(
                request.playlistName, 
                "Imported from Spotify", 
                "public"
            )
            print(f"Playlist created successfully with ID: {playlist_id}")
        except Exception as create_error:
            print(f"Failed to create playlist: {create_error}")
            raise HTTPException(status_code=500, detail=f"Failed to create playlist: {str(create_error)}")
        
        if not playlist_id:
            raise HTTPException(status_code=500, detail="Failed to create playlist - no playlist ID returned")
        
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
                        search_results = youtube_client.search_song(search_query, max_results=3)
                        
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
        
        # Add all found videos to playlist
        if video_ids:
            try:
                added_video_ids, failed_video_ids = youtube_client.add_songs_to_playlist(playlist_id, video_ids)
                
                # Map video IDs back to track names for reporting
                for i, video_id in enumerate(video_ids):
                    track_name = f"{request.tracks[i].name} - {request.tracks[i].artist}"
                    if video_id in added_video_ids:
                        added_tracks.append(track_name)
                    elif video_id in failed_video_ids:
                        failed_tracks.append(track_name)
                        
            except Exception as add_error:
                print(f"Failed to add songs to playlist: {add_error}")
                failed_tracks.extend([f"{track.name} - {track.artist}" for track in request.tracks if f"{track.name} - {track.artist}" not in failed_tracks])
        
        # Create response
        playlist_url = youtube_client.get_playlist_url(playlist_id) if playlist_id else None
        
        return ImportResponse(
            playlistUrl=playlist_url,
            addedTracks=added_tracks,
            failedTracks=failed_tracks,
            message=f"Import completed. {len(added_tracks)} tracks added, {len(failed_tracks)} failed."
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        print(f"Import failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to import playlist: {str(e)}")

@app.get("/setup-instructions")
async def get_setup_instructions():
    """Return instructions for setting up YouTube API authentication"""
    return {
        "message": "YouTube API Authentication Setup",
        "instructions": [
            "1. Go to Google Cloud Console: https://console.cloud.google.com/",
            "2. Create a new project or select existing one",
            "3. Enable YouTube Data API v3:",
            "   - Go to 'APIs & Services' > 'Library'",
            "   - Search for 'YouTube Data API v3'",
            "   - Click 'Enable'",
            "4. Create credentials:",
            "   - Go to 'APIs & Services' > 'Credentials'",
            "   - Click 'Create Credentials' > 'OAuth 2.0 Client IDs'",
            "   - Choose 'Desktop application'",
            "   - Download the JSON file",
            "5. Rename the downloaded file to 'youtube_credentials.json'",
            "6. Place it in the backend directory",
            "7. Run: python setup_youtube_api.py",
            "8. Follow the OAuth 2.0 authentication process"
        ],
        "note": "This uses official YouTube Data API v3 with OAuth 2.0 authentication"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 