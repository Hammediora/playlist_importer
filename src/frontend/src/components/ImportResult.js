import React from 'react';
import { motion } from 'framer-motion';
import { CheckCircle, XCircle, AlertCircle, Music2, ExternalLink, RotateCcw, Home } from 'lucide-react';

// Animation variants
const containerVariants = {
  initial: { opacity: 0, scale: 0.95 },
  animate: { 
    opacity: 1, 
    scale: 1,
    transition: {
      duration: 0.6,
      ease: "easeOut",
      staggerChildren: 0.1
    }
  }
};

const itemVariants = {
  initial: { opacity: 0, y: 20 },
  animate: { 
    opacity: 1, 
    y: 0,
    transition: {
      duration: 0.5,
      ease: "easeOut"
    }
  }
};

const ImportResult = ({ 
  result, 
  onBack, 
  onRetry, 
  onStartOver 
}) => {
  const getStatusIcon = (status) => {
    switch (status) {
      case 'success':
        return <CheckCircle className="w-8 h-8 text-green-400" />;
      case 'error':
        return <XCircle className="w-8 h-8 text-red-400" />;
      case 'warning':
        return <AlertCircle className="w-8 h-8 text-yellow-400" />;
      default:
        return <Music2 className="w-8 h-8 text-blue-400" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'success':
        return 'from-green-500 to-emerald-500';
      case 'error':
        return 'from-red-500 to-pink-500';
      case 'warning':
        return 'from-yellow-500 to-orange-500';
      default:
        return 'from-blue-500 to-purple-500';
    }
  };

  const getBackgroundGradient = (status) => {
    switch (status) {
      case 'success':
        return 'from-green-900 via-emerald-900 to-teal-900';
      case 'error':
        return 'from-red-900 via-pink-900 to-rose-900';
      case 'warning':
        return 'from-yellow-900 via-orange-900 to-red-900';
      default:
        return 'from-blue-900 via-purple-900 to-indigo-900';
    }
  };

  return (
    <div className={`min-h-screen bg-gradient-to-br ${getBackgroundGradient(result?.status)} flex items-center justify-center p-6`}>
      <motion.div 
        className="max-w-2xl w-full"
        variants={containerVariants}
        initial="initial"
        animate="animate"
      >
        {/* Main Result Card */}
        <motion.div 
          className="relative backdrop-blur-xl bg-white/10 border border-white/20 rounded-3xl shadow-2xl p-8 mb-6 overflow-hidden"
          variants={itemVariants}
          whileHover={{ scale: 1.01 }}
          transition={{ duration: 0.3 }}
        >
          {/* Animated Background Element */}
          <motion.div 
            className={`absolute inset-0 bg-gradient-to-r ${getStatusColor(result?.status)} rounded-3xl blur-xl opacity-30`}
            animate={{ scale: [1, 1.1, 1] }}
            transition={{ duration: 4, repeat: Infinity }}
          />
          
          {/* Shimmer effect */}
          <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent -translate-x-full animate-pulse"></div>
          
          <div className="relative text-center">
            {/* Status Icon */}
            <motion.div
              className="inline-flex items-center justify-center mb-6"
              initial={{ scale: 0, rotate: -180 }}
              animate={{ scale: 1, rotate: 0 }}
              transition={{ duration: 0.8, ease: "easeOut" }}
            >
              <motion.div
                animate={{ 
                  rotate: result?.status === 'success' ? [0, 360] : 0,
                  scale: [1, 1.1, 1] 
                }}
                transition={{ 
                  duration: result?.status === 'success' ? 2 : 1,
                  repeat: result?.status === 'success' ? 1 : Infinity,
                  repeatType: "loop"
                }}
              >
                {getStatusIcon(result?.status)}
              </motion.div>
            </motion.div>

            {/* Title */}
            <motion.h1 
              className="text-4xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent mb-4"
              variants={itemVariants}
            >
              {result?.status === 'success' && 'Import Successful!'}
              {result?.status === 'error' && 'Import Failed'}
              {result?.status === 'warning' && 'Import Completed with Issues'}
              {!result?.status && 'Import Result'}
            </motion.h1>

            {/* Message */}
            <motion.p 
              className="text-gray-300 text-lg mb-8 leading-relaxed"
              variants={itemVariants}
            >
              {result?.message || 'Your playlist import has been processed.'}
            </motion.p>

            {/* Stats */}
            {result?.stats && (
              <motion.div 
                className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8"
                variants={itemVariants}
              >
                {result.stats.total !== undefined && (
                  <motion.div 
                    className="backdrop-blur-sm bg-white/5 border border-white/10 rounded-xl p-4"
                    whileHover={{ scale: 1.05 }}
                  >
                    <div className="text-2xl font-bold text-white">{result.stats.total}</div>
                    <div className="text-gray-400 text-sm">Total Tracks</div>
                  </motion.div>
                )}
                
                {result.stats.successful !== undefined && (
                  <motion.div 
                    className="backdrop-blur-sm bg-white/5 border border-white/10 rounded-xl p-4"
                    whileHover={{ scale: 1.05 }}
                  >
                    <div className="text-2xl font-bold text-green-400">{result.stats.successful}</div>
                    <div className="text-gray-400 text-sm">Successful</div>
                  </motion.div>
                )}
                
                {result.stats.failed !== undefined && (
                  <motion.div 
                    className="backdrop-blur-sm bg-white/5 border border-white/10 rounded-xl p-4"
                    whileHover={{ scale: 1.05 }}
                  >
                    <div className="text-2xl font-bold text-red-400">{result.stats.failed}</div>
                    <div className="text-gray-400 text-sm">Failed</div>
                  </motion.div>
                )}
                
                {result.stats.skipped !== undefined && (
                  <motion.div 
                    className="backdrop-blur-sm bg-white/5 border border-white/10 rounded-xl p-4"
                    whileHover={{ scale: 1.05 }}
                  >
                    <div className="text-2xl font-bold text-yellow-400">{result.stats.skipped}</div>
                    <div className="text-gray-400 text-sm">Skipped</div>
                  </motion.div>
                )}
              </motion.div>
            )}

            {/* YouTube Playlist Link */}
            {result?.youtubePlaylistUrl && (
              <motion.a
                href={result.youtubePlaylistUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="group inline-flex items-center justify-center bg-gradient-to-r from-red-500 to-pink-600 hover:from-red-600 hover:to-pink-700 text-white font-semibold py-3 px-6 rounded-xl transition-all duration-300 shadow-lg hover:shadow-xl mb-8"
                variants={itemVariants}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.98 }}
              >
                <motion.div className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/20 to-white/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000" />
                <div className="relative flex items-center">
                  <Music2 className="w-5 h-5 mr-2" />
                  <span>View on YouTube Music</span>
                  <ExternalLink className="w-4 h-4 ml-2" />
                </div>
              </motion.a>
            )}
          </div>
        </motion.div>

        {/* Action Buttons */}
        <motion.div 
          className="flex flex-col sm:flex-row gap-4 justify-center"
          variants={itemVariants}
        >
          <motion.button
            onClick={onStartOver}
            className="group relative overflow-hidden bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white font-semibold py-3 px-6 rounded-xl transition-all duration-300 flex items-center justify-center shadow-lg hover:shadow-xl"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.98 }}
          >
            <motion.div className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/20 to-white/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000" />
            <div className="relative flex items-center">
              <Home className="w-5 h-5 mr-2" />
              <span>Start Over</span>
            </div>
          </motion.button>

          <motion.button
            onClick={onBack}
            className="group relative overflow-hidden backdrop-blur-sm bg-white/10 hover:bg-white/20 border border-white/20 hover:border-white/30 text-white font-semibold py-3 px-6 rounded-xl transition-all duration-300 flex items-center justify-center shadow-lg hover:shadow-xl"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.98 }}
          >
            <motion.div className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/10 to-white/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000" />
            <div className="relative flex items-center">
              <span>Back to Playlists</span>
            </div>
          </motion.button>

          {result?.status === 'error' && onRetry && (
            <motion.button
              onClick={onRetry}
              className="group relative overflow-hidden bg-gradient-to-r from-orange-500 to-red-600 hover:from-orange-600 hover:to-red-700 text-white font-semibold py-3 px-6 rounded-xl transition-all duration-300 flex items-center justify-center shadow-lg hover:shadow-xl"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.98 }}
            >
              <motion.div className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/20 to-white/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000" />
              <div className="relative flex items-center">
                <RotateCcw className="w-5 h-5 mr-2" />
                <span>Retry Import</span>
              </div>
            </motion.button>
          )}
        </motion.div>

        {/* Failed Tracks Details */}
        {result?.failedTracks && result.failedTracks.length > 0 && (
          <motion.div 
            className="mt-6 backdrop-blur-sm bg-white/5 border border-white/10 rounded-2xl p-6"
            variants={itemVariants}
          >
            <h3 className="text-xl font-bold text-white mb-4 flex items-center">
              <XCircle className="w-5 h-5 mr-2 text-red-400" />
              Failed Tracks ({result.failedTracks.length})
            </h3>
            <div className="max-h-48 overflow-y-auto space-y-2">
              {result.failedTracks.map((track, index) => (
                <motion.div 
                  key={index}
                  className="flex items-center justify-between py-2 px-3 backdrop-blur-sm bg-white/5 rounded-lg"
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.05 }}
                >
                  <div>
                    <div className="text-white font-medium">{track.name}</div>
                    <div className="text-gray-400 text-sm">{track.artist}</div>
                  </div>
                  <div className="text-red-400 text-sm">{track.reason}</div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}
      </motion.div>
    </div>
  );
};

export default ImportResult;
