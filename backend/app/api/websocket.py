"""
WebSocket API Handler
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict
import json
import time

from app.models.protocol import (
    MessageType, WSMessage, CommandMessage, OutputMessage,
    StateUpdateMessage, PromptMessage, SystemMessage
)
from app.core.engine import GameEngine


router = APIRouter()
game_engine = GameEngine()


class ConnectionManager:
    """Manage WebSocket connections"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, session_id: str, websocket: WebSocket):
        """Accept and store connection"""
        await websocket.accept()
        self.active_connections[session_id] = websocket
    
    def disconnect(self, session_id: str):
        """Remove connection"""
        if session_id in self.active_connections:
            del self.active_connections[session_id]
    
    async def send_message(self, session_id: str, message: WSMessage):
        """Send message to client"""
        websocket = self.active_connections.get(session_id)
        if websocket:
            await websocket.send_text(message.model_dump_json())


manager = ConnectionManager()


@router.websocket("/game")
async def game_websocket(websocket: WebSocket):
    """Main game WebSocket endpoint"""
    session_id = None
    
    try:
        # Create session
        session_id = game_engine.create_session()
        await manager.connect(session_id, websocket)
        
        # Send welcome message
        welcome_msg = WSMessage(
            type=MessageType.SYSTEM,
            payload=SystemMessage(
                message="=== CRT HACKER TERMINAL v1.0 ===\nType 'help' for available commands.",
                level="info"
            ).model_dump(),
            timestamp=time.time()
        )
        await manager.send_message(session_id, welcome_msg)
        
        # Send initial prompt
        prompt_msg = WSMessage(
            type=MessageType.PROMPT,
            payload=PromptMessage(
                prompt=game_engine.get_prompt(session_id)
            ).model_dump(),
            timestamp=time.time()
        )
        await manager.send_message(session_id, prompt_msg)
        
        # Send initial state
        world = game_engine.get_world(session_id)
        state_msg = WSMessage(
            type=MessageType.STATE_UPDATE,
            payload=StateUpdateMessage(
                current_host=world.player.current_host,
                current_path=world.player.current_path,
                user=world.player.username,
                level=world.player.level,
                score=world.player.score
            ).model_dump(),
            timestamp=time.time()
        )
        await manager.send_message(session_id, state_msg)
        
        # Main message loop
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = WSMessage.model_validate_json(data)
            
            if message.type == MessageType.COMMAND:
                # Process command
                cmd_msg = CommandMessage(**message.payload)
                result = await game_engine.process_command(session_id, cmd_msg.command)
                
                # Send output
                for output in result.output:
                    output_msg = WSMessage(
                        type=MessageType.OUTPUT,
                        payload=output.model_dump(),
                        timestamp=time.time()
                    )
                    await manager.send_message(session_id, output_msg)
                
                # Send updated prompt
                prompt_msg = WSMessage(
                    type=MessageType.PROMPT,
                    payload=PromptMessage(
                        prompt=game_engine.get_prompt(session_id)
                    ).model_dump(),
                    timestamp=time.time()
                )
                await manager.send_message(session_id, prompt_msg)
                
                # Send updated state
                world = game_engine.get_world(session_id)
                if world:
                    state_msg = WSMessage(
                        type=MessageType.STATE_UPDATE,
                        payload=StateUpdateMessage(
                            current_host=world.player.current_host,
                            current_path=world.player.current_path,
                            user=world.player.username,
                            level=world.player.level,
                            score=world.player.score
                        ).model_dump(),
                        timestamp=time.time()
                    )
                    await manager.send_message(session_id, state_msg)
            
            elif message.type == MessageType.DISCONNECT:
                break
    
    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        if session_id:
            manager.disconnect(session_id)
