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
        healthbar = f"[{'❤️' * self._pv_courant}{'🖤' * missing_hp}] {self._pv_courant}/{self._pv_max}hp"
        return(healthbar)

    def compute_damages(self, target):
        return self._attaque

    def attack(self, target: 'Personnage') -> str:
        if not self.is_alive():
            return
        damages = self.compute_damages(target)
        
        # Activation du passif d'attaque une seule fois si les PV sont inférieurs à 50
        if self._pv_courant < 20 and not self._passif_attaque_active:
            print(f"\n⚔️ {self._nom} active son passif et inflige {damages + 8} dégâts supplémentaires !")
            target.defense(damages + 8, self)
            self._passif_attaque_active = True  # Marquer le passif comme activé
        else:
            def_str = target.defense(damages, self)
            return(f"⚔️ {self._nom} attaque {target._nom} avec {self._nom_competence} (Dégâts: {self._attaque})\n{def_str}")

        
    def defense(self, damages, attaquer: 'Personnage') -> str:
        wounds = self.compute_defense(damages, attaquer)    
        self.decrease_health(wounds)
        return(f"🛡️ Grâce à {self._nom_defense}, {self._nom} prend {wounds} dégâts de {attaquer._nom} (Défense: {self._defense})")

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

 