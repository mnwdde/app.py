import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading

def execute(cmd):
    
    cmd = cmd.strip()
    if not cmd:
        return None
    try:
        output = subprocess.check_output(
            shlex.split(cmd),
            stderr=subprocess.STDOUT,
            shell=True
        )
        return output.decode()
    except subprocess.CalledProcessError as e:
        return e.output.decode()

class NetCat:
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        try:
            if self.args.listen:
                self.listen()
            else:
                self.send()
        except Exception as e:
            print(f"Error: {e}")
            self.socket.close()
            sys.exit(1)

    def send(self):
        try:
            self.socket.connect((self.args.target, self.args.port))
            if self.buffer:
                self.socket.send(self.buffer.encode())
            
            while True:
                recv_len = 1
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode('utf-8', errors='ignore')
                    if recv_len < 4096:
                        break
                if response:
                    print(response)
                    buffer = input('> ')
                    buffer += '\n'
                    self.socket.send(buffer.encode())
        except (KeyboardInterrupt, EOFError):
            print("\nConnection closed.")
            self.socket.close()
            sys.exit(0)
        except Exception as e:
            print(f"Connection error: {e}")
            self.socket.close()
            sys.exit(1)

    def listen(self):
        try:
            bind_address = '' if self.args.target == '0.0.0.0' else self.args.target
            self.socket.bind((bind_address, self.args.port))
            self.socket.listen(5)
            print(f'Listening on {bind_address or "all interfaces"}:{self.args.port}...')
            
            while True:
                client_socket, addr = self.socket.accept()
                print(f"Accepted connection from {addr[0]}:{addr[1]}")
                client_thread = threading.Thread(
                    target=self.handle,
                    args=(client_socket,)
                )
                client_thread.start()
        except OSError as e:
            print(f"Socket error: {e}")
            sys.exit(1)

    def handle(self, client_socket):
        try:
            if self.args.execute:
                output = execute(self.args.execute)
                if output:
                    client_socket.send(output.encode())
            elif self.args.upload:
                file_buffer = b''
                while True:
                    data = client_socket.recv(4096)
                    if not data:
                        break
                    file_buffer += data
                with open(self.args.upload, 'wb') as f:
                    f.write(file_buffer)
                message = f'Saved file {self.args.upload}'
                client_socket.send(message.encode())
            elif self.args.command:
                while True:
                    try:
                        client_socket.send(b'BHP: #> ')
                        cmd_buffer = b''
                        while b'\n' not in cmd_buffer:
                            cmd_buffer += client_socket.recv(64)
                        response = execute(cmd_buffer.decode().strip())
                        if response:
                            client_socket.send(response.encode())
                    except (ConnectionResetError, BrokenPipeError):
                        print("Client disconnected")
                        break
        finally:
            client_socket.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='BHP Net Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Examples:
  # Start listener (all interfaces):
  netcat.py -l -p 5555 -c
  
  # Connect to listener:
  netcat.py -t 127.0.0.1 -p 5555
  
  # Execute command on remote:
  netcat.py -t 192.168.1.10 -p 5555 -e "dir"
  
  # Upload file:
  netcat.py -t 192.168.1.10 -p 5555 -u file.txt
'''))
    parser.add_argument('-c', '--command', action='store_true', help='command shell')
    parser.add_argument('-e', '--execute', help='execute specified command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen')
    parser.add_argument('-p', '--port', type=int, default=5555, help='specified port')
    parser.add_argument('-t', '--target', default='127.0.0.1', help='specified IP (default: 127.0.0.1)')
    parser.add_argument('-u', '--upload', help='upload file')
    
    args = parser.parse_args()

    if args.listen:
        buffer = ''
        if args.target == '0.0.0.0':
            print("Warning: Listening on all interfaces (0.0.0.0)")
    else:
        buffer = sys.stdin.read()

    nc = NetCat(args, buffer)
    nc.run()