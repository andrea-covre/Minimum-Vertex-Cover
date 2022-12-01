"""
This file contains the logic needed to load a graph from a file.
"""

import os
from typing import List, Set

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
        self._accesses_count = 0
        self._vertex_cover_check_count = 0
        
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
        
        self.all_nodes = self.adj.keys()

        self.all_edges = set()
        for node in self.all_nodes:
            for neighbour in self.get_neighbours(node):
                self.all_edges.add(frozenset([node, neighbour]))
                
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
    
    def get_covered_edges(self, vertex_cover: List[int]) -> Set[frozenset]:
        """
        Returns the edges covered by the given vertex cover
        
        :param vertex_cover: list of nodes that compose the vertex cover
        :return: a set of frozensets, each frozenset represents an edge
        """
        self._vertex_cover_check_count += 1
        
        covered_edges = set()
        for node in vertex_cover:
            for neighbour in self.get_neighbours(node):
                covered_edges.add(frozenset([node, neighbour]))

        return covered_edges

    def get_all_edges(self) -> Set[frozenset]:
        """
        Returns all edges in G
        
        :return: a set of frozensets, each frozenset represents an edge
        """
        
        return self.all_edges

    def get_uncovered_edges(self, vertex_cover: List[int]) -> Set[frozenset]:
        """ Returns the edges not covered by the given vertex cover """
        return self.get_all_edges().difference(self.get_covered_edges(vertex_cover))

    def get_nodes_to_add(self, vertex_cover: List[int]) -> List[int]:
        """ Returns possible nodes to add into the cover """
        nodes_to_add=set()
        for node1, node2 in self.get_uncovered_edges(vertex_cover):
            nodes_to_add.add(node1)
            nodes_to_add.add(node2)
        return list(nodes_to_add)

    def count_covered_edges(self, vertex_cover: List[int]) -> int:
        """ Returns the number of edges covered by the given vertex cover """
        return len(self.get_covered_edges(vertex_cover))
    
    def is_vertex_cover(self, vertex_cover: List[int]) -> bool:
        """
        Returns True if the given vertex cover is a vertex cover of the graph
        
        :param vertex_cover: list of nodes that compose the vertex cover
        :return: True if the given vertex cover is a vertex cover of the graph, False otherwise
        """
        return self.count_covered_edges(vertex_cover) == self.e
    
    def get_solution_quality(self, solution: List[int]) -> int:
        """ Returns the quality of the given solution """
        return len(solution)
