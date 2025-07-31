# 🎵 Spotify → YouTube Playlist Importer

A professional web application that seamlessly imports your Spotify playlists to YouTube using the official YouTube Data API v3.

## ✨ Features

- 🔐 **Secure OAuth Authentication** - Both Spotify and YouTube
- 📋 **Smart Playlist Management** - Browse and select playlists
- 🎵 **Intelligent Track Matching** - Advanced search algorithms
- 🚀 **Bulk Import** - Import entire playlists with one click
- 📊 **Detailed Reports** - Track success and failure rates
- 🔗 **Direct Links** - Get direct links to your new YouTube playlists
- 🏗️ **Professional Architecture** - Clean, maintainable codebase

## 🏗️ Project Structure

```
playlist_importer/
├── 📁 src/
│   ├── 📁 backend/
│   │   ├── 📁 api/              # FastAPI endpoints
│   │   ├── 📁 services/         # Business logic (YouTube, Spotify)
│   │   ├── 📁 models/           # Database models
│   │   ├── 📁 utils/            # Utility functions
│   │   ├── 📁 config/           # Configuration management
│   │   ├── 📁 tests/            # Backend tests
│   │   ├── main.py             # Application entry point
│   │   └── requirements.txt    # Python dependencies
│   └── 📁 frontend/            # React application
├── 📁 scripts/                 # Setup & utility scripts
├── 📁 docs/                    # Documentation
├── 📁 config/                  # Project configuration
├── 📁 credentials/             # OAuth credentials (secure)
├── .env.example               # Environment template
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** (v16+)
- **Python** (v3.8+)
- **Spotify Developer Account**
- **Google Cloud Account** (for YouTube Data API v3)

### 1. Clone & Setup

```bash
git clone <your-repo-url>
cd playlist_importer
cp .env.example .env
```

### 2. Spotify API Setup

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new application
3. Add `http://localhost:3000/callback` to Redirect URIs
4. Update `.env` with your credentials:
   ```
   SPOTIFY_CLIENT_ID=your_client_id
   SPOTIFY_CLIENT_SECRET=your_client_secret
   ```

### 3. YouTube API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create/select a project
3. Enable YouTube Data API v3
4. Create OAuth 2.0 credentials (Desktop Application)
5. Download credentials as `youtube_credentials.json`
6. Place in `credentials/` directory

### 4. Backend Setup

```bash
cd src/backend
pip install -r requirements.txt
python main.py
```

### 5. Frontend Setup

```bash
cd src/frontend
npm install
npm start
```

## 🔧 Configuration

All configuration is managed through environment variables. See `.env.example` for all available options.

## 📚 API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation.

## 🧪 Testing

```bash
# Backend tests
cd src/backend
python -m pytest tests/

# Test YouTube API connection
python scripts/setup_youtube_api.py
```

## 🛡️ Security

- OAuth 2.0 for all authentication
- Credentials stored securely
- CORS properly configured
- No sensitive data logged

## 📄 License

Educational use only. Please respect Spotify and YouTube's terms of service.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

**Made with ❤️ for music lovers everywhere**