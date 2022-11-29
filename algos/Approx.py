"""
This file contains the logic for Heuristic with Approximation algorithm.
"""

from copy import deepcopy
from typing import Tuple, List

from graph import Graph
from utils import Timer, Trace


class Approx:
    IS_DETERMINISTIC = True

    def __init__(self):
        """ Constructor for the Approx class """
        if self.IS_DETERMINISTIC == None:
            raise ValueError(
                "IS_DETERMINISTIC must be set to True or False")

    def get_vertex_cover(self, G: Graph, timer: Timer, trace: Trace) -> Tuple[int, List[int]]:
        """
        Heuristic with Approximation algorithm implementation.

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
        solution = []

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

        #G_remaining = deepcopy(G)
        G_rem=G.adj.copy()
        G_nodes=G_rem.keys()
        G_e=G.e
        G_v=G.v

        while G_e != 0:

            # find the vertex with maximum degree in G_remaining and save its index and adj_num

            # set initial value of node_max[node_index, num_of_adj_nodes]
            node_max = [-1, -1]

            for node in G_nodes:
                if len(G_rem[node]) > node_max[1]:
                    node_max[0] = node
                    node_max[1] = len(G_rem[node])

            # add the vertex with max degree to solution set
            solution.append(node_max[0])

            # delete the vertex with max degree and its edges in G_remaining

            G_v -= 1
            G_e -= len(G_rem[node_max[0]])
            for node in G_rem[node_max[0]]:
                G_rem[node].remove(node_max[0])
                if len(G_rem[node]) == 0:
                    del G_rem[node]
                    G_v = G_v-1

            del G_rem[node_max[0]]

            G_nodes = G_rem.keys()

            # check run time
            if timer.cutoff():
                break

        # check solution quality
        if G.is_vertex_cover(solution):

            quality=G.get_solution_quality(solution)
            print(f"Solution is found with quality of {quality}.")

        else:

            edges_covered=G.count_covered_edges(solution)
            total_edges=G.e
            print(f"Solution is not found in time with {edges_covered} edges covered in total {total_edges} edges.")


        return quality, solution


if __name__ == "__main__":
    print("hello")
