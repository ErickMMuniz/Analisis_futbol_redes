"""
FACULTAD DE CIENCIAS, UNAM
SEMINARIO DE MATEMÁTICAS APLICADAS

-MUÑIZ MORALES ERICK, @ErickMM98
-GUZMÁN MORALES LÁZARO ABRAHAM

lu: 27/04/20
"""

import csv
import os
import Player
import io
from itertools import combinations
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
    return os.listdir("data//linesup")

def get_lineup(lup):
    """
    Función que dada un nombre de la formación, se obtiene un diccionario con la información de las alineacion
    :param lup: String
    :return: dic con esa info
    """
    dic_final = {}
    line_up_list = []
    with open('data//linesup//{}'.format(lup), newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if row[0] == "init_player":
                dic_final["init_player"] = row[1]
            else:
                for i in range(1,len(row)):
                    if row[i] != "":
                        line_up_list.append( (row[0],row[i]) )
                    else:
                        continue
    dic_final["lineup"] = line_up_list
    return dic_final



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

def read_all_versus():
    """
    Función que lee toda la carpeta \versuslineup
    :return: iterable of roots
    """
    return os.listdir("data//versuslineup")

def get_versus(lup1,lup2):
    """
    Función que dado el nombre de las formaciones
    :param lup1: String
    :param lup2: String
    :return:
    """
    root = "{}_{}.csv".format(lup1[0:-4],lup2[0:-4])
    list_versus = []
    with open('data//versuslineup//{}'.format(root), newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            list_versus.append((row[0], row[1]))
    return list_versus

"""
----------------
- END VERSUS
----------------
"""

"""
----------------
- BEGIN DATA TEAM
----------------
"""
def get_lineup_team_hombres():
    """
    Función que da el diccionario con el nombre del equipo y su formación
    :param lup: String
    :return: dic con esa info
    """
    dic_final = {}
    with open('data//Premier_League_2018-2019//EquiposYFormaciones.csv', newline='',encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            dic_final[row[0]] = row[1]
    return dic_final

def get_lineup_team_mujeres():
    """
    Función que da el diccionario con el nombre del equipo y su formación
    :param lup: String
    :return: dic con esa info
    """
    dic_final = {}
    line_up_list = []
    with open('data//Mundial_Femenil_2019//PaisesYFormaciones.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            dic_final[row[0]] = row[1]
    return dic_final



def read_all_passing():
    """
    Función que lee toda la información de la carpeta passing
    :return:
    """
    return os.listdir("data//passing")

def read_all_shooting():
    """
    Función que lee toda la información de la carpeta \shooting
    :return:
    """
    return os.listdir("data//shooting")

def get_all_data_team_passing_shooting(team):
    """
    Función que regresa un diccionario con la llave POS y llave Player respectivo.
    :param team:
    :return: Dictionary
    """
    #print(team)
    root = team[6:]
    name_team = root[:-4]
    dic_final = {}
    #Para pases
    with open('data//passing//Pases_{}'.format(root), newline='',encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if row[0] != "" and row[0] != "Player":
                name = row[0]
                pos = row[1]
                medium = float(row[12])
                total_medium = float(row[13])
                large =  float(row[15])
                total_large = float(row[16])
                dic_stats = {"passing":{"medium":{"complete":medium,"total":total_medium},
                                        "large":{"complete":large,"total":total_large}
                                        }
                             }
                dic_final[pos] = Player.Player(name,pos,name_team,dic_stats)
    with io.open('data//shooting//Tiros_{}'.format(root), newline='',encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if row[0] != "" and row[0] != "Player":
                pos = row[1].split()[0]
                shoot = float(row[8])
                total_shoot = float(row[7])
                shooting = {"complete":shoot,"total":total_shoot}
                dic_final[pos].stats["shooting"] = shooting
    return dic_final

"""
----------------
- END DATA TEAM
----------------
"""

if __name__ == '__main__':
    print(get_lineup_team_mujeres())