"""
WebSocket Protocol Types and Message Definitions
Shared between client and server
"""
from enum import Enum
from typing import Any, Optional, Dict, List
from pydantic import BaseModel


class MessageType(str, Enum):
    """WebSocket message types"""
    # Client -> Server
    COMMAND = "command"
    CONNECT = "connect"
    DISCONNECT = "disconnect"
    
    # Server -> Client
    OUTPUT = "output"
    ERROR = "error"
    STATE_UPDATE = "state_update"
    PROMPT = "prompt"
    SYSTEM = "system"


class WSMessage(BaseModel):
    """Base WebSocket message structure"""
    type: MessageType
    payload: Dict[str, Any]
    timestamp: Optional[float] = None


class CommandMessage(BaseModel):
    """Command input from client"""
    command: str
    args: List[str] = []


class OutputMessage(BaseModel):
    """Terminal output to client"""
    text: str
    style: Optional[str] = "normal"  # normal, success, error, warning, info


class ErrorMessage(BaseModel):
    """Error message"""
    error: str
    code: Optional[str] = None


class StateUpdateMessage(BaseModel):
    """Game state update"""
    current_host: str
    current_path: str
    user: str
    level: int
    score: int


class PromptMessage(BaseModel):
    """Terminal prompt update"""
    prompt: str


class SystemMessage(BaseModel):
    """System notification"""
    message: str
    level: str = "info"  # info, warning, critical
