class Player:
    
    def __init__(self, pseudo: str):
        self._pseudo = pseudo
        self._perso = None

    def get_pseudo(self):
        return self._pseudo
    
    def get_perso(self):
        return self._perso
    
    def set_perso(self, characters):
        self._perso = characters
    
