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
                    self.position_debut.append((i, j))  # Format : pos[0] = (X,Y), donc pos[0][0] = X et pos[0][1] = Y
                if char == "E":
                    self.position_fin.append((i, j))
        self.lignes = len(self.labyrinthe)
        self.colones = len(self.labyrinthe[0])
        print("Lignes")
        print(self.lignes)
        print("Colones")
        print(self.colones)
        print("Pos debut")
        print(self.position_debut[0])
        print("Pos fin")
        print(self.position_fin[0])

    def fct_heuristique(self, pos_a, pos_b):
        # Détermine le distance restante
        #print(pos_a)
        #print(pos_b)
        cout = abs(pos_a[0] - pos_b[0]) + abs(pos_a[1] - pos_b[1])
        #print(cout)
        return cout

    def validation_deplacement(self, position):
        return 0 <= position[0] < self.lignes and 0 <= position[1] < self.colones


    # FROM HERE IT IS BROKEN    



    def find_path(self):
        open_set = set()
        closed_set = set()
        #iteration = 0
        open_set.add((0 + self.fct_heuristique(self.position_debut[0], self.position_fin[0]), self.position_debut[0], tuple()))

        while open_set:
            #print("Iteration")
            #print(iteration)
            #iteration = iteration + 1
            current_cost, current_pos, current_path = min(open_set)
            print(current_pos)
            #print(current_path)
            open_set.remove((current_cost, current_pos, current_path))

            if current_pos == self.position_fin[0]:
                print("==============================================Check 1")
                return list(current_path) + [current_pos]

            closed_set.add(current_pos)

            neighbors = [(current_pos[0] + i, current_pos[1] + j) for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]]

            for neighbor in neighbors:
                if self.validation_deplacement(neighbor) and self.labyrinthe[neighbor[0]][neighbor[1]] in ['0', 'C', 'T', 'O', 'E']:
                    if neighbor not in closed_set:
                        new_cost = current_cost + 1 + self.fct_heuristique(neighbor, self.position_fin[0])

                        if not any(item[1] == neighbor for item in open_set) or new_cost < current_cost:
                            open_set.add((new_cost, neighbor, current_path + (current_pos,)))
                            
        return None
