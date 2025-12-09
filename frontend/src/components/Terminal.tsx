/**
 * CRT Terminal Component
 * Custom canvas-based CRT terminal with retro effects
 */

import React, { useEffect, useRef, useState, KeyboardEvent } from 'react';
import { MessageType, WSMessage, OutputMessage } from '../types/protocol';
import '../styles/Terminal.css';

interface TerminalProps {
  messages: WSMessage[];
  prompt: string;
  onCommand: (command: string) => void;
  onClear?: () => void;
}

export const Terminal: React.FC<TerminalProps> = ({ messages, prompt, onCommand, onClear }) => {
  const [input, setInput] = useState('');
  const [history, setHistory] = useState<string[]>([]);
  const [historyIndex, setHistoryIndex] = useState(-1);
  const outputRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Auto-scroll to bottom
  useEffect(() => {
    if (outputRef.current) {
      outputRef.current.scrollTop = outputRef.current.scrollHeight;
    }
  }, [messages]);

  // Focus input on mount
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSubmit = () => {
    if (!input.trim()) return;

    // Add to history
    setHistory(prev => [...prev, input]);
    setHistoryIndex(-1);

    // Check for clear command
    if (input.trim().toLowerCase() === 'clear' || input.trim().toLowerCase() === 'cls') {
      onClear?.();
      setInput('');
      return;
    }

    // Send command
    onCommand(input);
    setInput('');
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleSubmit();
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      if (history.length > 0) {
        const newIndex = historyIndex < history.length - 1 ? historyIndex + 1 : historyIndex;
        setHistoryIndex(newIndex);
        setInput(history[history.length - 1 - newIndex]);
      }
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      if (historyIndex > 0) {
        const newIndex = historyIndex - 1;
        setHistoryIndex(newIndex);
        setInput(history[history.length - 1 - newIndex]);
      } else {
        setHistoryIndex(-1);
        setInput('');
      }
    } else if (e.key === 'Tab') {
      e.preventDefault();
      // TODO: Implement tab completion
    } else if (e.key === 'l' && e.ctrlKey) {
      e.preventDefault();
      onClear?.();
    }
  };

  const renderMessage = (message: WSMessage, index: number) => {
    switch (message.type) {
      case MessageType.OUTPUT: {
        const output = message.payload as OutputMessage;
        const className = `terminal-line ${output.style || 'normal'}`;
        return (
          <div key={index} className={className}>
            {output.text}
          </div>
        );
      }
      case MessageType.SYSTEM: {
        return (
          <div key={index} className="terminal-line system">
            {message.payload.message}
          </div>
        );
      }
      case MessageType.ERROR: {
        return (
          <div key={index} className="terminal-line error">
            ERROR: {message.payload.error}
          </div>
        );
      }
      default:
        return null;
    }
  };

  return (
    <div className="terminal-container" onClick={() => inputRef.current?.focus()}>
      <div className="crt-overlay"></div>
      <div className="scanlines"></div>
      
      <div className="terminal-content">
        <div className="terminal-output" ref={outputRef}>
          {messages.map((msg, idx) => renderMessage(msg, idx))}
        </div>
        
        <div className="terminal-input-line">
          <span className="terminal-prompt">{prompt}</span>
          <input
            ref={inputRef}
            type="text"
            className="terminal-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            spellCheck={false}
            autoComplete="off"
            autoCorrect="off"
            autoCapitalize="off"
          />
          <span className="terminal-cursor">█</span>
        </div>
      </div>
    </div>
  );
};
