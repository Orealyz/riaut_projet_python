import socket
import sys
# from player import Player

class Server:
    def __init__(self, host = "192.168.1.98", port = 32500) -> None:
        self._host = host
        self._port = port
        self._addr = (self._host, self._port)
        self._conn = None
        self._game = None

    def start_server(self, game):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(self._addr)  
        s.listen(1)
        self._game = game
        try:
            self._conn, self._addr = s.accept()
        except:
            print("Error")
            sys.exit(1)
    
        self._game.start()

    def send_question_client(self, question, msg):
        print(msg)
        self._conn.sendall(question.encode())
        data = self._conn.recv(1024)
        return data.decode()
    
    def send_question_server(self, question, msg):
        self._conn.sendall(msg.encode())
        return input(question)
    
    def send_msg(self, msg_client, msg_server):
        self._conn.sendall(msg_client.encode())
        print(msg_server)

    def send_msg_client(self, msg_client):
        self._conn.sendall(msg_client.encode())
    
    def send_msg_server(self, msg_server):
        print(msg_server)


