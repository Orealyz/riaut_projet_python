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
        self._degats_subis = 0
        
    def show_healthbar(self):
        print(self._degats_subis)
        missing_hp = self._pv_max - self._pv_courant # 20
        if self._pv_max - self._degats_subis == self._pv_max - missing_hp:
                healthbar = f"[{'❤️' * self._pv_courant}{'💛' * abs(self._degats_subis)}] {self._pv_courant}/{self._pv_max}hp"
        else:
            if self._pv_courant == 0:
                healthbar = f"[{'💛' * self._degats_subis }{'🖤' * (self._pv_max - self._degats_subis)}] {self._pv_courant}/{self._pv_max}hp"
            else:
                healthbar = f"[{'❤️' * self._pv_courant}{'💛' * self._degats_subis }{'🖤' * (missing_hp - self._degats_subis)}] {self._pv_courant}/{self._pv_max}hp"
        return(healthbar)

    def compute_damages(self):
        return self._attaque

    def attack(self, target: 'Personnage') -> str and int:
        if not self.is_alive():
            return
        damages = self.compute_damages()
        passif_str = ""
        # Activation du passif d'attaque une seule fois si les PV sont inférieurs à 50
        if self._pv_courant < 20 and not self._passif_attaque_active:
            passif_str = f"\n⚔️ {self._nom} active son passif et inflige {damages + 8} dégâts !"
            damages = damages + 8
            self._passif_attaque_active = True  # Marquer le passif comme activé
        def_str, self._degats_subis = target.defense(damages, self)
        if passif_str == "":
            return(f"⚔️ {self._nom} attaque {target._nom} avec {self._nom_competence} (Dégâts: {self._attaque})\n{def_str}")
        else:
            return(f"{passif_str}\n⚔️ {self._nom} attaque {target._nom} avec {self._nom_competence} (Dégâts: {self._attaque})\n{def_str}")
        
    def defense(self, damages, attaquer: 'Personnage') -> str:
        wounds = self.compute_defense(damages, attaquer)    
        self.decrease_health(wounds)
        return(f"🛡️ Grâce à {self._nom_defense}, {self._nom} prend {wounds} dégâts de {attaquer._nom} (Défense: {self._defense})"), wounds

    def compute_defense(self, damages, attaquer):
        return damages - self._defense

    def decrease_health(self, amount):
        self._pv_courant -= amount
        self._degats_subis = amount
        if self._pv_courant < 0:
            self._degats_subis = amount - abs(self._pv_courant)
            self._pv_courant = 0
            

    def is_alive(self):
        return self._pv_courant > 0
    

    def __str__(self):
        return f"""👹 {self._nom} rentre dans la faille de l'invocateur 👺:
    💣 attack: {self._attaque} 
    ⛪ defense: {self._defense}"""

