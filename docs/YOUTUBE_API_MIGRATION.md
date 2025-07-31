# YouTube API Migration Guide

## Overview

This guide explains the migration from the unofficial `ytmusicapi` library to the **official YouTube Data API v3** for better reliability and long-term support.

## Why Migrate?

### Problems with ytmusicapi
- **Unofficial API**: Reverse-engineered, can break with YouTube updates
- **Authentication Issues**: Header-based auth is fragile and expires quickly
- **Write Operation Failures**: 401 Unauthorized errors for playlist creation
- **Maintenance Burden**: Requires constant header refreshing

### Benefits of YouTube Data API v3
- **Official Support**: Google-maintained API with long-term stability
- **Proper OAuth 2.0**: Secure, standard authentication flow
- **Full Write Support**: Complete playlist creation and management
- **Future-Proof**: Less likely to break with YouTube updates
- **Better Error Handling**: Clear, actionable error messages

## Migration Steps

### 1. Install New Dependencies

The requirements.txt has been updated to remove `ytmusicapi` and include official Google API libraries:

```bash
pip install -r requirements.txt
```

### 2. Set Up Google Cloud Project

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

### 3. Run Setup Script

```bash
cd backend
python setup_youtube_api.py
```

This will:
- Validate your credentials file
- Start OAuth 2.0 authentication flow
- Test playlist creation and search functionality
- Save authentication tokens for future use

### 4. Update Frontend (Optional)

The frontend has been updated to work with the new API, but you may want to update the UI text:

- "YouTube Music" → "YouTube"
- "Connect YouTube Music" → "Connect YouTube"

## New Architecture

### Backend Changes

#### Old (ytmusicapi)
```python
from ytmusicapi import YTMusic
youtube_client = YTMusic("auth_headers.json")
playlist_id = youtube_client.create_playlist(name, description)
```

#### New (YouTube Data API v3)
```python
from youtube_api import YouTubeAPIClient
youtube_client = YouTubeAPIClient()
youtube_client.authenticate()  # OAuth 2.0 flow
playlist_id = youtube_client.create_playlist(name, description)
```

### Authentication Flow

#### Old: Header-based
1. Manual header extraction from browser
2. Headers expire quickly (1 hour)
3. Constant refreshing required
4. Prone to 401 errors

#### New: OAuth 2.0
1. One-time setup with Google Cloud Console
2. Automatic token refresh
3. Secure, standard authentication
4. Long-term reliability

## API Endpoints

### Updated Endpoints

| Endpoint | Old Behavior | New Behavior |
|----------|-------------|--------------|
| `/youtube/auth-status` | Check header freshness | Check OAuth token validity |
| `/youtube/auto-authenticate` | Try existing headers | Try OAuth token refresh |
| `/youtube/authenticate` | Manual header input | OAuth 2.0 flow |
| `/import-playlist` | ytmusicapi methods | YouTube Data API v3 methods |

### New Features

- **Automatic Token Refresh**: OAuth tokens refresh automatically
- **Better Error Messages**: Clear, actionable error responses
- **Official API Limits**: Respects YouTube API quotas
- **Future-Proof**: Uses official Google APIs

## Troubleshooting

### Common Issues

#### 1. "Credentials file not found"
**Solution**: Download OAuth 2.0 credentials from Google Cloud Console

#### 2. "Authentication failed"
**Solution**: Run `python setup_youtube_api.py` and follow the browser flow

#### 3. "API quota exceeded"
**Solution**: YouTube Data API has daily quotas. Wait or upgrade your Google Cloud project

#### 4. "No channel found"
**Solution**: Make sure you're logged into the correct Google account during OAuth

### Debugging

Check authentication status:
```bash
curl http://localhost:8000/youtube/auth-status
```

Test API functionality:
```bash
python setup_youtube_api.py
```

## Benefits Summary

✅ **Reliability**: Official API with Google support  
✅ **Security**: OAuth 2.0 standard authentication  
✅ **Maintainability**: No more header management  
✅ **Future-Proof**: Long-term API stability  
✅ **Error Handling**: Clear, actionable error messages  
✅ **Quota Management**: Respects official API limits  

## Migration Checklist

- [ ] Install updated requirements.txt
- [ ] Set up Google Cloud project
- [ ] Download OAuth credentials
- [ ] Run setup script
- [ ] Test authentication
- [ ] Test playlist creation
- [ ] Update frontend text (optional)
- [ ] Remove old auth files (optional)

## Support

If you encounter issues:

1. Check the setup instructions: `GET /setup-instructions`
2. Run the setup script: `python setup_youtube_api.py`
3. Check authentication status: `GET /youtube/auth-status`
4. Review Google Cloud Console quotas and billing

The new implementation provides a much more robust and maintainable solution for YouTube playlist management. 