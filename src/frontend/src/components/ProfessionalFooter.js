import React from 'react';
import { motion } from 'framer-motion';
import { Heart, Github, ExternalLink, Shield, Zap } from 'lucide-react';

const ProfessionalFooter = () => {
  return (
    <motion.footer 
      className="bg-black/20 backdrop-blur-sm border-t border-white/10 mt-auto"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 1, duration: 0.6 }}
    >
      <div className="max-w-6xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          
          {/* Brand Section */}
          <div className="text-center md:text-left">
            <div className="flex items-center justify-center md:justify-start mb-4">
              <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-blue-600 rounded-full flex items-center justify-center mr-3">
                <Zap className="w-4 h-4 text-white" />
              </div>
              <h3 className="text-xl font-bold text-white">Playlist Importer</h3>
            </div>
            <p className="text-gray-400 text-sm">
              Professional playlist migration tool for seamless music platform transfers.
            </p>
          </div>

          {/* Features Section */}
          <div className="text-center">
            <h4 className="text-white font-semibold mb-4">Features</h4>
            <div className="space-y-2 text-sm text-gray-400">
              <div className="flex items-center justify-center">
                <Shield className="w-4 h-4 mr-2 text-green-400" />
                <span>Secure OAuth Authentication</span>
              </div>
              <div className="flex items-center justify-center">
                <Zap className="w-4 h-4 mr-2 text-blue-400" />
                <span>Fast & Reliable Transfer</span>
              </div>
              <div className="flex items-center justify-center">
                <Heart className="w-4 h-4 mr-2 text-red-400" />
                <span>Preserve All Track Data</span>
              </div>
            </div>
          </div>

          {/* Links Section */}
          <div className="text-center md:text-right">
            <h4 className="text-white font-semibold mb-4">Support</h4>
            <div className="space-y-2 text-sm">
              <button 
                className="flex items-center justify-center md:justify-end text-gray-400 hover:text-white transition-colors cursor-pointer"
                onClick={() => window.open('https://github.com', '_blank')}
              >
                <Github className="w-4 h-4 mr-2" />
                <span>GitHub</span>
              </button>
              <button 
                className="flex items-center justify-center md:justify-end text-gray-400 hover:text-white transition-colors cursor-pointer"
                onClick={() => window.open('https://docs.example.com', '_blank')}
              >
                <ExternalLink className="w-4 h-4 mr-2" />
                <span>Documentation</span>
              </button>
              <button 
                className="flex items-center justify-center md:justify-end text-gray-400 hover:text-white transition-colors cursor-pointer"
                onClick={() => window.open('https://privacy.example.com', '_blank')}
              >
                <Shield className="w-4 h-4 mr-2" />
                <span>Privacy Policy</span>
              </button>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-white/10 mt-8 pt-6">
          <div className="flex flex-col md:flex-row justify-between items-center text-sm text-gray-400">
            <div className="flex items-center mb-4 md:mb-0">
              <span>Made with</span>
              <Heart className="w-4 h-4 mx-1 text-red-400 animate-pulse" />
              <span>for music lovers</span>
            </div>
            <div className="flex items-center space-x-4">
              <span>© 2024 Playlist Importer</span>
              <span>•</span>
              <span>v1.0.0</span>
            </div>
          </div>
        </div>
      </div>
    </motion.footer>
  );
};

export default ProfessionalFooter; 