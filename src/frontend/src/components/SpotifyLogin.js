import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle } from 'lucide-react';
import { Music, Play, Headphones, Radio, Heart, Sparkles } from 'lucide-react';

const SpotifyLogin = ({ 
  onLogin, 
  isLoading, 
  error
}) => {
  const [hoveredButton, setHoveredButton] = useState(null);

  const floatingIcons = [
    { Icon: Music, delay: 0, x: -20, y: -30 },
    { Icon: Play, delay: 0.5, x: 40, y: -20 },
    { Icon: Headphones, delay: 1, x: -30, y: 20 },
    { Icon: Radio, delay: 1.5, x: 30, y: 30 },
    { Icon: Heart, delay: 2, x: -40, y: 0 },
    { Icon: Sparkles, delay: 2.5, x: 0, y: -40 }
  ];

  const handleSpotifyLogin = () => {
    onLogin();
  };

  // Spotify Logo SVG Component
  const SpotifyLogo = ({ className }) => (
    <svg viewBox="0 0 24 24" className={className} fill="currentColor">
      <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.42 1.56-.299.421-1.02.599-1.559.3z"/>
    </svg>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-900 via-black to-green-800 flex items-center justify-center relative overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0">
        {[...Array(20)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-2 h-2 bg-green-400 rounded-full opacity-20"
            animate={{
              x: [0, Math.random() * 100 - 50],
              y: [0, Math.random() * 100 - 50],
              scale: [1, 1.5, 1],
              opacity: [0.2, 0.5, 0.2]
            }}
            transition={{
              duration: 3 + Math.random() * 2,
              repeat: Infinity,
              delay: Math.random() * 2
            }}
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`
            }}
          />
        ))}
      </div>

      {/* Main content */}
      <motion.div
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="text-center z-10 max-w-md mx-auto px-6"
      >
        {/* Logo and floating icons */}
        <div className="relative mb-8">
          <motion.div
            initial={{ scale: 0, rotate: -180 }}
            animate={{ scale: 1, rotate: 0 }}
            transition={{ 
              duration: 1, 
              delay: 0.2,
              type: "spring",
              stiffness: 100
            }}
            className="w-24 h-24 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-6 relative shadow-2xl"
          >
            <SpotifyLogo className="w-12 h-12 text-white" />
            
            {/* Floating icons around the logo */}
            {floatingIcons.map(({ Icon, delay, x, y }, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, scale: 0 }}
                animate={{ 
                  opacity: 0.6, 
                  scale: 1,
                  x: x,
                  y: y
                }}
                transition={{ 
                  delay: delay,
                  duration: 0.5,
                  type: "spring"
                }}
                className="absolute w-8 h-8 bg-green-400 rounded-full flex items-center justify-center shadow-lg"
              >
                <Icon className="w-4 h-4 text-white" />
              </motion.div>
            ))}
          </motion.div>
        </div>

        {/* Title */}
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4, duration: 0.6 }}
          className="text-6xl font-bold bg-gradient-to-r from-white via-gray-100 to-gray-300 bg-clip-text text-transparent mb-4"
        >
          Playlist Importer
        </motion.h1>

        {/* Subtitle */}
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6, duration: 0.6 }}
          className="text-xl text-gray-300 mb-2"
        >
          Professional playlist migration tool
        </motion.p>
        
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7, duration: 0.6 }}
          className="text-2xl font-semibold bg-gradient-to-r from-green-400 to-blue-400 bg-clip-text text-transparent mb-8"
        >
          Spotify → YouTube Music
        </motion.p>

        {/* Error message */}
        <AnimatePresence>
          {error && (
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.8 }}
              className="bg-red-500/20 border border-red-500/30 text-red-300 p-4 rounded-xl mb-6 backdrop-blur-sm"
            >
              {error}
            </motion.div>
          )}
        </AnimatePresence>

        {/* Spotify Connect Button */}
        <motion.button
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8, duration: 0.6 }}
          whileHover={{ 
            scale: 1.02,
            boxShadow: "0 25px 50px rgba(34, 197, 94, 0.3)"
          }}
          whileTap={{ scale: 0.98 }}
          onHoverStart={() => setHoveredButton('spotify')}
          onHoverEnd={() => setHoveredButton(null)}
          onClick={handleSpotifyLogin}
          disabled={isLoading}
          className="group w-full bg-gradient-to-r from-green-500 via-green-600 to-green-700 hover:from-green-600 hover:via-green-700 hover:to-green-800 text-white font-bold py-5 px-8 rounded-2xl transition-all duration-300 mb-8 relative overflow-hidden shadow-2xl disabled:opacity-50 border border-green-400/20"
        >
          {/* Shimmer effect */}
          <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000"></div>
          
          <motion.div
            className="flex items-center justify-center relative z-10"
            animate={hoveredButton === 'spotify' ? { x: [0, 3, 0] } : {}}
            transition={{ duration: 0.3 }}
          >
            <SpotifyLogo className="w-6 h-6 mr-3" />
            <span className="text-lg font-semibold">{isLoading ? 'Connecting...' : 'Connect with Spotify'}</span>
          </motion.div>
        </motion.button>

        {/* Professional Features */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1, duration: 0.6 }}
          className="mt-8 space-y-3"
        >
          <div className="flex items-center justify-center space-x-6">
            <div className="flex items-center text-gray-400">
              <CheckCircle className="w-5 h-5 mr-2 text-green-400" />
              <span className="text-sm font-medium">Secure OAuth</span>
            </div>
            <div className="flex items-center text-gray-400">
              <CheckCircle className="w-5 h-5 mr-2 text-green-400" />
              <span className="text-sm font-medium">Fast Transfer</span>
            </div>
            <div className="flex items-center text-gray-400">
              <CheckCircle className="w-5 h-5 mr-2 text-green-400" />
              <span className="text-sm font-medium">No Data Loss</span>
            </div>
          </div>
        </motion.div>

        {/* Status indicators */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.2, duration: 0.6 }}
          className="flex justify-center space-x-4 mt-6"
        >
          <div className="flex items-center px-4 py-2 rounded-full text-sm bg-gray-800/50 backdrop-blur-sm border border-gray-700">
            <div className="w-2 h-2 rounded-full mr-2 bg-gray-400 animate-pulse" />
            <span className="text-gray-300">Spotify Disconnected</span>
          </div>
          
          <div className="flex items-center px-4 py-2 rounded-full text-sm bg-gray-800/50 backdrop-blur-sm border border-gray-700">
            <div className="w-2 h-2 rounded-full mr-2 bg-gray-400 animate-pulse" />
            <span className="text-gray-300">YouTube Music Disconnected</span>
          </div>
        </motion.div>
      </motion.div>
    </div>
  );
};

export default SpotifyLogin;
