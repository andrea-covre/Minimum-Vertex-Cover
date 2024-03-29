"""
This file contains the logic for the First Local Search algorithm.
"""

import random
import numpy as np
from typing import Tuple, List

from graph import Graph
from vertex_cover import Vertex_Cover
from utils import Timer, Trace
from algos.Approx import Approx

INITIALIZATION_MODE = "Approx"  # "Approx" | "full"
ANNEALING_MODE = "profile" # "profile" | "exponential"

# exponential cooling setting
INITIAL_TEMPERATURE = 0.1
COOLING_RATE = 0.9995
END_TEMPERATURE = 0.001

# annealing profile
HEATING_TEMP=0.1
ANNEALING_1_TEMP=0.05
ANNEALING_2_TEMP=0.01
COOLING_TEMP=0.001
# end time (percentage of the time limit)
HEATING_TIME=0.1
ANNEALING_1_TIME=0.4
ANNEALING_2_TIME=0.7
COOLING_TIME=1

ANNEALING_PROFILE={HEATING_TIME:HEATING_TEMP, ANNEALING_1_TIME:ANNEALING_1_TEMP, ANNEALING_2_TIME:ANNEALING_2_TEMP, COOLING_TIME:COOLING_TEMP }

DEBUG=True

class LS1:
    IS_DETERMINISTIC = False

    def __init__(self):
        """ Constructor for the LS1 class """
        if self.IS_DETERMINISTIC == None:
            raise ValueError("IS_DETERMINISTIC must be set to True or False")

    def get_vertex_cover(self, G: Vertex_Cover, timer: Timer, trace: Trace) -> Tuple[int, List[int]]:
        """
        First Local Search algorithm implementation.

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

        solution = None  # all-time best solution
        solution_temp = None # solution as a candidate
        quality = None
        quality_temp = None
        # print(f"ub:{self.G.get_upper_bound()}|lb:{self.G.get_lower_bound()}")

        # Initialize a vertex cover
        self.init_cover()
        self.temperature = INITIAL_TEMPERATURE
                
        solution = self.G.get_solution()
        quality_temp = self.G.get_solution_quality_new()
        quality = quality_temp

        while not timer.cutoff():
            
            if ANNEALING_MODE == "exponential":
                if self.temperature < END_TEMPERATURE:
                    break
            elif ANNEALING_MODE == "profile":
                self.temperature=self.get_temperature(ANNEALING_PROFILE, timer.elapsed()/timer.time_limit)

            # remove an vertex if the solution is already a vertex cover
            if len(self.G.get_uncovered_edges_new())==0:
                solution_temp = self.G.get_solution()
                quality_temp = self.G.get_solution_quality_new()
                if quality_temp < quality:
                    quality = quality_temp
                    solution = solution_temp
                    self.trace.add_record(quality)
                    print(f"Current temperature: {self.temperature:.3f} | Current quality:{quality_temp}", end="\r") 
                print(f"Current temperature: {self.temperature:.3f} | Current quality:{quality_temp}", end="\r") if DEBUG else None
                # remove_num=int(np.ceil((self.temperature*self.quality*0.05)))
                choice=random.choices(solution_temp,self.get_remove_probabilities(solution_temp),k=1)[0]
                if ANNEALING_MODE == "exponential":
                    self.temperature = self.temperature * COOLING_RATE
                self.G.remove_vertex(choice)
                # print(f"ub:{self.G.get_upper_bound()}|lb:{self.G.get_lower_bound()}")
                continue

            # add a vertex if the solution is not a vertex cover
            add_candidates=self.G.get_add_candidates()
            choice=random.choices(add_candidates,self.get_add_probabilities(list(add_candidates)),k=1)[0]
            self.G.add_vertex(choice)  
            # print(f"Current temperature: {self.temperature:.3f} | Current quality:{self.G.get_solution_quality_new()}", end="\r") if DEBUG else None
        
        # check solution
        if G.is_vertex_cover(solution):

            quality=G.get_solution_quality(solution)
            print(f"Solution is found with quality of {quality}.")

        else:

            edges_covered=G.count_covered_edges(solution)
            total_edges=G.e
            print(f"Solution is not found in time with {edges_covered} edges covered in total {total_edges} edges.")

        return quality, solution

    def init_cover(self) -> Tuple[int, List[int]]:
        """ Initiating a vertex cover"""

        if INITIALIZATION_MODE == "Approx":
            appr=Approx()
            self.quality, solution = appr.get_vertex_cover(self.G, self.timer, self.trace)
            self.G.set_solution(solution)
            self.G.fix_covered_edges()
            self.G.fix_uncovered_edges()

        elif INITIALIZATION_MODE == "full":
            self.G.set_solution(list(self.G.all_nodes))
            self.G.fix_covered_edges()
            self.G.fix_uncovered_edges()

        else:
            raise ValueError("Invalid initialization mode")

        # remove redundant nodes
        while True:
            for node in self.G.get_solution():
                if len(self.G.get_changes(node))==0:
                    self.G.remove_vertex(node)
                    continue
            break

    def get_add_probability(self,node):
        gain=self.G.get_gain(node)
        return 0 if gain==0 else 2**(gain/(self.temperature))

    def get_remove_probability(self,node):
        loss=self.G.get_loss(node)
        return 1 if loss==0 else 2**(-loss/self.temperature)

    def get_add_probabilities(self,nodes:List[int])->List[float]:
        probability=[]
        for node in nodes:
            probability.append(self.get_add_probability(node))
        return probability

    def get_remove_probabilities(self,nodes:List[int])->List[float]:
        probability=[]
        for node in nodes:
            probability.append(self.get_remove_probability(node))
        return probability

    def get_temperature(self, profile, time):
        for phase in profile.keys():
            if time<phase:
                return profile[phase]
            else: 
                continue


        # ===== Useful info: =====
        # > feel free to import the random module if needed, but do not worry about setting the seed as it is already set globally in exec.py
        # > G.v is the number of nodes in the graph
        # > G.e is the number of edges in the graph
        # > G.get_neighbours(node) returns the list of neighbours of the given node (use this API to access the graph, so that the accesses count is updated)
        # > G.get_all_nodes() returns the list of all nodes in the graph
        # > G.check_vertex_cover(vertex_cover) returns the number of vertexes covered by the vertex cover (use this API, so that the vertex cover checks count is updated)
        # > the nodes in the graph are numbered from 1 to G.v
        # > use timer.cutoff() to check if the time limit has been exceeded and you need to stop the algorithm
        # > use trace.add_record(quality) to add a new record to the trace, do not worry about the timestamp (as it is added automatically) or about saving the file
        # > return the best solution found (as a list of nodes) and its quality (number of edges covered)
        #
        # >>> if you need anything feel free to let Andrea know! <<<
        #
        ######################
