import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { Music, Play, CheckCircle, XCircle, Loader2, ExternalLink, Sparkles, Heart, Star, Zap } from 'lucide-react';

const BACKEND_URL = 'http://127.0.0.1:8000';

function App() {
  // --- State ---
  const [spotifyToken, setSpotifyToken] = useState(null);
  const [isSpotifyAuthenticated, setIsSpotifyAuthenticated] = useState(false);
  const [isYtMusicAuthenticated, setIsYtMusicAuthenticated] = useState(false);
  const [playlists, setPlaylists] = useState([]);
  const [selectedPlaylist, setSelectedPlaylist] = useState(null);
  const [tracks, setTracks] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [importResult, setImportResult] = useState(null);
  const [error, setError] = useState(null);
  const [showYtMusicInput, setShowYtMusicInput] = useState(false);
  const [ytMusicInput, setYtMusicInput] = useState('');
  const [callbackProcessed, setCallbackProcessed] = useState(false);

  // --- Spotify OAuth Flow ---
  const handleSpotifyLogin = async () => {
    try {
      const response = await axios.get(`${BACKEND_URL}/spotify/auth-url`);
      window.location.href = response.data.auth_url;
    } catch (error) {
      setError('Failed to start Spotify authentication');
    }
  };

  // Handle Spotify OAuth callback
  useEffect(() => {
    // Check for code in URL parameters (both search and hash)
    const urlParams = new URLSearchParams(window.location.search);
    const hashParams = new URLSearchParams(window.location.hash.substring(1));
    const code = urlParams.get('code') || hashParams.get('code');
    
    if (code && !spotifyToken && !isSpotifyAuthenticated && !callbackProcessed) {
      // Add a flag to prevent duplicate requests
      const processCallback = async () => {
        setCallbackProcessed(true); // Mark as processed immediately
        
        // Clear the code from URL immediately to prevent duplicate processing
        window.history.replaceState({}, document.title, '/');
        
        try {
          const res = await axios.post(`${BACKEND_URL}/spotify/callback`, { code });
          setSpotifyToken(res.data.access_token);
          setIsSpotifyAuthenticated(true);
        } catch (error) {
          setError('Spotify authentication failed');
          setCallbackProcessed(false); // Reset flag on error
        }
      };
      
      processCallback();
    }
  }, [spotifyToken, isSpotifyAuthenticated, callbackProcessed]); // Add missing dependencies

  // --- Fetch Playlists/Tracks ---
  const fetchPlaylists = useCallback(async (token) => {
    try {
      console.log('Fetching playlists...');
      const response = await axios.post(`${BACKEND_URL}/spotify/playlists`, { access_token: token });
      console.log('Playlists response:', response.data);
      setPlaylists(response.data.playlists);
    } catch (error) {
      console.error('Playlist fetch error:', error);
      const errorMessage = error.response?.data?.detail || 'Failed to fetch playlists';
      setError(errorMessage);
    }
  }, []); // No dependencies - token passed as parameter

  const fetchPlaylistTracks = useCallback(async (playlistId) => {
    try {
      const response = await axios.post(`${BACKEND_URL}/spotify/playlist/${playlistId}/tracks`, {
        access_token: spotifyToken
      });
      setTracks(response.data.tracks);
    } catch (error) {
      setError('Failed to fetch playlist tracks');
    }
  }, [spotifyToken]);

  // --- YouTube Music Auth Flow ---
  const checkYouTubeAuthStatus = useCallback(async () => {
    try {
      const response = await axios.get(`${BACKEND_URL}/youtube/auth-status`);
      const status = response.data;
      
      setIsYtMusicAuthenticated(status.authenticated);
      
      if (status.authenticated) {
        setError(null);
        return true;
      } else {
        return false;
      }
    } catch (error) {
      console.error('Error checking YouTube auth status:', error);
      return false;
    }
  }, []);

  const handleYtMusicAuth = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      // Try authentication
      const response = await axios.post(`${BACKEND_URL}/youtube/auto-authenticate`);
      const result = response.data;
      
      if (result.success) {
        // Authentication successful
        setIsYtMusicAuthenticated(true);
        setError(null);
      } else if (result.requires_manual_setup) {
        // Manual setup required
        setError(`Setup Required: ${result.message}`);
        setShowYtMusicInput(true);
      } else {
        setError(`Authentication failed: ${result.message}`);
      }
      
    } catch (error) {
      console.error('YouTube authentication error:', error);
      const errorMessage = error.response?.data?.detail || error.response?.data?.message || 'Failed to authenticate with YouTube';
      setError(errorMessage);
      setShowYtMusicInput(true);
    } finally {
      setIsLoading(false);
    }
  };

  // Check YouTube auth status on component mount
  useEffect(() => {
    checkYouTubeAuthStatus();
  }, [checkYouTubeAuthStatus]);

  const handleYtMusicSubmit = async () => {
    setIsLoading(true);
    try {
      // Parse the JSON to validate it, then send as string
      JSON.parse(ytMusicInput); // Just validate the JSON format
      await axios.post(`${BACKEND_URL}/youtube/authenticate`, { auth_headers: ytMusicInput });
      setIsYtMusicAuthenticated(true);
      setShowYtMusicInput(false);
      setYtMusicInput('');
      setError(null);
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Invalid YouTube Music headers or authentication failed';
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const handleReAuthenticateYtMusic = async () => {
    setIsYtMusicAuthenticated(false);
    setError(null);
    
    // Try auto-authentication first
    await handleYtMusicAuth();
  };

  // --- Import Playlist ---
  const importToYouTubeMusic = async () => {
    if (!selectedPlaylist || tracks.length === 0) return;
    
    // Check authentication status before importing
    const isAuthenticated = await checkYouTubeAuthStatus();
    if (!isAuthenticated) {
      setError('YouTube Music authentication expired. Please re-authenticate.');
      setIsYtMusicAuthenticated(false);
      return;
    }
    
    setIsLoading(true);
    setError(null);
    setImportResult(null);
    
    try {
      const response = await axios.post(`${BACKEND_URL}/import-playlist`, {
        playlistName: selectedPlaylist.name,
        tracks: tracks
      });
      setImportResult(response.data);
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Failed to import playlist';
      setError(errorMessage);
      
      // If it's an authentication error, trigger re-authentication
      if (errorMessage.includes('authentication failed') || 
          errorMessage.includes('Unauthorized') || 
          errorMessage.includes('not initialized')) {
        setIsYtMusicAuthenticated(false);
        setError(`${errorMessage} - Click "Connect YouTube Music" to fix this.`);
      }
    } finally {
      setIsLoading(false);
    }
  };

  // --- UI Logic ---
  const handlePlaylistSelect = (playlist) => {
    setSelectedPlaylist(playlist);
    fetchPlaylistTracks(playlist.id);
    setImportResult(null);
    setError(null);
  };

  const logout = () => {
    setSpotifyToken(null);
    setIsSpotifyAuthenticated(false);
    setIsYtMusicAuthenticated(false);
    setPlaylists([]);
    setSelectedPlaylist(null);
    setTracks([]);
    setImportResult(null);
    setError(null);
    setCallbackProcessed(false);
  };

  // --- Fetch playlists when both services are authenticated ---
  useEffect(() => {
    console.log('Auth status check:', { 
      spotifyToken: !!spotifyToken, 
      isSpotifyAuthenticated, 
      isYtMusicAuthenticated,
      playlistsCount: playlists.length 
    });
    
    // Only fetch if both authenticated AND playlists is empty AND we have a token
    if (spotifyToken && isSpotifyAuthenticated && isYtMusicAuthenticated && playlists.length === 0) {
      console.log('Both services authenticated, fetching playlists...');
      fetchPlaylists(spotifyToken);
    }
  }, [spotifyToken, isSpotifyAuthenticated, isYtMusicAuthenticated, playlists.length, fetchPlaylists]);

  // --- Render ---
  if (!isSpotifyAuthenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 flex items-center justify-center relative overflow-hidden">
        {/* Animated background elements */}
        <div className="absolute inset-0">
          <div className="absolute top-20 left-20 w-72 h-72 bg-pink-500 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-pulse"></div>
          <div className="absolute top-40 right-20 w-72 h-72 bg-yellow-500 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-pulse animation-delay-2000"></div>
          <div className="absolute -bottom-8 left-20 w-72 h-72 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-pulse animation-delay-4000"></div>
        </div>
        
        <div className="relative backdrop-blur-sm bg-white/10 rounded-3xl shadow-2xl border border-white/20 p-10 max-w-lg w-full mx-6 transform hover:scale-105 transition-all duration-300">
          <div className="text-center">
            <div className="relative mb-8">
              <div className="absolute inset-0 bg-gradient-to-r from-green-400 to-blue-500 rounded-full blur-lg opacity-75 animate-pulse"></div>
              <div className="relative bg-gradient-to-r from-green-400 to-blue-500 w-20 h-20 rounded-full flex items-center justify-center mx-auto">
                <Music className="w-10 h-10 text-white" />
              </div>
            </div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent mb-3">
              Playlist Importer
            </h1>
            <p className="text-gray-300 mb-8 text-lg leading-relaxed">
              Transform your music journey<br />
              <span className="text-sm opacity-80">Import your Spotify playlists to YouTube Music with style</span>
            </p>
            <button
              onClick={handleSpotifyLogin}
              className="group relative overflow-hidden bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white font-semibold py-4 px-8 rounded-2xl transition-all duration-300 flex items-center justify-center mx-auto shadow-lg hover:shadow-2xl transform hover:scale-105"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/20 to-white/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000"></div>
              <Play className="w-6 h-6 mr-3" />
              Connect with Spotify
              <Sparkles className="w-5 h-5 ml-2 opacity-80" />
            </button>
            {error && (
              <div className="mt-6 p-4 bg-red-500/20 border border-red-400/30 rounded-xl text-red-300 backdrop-blur-sm">
                {error}
              </div>
            )}
          </div>
        </div>
      </div>
    );
  }

  if (!isYtMusicAuthenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-red-900 via-pink-900 to-rose-900 flex items-center justify-center relative overflow-hidden">
        {/* Animated background elements */}
        <div className="absolute inset-0">
          <div className="absolute top-20 left-20 w-96 h-96 bg-red-500 rounded-full mix-blend-multiply filter blur-xl opacity-60 animate-bounce"></div>
          <div className="absolute top-40 right-20 w-80 h-80 bg-pink-500 rounded-full mix-blend-multiply filter blur-xl opacity-60 animate-bounce animation-delay-1000"></div>
          <div className="absolute -bottom-8 left-1/2 w-96 h-96 bg-orange-500 rounded-full mix-blend-multiply filter blur-xl opacity-60 animate-bounce animation-delay-2000"></div>
        </div>
        
        <div className="relative backdrop-blur-sm bg-white/10 rounded-3xl shadow-2xl border border-white/20 p-10 max-w-lg w-full mx-6 transform hover:scale-105 transition-all duration-300">
          <div className="text-center">
            <div className="relative mb-8">
              <div className="absolute inset-0 bg-gradient-to-r from-red-500 to-pink-500 rounded-full blur-lg opacity-75 animate-pulse"></div>
              <div className="relative bg-gradient-to-r from-red-500 to-pink-500 w-20 h-20 rounded-full flex items-center justify-center mx-auto">
                <Music className="w-10 h-10 text-white" />
              </div>
            </div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent mb-3">
              Connect YouTube
            </h1>
            <p className="text-gray-300 mb-8 text-lg leading-relaxed">
              Ready to rock YouTube Music?<br />
              <span className="text-sm opacity-80">
                {!showYtMusicInput ? 
                  'One-click OAuth 2.0 authentication. If first time, manual setup may be needed.' : 
                  'Follow the setup instructions below'}
              </span>
            </p>
            <button
              onClick={handleYtMusicAuth}
              disabled={isLoading}
              className="group relative overflow-hidden bg-gradient-to-r from-red-500 to-pink-600 hover:from-red-600 hover:to-pink-700 disabled:from-gray-500 disabled:to-gray-600 text-white font-semibold py-4 px-8 rounded-2xl transition-all duration-300 flex items-center justify-center mx-auto shadow-lg hover:shadow-2xl transform hover:scale-105 disabled:hover:scale-100 mb-6"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/20 to-white/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000"></div>
              {isLoading ? (
                <>
                  <Loader2 className="w-6 h-6 mr-3 animate-spin" />
                  <span>Connecting...</span>
                  <Zap className="w-5 h-5 ml-2 opacity-80" />
                </>
              ) : (
                <>
                  <Play className="w-6 h-6 mr-3" />
                  <span>Connect with YouTube</span>
                  <Heart className="w-5 h-5 ml-2 opacity-80" />
                </>
              )}
            </button>
            {showYtMusicInput && (
              <div className="mt-6 space-y-4">
                <div className="backdrop-blur-sm bg-blue-500/20 border border-blue-400/30 rounded-2xl p-6">
                  <div className="flex items-center mb-4">
                    <Star className="w-5 h-5 text-yellow-400 mr-2" />
                    <p className="font-semibold text-white">Manual Setup Required</p>
                  </div>
                  <ol className="list-decimal list-inside space-y-2 text-gray-300 text-sm">
                    <li>Open terminal in the backend directory</li>
                    <li>Run: <code className="bg-black/30 px-2 py-1 rounded text-green-400 font-mono">python setup_youtube_api.py</code></li>
                    <li>Follow the OAuth 2.0 authentication process</li>
                    <li>Or paste credentials manually below:</li>
                  </ol>
                </div>
                <textarea
                  className="w-full backdrop-blur-sm bg-white/10 border border-white/20 rounded-2xl p-4 text-white placeholder-gray-400 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-transparent transition-all duration-300"
                  rows={8}
                  placeholder="Paste OAuth credentials JSON here (if needed)"
                  value={ytMusicInput}
                  onChange={e => setYtMusicInput(e.target.value)}
                />
                <button
                  onClick={handleYtMusicSubmit}
                  disabled={isLoading}
                  className="group relative overflow-hidden bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 disabled:from-gray-500 disabled:to-gray-600 text-white font-semibold py-3 px-6 rounded-xl transition-all duration-300 flex items-center justify-center shadow-lg hover:shadow-xl transform hover:scale-105 disabled:hover:scale-100"
                >
                  <div className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/20 to-white/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000"></div>
                  {isLoading ? (
                    <>
                      <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                      <span>Submitting...</span>
                    </>
                  ) : (
                    <>
                      <span>Submit Headers</span>
                      <Zap className="w-4 h-4 ml-2" />
                    </>
                  )}
                </button>
              </div>
            )}
            {error && (
              <div className="mt-6 p-4 backdrop-blur-sm bg-red-500/20 border border-red-400/30 rounded-xl text-red-300">
                <div className="flex items-center">
                  <XCircle className="w-5 h-5 mr-2 flex-shrink-0" />
                  <span className="text-sm">{error}</span>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 relative overflow-hidden">
      {/* Animated background */}
      <div className="absolute inset-0">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse"></div>
        <div className="absolute top-1/3 right-1/4 w-96 h-96 bg-pink-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse animation-delay-2000"></div>
        <div className="absolute bottom-0 left-1/3 w-96 h-96 bg-blue-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse animation-delay-4000"></div>
      </div>
      
      {/* Header */}
      <div className="relative backdrop-blur-sm bg-white/5 border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-green-400 to-blue-500 rounded-full blur opacity-75 animate-pulse"></div>
                <div className="relative bg-gradient-to-r from-green-400 to-blue-500 w-12 h-12 rounded-full flex items-center justify-center">
                  <Music className="w-6 h-6 text-white" />
                </div>
              </div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent ml-4">
                Playlist Importer
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <button
                onClick={handleReAuthenticateYtMusic}
                className="group relative overflow-hidden bg-gradient-to-r from-blue-500/20 to-purple-500/20 hover:from-blue-500/30 hover:to-purple-500/30 backdrop-blur-sm border border-white/20 text-white font-medium py-2 px-4 rounded-xl transition-all duration-300 hover:scale-105"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/10 to-white/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000"></div>
                <span className="relative">Re-authenticate YouTube</span>
              </button>
              <button
                onClick={logout}
                className="group relative overflow-hidden bg-gradient-to-r from-red-500/20 to-pink-500/20 hover:from-red-500/30 hover:to-pink-500/30 backdrop-blur-sm border border-white/20 text-white font-medium py-2 px-4 rounded-xl transition-all duration-300 hover:scale-105"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/10 to-white/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000"></div>
                <span className="relative">Logout</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Status indicators */}
        <div className="mb-8 flex justify-center space-x-6">
          <div className="flex items-center space-x-2 backdrop-blur-sm bg-green-500/20 border border-green-400/30 rounded-full px-4 py-2">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
            <span className="text-green-300 text-sm font-medium">Spotify Connected</span>
          </div>
          <div className="flex items-center space-x-2 backdrop-blur-sm bg-red-500/20 border border-red-400/30 rounded-full px-4 py-2">
            <div className="w-2 h-2 bg-red-400 rounded-full animate-pulse"></div>
            <span className="text-red-300 text-sm font-medium">YouTube Connected</span>
          </div>
          <div className="flex items-center space-x-2 backdrop-blur-sm bg-blue-500/20 border border-blue-400/30 rounded-full px-4 py-2">
            <span className="text-blue-300 text-sm font-medium">{playlists.length} Playlists</span>
          </div>
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Playlists Section */}
          <div className="group backdrop-blur-sm bg-white/10 border border-white/20 rounded-3xl shadow-2xl p-8 hover:bg-white/15 transition-all duration-500 hover:scale-[1.02]">
            <div className="flex items-center mb-6">
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-green-400 to-blue-500 rounded-full blur opacity-75 animate-pulse"></div>
                <div className="relative bg-gradient-to-r from-green-400 to-blue-500 w-10 h-10 rounded-full flex items-center justify-center">
                  <Music className="w-5 h-5 text-white" />
                </div>
              </div>
              <h2 className="text-2xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent ml-4">
                Your Playlists ({playlists.length})
              </h2>
            </div>
            <div className="space-y-3 max-h-96 overflow-y-auto custom-scrollbar">
              {playlists.map((playlist) => (
                <button
                  key={playlist.id}
                  onClick={() => handlePlaylistSelect(playlist)}
                  className={`group/item w-full text-left p-4 rounded-2xl border transition-all duration-300 transform hover:scale-[1.02] hover:shadow-lg ${
                    selectedPlaylist?.id === playlist.id
                      ? 'border-green-400/50 bg-gradient-to-r from-green-500/20 to-blue-500/20 shadow-lg shadow-green-500/20'
                      : 'border-white/20 hover:border-white/30 hover:bg-white/10 backdrop-blur-sm'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="font-semibold text-white group-hover/item:text-green-300 transition-colors duration-300">
                        {playlist.name}
                      </div>
                      <div className="text-sm text-gray-400 group-hover/item:text-gray-300 transition-colors duration-300">
                        {playlist.tracks?.total || playlist.tracks?.length || 0} tracks
                      </div>
                    </div>
                    {selectedPlaylist?.id === playlist.id && (
                      <div className="flex items-center space-x-1">
                        <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                        <Sparkles className="w-4 h-4 text-green-400" />
                      </div>
                    )}
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Tracks Section */}
          <div className="group backdrop-blur-sm bg-white/10 border border-white/20 rounded-3xl shadow-2xl p-8 hover:bg-white/15 transition-all duration-500 hover:scale-[1.02]">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center">
                <div className="relative">
                  <div className="absolute inset-0 bg-gradient-to-r from-purple-400 to-pink-500 rounded-full blur opacity-75 animate-pulse"></div>
                  <div className="relative bg-gradient-to-r from-purple-400 to-pink-500 w-10 h-10 rounded-full flex items-center justify-center">
                    <Play className="w-5 h-5 text-white" />
                  </div>
                </div>
                <h2 className="text-2xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent ml-4">
                  {selectedPlaylist ? `${selectedPlaylist.name}` : 'Select a Playlist'}
                </h2>
              </div>
              {selectedPlaylist && (
                <div className="flex items-center space-x-2 backdrop-blur-sm bg-purple-500/20 border border-purple-400/30 rounded-full px-3 py-1">
                  <Star className="w-4 h-4 text-purple-300" />
                  <span className="text-purple-300 text-sm font-medium">{tracks.length} tracks</span>
                </div>
              )}
            </div>
            {selectedPlaylist && tracks.length > 0 && (
              <div className="mb-6">
                <div className="flex justify-between items-center mb-6">
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                    <span className="text-gray-300 font-medium">
                      {tracks.length} tracks ready to import
                    </span>
                  </div>
                  <button
                    onClick={importToYouTubeMusic}
                    disabled={isLoading || !isYtMusicAuthenticated}
                    className="group relative overflow-hidden bg-gradient-to-r from-purple-500 to-pink-600 hover:from-purple-600 hover:to-pink-700 disabled:from-gray-500 disabled:to-gray-600 text-white font-semibold py-3 px-6 rounded-2xl transition-all duration-300 flex items-center shadow-lg hover:shadow-2xl transform hover:scale-105 disabled:hover:scale-100"
                  >
                    <div className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/20 to-white/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000"></div>
                    <div className="relative flex items-center">
                      {isLoading ? (
                        <>
                          <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                          <span>Importing...</span>
                          <Sparkles className="w-4 h-4 ml-2 opacity-80" />
                        </>
                      ) : (
                        <>
                          <Play className="w-5 h-5 mr-2" />
                          <span>Import to YouTube</span>
                          <Heart className="w-4 h-4 ml-2 opacity-80" />
                        </>
                      )}
                    </div>
                  </button>
                </div>
                <div className="max-h-64 overflow-y-auto space-y-3 custom-scrollbar">
                  {tracks.map((track, index) => (
                    <div key={index} className="group/track p-4 backdrop-blur-sm bg-white/5 hover:bg-white/10 border border-white/20 rounded-2xl transition-all duration-300 transform hover:scale-[1.02] hover:shadow-lg">
                      <div className="flex items-center justify-between">
                        <div>
                          <div className="font-semibold text-white group-hover/track:text-purple-300 transition-colors duration-300">
                            {track.name}
                          </div>
                          <div className="text-sm text-gray-400 group-hover/track:text-gray-300 transition-colors duration-300">
                            {track.artist}
                          </div>
                        </div>
                        <div className="opacity-0 group-hover/track:opacity-100 transition-opacity duration-300">
                          <Music className="w-4 h-4 text-purple-400" />
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
            {error && (
              <div className="backdrop-blur-sm bg-red-500/20 border border-red-400/30 rounded-2xl p-6 mt-6">
                <div className="flex items-center">
                  <div className="relative">
                    <div className="absolute inset-0 bg-red-500 rounded-full blur opacity-75 animate-pulse"></div>
                    <div className="relative bg-red-500 w-8 h-8 rounded-full flex items-center justify-center">
                      <XCircle className="w-4 h-4 text-white" />
                    </div>
                  </div>
                  <span className="text-red-300 ml-4 font-medium">{error}</span>
                </div>
              </div>
            )}
            {importResult && (
              <div className="backdrop-blur-sm bg-green-500/20 border border-green-400/30 rounded-2xl p-6 mt-6">
                <div className="flex items-center mb-4">
                  <div className="relative">
                    <div className="absolute inset-0 bg-green-500 rounded-full blur opacity-75 animate-pulse"></div>
                    <div className="relative bg-green-500 w-8 h-8 rounded-full flex items-center justify-center">
                      <CheckCircle className="w-4 h-4 text-white" />
                    </div>
                  </div>
                  <span className="text-green-300 ml-4 font-bold text-lg">Import Complete!</span>
                  <Sparkles className="w-5 h-5 text-green-400 ml-2 animate-pulse" />
                </div>
                {importResult.playlistUrl && (
                  <div className="mb-4">
                    <a
                      href={importResult.playlistUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="group inline-flex items-center bg-gradient-to-r from-blue-500/20 to-purple-500/20 hover:from-blue-500/30 hover:to-purple-500/30 backdrop-blur-sm border border-white/20 text-blue-300 hover:text-white font-medium py-2 px-4 rounded-xl transition-all duration-300 hover:scale-105"
                    >
                      <ExternalLink className="w-4 h-4 mr-2" />
                      <span>View Playlist on YouTube</span>
                      <Heart className="w-4 h-4 ml-2 opacity-80" />
                    </a>
                  </div>
                )}
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div className="backdrop-blur-sm bg-white/10 rounded-xl p-3 border border-white/20">
                    <div className="flex items-center justify-between">
                      <span className="text-gray-300">Added:</span>
                      <div className="flex items-center space-x-1">
                        <span className="text-green-300 font-bold">{importResult.addedTracks?.length || 0}</span>
                        <CheckCircle className="w-4 h-4 text-green-400" />
                      </div>
                    </div>
                  </div>
                  {importResult.failedTracks && importResult.failedTracks.length > 0 && (
                    <div className="backdrop-blur-sm bg-white/10 rounded-xl p-3 border border-white/20">
                      <div className="flex items-center justify-between">
                        <span className="text-gray-300">Failed:</span>
                        <div className="flex items-center space-x-1">
                          <span className="text-red-300 font-bold">{importResult.failedTracks.length}</span>
                          <XCircle className="w-4 h-4 text-red-400" />
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App; 