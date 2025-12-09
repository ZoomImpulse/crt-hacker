/**
 * Autocomplete Service
 * Handles command and path completion
 */

// Available game commands
const AVAILABLE_COMMANDS = [
  'help',
  'ls',
  'cd',
  'pwd',
  'cat',
  'scan',
  'crack',
  'connect',
  'exit',
  'clear',
  'cls'
];

export interface AutocompleteResult {
  completed: string;
  suggestions: string[];
}

/**
 * Get autocomplete suggestions based on input
 */
export function getAutocompleteSuggestions(input: string): AutocompleteResult {
  const trimmed = input.trim();
  const parts = trimmed.split(/\s+/);
  const command = parts[0]?.toLowerCase() || '';
  
  // If typing first word (command)
  if (parts.length === 1) {
    return autocompleteCommand(command);
  }
  
  // If typing arguments
  return autocompleteArgument(command, parts.slice(1).join(' '));
}

/**
 * Autocomplete command name
 */
function autocompleteCommand(partial: string): AutocompleteResult {
  const matches = AVAILABLE_COMMANDS.filter(cmd => 
    cmd.toLowerCase().startsWith(partial.toLowerCase())
  );
  
  if (matches.length === 0) {
    return { completed: partial, suggestions: [] };
  }
  
  if (matches.length === 1) {
    return { completed: matches[0] + ' ', suggestions: [] };
  }
  
  // Find common prefix
  const commonPrefix = findCommonPrefix(matches);
  return {
    completed: commonPrefix,
    suggestions: matches
  };
}

/**
 * Autocomplete argument (basic)
 * For now, just suggests paths for cd and cat commands
 */
function autocompleteArgument(command: string, partial: string): AutocompleteResult {
  // Commands that take path arguments
  const pathCommands = ['cd', 'cat', 'ls'];
  
  if (!pathCommands.includes(command)) {
    return { completed: partial, suggestions: [] };
  }
  
  // Parse path
  const lastSlash = partial.lastIndexOf('/');
  const dir = lastSlash >= 0 ? partial.substring(0, lastSlash) || '/' : '';
  const partialName = lastSlash >= 0 ? partial.substring(lastSlash + 1) : partial;
  
  // Common directories
  const commonPaths = ['/', '/home/', '/home/user/', '../', './'];
  const suggestions = commonPaths
    .filter(path => path.startsWith(dir === '' ? '.' : dir))
    .map(path => dir === '' && path === './' ? path : path);
  
  if (suggestions.length === 0) {
    return { completed: partial, suggestions: [] };
  }
  
  if (suggestions.length === 1) {
    return { completed: suggestions[0], suggestions: [] };
  }
  
  return { completed: dir, suggestions };
}

/**
 * Find common prefix among strings
 */
function findCommonPrefix(strings: string[]): string {
  if (strings.length === 0) return '';
  
  const first = strings[0];
  let prefix = '';
  
  for (let i = 0; i < first.length; i++) {
    const char = first[i].toLowerCase();
    if (strings.every(s => s[i]?.toLowerCase() === char)) {
      prefix += first[i];
    } else {
      break;
    }
  }
  
  return prefix;
}

/**
 * Get all available commands for help text
 */
export function getAllCommands(): string[] {
  return [...AVAILABLE_COMMANDS];
}
