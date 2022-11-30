"""
This file contains the logic for the First Local Search algorithm.
"""

import random
import numpy as np
from typing import Tuple, List

from graph import Graph
from utils import Timer, Trace
from algos.Approx import Approx

INITIALIZATION_MODE = "Approx"  # "Approx" | "full"
INITIAL_TEMPERATURE = 1
COOLING_RATE = 0.95
END_TEMPERATURE = 0.0001

DEBUG=True

class LS1:
    IS_DETERMINISTIC = False

    def __init__(self):
        """ Constructor for the LS1 class """
        if self.IS_DETERMINISTIC == None:
            raise ValueError("IS_DETERMINISTIC must be set to True or False")

    def get_vertex_cover(self, G: Graph, timer: Timer, trace: Trace) -> Tuple[int, List[int]]:
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

        self.quality = None
        self.solution = None  # solution to work on
        solution = None  # solution as a candidate

        # Initialize a vertex cover
        self.init_cover()
        self.temperature = INITIAL_TEMPERATURE
        self.edges_not_covered=set()

        # remove redundant nodes
        while True:
            for node in self.solution:
                if self.get_loss(node)==0:
                    self.solution.remove(node)
                    break
            break
                
        
        while not timer.cutoff():
            
            if self.temperature < END_TEMPERATURE:
                break

            # remove an vertex if the solution is already a vertex cover
            if len(self.edges_not_covered)==0:
                solution = self.solution
                self.quality = self.G.get_solution_quality(solution)
                self.trace.add_record(self.quality)
                print(f"Current temperature: {self.temperature} | Current quality:{self.quality}") if DEBUG else None
                # remove_num=int(np.ceil((self.temperature*self.quality*0.05)))
                choice=random.choices(self.solution,self.get_remove_probabilities(self.solution),k=1)[0]
                self.temperature = self.temperature * COOLING_RATE

                for neighbor in set(self.G.get_neighbours(choice)).difference(set(self.solution)):
                    self.edges_not_covered.add(frozenset([choice, neighbor]))

                self.solution.remove(choice)
                continue

            # add a vertex if the solution is not a vertex cover
            nodes_to_add=set()
            for node1, node2 in self.edges_not_covered:
                nodes_to_add.add(node1)
                nodes_to_add.add(node2)
            nodes_to_add=list(nodes_to_add)
            choice=random.choices(nodes_to_add,self.get_remove_probabilities(list(nodes_to_add)),k=1)[0]
            for neighbor in set(self.G.get_neighbours(choice)).difference(set(self.solution)):
                self.edges_not_covered.remove(frozenset([choice, neighbor]))
            self.solution.append(choice)    
            
        return self.quality, solution

    def init_cover(self) -> Tuple[int, List[int]]:
        """ Initiating a vertex cover"""

        if INITIALIZATION_MODE == "Approx":
            appr=Approx()
            self.quality, self.solution = appr.get_vertex_cover(
                self.G, self.timer, self.trace)

        elif INITIALIZATION_MODE == "full":
            self.quality = self.G.v
            self.solution = list(self.G.all_nodes)

        else:
            raise ValueError("Invalid initialization mode")

    def get_remove_probability(self) -> List[int]:
        """ Get the propability of removal from the vertex cover for every node """
        remove_probability=np.zeros(self.quality)
        for idx, node in enumerate(self.solution):
            remove_probability[idx]=2**(-self.get_loss(node)/self.temperature)

        return remove_probability

    def get_add_probability(self) -> List[int]:
        """ Get the propability of adding into the vertex cover for every node """
        add_probability=np.zeros(len(self.rem))
        for idx,node in enumerate(self.rem):
            gain=self.get_gain(node)
            if gain==0:
                add_probability[idx]=0
            else:
                add_probability[idx]=2**(-1/(self.temperature*gain))

        return add_probability

    def get_add_probability(self,node):
        gain=self.get_gain(node)
        return 0 if gain==0 else 2**(-1/(self.temperature*gain))

    def get_remove_probability(self,node):
        loss=self.get_loss(node)
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

    def get_loss(self,node):
        """ Get the loss of covered edges if a node is removed """
        return len(set(self.G.get_neighbours(node)).difference(set(self.solution)))


    def get_gain(self,node):
        """ Get the gain of covered edges if a node is added """
        return len(set(self.G.get_neighbours(node)).difference(set(self.solution)))

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
