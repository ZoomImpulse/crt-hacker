# Game Design Document

## Concept

A text-based hacking simulation game set in a retro terminal environment. Players navigate a virtual network, exploit vulnerabilities, and collect flags to progress through increasingly difficult challenges.

## Core Gameplay Loop

1. **Explore** - Scan networks, discover hosts
2. **Analyze** - Examine services and vulnerabilities
3. **Exploit** - Crack passwords, exploit vulnerabilities
4. **Collect** - Capture flags and gather intel
5. **Progress** - Advance to harder challenges

## Game Mechanics

### Virtual Network

- Multiple interconnected hosts
- Realistic IP addressing (192.168.x.x, 10.x.x.x)
- Subnet isolation
- Network topology discovery

### Virtual Filesystem

- Tree-structured filesystem per host
- Standard Unix-like structure (/home, /var, /etc)
- Hidden files and directories
- Permission system

### Services & Vulnerabilities

Each host runs simulated services with vulnerabilities:

**Service Types:**

- SSH (port 22)
- HTTP (port 80)
- FTP (port 21)
- MySQL (port 3306)
- Custom services

**Vulnerability Types:**

- Weak passwords (brute force)
- Default credentials
- SQL injection
- Buffer overflow (simulated)
- Misconfiguration
- Zero-day exploits (fictional)

### Progression System

**Levels:**

1. **Novice** (0-500 pts) - Basic commands, local exploration
2. **Script Kiddie** (500-1500 pts) - Simple exploits
3. **Hacker** (1500-3000 pts) - Multi-host chains
4. **Elite** (3000-5000 pts) - Complex vulnerabilities
5. **Admin** (5000+ pts) - Full system control

**Scoring:**

- Discover host: +10 points
- Compromise host: +100 points
- Find flag: +50-500 points (difficulty-based)
- Solve puzzle: +200 points
- Complete objective: +1000 points

### Objectives & Flags

**Flag Format:** `FLAG{descriptive_name}`

**Objective Types:**

- Capture specific flags
- Compromise specific hosts
- Exfiltrate data
- Maintain persistence
- Cover tracks

## Command Set

### Navigation

- `ls [path]` - List directory
- `cd <path>` - Change directory
- `pwd` - Print working directory

### File Operations

- `cat <file>` - Display file contents
- `grep <pattern> <file>` - Search in file
- `find <path> <name>` - Find files

### Network

- `scan [--local|--range <ip>]` - Scan network
- `nmap <host>` - Port scan
- `ping <host>` - Check connectivity
- `traceroute <host>` - Trace route

### Exploitation

- `connect <host>` - SSH to host
- `crack <host> [port]` - Attempt exploit
- `brute <service> <wordlist>` - Brute force
- `exploit <vulnerability>` - Run exploit

### Recon

- `whois <host>` - Host information
- `netstat` - Show connections
- `ps` - List processes
- `history` - Command history

### System

- `help [command]` - Show help
- `clear` - Clear screen
- `exit` - Disconnect/quit

## Puzzle Design

### Example Puzzles

#### 1. Weak Password SSH

```
1. Scan network
2. Find SSH service
3. Run crack command
4. Connect to compromised host
5. Find flag in /root/flag.txt
```

#### 2. Hidden Directory

```
1. List files with ls -la
2. Find hidden .secret directory
3. Navigate to directory
4. Read encrypted file
5. Decrypt with password from another host
```

#### 3. SQL Injection

```
1. Discover web service
2. Test for SQL injection
3. Extract database credentials
4. Use credentials to access MySQL
5. Query for flag in admin table
```

#### 4. Multi-Host Chain

```
1. Compromise first host
2. Find SSH key in user home
3. Use key to access second host
4. Escalate privileges
5. Access final flag
```

## World Design

### Network Topology

```
Internet Gateway (10.0.0.1)
├── DMZ (192.168.1.0/24)
│   ├── Web Server (192.168.1.10)
│   └── Mail Server (192.168.1.11)
└── Internal Network (192.168.2.0/24)
    ├── File Server (192.168.2.10)
    ├── Database (192.168.2.11)
    └── Admin Workstation (192.168.2.100)
```

### Host Templates

#### Beginner Host

- 1-2 services
- Weak password vulnerability
- 1 flag
- Difficulty: 1

#### Intermediate Host

- 2-3 services
- SQL injection or misconfiguration
- Hidden files
- 2-3 flags
- Difficulty: 2-3

#### Advanced Host

- 3+ services
- Chained exploits required
- Privilege escalation needed
- Multiple flags
- Difficulty: 4-5

## Narrative Elements

### Story Arc

**Act 1: Initiation**

- Player receives anonymous tip
- Must prove skills by hacking test system
- Introduction to basic commands

**Act 2: Investigation**

- Uncover conspiracy at fictional corporation
- Piece together evidence from multiple hosts
- Learn advanced exploitation techniques

**Act 3: Confrontation**

- Infiltrate highly secured network
- Bypass sophisticated defenses
- Expose wrongdoing

### Lore Delivery

- Text files with background info
- Email messages between NPCs
- Log files revealing story
- Terminal messages from mysterious ally

## Technical Puzzles

### Cryptography

- Caesar cipher
- Base64 encoding
- XOR cipher
- Simple substitution

### Programming

- Script analysis
- Code review to find vulnerabilities
- Write simple exploits

### Logic

- Password hints in different files
- Coordinates leading to locations
- Sequences to unlock

## Replay Value

### Randomization

- Host placement varies
- Password changes
- Flag locations shuffle
- Service configurations differ

### Challenges

- Speed runs (time-based)
- Minimal commands (efficiency)
- Stealth mode (avoid detection)
- No hints mode (hardcore)

### Leaderboard

- Global high scores
- Daily challenges
- Achievement system

## Monetization (Optional)

### Free Tier

- Complete main campaign
- Daily challenges
- Basic customization

### Premium

- Additional campaigns
- Advanced challenges
- Custom color schemes
- Priority support

## Accessibility

### Difficulty Settings

- **Easy**: Hints available, forgiving timing
- **Normal**: Moderate hints, standard timing
- **Hard**: Minimal hints, realistic timing
- **Expert**: No hints, strict time limits

### Hints System

- Context-sensitive hints
- Progressive hint revelation
- Cooldown between hints
- Score penalty for hint usage

## Future Expansions

### Content Updates

- New host types
- Additional services
- Novel vulnerabilities
- Extended storylines

### Features

- Multiplayer co-op
- PvP hacking battles
- Mission creator/editor
- Achievement badges

### Technical

- Mobile version
- Offline mode
- Save slots
- Screenshot mode

## Balancing

### Difficulty Curve

- Level 1: 15 minutes
- Level 2: 30 minutes
- Level 3: 1 hour
- Level 4: 2 hours
- Level 5: 3+ hours

### Rewards Scaling

- Early rewards frequent
- Mid-game rewards moderate
- Late-game rewards rare but valuable

### Progression Gates

- Minimum score to unlock levels
- Required flags before advancing
- Skill checks (must demonstrate competency)
