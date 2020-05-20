from random import random as rd
import networkx as nx


def metric_defensive(G):
    """
    Función que da nuestra métrica defensiva.
    :param G: nx.DiGraph
    :return: dic[NODE] = Aij - Aji
    """
    nodes_m = {}
    d_in = dict(g.in_degree(weight="weight"))
    d_out = dict(g.out_degree(weight="weight"))
    for node in G.nodes:
        nodes_m[node] = d_out[node] - d_in[node]
    return nodes_m


if __name__ == '__main__':
    g = nx.DiGraph()

    g.add_edges_from([(1,2,{"weight":1}),
                      (2,3,{"weight":2}),(1,3,{"weight":1})])
    #print(dict(g.out_degree(weight="weight")))
    #print(dict(g.in_degree(weight="weight")))
    #print(defensive(g))
    #print("Hola.csv".split(".csv")[0])}
    print([]+[5,7,8])