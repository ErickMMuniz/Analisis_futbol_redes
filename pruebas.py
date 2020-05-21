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

def list_dic_maximo(dic_nodes):
    list_final = []
    max(dic_nodes, key=dic_nodes.get)
    return 1

def get_edges_shortpath(path):
    list_edges = list()
    for i in range(len(path)-1):
        list_edges.append((path[i],path[i+1]))
    return  list_edges


if __name__ == '__main__':
    g = nx.DiGraph()

    g.add_edges_from([("GK","CBL",{"weight":1, "capacity":1}),
                      ("CBL","GOAL",{"weight":2, "capacity":2}),("GK","GOAL",{"weight":1,"capacity":1})])
    #print(dict(g.out_degree(weight="weight")))
    #print(dict(g.in_degree(weight="weight")))
    #print(defensive(g))
    #print("Hola.csv".split(".csv")[0])}
    #print([]+[5,7,8])
    #max_flow = nx.maximum_flow(g, _s=1, _t=3, capacity="weight")
    #a = {"a":1,"b":2,"c":2}
    #beta = max(a, key=a.get)
    #print(beta)

    #print(
    A=nx.shortest_path(g,source="GK",target="GOAL",weight="weight")
    print(A)
    print(get_edges_shortpath(A))