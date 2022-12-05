"""
This file contains the logic for the Second Local Search algorithm.
"""

import random
import numpy as np
from typing import Tuple, List

from graph import Graph
from utils import Timer, Trace
from algos.Approx import Approx


# Parameters
INITIALIZATION_MODE = "approx" #"near_trivial" # "lognorm" | "uniform" | "normal" | "near_trivial" | "approx"
POPULATION_SIZE = 500
FITNESS_MODE = "minimizing_size_sub" # "size_penalty" | "covered_edges_focused" | "minimizing_size_sub" | "minimizing_size_inverse"
SIZE_PENALTY_MULTIPLIER = 1.1
CROSSOVER_MODE = "remove_not_shared" # "add_not_shared" | "remove_not_shared"
CROSSOVER_RATE = 0.5
MUTATION_RATE = 0.8
MUTATION_MODE = "switch" # "batch" | "switch" | "decrease_size"

class LOGNORMAL_PARAM:
    MU = 1
    SIGMA = 0.9
    DISTRIBUTION_RANGE = [0, 50]
    
class NEAR_TRIVIAL_PARAM:
    LOWER_BOUNDARY = 0.95

DEBUG = False

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
        print("\tInitiating population\n")
        population = self.init_population()
        population_fitness, total_fitness = self.get_population_fitness(population)
        
        average_size = sum([len(individual) for individual in population]) / len(population)
        print("init average size:", average_size) if DEBUG else None
        
        # Generation loop
        generation = 0
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
            sizes = [len(individual) for individual in population]
            average_size = sum(sizes) / len(population)
            variance = sum([((x - average_size) ** 2) for x in sizes]) / len(sizes)
            std = round(variance ** 0.5, 3)
            print(f"\tGen: {generation:<4}  | Avg. Fit: {round(total_fitness/POPULATION_SIZE, 3):7.3f}\t | Avg. Size: {average_size:7.3f}\t | Std. Size: {std:5.3f}\t | Best Sol Quality: {self.quality}")
            
            generation += 1
            
        return self.quality, self.solution
    
    
    def init_population(self) -> List[List[int]]:
        """ Initiating population with of random vertex covers"""
        
        population = []
        all_nodes = self.G.all_nodes
        
        if INITIALIZATION_MODE == "uniform":
            get_number_of_nodes = lambda: random.randint(1, self.G.v)
            
        elif INITIALIZATION_MODE == "normal":
            get_number_of_nodes = lambda: int(np.random.normal(self.G.v/2, self.G.v/4))
            
        elif INITIALIZATION_MODE == "lognorm":
            get_number_of_nodes = self.get_lognormal_vertexes_count
            
        elif INITIALIZATION_MODE == "near_trivial":
            get_number_of_nodes = lambda: random.randint(int(self.G.v-self.G.v*(1-NEAR_TRIVIAL_PARAM.LOWER_BOUNDARY)), self.G.v)
            
        elif INITIALIZATION_MODE == "approx":
            
            appr = Approx()
            t_timer = Timer(self.timer.time_limit)
            t_trace = Trace(t_timer, self.G)
            t_timer.start()
            
            vertex_cover = appr.get_vertex_cover(self.G, t_timer, t_trace)[1]
            
            return [vertex_cover for i in range(POPULATION_SIZE)]
            
        else:
            raise ValueError("Invalid initialization mode")
            
        for i in range(POPULATION_SIZE):
            # Create a random vertex cover of size ranging from 1 to G.v, with the given distribution mode
            number_of_vertexes = get_number_of_nodes()

            individual = random.sample(all_nodes, number_of_vertexes)  
            print(number_of_vertexes, len(individual)) if DEBUG else None
            population.append(individual)
            
        return population
    
    
    def get_lognormal_vertexes_count(self):
        """ Returns a random number from an inversed lognormal distribution mapped to the vertexes range """
        sample = np.random.lognormal(LOGNORMAL_PARAM.MU, LOGNORMAL_PARAM.SIGMA)
        
        src_lower_bound = LOGNORMAL_PARAM.DISTRIBUTION_RANGE[0]
        src_upper_bound = LOGNORMAL_PARAM.DISTRIBUTION_RANGE[1]
        
        dst_lower_bound = 0
        dst_upper_bound = self.G.v
        
        dst_span = dst_upper_bound - dst_lower_bound
        src_span = src_upper_bound - src_lower_bound
        
        valueScaled = float(sample - src_lower_bound) / float(src_span)
        mapped_sample = dst_lower_bound + (valueScaled * dst_span)
        
        random_vertex_count = int(self.G.v - mapped_sample)
        
        if random_vertex_count < 0: random_vertex_count = 0
        
        return random_vertex_count


    def get_fitness(self, individual: List[int]) -> List[int]:
        """ Evaluating fitness of the individual (this is the our scoring function) """
        if len(individual) == 0: 
            return 0
        
        if FITNESS_MODE == "size_penalty":
            covered_edges = self.G.count_covered_edges(individual) 
            
            denominator = self.G.e - covered_edges + len(individual) * SIZE_PENALTY_MULTIPLIER
            if denominator == 0:
                denominator = 0.001
            
            return (self.G.e / denominator) #/ len(individual)
        
        elif FITNESS_MODE == "covered_edges_focused":
            return (covered_edges * 10 - len(individual))
        
        elif FITNESS_MODE == "minimizing_size_inverse":
            """ Minimizing size with fitness ratio and weeding out not complete solutions """
            covered_edges = self.G.count_covered_edges(individual) 
            if not self.G.is_vertex_cover(individual):
                return 0.001
            return self.G.v/len(individual)
        
        elif FITNESS_MODE == "minimizing_size_sub":
            """ Minimizing size with size difference and weeding out not complete solutions """
            covered_edges = self.G.count_covered_edges(individual) 
            if not self.G.is_vertex_cover(individual):
                return 0.001
            return self.G.v - len(individual)
        
        else:
            raise ValueError("Invalid fitness mode")

    
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
            
            print("parent 1 size:", len(parents[0]), "parent 2 size:", len(parents[1])) if DEBUG else None
            
            # Creating a child by crossing over the parents
            child = self.crossover(parents[0], parents[1])
            
            print("cross child size:", len(child)) if DEBUG else None
            
            # Mutating the child
            child = self.mutate(child)
            
            print("mut child size:", len(child), "\n") if DEBUG else None
            
            next_gen.append(child)
            
            
        return next_gen
    
    
    def crossover(self, parent1: List[int], parent2: List[int]) -> List[int]:
        """ Crossover between two parents to create a next generation's individual """
        
        shared_nodes = set(parent1).intersection(set(parent2))
        not_shared_nodes = set(parent1).symmetric_difference(set(parent2))
        
        if CROSSOVER_MODE == "add_not_shared":
            
            for node in list(not_shared_nodes):
                if random.random() < CROSSOVER_RATE:
                    shared_nodes.add(node)
                    
            return list(shared_nodes)
        
        elif CROSSOVER_MODE == "remove_not_shared":
            return list(shared_nodes)
        
        else:
            raise ValueError("Invalid crossover mode")
    
    
    def mutate(self, individual: List[int]) -> List[int]:
        """ Mutating the individual adding and/or removing nodes """  
        
        if MUTATION_MODE == "batch":
            changing_nodes = random.sample(self.G.all_nodes, self.mutating_nodes)
            for node in changing_nodes:
                if node in individual:
                    individual.remove(node)
                else:
                    individual.append(node)
                    
        elif MUTATION_MODE == "switch":                
            while random.random() < MUTATION_RATE:
                if len(individual) == 0: break
                active_node = random.choice(individual)
                individual.remove(active_node)
                
            while random.random() < MUTATION_RATE:
                inactive_nodes = list( set(self.G.all_nodes).difference(set(individual)) )
                if len(inactive_nodes) == 0: break
                inactive_node = random.choice(inactive_nodes)
                individual.append(inactive_node)
                
        elif MUTATION_MODE == "decrease_size":
            while random.random() < MUTATION_RATE:
                if len(individual) <= 1: break
                active_node = random.choice(individual)
                individual.remove(active_node)
                    
        else:
            raise ValueError("Invalid mutation mode")
                
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
        
    