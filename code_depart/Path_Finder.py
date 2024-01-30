# import pygame
# import random
# from Maze import *
import numpy as np
import csv
from Constants import *

class Path_Finder:

    def __init__(self, mazefile):
        # Code provenant de Maze.py
        self.labyrinthe = []
        self.position_debut = []
        self.position_fin = []
        with open(mazefile) as fichier_brut:
            # Read the entire contents of the file
            fichier_labyrinthe = csv.reader(fichier_brut, delimiter=',')
            for ligne in fichier_labyrinthe:
                self.labyrinthe.append(ligne)
        #print(self.labyrinthe)
        for i, row in enumerate(self.labyrinthe):
            for j, char in enumerate(row):
                if char == "S":
                    self.position_debut.append((j, i))  # Format : pos[0] = (X,Y), donc pos[0][0] = X et pos[0][1] = Y
                if char == "E":
                    self.position_fin.append((j, i))
        self.lignes = len(self.labyrinthe)
        self.colones = len(self.labyrinthe[0])

    def fct_heuristique(self, pos_a, pos_b):
        # Détermine le distance restante
        cout = abs(pos_a[0] - pos_b[0]) + abs(pos_a[1] - pos_b[1])
        return cout

    def validation_deplacement(self, position):
        return 0 <= position[0] < self.colones and 0 <= position[1] < self.lignes

    def find_path(self):
        open_set = set()
        closed_set = set()
        open_set.add((0 + self.fct_heuristique(self.position_debut[0], self.position_fin[0]), self.position_debut[0], tuple()))
        while open_set:
            current_cost, current_pos, current_path = min(open_set)
            #print(current_pos)
            #print(current_path)
            open_set.remove((current_cost, current_pos, current_path))
            if current_pos == self.position_fin[0]:
                print("========================Chemin Trouvé======================")
                return list(current_path) + [current_pos]
            closed_set.add(current_pos)
            adjacents = [(current_pos[0] + j, current_pos[1] + i) for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
            for adjacent in adjacents:
                if self.validation_deplacement(adjacent) and self.labyrinthe[adjacent[1]][adjacent[0]] in ['0','O','D', 'M']:
                    if adjacent not in closed_set:
                        new_cost = current_cost + 2 + self.fct_heuristique(adjacent, self.position_fin[0])
                        if not any(item[1] == adjacent for item in open_set) or new_cost < current_cost:
                            open_set.add((new_cost, adjacent, current_path + (current_pos,)))
                elif self.validation_deplacement(adjacent) and self.labyrinthe[adjacent[1]][adjacent[0]] in ['C', 'T','E']:
                    if adjacent not in closed_set:
                        new_cost = current_cost + 1 + self.fct_heuristique(adjacent, self.position_fin[0])
                        if not any(item[1] == adjacent for item in open_set) or new_cost < current_cost:
                            open_set.add((new_cost, adjacent, current_path + (current_pos,)))        
        print("No Path Found")
        return None
