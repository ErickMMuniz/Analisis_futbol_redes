"""
FACULTAD DE CIENCIAS, UNAM
SEMINARIO DE MATEMÁTICAS APLICADAS

-MUÑIZ MORALES ERICK, @ErickMM98
-GUZMÁN MORALES LÁZARO ABRAHAM

lu: 27/04/20
"""

import networkx as nx
import readata
from random import random, choice
import matplotlib.pyplot as plt

"""
------------------------
- BEGIN AUXILIAR FUNCTIONS
------------------------
"""

def join_player_team(pos_player, pos_team):
    """
    FUNCIÓN QUE UNE ASOCIA LA POSICIÓN CON EL EQUIPO.
    :param player:
    :param team:
    :return:
    """
    return pos_player +"___"+ pos_team

def desjoin_player_team(player_team):
    """
    FUNCION QUE NOS SEPARA LO DE ARRIBA
    :param player_team:
    :return:
    """
    sep = player_team.split("___")
    return sep[0], sep[1]

def gen_graph_list(list_edges):
    """
    Funcion que genera una gráfica dada una lista de aristas
    :param list_edges:
    :return:
    """
    G = nx.Graph()
    G.add_edges_from(list_edges)
    return G

def get_nodes_str(G):
    """
    Función que nos da una lista de nodos como str
    :param G:
    :return:
    """
    list_nodes = []
    for node in G.nodes:
        list_nodes.append(node)
    return list_nodes

def get_vecinos_medium(G, node):
    """
    Funcion que nos regresa los vecinos a distancia 1
    :param G:
    :param node:
    :return:
    """
    list_node_final = []
    nodes = G[node]
    for node in nodes:
        list_node_final.append(node)
    return list_node_final

def get_vecinos_large(G,node):
    """
    Funcion que nos regresa los vecinos de distancia mayor a 1
    :param G:
    :param node:
    :return:
    """
    all_nodes = get_nodes_str(G)
    list_medium = get_vecinos_medium(G,node)
    sigulete = set()
    sigulete.add(node)
    return list(set(all_nodes) - set(list_medium) - sigulete)

def get_vecinos_versus(G,node):
    """
    Obtenemos los vecinos versus
    :param G:
    :param node:
    :return:
    """
    return get_vecinos_medium(G,node)


"""
------------------------
- END AUXILIAR FUNCTIONS
------------------------
"""

def game(lineupA,lineupB, teamA, teamB,N):
    """

    :param lineupA: DEBEN SER STRING CON LA TERMINACIÓN .CSV
    :param lineupB: DEBEN SER STRING CON LA TERMINACIÓN .CSV
    :param teamA: DEBEN SER STRING CON LA TERMINACIÓN .CSV
    :param teamB: DEBEN SER STRING CON LA TERMINACIÓN .CSV
    :return:
    """

    #OBTENEMOS INFO
    data_a = readata.get_lineup(lineupA)
    data_b = readata.get_lineup(lineupB)
    data_versus = readata.get_versus(lineupA,lineupB)

    #LISTA DE PLAYERS
    team_data_a = readata.get_all_data_team_passing_shooting(teamA)
    team_data_b = readata.get_all_data_team_passing_shooting(teamB)


    g_a = gen_graph_list(data_a["lineup"])
    g_b = gen_graph_list(data_b["lineup"])
    g_v = gen_graph_list(data_versus)

    init_a = data_a["init_player"]
    init_b = data_b["init_player"]

    team_graph = {team_data_a[init_a].name_team:
                      {"init": init_a, "lineup": g_a, "team_data":team_data_a, "versus":team_data_b[init_b].name_team },
                  team_data_b[init_b].name_team:
                      {"init": init_b, "lineup": g_b, "team_data":team_data_b, "versus":team_data_a[init_a].name_team },
                  }
    #INFORMACIÓN FINAL
    b_path = []


    #SIEMPRE INICIA A
    p_path = team_data_a[init_a]

    b_path.append(join_player_team(p_path.pos,p_path.name_team))


    n = 0
    for n in range(N):
        pos = p_path.pos
        lineup = team_graph[p_path.name_team]["lineup"]

        passing = p_path.stats["passing"]
        shooting = p_path.stats["shooting"]

        cobertura = passing["medium"]["complete"] + passing["large"]["complete"] + shooting["complete"]

        #DECIDIMOS SI PASE O TIRO A GOL
        if random() < shooting["complete"] / cobertura:
            #AQUI ES TIRO A GOL
            p = 0
            try:
                p = shooting["complete"] / shooting["total"]
            except:
                continue
            if random() < p:
                #GOL

                #AQUI MARCAMOS EL GOL
                goal_node = join_player_team("*GOAL*", p_path.name_team)
                b_path.append(goal_node)

                #PASAMOS AL OTRO EQUIPO
                team_change = team_graph[p_path.name_team]["versus"]
                pos_init_change = team_graph[team_change]["init"]
                p_path = team_graph[team_change]["team_data"][pos_init_change]
                b_path.append(join_player_team(p_path.pos, p_path.name_team))
            else:
                #NO GOL
                team_change = team_graph[p_path.name_team]["versus"]
                pos_init_change = "GK"
                p_path = team_graph[team_change]["team_data"][pos_init_change]
                b_path.append(join_player_team(p_path.pos, p_path.name_team))


        else:
            #AQUI ES PASE
            medium_pass = passing["medium"]
            large_pass = passing["large"]

            cobertura = medium_pass["complete"] + large_pass["complete"]

            if random() < medium_pass["complete"] / cobertura:
                #PASE CORTO MEDIO
                vecinos = get_vecinos_medium(lineup,pos)
                next_pos = choice(vecinos)
                p = 0
                try:
                    p = medium_pass["complete"] / medium_pass["total"]
                except:
                    continue
                if random() < p:
                    #PASE COMPLETO (ME MANTENGO EN EL EQUIPO
                    p_path = team_graph[p_path.name_team]["team_data"][next_pos]
                    b_path.append(join_player_team(p_path.pos, p_path.name_team))
                else:
                    #INTERCEPCION
                    versus = None
                    try:
                        versus = get_vecinos_versus(g_v,next_pos)
                        next_pos = choice(versus)
                    except:
                        print(next_pos,p_path.name_team,"NO TIENE ENEMIGOS")
                    team_change = team_graph[p_path.name_team]["versus"]
                    try:
                        p_path = team_graph[team_change]["team_data"][next_pos]
                        b_path.append(join_player_team(p_path.pos, p_path.name_team))
                    except:
                        singulete_af = set()
                        singulete_af.add(next_pos)
                        next_pos = choice(list(set(versus) - singulete_af))
                        p_path = team_graph[team_change]["team_data"][next_pos]
                        b_path.append(join_player_team(p_path.pos, p_path.name_team))
            else:
                #PASE LARGO
                vecinos = get_vecinos_large(lineup, pos)
                next_pos = choice(vecinos)
                p = 0
                try:
                    p = large_pass["complete"] / large_pass["total"]
                except:
                    continue
                if random() < p:
                    # PASE COMPLETO (ME MANTENGO EN EL EQUIPO
                    p_path = team_graph[p_path.name_team]["team_data"][next_pos]
                    b_path.append(join_player_team(p_path.pos, p_path.name_team))
                else:
                    # INTERCEPCION
                    versus = None
                    try:
                        versus = get_vecinos_versus(g_v, next_pos)
                        next_pos = choice(versus)
                    except:
                        print(next_pos, p_path.name_team, "NO TIENE ENEMIGOS")
                    team_change = team_graph[p_path.name_team]["versus"]
                    try:
                        p_path = team_graph[team_change]["team_data"][next_pos]
                        b_path.append(join_player_team(p_path.pos, p_path.name_team))
                    except:
                        singulete_af = set()
                        singulete_af.add(next_pos)
                        next_pos = choice(list(set(versus) - singulete_af))
                        p_path = team_graph[team_change]["team_data"][next_pos]
                        b_path.append(join_player_team(p_path.pos, p_path.name_team))

    return b_path









if __name__ == '__main__':
    print(len(game("433D.csv","433A.csv", "Pases_EUA.csv","Pases_Holanda.csv",1000)))
    #team_data_a = readata.get_all_data_team_passing_shooting("Pases_EUA.csv")
    #team_data_b = readata.get_all_data_team_passing_shooting("Pases_Holanda.csv")
    #print(len(team_data_b))
    #print(len(team_data_a))