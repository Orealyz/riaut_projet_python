import random

class Personnage:
    def __init__(self, nom: str, max_pv: int, attaque: int, defense: int, vitesse: int, nom_competence: str, nom_defense: str):
        self._nom = nom
        self._pv_max = max_pv
        self._pv_courant = max_pv
        self._attaque = attaque
        self._defense = defense
        self._vitesse = vitesse
        self._nom_competence = nom_competence
        self._nom_defense = nom_defense 
        self._passif_attaque_active = False
        

    def show_healthbar(self):
        missing_hp = self._pv_max - self._pv_courant
        healthbar = f"[{'❤️ ' * self._pv_courant}{'🖤' * missing_hp}] {self._pv_courant}/{self._pv_max}hp"
        print(healthbar)

    def compute_damages(self, target):
        return self._attaque

    def attack(self, target: 'Personnage'):
        if not self.is_alive():
            return
        damages = self.compute_damages(target)
        
        # Activation du passif d'attaque une seule fois si les PV sont inférieurs à 50
        if self._pv_courant < 20 and not self._passif_attaque_active:
            print(f"\n⚔️ {self._nom} active son passif et inflige {damages + 8} dégâts supplémentaires !")
            target.defense(damages + 8, self)
            self._passif_attaque_active = True  # Marquer le passif comme activé
        else:
            print(f"\n⚔️ {self._nom} attaque {target._nom} avec {self._nom_competence} (Dégâts: {self._attaque})")
            target.defense(damages, self)

        
    def defense(self, damages, attaquer: 'Personnage'):
        wounds = self.compute_defense(damages, attaquer)    
        print(f"🛡️ Grâce à {self._nom_defense}, {self._nom} prend {wounds} dégâts de {attaquer._nom} (Défense: {self._defense})")
        self.decrease_health(wounds)




    def compute_defense(self, damages, attaquer,):
        return damages - self._defense

    def decrease_health(self, amount):
        self._pv_courant -= amount
        if self._pv_courant < 0:
            self._pv_courant = 0

    def is_alive(self):
        return self._pv_courant > 0

    
    def __str__(self):
        return f"""👹 {self._nom} rentre dans la faille de l'invocateur 👺:
    💣 attack: {self._attaque} 
     defense: {self._defense}"""

if __name__ == "__main__":

    equipe1 = [
        Personnage("Sylvan", 30, 8, 4, 9, "Foudre", "Ombre"),
        Personnage("Ignis", 32, 10, 2, 7, "Brûlure", "Flamme"),
        Personnage("Zephyr", 30, 8, 5, 8, "Tourbillon", "Souffle")
    ]

    equipe2 = [
        Personnage("Thorn", 45, 9, 3, 6, "Épine", "Carapace"),
        Personnage("Aqua", 35, 7, 6, 5, "Vague", "Cascade"),
        Personnage("Zephyr", 30, 8, 5, 8, "Tourbillon", "Souffle")
    ]
    while equipe1 and equipe2 and equipe1[0].is_alive() and equipe2[0].is_alive():
        # Tour de l'équipe 1 (premier personnage)
        personnage1 = equipe1[0]
        if personnage1.is_alive():
            action = input(f"\nTour de {personnage1._nom}. Choisissez une action (1 pour attaquer, 0 pour passer) : ")
            while action not in ['0', '1']:
                print(f"Entrée invalide. Veuillez saisir 0 pour passer ou 1 pour attaquer.")
                action = input(f"\nTour de {personnage1._nom}. Choisissez une action (1 pour attaquer, 0 pour passer) : ")

            if action == '1':
                target = equipe2[0]
                personnage1.attack(target)
                target.show_healthbar()
            elif action == '0':
                print(f"{personnage1._nom} a passé son tour.")
                equipe2[0].show_healthbar()

        # Tour de l'équipe 2 (premier personnage)
        personnage2 = equipe2[0]
        if personnage2.is_alive():
            action = input(f"\nTour de {personnage2._nom}. Choisissez une action (1 pour attaquer, 0 pour passer) :") 
            while action not in ['0', '1']:
                print(f"Entrée invalide. Veuillez saisir 0 pour passer ou 1 pour attaquer.")
                action = input(f"\nTour de {personnage2._nom}. Choisissez une action (1 pour attaquer, 0 pour passer) : ")

            if action == '1':
                target = equipe1[0]
                personnage2.attack(target)
                target.show_healthbar()
            elif action == '0':
                print(f"{personnage2._nom} a passé son tour.")
                equipe1[0].show_healthbar()

        # Vérifier si le premier personnage de l'équipe 1 est mort
        if equipe1 and not equipe1[0].is_alive():
            print(f"\n{equipe1[0]._nom} est éliminé de l'équipe 1.")
            equipe1.pop(0)  # Retirer le personnage mort
            if equipe1:
                print(f"{equipe1[0]._nom} fait son entrée dans la faille")

        # Vérifier si le premier personnage de l'équipe 2 est mort
        if equipe2 and not equipe2[0].is_alive():
            print(f"\n{equipe2[0]._nom} est éliminé de l'équipe 2.")
            equipe2.pop(0)  # Retirer le personnage mort
            print(f"{equipe2[0]._nom} fait son entrée dans la faille")

    if equipe1 and equipe2:
        if equipe1[0].is_alive():
            print(f"\n🏆 L'équipe 1 remporte la victoire!")
        else:
            print(f"\n🏆 L'équipe 2 remporte la victoire!")
    else:
        print(f"\n🏆 L'équipe 2 remporte la victoire!")
