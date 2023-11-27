from server import Server
from player import Player
from character import Personnage
import time

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
        list_perso = [
            Personnage("Sylvan", 110, 8, 4, 9, "Foudre", "Ombre"),
            Personnage("Ignis", 120, 10, 2, 7, "Brûlure", "Flamme"),
            Personnage("Zephyr", 90, 6, 5, 8, "Tourbillon", "Souffle"),
            Personnage("Thorn", 140, 9, 3, 6, "Épine", "Carapace"),
            Personnage("Aqua", 130, 7, 6, 5, "Vague", "Cascade")
        ]

        message = "Voici la liste des personnages : \n"
        self._server.send_msg(message, message)
        for perso in list_perso:
            message = perso.__str__() + "\n"
            self._server.send_msg(message, message)
            time.sleep(0.5)

        
        perso_1 = self.choisir_personnage(1, list_perso, "server")
        perso_2 = self.choisir_personnage(2, list_perso, "server")
        perso_3 = self.choisir_personnage(3, list_perso, "server")

        self._player_1.set_perso([perso_1, perso_2, perso_3])

        perso_1 = self.choisir_personnage(1, list_perso, "client")
        perso_2 = self.choisir_personnage(2, list_perso, "client")
        perso_3 = self.choisir_personnage(3, list_perso, "client")

        self._player_2.set_perso([perso_1, perso_2, perso_3])

        send_data = (f"M| {self._player_1.get_pseudo()} a choisi {self._player_1.get_perso()[0]._nom}, {self._player_1.get_perso()[1]._nom} et {self._player_1.get_perso()[2]._nom}")
        self._server.send_msg(send_data, send_data)
        send_data = (f"M| {self._player_2.get_pseudo()} a choisi {self._player_2.get_perso()[0]._nom}, {self._player_2.get_perso()[1]._nom} et {self._player_2.get_perso()[2]._nom}")
        self._server.send_msg(send_data, send_data)

    def choisir_personnage(self, joueur_numero, list_perso, client_server):
        personnage = None
        while personnage is None:
            message_question = f"Q| Choisis ton {joueur_numero} personnage : "
            message_confirmation = f"M| Joueur {joueur_numero} choisis son {joueur_numero} personnage"
            
            if client_server == "server":
                personnage_nom = self._server.send_question_server(message_question, message_confirmation)
            if client_server == "client":
                personnage_nom = self._server.send_question_client(message_question, message_confirmation)
            
            if personnage_nom in ["Sylvan", "Ignis", "Zephyr", "Thorn", "Aqua"]:
                noms_perso = ["Sylvan", "Ignis", "Zephyr", "Thorn", "Aqua"]
                personnage = list_perso[noms_perso.index(personnage_nom)]
            else:
                personnage = None
        return personnage

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
    

