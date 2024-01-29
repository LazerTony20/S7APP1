# Université de Sherbrooke
# Code préparé par Audrey Corbeil Therrien
# Laboratoire 1 - Interaction avec prolog
import json
import sys
import os
chemin_parent = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(chemin_parent)
from Games2D import *
from swiplserver import PrologMQI

def test():
    #test porte
    path = os.path.join("tests","testPorte.JSON")
    with open(path, 'r') as fichier:
        data = json.load(fichier)
    with PrologMQI() as mqi:
        with PrologMQI() as mqi_file:
            with mqi_file.create_thread() as prolog_thread:
                result = prolog_thread.query("consult('./prolog/door.pl').")
                # result = prolog_thread.query("[door.pl].")
                for doorInfo in data:
                    result = prolog_thread.query("ouvrirPorte("+str(doorInfo["entree"])+", Cle).")
                    if result[0]["Cle"] != doorInfo["sortie"]:
                        print("Erreur dans le test de la porte: "+ str(doorInfo))
                        print("Cle attendue: "+str(doorInfo["sortie"]))
                        print("Cle obtenue: "+str(result[0]["Cle"]))
                        return False
    #test monstre
    maze = Maze('assets/Mazes/mazeLarge_3')
    maze.make_maze_wall_list()
    maze.make_maze_item_lists()    
    killMonster = KillMonster(1000,0.02,50,0.9,0.2,maze) #best config a date
    best = killMonster.genetic_algorithm()
    if(best["kill"] < 4):
        print("Erreur dans le test du monstre: "+ str(best))
        return False
    return True

test()