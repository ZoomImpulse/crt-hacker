"""
Example: Adding a New Command

This example demonstrates how to add a new command to the game.
We'll create a 'whoami' command that displays the current user.
"""

from typing import List
from app.core.dispatcher import Command, CommandResult
from app.models.protocol import OutputMessage
from app.models.game_state import GameWorld

class WhoamiCommand(Command):
"""Display current user"""

    def __init__(self):
        # Initialize with command name, description, and optional aliases
        super().__init__(
            name="whoami",
            description="Display current username",
            aliases=["who"]  # Optional alternative command names
        )

    async def execute(self, world: GameWorld, args: List[str]) -> CommandResult:
        """
        Execute the command

        Args:
            world: Current game world state
            args: Command arguments (unused for whoami)

        Returns:
            CommandResult with output
        """
        # Get username from player state
        username = world.player.username

        # Create output message
        output = OutputMessage(
            text=username,
            style="normal"
        )

        # Return result
        return CommandResult(
            output=[output],
            success=True
        )

# To register this command:

# 1. Import it in app/core/dispatcher.py

# 2. Add to \_register_builtin_commands():

# self.register(WhoamiCommand())

"""
Example: Creating a New Host

This example shows how to add a new host to the game world.
"""

from app.models.game_state import (
VirtualHost, VirtualFile, NetworkService,
FileType, ServiceStatus
)

def create_example_host():
"""Create a new host with filesystem and services"""

    # Create filesystem structure
    filesystem = VirtualFile(
        name="/",
        type=FileType.DIRECTORY,
        children={
            "home": VirtualFile(
                name="home",
                type=FileType.DIRECTORY,
                children={
                    "admin": VirtualFile(
                        name="admin",
                        type=FileType.DIRECTORY,
                        children={
                            "secret.txt": VirtualFile(
                                name="secret.txt",
                                type=FileType.FILE,
                                content="FLAG{example_flag}",
                                size=20,
                                permissions="r--------",
                                owner="admin"
                            )
                        }
                    )
                }
            ),
            "var": VirtualFile(
                name="var",
                type=FileType.DIRECTORY,
                children={
                    "log": VirtualFile(
                        name="log",
                        type=FileType.DIRECTORY,
                        children={
                            "access.log": VirtualFile(
                                name="access.log",
                                type=FileType.FILE,
                                content="[2024-01-01] User login: admin\n",
                                size=32
                            )
                        }
                    )
                }
            )
        }
    )

    # Create network services
    services = [
        NetworkService(
            port=22,
            name="ssh",
            status=ServiceStatus.OPEN,
            banner="OpenSSH 8.0",
            vulnerability="weak_password"
        ),
        NetworkService(
            port=3306,
            name="mysql",
            status=ServiceStatus.OPEN,
            banner="MySQL 5.7",
            vulnerability="default_credentials"
        )
    ]

    # Create host
    host = VirtualHost(
        hostname="example-host",
        ip="192.168.1.100",
        services=services,
        filesystem=filesystem,
        compromised=False,
        difficulty=2
    )

    return host

# To add this host to the game:

# In app/core/engine.py, in \_create_initial_world():

# world.hosts["example-host"] = create_example_host()

"""
Example: Custom WebSocket Message Handler

This example shows how to handle custom client messages.
"""

from app.models.protocol import MessageType, WSMessage
from app.api.websocket import manager

async def handle_custom_message(session_id: str, message: WSMessage):
"""Handle a custom message type"""

    if message.type == "custom_action":
        # Process custom action
        action = message.payload.get("action")

        if action == "save_game":
            # Implement save logic
            response = WSMessage(
                type=MessageType.SYSTEM,
                payload={
                    "message": "Game saved successfully!",
                    "level": "info"
                },
                timestamp=time.time()
            )
            await manager.send_message(session_id, response)

"""
Example: Adding a New Vulnerability Type

This example demonstrates creating a custom vulnerability puzzle.
"""

from app.core.parser import CommandParser

class SqlInjectionPuzzle:
"""SQL Injection puzzle implementation"""

    def __init__(self, target_host: VirtualHost):
        self.target = target_host
        self.attempts = 0
        self.max_attempts = 3

    def attempt_exploit(self, payload: str) -> tuple[bool, str]:
        """
        Attempt SQL injection

        Args:
            payload: User's injection attempt

        Returns:
            Tuple of (success, message)
        """
        self.attempts += 1

        # Check for correct payload
        correct_payloads = [
            "' OR '1'='1",
            "' OR 1=1--",
            "admin' --"
        ]

        if payload in correct_payloads:
            self.target.compromised = True
            return True, "SQL Injection successful! Access granted."

        if self.attempts >= self.max_attempts:
            return False, "Too many failed attempts. WAF activated."

        return False, f"Injection failed. Attempts remaining: {self.max_attempts - self.attempts}"

# To integrate into a command:

# In your exploit command, check vulnerability type:

# if service.vulnerability == "sql_injection":

# puzzle = SqlInjectionPuzzle(target_host)

# success, msg = puzzle.attempt_exploit(args[0])

"""
Example: Frontend Message Handler

This example shows how to handle custom messages in the frontend.
"""

# In src/hooks/useWebSocket.ts:

"""
const unsubscribe = ws.onMessage((message) => {
// Handle custom message type
if (message.type === 'achievement_unlocked') {
const achievement = message.payload;
showNotification(`Achievement: ${achievement.name}`);
}

// Store message for display
setMessages(prev => [...prev, message]);
});
"""

"""
Example: Adding Custom Terminal Styles

This example shows how to add new output styles.
"""

# 1. In backend/app/models/protocol.py, update OutputMessage:

"""
class OutputMessage(BaseModel):
text: str
style: Optional[str] = "normal" # Add new styles: 'highlight', 'dim', etc.
"""

# 2. In frontend/src/styles/Terminal.css, add style:

"""
.terminal-line.highlight {
color: #ffff00;
background: rgba(255, 255, 0, 0.1);
text-shadow: 0 0 10px #ffff00;
font-weight: bold;
}
"""

# 3. In frontend/src/components/Terminal.tsx, renderMessage handles it automatically

"""
Example: Creating a Multi-Stage Puzzle

This example shows a puzzle requiring multiple steps.
"""

class MultiStagePuzzle:
"""A puzzle with multiple sequential stages"""

    def __init__(self):
        self.stage = 0
        self.stages = [
            {
                "hint": "Find the password in /etc/passwd.bak",
                "required_action": "cat /etc/passwd.bak",
                "reward": "password: hunter2"
            },
            {
                "hint": "Use the password to decrypt /home/user/encrypted.txt",
                "required_action": "decrypt /home/user/encrypted.txt hunter2",
                "reward": "Private key obtained"
            },
            {
                "hint": "Use the private key to connect to admin server",
                "required_action": "connect admin-server --key private.key",
                "reward": "FLAG{multi_stage_complete}"
            }
        ]

    def check_action(self, action: str) -> tuple[bool, str]:
        """Check if action advances the puzzle"""
        current = self.stages[self.stage]

        if current["required_action"] in action:
            reward = current["reward"]
            self.stage += 1

            if self.stage >= len(self.stages):
                return True, f"Puzzle complete! {reward}"
            else:
                next_hint = self.stages[self.stage]["hint"]
                return False, f"{reward}\n\nNext: {next_hint}"

        return False, current["hint"]
