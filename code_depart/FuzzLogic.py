import numpy as np 
import math as m 
import matplotlib.pyplot as plt
import skfuzzy as sk
from skfuzzy import control

from Player import *
from Constants import*
from Maze import *

class Dodge:
    def __init__(self, player, current_node, mazefile):
        
        self.to_correct_and_dodge = []
        self.maze = None
        self.last_instruction = "DOWN" 
        self.last_position = None
        self.player = player
        self.position = current_node
        self.maze = Maze(mazefile)
        self.dodge = None
        self.dodge = self.initiate_fuzzy_logic_controller()
        
    def initiate_fuzzy_logic_controller(self):

        controller_rules = []
        #Input du contrôleur
        obstacle_position = control.Antecedent(np.linspace(-10, 10, 1000), 'obstacle_position')
        player_position = control.Antecedent(np.linspace(-10, 10, 1000), 'player_position')
        distance = control.Antecedent(np.linspace(0, 10, 1000), 'distance')
        #Output du contrôleur
        to_go_position = control.Consequent(np.linspace(-1,1,1000), 'to_direction')

        #Règles pour notre controlleur de logique floue

        obstacle_position['left'] = sk.trapmf(obstacle_position.universe, [-10, -10, -5, 0])
        obstacle_position['left-center'] = sk.trapmf(obstacle_position.universe, [-5, -2, 0, 0])
        obstacle_position['right-center'] = sk.trapmf(obstacle_position.universe, [0, 0, 2, 5])
        obstacle_position['right'] = sk.trapmf(obstacle_position.universe,[0, 5, 10, 10])

        player_position['left'] = sk.trapmf(player_position.universe, [-10, -10, -5, 0])
        player_position['left-center'] = sk.trapmf(player_position.universe, [-5, -2, 0, 0])
        player_position['right-center'] = sk.trapmf(player_position.universe, [0, 0, 2, 5])
        player_position['right'] = sk.trapmf(player_position.universe, [0, 5, 10, 10])

        distance['close'] = sk.trimf(distance.universe, [0, 0, 5])
        distance['mid'] = sk.trimf(distance.universe, [0, 5, 10])
        distance['far'] = sk.trimf(distance.universe, [5, 10, 10])

        to_go_position['left'] = sk.trapmf(to_go_position.universe, [-1, -1, -0.5, 0])
        to_go_position['straight'] = sk.trimf(to_go_position.universe, [-1, 0, 1])
        to_go_position['right'] = sk.trapmf(to_go_position.universe, [0, 0.5, 1, 1])

        # Rule for going straight when far or mid distance
        controller_rules.append(control.Rule(distance['far'], to_go_position['straight']))

        # controller_rules for turning left when mid & obstacle is on the left
        controller_rules.append(control.Rule(distance['mid'] & obstacle_position['left'] & player_position['left'], to_go_position['right']))
        controller_rules.append(control.Rule(distance['mid'] & obstacle_position['left'] & player_position['left-center'], to_go_position['right']))
        controller_rules.append(control.Rule(distance['mid'] & obstacle_position['left'] & player_position['right-center'], to_go_position['right']))
        controller_rules.append(control.Rule(distance['mid'] & obstacle_position['left'] & player_position['right'], to_go_position['right']))

        controller_rules.append(control.Rule(distance['mid'] & obstacle_position['left-center'] & player_position['left'], to_go_position['right']))
        controller_rules.append(control.Rule(distance['mid'] & obstacle_position['left-center'] & player_position['left-center'], to_go_position['right']))
        controller_rules.append(control.Rule(distance['mid'] & obstacle_position['left-center'] & player_position['right-center'], to_go_position['right']))
        controller_rules.append(control.Rule(distance['mid'] & obstacle_position['left-center'] & player_position['right'], to_go_position['right']))

        controller_rules.append(control.Rule(distance['mid'] & obstacle_position['right-center'] & player_position['left'], to_go_position['left']))
        controller_rules.append(control.Rule(distance['mid'] & obstacle_position['right-center'] & player_position['left-center'], to_go_position['left']))
        controller_rules.append(control.Rule(distance['mid'] & obstacle_position['right-center'] & player_position['right-center'], to_go_position['left']))
        controller_rules.append(control.Rule(distance['mid'] & obstacle_position['right-center'] & player_position['right'], to_go_position['left']))

        controller_rules.append(control.Rule(distance['mid'] & obstacle_position['right'] & player_position['left'], to_go_position['left']))
        controller_rules.append(control.Rule(distance['mid'] & obstacle_position['right'] & player_position['left-center'], to_go_position['left']))
        controller_rules.append(control.Rule(distance['mid'] & obstacle_position['right'] & player_position['right-center'], to_go_position['left']))
        controller_rules.append(control.Rule(distance['mid'] & obstacle_position['right'] & player_position['right'], to_go_position['left']))

        controller_rules.append(control.Rule(distance['close'] & obstacle_position['left'] & player_position['left'], to_go_position['right']))
        controller_rules.append(control.Rule(distance['close'] & obstacle_position['left'] & player_position['left-center'], to_go_position['right']))
        controller_rules.append(control.Rule(distance['close'] & obstacle_position['left'] & player_position['right-center'], to_go_position['right']))
        controller_rules.append(control.Rule(distance['close'] & obstacle_position['left'] & player_position['right'],to_go_position['right']))

        controller_rules.append(control.Rule(distance['close'] & obstacle_position['left-center'] & player_position['left'], to_go_position['right']))
        controller_rules.append(control.Rule(distance['close'] & obstacle_position['left-center'] & player_position['left-center'],to_go_position['right']))
        controller_rules.append(control.Rule(distance['close'] & obstacle_position['left-center'] & player_position['right-center'],to_go_position['right']))
        controller_rules.append(control.Rule(distance['close'] & obstacle_position['left-center'] & player_position['right'],to_go_position['right']))

        controller_rules.append(control.Rule(distance['close'] & obstacle_position['right-center'] & player_position['left'],to_go_position['left']))
        controller_rules.append(control.Rule(distance['close'] & obstacle_position['right-center'] & player_position['left-center'],to_go_position['left']))
        controller_rules.append(control.Rule(distance['close'] & obstacle_position['right-center'] & player_position['right-center'],to_go_position['left']))
        controller_rules.append(control.Rule(distance['close'] & obstacle_position['right-center'] & player_position['right'],to_go_position['left']))

        controller_rules.append(control.Rule(distance['close'] & obstacle_position['right'] & player_position['left'], to_go_position['left']))
        controller_rules.append(control.Rule(distance['close'] & obstacle_position['right'] & player_position['left-center'], to_go_position['left']))
        controller_rules.append(control.Rule(distance['close'] & obstacle_position['right'] & player_position['right-center'], to_go_position['left']))
        controller_rules.append(control.Rule(distance['close'] & obstacle_position['right'] & player_position['right'], to_go_position['left']))
        
        for rule_nbr in controller_rules:
            rule_nbr.and_func = np.fmin
            rule_nbr.or_func = np.fmax

        self.dodge_controller = control.ControlSystem(controller_rules)
        self.dodge = control.ControlSystemSimulation(self.dodge_controller)
        
        # for var in self.dodge.ctrl.fuzzy_variables:
        #     var.view()
        # plt.show()
      
    def to_dodge(self, obstacle, player, instruction):
        if self.dodge is None:
            self.initiate_fuzzy_logic_controller()
            
        if instruction == "DOWN" or instruction == "UP":
            canPassLeft = obstacle.left % self.maze.tile_size_x > player.width
            canPassRight = self.maze.tile_size_x - (obstacle.right % self.maze.tile_size_x) > player.width

            if canPassLeft or canPassRight:
                half = self.maze.tile_size_x // 2
                self.dodge.input['obstacle_position'] = (((obstacle.centerx % self.maze.tile_size_x) - half) * 10) / half
                self.dodge.input['player_position'] = (((player.centerx % self.maze.tile_size_x) - half) * 10) / half
            else:
                print("Player can't pass on the left or the right inside the tile")
                return "BLOCKED"

        else:
            canPassOver = obstacle.top % self.maze.tile_size_y > player.height
            canPassUnder = self.maze.tile_size_y - (obstacle.bottom % self.maze.tile_size_y) > player.height

            if canPassOver or canPassUnder:
                half = self.maze.tile_size_y // 2
                self.dodge.input['obstacle_position'] = (((obstacle.centery % self.maze.tile_size_y) - half) * 10) / half
                self.dodge.input['player_position'] = (((player.centery % self.maze.tile_size_y) - half) * 10) / half
            else:
                print("Player can't pass over or under the obstacle inside the tile")
                return "BLOCKED"
            
        if instruction == "UP":
            self.dodge.input['distance'] = ((player.top - obstacle.bottom))
        elif instruction == "RIGHT":
            self.dodge.input['distance'] = ((player.right - obstacle.left))
        elif instruction == "DOWN":
            self.dodge.input['distance'] = ((player.bottom - obstacle.top))
        elif instruction == "LEFT":
            self.dodge.input['distance'] = ((player.left - obstacle.right))
            
        self.dodge.compute()
        new_instruction = self.dodge.output["to_direction"]
        #to_go_position dans pour le jeu
        game_direction = self.decode_instruction(new_instruction,instruction)
        print("Instruction : ", instruction, "New Instruction : ", game_direction)
        return game_direction
    
    def decode_instruction(self,new,instruction):
        to_go_instruction = "DOWN"
        if new < 0:
            if instruction == "UP" or instruction == "DOWN":
                to_go_instruction = "LEFT"
            elif instruction == "RIGHT":
                to_go_instruction = "UP"
            elif instruction == "LEFT":
                to_go_instruction = "DOWN"
        elif new > 0:
            if instruction == "UP" or instruction == "DOWN":
                to_go_instruction = "RIGHT"
            elif instruction == "RIGHT":
                to_go_instruction = "DOWN"
            elif instruction == "LEFT":
                to_go_instruction = "UP"
        else:
            to_go_instruction = instruction
        return to_go_instruction

