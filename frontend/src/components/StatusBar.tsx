/**
 * Status Bar Component
 * Displays game state information
 */

import React from 'react';
import { GameState } from '../hooks/useWebSocket';
import '../styles/StatusBar.css';

interface StatusBarProps {
  gameState: GameState;
  connected: boolean;
}

export const StatusBar: React.FC<StatusBarProps> = ({ gameState, connected }) => {
  return (
    <div className="status-bar">
      <div className="status-item">
        <span className="status-label">CONNECTION:</span>
        <span className={`status-value ${connected ? 'connected' : 'disconnected'}`}>
          {connected ? '● ONLINE' : '○ OFFLINE'}
        </span>
      </div>
      
      <div className="status-item">
        <span className="status-label">HOST:</span>
        <span className="status-value">{gameState.currentHost}</span>
      </div>
      
      <div className="status-item">
        <span className="status-label">USER:</span>
        <span className="status-value">{gameState.user}</span>
      </div>
      
      <div className="status-item">
        <span className="status-label">LEVEL:</span>
        <span className="status-value">{gameState.level}</span>
      </div>
      
      <div className="status-item">
        <span className="status-label">SCORE:</span>
        <span className="status-value score">{gameState.score}</span>
      </div>
    </div>
  );
};
