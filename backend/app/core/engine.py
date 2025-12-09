"""
Game Engine
Core game logic and state management
"""
import uuid
import json
from typing import Dict, Optional
from app.models.game_state import (
    GameWorld, PlayerState, VirtualHost, VirtualFile,
    NetworkService, FileType, ServiceStatus, GameLevel
)
from app.core.parser import CommandParser
from app.core.dispatcher import CommandDispatcher, CommandResult
from app.core.database import save_game_state, load_game_state


class GameEngine:
    """Main game engine managing world state and logic"""
    
    def __init__(self):
        self.parser = CommandParser()
        self.dispatcher = CommandDispatcher()
        self.worlds: Dict[str, GameWorld] = {}
    
    def create_session(self, username: str = "anonymous") -> str:
        """Create a new game session"""
        session_id = str(uuid.uuid4())
        world = self._create_initial_world(session_id, username)
        self.worlds[session_id] = world
        return session_id
    
    def get_world(self, session_id: str) -> Optional[GameWorld]:
        """Get game world for session"""
        return self.worlds.get(session_id)
    
    async def process_command(self, session_id: str, command_line: str) -> CommandResult:
        """
        Process a command for a session
        
        Args:
            session_id: Session identifier
            command_line: Raw command input
            
        Returns:
            CommandResult with output
        """
        world = self.get_world(session_id)
        if not world:
            from app.models.protocol import OutputMessage
            return CommandResult(
                output=[OutputMessage(text="Session not found", style="error")],
                success=False
            )
        
        # Parse command
        command, args = self.parser.parse(command_line)
        
        if not command:
            from app.models.protocol import OutputMessage
            return CommandResult(output=[], success=True)
        
        # Add to history
        world.player.command_history.append(command_line)
        
        # Dispatch command
        result = await self.dispatcher.dispatch(command, args, world)
        
        # Auto-save after each command
        await self._save_world(session_id, world)
        
        return result
    
    async def _save_world(self, session_id: str, world: GameWorld):
        """Persist game world state"""
        world_json = world.model_dump_json()
        await save_game_state(session_id, world_json)
    
    async def load_session(self, session_id: str) -> bool:
        """Load a saved session"""
        world_json = await load_game_state(session_id)
        if world_json:
            world = GameWorld.model_validate_json(world_json)
            self.worlds[session_id] = world
            return True
        return False
    
    def _create_initial_world(self, session_id: str, username: str) -> GameWorld:
        """Create initial game world"""
        # Create localhost
        localhost_fs = VirtualFile(
            name="/",
            type=FileType.DIRECTORY,
            children={
                "home": VirtualFile(
                    name="home",
                    type=FileType.DIRECTORY,
                    children={
                        "user": VirtualFile(
                            name="user",
                            type=FileType.DIRECTORY,
                            children={
                                "readme.txt": VirtualFile(
                                    name="readme.txt",
                                    type=FileType.FILE,
                                    content="Welcome to CRT Hacker!\n\nYour mission: Explore the network, find vulnerabilities, and collect flags.\n\nStart by scanning the network: scan --local\n",
                                    size=150
                                ),
                                "tools": VirtualFile(
                                    name="tools",
                                    type=FileType.DIRECTORY,
                                    children={}
                                )
                            }
                        )
                    }
                ),
                "etc": VirtualFile(
                    name="etc",
                    type=FileType.DIRECTORY,
                    children={
                        "hosts": VirtualFile(
                            name="hosts",
                            type=FileType.FILE,
                            content="127.0.0.1 localhost\n192.168.1.1 router\n192.168.1.10 target-01\n",
                            size=64
                        )
                    }
                )
            }
        )
        
        localhost = VirtualHost(
            hostname="localhost",
            ip="127.0.0.1",
            services=[],
            filesystem=localhost_fs,
            compromised=True,
            difficulty=0
        )
        
        # Create target host
        target_fs = VirtualFile(
            name="/",
            type=FileType.DIRECTORY,
            children={
                "var": VirtualFile(
                    name="var",
                    type=FileType.DIRECTORY,
                    children={
                        "flag.txt": VirtualFile(
                            name="flag.txt",
                            type=FileType.FILE,
                            content="FLAG{welcome_to_the_game}",
                            size=26,
                            permissions="r--------",
                            owner="admin"
                        )
                    }
                )
            }
        )
        
        target = VirtualHost(
            hostname="target-01",
            ip="192.168.1.10",
            services=[
                NetworkService(
                    port=22,
                    name="ssh",
                    status=ServiceStatus.OPEN,
                    banner="OpenSSH 7.4",
                    vulnerability="weak_password"
                ),
                NetworkService(
                    port=80,
                    name="http",
                    status=ServiceStatus.OPEN,
                    banner="Apache 2.4.29"
                )
            ],
            filesystem=target_fs,
            difficulty=1
        )
        
        # Create player state
        player = PlayerState(
            session_id=session_id,
            username=username,
            level=GameLevel.NOVICE,
            score=0,
            current_host="localhost",
            current_path="/home/user"
        )
        
        # Create world
        world = GameWorld(
            hosts={
                "localhost": localhost,
                "target-01": target
            },
            player=player,
            objectives=[
                "Scan the network to discover hosts",
                "Find and exploit a vulnerability",
                "Capture the flag"
            ],
            hints={
                "scan": "Use 'scan --local' to discover hosts on the network",
                "ssh": "Try connecting with 'connect <hostname>' once you find a target"
            }
        )
        
        return world
    
    def get_prompt(self, session_id: str) -> str:
        """Generate terminal prompt for session"""
        world = self.get_world(session_id)
        if not world:
            return "$ "
        
        user = world.player.username
        host = world.player.current_host
        path = world.player.current_path
        
        # Shorten path if in home directory
        if path.startswith("/home/user"):
            path = "~" + path[10:]
        
        return f"{user}@{host}:{path}$ "
