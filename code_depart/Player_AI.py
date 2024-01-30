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
        self.player = player_size
        self.lastPosition = self.player.get_rect().center
        self.stuck = 0
        self.counter = 0
        self.obstacle = None
        self.fuzz_instance = Dodge(self.player, self.current_node, self.maze)
        
    def obstacleDansLeChemin(self, obstacles, player, instruction):
        for obstacle in obstacles:
            if instruction == "UP" and obstacle.centery < player.centery:
                if player.left < obstacle.right and player.right > obstacle.left:
                    self.obstacle = obstacle
                    return True
            elif instruction == "DOWN" and obstacle.centery > player.centery:
                if player.left < obstacle.right and player.right > obstacle.left:
                    self.obstacle = obstacle
                    return True
            elif instruction == "RIGHT" and obstacle.centerx > player.centerx:
                if player.bottom > obstacle.top and player.top < obstacle.bottom:
                    self.obstacle = obstacle
                    return True
            elif instruction == "LEFT" and obstacle.centerx < player.centerx:
                if player.bottom > obstacle.top and player.top < obstacle.bottom:
                    self.obstacle = obstacle
                    return True

        return False
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
        print(self.perception[1])
        print(len(self.perception[1]))
        if(len(self.perception[1]) != 0):
            if self.obstacleDansLeChemin(self.perception[1], self.player_size, self.instruction) == True:
                print("obstacle dans le chemin")
                self.instruction = self.fuzz_instance.to_dodge(self.obstacle,self.player_size, self.instruction)
        if self.player.get_rect().center == self.lastPosition:
            self.stuck += 1
            if self.stuck >= 5:
                self.counter += 1
        print("origine",self.instruction)
        if self.counter > 0 and self.counter <= 10:
            self.counter += 1
            match self.instruction:
                    case 'RIGHT':
                        self.instruction = "LEFT"
                    case 'LEFT':
                        self.instruction = "RIGHT"
                    case 'DOWN':
                        self.instruction = "UP"
                    case 'UP':
                        self.instruction = "DOWN"
                    case "BLOCKED":
                        self.instruction = "BLOCKED"
            self.stuck = 0
            print("inversé",self.instruction)
        else:
            self.counter = 0
        print("final",self.instruction)
        match self.instruction:
            case 'RIGHT':
                self.instruction = "RIGHT"
            case 'LEFT':
                self.instruction = "LEFT"
            case 'DOWN':
                self.instruction = "DOWN"
            case 'UP':
                self.instruction = "UP"
            case "BLOCKED":
                self.instruction = "BLOCKED"
        return self.instruction
    
