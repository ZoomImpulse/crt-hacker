/**
 * WebSocket Protocol Types
 * Matches backend protocol definitions
 */

export enum MessageType {
  // Client -> Server
  COMMAND = 'command',
  CONNECT = 'connect',
  DISCONNECT = 'disconnect',
  
  // Server -> Client
  OUTPUT = 'output',
  ERROR = 'error',
  STATE_UPDATE = 'state_update',
  PROMPT = 'prompt',
  SYSTEM = 'system',
  INPUT = 'input'
}

export interface WSMessage {
  type: MessageType;
  payload: any;
  timestamp?: number;
}

export interface CommandMessage {
  command: string;
  args?: string[];
}

export interface OutputMessage {
  text: string;
  style?: 'normal' | 'success' | 'error' | 'warning' | 'info';
}

export interface ErrorMessage {
  error: string;
  code?: string;
}

export interface StateUpdateMessage {
  current_host: string;
  current_path: string;
  user: string;
  level: number;
  score: number;
}

export interface PromptMessage {
  prompt: string;
}

export interface SystemMessage {
  message: string;
  level?: 'info' | 'warning' | 'critical';
}
