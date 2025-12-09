/**
 * Autocomplete Service
 * Handles command and path completion
 * Classic TAB autocomplete - directly completes input
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
  hasMultipleMatches: boolean;
  matches?: string[];
}

/**
 * Get autocomplete completion based on input
 * Returns the completed text and whether there are multiple matches
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
    return { completed: partial, hasMultipleMatches: false };
  }
  
  if (matches.length === 1) {
    // Single match - complete with space
    return { completed: matches[0] + ' ', hasMultipleMatches: false };
  }
  
  // Multiple matches - complete to common prefix
  const commonPrefix = findCommonPrefix(matches);
  return {
    completed: commonPrefix,
    hasMultipleMatches: true,
    matches: matches
  };
}

/**
 * Autocomplete argument (basic)
 * For now, just auto-completes paths for cd and cat commands
 */
function autocompleteArgument(command: string, partial: string): AutocompleteResult {
  // Commands that take path arguments
  const pathCommands = ['cd', 'cat', 'ls'];
  
  if (!pathCommands.includes(command)) {
    return { completed: partial, hasMultipleMatches: false };
  }
  
  // Parse path
  const lastSlash = partial.lastIndexOf('/');
  const dir = lastSlash >= 0 ? partial.substring(0, lastSlash) || '/' : '';
  
  // Common directories
  const commonPaths = ['/home/user/', '/home/', '/', '../', './'];
  const matches = commonPaths
    .filter(path => path.startsWith(partial === '' ? '.' : dir))
    .filter(path => path !== partial); // Exclude exact matches
  
  if (matches.length === 0) {
    return { completed: partial, hasMultipleMatches: false };
  }
  
  if (matches.length === 1) {
    return { completed: matches[0], hasMultipleMatches: false };
  }
  
  // Find common prefix of matches
  const commonPrefix = findCommonPrefix(matches);
  return {
    completed: commonPrefix,
    hasMultipleMatches: true,
    matches: matches
  };
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
