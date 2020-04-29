"""
FACULTAD DE CIENCIAS, UNAM
SEMINARIO DE MATEMÁTICAS APLICADAS

-MUÑIZ MORALES ERICK, @ErickMM98
-GUZMÁN MORALES LÁZARO ABRAHAM

lu: 27/04/20
"""
import collections

from sympy.physics.units import kat

import readata
import networkx as nx
import matplotlib.pyplot as plt
from random import random, choice, seed
from itertools import combinations
from numpy import mean, sum


seed(a=315230372, version=2)
N = 600

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

pos_dic_1352 = {}
pos_dic_1433 = {}
pos_dic_1442 = {}
pos_dic_1451 = {}

lineup_by_key = {"1352":pos_dic_1352,
                 "1433":pos_dic_1433,
                 "1442":pos_dic_1442,
                 "1451":pos_dic_1451}


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

def make_table_analysis_lineup_team(hombres, mujeres, lineups):
    dic_lineup = {"1442":dict(number=0, hombres=0, mujeres=0, clustering=[], edge_conec=[], edge_conec_nd=[],
                                eigen=[], pg=[], pases=[]),
                  "1352": dict(number=0, hombres=0, mujeres=0, clustering=[], edge_conec=[], edge_conec_nd=[],
                                eigen=[], pg=[], pases=[]),
                  "1451":dict(number=0, hombres=0, mujeres=0, clustering=[], edge_conec=[], edge_conec_nd=[],
                                eigen=[], pg=[], pases=[]),
                  "1433":dict(number=0, hombres=0, mujeres=0, clustering=[], edge_conec=[], edge_conec_nd=[],
                                eigen=[], pg=[], pases=[]),
                  }
    print("GEN" + "&",
          "EQUIPO" + "&",
          "FORMACION" + "&",
          "p"+ "&",
          "$c$"+ "&",
          "$E_c$"+ "&",
          "$E_{nd}$" + "&",
          "prome_clus" + "&",
          "prome_eigen" + "&",
          "prome_PG" + "&",
          )
    r = 5
    for team in hombres:
        Dg = hombres[team]
        pases = sum([Dg[u][v]['weight'] for u, v in Dg.edges]) / (len(hombres) - 1)

        #clique = nx.algorithms.ap
        edge_conec = nx.edge_connectivity(Dg)
        edge_conec_nd = nx.edge_connectivity(Dg.to_undirected())
        ave_clus = round(nx.average_clustering(Dg,weight='weight'),r)
        eigenvector_centrality = mean(list(nx.eigenvector_centrality(Dg,weight='weight').values()))
        pagerank_centrality = mean(list(nx.pagerank(Dg, weight='weight').values()))

        dic_lineup[lineups[team]]["number"] += 1
        dic_lineup[lineups[team]]["hombres"] += 1
        dic_lineup[lineups[team]]["clustering"].append(ave_clus)
        dic_lineup[lineups[team]]["edge_conec"].append(edge_conec)
        dic_lineup[lineups[team]]["edge_conec_nd"].append(edge_conec_nd)
        dic_lineup[lineups[team]]["eigen"].append(eigenvector_centrality)
        dic_lineup[lineups[team]]["pg"].append(pagerank_centrality)
        dic_lineup[lineups[team]]["pases"].append(pases)

        print("H" +"&" ,
              team +"&" ,
              lineups[team] + "&" ,
              str(pases) + "&",
              #str(clique) + "&",
              str(edge_conec) + "&",
              str(edge_conec_nd) + "&",
              str(ave_clus) + "&",
              str(eigenvector_centrality) + "&",
              str(pagerank_centrality) + "\\" + "\\"
              )

    for team in mujeres:
        Dg = mujeres[team]
        pases = sum([Dg[u][v]['weight'] for u, v in Dg.edges]) / (len(mujeres) - 1)

        #clique = nx.algorithms.ap
        edge_conec = nx.edge_connectivity(Dg)
        edge_conec_nd = nx.edge_connectivity(Dg.to_undirected())
        ave_clus = round(nx.average_clustering(Dg,weight='weight'),r)
        eigenvector_centrality = mean(list(nx.eigenvector_centrality(Dg,weight='weight').values()))
        pagerank_centrality = mean(list(nx.pagerank(Dg, weight='weight').values()))

        dic_lineup[lineups[team]]["number"] += 1
        dic_lineup[lineups[team]]["mujeres"] += 1
        dic_lineup[lineups[team]]["clustering"].append(ave_clus)
        dic_lineup[lineups[team]]["edge_conec"].append(edge_conec)
        dic_lineup[lineups[team]]["edge_conec_nd"].append(edge_conec_nd)
        dic_lineup[lineups[team]]["eigen"].append(eigenvector_centrality)
        dic_lineup[lineups[team]]["pg"].append(pagerank_centrality)
        dic_lineup[lineups[team]]["pases"].append(pases)

        print("M" +"&" ,
              team +"&" ,
              lineups[team] + "&" ,
              str(pases) + "&",
              #str(clique) + "&",
              str(edge_conec) + "&",
              str(edge_conec_nd) + "&",
              str(ave_clus) + "&",
              str(eigenvector_centrality) + "&",
              str(pagerank_centrality) + "\\" + "\\"
              )
    #POR FORMACIÓN

    print("FORMACIÓN" +"&",
          "EQUIPOS" +"&",
          "H"+"&",
          "M"+"&",
          "Pases"+"&",
          "clus" +"&",
          "edge_c" +"&",
          "edge_nd"+"&",
          "eigen"+"&",
          "pg"+"\\"+"\\")
    for lup in dic_lineup:
        print(lup +"&",
              str(dic_lineup[lup]["number"]) +"&",
              str(dic_lineup[lup]["hombres"]) +"&",
              str(dic_lineup[lup]["mujeres"]) +"&",
              str(mean(dic_lineup[lup]["pases"]))+"&",
              str(mean(dic_lineup[lup]["clustering"])) +"&",
              str(mean(dic_lineup[lup]["edge_conec"]))+"&",
              str(mean(dic_lineup[lup]["edge_conec_nd"]))+"&",
              str(mean(dic_lineup[lup]["eigen"]))+"&",
              str(mean(dic_lineup[lup]["pg"])) +"\\"+"\\")




def make_table_analysis_players_team(G,team_data):
    """

    :param G: graph
    :param team_data: dic[ pos] = Player
    :return:
    """

    #EN LOS DATOS SÍ SE CUENTA EL GOL Y FAIL PARA CÁLCULOS

    r = 5

    degree = G.degree
    degree_centrality = nx.degree_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G,weight='weight')
    closeness_centrality = nx.closeness_centrality(G, distance='weight')
    eigenvector_centrality = nx.eigenvector_centrality(G,weight='weight')
    #katz_centrality = nx.katz_centrality(G, tol= 0.05,weight='weight')
    pagerank_centrality = nx.pagerank(G,weight='weight')
    clustering_data = nx.clustering(G, weight='weight')

    print("------------------------------*******TABLA******----------------------------")
    print("TEAM" + "&",
          "POS"+"&",
          "NAME" + "&",
          "$\delta$"+"&",
          "$\delta_{c}$"+"&",
          "$\delta_{bet}$"+"&",
          "$Clos$"+"&",
          "$E_c$"+"&",
          #"$Katz_c$" + "&",
          "$PR$"+"&",
          "Clus"+"\\")
    for p_pos in team_data:
        player = team_data[p_pos]
        player_name = player.name
        player_pos = player.pos
        player_degree = str(round(degree[player_pos],r)) + "&"
        player_degree_c = str( round(degree_centrality[player_pos],r) ) + "&"
        player_betwee_c = str( round(betweenness_centrality[player_pos],r)) + "&"
        player_closeness_c = str( round(closeness_centrality[player_pos],r)) + "&"
        player_eigen_c = str( round(eigenvector_centrality[player_pos],r) ) + "&"
        #player_katz_c = str( round(katz_centrality[player_pos],r) ) + "&"
        player_pagerank = str( round(pagerank_centrality[player_pos],r)) + "&"
        player_clustering = str( round(clustering_data[player_pos],r)) + "\\" +  "\\"
        print(player.name_team + "&",
                  player_pos + "&",
                  player_name + "&",
                  player_degree,
                  player_degree_c,
                  player_betwee_c,
                  player_closeness_c,
                  player_eigen_c,
                  #player_katz_c,
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
                        #print(next_pos,p_path.name_team,"NO TIENE ENEMIGOS")
                        continue
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
                        #print(next_pos, p_path.name_team, "NO TIENE ENEMIGOS")
                        continue
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

    return b_path, dic_team, team_graph


def simulate_hombres():
    team_lineup = readata.get_lineup_team_hombres()
    team_macth = combinations(team_lineup, 2)
    games = {}
    for team in team_lineup.keys():
        games[team] = []

    for macth in team_macth:
        print("JUEGO ---->  <<< ", macth[0], "vs", macth[1] ,">>>")
        teamA = "Pases_{}.csv".format(macth[0])
        teamB = "Pases_{}.csv".format(macth[1])

        lineupA = team_lineup[macth[0]] + ".csv"
        lineupB = team_lineup[macth[1]] + ".csv"

        macth_game = game(lineupA, lineupB,teamA, teamB, N)

        games[macth[0]].append(macth_game[1][macth[0]])
        games[macth[1]].append(macth_game[1][macth[1]])

    return games





def simulate_mujeres():
    team_lineup = readata.get_lineup_team_mujeres()
    team_macth = combinations(team_lineup, 2)

    games = {}
    for team in team_lineup.keys():
        games[team] = []

    for macth in team_macth:
        print("JUEGO ---->  <<< ", macth[0], "vs", macth[1], ">>>")
        teamA = "Pases_{}.csv".format(macth[0])
        teamB = "Pases_{}.csv".format(macth[1])

        lineupA = team_lineup[macth[0]] + ".csv"
        lineupB = team_lineup[macth[1]] + ".csv"

        macth_game = game(lineupA, lineupB, teamA, teamB, N)

        games[macth[0]].append(macth_game[1][macth[0]])
        games[macth[1]].append(macth_game[1][macth[1]])

    return games

def make_unic_grap_team(games_teams):
    dic_final = {}

    for team in games_teams:
        games = games_teams[team]
        team_dic = {}
        for game in games:
            for passing in game:
                try:
                    team_dic[passing] += game[passing]
                except:
                    team_dic[passing] = game[passing]
        dic_final[team] = team_dic
    return dic_final

def data_team_genders(teams):
    dic_final = {}
    for team in teams:
        teamA = "Pases_{}.csv".format(team)
        team_data_a = readata.get_all_data_team_passing_shooting(teamA)
        dic_final[team] = team_data_a
    return dic_final


if __name__ == '__main__':

    team_lineup_hombres = readata.get_lineup_team_hombres()
    games_hombres = simulate_hombres()
    final_team_hombres = make_unic_grap_team(games_hombres)
    final_graps_hombres = {}
    for team in final_team_hombres:
        tuplas = get_directed_list_digraph(final_team_hombres[team])
        final_graps_hombres[team] = gen_digraph_list_weight(tuplas)
    data_by_team_hombres = data_team_genders(team_lineup_hombres)

    #POR JUGADORS
    #for team in data_by_team_hombres:
    #    make_table_analysis_players_team(final_graps[team] , data_by_team_hombres[team])



    team_lineup_mujeres = readata.get_lineup_team_mujeres()
    games_mujeres = simulate_mujeres()
    final_team_mujeres = make_unic_grap_team(games_mujeres)
    final_graps_mujeres = {}
    for team in final_team_mujeres:
        tuplas = get_directed_list_digraph(final_team_mujeres[team])
        final_graps_mujeres[team] = gen_digraph_list_weight(tuplas)
    data_by_team_mujeres = data_team_genders(team_lineup_mujeres)

    make_table_analysis_lineup_team(final_graps_hombres, final_graps_mujeres,
                                    {**team_lineup_hombres,**team_lineup_mujeres})




    #for team in teams_hombres:
    #    print(team)
    #    print(len(teams_hombres[team]))
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