"""
FACULTAD DE CIENCIAS, UNAM
SEMINARIO DE MATEMÁTICAS APLICADAS

-MUÑIZ MORALES ERICK, @ErickMM98
-GUZMÁN MORALES LÁZARO ABRAHAM

lu: 27/04/20
"""

class Player():
    """
    Clase que define a un jugador
    """
    def __init__(self, name,pos,stats):
        self.name = name
        self.pos = pos
        self.stats = stats
        self.balon = None
        self.count_balon = 0

    def __repr__(self):
        return "<{}-{}>".format(self.pos,self.name)