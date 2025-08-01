import React from 'react';
import { Toaster } from 'react-hot-toast';

const ToasterConfig = () => {
  return (
    <Toaster 
      position="top-right"
      toastOptions={{
        duration: 4000,
        style: {
          borderRadius: '12px',
          background: '#1e293b',
          color: '#fff',
          border: '1px solid #334155',
          backdropFilter: 'blur(8px)',
          fontSize: '14px',
          fontWeight: '500',
        },
        success: {
          iconTheme: {
            primary: '#22c55e',
            secondary: '#fff',
          },
          style: {
            border: '1px solid #22c55e',
            boxShadow: '0 8px 32px rgba(34, 197, 94, 0.2)',
          },
        },
        error: {
          iconTheme: {
            primary: '#ef4444',
            secondary: '#fff',
          },
          style: {
            border: '1px solid #ef4444',
            boxShadow: '0 8px 32px rgba(239, 68, 68, 0.2)',
          },
        },
        loading: {
          iconTheme: {
            primary: '#3b82f6',
            secondary: '#fff',
          },
          style: {
            border: '1px solid #3b82f6',
            boxShadow: '0 8px 32px rgba(59, 130, 246, 0.2)',
          },
        },
      }}
    />
  );
};

export default ToasterConfig;
