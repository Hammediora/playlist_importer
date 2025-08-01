import React from 'react';
import { motion } from 'framer-motion';
import { Music, Sparkles, Zap } from 'lucide-react';

const ProfessionalHeader = ({ title, subtitle, showLogo = true, showStats = false, stats = {} }) => {
  return (
    <motion.div 
      className="text-center mb-8"
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      {/* Logo */}
      {showLogo && (
        <motion.div 
          className="relative inline-block mb-6"
          whileHover={{ scale: 1.05 }}
        >
          <motion.div 
            className="absolute inset-0 bg-gradient-to-r from-purple-400 to-blue-600 rounded-full blur-lg opacity-75"
            animate={{ scale: [1, 1.1, 1] }}
            transition={{ duration: 3, repeat: Infinity }}
          />
          <div className="relative bg-gradient-to-r from-purple-500 to-blue-600 w-20 h-20 rounded-full flex items-center justify-center shadow-2xl">
            <Music className="w-10 h-10 text-white" />
          </div>
        </motion.div>
      )}
      
      {/* Title */}
      <motion.h1
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2, duration: 0.6 }}
        className="text-6xl font-bold bg-gradient-to-r from-white via-gray-100 to-gray-300 bg-clip-text text-transparent mb-4"
      >
        {title}
      </motion.h1>
      
      {/* Subtitle */}
      <motion.p
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4, duration: 0.6 }}
        className="text-gray-300 text-xl font-medium mb-6"
      >
        {subtitle}
      </motion.p>

      {/* Stats */}
      {showStats && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6, duration: 0.6 }}
          className="flex justify-center space-x-8 mt-6"
        >
          {Object.entries(stats).map(([key, value]) => (
            <div key={key} className="flex items-center text-gray-400">
              <Sparkles className="w-4 h-4 mr-2 text-purple-400" />
              <span className="text-sm font-medium">{key}: {value}</span>
            </div>
          ))}
        </motion.div>
      )}

      {/* Decorative elements */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.8, duration: 0.6 }}
        className="flex justify-center space-x-2 mt-4"
      >
        <motion.div
          animate={{ rotate: [0, 360] }}
          transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
        >
          <Zap className="w-4 h-4 text-purple-400" />
        </motion.div>
        <motion.div
          animate={{ rotate: [360, 0] }}
          transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
        >
          <Sparkles className="w-4 h-4 text-blue-400" />
        </motion.div>
        <motion.div
          animate={{ rotate: [0, 360] }}
          transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
        >
          <Zap className="w-4 h-4 text-purple-400" />
        </motion.div>
      </motion.div>
    </motion.div>
  );
};

export default ProfessionalHeader; 