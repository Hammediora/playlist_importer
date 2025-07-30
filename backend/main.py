from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import ytmusicapi
import json
import os
import requests
from datetime import datetime

app = FastAPI(title="Playlist Importer API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Spotify API configuration
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "your_spotify_client_id")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "your_spotify_client_secret")
SPOTIFY_REDIRECT_URI = "http://localhost:3000"

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

# Global ytmusic instance
ytmusic = None

def initialize_ytmusic():
    """Initialize YouTube Music API with authentication"""
    global ytmusic
    
    # Check if auth headers file exists
    auth_headers_path = "auth_headers.json"
    
    if os.path.exists(auth_headers_path):
        try:
            with open(auth_headers_path, 'r') as f:
                headers = json.load(f)
            ytmusic = ytmusicapi.YTMusic(headers=headers)
            print("YouTube Music API initialized with saved headers")
            return True
        except Exception as e:
            print(f"Failed to load auth headers: {e}")
    
    # If no saved headers, try to create new ones
    try:
        ytmusic = ytmusicapi.YTMusic()
        print("YouTube Music API initialized (you may need to authenticate)")
        return True
    except Exception as e:
        print(f"Failed to initialize YouTube Music API: {e}")
        return False

@app.on_event("startup")
async def startup_event():
    """Initialize YouTube Music API on startup"""
    initialize_ytmusic()

@app.get("/")
async def root():
    return {"message": "Playlist Importer API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "ytmusic_initialized": ytmusic is not None}

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
        response.raise_for_status()
        
        token_data = response.json()
        return {"access_token": token_data["access_token"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to exchange code for token: {str(e)}")

@app.post("/spotify/playlists")
async def get_spotify_playlists(request: SpotifyPlaylistsRequest):
    """Get user's Spotify playlists"""
    try:
        headers = {"Authorization": f"Bearer {request.access_token}"}
        response = requests.get("https://api.spotify.com/v1/me/playlists", headers=headers)
        response.raise_for_status()
        
        playlists_data = response.json()
        playlists = []
        
        for playlist in playlists_data.get("items", []):
            playlists.append({
                "id": playlist["id"],
                "name": playlist["name"],
                "tracks": {"total": playlist["tracks"]["total"]}
            })
        
        return {"playlists": playlists}
    except Exception as e:
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

# YouTube Music endpoints
@app.post("/youtube/authenticate")
async def authenticate_youtube_music(request: YouTubeAuthRequest):
    """Authenticate with YouTube Music using provided headers"""
    try:
        # Parse and validate the auth headers
        headers = json.loads(request.auth_headers)
        
        # Test the headers by creating a YTMusic instance
        test_ytmusic = ytmusicapi.YTMusic(headers=headers)
        
        # Save the headers for future use
        with open("auth_headers.json", "w") as f:
            json.dump(headers, f)
        
        # Update the global instance
        global ytmusic
        ytmusic = test_ytmusic
        
        return {"message": "YouTube Music authentication successful"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to authenticate with YouTube Music: {str(e)}")

@app.post("/import-playlist", response_model=ImportResponse)
async def import_playlist(request: ImportRequest):
    """Import a playlist from Spotify to YouTube Music"""
    
    if not ytmusic:
        raise HTTPException(status_code=500, detail="YouTube Music API not initialized")
    
    try:
        # Create playlist
        playlist_name = request.playlistName
        playlist_id = ytmusic.create_playlist(playlist_name, "Imported from Spotify")
        
        added_tracks = []
        failed_tracks = []
        
        # Process each track
        for track in request.tracks:
            try:
                # Search for the track
                search_query = f"{track.name} {track.artist}"
                search_results = ytmusic.search(search_query, filter="songs", limit=1)
                
                if search_results and len(search_results) > 0:
                    # Add the first (best) match to the playlist
                    video_id = search_results[0]['videoId']
                    ytmusic.add_playlist_items(playlist_id, [video_id])
                    added_tracks.append(f"{track.name} - {track.artist}")
                else:
                    failed_tracks.append(f"{track.name} - {track.artist}")
                    
            except Exception as e:
                print(f"Failed to process track {track.name}: {e}")
                failed_tracks.append(f"{track.name} - {track.artist}")
        
        # Get playlist URL
        playlist_url = f"https://music.youtube.com/playlist?list={playlist_id}"
        
        return ImportResponse(
            playlistUrl=playlist_url,
            addedTracks=added_tracks,
            failedTracks=failed_tracks,
            message=f"Successfully imported {len(added_tracks)} tracks to YouTube Music"
        )
        
    except Exception as e:
        print(f"Import failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to import playlist: {str(e)}")

@app.get("/setup-instructions")
async def get_setup_instructions():
    """Return instructions for setting up YouTube Music authentication"""
    return {
        "message": "YouTube Music Authentication Setup",
        "instructions": [
            "1. Install ytmusicapi: pip install ytmusicapi",
            "2. Run: python -c \"import ytmusicapi; ytmusicapi.setup(filepath='auth_headers.json')\"",
            "3. Follow the browser authentication process",
            "4. The auth_headers.json file will be created in the backend directory",
            "5. Restart the FastAPI server"
        ],
        "note": "The auth_headers.json file contains your YouTube Music authentication tokens"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 