"""
Command Dispatcher
Routes commands to appropriate handlers
"""
from typing import Callable, Dict, Optional, List
from app.models.game_state import GameWorld
from app.models.protocol import OutputMessage


class CommandResult:
    """Result of command execution"""
    def __init__(self, output: List[OutputMessage], success: bool = True):
        self.output = output
        self.success = success


class Command:
    """Base command class"""
    def __init__(self, name: str, description: str, aliases: List[str] = None):
        self.name = name
        self.description = description
        self.aliases = aliases or []
    
    async def execute(self, world: GameWorld, args: List[str]) -> CommandResult:
        """Execute the command"""
        raise NotImplementedError


class CommandDispatcher:
    """Dispatches commands to handlers"""
    
    def __init__(self):
        self.commands: Dict[str, Command] = {}
        self._register_builtin_commands()
    
    def register(self, command: Command):
        """Register a command"""
        self.commands[command.name] = command
        for alias in command.aliases:
            self.commands[alias] = command
    
    def _register_builtin_commands(self):
        """Register all built-in commands"""
        from app.game.commands import (
            HelpCommand, LsCommand, CdCommand, PwdCommand,
            CatCommand, ScanCommand, ConnectCommand, CrackCommand,
            ExitCommand, ClearCommand
        )
        
        self.register(HelpCommand())
        self.register(LsCommand())
        self.register(CdCommand())
        self.register(PwdCommand())
        self.register(CatCommand())
        self.register(ScanCommand())
        self.register(ConnectCommand())
        self.register(CrackCommand())
        self.register(ExitCommand())
        self.register(ClearCommand())
    
    async def dispatch(self, command_name: str, args: List[str], world: GameWorld) -> CommandResult:
        """
        Dispatch command to appropriate handler
        
        Args:
            command_name: Command to execute
            args: Command arguments
            world: Current game world state
            
        Returns:
            CommandResult with output
        """
        command = self.commands.get(command_name)
        
        if not command:
            return CommandResult(
                output=[OutputMessage(
                    text=f"Command not found: {command_name}\nType 'help' for available commands.",
                    style="error"
                )],
                success=False
            )
        
        try:
            return await command.execute(world, args)
        except Exception as e:
            return CommandResult(
                output=[OutputMessage(
                    text=f"Error executing command: {str(e)}",
                    style="error"
                )],
                success=False
            )
    
    def get_help_text(self) -> str:
        """Get formatted help text for all commands"""
        unique_commands = {}
        for cmd in self.commands.values():
            if cmd.name not in unique_commands:
                unique_commands[cmd.name] = cmd
        
        help_lines = ["Available commands:\n"]
        for cmd in sorted(unique_commands.values(), key=lambda c: c.name):
            aliases = f" (aliases: {', '.join(cmd.aliases)})" if cmd.aliases else ""
            help_lines.append(f"  {cmd.name:<12} - {cmd.description}{aliases}")
        
        return "\n".join(help_lines)
