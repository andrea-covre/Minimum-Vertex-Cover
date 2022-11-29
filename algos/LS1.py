"""
This file contains the logic for the First Local Search algorithm.
"""

import random
import numpy as np
from typing import Tuple, List

from graph import Graph
from utils import Timer, Trace
from Approx import Approx

INITIALIZATION_MODE = "Approx"  # "Approx" | "full"
INITIAL_TEMPERATURE = 10
COOLING_RATE = 0.95


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
        while not timer.cutoff():
            # remove an vertex if the solution is already a vertex cover
            if self.G.is_vertex_cover(self.solution):
                solution = self.solution
                self.quality = self.G.get_solution_quality(solution)
                self.trace.add_record(self.quality)
                self.solution.remove(random.choices(
                    self.G.all_nodes, self.get_remove_probability(), k=1))
                continue

            # add a vertex if the solution is not a vertex cover
            self.solution.add(random.choices(
                self.G.all_nodes, self.get_add_probability(), k=1))

            self.temperature = self.temperature * COOLING_RATE

        return self.quality, solution

    def init_cover(self) -> Tuple[int, List[int]]:
        """ Initiating a vertex cover"""

        if INITIALIZATION_MODE == "Approx":
            self.quality, self.solution = Approx.get_vertex_cover(
                self.G, self.timer, self.trace)

        if INITIALIZATION_MODE == "full":
            self.quality = self.G.v
            self.solution = self.G.all_nodes

        else:
            raise ValueError("Invalid initialization mode")

    def get_remove_probability(self) -> List[int]:
        """ Get the propability of removal from the vertex cover for every node """
        remove_probability=np.zeros(self.G.v)
        for node in self.solution:
            remove_probability[node-1]=2**(self.get_loss(node)/self.temperature)

        return remove_probability

    def get_add_probability(self) -> List[int]:
        """ Get the propability of adding into the vertex cover for every node """
        add_probability=np.zeros(self.G.v)
        for node in self.G.all_nodes:
            if node in self.solution:
                continue
            add_probability[node-1]=2**(self.get_gain(node)/self.temperature)

        return add_probability

    def get_loss(self,node):
        """ Get the loss of covered edges if a node is removed """
        return set(self.G.get_neighbours(node)).difference(set(self.solution))


    def get_gain(self,node):
        """ Get the gain of covered edges if a node is added """
        return set(self.G.get_neighbours(node)).difference(set(self.solution))

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
