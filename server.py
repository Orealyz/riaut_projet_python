import socket
import sys
# from player import Player

class Server:
    def __init__(self, host = "", port = 32500) -> None:
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
        
        self.serve_forever()

    def serve_forever(self):
        data = self.send_question("On peut parler ?")
        while True:
            try:
                if data.__contains__("stop"):
                    self._conn.close()
                    break
                else:
                    self._game.start()

            except socket.error:
                print("Error Occured.")
        sys.exit(1)

    def send_question(self, question):
        self._conn.sendall(question.encode())
        data = self._conn.recv(1024)
        return data.decode()

if __name__ == "__main__":
    server = Server()
    server.start_server()