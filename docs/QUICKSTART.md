# Quick Start Guide

## Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- npm or yarn

## Installation

### 1. Clone Repository

```bash
git clone <repository-url>
cd crt-hacker
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows CMD:
.\venv\Scripts\activate.bat
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
copy .env.example .env
```

### 3. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install
```

## Running the Application

### Terminal 1: Start Backend

```bash
cd backend
.\venv\Scripts\Activate.ps1  # Or your platform's activation command
python main.py
```

Backend will run on `http://localhost:8000`

### Terminal 2: Start Frontend

```bash
cd frontend
npm run dev
```

Frontend will run on `http://localhost:5173`

### Access the Game

Open your browser and navigate to:

```
http://localhost:5173
```

## First Steps in the Game

### Basic Commands

1. **Get Help**

   ```
   help
   ```

2. **List Files**

   ```
   ls
   ```

3. **Read a File**

   ```
   cat readme.txt
   ```

4. **Scan Network**

   ```
   scan --local
   ```

5. **Crack a Host**

   ```
   crack target-01 22
   ```

6. **Connect to Host**

   ```
   connect target-01
   ```

7. **Find Flag**
   ```
   cd /var
   cat flag.txt
   ```

### Keyboard Shortcuts

- **Up/Down Arrows** - Navigate command history
- **Ctrl+L** - Clear screen
- **Tab** - Auto-complete (coming soon)

## Project Structure

```
crt-hacker/
├── backend/              # Python FastAPI backend
│   ├── app/
│   │   ├── api/         # WebSocket endpoints
│   │   ├── core/        # Game engine
│   │   ├── game/        # Commands & game logic
│   │   └── models/      # Data models
│   └── main.py          # Entry point
│
├── frontend/            # TypeScript React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── hooks/       # Custom hooks
│   │   ├── services/    # WebSocket client
│   │   ├── styles/      # CSS
│   │   └── types/       # TypeScript types
│   └── index.html
│
└── docs/                # Documentation
    ├── BACKEND.md
    ├── FRONTEND.md
    ├── PROTOCOL.md
    └── GAME_DESIGN.md
```

## Troubleshooting

### Backend Issues

**Issue:** `ModuleNotFoundError`

```bash
# Ensure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

**Issue:** `Port 8000 already in use`

```bash
# Change port in main.py:
uvicorn.run("main:app", host="0.0.0.0", port=8001)
```

**Issue:** Database errors

```bash
# Delete database and restart
del game.db
python main.py
```

### Frontend Issues

**Issue:** `Cannot connect to WebSocket`

- Ensure backend is running on port 8000
- Check browser console for errors
- Verify WebSocket URL in `src/App.tsx`

**Issue:** `npm install fails`

```bash
# Clear cache and retry
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

**Issue:** Blank screen

- Check browser console for errors
- Ensure backend is running and accessible
- Try hard refresh (Ctrl+Shift+R)

### Common Problems

**WebSocket disconnects immediately**

- Check CORS settings in backend
- Verify WebSocket endpoint URL
- Check browser's network tab for errors

**Terminal not responding**

- Click inside terminal to focus
- Check connection status in status bar
- Refresh page if needed

## Development Mode

### Backend Hot Reload

The backend automatically reloads on code changes when using:

```bash
python main.py  # Uses uvicorn with reload=True
```

### Frontend Hot Reload

Vite provides instant hot module replacement:

```bash
npm run dev
```

## Building for Production

### Backend

```bash
cd backend
pip install -r requirements.txt

# Run with production settings
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Frontend

```bash
cd frontend
npm run build
```

Output in `frontend/dist/` directory.

Serve with:

```bash
npm run preview
# Or use any static file server
```

## Testing

### Backend Tests

```bash
cd backend
pytest tests/
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Next Steps

1. Read [GAME_DESIGN.md](docs/GAME_DESIGN.md) for gameplay mechanics
2. Read [BACKEND.md](docs/BACKEND.md) for backend architecture
3. Read [FRONTEND.md](docs/FRONTEND.md) for frontend architecture
4. Read [PROTOCOL.md](docs/PROTOCOL.md) for WebSocket protocol

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

See [LICENSE](LICENSE) for details.
