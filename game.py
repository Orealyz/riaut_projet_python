from server import Server
from player import Player

class Game:
    def __init__(self, server) -> None:
        self._player_1 = None
        self._player_2 = None
        self._server = server

    def team_creation(self):
        pass

if __name__ == "__main__":
    server = Server()
    game = Game(server)
    server.start_server(game)

