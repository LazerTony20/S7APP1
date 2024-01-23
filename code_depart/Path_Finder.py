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
        with open(mazefile, 'r') as fichier_brut:
            # Read the entire contents of the file
            fichier_labyrinthe = csv.reader(fichier_brut, delimiter=',')
            for colone in fichier_labyrinthe:
                self.labyrinthe.append(colone)
        for i, row in enumerate(self.labyrinthe):
            for j, char in enumerate(row):
                if char == "S":
                    self.position_debut.append((i, j))
                if char == "E":
                    self.position_fin.append((i, j))
        self.lignes = len(self.labyrinthe)
        self.colones = len(self.labyrinthe[0])
        #print(self.lignes)
        #print(self.colones)
        #print(self.position_debut)
        #print(self.position_fin)


    # FROM HERE IT IS BROKEN    

    def heuristic_cost_estimate(self, pos_debut, pos_fin):
        return abs(pos_debut[0] - pos_fin[0]) + abs(pos_debut[1] - pos_fin[1])

    def is_valid_move(self, position):
        return 0 <= position[0] < self.lignes and 0 <= position[1] < self.colones

    def find_path(self):
        open_set = set()
        closed_set = set()

        open_set.add((0 + self.heuristic_cost_estimate(self.position_debut, self.position_fin), self.position_debut, tuple()))

        while open_set:
            current_cost, current_pos, current_path = min(open_set)
            open_set.remove((current_cost, current_pos, current_path))

            if current_pos == self.position_fin:
                return list(current_path) + [current_pos]

            closed_set.add(current_pos)

            neighbors = [(current_pos[0] + i, current_pos[1] + j) for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]]

            for neighbor in neighbors:
                if self.is_valid_move(neighbor) and self.labyrinthe[neighbor[0], neighbor[1]] in ['C', 'T', 'O', '0']:
                    if neighbor not in closed_set:
                        new_cost = current_cost[0] + 1 + self.heuristic_cost_estimate(neighbor, self.position_fin)

                        if not any(item[1] == neighbor for item in open_set) or new_cost < current_cost[0]:
                            open_set.add((new_cost, neighbor, current_path + (current_pos,)))
                            return None
