# Frontend Architecture Documentation

## Overview

React + TypeScript frontend with custom CRT terminal rendering and WebSocket communication.

## Directory Structure

```
frontend/
├── src/
│   ├── components/       # React components
│   │   ├── Terminal.tsx  # Main terminal component
│   │   └── StatusBar.tsx # Game status display
│   ├── hooks/            # Custom React hooks
│   │   └── useWebSocket.ts
│   ├── services/         # Business logic
│   │   └── websocket.ts  # WebSocket client
│   ├── styles/           # CSS files
│   │   ├── App.css
│   │   ├── Terminal.css
│   │   └── StatusBar.css
│   ├── types/            # TypeScript types
│   │   └── protocol.ts   # WebSocket protocol types
│   ├── App.tsx           # Root component
│   └── main.tsx          # Entry point
├── index.html
├── package.json
├── tsconfig.json
└── vite.config.ts
```

## Key Components

### 1. WebSocket Service (`services/websocket.ts`)

Low-level WebSocket client with:

- Automatic reconnection logic
- Message handler subscription system
- Connection state management

**Usage:**

```typescript
const ws = new WebSocketService("ws://localhost:8000/ws/game");
await ws.connect();
ws.onMessage((message) => {
  // Handle message
});
ws.sendCommand("ls");
```

### 2. useWebSocket Hook (`hooks/useWebSocket.ts`)

React hook providing:

- WebSocket connection management
- Game state synchronization
- Message history
- Command sending

**Returns:**

- `connected` - Connection status
- `gameState` - Current game state
- `messages` - Message history
- `sendCommand(cmd)` - Send command function
- `clearMessages()` - Clear terminal

### 3. Terminal Component (`components/Terminal.tsx`)

Main terminal UI with:

- Message rendering
- Input handling
- Command history (up/down arrows)
- Keyboard shortcuts
- Auto-scroll

**Features:**

- Style-aware message rendering (normal, error, success, etc.)
- Command history navigation
- Tab completion (placeholder)
- Ctrl+L to clear

### 4. StatusBar Component (`components/StatusBar.tsx`)

Displays:

- Connection status
- Current host
- Username
- Level
- Score

## CRT Effects

### Visual Effects Applied

1. **Screen Curvature** - Radial gradient overlay
2. **Scanlines** - Horizontal lines with animation
3. **Phosphor Glow** - Green text-shadow
4. **Screen Flicker** - Subtle opacity animation
5. **CRT Overlay** - Repeating gradient for texture

### CSS Animations

- `flicker` - Screen intensity variation
- `scroll` - Scanline movement
- `blink` - Cursor blinking
- `pulse` - Status indicator pulsing

## Protocol Implementation

Messages are strongly-typed using TypeScript interfaces matching the backend protocol.

**Example Message Flow:**

```typescript
// Client sends command
{
  type: MessageType.COMMAND,
  payload: { command: 'ls', args: [] },
  timestamp: Date.now()
}

// Server responds with output
{
  type: MessageType.OUTPUT,
  payload: { text: 'file1.txt\nfile2.txt', style: 'normal' },
  timestamp: 1234567890
}

// Server updates prompt
{
  type: MessageType.PROMPT,
  payload: { prompt: 'user@host:~$ ' },
  timestamp: 1234567891
}
```

## State Management

State is managed through:

1. **Local State** - React useState for UI state
2. **WebSocket State** - Custom hook for game state
3. **Message History** - Array of WSMessage objects

No external state management library needed due to simple data flow.

## Styling Architecture

Pure CSS with custom properties for:

- CRT green: `#00ff00`
- Dark background: `#0a0a0a`
- Error red: `#ff0055`
- Success cyan: `#00ff88`

All animations are CSS-based for performance.

## Running the Frontend

```bash
cd frontend
npm install
npm run dev
```

Development server runs on `http://localhost:5173`

## Building for Production

```bash
npm run build
```

Output in `dist/` directory. Serve with any static file server.

## Customization

### Changing CRT Color

Modify CSS variables in `Terminal.css`:

```css
/* Change from green to amber */
color: #ffb000;
text-shadow: 0 0 5px #ffb000;
```

### Adding New Message Styles

1. Add style to `OutputMessage` type in `protocol.ts`
2. Add CSS class in `Terminal.css`
3. Add case in `renderMessage()` in `Terminal.tsx`

### Custom Keyboard Shortcuts

Add cases in `handleKeyDown()` in `Terminal.tsx`:

```typescript
if (e.key === "h" && e.ctrlKey) {
  e.preventDefault();
  sendCommand("help");
}
```

## Performance Considerations

1. **Message Limit** - Consider limiting message history (e.g., last 1000)
2. **Virtual Scrolling** - For very long output, implement virtual scrolling
3. **Debouncing** - Add debouncing to input for network efficiency
4. **Memoization** - Use React.memo for StatusBar

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

WebSocket and CSS animations required.

## Accessibility

Currently minimal. Consider adding:

- ARIA labels for screen readers
- High contrast mode
- Keyboard navigation indicators
- Focus management
