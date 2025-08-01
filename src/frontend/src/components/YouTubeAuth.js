import React from 'react';

const YouTubeAuth = ({
  onAuth,
  onSubmit,
  isLoading,
  showInput,
  inputValue,
  onInputChange,
  error
}) => {
  console.log('YouTubeAuth component rendering with props:', { isLoading, showInput, error: !!error });

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #dc2626 0%, #000000 50%, #dc2626 100%)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      color: 'white',
      fontFamily: 'Arial, sans-serif'
    }}>
      <div style={{
        textAlign: 'center',
        padding: '2rem',
        background: 'rgba(0,0,0,0.3)',
        borderRadius: '1rem',
        maxWidth: '500px',
        width: '90%'
      }}>
        <h1 style={{ fontSize: '3rem', marginBottom: '1rem' }}>🎵 YouTube Music</h1>
        <p style={{ fontSize: '1.2rem', marginBottom: '2rem' }}>
          {error?.includes('expired') || error?.includes('re-authenticate')
            ? 'Re-authenticate your YouTube Music account'
            : 'Connect your YouTube Music account'
          }
        </p>

        {!showInput ? (
          <button
            onClick={onAuth}
            disabled={isLoading}
            style={{
              background: '#dc2626',
              color: 'white',
              border: 'none',
              padding: '15px 30px',
              borderRadius: '25px',
              fontSize: '16px',
              cursor: isLoading ? 'not-allowed' : 'pointer',
              opacity: isLoading ? 0.7 : 1,
              transition: 'all 0.3s ease'
            }}
          >
            {isLoading ? 'Connecting...' : 'Connect YouTube Music'}
          </button>
        ) : (
          <div>
            <p style={{ marginBottom: '1rem', color: '#fbbf24' }}>
              {error?.includes('expired') ? 'Authentication Expired' : 'Manual setup required'}
            </p>
            <p style={{ marginBottom: '1rem', fontSize: '0.9rem', color: '#d1d5db' }}>
              {error?.includes('expired')
                ? 'Your YouTube Music session has expired. Please get fresh credentials and paste them below:'
                : 'Please follow the YouTube Music setup instructions and paste your OAuth credentials below:'
              }
            </p>

            {/* Instructions for getting headers */}
            <div className="bg-blue-500/10 border border-blue-500/30 rounded-xl p-6 mb-6 backdrop-blur-sm">
              <div className="flex items-center mb-4">
                <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center mr-3">
                  <span className="text-white text-sm font-bold">1</span>
                </div>
                <h3 className="text-blue-300 font-semibold">📋 Copy as cURL (Recommended)</h3>
              </div>
              <ol className="text-blue-200 text-sm space-y-2 ml-4">
                <li className="flex items-start">
                  <span className="w-2 h-2 bg-blue-400 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                  Open YouTube Music in Chrome and log in
                </li>
                <li className="flex items-start">
                  <span className="w-2 h-2 bg-blue-400 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                  Open Developer Tools (F12) → Network tab
                </li>
                <li className="flex items-start">
                  <span className="w-2 h-2 bg-blue-400 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                  Play any song or search for something
                </li>
                <li className="flex items-start">
                  <span className="w-2 h-2 bg-blue-400 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                  Look for a request to <code className="bg-blue-500/20 px-1 rounded">music.youtube.com/youtubei/v1/</code>
                </li>
                <li className="flex items-start">
                  <span className="w-2 h-2 bg-blue-400 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                  Right-click → Copy → Copy as cURL
                </li>
                <li className="flex items-start">
                  <span className="w-2 h-2 bg-blue-400 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                  Paste the entire cURL command below
                </li>
              </ol>

              <div className="mt-6 pt-4 border-t border-blue-500/20">
                <div className="flex items-center mb-3">
                  <div className="w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center mr-3">
                    <span className="text-white text-sm font-bold">2</span>
                  </div>
                  <h3 className="text-purple-300 font-semibold">📝 Raw Headers (Alternative)</h3>
                </div>
                <p className="text-purple-200 text-sm mb-2">
                  You can also paste headers manually in this format:
                </p>
                <code className="bg-purple-500/20 px-2 py-1 rounded text-xs text-purple-200 block">
                  cookie: VISITOR_INFO1_LIVE=...<br/>
                  authorization: SAPISIDHASH ...<br/>
                  x-goog-authuser: 0
                </code>
              </div>

              <div className="mt-4 p-3 bg-blue-500/20 rounded-lg border border-blue-500/30">
                <p className="text-blue-200 text-sm font-medium">
                  💡 <strong>Pro Tip:</strong> cURL format is easier and more reliable!
                </p>
              </div>
            </div>
            <div className="relative">
              <textarea
                value={inputValue}
                onChange={(e) => onInputChange(e.target.value)}
                placeholder="Paste your cURL command or raw headers here...&#10;&#10;Example:&#10;curl 'https://music.youtube.com/youtubei/v1/...' \&#10;  -H 'authorization: SAPISIDHASH ...' \&#10;  -H 'cookie: VISITOR_INFO1_LIVE=...' \&#10;  --data-raw '{...}'"
                className="w-full h-48 p-4 rounded-xl border border-gray-600/30 bg-white/5 backdrop-blur-sm text-white text-sm font-mono resize-none focus:outline-none focus:ring-2 focus:ring-red-500/50 focus:border-red-500/50 transition-all duration-300"
                style={{ lineHeight: '1.4' }}
              />
              <div className="absolute top-2 right-2 text-xs text-gray-400 bg-black/20 px-2 py-1 rounded">
                {inputValue.length} chars
              </div>
            </div>
            
            <button
              onClick={onSubmit}
              disabled={isLoading || !inputValue.trim()}
              className={`w-full py-4 px-6 rounded-xl font-semibold text-white transition-all duration-300 transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none ${
                inputValue.trim() 
                  ? 'bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 shadow-lg hover:shadow-xl' 
                  : 'bg-gray-600 cursor-not-allowed'
              }`}
            >
              <div className="flex items-center justify-center">
                {isLoading ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Authenticating...
                  </>
                ) : (
                  <>
                    <span className="mr-2">🔐</span>
                    {error?.includes('expired') ? 'Re-authenticate' : 'Submit Credentials'}
                  </>
                )}
              </div>
            </button>
          </div>
        )}

        {error && (
          <div style={{
            color: '#ff6b6b',
            marginTop: '1rem',
            padding: '10px',
            background: 'rgba(255, 107, 107, 0.1)',
            borderRadius: '5px',
            border: '1px solid rgba(255, 107, 107, 0.3)'
          }}>
            {error}
          </div>
        )}
      </div>
    </div>
  );
};

export default YouTubeAuth