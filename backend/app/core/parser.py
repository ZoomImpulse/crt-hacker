"""
Command Parser
Parses and tokenizes terminal commands
"""
import shlex
from typing import List, Tuple, Optional


class CommandParser:
    """Parse terminal commands into command and arguments"""
    
    @staticmethod
    def parse(command_line: str) -> Tuple[Optional[str], List[str]]:
        """
        Parse command line into command and arguments
        
        Args:
            command_line: Raw command string
            
        Returns:
            Tuple of (command, args) or (None, []) if empty
        """
        if not command_line or not command_line.strip():
            return None, []
        
        try:
            # Use shlex for proper shell-like parsing
            tokens = shlex.split(command_line)
        except ValueError:
            # Handle unclosed quotes
            tokens = command_line.split()
        
        if not tokens:
            return None, []
        
        command = tokens[0].lower()
        args = tokens[1:] if len(tokens) > 1 else []
        
        return command, args
    
    @staticmethod
    def parse_flags(args: List[str]) -> Tuple[List[str], dict]:
        """
        Separate positional args from flags
        
        Args:
            args: List of arguments
            
        Returns:
            Tuple of (positional_args, flags_dict)
        """
        positional = []
        flags = {}
        
        i = 0
        while i < len(args):
            arg = args[i]
            
            if arg.startswith('--'):
                # Long flag (--flag or --flag=value)
                if '=' in arg:
                    key, value = arg[2:].split('=', 1)
                    flags[key] = value
                else:
                    key = arg[2:]
                    # Check if next arg is a value
                    if i + 1 < len(args) and not args[i + 1].startswith('-'):
                        flags[key] = args[i + 1]
                        i += 1
                    else:
                        flags[key] = True
            elif arg.startswith('-') and len(arg) > 1:
                # Short flag(s) (-f or -abc)
                for char in arg[1:]:
                    flags[char] = True
            else:
                positional.append(arg)
            
            i += 1
        
        return positional, flags
