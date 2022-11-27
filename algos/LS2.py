"""
This file contains the logic for the Second Local Search algorithm.
"""

import random
from typing import Tuple, List

from graph import Graph
from utils import Timer, Trace

POPULATION_SIZE = 100

class LS2:
    IS_DETERMINISTIC = False
    
    def __init__(self):
        """ Constructor for the LS2 class """
        raise ValueError("IS_DETERMINISTIC must be set to True or False") if self.IS_DETERMINISTIC == None else None
    
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
        
        quality = None
        solution = None
        
        population = init_population(G)
        for individual in population:
            print(individual, )
        
    
        quality = 0
        solution = 0
        return quality, solution
    
    
def init_population(G: Graph) -> List[List[int]]:
    """ Initiating population with a list of random vertex covers"""
    
    population = []
    all_nodes = G.get_all_nodes()
    
    for i in range(POPULATION_SIZE):
        # Create a random vertex cover of size ranging from 1 to G.v
        individual = random.sample(all_nodes, random.randint(1, G.v))            
        population.append(individual)
        
    return population


def get_fitness(G: Graph, population: List[List[int]]) -> List[int]:
    """ Evaluating fitness of each individual in the population """
    
    fitness = []
    
    for individual in population:
        fitness.append(G.check_vertex_cover(individual))
        
    return fitness
