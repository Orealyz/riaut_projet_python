class Personnage:
    def __init__(self, nom: str, max_pv: int, attaque: int, defense: int, vitesse: int, nom_competence: str,nom_defense: str):
        self._nom = nom
        self._pv_max = max_pv
        self._pv_courant = max_pv
        self._attaque = attaque
        self._defense = defense
        self._vitesse = vitesse
        self._nom_competence = nom_competence
        self._nom_defense = nom_defense 

    def show_healthbar(self):
        missing_hp = self._pv_max - self._pv_courant
        healthbar = f"[{'♥' * self._pv_courant}{'♡' * missing_hp}] {self._pv_courant}/{self._pv_max}hp"
        print(healthbar)

    def compute_damages(self, target):
        return self._attaque

    def attack(self, target: 'Personnage'):
        if not self.is_alive():
            return
        damages = self.compute_damages(target)
        print(f"⚔️  {self._nom} attaque {target._nom} avec {self._nom_competence} (Dégâts: {self._attaque})")
        target.defense(damages, self)
        
    def compute_defense(self, damages, attaquer):
        return damages - self._defense  

    def defense(self, damages, attaquer: 'Personnage'):
        wounds = self.compute_defense(damages, attaquer)
        print(f"🛡️  Grâce à {self._nom_defense},  {self._nom} prend {wounds} dégâts de {attaquer._nom} (Défense: {self._defense})")  
        self.decrease_health(wounds)

    def decrease_health(self, amount):
        self._pv_courant -= amount
        if self._pv_courant < 0:
            self._pv_courant = 0

    def is_alive(self):
        return self._pv_courant > 0

    
    def __str__(self):
        return f"""👹 {self._nom} rentre dans la faille de l'invocateur 👺:
    💣 attack: {self._attaque} 
    ⛪ defense: {self._defense}"""


if __name__ == "__main__":
    personnage1 = Personnage("Sylvan", 110, 8, 4, 9, "Foudre", "Ombre")
    personnage2 = Personnage("Ignis", 120, 10, 2, 7, "Brûlure", "Flamme")
    personnage3 = Personnage("Zephyr", 90, 6, 5, 8, "Tourbillon", "Souffle")
    personnage4 = Personnage("Thorn", 140, 9, 3, 6, "Épine", "Carapace")
    personnage5 = Personnage("Aqua", 130, 7, 6, 5, "Vague", "Cascade")
    print(personnage1)
    print(personnage2)   
    while (personnage1.is_alive() and personnage2.is_alive()):
        
        personnage1.attack(personnage2)
        personnage2.show_healthbar()
        personnage2.attack(personnage1)
        personnage1.show_healthbar()
        print('\n')