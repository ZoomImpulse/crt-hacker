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
  const [isActive, setIsActive] = useState(true);
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
        const newInput = history[history.length - 1 - newIndex];
        setInput(newInput);
        // Move cursor to end
        setTimeout(() => setCursorPos(newInput.length), 0);
      }
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      if (historyIndex > 0) {
        const newIndex = historyIndex - 1;
        setHistoryIndex(newIndex);
        const newInput = history[history.length - 1 - newIndex];
        setInput(newInput);
        // Move cursor to end
        setTimeout(() => setCursorPos(newInput.length), 0);
      } else {
        setHistoryIndex(-1);
        setInput('');
        setCursorPos(0);
      }
    } else if (e.key === 'ArrowLeft') {
      e.preventDefault();
      setCursorPos(Math.max(0, cursorPos - 1));
      setTimeout(() => {
        if (inputRef.current) {
          inputRef.current.setSelectionRange(cursorPos - 1, cursorPos - 1);
        }
      }, 0);
    } else if (e.key === 'ArrowRight') {
      e.preventDefault();
      setCursorPos(Math.min(input.length, cursorPos + 1));
      setTimeout(() => {
        if (inputRef.current) {
          inputRef.current.setSelectionRange(cursorPos + 1, cursorPos + 1);
        }
      }, 0);
    } else if (e.key === 'Home') {
      e.preventDefault();
      setCursorPos(0);
      if (inputRef.current) {
        inputRef.current.setSelectionRange(0, 0);
      }
    } else if (e.key === 'End') {
      e.preventDefault();
      setCursorPos(input.length);
      if (inputRef.current) {
        inputRef.current.setSelectionRange(input.length, input.length);
      }
    } else if (e.key === 'Tab') {
      e.preventDefault();
      const result = getAutocompleteSuggestions(input);
      
      // Always apply the completion directly (classic TAB behavior)
      if (result.completed && result.completed !== input) {
        setInput(result.completed);
        // Set cursor to end of input
        setTimeout(() => {
          if (inputRef.current) {
            inputRef.current.setSelectionRange(result.completed.length, result.completed.length);
          }
        }, 0);
      }
      
      // Only show suggestions if there are multiple matches and we're at the common prefix
      if (result.hasMultipleMatches && result.matches) {
        setSuggestions(result.matches);
      } else {
        setSuggestions([]);
      }
    } else if (e.key === 'l' && e.ctrlKey) {
      e.preventDefault();
      onClear?.();
    } else if (e.key === 'Backspace') {
      // Let the browser handle backspace, just update cursorPos after
      setTimeout(() => {
        const newPos = inputRef.current?.selectionStart || 0;
        setCursorPos(newPos);
      }, 0);
    } else if (e.key === 'Delete') {
      // Let the browser handle delete, just update cursorPos after
      setTimeout(() => {
        const newPos = inputRef.current?.selectionStart || 0;
        setCursorPos(newPos);
      }, 0);
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
                  // Update cursor position on every keystroke
                  const newPos = e.currentTarget.selectionStart || 0;
                  setCursorPos(newPos);
                  setSuggestions([]);
                }}
                onKeyDown={handleKeyDown}
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
                  whiteSpace: 'pre-wrap',
                  fontFamily: 'inherit',
                  fontSize: 'inherit',
                  letterSpacing: 'inherit',
                  fontWeight: 'inherit'
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
        </div>
      </div>
    </div>
  );
};
