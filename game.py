from server import Server
from player import Player

class Game:
    def __init__(self, server) -> None:
        self._player_1 = None
        self._player_2 = None
        self._server = server
        self._start = False

    def team_creation(self):
        pass

    def players(self):
        self._player_1 = Player(self._server.send_question_server("Q| Choisis ton pseudo : ", "M| Joueur 1 choisis son pseudo"))
        self._player_2 = Player(self._server.send_question_client("Q| Choisis ton pseudo : ", "M| Joueur 2 choisis son pseudo"))
        send_data = (f"M| Le pseudo du joueur 1 est : {self._player_1.get_pseudo()} et le joueur 2 est : {self._player_2.get_pseudo()}")
        self._server.send_msg(send_data, send_data)
        return self._player_1, self._player_2
    
    def perso(self):
        pass

    def start(self):
        self._start = True

    def get_start(self):
        return self._start

if __name__ == "__main__":
    server = Server()
    game = Game(server)
    server.start_server(game)
    if game.get_start:
        game.players()
        game.perso()
    

