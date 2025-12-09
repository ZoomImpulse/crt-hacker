# CRT Hacker - Terminal-Based Hacking Game

A retro-styled, web-based hacker terminal game with full command-line interface and CRT aesthetics.

## Tech Stack

### Frontend

- TypeScript
- Vite + React
- xterm.js for terminal emulation
- Custom CRT shader effects

### Backend

- Python 3.11+
- FastAPI
- WebSocket communication
- SQLite for persistence
- Redis (optional) for session state

## Project Structure

```
crt-hacker/
├── backend/              # Python FastAPI backend
│   ├── app/
│   │   ├── core/        # Game engine, state machine
│   │   ├── models/      # Data models
│   │   ├── services/    # Business logic
│   │   ├── api/         # WebSocket handlers
│   │   └── game/        # Game world components
│   ├── tests/
│   └── main.py
├── frontend/            # TypeScript React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── hooks/       # Custom hooks
│   │   ├── services/    # WebSocket client
│   │   ├── types/       # TypeScript types
│   │   └── styles/      # CRT effects CSS
│   └── index.html
└── shared/              # Shared protocol definitions
```

## Getting Started

### Backend Setup

```bash
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Game Features

- Virtual filesystem navigation
- Network discovery and scanning
- Password cracking puzzles
- Port scanning simulation
- Multi-level progression system
- Save/load game state

## Architecture

- **Deterministic**: All game logic runs server-side
- **Command-driven**: Text-based command interface
- **Stateful**: Server maintains complete game state
- **Real-time**: WebSocket bidirectional communication
