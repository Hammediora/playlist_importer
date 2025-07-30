# Spotify → YouTube Music Playlist Importer

A web application that allows you to import your Spotify playlists to YouTube Music seamlessly.

## Features

- 🔐 **Spotify OAuth Authentication** - Secure login with your Spotify account
- 📋 **Playlist Selection** - Browse and select from your Spotify playlists
- 🎵 **Track Preview** - View all tracks before importing
- 🚀 **One-Click Import** - Import entire playlists to YouTube Music
- 📊 **Import Summary** - See which tracks were successfully added and which failed
- 🔗 **Direct Links** - Get direct links to your new YouTube Music playlists

## Project Structure

```
playlist_importer/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main API server
│   └── requirements.txt    # Python dependencies
├── public/                 # React public files
├── src/                    # React source code
│   ├── App.js             # Main React component
│   ├── index.js           # React entry point
│   └── index.css          # Styles with Tailwind
├── package.json           # React dependencies
├── tailwind.config.js     # Tailwind configuration
└── README.md              # This file
```

## Prerequisites

- **Node.js** (v16 or higher)
- **Python** (v3.8 or higher)
- **Spotify Developer Account** (for OAuth)
- **YouTube Music Account** (for importing)

## Setup Instructions

### 1. Spotify OAuth Setup

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new application
3. Add `http://localhost:3000/callback` to the Redirect URIs
4. Copy your Client ID
5. Update the `clientId` in `src/App.js` (line 47):
   ```javascript
   const clientId = 'YOUR_SPOTIFY_CLIENT_ID'; // Replace with your actual Client ID
   ```

### 2. Frontend Setup

```bash
# Install dependencies
npm install

# Start the development server
npm start
```

The React app will run on `http://localhost:3000`

### 3. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup YouTube Music authentication
python -c "import ytmusicapi; ytmusicapi.setup(filepath='auth_headers.json')"

# Start the FastAPI server
python main.py
```

The FastAPI backend will run on `http://localhost:8000`

### 4. YouTube Music Authentication

The `ytmusicapi.setup()` command will:
1. Open your browser
2. Ask you to log into your Google account
3. Request permission to access YouTube Music
4. Save authentication headers to `auth_headers.json`

**Important**: Keep the `auth_headers.json` file secure - it contains your authentication tokens.

## Usage

1. **Start both servers** (frontend on port 3000, backend on port 8000)
2. **Open** `http://localhost:3000` in your browser
3. **Click** "Connect with Spotify" and authorize the app
4. **Select** a playlist from your Spotify library
5. **Review** the tracks that will be imported
6. **Click** "Import to YouTube Music"
7. **Wait** for the import to complete
8. **Click** the link to view your new YouTube Music playlist

## API Endpoints

### Backend API (FastAPI)

- `GET /` - Health check
- `GET /health` - Detailed health status
- `POST /import-playlist` - Import playlist to YouTube Music
- `GET /setup-instructions` - YouTube Music setup instructions

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
  "playlistUrl": "https://music.youtube.com/playlist?list=...",
  "addedTracks": ["Song 1 - Artist 1", "Song 2 - Artist 2"],
  "failedTracks": ["Song 3 - Artist 3"],
  "message": "Successfully imported 2 tracks to YouTube Music"
}
```

## Troubleshooting

### Common Issues

1. **"YouTube Music API not initialized"**
   - Run the YouTube Music authentication setup again
   - Check that `auth_headers.json` exists in the backend directory

2. **"Failed to fetch playlists"**
   - Check your Spotify Client ID in `src/App.js`
   - Ensure the redirect URI is correctly set in Spotify Developer Dashboard

3. **"Import failed"**
   - Check that both servers are running
   - Verify YouTube Music authentication is working
   - Check browser console for detailed error messages

4. **CORS errors**
   - Ensure the backend is running on port 8000
   - Check that CORS is properly configured in `main.py`

### Debug Mode

To run the backend in debug mode:
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Security Notes

- **Spotify tokens** are stored in browser localStorage (temporary)
- **YouTube Music headers** are stored in `auth_headers.json` (keep secure)
- **CORS** is configured to only allow `localhost:3000`
- **No sensitive data** is logged or stored permanently

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational purposes. Please respect Spotify and YouTube Music's terms of service.

## Dependencies

### Frontend
- React 18.2.0
- Axios 1.6.0
- Lucide React 0.294.0
- Tailwind CSS 3.3.0

### Backend
- FastAPI 0.104.1
- Uvicorn 0.24.0
- ytmusicapi 0.24.1
- Pydantic 2.5.0 