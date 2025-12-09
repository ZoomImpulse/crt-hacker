/**
 * Custom React Hook for WebSocket Connection
 */

import { useEffect, useRef, useState } from 'react';
import { WebSocketService } from '../services/websocket';
import { WSMessage, MessageType, StateUpdateMessage } from '../types/protocol';

export interface GameState {
  currentHost: string;
  currentPath: string;
  user: string;
  level: number;
  score: number;
  prompt: string;
}

export function useWebSocket(url: string) {
  const wsRef = useRef<WebSocketService | null>(null);
  const [connected, setConnected] = useState(false);
  const [gameState, setGameState] = useState<GameState>({
    currentHost: 'localhost',
    currentPath: '/home/user',
    user: 'anonymous',
    level: 1,
    score: 0,
    prompt: '$ '
  });
  const [messages, setMessages] = useState<WSMessage[]>([]);

  useEffect(() => {
    const ws = new WebSocketService(url);
    wsRef.current = ws;

    // Subscribe to messages
    const unsubscribe = ws.onMessage((message) => {
      // Update game state
      if (message.type === MessageType.STATE_UPDATE) {
        const state = message.payload as StateUpdateMessage;
        setGameState(prev => ({
          ...prev,
          currentHost: state.current_host,
          currentPath: state.current_path,
          user: state.user,
          level: state.level,
          score: state.score
        }));
      } else if (message.type === MessageType.PROMPT) {
        setGameState(prev => ({
          ...prev,
          prompt: message.payload.prompt
        }));
      }

      // Store message for display
      setMessages(prev => [...prev, message]);
    });

    // Connect
    ws.connect()
      .then(() => setConnected(true))
      .catch((error) => {
        console.error('Failed to connect:', error);
        setConnected(false);
      });

    // Cleanup
    return () => {
      unsubscribe();
      ws.disconnect();
    };
  }, [url]);

  const sendCommand = (command: string) => {
    if (wsRef.current) {
      wsRef.current.sendCommand(command);
    }
  };

  const clearMessages = () => {
    setMessages([]);
  };

  return {
    connected,
    gameState,
    messages,
    sendCommand,
    clearMessages
  };
}
