import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Music, Play, CheckCircle, XCircle, Loader2, ExternalLink } from 'lucide-react';

const BACKEND_URL = 'http://localhost:8000';

function App() {
  // --- State ---
  const [spotifyToken, setSpotifyToken] = useState(null);
  const [ytMusicHeaders, setYtMusicHeaders] = useState(null);
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
    
    if (code && !spotifyToken) {
      axios.post(`${BACKEND_URL}/spotify/callback`, { code })
        .then(res => {
          setSpotifyToken(res.data.access_token);
          setIsSpotifyAuthenticated(true);
          // Clean up the URL
          window.history.replaceState({}, document.title, '/');
        })
        .catch(() => setError('Spotify authentication failed'));
    }
  }, [spotifyToken]);

  // --- Fetch Playlists/Tracks ---
  const fetchPlaylists = async () => {
    try {
      const response = await axios.post(`${BACKEND_URL}/spotify/playlists`, { access_token: spotifyToken });
      setPlaylists(response.data.playlists);
    } catch (error) {
      setError('Failed to fetch playlists');
    }
  };

  const fetchPlaylistTracks = async (playlistId) => {
    try {
      const response = await axios.post(`${BACKEND_URL}/spotify/playlist/${playlistId}/tracks`, {
        access_token: spotifyToken
      });
      setTracks(response.data.tracks);
    } catch (error) {
      setError('Failed to fetch playlist tracks');
    }
  };

  // --- YouTube Music Auth Flow ---
  const handleYtMusicAuth = async () => {
    setShowYtMusicInput(true);
  };

  const handleYtMusicSubmit = async () => {
    try {
      // Parse the JSON to validate it, then send as string
      const headers = JSON.parse(ytMusicInput);
      await axios.post(`${BACKEND_URL}/youtube/authenticate`, { auth_headers: ytMusicInput });
      setYtMusicHeaders(headers);
      setIsYtMusicAuthenticated(true);
      setShowYtMusicInput(false);
      setError(null);
    } catch (error) {
      setError('Invalid YouTube Music headers or authentication failed');
    }
  };

  // --- Import Playlist ---
  const importToYouTubeMusic = async () => {
    if (!selectedPlaylist || tracks.length === 0 || !ytMusicHeaders) return;
    setIsLoading(true);
    setError(null);
    setImportResult(null);
    try {
      const response = await axios.post(`${BACKEND_URL}/import-playlist`, {
        playlistName: selectedPlaylist.name,
        tracks: tracks,
        youtube_auth_headers: JSON.stringify(ytMusicHeaders)
      });
      setImportResult(response.data);
    } catch (error) {
      setError(error.response?.data?.detail || 'Failed to import playlist');
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
    setYtMusicHeaders(null);
    setIsYtMusicAuthenticated(false);
    setPlaylists([]);
    setSelectedPlaylist(null);
    setTracks([]);
    setImportResult(null);
    setError(null);
  };

  // --- Fetch playlists when authenticated ---
  useEffect(() => {
    if (spotifyToken) {
      setIsSpotifyAuthenticated(true);
      fetchPlaylists();
    }
  }, [spotifyToken]); // eslint-disable-line react-hooks/exhaustive-deps

  // --- Render ---
  if (!isSpotifyAuthenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-400 to-blue-500 flex items-center justify-center">
        <div className="bg-white rounded-lg shadow-xl p-8 max-w-md w-full mx-4">
          <div className="text-center">
            <Music className="w-16 h-16 text-green-500 mx-auto mb-4" />
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Playlist Importer</h1>
            <p className="text-gray-600 mb-6">Import your Spotify playlists to YouTube Music</p>
            <button
              onClick={handleSpotifyLogin}
              className="bg-green-500 hover:bg-green-600 text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-200 flex items-center justify-center mx-auto"
            >
              <Play className="w-5 h-5 mr-2" />
              Connect with Spotify
            </button>
            {error && <div className="text-red-600 mt-4">{error}</div>}
          </div>
        </div>
      </div>
    );
  }

  if (!isYtMusicAuthenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-yellow-400 to-red-500 flex items-center justify-center">
        <div className="bg-white rounded-lg shadow-xl p-8 max-w-md w-full mx-4">
          <div className="text-center">
            <Music className="w-16 h-16 text-red-500 mx-auto mb-4" />
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Connect YouTube Music</h1>
            <p className="text-gray-600 mb-6">Paste your YouTube Music auth headers below.<br/>To get them, run:<br/><code>python -c \"import ytmusicapi; ytmusicapi.setup(filepath='temp_auth.json')\"</code> and open the file.</p>
            <button
              onClick={handleYtMusicAuth}
              className="bg-red-500 hover:bg-red-600 text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-200 flex items-center justify-center mx-auto mb-4"
            >
              <Play className="w-5 h-5 mr-2" />
              Connect with YouTube Music
            </button>
            {showYtMusicInput && (
              <div className="mt-4">
                <textarea
                  className="w-full border rounded p-2 text-sm"
                  rows={8}
                  placeholder="Paste the contents of temp_auth.json here"
                  value={ytMusicInput}
                  onChange={e => setYtMusicInput(e.target.value)}
                />
                <button
                  onClick={handleYtMusicSubmit}
                  className="mt-2 bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded"
                >
                  Submit
                </button>
              </div>
            )}
            {error && <div className="text-red-600 mt-4">{error}</div>}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <Music className="w-8 h-8 text-green-500 mr-3" />
              <h1 className="text-2xl font-bold text-gray-900">Playlist Importer</h1>
            </div>
            <button
              onClick={logout}
              className="text-gray-500 hover:text-gray-700 font-medium"
            >
              Logout
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Playlists Section */}
          <div className="bg-white rounded-lg shadow-sm border p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Your Playlists</h2>
            <div className="space-y-2 max-h-96 overflow-y-auto">
              {playlists.map((playlist) => (
                <button
                  key={playlist.id}
                  onClick={() => handlePlaylistSelect(playlist)}
                  className={`w-full text-left p-3 rounded-lg border transition-colors duration-200 ${
                    selectedPlaylist?.id === playlist.id
                      ? 'border-green-500 bg-green-50'
                      : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                  }`}
                >
                  <div className="font-medium text-gray-900">{playlist.name}</div>
                  <div className="text-sm text-gray-500">
                    {playlist.tracks?.total || playlist.tracks?.length || 0} tracks
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Tracks Section */}
          <div className="bg-white rounded-lg shadow-sm border p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              {selectedPlaylist ? `${selectedPlaylist.name} - Tracks` : 'Select a Playlist'}
            </h2>
            {selectedPlaylist && tracks.length > 0 && (
              <div className="mb-4">
                <div className="flex justify-between items-center mb-4">
                  <span className="text-sm text-gray-600">
                    {tracks.length} tracks ready to import
                  </span>
                  <button
                    onClick={importToYouTubeMusic}
                    disabled={isLoading}
                    className="bg-blue-500 hover:bg-blue-600 disabled:bg-gray-400 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-200 flex items-center"
                  >
                    {isLoading ? (
                      <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    ) : (
                      <Play className="w-4 h-4 mr-2" />
                    )}
                    {isLoading ? 'Importing...' : 'Import to YouTube Music'}
                  </button>
                </div>
                <div className="max-h-64 overflow-y-auto space-y-2">
                  {tracks.map((track, index) => (
                    <div key={index} className="p-2 bg-gray-50 rounded border">
                      <div className="font-medium text-sm text-gray-900">{track.name}</div>
                      <div className="text-xs text-gray-600">{track.artist}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <div className="flex items-center">
                  <XCircle className="w-5 h-5 text-red-500 mr-2" />
                  <span className="text-red-700">{error}</span>
                </div>
              </div>
            )}
            {importResult && (
              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <div className="flex items-center mb-3">
                  <CheckCircle className="w-5 h-5 text-green-500 mr-2" />
                  <span className="text-green-700 font-medium">Import Complete!</span>
                </div>
                {importResult.playlistUrl && (
                  <div className="mb-3">
                    <a
                      href={importResult.playlistUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:text-blue-800 flex items-center text-sm"
                    >
                      <ExternalLink className="w-4 h-4 mr-1" />
                      View Playlist on YouTube Music
                    </a>
                  </div>
                )}
                <div className="text-sm text-gray-700">
                  <div className="mb-2">
                    <span className="font-medium">Added:</span> {importResult.addedTracks?.length || 0} tracks
                  </div>
                  {importResult.failedTracks && importResult.failedTracks.length > 0 && (
                    <div>
                      <span className="font-medium">Failed:</span> {importResult.failedTracks.length} tracks
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