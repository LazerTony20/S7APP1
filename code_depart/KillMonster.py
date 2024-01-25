import pygame
import random
from Constants import *
from Monster import *
from Maze import *
from Player import Player
class KillMonster:
    def __init__(self, pop_size=2, mutation_rate=0.01, generations=10,crossover_rate=0.8, elite_ratio=0.1):
        self.population_size = pop_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.generations = generations
        self.maxKill = 4
        self.bestKill = 0
        self.bestFitness = 0
        self.current_gen = 0
        self.elite_ratio = elite_ratio
        self.bestIndividual = []
        self.population = []
        self.monster = None
        self.scores = []
        self.kill = []
        self.Player = Player()
    def __init__(self, pop_size=2, mutation_rate=0.01, generations=10,crossover_rate=0.8, elite_ratio=0.1, maze=None):
        self.population_size = pop_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.generations = generations
        self.maxKill = 4
        self.bestKill = 0
        self.bestFitness = 0
        self.current_gen = 0
        self.elite_ratio = elite_ratio
        self.bestIndividual = []
        self.population = []
        self.monster = None
        self.maze = maze
        self.kill = []
        self.scores = []
        self.Player = Player()
    # Générer une population initiale
    def generate_population(self,size):
        self.population = [[random.randrange(-MAX_ATTRIBUTE, MAX_ATTRIBUTE) for _ in range(NUM_ATTRIBUTES)] for _ in range(size)]    
        self.population = [[encode_population(gene) for gene in individual] for individual in self.population]
    # Encoder la population
    def evaluate_population(self, population):
        decode = [[decode_population(gene) for gene in individual] for individual in population]
        self.scores = []
        self.kill = []
        for individual in decode:
            self.Player.set_attributes(individual)
            self.kill.append(self.fitness_function()[0])
            self.scores.append(self.fitness_function()[1])
        
    # Calculer le score d'un individu
    def fitness_function(self):
        if self.maze != None:
            for monster in self.maze.monsterList:
                return monster.mock_fight(self.Player)
        else:
            if self.monster == None:
                return  [0,0]
            return self.monster.mock_fight(self.Player)
    
    # Sélectionner un monstre
    def setMonster(self,monster):
        self.monster = monster
    
    # Sélectionner des individus pour la reproduction
    def selection(self):
        
        selected_indices = random.sample(range(len(self.population)), 1)
        selected_individuals = [self.population[i] for i in selected_indices]
        selected_scores = [self.scores[i] for i in selected_indices]
        return selected_individuals[selected_scores.index(max(selected_scores))]
    
    # Sélectionner un individu par roulette
    # def roulette_wheel_selection(self):
    #     if len(self.population) != len(self.scores):
    #         raise ValueError("La taille de la population et celle des valeurs de fitness doivent être égales.")

    #     total_fitness = sum(self.scores)
    #     if total_fitness == 0:
    #         raise ValueError("La somme des valeurs de fitness ne doit pas être nulle.")

    #     roulette_spin = random.uniform(0, total_fitness)
    #     cumulative_fitness = 0

    #     for i, fitness in enumerate(self.scores):
    #         cumulative_fitness += fitness
    #         if cumulative_fitness >= roulette_spin:
    #             return self.population[i]
        
    # Effectuer la reproduction
    def crossover(self, parent1, parent2):
        if(self.crossover_rate < random.uniform(0, 1)):
            return random.choice([parent1, parent2])
        else:
            crossover_point = random.randint(1, len(parent1) - 2)
            child = parent1[:crossover_point] + parent2[crossover_point:]
            return child

    # Appliquer une mutation à un individu
    def mutate(self, individual):
        for gene in individual:
            if random.uniform(0, 1) < self.mutation_rate:
                i = random.randint(0, len(gene) - 1)
                gene = gene[:i] + ('1' if gene[i] == '0' else '0') + gene[i + 1:]
        return individual
    
    def elitism(self):
        elites_indices = sorted(range(len(self.scores)), key=lambda i: self.scores[i], reverse=True)[:int(self.elite_ratio * self.population_size)]
        elites = [self.population[i] for i in elites_indices]
        return elites
    
    # Générer une nouvelle population
    def genetic_algorithm(self):
        self.current_gen = 0
        self.generate_population(self.population_size)
        while(True):
            self.evaluate_population(self.population)
            new_population = self.elitism()
            remaining_size = int(self.population_size * (1 - self.elite_ratio))
            if self.current_gen % self.generations == 0:
                self.generate_population(remaining_size)
                new_population.extend(self.population)
            else:
                for _ in range(self.population_size // 2):
                    parent1 = self.selection()
                    parent2 = self.selection()
                    child1 = self.crossover(parent1, parent2)
                    child2 = self.crossover(parent2, parent1)
                    child1 = self.mutate(child1)
                    child2 = self.mutate(child2)
                    new_population.extend([child1, child2])
            self.evaluate_population(new_population)
            self.population = new_population
            self.current_gen += 1
            self.bestKill = max(self.kill, key=int)
            self.bestFitness = max(self.scores, key=float)
            self.bestIndividual = self.population[self.scores.index(self.bestFitness)]
            if(self.current_gen % 10 == 0):
                # self.mutation_rate += 0.01
                print("Generation: ", self.current_gen)
                print("Best fitness: ", self.bestFitness)
                print("Best Individual: ", [decode_population(gene) for gene in self.bestIndividual])
                print("Best kill: ", self.bestKill)
                print("Max kill: ", self.maxKill)
                print("======================================================")
            if self.bestKill == self.maxKill:
                self.bestIndividual = self.population[self.kill.index(self.bestKill)]
                self.bestFitness = self.scores[self.kill.index(self.bestKill)]
                print("======================================================")
                print("Solution trouvée: ")
                print("Generation: ", self.current_gen)
                print("Best fitness: ", self.bestFitness)
                print("Best Individual: ", [decode_population(gene) for gene in self.bestIndividual])
                print("======================================================")
                return [decode_population(gene) for gene in self.bestIndividual]
        return [decode_population(gene) for gene in self.bestIndividual]
    
def encode_population(value, bits=11):
        if not isinstance(value, int) or not isinstance(bits, int) or bits <= 0:
            raise ValueError("La valeur doit être un entier positif et le nombre de bits doit être un entier positif.")
        value = max(-1000, min(1000, value))
        if value < 0:
            signe = '1'
            value = abs(value)
        else:
            signe = '0'
        bin_value = bin(value)[2:]
        bin_value = bin_value.zfill(bits-1)
        bin_value = signe + bin_value
        return bin_value
    # Decoder Population
def decode_population(bin):
    if not isinstance(bin, str) or len(bin) == 0:
        raise ValueError("La représentation binaire doit être une chaîne de caractères non vide.")
    signe = bin[0]
    value = bin[1:]
    value = int(value, base=2)
    if signe == '1':
        value = -value
    return value        