"""
FACULTAD DE CIENCIAS, UNAM
SEMINARIO DE MATEMÁTICAS APLICADAS

-MUÑIZ MORALES ERICK, @ErickMM98
-GUZMÁN MORALES LÁZARO ABRAHAM

lu: 27/04/20
"""
import collections

import readata
import networkx as nx
import matplotlib.pyplot as plt
from random import random, choice
from itertools import combinations

N = 1000

pos_dic_433D = {"GK": (3,0),
               "LB": (1,1),
               "CBL": (2,1),
               "CBR": (4,1),
               "RB": (5,1),
               "DM": (3,2),
               "CML": (2,3),
               "CMR": (4,3),
               "FW": (3,5),
               "LW": (1,4),
               "RW": (5,4),
               "FAIL": (2,7),
               "GOAL": (4,7)}

pos_dic_433A = {"GK": (3,0),
               "LB": (1,1),
               "CBL": (2,1),
               "CBR": (4,1),
               "RB": (5,1),
               "AM": (3,4),
               "CML": (2,3),
               "CMR": (4,3),
               "FW": (3,6),
               "LW": (1,5),
               "RW": (5,5),
               "FAIL": (2,8),
               "GOAL": (4,8)}


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

def gen_digraph_list_weight(list_edges):
    """
    Función que genera una gráfica dirigida con pesos
    :param list_edges:
    :return:
    """
    D = nx.DiGraph()
    D.add_edges_from(list_edges)
    return D

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

def count_edge_dic(dic_team,edge):
    """
    Función que cuenta los pases
    :param dic_team:
    :param edge:
    :return:
    """
    if edge in dic_team:
        dic_team[edge] += 1
    else:
        dic_team[edge] = 1

def get_directed_list_digraph(dic_team):
    """
    Función auxiliar para obtener una lista de
                [(SOURCE , TARGET , {"WEIGHT" : PASES})]
    :param dic_team:
    :return: list
    """
    list_final_digraph = []
    for edge in dic_team:
        pases = dic_team[edge]
        list_final_digraph.append((edge[0],edge[1],{"weight":pases}) )
    return list_final_digraph



"""
------------------------
- END AUXILIAR FUNCTIONS
------------------------
"""

def make_table_analysis_players_team(G,team_data):
    """

    :param G: graph
    :param team_data: dic[ pos] = Player
    :return:
    """

    #EN LOS DATOS SÍ SE CUENTA EL GOL Y FAIL PARA CÁLCULOS

    degree = G.degree
    degree_centrality = nx.degree_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)
    closeness_centrality = nx.closeness_centrality(G)
    eigenvector_centrality = nx.eigenvector_centrality(G)
    pagerank_centrality = nx.pagerank(G)

    clustering_data = nx.clustering(G)
    print("*******TABLA******")
    print("NAME"+"&",
          "POS"+"&",
          "DEGREE"+"&",
          "DEGRE_C"+"&",
          "BETW"+"&",
          "CLOSE_C"+"&",
          "EIGEN_C"+"&",
          "PAGERANK"+"&",
          "CLUSTERING"+"\\")
    for p_pos in team_data:
        player = team_data[p_pos]
        player_name = player.name
        player_pos = player.pos
        player_degree = str(degree[player_pos]) + "&"
        player_degree_c = str(degree_centrality[player_pos]) + "&"
        player_betwee_c = str(betweenness_centrality[player_pos]) + "&"
        player_closeness_c = str(closeness_centrality[player_pos]) + "&"
        player_eigen_c = str(eigenvector_centrality[player_pos]) + "&"
        player_pagerank = str(pagerank_centrality[player_pos]) + "&"
        player_clustering = str(clustering_data[player_pos]) + "\\"
        print(player_name+ "&",
                  player_pos + "&",
                  player_degree,
                  player_degree_c,
                  player_betwee_c,
                  player_closeness_c,
                  player_eigen_c,
                  player_pagerank,
                  player_clustering)

"""
------------------------
- BEGIN ANALISYS FUNCTIONS
------------------------
"""


def plot_fancy_graph(Dg,name_team, formation):
    weights = [Dg[u][v]['weight'] for u, v in Dg.edges]
    plt.title(name_team)
    nx.draw(Dg, with_labels="TRUE", width=weights, pos=formation)
    plt.show()


def plot_degre_distribution(G):
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())
    fig, ax = plt.subplots()
    plt.bar(deg, cnt, width=0.80, color='b')

    plt.title("Degree Histogram")
    plt.ylabel("Count")
    plt.xlabel("Degree")
    ax.set_xticks([d + 0.4 for d in deg])
    ax.set_xticklabels(deg)

    plt.show()


"""
------------------------
- END ANALISYS FUNCTIONS
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
    dic_edge_A = {}
    dic_edge_B = {}

    dic_team = {team_data_a[init_a].name_team:dic_edge_A,
                team_data_b[init_b].name_team:dic_edge_B}

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
                edge = (pos,"GOAL")
                count_edge_dic(dic_team[p_path.name_team],edge)

                goal_node = join_player_team("GOAL", p_path.name_team)
                b_path.append(goal_node)

                #PASAMOS AL OTRO EQUIPO
                team_change = team_graph[p_path.name_team]["versus"]
                pos_init_change = team_graph[team_change]["init"]
                p_path = team_graph[team_change]["team_data"][pos_init_change]
                b_path.append(join_player_team(p_path.pos, p_path.name_team))
            else:
                #NO GOL
                edge = (pos, "FAIL")
                count_edge_dic(dic_team[p_path.name_team], edge)

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
                    edge = (pos, next_pos)
                    count_edge_dic(dic_team[p_path.name_team], edge)

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
                        try:
                            next_pos = choice(list(set(versus) - singulete_af))
                        except:
                            continue
                        try:
                            p_path = team_graph[team_change]["team_data"][next_pos]
                            b_path.append(join_player_team(p_path.pos, p_path.name_team))
                        except:
                            pos_init_change = team_graph[team_change]["init"]
                            p_path = team_graph[team_change]["team_data"][pos_init_change]
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
                    edge = (pos, next_pos)
                    count_edge_dic(dic_team[p_path.name_team], edge)

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

    return b_path, dic_team, team_graph


def simulate_hombres():
    team_lineup = readata.get_lineup_team_hombres()
    team_macth = combinations(team_lineup, 2)
    games = {}
    for team in team_lineup.keys():
        games[team] = []

    for macth in team_macth:
        print("juego----", macth[0],"vs", macth[1])
        teamA = "Pases_{}.csv".format(macth[0])
        teamB = "Pases_{}.csv".format(macth[1])

        lineupA = team_lineup[macth[0]] + ".csv"
        lineupB = team_lineup[macth[1]] + ".csv"

        macth_game = game(lineupA, lineupB,teamA, teamB, N)

        games[macth[0]].append( gen_digraph_list_weight(get_directed_list_digraph(macth_game[1][macth[0]])))
        games[macth[1]].append( gen_digraph_list_weight(get_directed_list_digraph(macth_game[1][macth[1]])))

    return games





def simulate_mujeres():
    team_lineup = readata.get_lineup_team_mujeres()
    team_macth = combinations(team_lineup, 2)

    games = {}
    for team in team_lineup.keys():
        games[team] = []

    for macth in team_macth:
        print("juego----", macth[0], "vs", macth[1])
        teamA = "Pases_{}.csv".format(macth[0])
        teamB = "Pases_{}.csv".format(macth[1])

        lineupA = team_lineup[macth[0]] + ".csv"
        lineupB = team_lineup[macth[1]] + ".csv"

        macth_game = game(lineupA, lineupB, teamA, teamB, N)

        games[macth[0]].append(macth_game[1][macth[0]])
        games[macth[1]].append(macth_game[1][macth[1]])

    return games

if __name__ == '__main__':

    teams_hombres = simulate_hombres()

    for team in teams_hombres:
        print(team)
        print(teams_hombres[team][0].edges)
    """
    A = game("433D.csv", "433A.csv", "Pases_EUA.csv", "Pases_Holanda.csv", 1000)
    #A = game("433D.csv","433A.csv", "Pases_Liverpool.csv","Pases_Tottenham.csv",1000)

    juego = A[1]

    team_view = "Holanda"
    c = get_directed_list_digraph(juego[team_view])
    D = gen_digraph_list_weight(c)

    make_table_analysis_players_team(D, A[2][team_view]["team_data"])

    plot_fancy_graph(D,team_view,pos_dic_433A)

    plot_degre_distribution(D)
    """