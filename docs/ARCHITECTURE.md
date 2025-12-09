# System Architecture Overview

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Browser                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              React Frontend (Port 5173)                 │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │ │
│  │  │   Terminal   │  │  Status Bar  │  │     App      │ │ │
│  │  │  Component   │  │  Component   │  │  Component   │ │ │
│  │  └──────┬───────┘  └──────────────┘  └──────┬───────┘ │ │
│  │         │                                     │         │ │
│  │         └─────────────┬───────────────────────┘         │ │
│  │                       │                                 │ │
│  │              ┌────────▼────────┐                        │ │
│  │              │  useWebSocket   │                        │ │
│  │              │      Hook       │                        │ │
│  │              └────────┬────────┘                        │ │
│  │                       │                                 │ │
│  │              ┌────────▼────────┐                        │ │
│  │              │   WebSocket     │                        │ │
│  │              │    Service      │                        │ │
│  │              └────────┬────────┘                        │ │
│  └───────────────────────┼─────────────────────────────────┘ │
│                          │                                   │
└──────────────────────────┼───────────────────────────────────┘
                           │
                    WebSocket (JSON)
                           │
┌──────────────────────────▼───────────────────────────────────┐
│                  FastAPI Backend (Port 8000)                  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │                   WebSocket Handler                     │  │
│  │              (api/websocket.py)                         │  │
│  └────────────────────────┬───────────────────────────────┘  │
│                           │                                   │
│  ┌────────────────────────▼───────────────────────────────┐  │
│  │                    Game Engine                          │  │
│  │                  (core/engine.py)                       │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │  │
│  │  │   Session    │  │  Game World  │  │   Player     │ │  │
│  │  │  Management  │  │    State     │  │    State     │ │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘ │  │
│  └────────────────────────┬───────────────────────────────┘  │
│                           │                                   │
│  ┌────────────────────────▼───────────────────────────────┐  │
│  │                  Command Parser                         │  │
│  │                 (core/parser.py)                        │  │
│  └────────────────────────┬───────────────────────────────┘  │
│                           │                                   │
│  ┌────────────────────────▼───────────────────────────────┐  │
│  │                Command Dispatcher                       │  │
│  │               (core/dispatcher.py)                      │  │
│  └────────┬──────────────────────────────────┬────────────┘  │
│           │                                  │                │
│  ┌────────▼────────┐              ┌─────────▼────────────┐  │
│  │   File System   │              │   Network Commands   │  │
│  │    Commands     │              │   (scan, connect,    │  │
│  │  (ls, cd, cat)  │              │      crack)          │  │
│  └─────────────────┘              └──────────────────────┘  │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │                  Database Layer                         │  │
│  │                (core/database.py)                       │  │
│  │                                                          │  │
│  │    SQLite (game.db)                                     │  │
│  │    - players                                            │  │
│  │    - sessions                                           │  │
│  │    - game_saves                                         │  │
│  └────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────┘
```

## Data Flow

### Command Execution Flow

```
1. User Input
   │
   ▼
2. Terminal Component (captures input)
   │
   ▼
3. WebSocket Service (sends COMMAND message)
   │
   ▼
4. WebSocket Handler (receives message)
   │
   ▼
5. Game Engine (retrieves session)
   │
   ▼
6. Command Parser (tokenizes command)
   │
   ▼
7. Command Dispatcher (routes to handler)
   │
   ▼
8. Command Implementation (executes logic)
   │
   ▼
9. Game Engine (updates state, saves)
   │
   ▼
10. WebSocket Handler (sends OUTPUT, PROMPT, STATE_UPDATE)
    │
    ▼
11. WebSocket Service (receives messages)
    │
    ▼
12. useWebSocket Hook (updates React state)
    │
    ▼
13. Terminal Component (renders output)
```

## Component Responsibilities

### Frontend Components

#### Terminal Component

- **Responsibilities:**
  - Render terminal output
  - Capture user input
  - Handle keyboard events
  - Manage command history
  - Auto-scroll output
- **Dependencies:**
  - WebSocket hook
  - Protocol types

#### StatusBar Component

- **Responsibilities:**
  - Display connection status
  - Show game state (host, user, level, score)
  - Visual status indicators
- **Dependencies:**
  - Game state from WebSocket hook

#### App Component

- **Responsibilities:**
  - Root component
  - Layout management
  - Loading state
  - Component composition
- **Dependencies:**
  - Terminal, StatusBar components
  - WebSocket hook

### Frontend Services

#### WebSocket Service

- **Responsibilities:**
  - Establish WebSocket connection
  - Send/receive messages
  - Automatic reconnection
  - Message handler subscription
- **Dependencies:**
  - Native WebSocket API
  - Protocol types

#### useWebSocket Hook

- **Responsibilities:**
  - React integration for WebSocket
  - Game state management
  - Message history
  - Command sending
- **Dependencies:**
  - WebSocket Service
  - React hooks

### Backend Components

#### Game Engine

- **Responsibilities:**
  - Session lifecycle
  - World state management
  - Command processing coordination
  - State persistence
- **Dependencies:**
  - Parser, Dispatcher
  - Database layer
  - Game state models

#### Command Parser

- **Responsibilities:**
  - Tokenize command strings
  - Parse flags and arguments
  - Shell-like syntax support
- **Dependencies:**
  - Python shlex

#### Command Dispatcher

- **Responsibilities:**
  - Command registration
  - Command routing
  - Error handling
  - Help generation
- **Dependencies:**
  - Command implementations

#### Commands

- **Responsibilities:**
  - Implement game logic
  - Validate inputs
  - Generate output
  - Update game state
- **Dependencies:**
  - Game state models
  - Protocol models

#### WebSocket Handler

- **Responsibilities:**
  - Accept connections
  - Message routing
  - Send responses
  - Connection management
- **Dependencies:**
  - Game Engine
  - Protocol models

#### Database Layer

- **Responsibilities:**
  - Schema management
  - State persistence
  - Session storage
  - Query interface
- **Dependencies:**
  - aiosqlite

## State Management

### Client State

```typescript
{
  // WebSocket connection state
  connected: boolean,

  // Game state (synced with server)
  gameState: {
    currentHost: string,
    currentPath: string,
    user: string,
    level: number,
    score: number,
    prompt: string
  },

  // UI state
  messages: WSMessage[],
  inputValue: string,
  commandHistory: string[]
}
```

### Server State

```python
{
  # Session registry
  worlds: Dict[str, GameWorld],

  # Per-session state
  GameWorld: {
    hosts: Dict[str, VirtualHost],
    player: PlayerState,
    objectives: List[str],
    hints: Dict[str, str]
  },

  # Player state
  PlayerState: {
    session_id: str,
    username: str,
    level: GameLevel,
    score: int,
    current_host: str,
    current_path: str,
    inventory: List[str],
    flags_collected: List[str],
    hosts_compromised: List[str],
    command_history: List[str]
  }
}
```

## Protocol Messages

### Message Flow Diagram

```
Client                                Server
  │                                     │
  │────── COMMAND ──────────────────────▶│
  │                                     │
  │                      ┌──────────────┤
  │                      │ Process      │
  │                      └──────────────┤
  │                                     │
  │◀────── OUTPUT ───────────────────────│
  │◀────── PROMPT ───────────────────────│
  │◀────── STATE_UPDATE ─────────────────│
  │                                     │
```

### Message Types Summary

**Client → Server:**

- `COMMAND` - Execute command
- `DISCONNECT` - Graceful shutdown

**Server → Client:**

- `OUTPUT` - Terminal output
- `PROMPT` - Prompt update
- `STATE_UPDATE` - Game state sync
- `SYSTEM` - System notifications
- `ERROR` - Error messages

## Security Architecture

### Authentication (Future)

```
┌────────────┐
│   Client   │
└─────┬──────┘
      │
      │ 1. POST /auth/login
      │    {username, password}
      ▼
┌────────────┐
│   Backend  │
│            │
│ 2. Verify credentials
│ 3. Generate JWT token
│            │
└─────┬──────┘
      │
      │ 4. Return {token}
      ▼
┌────────────┐
│   Client   │
│            │
│ 5. Store token
│ 6. Connect WebSocket with token
│            │
└────────────┘
```

### Input Validation

```
User Input
   │
   ▼
Frontend Basic Validation
   │
   ▼
WebSocket Transport
   │
   ▼
Backend Command Parser
   │
   ▼
Command-Specific Validation
   │
   ▼
Safe Execution
```

## Deployment Architecture

### Development

```
┌──────────────┐     ┌──────────────┐
│   Vite Dev   │     │   Uvicorn    │
│   Server     │────▶│   (reload)   │
│  Port 5173   │ WS  │  Port 8000   │
└──────────────┘     └──────┬───────┘
                            │
                     ┌──────▼───────┐
                     │   SQLite     │
                     │   game.db    │
                     └──────────────┘
```

### Production

```
┌──────────────┐     ┌──────────────┐
│    Nginx     │     │   Uvicorn    │
│  (Static +   │────▶│   Workers    │
│   Proxy)     │ WS  │  Port 8000   │
│  Port 80/443 │     └──────┬───────┘
└──────────────┘            │
                     ┌──────▼───────┐
                     │  PostgreSQL  │
                     │   (or Redis) │
                     └──────────────┘
```

## Performance Considerations

### Frontend Optimizations

1. **React.memo** - Memoize components
2. **Virtual Scrolling** - For long output
3. **Debouncing** - Input and network calls
4. **Code Splitting** - Lazy load components

### Backend Optimizations

1. **Connection Pooling** - Database connections
2. **Caching** - Redis for session state
3. **Load Balancing** - Multiple workers
4. **Rate Limiting** - Prevent abuse

## Scalability

### Horizontal Scaling

```
          Load Balancer
               │
    ┌──────────┼──────────┐
    │          │          │
    ▼          ▼          ▼
Worker 1   Worker 2   Worker 3
    │          │          │
    └──────────┼──────────┘
               │
        Shared Redis
        (Session State)
```

### Database Scaling

- **Read Replicas** - For read-heavy workloads
- **Partitioning** - By user/session
- **Caching** - Redis for hot data

## Monitoring

### Metrics to Track

- WebSocket connection count
- Active sessions
- Commands per second
- Average response time
- Error rate
- Database query time

### Logging

```python
# Backend logging structure
{
  "timestamp": "2024-01-01T12:00:00Z",
  "level": "INFO",
  "session_id": "abc-123",
  "event": "command_executed",
  "command": "ls",
  "duration_ms": 15,
  "success": true
}
```

## Error Handling

### Error Flow

```
Error Occurs
   │
   ▼
Component Try/Catch
   │
   ▼
Log Error
   │
   ▼
Send Error Message to Client
   │
   ▼
Display User-Friendly Message
   │
   ▼
Optionally Retry or Recover
```

### Error Types

1. **Network Errors** - WebSocket disconnect
2. **Validation Errors** - Invalid input
3. **Game Logic Errors** - Invalid command
4. **System Errors** - Database failure

## Testing Strategy

### Unit Tests

- Command implementations
- Parser logic
- State management

### Integration Tests

- WebSocket communication
- Database operations
- Command pipeline

### E2E Tests

- Full gameplay scenarios
- Connection handling
- State persistence
