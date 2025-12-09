"""
Database initialization and models
"""
import aiosqlite
from pathlib import Path
from typing import Optional


DATABASE_PATH = Path(__file__).parent.parent.parent / "game.db"


async def init_db():
    """Initialize database schema"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS game_saves (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER NOT NULL,
                save_name TEXT NOT NULL,
                game_state TEXT NOT NULL,
                saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (player_id) REFERENCES players(id)
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                player_id INTEGER,
                game_state TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (player_id) REFERENCES players(id)
            )
        """)
        
        await db.commit()


async def save_game_state(session_id: str, game_state: str):
    """Save game state for a session"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            """INSERT OR REPLACE INTO sessions (session_id, game_state, last_activity)
               VALUES (?, ?, CURRENT_TIMESTAMP)""",
            (session_id, game_state)
        )
        await db.commit()


async def load_game_state(session_id: str) -> Optional[str]:
    """Load game state for a session"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT game_state FROM sessions WHERE session_id = ?",
            (session_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None
