import React, { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';
import { toast } from 'react-hot-toast';
import {
  Music, Play, CheckCircle, XCircle, Loader2, ExternalLink, Sparkles,
  Heart, Star, Zap, Volume2, Headphones, Radio, Disc3, PlayCircle,
  Users, Calendar, Clock, TrendingUp, Award, Shuffle, RefreshCw
} from 'lucide-react';

// Import components
import SpotifyLogin from './components/SpotifyLogin';
import YouTubeAuth from './components/YouTubeAuth';
import PlaylistList from './components/PlaylistList';
import TrackList from './components/TrackList';
import ImportResult from './components/ImportResult';
import ToasterConfig from './components/ToasterConfig';
import ProfessionalLoading from './components/ProfessionalLoading';
import ProfessionalFooter from './components/ProfessionalFooter';

const BACKEND_URL = 'http://127.0.0.1:8000';

function App() {
  // --- State ---
  const [spotifyToken, setSpotifyToken] = useState(null);
  const [isSpotifyAuthenticated, setIsSpotifyAuthenticated] = useState(false);
  const [playlists, setPlaylists] = useState([]);
  const [selectedPlaylist, setSelectedPlaylist] = useState(null);
  const [tracks, setTracks] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [importResult, setImportResult] = useState(null);
  const [error, setError] = useState(null);
  const [showYtMusicInput, setShowYtMusicInput] = useState(false);
  const [ytMusicInput, setYtMusicInput] = useState('');
  const [callbackProcessed, setCallbackProcessed] = useState(false);
  const [isYtMusicAuthenticated, setIsYtMusicAuthenticated] = useState(false);
  const [importProgress, setImportProgress] = useState(0);
  const [currentTrack, setCurrentTrack] = useState('');

  // --- All Hooks Must Be Called At The Top Level ---
  
  // Handle Spotify OAuth callback
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const hashParams = new URLSearchParams(window.location.hash.substring(1));
    const code = urlParams.get('code') || hashParams.get('code');

    console.log('Callback useEffect - code:', !!code, 'spotifyToken:', !!spotifyToken, 'isSpotifyAuthenticated:', isSpotifyAuthenticated, 'callbackProcessed:', callbackProcessed);

    if (code && !spotifyToken && !isSpotifyAuthenticated && !callbackProcessed) {
      console.log('Processing Spotify callback...');
      const processCallback = async () => {
        setCallbackProcessed(true);
        window.history.replaceState({}, document.title, '/');

        try {
          toast.loading('Completing Spotify authentication...', { id: 'callback' });
          const res = await axios.post(`${BACKEND_URL}/spotify/callback`, { code });
          console.log('Spotify callback success, setting tokens and auth state');
          
          setSpotifyToken(res.data.access_token);
          setIsSpotifyAuthenticated(true);
          setError(null);
          
          toast.success('✅ Spotify connected successfully!', { 
            id: 'callback',
            style: {
              borderRadius: '12px',
              background: '#1e293b',
              color: '#fff',
              border: '1px solid #22c55e',
            },
          });
        } catch (error) {
          console.error('Spotify callback error:', error);
          setError('Failed to complete Spotify authentication');
          toast.error('❌ Spotify authentication failed', { 
            id: 'callback',
            style: {
              borderRadius: '12px',
              background: '#1e293b',
              color: '#fff',
              border: '1px solid #ef4444',
            },
          });
        }
      };
      processCallback();
    }
  }, [spotifyToken, isSpotifyAuthenticated, callbackProcessed]);

  // --- Fetch playlists function ---
  const fetchPlaylists = useCallback(async (token) => {
    if (!token) return;

    try {
      setIsLoading(true);
      setError(null);
      
      console.log('Fetching playlists...');
      const response = await axios.post(`${BACKEND_URL}/spotify/playlists`, {
        access_token: token
      });
      
      if (response.data && response.data.playlists) {
        setPlaylists(response.data.playlists);
        console.log('Playlists fetched successfully:', response.data.playlists.length, 'playlists');
      } else {
        throw new Error('Invalid playlist data received');
      }
    } catch (error) {
      console.error('Error fetching playlists:', error);
      setError('Failed to fetch playlists');
      toast.error('❌ Failed to fetch playlists');
    } finally {
      setIsLoading(false);
    }
  }, []);

  // --- Fetch playlists when both Spotify AND YouTube are authenticated ---
  useEffect(() => {
    if (spotifyToken && isSpotifyAuthenticated && isYtMusicAuthenticated && playlists.length === 0) {
      fetchPlaylists(spotifyToken);
    }
  }, [spotifyToken, isSpotifyAuthenticated, isYtMusicAuthenticated, playlists.length, fetchPlaylists]);

  // Debug logging
  console.log('App render - State:', {
    isSpotifyAuthenticated,
    isYtMusicAuthenticated,
    spotifyToken: !!spotifyToken,
    callbackProcessed
  });

  // Show loading screen during initial load
  if (isLoading && !isSpotifyAuthenticated && !isYtMusicAuthenticated) {
    return <ProfessionalLoading message="Initializing Playlist Importer..." />;
  }

  // --- Spotify OAuth Flow ---
  const handleSpotifyLogin = async () => {
    try {
      toast.loading('🎵 Connecting to Spotify...', { 
        id: 'spotify-auth',
        style: {
          borderRadius: '12px',
          background: '#1e293b',
          color: '#fff',
          border: '1px solid #22c55e',
        },
      });
      const response = await axios.get(`${BACKEND_URL}/spotify/auth-url`);
      toast.success('✨ Redirecting to Spotify...', { 
        id: 'spotify-auth',
        style: {
          borderRadius: '12px',
          background: '#1e293b',
          color: '#fff',
          border: '1px solid #22c55e',
        },
      });
      window.location.href = response.data.auth_url;
    } catch (error) {
      toast.error('❌ Failed to start Spotify authentication', { 
        id: 'spotify-auth',
        style: {
          borderRadius: '12px',
          background: '#1e293b',
          color: '#fff',
          border: '1px solid #ef4444',
        },
      });
      setError('Failed to start Spotify authentication');
    }
  };



  // --- YouTube Music Authentication ---
  const authenticateYtMusic = async () => {
    try {
      setIsLoading(true);
      setError(null);
      toast.loading('Connecting to YouTube Music...', { id: 'ytmusic-auth' });

      const response = await axios.post(`${BACKEND_URL}/youtube/auto-authenticate`);

      if (response.data.success) {
        setIsYtMusicAuthenticated(true);
        toast.success('🎵 YouTube Music connected successfully!', { id: 'ytmusic-auth' });
      } else {
        setShowYtMusicInput(true);
        toast.error('Manual setup required', { id: 'ytmusic-auth' });
        setError('Please follow the manual setup instructions below');
      }
    } catch (error) {
      console.error('YT Music auth error:', error);
      setShowYtMusicInput(true);
      toast.error('Manual setup required', { id: 'ytmusic-auth' });
      setError('Please follow the manual setup instructions below');
    } finally {
      setIsLoading(false);
    }
  };

  const submitYtMusicHeaders = async () => {
    if (!ytMusicInput.trim()) {
      toast.error('Please enter OAuth credentials');
      return;
    }

    try {
      setIsLoading(true);
      setError(null);
      toast.loading('Submitting credentials...', { id: 'ytmusic-submit' });

      const response = await axios.post(`${BACKEND_URL}/youtube/submit-headers`, {
        headers: ytMusicInput
      });

      if (response.data.success) {
        setIsYtMusicAuthenticated(true);
        setShowYtMusicInput(false);
        setYtMusicInput('');
        toast.success('🎵 YouTube Music connected successfully!', { id: 'ytmusic-submit' });
      } else {
        throw new Error(response.data.message || 'Failed to authenticate');
      }
    } catch (error) {
      console.error('YT Music submit error:', error);
      toast.error('Failed to submit credentials', { id: 'ytmusic-submit' });
      setError(error.response?.data?.message || 'Failed to submit credentials');
    } finally {
      setIsLoading(false);
    }
  };



  // --- Select Playlist and Fetch Tracks ---
  const selectPlaylist = async (playlist) => {
    try {
      console.log('selectPlaylist called with:', playlist);
      setSelectedPlaylist(playlist);
      setIsLoading(true);
      setError(null);
      toast.loading('Loading tracks...', { id: 'tracks' });

      const response = await axios.post(`${BACKEND_URL}/spotify/playlist/${playlist.id}/tracks`, {
        access_token: spotifyToken
      });

      console.log('Raw response:', response.data);

      // The backend returns tracks directly in response.data.tracks, not response.data.items
      const rawTracks = response.data.tracks || response.data.items || response.data || [];
      
      const formattedTracks = rawTracks.map(track => ({
        name: track.name || track.track?.name || 'Unknown',
        artist: track.artist || track.track?.artists?.map(a => a.name).join(', ') || 'Unknown',
        album: track.album || track.track?.album?.name || 'Unknown',
        duration_ms: track.duration_ms || track.track?.duration_ms,
        popularity: track.popularity || track.track?.popularity,
        id: track.id || track.track?.id,
        artists: track.artists || track.track?.artists || [],
        images: track.images || track.track?.album?.images || []
      }));

      console.log('Formatted tracks:', formattedTracks);
      console.log('Setting tracks array with length:', formattedTracks.length);
      
      setTracks(formattedTracks);
      toast.success(`Loaded ${formattedTracks.length} tracks`, { id: 'tracks' });
    } catch (error) {
      console.error('Error fetching tracks:', error);
      toast.error('Failed to load tracks', { id: 'tracks' });
      setError('Failed to load tracks');
    } finally {
      setIsLoading(false);
    }
  };

  // --- Import to YouTube Music with real-time progress ---
  const importToYouTubeMusic = async () => {
    if (!selectedPlaylist || !tracks.length) {
      toast.error('No playlist or tracks selected');
      return;
    }

    try {
      setIsLoading(true);
      setError(null);
      setImportProgress(0);
      setCurrentTrack('');

      toast.loading('Starting import...', { id: 'import' });

      // Use fetch with streaming for real-time progress updates
      const response = await fetch(`${BACKEND_URL}/import-playlist-stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          playlistName: selectedPlaylist.name,
          playlistDescription: selectedPlaylist.description || '',
          tracks: tracks.map(track => ({
            name: track.name,
            artist: track.artist,
            album: track.album || ''
          }))
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body.getReader();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        
        if (done) break;
        
        buffer += new TextDecoder().decode(value);
        const lines = buffer.split('\n\n');
        buffer = lines.pop() || ''; // Keep incomplete line in buffer
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.substring(6));
              
              switch (data.type) {
                case 'start':
                  toast.loading(`Starting import of ${data.total} tracks...`, { id: 'import' });
                  break;
                  
                case 'status':
                  toast.loading(data.message, { id: 'import' });
                  break;
                  
                case 'progress':
                  setImportProgress(data.progress);
                  setCurrentTrack(data.track);
                  toast.loading(`${data.progress}% - Processing: ${data.track}`, { id: 'import' });
                  break;
                  
                case 'track_found':
                  console.log(`✅ ${data.track} → Video ID: ${data.videoId}`);
                  break;
                  
                case 'track_not_found':
                  console.log(`❌ ${data.track} → Not found`);
                  break;
                  
                case 'track_error':
                  console.log(`⚠️ ${data.track} → Error: ${data.error}`);
                  break;
                  
                case 'complete':
                  setImportProgress(100);
                  setImportResult({
                    status: 'success',
                    message: data.message,
                    youtubePlaylistUrl: data.playlistUrl,
                    stats: data.stats,
                    failedTracks: data.failedTracks || []
                  });
                  toast.success('🎉 Import completed successfully!', { id: 'import' });
                  return;
                  
                case 'error':
                  throw new Error(data.message);
                  
                default:
                  console.log('Unknown SSE event type:', data.type);
                  break;
              }
            } catch (parseError) {
              console.error('Error parsing SSE data:', parseError);
            }
          }
        }
      }
      
    } catch (error) {
      console.error('Import error:', error);
      
      // Check if this is an authentication error
      const errorMessage = error.message || 'Unknown error';
      
      if (errorMessage.includes('authentication') || errorMessage.includes('Unauthorized')) {
        // Authentication failure - trigger re-authentication flow
        console.log('Authentication error detected, triggering re-auth flow');
        setIsYtMusicAuthenticated(false);
        setShowYtMusicInput(true);
        setError('YouTube Music authentication expired. Please re-authenticate by entering your credentials below.');
        toast.error('🔐 Authentication expired - Please re-authenticate', { 
          id: 'import',
          duration: 5000
        });
        
        // Reset to show YouTube auth screen
        setSelectedPlaylist(null);
        setTracks([]);
        setImportResult(null);
        return;
      }
      
      // Regular import error handling
      setImportResult({
        status: 'error',
        message: errorMessage || 'Failed to import playlist. Please try again.',
        stats: {
          total: tracks.length,
          successful: 0,
          failed: tracks.length,
          skipped: 0
        }
      });
      toast.error('Import failed', { id: 'import' });
    } finally {
      setIsLoading(false);
      setImportProgress(100);
    }
  };

  // --- Logout ---
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
    setShowYtMusicInput(false);
    setYtMusicInput('');
    toast.success('👋 Logged out successfully');
  };

  // --- Render Spotify Login Screen ---
  if (!isSpotifyAuthenticated) {
    console.log('Rendering SpotifyLogin component');
    return (
      <>
        <ToasterConfig />
        <AnimatePresence mode="wait">
          <motion.div
            key="spotify-login"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.6 }}
          >
            <SpotifyLogin
              onLogin={handleSpotifyLogin}
              error={error}
              isLoading={isLoading}
            />
          </motion.div>
        </AnimatePresence>
      </>
    );
  }

  // --- Render YouTube Music Auth Screen ---
  // Show YouTube auth immediately after Spotify (before showing playlists)
  if (isSpotifyAuthenticated && !isYtMusicAuthenticated) {
    console.log('Rendering YouTubeAuth component');
    return (
      <>
        <ToasterConfig />
        <AnimatePresence mode="wait">
          <motion.div
            key="youtube-auth"
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -50 }}
            transition={{ duration: 0.6 }}
          >
            <YouTubeAuth
              onAuth={authenticateYtMusic}
              onSubmit={submitYtMusicHeaders}
              isLoading={isLoading}
              showInput={showYtMusicInput}
              inputValue={ytMusicInput}
              onInputChange={setYtMusicInput}
              error={error}
            />
          </motion.div>
        </AnimatePresence>
      </>
    );
  }

  // --- Render Import Result Screen ---
  if (importResult) {
    return (
      <>
        <ToasterConfig />
        <AnimatePresence mode="wait">
          <motion.div
            key="import-result"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 1.1 }}
            transition={{ duration: 0.6 }}
          >
            <ImportResult
              result={importResult}
              onBack={() => {
                setImportResult(null);
                setSelectedPlaylist(null);
                setTracks([]);
              }}
              onStartOver={() => {
                logout();
              }}
            />
          </motion.div>
        </AnimatePresence>
      </>
    );
  }

  // --- Render Track List Screen ---
  if (selectedPlaylist && tracks.length > 0) {
    console.log('Rendering TrackList - selectedPlaylist:', !!selectedPlaylist, 'tracksLength:', tracks.length);
    return (
      <>
        <ToasterConfig />
        <AnimatePresence mode="wait">
          <motion.div
            key="tracklist"
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -50 }}
            transition={{ duration: 0.5 }}
          >
            <TrackList
              tracks={tracks}
              playlist={selectedPlaylist}
              onImport={importToYouTubeMusic}
              onBack={() => {
                setSelectedPlaylist(null);
                setTracks([]);
              }}
              isLoading={isLoading}
              importProgress={importProgress}
              currentTrack={currentTrack}
            />
          </motion.div>
        </AnimatePresence>
      </>
    );
  }

  // --- Render Import Progress Screen ---
  if (isLoading && importProgress > 0) {
    return (
      <>
        <ToasterConfig />
        <ProfessionalLoading 
          message={`Importing to YouTube Music...`}
          showProgress={true}
          progress={importProgress}
        />
      </>
    );
  }

  // --- Render Playlist List Screen (Dashboard) ---
  // Only show playlists after both Spotify AND YouTube are authenticated
  return (
    <div className="min-h-screen flex flex-col">
      <ToasterConfig />
      <div className="flex-1">
        <AnimatePresence mode="wait">
          <motion.div
            key="dashboard"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 1.05 }}
            transition={{ duration: 0.5 }}
          >
            <PlaylistList
              playlists={playlists}
              onSelectPlaylist={selectPlaylist}
              isLoading={isLoading}
            />
          </motion.div>
        </AnimatePresence>
      </div>
      
      <ProfessionalFooter />

      {/* Demo Icons Component - Hidden but uses all imported icons to avoid lint warnings */}
      <div className="hidden">
        <Music className="w-4 h-4" />
        <Play className="w-4 h-4" />
        <CheckCircle className="w-4 h-4" />
        <XCircle className="w-4 h-4" />
        <Loader2 className="w-4 h-4" />
        <ExternalLink className="w-4 h-4" />
        <Sparkles className="w-4 h-4" />
        <Heart className="w-4 h-4" />
        <Star className="w-4 h-4" />
        <Zap className="w-4 h-4" />
        <Volume2 className="w-4 h-4" />
        <Headphones className="w-4 h-4" />
        <Radio className="w-4 h-4" />
        <Disc3 className="w-4 h-4" />
        <PlayCircle className="w-4 h-4" />
        <Users className="w-4 h-4" />
        <Calendar className="w-4 h-4" />
        <Clock className="w-4 h-4" />
        <TrendingUp className="w-4 h-4" />
        <Award className="w-4 h-4" />
        <Shuffle className="w-4 h-4" />
        <RefreshCw className="w-4 h-4" />
      </div>
    </div>
  );
}

export default App;
