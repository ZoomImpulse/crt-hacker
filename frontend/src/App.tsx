/**
 * Main App Component
 */

import React, { useState, useEffect } from 'react';
import { Terminal } from './components/Terminal';
import { StatusBar } from './components/StatusBar';
import { useWebSocket } from './hooks/useWebSocket';
import './styles/App.css';

const WS_URL = 'ws://localhost:8000/ws/game';

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
      
      <StatusBar gameState={gameState} connected={connected} />
      
      <div className="terminal-wrapper">
        <Terminal
          messages={messages}
          prompt={gameState.prompt}
          onCommand={sendCommand}
          onClear={handleClear}
        />
      </div>
    </div>
  );
}

export default App;
