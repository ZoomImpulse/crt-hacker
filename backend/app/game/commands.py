"""
Game Commands Implementation
"""
from typing import List
from app.core.dispatcher import Command, CommandResult
from app.models.protocol import OutputMessage
from app.models.game_state import GameWorld, FileType


class HelpCommand(Command):
    """Display help information"""
    def __init__(self):
        super().__init__("help", "Display available commands", aliases=["?"])
    
    async def execute(self, world: GameWorld, args: List[str]) -> CommandResult:
        from app.core.dispatcher import CommandDispatcher
        dispatcher = CommandDispatcher()
        help_text = dispatcher.get_help_text()
        return CommandResult(output=[OutputMessage(text=help_text, style="info")])


class LsCommand(Command):
    """List directory contents"""
    def __init__(self):
        super().__init__("ls", "List directory contents", aliases=["dir"])
    
    async def execute(self, world: GameWorld, args: List[str]) -> CommandResult:
        current_host = world.hosts.get(world.player.current_host)
        if not current_host:
            return CommandResult(
                output=[OutputMessage(text="Error: Current host not found", style="error")],
                success=False
            )
        
        # Navigate to current path
        current_node = self._get_node(current_host.filesystem, world.player.current_path)
        if not current_node or current_node.type != FileType.DIRECTORY:
            return CommandResult(
                output=[OutputMessage(text="Error: Not a directory", style="error")],
                success=False
            )
        
        if not current_node.children:
            return CommandResult(output=[OutputMessage(text="", style="normal")])
        
        # Format output
        lines = []
        for name, node in sorted(current_node.children.items()):
            type_indicator = "/" if node.type == FileType.DIRECTORY else ""
            size_str = f"{node.size:>8}" if node.type == FileType.FILE else "     DIR"
            lines.append(f"{node.permissions}  {node.owner:<8}  {size_str}  {name}{type_indicator}")
        
        return CommandResult(output=[OutputMessage(text="\n".join(lines), style="normal")])
    
    def _get_node(self, root, path):
        """Navigate to path in filesystem"""
        if path == "/":
            return root
        
        parts = [p for p in path.split("/") if p]
        current = root
        
        for part in parts:
            if not current.children or part not in current.children:
                return None
            current = current.children[part]
        
        return current


class CdCommand(Command):
    """Change directory"""
    def __init__(self):
        super().__init__("cd", "Change directory")
    
    async def execute(self, world: GameWorld, args: List[str]) -> CommandResult:
        if not args:
            # Go to home
            world.player.current_path = "/home/user"
            return CommandResult(output=[])
        
        target = args[0]
        current_host = world.hosts.get(world.player.current_host)
        
        # Resolve path
        if target.startswith("/"):
            new_path = target
        elif target == "..":
            parts = world.player.current_path.rstrip("/").split("/")
            new_path = "/".join(parts[:-1]) or "/"
        elif target == ".":
            return CommandResult(output=[])
        else:
            new_path = f"{world.player.current_path.rstrip('/')}/{target}"
        
        # Validate path exists
        ls_cmd = LsCommand()
        node = ls_cmd._get_node(current_host.filesystem, new_path)
        if not node or node.type != FileType.DIRECTORY:
            return CommandResult(
                output=[OutputMessage(text=f"cd: {target}: No such directory", style="error")],
                success=False
            )
        
        world.player.current_path = new_path
        return CommandResult(output=[])


class PwdCommand(Command):
    """Print working directory"""
    def __init__(self):
        super().__init__("pwd", "Print current directory path")
    
    async def execute(self, world: GameWorld, args: List[str]) -> CommandResult:
        return CommandResult(
            output=[OutputMessage(text=world.player.current_path, style="normal")]
        )


class CatCommand(Command):
    """Display file contents"""
    def __init__(self):
        super().__init__("cat", "Display file contents")
    
    async def execute(self, world: GameWorld, args: List[str]) -> CommandResult:
        if not args:
            return CommandResult(
                output=[OutputMessage(text="cat: missing file operand", style="error")],
                success=False
            )
        
        filename = args[0]
        current_host = world.hosts.get(world.player.current_host)
        
        # Resolve path
        if filename.startswith("/"):
            filepath = filename
        else:
            filepath = f"{world.player.current_path.rstrip('/')}/{filename}"
        
        # Get file
        ls_cmd = LsCommand()
        node = ls_cmd._get_node(current_host.filesystem, filepath)
        
        if not node:
            return CommandResult(
                output=[OutputMessage(text=f"cat: {filename}: No such file", style="error")],
                success=False
            )
        
        if node.type != FileType.FILE:
            return CommandResult(
                output=[OutputMessage(text=f"cat: {filename}: Is a directory", style="error")],
                success=False
            )
        
        content = node.content or ""
        return CommandResult(output=[OutputMessage(text=content, style="normal")])


class ScanCommand(Command):
    """Scan network for hosts"""
    def __init__(self):
        super().__init__("scan", "Scan network for hosts and services")
    
    async def execute(self, world: GameWorld, args: List[str]) -> CommandResult:
        lines = ["Scanning network...\n"]
        
        for hostname, host in world.hosts.items():
            if hostname == "localhost":
                continue
            
            lines.append(f"\nHost: {hostname} ({host.ip})")
            lines.append(f"Status: {'COMPROMISED' if host.compromised else 'ACTIVE'}")
            
            if host.services:
                lines.append("Open ports:")
                for svc in host.services:
                    banner = f" - {svc.banner}" if svc.banner else ""
                    lines.append(f"  {svc.port:>5}/tcp  {svc.name:<10}  {svc.status.value}{banner}")
        
        return CommandResult(output=[OutputMessage(text="\n".join(lines), style="success")])


class ConnectCommand(Command):
    """Connect to remote host"""
    def __init__(self):
        super().__init__("connect", "Connect to a remote host", aliases=["ssh"])
    
    async def execute(self, world: GameWorld, args: List[str]) -> CommandResult:
        if not args:
            return CommandResult(
                output=[OutputMessage(text="Usage: connect <hostname>", style="error")],
                success=False
            )
        
        hostname = args[0]
        target_host = world.hosts.get(hostname)
        
        if not target_host:
            return CommandResult(
                output=[OutputMessage(text=f"Host not found: {hostname}", style="error")],
                success=False
            )
        
        if not target_host.compromised:
            return CommandResult(
                output=[OutputMessage(text=f"Access denied. Try cracking the password first.", style="error")],
                success=False
            )
        
        world.player.current_host = hostname
        world.player.current_path = "/"
        
        return CommandResult(
            output=[OutputMessage(text=f"Connected to {hostname}", style="success")]
        )


class CrackCommand(Command):
    """Attempt to crack password"""
    def __init__(self):
        super().__init__("crack", "Attempt to crack a service password")
    
    async def execute(self, world: GameWorld, args: List[str]) -> CommandResult:
        if not args:
            return CommandResult(
                output=[OutputMessage(text="Usage: crack <hostname> [port]", style="error")],
                success=False
            )
        
        hostname = args[0]
        port = int(args[1]) if len(args) > 1 else 22
        
        target_host = world.hosts.get(hostname)
        if not target_host:
            return CommandResult(
                output=[OutputMessage(text=f"Host not found: {hostname}", style="error")],
                success=False
            )
        
        # Find service
        service = next((s for s in target_host.services if s.port == port), None)
        if not service or service.status != "open":
            return CommandResult(
                output=[OutputMessage(text=f"No open service on port {port}", style="error")],
                success=False
            )
        
        if not service.vulnerability:
            return CommandResult(
                output=[OutputMessage(text="No known vulnerability", style="error")],
                success=False
            )
        
        # Simple puzzle: always succeeds for now
        target_host.compromised = True
        world.player.hosts_compromised.append(hostname)
        world.player.score += 100
        
        return CommandResult(
            output=[OutputMessage(text=f"Successfully exploited {service.name} on {hostname}!\nAccess granted. +100 points", style="success")]
        )


class ExitCommand(Command):
    """Exit the game"""
    def __init__(self):
        super().__init__("exit", "Exit the game", aliases=["quit", "logout"])
    
    async def execute(self, world: GameWorld, args: List[str]) -> CommandResult:
        return CommandResult(
            output=[OutputMessage(text="Goodbye!", style="info")]
        )


class ClearCommand(Command):
    """Clear terminal screen"""
    def __init__(self):
        super().__init__("clear", "Clear the terminal screen", aliases=["cls"])
    
    async def execute(self, world: GameWorld, args: List[str]) -> CommandResult:
        return CommandResult(
            output=[OutputMessage(text="\x1b[2J\x1b[H", style="normal")]
        )
