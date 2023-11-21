import socket

class Client:
    def __init__(self, host = '10.33.76.200', port = 32500) -> None:
        self._host = host
        self._port = port
        self._addr = (self._host, self._port)
    
    def join_server(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(self._addr)
    
        while True:
            data = s.recv(1024)

            if data:
                message = input(data.decode())

            s.sendall(message.encode())
            
            if message == "stop":
                break

client = Client()
client.join_server()