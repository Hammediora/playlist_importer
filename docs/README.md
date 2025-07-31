# Spotify → YouTube Playlist Importer

A web application that allows you to import your Spotify playlists to YouTube seamlessly using the official YouTube Data API v3.

## Features

- 🔐 **Spotify OAuth Authentication** - Secure login with your Spotify account
- 📋 **Playlist Selection** - Browse and select from your Spotify playlists
- 🎵 **Track Preview** - View all tracks before importing
- 🚀 **One-Click Import** - Import entire playlists to YouTube
- 📊 **Import Summary** - See which tracks were successfully added and which failed
- 🔗 **Direct Links** - Get direct links to your new YouTube playlists

## Project Structure

```
playlist_importer/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main API server
│   ├── youtube_api.py      # YouTube Data API v3 client
│   ├── setup_youtube_api.py # OAuth 2.0 setup script
│   ├── test_youtube_api.py # API testing script
│   └── requirements.txt    # Python dependencies
├── Frontend/               # React frontend
│   ├── src/
│   │   ├── App.js         # Main React component
│   │   ├── index.js       # React entry point
│   │   └── index.css      # Styles with Tailwind
│   ├── package.json       # React dependencies
│   └── tailwind.config.js # Tailwind configuration
├── YOUTUBE_API_MIGRATION.md # Migration guide
├── MIGRATION_SUMMARY.md   # Migration summary
└── README.md              # This file
```

## Prerequisites

- **Node.js** (v16 or higher)
- **Python** (v3.8 or higher)
- **Spotify Developer Account** (for OAuth)
- **Google Cloud Account** (for YouTube Data API v3)
- **YouTube Account** (for importing)

## Setup Instructions

### 1. Spotify OAuth Setup

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new application
3. Add `http://localhost:3000/callback` to the Redirect URIs
4. Copy your Client ID and Client Secret
5. Create a `.env` file in the backend directory:
   ```
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   SPOTIFY_REDIRECT_URI=http://127.0.0.1:3000/callback
   ```

### 2. YouTube API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable YouTube Data API v3:
   - Go to 'APIs & Services' > 'Library'
   - Search for 'YouTube Data API v3'
   - Click 'Enable'
4. Create OAuth 2.0 credentials:
   - Go to 'APIs & Services' > 'Credentials'
   - Click 'Create Credentials' > 'OAuth 2.0 Client IDs'
   - Choose 'Desktop application'
   - Download the JSON file
5. Rename the downloaded file to `youtube_credentials.json`
6. Place it in the `backend/` directory

### 3. Frontend Setup

```bash
cd Frontend
npm install
npm start
```

The React app will run on `http://localhost:3000`

### 4. Backend Setup

```bash
cd backend

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Test YouTube API setup
python test_youtube_api.py

# Start the FastAPI server
python main.py
```

The FastAPI backend will run on `http://localhost:8000`

## Usage

1. **Start both servers** (frontend on port 3000, backend on port 8000)
2. **Open** `http://localhost:3000` in your browser
3. **Click** "Connect with Spotify" and authorize the app
4. **Click** "Connect YouTube" and complete OAuth 2.0 authentication
5. **Select** a playlist from your Spotify library
6. **Review** the tracks that will be imported
7. **Click** "Import to YouTube"
8. **Wait** for the import to complete
9. **Click** the link to view your new YouTube playlist

## API Endpoints

### Backend API (FastAPI)

- `GET /` - Health check
- `GET /health` - Detailed health status
- `GET /youtube/auth-status` - Check YouTube authentication status
- `POST /youtube/auto-authenticate` - Authenticate with YouTube API
- `POST /import-playlist` - Import playlist to YouTube
- `GET /setup-instructions` - YouTube API setup instructions

### Request/Response Format

**Import Request:**
```json
{
  "playlistName": "My Playlist",
  "tracks": [
    {
      "name": "Song Title",
      "artist": "Artist Name",
      "album": "Album Name"
    }
  ]
}
```

**Import Response:**
```json
{
  "playlistUrl": "https://www.youtube.com/playlist?list=...",
  "addedTracks": ["Song 1 - Artist 1", "Song 2 - Artist 2"],
  "failedTracks": ["Song 3 - Artist 3"],
  "message": "Successfully imported 2 tracks to YouTube"
}
```

## Troubleshooting

### Common Issues

1. **"YouTube API not initialized"**
   - Click "Connect YouTube" in the frontend
   - Complete the OAuth 2.0 authentication flow
   - Check that `youtube_credentials.json` exists in the backend directory

2. **"Failed to fetch playlists"**
   - Check your Spotify credentials in the `.env` file
   - Ensure the redirect URI is correctly set in Spotify Developer Dashboard

3. **"Import failed"**
   - Check that both servers are running
   - Verify YouTube authentication is working
   - Check browser console for detailed error messages

4. **"OAuth consent screen error"**
   - Add your email as a test user in Google Cloud Console
   - Or change publishing status to "External"

### Debug Mode

To run the backend in debug mode:
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Security Notes

- **Spotify tokens** are stored in browser localStorage (temporary)
- **YouTube OAuth tokens** are stored in `youtube_token.pickle` (keep secure)
- **OAuth credentials** are stored in `youtube_credentials.json` (keep secure)
- **CORS** is configured to only allow `localhost:3000`
- **No sensitive data** is logged or stored permanently

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational purposes. Please respect Spotify and YouTube's terms of service.

## Dependencies

### Frontend
- React 18.2.0
- Axios 1.6.0
- Lucide React 0.294.0
- Tailwind CSS 3.3.0

### Backend
- FastAPI 0.104.1
- Uvicorn 0.24.0
- Google API Python Client 2.108.0
- Google Auth OAuthlib 1.1.0
- Pydantic 2.5.0 