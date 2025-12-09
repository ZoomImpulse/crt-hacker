#!/usr/bin/env python3
"""
CRT Hacker - Terminal-based Hacking Game
Main game loop with curses interface
"""
import curses
import asyncio
import sys
from typing import List, Optional
from backend.app.core.engine import GameEngine
from backend.app.models.protocol import OutputMessage


class TerminalRenderer:
    """Handles terminal rendering with curses"""
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.max_y, self.max_x = stdscr.getmaxyx()
        self.output_lines: List[str] = []
        self.scroll_offset = 0
        self.input_buffer = ""
        self.cursor_pos = 0
        self.history: List[str] = []
        self.history_index = -1
        
        # Initialize colors
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_GREEN, -1)    # normal text
        curses.init_pair(2, curses.COLOR_CYAN, -1)     # info
        curses.init_pair(3, curses.COLOR_RED, -1)      # error
        curses.init_pair(4, curses.COLOR_YELLOW, -1)   # warning
        curses.init_pair(5, curses.COLOR_MAGENTA, -1)  # prompt
        curses.init_pair(6, curses.COLOR_WHITE, -1)    # system
        
        # Setup cursor
        curses.curs_set(2)  # Block cursor
        self.stdscr.keypad(True)
        self.stdscr.nodelay(False)
        
    def get_color(self, style: str) -> int:
        """Get color pair for style"""
        color_map = {
            "normal": 1,
            "info": 2,
            "error": 3,
            "warning": 4,
            "success": 2,
            "system": 6,
        }
        return curses.color_pair(color_map.get(style, 1))
    
    def add_output(self, text: str, style: str = "normal"):
        """Add text to output buffer"""
        lines = text.split('\n')
        for line in lines:
            self.output_lines.append((line, style))
        
        # Auto-scroll to bottom
        self.scroll_to_bottom()
    
    def scroll_to_bottom(self):
        """Scroll to show latest output"""
        output_height = self.max_y - 2  # Reserve space for input line
        if len(self.output_lines) > output_height:
            self.scroll_offset = len(self.output_lines) - output_height
        else:
            self.scroll_offset = 0
    
    def clear_screen(self):
        """Clear all output"""
        self.output_lines = []
        self.scroll_offset = 0
        self.stdscr.clear()
    
    def render(self, prompt: str):
        """Render the entire screen"""
        self.max_y, self.max_x = self.stdscr.getmaxyx()
        self.stdscr.clear()
        
        # Render output lines
        output_height = self.max_y - 2
        visible_lines = self.output_lines[self.scroll_offset:self.scroll_offset + output_height]
        
        for idx, (line, style) in enumerate(visible_lines):
            if idx >= output_height:
                break
            try:
                # Truncate line if too long
                display_line = line[:self.max_x - 1]
                self.stdscr.addstr(idx, 0, display_line, self.get_color(style))
            except curses.error:
                pass  # Ignore errors from writing to last cell
        
        # Render input line at bottom
        input_y = self.max_y - 1
        try:
            # Draw prompt
            self.stdscr.addstr(input_y, 0, prompt, curses.color_pair(5) | curses.A_BOLD)
            prompt_len = len(prompt)
            
            # Draw input
            display_input = self.input_buffer[:self.max_x - prompt_len - 1]
            self.stdscr.addstr(input_y, prompt_len, display_input, curses.color_pair(1))
            
            # Position cursor
            cursor_x = min(prompt_len + self.cursor_pos, self.max_x - 1)
            self.stdscr.move(input_y, cursor_x)
        except curses.error:
            pass
        
        self.stdscr.refresh()
    
    def handle_input(self, key) -> Optional[str]:
        """
        Handle keyboard input
        Returns command string if Enter was pressed, None otherwise
        """
        if key == curses.KEY_ENTER or key == ord('\n'):
            # Submit command
            command = self.input_buffer
            if command.strip():
                self.history.append(command)
                self.history_index = -1
            self.input_buffer = ""
            self.cursor_pos = 0
            return command
        
        elif key == curses.KEY_BACKSPACE or key == 127 or key == 8:
            # Backspace
            if self.cursor_pos > 0:
                self.input_buffer = (
                    self.input_buffer[:self.cursor_pos - 1] + 
                    self.input_buffer[self.cursor_pos:]
                )
                self.cursor_pos -= 1
        
        elif key == curses.KEY_DC:
            # Delete key
            if self.cursor_pos < len(self.input_buffer):
                self.input_buffer = (
                    self.input_buffer[:self.cursor_pos] + 
                    self.input_buffer[self.cursor_pos + 1:]
                )
        
        elif key == curses.KEY_LEFT:
            self.cursor_pos = max(0, self.cursor_pos - 1)
        
        elif key == curses.KEY_RIGHT:
            self.cursor_pos = min(len(self.input_buffer), self.cursor_pos + 1)
        
        elif key == curses.KEY_HOME:
            self.cursor_pos = 0
        
        elif key == curses.KEY_END:
            self.cursor_pos = len(self.input_buffer)
        
        elif key == curses.KEY_UP:
            # History up
            if self.history and self.history_index < len(self.history) - 1:
                self.history_index += 1
                self.input_buffer = self.history[-(self.history_index + 1)]
                self.cursor_pos = len(self.input_buffer)
        
        elif key == curses.KEY_DOWN:
            # History down
            if self.history_index > 0:
                self.history_index -= 1
                self.input_buffer = self.history[-(self.history_index + 1)]
                self.cursor_pos = len(self.input_buffer)
            elif self.history_index == 0:
                self.history_index = -1
                self.input_buffer = ""
                self.cursor_pos = 0
        
        elif key == 12:  # Ctrl+L
            self.clear_screen()
        
        elif 32 <= key <= 126:  # Printable characters
            # Insert character at cursor position
            char = chr(key)
            self.input_buffer = (
                self.input_buffer[:self.cursor_pos] + 
                char + 
                self.input_buffer[self.cursor_pos:]
            )
            self.cursor_pos += 1
        
        return None


class Game:
    """Main game controller"""
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.renderer = TerminalRenderer(stdscr)
        self.engine = GameEngine()
        self.session_id: Optional[str] = None
        self.running = True
        
    def get_prompt(self) -> str:
        """Get current prompt string"""
        if not self.session_id:
            return "> "
        
        world = self.engine.get_world(self.session_id)
        if not world:
            return "> "
        
        username = world.player.username
        hostname = world.player.current_host
        path = world.player.current_path
        
        # Shorten path for display
        if path.startswith("/home/user"):
            display_path = "~" + path[10:]
        else:
            display_path = path
        
        return f"{username}@{hostname}:{display_path}$ "
    
    async def start(self):
        """Start the game"""
        # Create new session
        self.session_id = self.engine.create_session("player")
        
        # Show welcome message
        self.renderer.add_output("═" * 60, "info")
        self.renderer.add_output("  CRT HACKER - Terminal Infiltration Game", "success")
        self.renderer.add_output("═" * 60, "info")
        self.renderer.add_output("", "normal")
        self.renderer.add_output("Welcome to the underground network.", "system")
        self.renderer.add_output("Type 'help' for available commands.", "system")
        self.renderer.add_output("", "normal")
        
        # Main game loop
        while self.running:
            prompt = self.get_prompt()
            self.renderer.render(prompt)
            
            # Get input
            key = self.stdscr.getch()
            command = self.renderer.handle_input(key)
            
            if command is not None:
                await self.process_command(command)
    
    async def process_command(self, command: str):
        """Process a game command"""
        # Handle local commands
        if command.strip().lower() in ['clear', 'cls']:
            self.renderer.clear_screen()
            return
        
        if command.strip().lower() in ['exit', 'quit']:
            self.running = False
            return
        
        # Show command in output
        prompt = self.get_prompt()
        self.renderer.add_output(f"{prompt}{command}", "normal")
        
        # Send to game engine
        result = await self.engine.process_command(self.session_id, command)
        
        # Display output
        for output_msg in result.output:
            if isinstance(output_msg, OutputMessage):
                self.renderer.add_output(output_msg.text, output_msg.style)
            else:
                self.renderer.add_output(str(output_msg), "normal")


async def game_main(stdscr):
    """Async main game function"""
    game = Game(stdscr)
    await game.start()


def main(stdscr):
    """Entry point for curses wrapper"""
    asyncio.run(game_main(stdscr))


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("\nGame terminated.")
        sys.exit(0)
