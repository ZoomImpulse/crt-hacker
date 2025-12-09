# CRT Hacker - Terminal Edition

Ein terminal-basiertes Hacking-Spiel mit retro CRT-Ästhetik.

## Beschreibung

CRT Hacker ist ein interaktives Terminal-Spiel, in dem du als Hacker durch virtuelle Netzwerke navigierst, Systeme infiltrierst und Flags sammelst. Das Spiel nutzt Python und curses für ein authentisches Terminal-Erlebnis mit Farben, History und CRT-Effekten.

## Features

- 🖥️ Natives Terminal-Interface mit curses
- 🎨 Farbige Ausgaben und CRT-inspirierte Ästhetik
- 📜 Befehlshistorie mit Pfeiltasten
- 💾 Automatisches Speichern des Spielstands
- 🌐 Virtuelle Netzwerke mit mehreren Hosts
- 📁 Simuliertes Dateisystem pro Host
- 🎯 Verschiedene Schwierigkeitsgrade und Objectives

## Installation

### Voraussetzungen

- Python 3.8 oder höher
- Unix-basiertes System (Linux, macOS) oder Windows mit WSL

### Setup

1. Repository klonen:
```bash
git clone <repository-url>
cd crt-hacker
```

2. Dependencies installieren:
```bash
pip install -r requirements.txt
```

## Spiel starten

```bash
python3 game.py
```

## Steuerung

- **Enter**: Befehl ausführen
- **Pfeiltasten ↑/↓**: Durch Befehlshistorie navigieren
- **Pfeiltasten ←/→**: Cursor bewegen
- **Backspace/Delete**: Zeichen löschen
- **Ctrl+L**: Bildschirm löschen
- **Home/End**: Zum Anfang/Ende der Zeile

## Verfügbare Befehle

- `help` - Zeigt alle verfügbaren Befehle
- `ls` - Listet Dateien und Verzeichnisse
- `cd <dir>` - Wechselt in ein Verzeichnis
- `cat <file>` - Zeigt Dateiinhalt an
- `pwd` - Zeigt aktuelles Verzeichnis
- `whoami` - Zeigt aktuellen Benutzer
- `hostname` - Zeigt aktuellen Host
- `scan` - Scannt das Netzwerk nach Hosts
- `connect <ip>` - Verbindet zu einem Host
- `clear` - Löscht den Bildschirm
- `exit` oder `quit` - Beendet das Spiel

## Spielziel

Navigiere durch virtuelle Netzwerke, kompromittiere Hosts und sammle Flags. Jeder Host hat ein eigenes Dateisystem mit versteckten Informationen und Vulnerabilities.

## Speicherstände

Das Spiel speichert automatisch nach jedem Befehl. Speicherstände werden in `backend/saves/` abgelegt.

## Entwicklung

### Projektstruktur

```
crt-hacker/
├── game.py                 # Hauptprogramm mit curses UI
├── requirements.txt        # Python-Dependencies
└── backend/
    └── app/
        ├── core/          # Game Engine, Parser, Dispatcher
        ├── game/          # Game Commands
        ├── models/        # Data Models
        └── saves/         # Spielstände (automatisch erstellt)
```

### Neue Befehle hinzufügen

1. Erstelle eine neue Command-Klasse in `backend/app/game/commands.py`
2. Registriere den Befehl im `CommandDispatcher` in `backend/app/core/dispatcher.py`

## Troubleshooting

### Terminal-Größe

Das Spiel benötigt mindestens 80x24 Zeichen. Bei zu kleinem Terminal wird die Ausgabe möglicherweise abgeschnitten.

### Farben funktionieren nicht

Stelle sicher, dass dein Terminal 256 Farben unterstützt:
```bash
echo $TERM
```

Sollte `xterm-256color` oder ähnlich anzeigen.

### Windows

Unter Windows empfehlen wir WSL (Windows Subsystem for Linux) für die beste Terminal-Erfahrung.

## Lizenz

[Lizenz hier einfügen]

## Credits

Entwickelt mit Python und curses für ein authentisches retro Terminal-Erlebnis.
