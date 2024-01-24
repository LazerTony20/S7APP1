import pygame
import random
from Constants import *


class Player_AI:


    def __init__(self,current_node, remaining_nodes):
        self.current_node = current_node
        self.remaining_nodes = remaining_nodes

    def get_instruction(self):
        if self.current_node == self.remaining_nodes[0]:
            print("This node has been reached : " + str(self.remaining_nodes.pop(0)))
            
        if self.current_node[0] < self.remaining_nodes[0][0]:
            instruction = "RIGHT"
        elif self.current_node[0] > self.remaining_nodes[0][0]:
            instruction = "LEFT"
        elif self.current_node[1] < self.remaining_nodes[0][1]:
            instruction = "DOWN"
        elif self.current_node[1] > self.remaining_nodes[0][1]:
            instruction = "UP"

        return instruction
