/**
 * CRT Terminal Component
 * Custom canvas-based CRT terminal with retro effects
 */

import React, { useEffect, useRef, useState, KeyboardEvent } from 'react';
import { MessageType, WSMessage, OutputMessage } from '../types/protocol';
import { getAutocompleteSuggestions } from '../services/autocomplete';
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
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [cursorPos, setCursorPos] = useState(0);
  const outputRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const cursorRefRef = useRef<HTMLSpanElement>(null);

  // Auto-scroll to bottom
  useEffect(() => {
    if (outputRef.current) {
      outputRef.current.scrollTop = outputRef.current.scrollHeight;
    }
  }, [messages, input]);

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

    // Send command to server
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
      const result = getAutocompleteSuggestions(input);
      
      if (result.completed && result.completed !== input) {
        // There's a completion to apply
        setInput(result.completed);
        setSuggestions([]);
      } else if (result.suggestions.length > 0) {
        // Show suggestions
        setSuggestions(result.suggestions);
      }
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
      case MessageType.INPUT: {
        // Show previously entered commands
        const inputLine = message.payload;
        return (
          <div key={index} className="terminal-input-history">
            <span className="terminal-prompt">{inputLine.prompt}</span>
            <span className="terminal-command-text">{inputLine.command}</span>
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
          
          {/* Current input line shows in output */}
          <div className="terminal-input-line">
            <span className="terminal-prompt">{prompt}</span>
            <div style={{ position: 'relative', flex: 1 }}>
              <input
                ref={inputRef}
                type="text"
                className="terminal-input"
                value={input}
                onChange={(e) => {
                  setInput(e.target.value);
                  setCursorPos(e.currentTarget.selectionStart || 0);
                  setSuggestions([]);
                }}
                onKeyDown={handleKeyDown}
                onKeyUp={(e) => setCursorPos(e.currentTarget.selectionStart || 0)}
                onClick={(e) => setCursorPos(e.currentTarget.selectionStart || 0)}
                spellCheck={false}
                autoComplete="off"
                autoCorrect="off"
                autoCapitalize="off"
              />
              {/* Cursor Positionierungshilfe */}
              <span 
                ref={cursorRefRef}
                style={{ 
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  visibility: 'hidden',
                  whiteSpace: 'pre',
                  fontFamily: 'inherit',
                  fontSize: 'inherit',
                  letterSpacing: 'inherit'
                }}
              >
                {input.substring(0, cursorPos)}
              </span>
              <span
                className="terminal-cursor"
                style={{
                  left: cursorRefRef.current ? `${cursorRefRef.current.offsetWidth}px` : '0px'
                }}
              >
                █
              </span>
            </div>
          </div>
          
          {suggestions.length > 0 && (
            <div className="terminal-suggestions">
              {suggestions.map((suggestion, idx) => (
                <div key={idx} className="suggestion-item">
                  {suggestion}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
