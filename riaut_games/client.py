import socket

class Client:
    def __init__(self, host = '192.168.1.98', port = 32500) -> None:
        self._host = host
        self._port = port
        self._addr = (self._host, self._port)
    
    def join_server(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(self._addr)
    
        while True:
            data = s.recv(1024)
            message = ""

            if data:
                data = data.decode()
                if (data[0] == "Q"):
                    message = input(data)
                    s.sendall(message.encode())
                else:
                    print(data)
            
            if message == "stop":
                break

if __name__ == "__main__":
    client = Client()
    client.join_server()
