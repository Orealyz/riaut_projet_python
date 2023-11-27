from server import Server
from player import Player
from character import Personnage

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
        list_perso = [Personnage("Sylvan", 110, 8, 4, 9, "Foudre", "Ombre"), Personnage("Ignis", 120, 10, 2, 7, "Brûlure", "Flamme"), 
                       Personnage("Zephyr", 90, 6, 5, 8, "Tourbillon", "Souffle"), Personnage("Thorn", 140, 9, 3, 6, "Épine", "Carapace"),
                       Personnage("Aqua", 130, 7, 6, 5, "Vague", "Cascade")]
        self._server.send_msg("Voici la liste des personnages : \n" + list_perso[0].__str__() + "\n" + list_perso[1].__str__() + "\n" + list_perso[2].__str__() 
                              + "\n" + list_perso[3].__str__() + "\n" + list_perso[4].__str__() + "\n","Voici la liste des personnages : \n" + list_perso[0].__str__() + "\n" + list_perso[1].__str__() + "\n" + list_perso[2].__str__() 
                              + "\n" + list_perso[3].__str__() + "\n" + list_perso[4].__str__() + "\n")
        perso_1 = None
        while perso_1 == None:
            perso_1 = self._server.send_question_client("Q| Choisis ton 1er personnage : ", "M| Joueur 1 choisis son 1er personnage")
            if perso_1 == "Sylvan":
                perso_1 = list_perso[0]
            elif perso_1 == "Ignis":
                perso_1 = list_perso[1]
            elif perso_1 == "Zephyr":
                perso_1 = list_perso[2]
            elif perso_1 == "Thorn":
                perso_1 = list_perso[3]
            elif perso_1 == "Aqua":
                perso_1 = list_perso[4]
            else:
                perso_1 = None
        
        perso_2 = None
        while perso_2 == None:
            perso_2 = self._server.send_question_client("Q| Choisis ton 2eme personnage : ", "M| Joueur 1 choisis son 2eme personnage")
            if perso_2 == "Sylvan":
                perso_2 = list_perso[0]
            elif perso_2 == "Ignis":
                perso_2 = list_perso[1]
            elif perso_2 == "Zephyr":
                perso_2 = list_perso[2]
            elif perso_2 == "Thorn":
                perso_2 = list_perso[3]
            elif perso_2 == "Aqua":
                perso_2 = list_perso[4]
            else:
                perso_2 = None

        perso_3 = None
        while perso_3 == None:
            perso_3 = self._server.send_question_client("Q| Choisis ton 3eme personnage : ", "M| Joueur 1 choisis son 3eme personnage")
            if perso_3 == "Sylvan":
                perso_3 = list_perso[0]
            elif perso_3 == "Ignis":
                perso_3 = list_perso[1]
            elif perso_3 == "Zephyr":
                perso_3 = list_perso[2]
            elif perso_3 == "Thorn":
                perso_3 = list_perso[3]
            elif perso_3 == "Aqua":
                perso_3 = list_perso[4]
            else:
                perso_3 = None

        self._player_1.set_perso([perso_1, perso_2, perso_3])

        # perso_1 = self._server.send_question_server("Q| Choisis ton 1er personnage : ", "M| Joueur 2 choisis son 1er personnage")
        # perso_2 = self._server.send_question_server("Q| Choisis ton 2eme personnage : ", "M| Joueur 2 choisis son 2eme personnage")
        # perso_3 = self._server.send_question_server("Q| Choisis ton 3eme personnage : ", "M| Joueur 2 choisis son 3eme personnage")

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
    

