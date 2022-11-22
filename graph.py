"""
This file contains the logic needed to load a graph from a file.
"""

import os
from typing import List

class Graph:
    """
    The graph is represented through adjacency lists stored in dictionary where:
    - keys are the nodes
    - values are the lists of nodes that are adjacent to the key node
    
    Attributes:
        - v: int - number of nodes
        - e: int - number of edges
        - adj: dict - adjacency lists representation of thr graph as described above
        - _accesses_count: int - number of accesses to the graph
    """
    
    def __init__(self, path: str):
        """
        Constructor for the Graph class
        
        :param path: path to the graph dataset
        """
        
        self.adj = {}
        self.__accesses_count = 0
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"Graph file not found at {path}")
        
        # Loading graph from file
        with open(path, 'r') as f:
            lines = f.readlines()
            
            # Loading graph info (V, E)
            self.v, self.e, _ = [int(x) for x in lines[0].split()]
        
            # Loading edges
            current_node_idx = 1
            for line in lines[1:]:
                self.adj[current_node_idx] = [int(x) for x in line.split()]
                current_node_idx += 1
                
    def get_neighbours(self, node: int) -> List[int]:
        """
        Returns the list of neighbours of the given node
        
        :param node: node to get the neighbours of
        :return: list of neighbours
        """
        if node not in self.adj:
            raise ValueError(f"Node {node} not in graph")
        
        self._accesses_count += 1
        
        return self.adj[node]
    
    def get_all_nodes(self) -> List[int]:
        """ Returns the list of all nodes in the graph """
        return list(self.adj.keys())
