"""
This file contains the logic for the Second Local Search algorithm.
"""

import random
from typing import Tuple, List
from dataclasses import dataclass

from graph import Graph
from utils import Timer, Trace

POPULATION_SIZE = 100
CROSSOVER_RATE = 0.5
MUTATION_RATE = 0.5

# TODO: try to start from all nodes and then minimize them in the solution

class LS2:
    IS_DETERMINISTIC = False
    
    def __init__(self):
        """ Constructor for the LS2 class """
        if self.IS_DETERMINISTIC == None: raise ValueError("IS_DETERMINISTIC must be set to True or False")
        
    def get_vertex_cover(self, G: Graph, timer: Timer, trace: Trace) -> Tuple[int, List[int]]:
        """
        Second Local Search algorithm implementation.
        
        Args:
            G: graph to perform the search on
            timer: object to keep track of the time spent by the algorithm
            trace: object to keep track of the best solutions found by the algorithm at each iteration
            
        Returns:
            quality: quality of the best solution found
            solution: best solution found as list of nodes
        """
        
        self.G = G
        self.timer = timer
        self.trace = trace
        
        self.quality = None
        self.solution = None
        
        # Initiating recurring variables
        self.mutating_nodes = int(self.G.v * MUTATION_RATE)
        
        # Initiating population and evaluating its fitness
        population = self.init_population()
        population_fitness, total_fitness = self.get_population_fitness(population)
        
        # Generation loop
        geration = 0
        while not timer.cutoff():
            # Find mating probabilities
            mating_probabilities = self.get_mating_probability(population_fitness, total_fitness)
            
            # Create next generation
            population = self.make_next_generation(population, mating_probabilities)
            
            # Evaluate fitness of the new population
            population_fitness, total_fitness = self.get_population_fitness(population)
            
            # Find the best individual in the population
            self.update_best_solution(population, population_fitness)
            
            # Print progress
            average_size = int(sum([len(individual) for individual in population]) / len(population))
            print(f"\tGen: {geration} - Avg. Fit: {int(total_fitness/POPULATION_SIZE)} - Avg. Size: {average_size} - Best Sol Quality: {self.quality}")
            
            geration += 1
            
        # for i in range(len(population)):
        #     print(f"\t{i}: {population[i]} - {population_fitness[i]}")
            
        return self.quality, self.solution
    
    
    def init_population(self) -> List[List[int]]:
        """ Initiating population with of random vertex covers"""
        
        population = []
        all_nodes = self.G.all_nodes
        
        for i in range(POPULATION_SIZE):
            # Create a random vertex cover of size ranging from 1 to G.v
            individual = random.sample(all_nodes, random.randint(1, self.G.v))  
            population.append(individual)
            
        return population


    def get_fitness(self, individual: List[int]) -> List[int]:
        """ Evaluating fitness of the individual (this is the our scoring function) """
        if len(individual) == 0: 
            return 0
        
        return self.G.count_covered_edges(individual) * 100 - len(individual)
    
    
    def get_population_fitness(self, population: List[List[int]]) -> Tuple[List[int], float]:
        """ Evaluating fitness of the population """
        total_fitness = 0
        population_fitness = []
        for individual in population:
            fitness = self.get_fitness(individual)
            population_fitness.append(fitness)
            total_fitness += fitness
        return population_fitness, total_fitness
    
    
    def get_mating_probability(self, population_fitness: List[int], total_fitness: int) -> List[float]:
        """ Creates a list of weights corresponding to each individual's probability to mate based on its fitness """
        probabilities = []
        for fitness in population_fitness:
            probabilities.append(fitness/total_fitness)
            
        return probabilities
    
    
    def make_next_generation(self, current_population: List[List[int]], mating_probabilities: List[float]) -> List[List[int]]:
        """ Creates the next generation of individuals """
        next_gen = []
        
        while len(next_gen) < POPULATION_SIZE:
            # Selecting two parents
            parents = random.choices(current_population, weights=mating_probabilities, k=2)
            
            # Creating a child by crossing over the parents
            child = self.crossover(parents[0], parents[1])
            
            # Mutating the child
            child = self.mutate(child)
            
            next_gen.append(child)
            
        return next_gen
    
    
    def crossover(self, parent1: List[int], parent2: List[int]) -> List[int]:
        """ Crossover between two parents to create a next generation's individual """
        shared_nodes = set(parent1).intersection(set(parent2))
        not_shared_nodes = set(parent1).symmetric_difference(set(parent2))
        
        for node in list(not_shared_nodes):
            if random.random() < CROSSOVER_RATE:
                shared_nodes.add(node)
                
        return list(shared_nodes)
    
    
    def mutate(self, individual: List[int]) -> List[int]:
        """ Mutating the individual adding and/or removing nodes """  
        changing_nodes = random.sample(self.G.all_nodes, self.mutating_nodes)
        for node in changing_nodes:
            if node in individual:
                individual.remove(node)
            else:
                individual.append(node)
                
        return individual
    
    
    def update_best_solution(self, population: List[List[int]], population_fitness: List[int]) -> Tuple[int, List[int]]:
        """ Updates the best solution found so far """
        # Doing argmax on the population fitness
        best_individual = population[population_fitness.index(max(population_fitness))]
        
        # Continue only if best_individual is actually a vertex cover
        if not self.G.is_vertex_cover(best_individual):
            return
        
        current_quality = self.G.get_solution_quality(best_individual)

        # Updating the best solution found so far
        if self.quality == None or current_quality < self.quality:
            self.quality = current_quality
            self.solution = best_individual
            self.trace.add_record(self.quality)
        
    