# Simple interactive dungeon crawler
# This code was written for the AI courses in computer engineering at Université de Sherbrooke
# Author : Audrey Corbeil Therrien

from Games2D import *
from KillMonster import *

if __name__ == '__main__':
    # Niveau 0 - sans obstacle - 'assets/Mazes/mazeMedium_0'
    # Niveau 1 - avec obstacles - 'assets/Mazes/mazeMedium_1'
    # Niveau 2 - avec obstacles, portes et un ennemi - 'assets/Mazes/mazeMedium_2'
    # Niveau 2 - avec obstacles, portes et plusieurs ennemis - 'assets/Mazes/mazeMedium_2'
    maze = Maze('assets/Mazes/mazeMedium_3')
    maze.make_maze_wall_list()
    maze.make_maze_item_lists()    
    killMonster = KillMonster(1000,0.01,20,0.99,0.3,maze) #best config a date
    best = killMonster.genetic_algorithm()
    # print(best)
    # theAPP = App('assets/Mazes/mazeMedium_3')
    # theAPP.on_execute()