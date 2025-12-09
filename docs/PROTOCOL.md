# WebSocket Protocol Specification

## Overview

Bidirectional WebSocket communication protocol for real-time terminal game interaction.

## Connection

**Endpoint:** `ws://localhost:8000/ws/game`

**Lifecycle:**

1. Client establishes WebSocket connection
2. Server creates game session and assigns UUID
3. Server sends welcome message
4. Server sends initial prompt and state
5. Bidirectional message exchange begins
6. On disconnect, session is stored for potential reconnection

## Message Format

All messages use JSON with the following structure:

```typescript
{
  "type": MessageType,
  "payload": Object,
  "timestamp": number  // Unix timestamp in seconds (optional)
}
```

## Message Types

### Client → Server

#### COMMAND

Execute a terminal command.

```json
{
  "type": "command",
  "payload": {
    "command": "ls -la",
    "args": [] // Optional, parsed from command string
  },
  "timestamp": 1234567890.123
}
```

#### DISCONNECT

Request graceful disconnection.

```json
{
  "type": "disconnect",
  "payload": {},
  "timestamp": 1234567890.123
}
```

### Server → Client

#### OUTPUT

Terminal output to display.

```json
{
  "type": "output",
  "payload": {
    "text": "file1.txt\nfile2.txt\n",
    "style": "normal" // normal, success, error, warning, info
  },
  "timestamp": 1234567890.123
}
```

**Styles:**

- `normal` - Standard output (green)
- `success` - Success messages (cyan)
- `error` - Error messages (red)
- `warning` - Warnings (yellow/amber)
- `info` - Information (blue)

#### PROMPT

Update terminal prompt.

```json
{
  "type": "prompt",
  "payload": {
    "prompt": "user@localhost:/home/user$ "
  },
  "timestamp": 1234567890.123
}
```

#### STATE_UPDATE

Synchronize game state.

```json
{
  "type": "state_update",
  "payload": {
    "current_host": "localhost",
    "current_path": "/home/user",
    "user": "anonymous",
    "level": 1,
    "score": 0
  },
  "timestamp": 1234567890.123
}
```

#### SYSTEM

System-level notifications.

```json
{
  "type": "system",
  "payload": {
    "message": "=== Welcome to CRT Hacker ===",
    "level": "info" // info, warning, critical
  },
  "timestamp": 1234567890.123
}
```

#### ERROR

Error message.

```json
{
  "type": "error",
  "payload": {
    "error": "Command not found: invalid_command",
    "code": "CMD_NOT_FOUND" // Optional error code
  },
  "timestamp": 1234567890.123
}
```

## Message Flow Examples

### Successful Command Execution

```
1. Client → Server:
{
  "type": "command",
  "payload": {"command": "ls"},
  "timestamp": 1000
}

2. Server → Client:
{
  "type": "output",
  "payload": {
    "text": "file1.txt\nfile2.txt\n",
    "style": "normal"
  },
  "timestamp": 1001
}

3. Server → Client:
{
  "type": "prompt",
  "payload": {"prompt": "user@localhost:~$ "},
  "timestamp": 1002
}

4. Server → Client:
{
  "type": "state_update",
  "payload": {
    "current_host": "localhost",
    "current_path": "/home/user",
    "user": "anonymous",
    "level": 1,
    "score": 0
  },
  "timestamp": 1003
}
```

### Command Error

```
1. Client → Server:
{
  "type": "command",
  "payload": {"command": "invalid"},
  "timestamp": 2000
}

2. Server → Client:
{
  "type": "output",
  "payload": {
    "text": "Command not found: invalid\nType 'help' for available commands.",
    "style": "error"
  },
  "timestamp": 2001
}

3. Server → Client:
{
  "type": "prompt",
  "payload": {"prompt": "user@localhost:~$ "},
  "timestamp": 2002
}
```

### State Change (Host Connection)

```
1. Client → Server:
{
  "type": "command",
  "payload": {"command": "connect target-01"},
  "timestamp": 3000
}

2. Server → Client:
{
  "type": "output",
  "payload": {
    "text": "Connected to target-01",
    "style": "success"
  },
  "timestamp": 3001
}

3. Server → Client:
{
  "type": "prompt",
  "payload": {"prompt": "user@target-01:/$ "},
  "timestamp": 3002
}

4. Server → Client:
{
  "type": "state_update",
  "payload": {
    "current_host": "target-01",
    "current_path": "/",
    "user": "anonymous",
    "level": 1,
    "score": 100
  },
  "timestamp": 3003
}
```

## Error Handling

### Connection Errors

- **Connection Failed**: Client should retry with exponential backoff
- **Connection Closed**: Server may close on error; client should attempt reconnection
- **Heartbeat**: Consider implementing ping/pong for connection health

### Message Errors

- **Invalid JSON**: Server ignores malformed messages
- **Unknown Message Type**: Server responds with error message
- **Invalid Payload**: Server responds with error message

## Best Practices

### Client Implementation

1. **Parse all messages** - Type-check message types
2. **Handle all message types** - Don't assume message order
3. **Store state locally** - Don't rely solely on STATE_UPDATE
4. **Implement reconnection** - Handle network failures gracefully
5. **Queue commands** - Don't send multiple commands simultaneously

### Server Implementation

1. **Always send prompt** - After every command
2. **Always send state** - After state-changing commands
3. **Validate inputs** - Sanitize all command inputs
4. **Handle disconnects** - Clean up resources
5. **Rate limiting** - Prevent command flooding

## Security Considerations

1. **No authentication in messages** - Use WebSocket handshake for auth
2. **Validate all commands** - Server-side validation only
3. **Sanitize output** - Prevent XSS in terminal output
4. **Rate limiting** - Prevent DoS attacks
5. **Session timeout** - Expire inactive sessions

## Future Extensions

### Potential Additions

1. **Binary messages** - For file transfers
2. **Compression** - For large outputs
3. **Multiplayer** - Additional message types for P2P
4. **Chat** - In-game communication
5. **Achievements** - Achievement unlock notifications

### Version Negotiation

For future protocol changes:

```json
{
  "type": "connect",
  "payload": {
    "protocol_version": "1.0.0",
    "client_version": "1.0.0"
  }
}
```

## Testing Protocol

### Example Test Cases

```python
# Test command execution
await ws.send_json({
    "type": "command",
    "payload": {"command": "help"}
})
response = await ws.receive_json()
assert response["type"] == "output"
assert "help" in response["payload"]["text"]

# Test invalid command
await ws.send_json({
    "type": "command",
    "payload": {"command": "invalid"}
})
response = await ws.receive_json()
assert response["payload"]["style"] == "error"
```

### Mock Server Example

```python
async def mock_game_server(websocket):
    await websocket.send_json({
        "type": "system",
        "payload": {"message": "Welcome!", "level": "info"}
    })

    async for message in websocket:
        if message["type"] == "command":
            await websocket.send_json({
                "type": "output",
                "payload": {"text": "Mock output", "style": "normal"}
            })
```
