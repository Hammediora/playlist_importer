import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Music, Play, SkipForward, Volume2, Clock, Award, RefreshCw, Disc3 } from 'lucide-react';

// Spotify Logo SVG Component
const SpotifyLogo = ({ className }) => (
  <svg viewBox="0 0 24 24" className={className} fill="currentColor">
    <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.42 1.56-.299.421-1.02.599-1.559.3z"/>
  </svg>
);

// YouTube Logo SVG Component
const YouTubeLogo = ({ className }) => (
  <svg viewBox="0 0 24 24" className={className} fill="currentColor">
    <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
  </svg>
);

// Animation variants
const containerVariants = {
  initial: { opacity: 0 },
  animate: {
    opacity: 1,
    transition: {
      staggerChildren: 0.05
    }
  }
};

const trackVariants = {
  initial: { 
    opacity: 0, 
    x: -20,
    scale: 0.98
  },
  animate: { 
    opacity: 1, 
    x: 0,
    scale: 1,
    transition: {
      duration: 0.4,
      ease: "easeOut"
    }
  },
  hover: {
    scale: 1.01,
    x: 5,
    transition: {
      duration: 0.2
    }
  }
};

const TrackList = ({ 
  tracks, 
  playlist, 
  onImport, 
  onBack, 
  isLoading, 
  importProgress, 
  currentTrack 
}) => {
  const formatDuration = (ms) => {
    if (!ms) return '0:00';
    const minutes = Math.floor(ms / 60000);
    const seconds = ((ms % 60000) / 1000).toFixed(0);
    return `${minutes}:${seconds.padStart(2, '0')}`;
  };

  const formatNumber = (num) => {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num?.toString() || '0';
  };

  const getPopularityColor = (popularity) => {
    if (popularity >= 80) return 'text-green-400';
    if (popularity >= 60) return 'text-yellow-400';
    if (popularity >= 40) return 'text-orange-400';
    return 'text-red-400';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-indigo-900 to-blue-900 p-6 relative overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0">
        <div className="absolute top-20 left-20 w-72 h-72 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse"></div>
        <div className="absolute top-40 right-20 w-72 h-72 bg-blue-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse delay-1000"></div>
        <div className="absolute -bottom-8 left-20 w-72 h-72 bg-indigo-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse delay-2000"></div>
      </div>
      
      <motion.div 
        className="max-w-6xl mx-auto relative z-10"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        {/* Header */}
        <motion.div 
          className="mb-8"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <button
            onClick={onBack}
            className="group flex items-center text-gray-300 hover:text-white mb-6 transition-colors duration-300 hover:scale-105"
          >
            <motion.div
              whileHover={{ x: -5 }}
              transition={{ duration: 0.2 }}
            >
              <SkipForward className="w-5 h-5 mr-2 rotate-180" />
            </motion.div>
            <span>Back to Playlists</span>
          </button>

          <div className="flex items-center space-x-8">
            {/* Playlist Cover */}
            <motion.div 
              className="relative"
              whileHover={{ scale: 1.05 }}
              transition={{ duration: 0.3 }}
            >
              {playlist?.images && playlist.images[0] ? (
                <motion.img
                  src={playlist.images[0].url}
                  alt={playlist.name}
                  className="w-40 h-40 rounded-3xl shadow-2xl"
                  initial={{ scale: 0.8, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={{ duration: 0.5 }}
                />
              ) : (
                <motion.div 
                  className="w-40 h-40 bg-gradient-to-br from-purple-500 via-indigo-600 to-blue-600 rounded-3xl shadow-2xl flex items-center justify-center relative"
                  initial={{ scale: 0.8, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={{ duration: 0.5 }}
                >
                  <div className="absolute inset-0 bg-black/20 rounded-3xl" />
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
                    className="relative z-10"
                  >
                    <Disc3 className="w-20 h-20 text-white opacity-90" />
                  </motion.div>
                </motion.div>
              )}
              
              {/* Animated border */}
              <motion.div 
                className="absolute inset-0 border-2 border-purple-400/50 rounded-3xl opacity-0"
                animate={{ 
                  opacity: [0, 0.8, 0],
                  scale: [1, 1.05, 1]
                }}
                transition={{ 
                  duration: 3, 
                  repeat: Infinity,
                  ease: "easeInOut" 
                }}
              />
            </motion.div>

            {/* Playlist Info */}
            <div className="flex-1">
              <motion.h1 
                className="text-5xl font-bold bg-gradient-to-r from-white via-purple-200 to-blue-200 bg-clip-text text-transparent mb-3"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5, delay: 0.3 }}
              >
                {playlist?.name || 'Playlist'}
              </motion.h1>
              
              <motion.p 
                className="text-gray-300 mb-6 text-lg"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5, delay: 0.4 }}
              >
                {playlist?.description || 'No description'}
              </motion.p>
              
              {/* Enhanced Stats */}
              <motion.div 
                className="flex items-center space-x-6 mb-6"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5, delay: 0.5 }}
              >
                <div className="flex items-center bg-white/10 rounded-lg px-4 py-2 backdrop-blur-sm">
                  <Music className="w-5 h-5 mr-2 text-purple-400" />
                  <span className="text-white font-medium">{tracks?.length || 0} tracks</span>
                </div>
                <div className="flex items-center bg-white/10 rounded-lg px-4 py-2 backdrop-blur-sm">
                  <Volume2 className="w-5 h-5 mr-2 text-blue-400" />
                  <span className="text-white font-medium">{formatNumber(playlist?.followers?.total || 0)} followers</span>
                </div>
                <div className="flex items-center bg-white/10 rounded-lg px-4 py-2 backdrop-blur-sm">
                  <Clock className="w-5 h-5 mr-2 text-green-400" />
                  <span className="text-white font-medium">
                    {Math.round((tracks?.reduce((acc, track) => acc + (track.duration_ms || 0), 0) || 0) / 60000)} min
                  </span>
                </div>
              </motion.div>
              
              {/* Platform Badges */}
              <motion.div 
                className="flex items-center space-x-4 mb-4"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5, delay: 0.6 }}
              >
                <div className="flex items-center bg-green-500/20 border border-green-500/30 rounded-lg px-4 py-2 backdrop-blur-sm">
                  <SpotifyLogo className="w-5 h-5 mr-2" />
                  <span className="text-green-300 font-medium">From Spotify</span>
                </div>
                <div className="flex items-center text-gray-400">
                  <span className="mr-2">→</span>
                </div>
                <div className="flex items-center bg-red-500/20 border border-red-500/30 rounded-lg px-4 py-2 backdrop-blur-sm">
                  <YouTubeLogo className="w-5 h-5 mr-2" />
                  <span className="text-red-300 font-medium">To YouTube Music</span>
                </div>
              </motion.div>
            </div>

            {/* Import Button */}
            <motion.button
              onClick={onImport}
              disabled={isLoading}
              className="group relative overflow-hidden bg-gradient-to-r from-red-500 via-red-600 to-red-700 hover:from-red-600 hover:via-red-700 hover:to-red-800 disabled:from-gray-500 disabled:to-gray-600 text-white font-bold py-5 px-10 rounded-2xl transition-all duration-300 flex items-center shadow-2xl hover:shadow-red-500/25"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5, delay: 0.7 }}
              whileHover={{ scale: isLoading ? 1 : 1.05 }}
              whileTap={{ scale: isLoading ? 1 : 0.95 }}
            >
              <motion.div className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/30 to-white/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000" />
              <div className="relative flex items-center">
                {isLoading ? (
                  <>
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                    >
                      <RefreshCw className="w-6 h-6 mr-3" />
                    </motion.div>
                    <span className="text-lg">Importing...</span>
                  </>
                ) : (
                  <>
                    <YouTubeLogo className="w-6 h-6 mr-3" />
                    <span className="text-lg">Import to YouTube Music</span>
                  </>
                )}
              </div>
            </motion.button>
          </div>
        </motion.div>

        {/* Progress Bar */}
        <AnimatePresence>
          {isLoading && importProgress !== undefined && (
            <motion.div 
              className="mb-8 backdrop-blur-sm bg-white/10 border border-white/20 rounded-xl p-6"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.5 }}
            >
              <div className="flex items-center justify-between mb-4">
                <span className="text-white font-medium">Import Progress</span>
                <span className="text-gray-300">{Math.round(importProgress)}%</span>
              </div>
              
              <div className="relative h-3 bg-gray-700 rounded-full overflow-hidden">
                <motion.div 
                  className="absolute inset-y-0 left-0 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full"
                  initial={{ width: 0 }}
                  animate={{ width: `${importProgress}%` }}
                  transition={{ duration: 0.5, ease: "easeOut" }}
                />
                <motion.div 
                  className="absolute inset-y-0 left-0 bg-gradient-to-r from-white/30 to-transparent rounded-full"
                  animate={{ 
                    x: [`-${100-importProgress}%`, `${importProgress}%`] 
                  }}
                  transition={{ 
                    duration: 2, 
                    repeat: Infinity, 
                    ease: "easeInOut" 
                  }}
                  style={{ width: '30%' }}
                />
              </div>
              
              {currentTrack && (
                <motion.p 
                  className="text-gray-400 text-sm mt-3"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  key={currentTrack}
                >
                  Currently importing: <span className="text-white">{currentTrack}</span>
                </motion.p>
              )}
            </motion.div>
          )}
        </AnimatePresence>

        {/* Track List */}
        <motion.div 
          className="backdrop-blur-sm bg-white/5 border border-white/10 rounded-2xl overflow-hidden"
          variants={containerVariants}
          initial="initial"
          animate="animate"
        >
          {/* Table Header */}
          <div className="grid grid-cols-12 gap-4 p-4 border-b border-white/10 text-gray-400 text-sm font-medium">
            <div className="col-span-1">#</div>
            <div className="col-span-5">Title</div>
            <div className="col-span-3">Artist</div>
            <div className="col-span-1">Popularity</div>
            <div className="col-span-2">Duration</div>
          </div>

          {/* Track Items */}
          <div className="max-h-96 overflow-y-auto">
            {tracks?.map((track, index) => (
              <motion.div
                key={track.id || index}
                variants={trackVariants}
                whileHover="hover"
                className="grid grid-cols-12 gap-4 p-4 border-b border-white/5 hover:bg-white/5 transition-colors group"
              >
                <div className="col-span-1 flex items-center">
                  <span className="text-gray-400 text-sm group-hover:hidden">
                    {index + 1}
                  </span>
                  <motion.div
                    className="hidden group-hover:block"
                    whileHover={{ scale: 1.2 }}
                  >
                    <Play className="w-4 h-4 text-white" />
                  </motion.div>
                </div>
                
                <div className="col-span-5 flex items-center">
                  <div className="flex items-center space-x-3">
                    {track.album?.images && track.album.images[0] ? (
                      <motion.img
                        src={track.album.images[0].url}
                        alt={track.album.name}
                        className="w-10 h-10 rounded-lg shadow-md"
                        whileHover={{ scale: 1.1 }}
                        transition={{ duration: 0.2 }}
                      />
                    ) : (
                      <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-blue-500 rounded-lg flex items-center justify-center">
                        <Music className="w-5 h-5 text-white" />
                      </div>
                    )}
                    <div>
                      <p className="text-white font-medium line-clamp-1 group-hover:text-purple-300 transition-colors">
                        {track.name}
                      </p>
                      <p className="text-gray-400 text-sm line-clamp-1">
                        {track.album?.name || 'Unknown Album'}
                      </p>
                    </div>
                  </div>
                </div>
                
                <div className="col-span-3 flex items-center">
                  <p className="text-gray-300 line-clamp-1">
                    {track.artists?.map(artist => artist.name).join(', ') || 'Unknown Artist'}
                  </p>
                </div>
                
                <div className="col-span-1 flex items-center">
                  <div className="flex items-center space-x-1">
                    <Award className={`w-4 h-4 ${getPopularityColor(track.popularity)}`} />
                    <span className={`text-sm ${getPopularityColor(track.popularity)}`}>
                      {track.popularity || 0}
                    </span>
                  </div>
                </div>
                
                <div className="col-span-2 flex items-center">
                  <div className="flex items-center text-gray-400">
                    <Clock className="w-4 h-4 mr-1" />
                    <span className="text-sm">{formatDuration(track.duration_ms)}</span>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Empty State */}
        {!tracks || tracks.length === 0 ? (
          <motion.div 
            className="text-center py-20"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <motion.div
              animate={{ 
                y: [0, -10, 0],
                rotate: [0, 10, -10, 0] 
              }}
              transition={{ 
                duration: 4, 
                repeat: Infinity,
                ease: "easeInOut" 
              }}
            >
              <Music className="w-16 h-16 text-gray-500 mx-auto mb-4" />
            </motion.div>
            <h3 className="text-2xl font-bold text-gray-400 mb-2">No Tracks Found</h3>
            <p className="text-gray-500">
              This playlist appears to be empty or the tracks couldn't be loaded.
            </p>
          </motion.div>
        ) : null}
      </motion.div>
    </div>
  );
};

export default TrackList;
