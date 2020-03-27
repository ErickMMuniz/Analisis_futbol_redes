"""
FACULTAD DE CIENCIAS, UNAM
SEMINARIO DE MATEMÁTICAS APLICADAS

-MUÑIZ MORALES ERICK, @ErickMM98
-GUZMÁN MORALES LÁZARO ABRAHAM

lu: 27/04/20
"""

import networkx as nx
import readata
from random import random
import matplotlib.pyplot as plt

"""
------------------------
- BEGIN AUXILIAR FUNCTIONS
------------------------
"""

def gen_graph_list(list_edges):
    """
    Funcion que genera una gráfica dada una lista de aristas
    :param list_edges:
    :return:
    """
    G = nx.Graph()
    G.add_edges_from(list_edges)
    return G



"""
------------------------
- END AUXILIAR FUNCTIONS
------------------------
"""

def game(lineupA,lineupB):
    #OBTENEMOS INFO
    data_a = readata.get_lineup(lineupA)
    data_b = readata.get_lineup(lineupB)
    data_versus = readata.get_versus(lineupA,lineupB)

    g_a = gen_graph_list(data_a["lineup"])
    g_b = gen_graph_list(data_b["lineup"])
    g_v = gen_graph_list(data_versus)

    nx.draw(g_a, with_labels=True)
    plt.show()






if __name__ == '__main__':
    game("433D.csv","433A.csv")