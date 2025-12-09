"""
Game State Models
"""
from typing import Dict, List, Optional, Any
from pydantic import BaseModel
from enum import Enum


class GameLevel(int, Enum):
    """Player progression levels"""
    NOVICE = 1
    SCRIPT_KIDDIE = 2
    HACKER = 3
    ELITE = 4
    ADMIN = 5


class FileType(str, Enum):
    """Virtual filesystem types"""
    FILE = "file"
    DIRECTORY = "directory"
    LINK = "link"


class ServiceStatus(str, Enum):
    """Network service status"""
    OPEN = "open"
    CLOSED = "closed"
    FILTERED = "filtered"


class VirtualFile(BaseModel):
    """Virtual filesystem node"""
    name: str
    type: FileType
    content: Optional[str] = None
    size: int = 0
    permissions: str = "rw-r--r--"
    owner: str = "root"
    children: Optional[Dict[str, 'VirtualFile']] = None


class NetworkService(BaseModel):
    """Simulated network service"""
    port: int
    name: str
    status: ServiceStatus
    banner: Optional[str] = None
    vulnerability: Optional[str] = None


class VirtualHost(BaseModel):
    """Simulated network host"""
    hostname: str
    ip: str
    services: List[NetworkService]
    filesystem: VirtualFile
    compromised: bool = False
    difficulty: int = 1


class PlayerState(BaseModel):
    """Player game state"""
    session_id: str
    username: str
    level: GameLevel = GameLevel.NOVICE
    score: int = 0
    current_host: str = "localhost"
    current_path: str = "/home/user"
    inventory: List[str] = []
    flags_collected: List[str] = []
    hosts_compromised: List[str] = []
    command_history: List[str] = []


class GameWorld(BaseModel):
    """Complete game world state"""
    hosts: Dict[str, VirtualHost]
    player: PlayerState
    objectives: List[str]
    hints: Dict[str, str]
