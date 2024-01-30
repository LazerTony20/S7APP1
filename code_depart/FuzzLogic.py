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

    def initiate_fuzzy_logic_controller(self):

        controller_rules = []
        #Input du contrôleur
        ob_position = control.Antecedent(np.arange(-10, 11, 1), 'ob_position')
        p_position = control.Antecedent(np.arange(-10, 11, 1), 'p_position')
        #Output du contrôleur
        inst_distance = control.Consequent(np.arange(0, 11, 1), 'inst_distance')
        to_go_position = control.Consequent(np.arange(-1,2,1), 'to_direction')

        #Règles pour notre controlleur de logique floue
        to_go_position['right'] = sk.trimf(to_go_position.universe, [-1, -1, 0.25])
        to_go_position['straight'] = sk.trimf(to_go_position.universe, [-0.25, 0, 0.25])
        to_go_position['left'] = sk.trimf(to_go_position.universe, [-0.25, 1, 1])

        inst_distance['far'] = sk.trimf(inst_distance.universe, [5,10,10])
        inst_distance['mid'] = sk.trimf(inst_distance.universe, [0,5,10])
        inst_distance['close'] = sk.trimf(inst_distance.universe, [0,0,5])

        p_position['left'] = sk.trimf(p_position.universe, [-10, -10, 2])
        p_position['center'] = sk.trimf(p_position.universe, [0, 0, 0])
        p_position['right'] = sk.trimf(p_position.universe, [-10, -10, 2])

        ob_position['left'] = sk.trimf(ob_position.universe, [-10, -10, 2])
        ob_position['center'] = sk.trimf(ob_position.universe, [0, 0, 0])
        ob_position['right'] = sk.trimf(ob_position.universe, [-10, -10, 2])
        

        # Rule for going straight when far or mid distance

        rule_straight = control.Rule(inst_distance['far'] | inst_distance['mid'], to_go_position['straight'])
        controller_rules.append(rule_straight)

         # Rule for turning left when close and obstacle is on the right
        rule_left = control.Rule(inst_distance['close'] & ob_position['right'], to_go_position['left'])
        controller_rules.append(rule_left)

        # Rule for turning right when close and obstacle is on the left
        rule_right = control.Rule(inst_distance['close'] & ob_position['left'], to_go_position['right'])
        controller_rules.append(rule_right)

        # Default rule (go straight)
        rule_default = control.Rule(~(rule_left.antecedent | rule_right.antecedent | rule_straight.antecedent), to_go_position['straight'])
        controller_rules.append(rule_default)

        """ # Rule for going straight when far or mid distance
        controller_rules.append(control.Rule(inst_distance['far'] or inst_distance['mid'], to_go_position['straight']))

        # Rules for turning left when close and obstacle is on the right
        controller_rules.append(control.Rule(inst_distance['close'] and ob_position['right'], to_go_position['left']))

        # Rules for turning right when close and obstacle is on the left
        controller_rules.append(control.Rule(inst_distance['close'] and ob_position['left'], to_go_position['right']))

        # Default rule (go straight)
        controller_rules.append(control.Rule(inst_distance['close'] and ob_position['left'] and ob_position['right'], to_go_position['straight'])) """

        """       #Si objet loin, continue
        controller_rules.append(control.Rule(inst_distance['far'], to_go_position['straight']))
        controller_rules.append(control.Rule(inst_distance['mid'], to_go_position['straight']))

        #Rules for turning left
        controller_rules.append(control.Rule(inst_distance['close'] & ob_position['right'], to_go_position['left']))
        controller_rules.append(control.Rule(inst_distance['close'] & ob_position['left'] & p_position['right'], to_go_position['left']))
        controller_rules.append(control.Rule(inst_distance['close'] & ob_position['center'] & p_position['left'], to_go_position['left']))

        # Rules for turning right
        controller_rules.append(control.Rule(inst_distance['close'] & ob_position['left'], to_go_position['right']))
        controller_rules.append(control.Rule(inst_distance['close'] & ob_position['right'] & p_position['left'], to_go_position['right']))
        controller_rules.append(control.Rule(inst_distance['close'] & ob_position['center'] & p_position['right'], to_go_position['right']))

        # Default rule (go straight)
        controller_rules.append(control.Rule(inst_distance['close'], to_go_position['straight'])) """

        

        for rule_nbr in controller_rules:
            rule_nbr.and_func = np.fmin
            rule_nbr.or_func = np.fmax

        self.dodge_controller = control.ControlSystem(controller_rules)
        self.dodge = control.ControlSystemSimulation(self.dodge_controller)
      
        """ Exemple Lab
        ant1 = ctrl.Antecedent(np.linspace(-1, 1, 1000), 'input1')
        ant2 = ctrl.Antecedent(np.linspace(-1, 1, 1000), 'input2')
        cons1 = ctrl.Consequent(np.linspace(-1, 1, 1000), 'output1', defuzzify_method='centroid')
        cons1.accumulation_method = np.fmax
        ant1['membership1'] = fuzz.trapmf(ant1.universe, [-1, -0.5, 0.5, 1])
        ant1['membership2'] = fuzz.trapmf(ant1.universe, [-0.75, -0.5, 0.5, 0.75])

        ant2['membership1'] = fuzz.trapmf(ant1.universe, [-1, -0.5, 0.5, 1])

        cons1['membership1'] = fuzz.trimf(cons1.universe, [-1, 0, 1])
        rules = []
        rules.append(ctrl.Rule(antecedent=(ant1['membership1'] & ant2['membership1']), consequent=cons1['membership1']))
        for rule in rules:
            rule.and_func = np.fmin
            rule.or_func = np.fmax

        system = ctrl.ControlSystem(rules)
        sim = ctrl.ControlSystemSimulation(system)"""

    def to_dodge(self, perception, player_size, instruction):

        #Vérifié que le joueur voit un objet dans sa perception, return dernière instruction
        perception_lenght = len(perception[1])
        if perception_lenght == 0:
            return instruction
        
        
        p_hitbox = player_size
        p_pos = self.position

        ob_hitbox = (perception[1][0].width, perception[1][0].height)
        ob_pos = (perception[1][0].x, perception[1][0].y)
        ob_mapped = (ob_pos[0] % int(self.maze.tile_size_x), ob_pos[1] % int(self.maze.tile_size_y))

        #Portée des obstacles, max x = 52, max y = 63
        ob_mapped = (self.calculate_new_ob_pos(ob_mapped[0], 0, 52, 100, 0), self.calculate_new_ob_pos(ob_mapped[1], 0, 59, 100, 0))
        
        self.initiate_fuzzy_logic_controller()
        if instruction == "DOWN" or instruction == "UP":
            self.dodge.input['p_position'] = ob_mapped[0]
        else:
            self.dodge.input['p_position'] = ob_mapped[1]
        self.dodge.compute()
        new_instruction = self.dodge.output["to_direction"]
        #Direction dans pour le jeu
        game_direction = self.decode_instruction(new_instruction)
        return game_direction

    def calculate_new_ob_pos(self, value, minimum, maximum, new_minimum, new_maximum):
        return (value - minimum) * (new_maximum - new_minimum) / (maximum - minimum) + new_minimum
    
    def decode_instruction(self,instruction):
        to_go_instruction = "DOWN"
        match instruction:
            case -2:
                to_go_instruction = "LEFT"
            case -1:
                to_go_instruction = "SLIGHTLY_LEFT"
            case 0:
                to_go_instruction = "DOWN"
            case 1:
                to_go_instruction = "SLIGHTLY_RIGHT"
            case 2:
                to_go_instruction = "RIGHT"
        return to_go_instruction

