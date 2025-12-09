"""
Database - Simple file-based save system (no async DB needed for terminal version)
"""
import json
from pathlib import Path
from typing import Optional


SAVE_DIR = Path(__file__).parent.parent.parent / "saves"
SAVE_DIR.mkdir(exist_ok=True)


def init_db():
    """Initialize save directory"""
    SAVE_DIR.mkdir(exist_ok=True)


def save_game_state(session_id: str, game_state: str):
    """Save game state for a session"""
    save_file = SAVE_DIR / f"{session_id}.json"
    save_file.write_text(game_state)


def load_game_state(session_id: str) -> Optional[str]:
    """Load game state for a session"""
    save_file = SAVE_DIR / f"{session_id}.json"
    if save_file.exists():
        return save_file.read_text()
    return None
