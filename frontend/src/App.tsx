/**
 * Main App Component
 */

import React, { useState, useEffect } from 'react';
import { Terminal } from './components/Terminal';
import { StatusBar } from './components/StatusBar';
import { useWebSocket } from './hooks/useWebSocket';
import './styles/App.css';

// Construct WebSocket URL based on current location
// This handles both localhost and GitHub Codespaces environments
const getWebSocketURL = (): string => {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const host = window.location.host;
  // Use the same host as the frontend
  return `${protocol}//${host}/ws/game`;
};

const WS_URL = getWebSocketURL();

function App() {
  const { connected, gameState, messages, sendCommand, clearMessages } = useWebSocket(WS_URL);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (connected) {
      // Small delay for initial messages to arrive
      setTimeout(() => setIsLoading(false), 500);
    }
  }, [connected]);

  const handleClear = () => {
    clearMessages();
  };

  if (isLoading) {
    return (
      <div className="loading-screen">
        <div className="loading-text">INITIALIZING TERMINAL...</div>
        <div className="loading-spinner"></div>
      </div>
    );
  }

  return (
    <div className="app-container">
      <div className="app-header">
        <div className="app-title">◈ CRT HACKER ◈</div>
        <div className="app-subtitle">TERMINAL ACCESS SYSTEM v1.0</div>
      </div>
      
      <div className="app-main">
        {/* Task Box */}
        <div className="task-box">
          <div className="task-box-title">[ CURRENT MISSION ]</div>
          <div className="task-box-content">
            <div className="task-box-item">
              • Scan local network
            </div>
            <div className="task-box-item">
              • Find target host
            </div>
            <div className="task-box-item">
              • Exploit vulnerability
            </div>
            <div className="task-box-item">
              • Capture flag
            </div>
          </div>
        </div>
        
        {/* Terminal Section */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <div className="terminal-wrapper">
            <Terminal
              messages={messages}
              prompt={gameState.prompt}
              onCommand={sendCommand}
              onClear={handleClear}
            />
          </div>
          
          <StatusBar gameState={gameState} connected={connected} />
        </div>
      </div>
    </div>
  );
}

export default App;
