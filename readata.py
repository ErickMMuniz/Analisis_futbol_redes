"""
FACULTAD DE CIENCIAS, UNAM
SEMINARIO DE MATEMÁTICAS APLICADAS

-MUÑIZ MORALES ERICK, @ErickMM98
-GUZMÁN MORALES LÁZARO ABRAHAM

lu: 27/04/20
"""

import csv
import os

"""
----------------
- BEGIN READ LINE UP
----------------
"""

def read_all_lineup():
    """
    Función que lee toda la carpeta \linesup
    :return: iterable of roots
    """
    return os.listdir("data\linesup")

def get_lineup(lup):
    """
    Función que dada un nombre de la formación, se obtiene una lista de tuplas con la respesctiva formación inicial.
    :param lup: String
    :return: list of tuples
    """
    
"""
----------------
- END READ LINE UP
----------------
"""

"""
----------------
- BEGIN VERSUS
----------------
"""


"""
----------------
- END VERSUS
----------------
"""