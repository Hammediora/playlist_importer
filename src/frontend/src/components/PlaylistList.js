import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Music2, ChevronRight, Users, Calendar, TrendingUp, Eye, Lock, Shuffle } from 'lucide-react';

// Spotify Logo SVG Component
const SpotifyLogo = ({ className }) => (
  <svg viewBox="0 0 24 24" className={className} fill="currentColor">
    <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.42 1.56-.299.421-1.02.599-1.559.3z"/>
  </svg>
);

// Animation variants
const listVariants = {
  initial: { opacity: 0 },
  animate: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
};

const itemVariants = {
  initial: { 
    opacity: 0, 
    x: -30,
    scale: 0.95
  },
  animate: { 
    opacity: 1, 
    x: 0,
    scale: 1,
    transition: {
      duration: 0.5,
      ease: "easeOut"
    }
  },
  hover: {
    scale: 1.02,
    x: 10,
    transition: {
      duration: 0.2,
      ease: "easeOut"
    }
  }
};

const PlaylistList = ({ playlists, onSelectPlaylist, isLoading }) => {
  const formatNumber = (num) => {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num?.toString() || '0';
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Unknown';
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  };

  const getPrivacyIcon = (isPublic) => {
    return isPublic ? <Eye className="w-4 h-4" /> : <Lock className="w-4 h-4" />;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-900 via-emerald-900 to-teal-900 p-6">
      <motion.div 
        className="max-w-6xl mx-auto"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        {/* Header */}
        <motion.div 
          className="text-center mb-10"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <motion.div 
            className="relative inline-block mb-6"
            whileHover={{ scale: 1.05 }}
          >
            <motion.div 
              className="absolute inset-0 bg-gradient-to-r from-green-400 to-green-600 rounded-full blur-lg opacity-75"
              animate={{ scale: [1, 1.1, 1] }}
              transition={{ duration: 3, repeat: Infinity }}
            />
            <div className="relative bg-gradient-to-r from-green-500 to-green-600 w-20 h-20 rounded-full flex items-center justify-center shadow-2xl">
              <SpotifyLogo className="w-10 h-10 text-white" />
            </div>
          </motion.div>
          
          <h1 className="text-6xl font-bold bg-gradient-to-r from-white via-green-100 to-green-300 bg-clip-text text-transparent mb-4">
            Your Spotify Playlists
          </h1>
          <p className="text-gray-300 text-xl font-medium">
            Select a playlist to import to YouTube Music
          </p>
          
          {/* Connected status badges */}
          <div className="flex justify-center space-x-4 mt-6">
            <motion.div
              initial={{ opacity: 0, scale: 0 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.4, duration: 0.5 }}
              className="flex items-center px-6 py-3 rounded-full text-sm bg-green-500/20 backdrop-blur-sm border border-green-500/30"
            >
              <div className="w-3 h-3 rounded-full mr-3 bg-green-400 animate-pulse" />
              <SpotifyLogo className="w-4 h-4 mr-2" />
              <span className="text-green-300 font-medium">Spotify Connected</span>
            </motion.div>
            
            <motion.div
              initial={{ opacity: 0, scale: 0 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.6, duration: 0.5 }}
              className="flex items-center px-6 py-3 rounded-full text-sm bg-red-500/20 backdrop-blur-sm border border-red-500/30"
            >
              <div className="w-3 h-3 rounded-full mr-3 bg-red-400 animate-pulse" />
              <svg viewBox="0 0 24 24" className="w-4 h-4 mr-2" fill="currentColor">
                <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
              </svg>
              <span className="text-red-300 font-medium">YouTube Connected</span>
            </motion.div>
          </div>
        </motion.div>

        {/* Loading State */}
        <AnimatePresence>
          {isLoading && (
            <motion.div 
              className="text-center py-20"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                className="inline-block"
              >
                <Shuffle className="w-12 h-12 text-green-400 mb-4" />
              </motion.div>
              <p className="text-gray-300 text-lg">Loading your playlists...</p>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Playlists Grid */}
        <AnimatePresence>
          {!isLoading && playlists && playlists.length > 0 && (
            <motion.div 
              className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
              variants={listVariants}
              initial="initial"
              animate="animate"
            >
              {playlists.map((playlist, index) => (
                <motion.div
                  key={playlist.id}
                  variants={itemVariants}
                  whileHover="hover"
                  onClick={() => onSelectPlaylist(playlist)}
                  className="group cursor-pointer backdrop-blur-sm bg-white/5 border border-white/10 rounded-3xl overflow-hidden shadow-xl hover:shadow-2xl transition-all duration-500 hover:border-green-400/30"
                >
                  {/* Playlist Image */}
                  <div className="relative h-56 overflow-hidden">
                    {playlist.images && playlist.images[0] ? (
                      <motion.img
                        src={playlist.images[0].url}
                        alt={playlist.name}
                        className="w-full h-full object-cover"
                        whileHover={{ scale: 1.15 }}
                        transition={{ duration: 0.6, ease: "easeOut" }}
                      />
                    ) : (
                      <motion.div 
                        className="w-full h-full bg-gradient-to-br from-green-500 via-green-600 to-emerald-600 flex items-center justify-center relative"
                        whileHover={{ scale: 1.15 }}
                        transition={{ duration: 0.6, ease: "easeOut" }}
                      >
                        <div className="absolute inset-0 bg-black/20" />
                        <Music2 className="w-20 h-20 text-white opacity-80 relative z-10" />
                      </motion.div>
                    )}
                    
                    {/* Gradient Overlay */}
                    <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent" />
                    
                    {/* Play Button */}
                    <motion.div 
                      className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100"
                      initial={{ scale: 0.8, y: 20 }}
                      whileHover={{ scale: 1, y: 0 }}
                      transition={{ duration: 0.3, ease: "easeOut" }}
                    >
                      <motion.div 
                        className="bg-green-500/90 backdrop-blur-sm rounded-full p-4 shadow-2xl"
                        whileHover={{ scale: 1.1, backgroundColor: "rgba(34, 197, 94, 1)" }}
                        whileTap={{ scale: 0.95 }}
                      >
                        <ChevronRight className="w-8 h-8 text-white" />
                      </motion.div>
                    </motion.div>
                    
                    {/* Track Count Badge */}
                    <div className="absolute top-4 right-4">
                      <motion.div 
                        className="bg-black/50 backdrop-blur-sm px-3 py-1 rounded-full text-sm font-medium text-white"
                        initial={{ opacity: 0, scale: 0.8 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: 0.1 * index }}
                      >
                        {formatNumber(playlist.tracks?.total || 0)} tracks
                      </motion.div>
                    </div>
                  </div>

                  {/* Playlist Info */}
                  <div className="p-6 space-y-4">
                    <div>
                      <h3 className="font-bold text-white text-xl mb-2 line-clamp-2 group-hover:text-green-300 transition-colors duration-300">
                        {playlist.name}
                      </h3>
                      
                      {playlist.description && (
                        <p className="text-gray-400 text-sm line-clamp-2">
                          {playlist.description}
                        </p>
                      )}
                    </div>

                    {/* Enhanced Stats Grid */}
                    <div className="grid grid-cols-2 gap-3">
                      <div className="flex items-center text-gray-300 bg-white/5 rounded-lg px-3 py-2">
                        <Music2 className="w-4 h-4 mr-2 text-green-400" />
                        <span className="text-sm font-medium">{formatNumber(playlist.tracks?.total || 0)}</span>
                      </div>
                      
                      <div className="flex items-center text-gray-300 bg-white/5 rounded-lg px-3 py-2">
                        {getPrivacyIcon(playlist.public)}
                        <span className="ml-2 text-sm font-medium">{playlist.public ? 'Public' : 'Private'}</span>
                      </div>
                      
                      <div className="flex items-center text-gray-300 bg-white/5 rounded-lg px-3 py-2">
                        <Users className="w-4 h-4 mr-2 text-blue-400" />
                        <span className="text-sm font-medium">{formatNumber(playlist.followers?.total || 0)}</span>
                      </div>
                      
                      <div className="flex items-center text-gray-300 bg-white/5 rounded-lg px-3 py-2">
                        <Calendar className="w-4 h-4 mr-2 text-purple-400" />
                        <span className="text-sm font-medium">{formatDate(playlist.created_at)}</span>
                      </div>
                    </div>

                    {/* Owner */}
                    {playlist.owner && (
                      <div className="pt-4 border-t border-white/10">
                        <div className="flex items-center text-gray-400 text-sm">
                          <TrendingUp className="w-4 h-4 mr-2" />
                          <span>by {playlist.owner.display_name || 'Unknown'}</span>
                        </div>
                      </div>
                    )}
                  </div>
                </motion.div>
              ))}
            </motion.div>
          )}
        </AnimatePresence>

        {/* Empty State */}
        <AnimatePresence>
          {!isLoading && playlists && playlists.length === 0 && (
            <motion.div 
              className="text-center py-20"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.5 }}
            >
              <motion.div
                animate={{ 
                  y: [0, -10, 0],
                  rotate: [0, 5, -5, 0] 
                }}
                transition={{ 
                  duration: 4, 
                  repeat: Infinity,
                  ease: "easeInOut" 
                }}
              >
                <Music2 className="w-16 h-16 text-gray-500 mx-auto mb-4" />
              </motion.div>
              <h3 className="text-2xl font-bold text-gray-400 mb-2">No Playlists Found</h3>
              <p className="text-gray-500">
                It looks like you don't have any playlists yet. Create some in Spotify first!
              </p>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>
    </div>
  );
};

export default PlaylistList;
