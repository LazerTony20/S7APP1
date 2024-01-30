import math as m 
import matplotlib.pyplot as plt
import pygame as pg

from Player import *
from Path_Finder import *
from Maze import *
from Constants import *
from swiplserver import PrologMQI as PMQI 
from KillMonster import *
from Constants import *
from FuzzLogic import *


class Player_AI:


    def __init__(self,current_node, remaining_nodes, perception, player_size, mazefile):
        self.current_node = current_node
        self.perception = perception
        self.player_size = player_size
        self.remaining_nodes = remaining_nodes
        self.maze = mazefile
        self.player = Player()
        self.fuzz_instance = Dodge(self.player, self.current_node, self.maze)

    def get_instruction(self):
        if self.current_node == self.remaining_nodes[0]:
            print("This node has been reached : " + str(self.remaining_nodes.pop(0)))
            
        if self.current_node[0] < self.remaining_nodes[0][0]:
            self.instruction = "RIGHT"
        elif self.current_node[0] > self.remaining_nodes[0][0]:
            self.instruction = "LEFT"
        elif self.current_node[1] < self.remaining_nodes[0][1]:
            self.instruction = "DOWN"
        elif self.current_node[1] > self.remaining_nodes[0][1]:
            self.instruction = "UP"
        self.instruction = self.fuzz_instance.to_dodge(self.perception,self.player_size, self.instruction)
        match self.instruction:
            case 'RIGHT':
                self.instruction = "RIGHT"
            case 'LEFT':
                self.instruction = "LEFT"
            case 'DOWN':
                self.instruction = "DOWN"
            case 'UP':
                self.instruction = "UP"
            case 'SLIGHTLY_LEFT':
                self.instruction = "LEFT"
            case 'SLIGHTLY_RIGHT':
                self.instruction = "RIGHT"
        return self.instruction
