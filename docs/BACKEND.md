# Backend Architecture Documentation

## Overview

The backend is built with FastAPI and WebSocket for real-time communication. It implements a deterministic game engine with command parsing, state management, and persistence.

## Directory Structure

```
backend/
├── app/
│   ├── api/              # WebSocket endpoints
│   │   └── websocket.py  # Main WS handler
│   ├── core/             # Core game logic
│   │   ├── database.py   # Database operations
│   │   ├── dispatcher.py # Command routing
│   │   ├── engine.py     # Game engine
│   │   └── parser.py     # Command parser
│   ├── game/             # Game world
│   │   └── commands.py   # Command implementations
│   └── models/           # Data models
│       ├── game_state.py # Game state models
│       └── protocol.py   # WebSocket protocol
├── main.py               # Application entry point
└── requirements.txt      # Python dependencies
```

## Core Components

### 1. Game Engine (`core/engine.py`)

The central orchestrator managing:

- Session creation and lifecycle
- Game world state
- Command processing pipeline
- Auto-save functionality

**Key Methods:**

- `create_session(username)` - Initialize new game
- `process_command(session_id, command_line)` - Process player input
- `get_prompt(session_id)` - Generate terminal prompt

### 2. Command Parser (`core/parser.py`)

Tokenizes command strings into command and arguments using shell-like parsing with `shlex`.

**Features:**

- Handles quoted strings
- Separates positional args from flags
- Supports both short (`-f`) and long (`--flag`) options

### 3. Command Dispatcher (`core/dispatcher.py`)

Routes parsed commands to appropriate handlers.

**Architecture:**

- Registry pattern for command registration
- Command base class for extensibility
- Built-in error handling

### 4. Command Implementations (`game/commands.py`)

Built-in commands:

- **Navigation**: `ls`, `cd`, `pwd`
- **File Operations**: `cat`
- **Network**: `scan`, `connect`, `crack`
- **System**: `help`, `clear`, `exit`

**Adding New Commands:**

```python
class NewCommand(Command):
    def __init__(self):
        super().__init__("commandname", "Description", aliases=["alias"])

    async def execute(self, world: GameWorld, args: List[str]) -> CommandResult:
        # Implementation
        return CommandResult(output=[...])
```

### 5. WebSocket Protocol (`models/protocol.py`)

Strongly-typed message system using Pydantic:

**Message Types:**

- `COMMAND` - Client → Server command input
- `OUTPUT` - Server → Client terminal output
- `STATE_UPDATE` - Server → Client game state sync
- `PROMPT` - Server → Client prompt update
- `SYSTEM` - Server → Client system messages
- `ERROR` - Server → Client error messages

### 6. Game State Models (`models/game_state.py`)

**Core Models:**

- `GameWorld` - Complete game state
- `PlayerState` - Player progress and inventory
- `VirtualHost` - Network host with services and filesystem
- `VirtualFile` - Filesystem node (tree structure)
- `NetworkService` - Simulated network service

## WebSocket Flow

```
1. Client connects → Server creates session
2. Server sends welcome message
3. Server sends initial prompt and state
4. Client sends command
5. Server processes command
6. Server sends output messages
7. Server sends updated prompt and state
8. Repeat from step 4
```

## Database Schema

### Tables

**players**

- `id` - Primary key
- `username` - Unique username
- `password_hash` - Hashed password
- `created_at`, `last_login` - Timestamps

**sessions**

- `session_id` - Primary key (UUID)
- `player_id` - Foreign key (optional)
- `game_state` - Serialized JSON
- `created_at`, `last_activity` - Timestamps

**game_saves**

- `id` - Primary key
- `player_id` - Foreign key
- `save_name` - Save slot name
- `game_state` - Serialized JSON
- `saved_at` - Timestamp

## Extending the Game

### Adding New Hosts

In `engine.py`, modify `_create_initial_world()`:

```python
new_host = VirtualHost(
    hostname="newhost",
    ip="192.168.1.20",
    services=[
        NetworkService(
            port=80,
            name="http",
            status=ServiceStatus.OPEN,
            vulnerability="sql_injection"
        )
    ],
    filesystem=create_filesystem(),
    difficulty=2
)
world.hosts["newhost"] = new_host
```

### Adding Puzzles

Puzzles are implemented as vulnerabilities on services. Modify the `CrackCommand` to add logic:

```python
if service.vulnerability == "custom_puzzle":
    # Implement puzzle logic
    if user_solved_puzzle(args):
        target_host.compromised = True
        return success_result
    else:
        return failure_result
```

## Running the Backend

```bash
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Server runs on `http://localhost:8000`
WebSocket endpoint: `ws://localhost:8000/ws/game`

## Testing

```bash
pytest tests/
```

## Production Considerations

1. **Authentication**: Implement JWT tokens
2. **Rate Limiting**: Add command rate limits
3. **Input Validation**: Sanitize all user input
4. **Session Cleanup**: Background task to clean old sessions
5. **Horizontal Scaling**: Use Redis for shared session state
6. **Monitoring**: Add logging and metrics
