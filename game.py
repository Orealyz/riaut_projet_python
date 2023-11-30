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

    def players(self):
        self._player_1 = Player(self._server.send_question_server("Q| Choisis ton pseudo : ", "M| Joueur 1 choisis son pseudo"))
        self._player_2 = Player(self._server.send_question_client("Q| Choisis ton pseudo : ", "M| Joueur 2 choisis son pseudo"))
        send_data = (f"M| Le pseudo du joueur 1 est : {self._player_1.get_pseudo()} et le joueur 2 est : {self._player_2.get_pseudo()}")
        self._server.send_msg(send_data, send_data)
        return self._player_1, self._player_2
    
    def perso(self):
        list_perso = [
            Personnage("Sylvan", 30, 8, 4, 9, "Foudre", "Ombre"),
            Personnage("Ignis", 32, 10, 2, 7, "Brûlure", "Flamme"),
            Personnage("Zephyr", 30, 8, 5, 8, "Tourbillon", "Souffle"),
            Personnage("Thorn", 45, 9, 3, 6, "Épine", "Carapace"),
            Personnage("Aqua", 35, 7, 6, 5, "Vague", "Cascade")
        ]

        message = "Voici la liste des personnages : \n"
        self._server.send_msg(message, message)
        for perso in list_perso:
            message = perso.__str__() + "\n"
            self._server.send_msg(message, message)
            time.sleep(0.5)

        
        perso_1 = self.choisir_personnage("1er", self._player_1.get_pseudo(), list_perso, "server")
        perso_2 = self.choisir_personnage("2me", self._player_1.get_pseudo(), list_perso, "server")
        while perso_2 == perso_1:
            perso_2 = self.choisir_personnage("2me", self._player_1.get_pseudo(), list_perso, "server")
        perso_3 = self.choisir_personnage("3me", self._player_1.get_pseudo(), list_perso, "server")
        while perso_3 == perso_1 or perso_3 == perso_2:
            perso_3 = self.choisir_personnage("3me", self._player_1.get_pseudo(), list_perso, "server")
        self._player_1.set_perso([perso_1, perso_2, perso_3])

        perso_1 = self.choisir_personnage("1er", self._player_2.get_pseudo(), list_perso, "client")
        perso_2 = self.choisir_personnage("2me", self._player_2.get_pseudo(), list_perso, "client")
        while perso_2 == perso_1:
            perso_2 = self.choisir_personnage("2me", self._player_2.get_pseudo(), list_perso, "client")
        perso_3 = self.choisir_personnage("3me", self._player_2.get_pseudo(), list_perso, "client")
        while perso_3 == perso_1 or perso_3 == perso_2:
            perso_3 = self.choisir_personnage("3me", self._player_2.get_pseudo(), list_perso, "client")
        

        self._player_2.set_perso([perso_1, perso_2, perso_3])

        send_data = (f"M| {self._player_1.get_pseudo()} a choisi {self._player_1.get_perso()[0]._nom}, {self._player_1.get_perso()[1]._nom} et {self._player_1.get_perso()[2]._nom}")
        self._server.send_msg(send_data, send_data)
        send_data = (f"M| {self._player_2.get_pseudo()} a choisi {self._player_2.get_perso()[0]._nom}, {self._player_2.get_perso()[1]._nom} et {self._player_2.get_perso()[2]._nom}")
        self._server.send_msg(send_data, send_data)

    def choisir_personnage(self, perso_numero, pseudo, list_perso, client_server):
        personnage = None
        while personnage is None:
            message_question = f"Q| Choisis ton {perso_numero} personnage : "
            message_confirmation = f"M| {pseudo} choisis son {perso_numero} personnage"
            
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
    
    def play(self):
         while team_alive(self._player_1._perso) and team_alive(self._player_2._perso):
            # Tour de l'equipe 1 choisis qui va attaquer  
            player_1_attaquant = ""
            while player_1_attaquant not in [game._player_1.get_perso()[0]._nom,game._player_1.get_perso()[1]._nom, game._player_1.get_perso()[2]._nom]:
                player_1_attaquant = self._server.send_question_server(f"""Q| Vos personnage sont :
{game._player_1.get_perso()[0]._nom}   {game._player_1.get_perso()[1]._nom}   {game._player_1.get_perso()[2]._nom}
Choisissez le personnage attaquant : """, 
                                                                        f"\nM| {game._player_1.get_pseudo()} choisis le personnage attaquant")
                if player_1_attaquant == game._player_1.get_perso()[0]._nom:
                    player_1_attaquant = game._player_1.get_perso()[0]
                elif player_1_attaquant == game._player_1.get_perso()[1]._nom:
                    player_1_attaquant = game._player_1.get_perso()[1]
                elif player_1_attaquant == game._player_1.get_perso()[2]._nom:
                    player_1_attaquant = game._player_1.get_perso()[2]
                else:
                    self._server.send_msg_server(f"""M| Entrée invalide. Veuillez saisir 
"{game._player_1.get_perso()[0]._nom}"  ou  "{game._player_1.get_perso()[1]._nom}"  ou  "{game._player_1.get_perso()[2]._nom}" """)
                    continue
                if player_1_attaquant.is_alive():
                    break
                else:
                    self._server.send_msg_server("M| Ton perso est mort. Choisis en un autre.")
                    continue

            self._server.send_msg_server(f"M| Le personnage choisis est {player_1_attaquant._nom}")

            # Détermine si l'équipe 2 est vivante 
            if team_alive(game._player_2.get_perso()) == True:
                pass
            else:
                self._server.send_msg(f"M| 🏆 L'équipe 1 remporte la victoire!")
                break

            # Tour de l'equipe 2 choisis qui va attaquer  
            player_2_attaquant = ""
            while player_2_attaquant not in [game._player_2.get_perso()[0]._nom, game._player_2.get_perso()[1]._nom, game._player_2.get_perso()[2]._nom]:
                player_2_attaquant = self._server.send_question_client(f"""Q| Vos personnage sont :
{game._player_2.get_perso()[0]._nom}   {game._player_2.get_perso()[1]._nom}   {game._player_2.get_perso()[2]._nom}
Choisissez le personnage attaquant : """, 
                                                                        f"M| {game._player_2.get_pseudo()} choisis le personnage attaquant")
                if player_2_attaquant == game._player_2.get_perso()[0]._nom:
                    player_2_attaquant = game._player_2.get_perso()[0]
                elif player_2_attaquant == game._player_2.get_perso()[1]._nom:
                    player_2_attaquant = game._player_2.get_perso()[1]
                elif player_2_attaquant == game._player_2.get_perso()[2]._nom:
                    player_2_attaquant = game._player_2.get_perso()[2]
                else:
                    self._server.send_msg_client(f"""M| Entrée invalide. Veuillez saisir 
"{game._player_2.get_perso()[0]._nom}"  ou  "{game._player_2.get_perso()[1]._nom}"  ou  "{game._player_2.get_perso()[2]._nom}" """)
                    continue
                if player_2_attaquant.is_alive():
                    break
                else:
                    self._server.send_msg_client("M| Ton perso est mort. Choisis en un autre.")
                    continue

            self._server.send_msg_client(f"M| Le personnage choisis est {player_2_attaquant._nom}")

             # Détermine si l'équipe 1 est vivante 
            if team_alive(game._player_1.get_perso()) == True:
                pass
            else:
                self._server.send_msg(f"M| 🏆 L'équipe 1 remporte la victoire!")
                break


            if player_1_attaquant._vitesse < player_2_attaquant._vitesse:
                # Tour de l'équipe 2
                # Le joueur 2 attaque en premier car son personnage a plus de vitesse
                action = self._server.send_question_client(f"Q| {game._player_2.get_pseudo()}, choisissez une action (attaque, passe) : ", f"M| {game._player_2.get_pseudo()} se décide à quoi faire")
                while action not in ['attaque','passe']:
                    self._server.send_msg_client(f"M| Entrée invalide. Veuillez saisir \"attaque\" pour attaquer ou \"passe\" pour passer.")
                    action = self._server.send_question_client(f"Q| {game._player_2.get_pseudo()}, choisissez une action (attaque, passe) : ", f"{game._player_2.get_pseudo()} se décide à quoi faire")
                if action == "attaque":
                    cible_attaquant_player_2 = self._server.send_question_client(f"""Q| Qui veux tu attaquer ?
Equipe adverse : {game._player_1.get_perso()[0]._nom}   {game._player_1.get_perso()[1]._nom}   {game._player_1.get_perso()[2]._nom}
La cible : """, f"M| {self._player_1.get_pseudo()} choisis qui attaquer")
                    while True:
                        if cible_attaquant_player_2 == game._player_1.get_perso()[0]._nom:
                            cible_attaquant_player_2 = game._player_1.get_perso()[0]
                        elif cible_attaquant_player_2 == game._player_1.get_perso()[1]._nom:
                            cible_attaquant_player_2 = game._player_1.get_perso()[1]
                        elif cible_attaquant_player_2 == game._player_1.get_perso()[2]._nom:
                            cible_attaquant_player_2 = game._player_1.get_perso()[2]
                        else:
                            self._server.send_msg_client(f"""M| Entrée invalide. Veuillez saisir 
"{game._player_1.get_perso()[0]._nom}"  ou  "{game._player_1.get_perso()[1]._nom}"  ou  "{game._player_1.get_perso()[2]._nom}" """)
                            continue
                        print("Juste avant affichage de la helthbar")
                        if cible_attaquant_player_2.is_alive():
                            target = cible_attaquant_player_2
                            info_attack = player_2_attaquant.attack(target)
                            self._server.send_msg(info_attack, info_attack)
                            self._server.send_msg(target.show_healthbar(), target.show_healthbar())
                            break
                        else:
                            self._server.send_msg_client("M| Son perso est mort. Arrète de focus et choisis en un autre.")
                            continue
                    if team_alive(self._player_2.get_perso()):
                        pass
                    else:
                        self._server.send_msg(f"🏆 {self._player_2.get_pseudo()} remporte la victoire!", f"🏆 {self._player_2.get_pseudo()} remporte la victoire!")
                else:
                    pass

                # Tour de l'équipe 1
                action = self._server.send_question_server(f"Q| {game._player_1.get_pseudo()}, choisissez une action (attaque, passe) : ", f"M| {game._player_1.get_pseudo()} se décide à quoi faire")
                while action not in ['attaque','passe']:
                    self._server.send_msg_server(f"M| Entrée invalide. Veuillez saisir \"attaque\" pour attaquer ou \"passe\" pour passer.")
                    action = self._server.send_question_server(f"Q| {game._player_1.get_pseudo()}, choisissez une action (attaque, passe) : ", f"M| {game._player_1.get_pseudo()} se décide à quoi faire")
                if action == "attaque":
                    cible_attaquant_player_1 = self._server.send_question_server(f"""Q| Qui veux tu attaquer ?
Equipe adverse : {game._player_2.get_perso()[0]._nom}   {game._player_2.get_perso()[1]._nom}   {game._player_2.get_perso()[2]._nom}
La cible : """, f"M| {self._player_1.get_pseudo()} choisis qui attaquer")
                    while True:
                        if cible_attaquant_player_1 == game._player_2.get_perso()[0]._nom:
                            cible_attaquant_player_1 = game._player_2.get_perso()[0]
                        elif cible_attaquant_player_1 == game._player_2.get_perso()[1]._nom:
                            cible_attaquant_player_1 = game._player_2.get_perso()[1]
                        elif cible_attaquant_player_1 == game._player_2.get_perso()[2]._nom:
                            cible_attaquant_player_1 = game._player_2.get_perso()[2]
                        else:
                            self._server.send_msg_client(f"""M| Entrée invalide. Veuillez saisir 
"{game._player_2.get_perso()[0]._nom}"  ou  "{game._player_2.get_perso()[1]._nom}"  ou  "{game._player_2.get_perso()[2]._nom}" """)
                            continue
                        print("Juste avant affichage de la helthbar")
                        if cible_attaquant_player_1.is_alive():
                            target = cible_attaquant_player_1
                            info_attack = player_1_attaquant.attack(target)
                            self._server.send_msg(info_attack, info_attack)
                            self._server.send_msg(target.show_healthbar(), target.show_healthbar())
                            break
                        else:
                            self._server.send_msg_client("M| Son perso est mort. Arrète de focus et choisis en un autre.")
                            continue      
                    if team_alive(self._player_2.get_perso()):
                        pass
                    else:
                        self._server.send_msg(f"🏆 {self._player_1.get_pseudo()} remporte la victoire!", f"🏆 {self._player_1.get_pseudo()} remporte la victoire!")
# -------------------------------------------------------------------------------------------------------------------------------------
                 
            else:
                # Tour de l'équipe 1
                # Le joueur 1 attaque en premier car son personnage a plus de vitesse
                action = self._server.send_question_server(f"Q| {game._player_1.get_pseudo()}, choisissez une action (attaque, passe) : ", f"M| {game._player_1.get_pseudo()} se décide à quoi faire")
                while action not in ['attaque','passe']:
                    self._server.send_msg_server(f"M| Entrée invalide. Veuillez saisir \"attaque\" pour attaquer ou \"passe\" pour passer.")
                    action = self._server.send_question_server(f"Q| {game._player_1.get_pseudo()}, choisissez une action (attaque, passe) : ", f"M| {game._player_1.get_pseudo()} se décide à quoi faire")
                if action == "attaque":
                    cible_attaquant_player_1 = self._server.send_question_server(f"""Q| Qui veux tu attaquer ?
Equipe adverse : {game._player_2.get_perso()[0]._nom}   {game._player_2.get_perso()[1]._nom}   {game._player_2.get_perso()[2]._nom}
La cible : """, f"M| {self._player_1.get_pseudo()} choisis qui attaquer")
                    while True:
                        if cible_attaquant_player_1 == game._player_2.get_perso()[0]._nom:
                            cible_attaquant_player_1 = game._player_2.get_perso()[0]
                        elif cible_attaquant_player_1 == game._player_2.get_perso()[1]._nom:
                            cible_attaquant_player_1 = game._player_2.get_perso()[1]
                        elif cible_attaquant_player_1 == game._player_2.get_perso()[2]._nom:
                            cible_attaquant_player_1 = game._player_2.get_perso()[2]
                        else:
                            self._server.send_msg_client(f"""M| Entrée invalide. Veuillez saisir 
"{game._player_2.get_perso()[0]._nom}"  ou  "{game._player_2.get_perso()[1]._nom}"  ou  "{game._player_2.get_perso()[2]._nom}" """)
                            continue
                        print("Juste avant affichage de la helthbar")
                        if cible_attaquant_player_1.is_alive():
                            target = cible_attaquant_player_1
                            info_attack = player_1_attaquant.attack(target)
                            self._server.send_msg(info_attack, info_attack)
                            self._server.send_msg(target.show_healthbar(), target.show_healthbar())
                            break
                        else:
                            self._server.send_msg_client("M| Son perso est mort. Arrète de focus et choisis en un autre.")
                            continue
                    if team_alive(self._player_2.get_perso()):
                        pass
                    else:
                        self._server.send_msg(f"🏆 {self._player_1.get_pseudo()} remporte la victoire!", f"🏆 {self._player_1.get_pseudo()} remporte la victoire!")
                # Tour de l'équipe 2
                action = self._server.send_question_client(f"Q| {game._player_2.get_pseudo()}, choisissez une action (attaque, passe) : ", f"M| {game._player_2.get_pseudo()} se décide à quoi faire")
                while action not in ['attaque','passe']:
                    self._server.send_msg_client(f"M| Entrée invalide. Veuillez saisir \"attaque\" pour attaquer ou \"passe\" pour passer.")
                    action = self._server.send_question_client(f"Q| {game._player_2.get_pseudo()}, choisissez une action (attaque, passe) : ", f"{game._player_2.get_pseudo()} se décide à quoi faire")
                if action == "attaque":
                    cible_attaquant_player_2 = self._server.send_question_client(f"""Q| Qui veux tu attaquer ?
Equipe adverse : {game._player_1.get_perso()[0]._nom}   {game._player_1.get_perso()[1]._nom}   {game._player_1.get_perso()[2]._nom}
La cible : """, f"M| {self._player_1.get_pseudo()} Choisis qui attaquer")
                    while True:
                        if cible_attaquant_player_2 == game._player_1.get_perso()[0]._nom:
                            cible_attaquant_player_2 = game._player_1.get_perso()[0]
                        elif cible_attaquant_player_2 == game._player_1.get_perso()[1]._nom:
                            cible_attaquant_player_2 = game._player_1.get_perso()[1]
                        elif cible_attaquant_player_2 == game._player_1.get_perso()[2]._nom:
                            cible_attaquant_player_2 = game._player_1.get_perso()[2]
                        else:
                            self._server.send_msg_client(f"""M| Entrée invalide. Veuillez saisir 
"{game._player_1.get_perso()[0]._nom}"  ou  "{game._player_1.get_perso()[1]._nom}"  ou  "{game._player_1.get_perso()[2]._nom}" """)
                            continue
                        print("Juste avant affichage de la helthbar")
                        if cible_attaquant_player_2.is_alive():
                            target = cible_attaquant_player_2
                            info_attack = player_2_attaquant.attack(target)
                            self._server.send_msg(info_attack, info_attack)
                            self._server.send_msg(target.show_healthbar(), target.show_healthbar())
                            break
                        else:
                            self._server.send_msg_client("M| Son perso est mort. Arrète de focus et choisis en un autre.")
                            continue
                    if team_alive(self._player_2.get_perso()):
                        pass
                    else:
                        self._server.send_msg(f"🏆 {self._player_2.get_pseudo()} remporte la victoire!", f"🏆 {self._player_2.get_pseudo()} remporte la victoire!")                        
                else:
                    pass                 

    
    def start(self):
        self._start = True

    def get_start(self):
        return self._start
    
def team_alive(equipe) -> bool:
    for i in range (2):
        if equipe[i].is_alive():
            return True
    return False

if __name__ == "__main__":
    server = Server()
    game = Game(server)
    server.start_server(game)
    if game.get_start:
        game.players()
        game.perso()
        game.play()
    
