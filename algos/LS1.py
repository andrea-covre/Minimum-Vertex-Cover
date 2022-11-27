"""
This file contains the logic for the First Local Search algorithm.
"""

from typing import Tuple, List

from graph import Graph
from utils import Timer, Trace


def first_local_search(G: Graph, timer: Timer, trace: Trace) -> Tuple[int, List[int]]:
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
    
    quality = None
    solution = None
    
    ######################
    ### YOUR CODE HERE ###
    ######################
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
    
    raise NotImplementedError("first_local_search in algos/LS1.py not implemented yet")
    
    return quality, solution
