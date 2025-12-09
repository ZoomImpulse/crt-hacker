# CRT Hacker - Terminal-Based Hacking Game

A retro-styled, web-based hacker terminal game with full command-line interface and CRT aesthetics.

![Status](https://img.shields.io/badge/status-ready-green)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![TypeScript](https://img.shields.io/badge/typescript-5.2+-blue)
![License](https://img.shields.io/badge/license-MIT-blue)

## 🎮 Quick Start

```bash
# Terminal 1: Backend
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py

# Terminal 2: Frontend
cd frontend
npm install
npm run dev
```

Visit: **http://localhost:5173**

## ✨ Features

- 🖥️ **Full CRT Terminal Experience** - Scanlines, phosphor glow, screen curvature
- ⚡ **Real-time WebSocket Communication** - Instant command execution
- 🎯 **Deterministic Game Logic** - No AI, pure algorithmic challenges
- 🗂️ **Virtual Filesystem** - Navigate Unix-like directory structure
- 🌐 **Network Simulation** - Scan hosts, exploit vulnerabilities
- 💾 **State Persistence** - SQLite-backed save system
- 🎚️ **Progressive Difficulty** - From novice to elite hacker
- 📊 **Score & Achievements** - Track your progress

## 🎯 Game Commands

```bash
help              # Display available commands
ls                # List directory contents
cd <path>         # Change directory
cat <file>        # Display file contents
scan --local      # Scan local network
crack <host>      # Exploit vulnerability
connect <host>    # SSH to remote host
clear             # Clear terminal screen
```

## 🏗️ Tech Stack

### Frontend
- **TypeScript** - Type-safe frontend code
- **React 18** - Modern UI library
- **Vite** - Lightning-fast build tool
- **Custom CSS** - Pure CSS CRT effects

### Backend
- **Python 3.11+** - Modern async Python
- **FastAPI** - High-performance web framework
- **WebSockets** - Real-time bidirectional communication
- **SQLite** - Embedded database
- **Pydantic** - Data validation

## 📁 Project Structure

```
crt-hacker/
├── backend/              # Python FastAPI backend
│   ├── app/
│   │   ├── api/         # WebSocket endpoints
│   │   ├── core/        # Game engine, parser, dispatcher
│   │   ├── game/        # Command implementations
│   │   └── models/      # Data models & protocol
│   └── main.py          # Application entry point
│
├── frontend/            # TypeScript React frontend
│   ├── src/
│   │   ├── components/  # Terminal & StatusBar
│   │   ├── hooks/       # useWebSocket
│   │   ├── services/    # WebSocket client
│   │   ├── styles/      # CRT CSS effects
│   │   └── types/       # Protocol types
│   └── index.html
│
└── docs/                # Comprehensive documentation
    ├── QUICKSTART.md    # 5-minute setup guide
    ├── ARCHITECTURE.md  # System design
    ├── BACKEND.md       # Backend internals
    ├── FRONTEND.md      # Frontend architecture
    ├── PROTOCOL.md      # WebSocket protocol
    ├── GAME_DESIGN.md   # Game mechanics
    └── EXAMPLES.md      # Code examples
```

## 📚 Documentation

- **[Quick Start Guide](docs/QUICKSTART.md)** - Get up and running in 5 minutes
- **[Architecture Overview](docs/ARCHITECTURE.md)** - System design and data flow
- **[Backend Documentation](docs/BACKEND.md)** - API and game engine internals
- **[Frontend Documentation](docs/FRONTEND.md)** - Component architecture and state management
- **[WebSocket Protocol](docs/PROTOCOL.md)** - Message format specification
- **[Game Design](docs/GAME_DESIGN.md)** - Gameplay mechanics and puzzles
- **[Code Examples](docs/EXAMPLES.md)** - How to extend the game

## 🎮 Gameplay

### Starting Out
1. Type `help` to see available commands
2. Read `readme.txt` with `cat readme.txt`
3. Scan the network with `scan --local`
4. Find a target host
5. Exploit it with `crack target-01 22`
6. Connect with `connect target-01`
7. Find the flag!

### Game World
- **Localhost** - Your starting system
- **Target Hosts** - Systems to compromise
- **Virtual Services** - SSH, HTTP, MySQL, etc.
- **Flags** - Hidden rewards to collect
- **Scoring** - Earn points for discoveries and exploits

## 🔧 Extending the Game

### Add a New Command

```python
# backend/app/game/commands.py
class MyCommand(Command):
    def __init__(self):
        super().__init__("mycommand", "Description")
    
    async def execute(self, world: GameWorld, args: List[str]) -> CommandResult:
        return CommandResult(output=[OutputMessage(text="Hello!")])
```

### Add a New Host

```python
# backend/app/core/engine.py
new_host = VirtualHost(
    hostname="newhost",
    ip="192.168.1.100",
    services=[...],
    filesystem=create_filesystem(),
    difficulty=2
)
world.hosts["newhost"] = new_host
```

See **[EXAMPLES.md](docs/EXAMPLES.md)** for more details.

## 🚀 Production Deployment

```bash
# Backend
cd backend
pip install -r requirements.txt
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app

# Frontend
cd frontend
npm run build
# Serve dist/ with nginx or any static server
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/

# Frontend tests
cd frontend
npm test
```

## 🤝 Contributing

Contributions welcome! Please read the contributing guidelines first.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🎯 Roadmap

- [ ] Additional commands (grep, find, nmap)
- [ ] More host types and vulnerabilities
- [ ] User authentication system
- [ ] Multiplayer leaderboards
- [ ] Achievement system
- [ ] Mobile responsive design
- [ ] Save/load game slots
- [ ] Custom campaigns

## 🐛 Known Issues

None currently! Report issues on GitHub.

## 📞 Support

- **Documentation**: See `docs/` directory
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions

## 🙏 Acknowledgments

- Inspired by classic hacking games
- Built with modern web technologies
- CRT shader effects inspired by retro computing

---

**Made with 💚 for terminal enthusiasts and hacker wannabes**

Star ⭐ this repo if you like it!
