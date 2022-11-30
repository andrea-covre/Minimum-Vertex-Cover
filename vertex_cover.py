"""
This file contains the common functions used in vertex cover algorithms.
"""

from typing import List, Set
from graph import Graph

class Vertex_Cover(Graph):
    """
    This class is inherited from the Graph class:
    - keys are the nodes
    - values are the lists of nodes that are adjacent to the key node
    
    Graph class Attributes:
        - v: int - number of nodes
        - e: int - number of edges
        - adj: dict - adjacency lists representation of thr graph as described above
        - _accesses_count: int - number of accesses to the graph

    Vertex_Cover class Attributes:
        - solution: set of chosen vertices
        - quality: number of chosen vertices
        - is_vertex_cover: True if the solution is a vertex cover
    """
    
    def __init__(self, path: str):
        """
        Constructor for the Vertex_Cover class
        
        :param path: path to the graph dataset
        """
        Graph.__init__(self, path)
        self.solution=set()
        self.quality=0
        self.is_vertex_cover=False
        self.covered_edges=set()
        self.uncovered_edges=self.get_all_edges()

    def is_vertex_cover(self):
        return self.is_vertex_cover
    
    def get_solution_quality(self):
        return self.quality

    def get_covered_edges(self):
        return self.covered_edges

    def get_uncovered_edges(self):
        return self.uncovered_edges

    def update_solution(self):
        self.quality=len(self.solution)
        self.is_vertex_cover=(len(self.uncovered_edges)==0)

    def add_vertex(self,node):
        changes=set(self.get_neighbours(node)).difference(set(self.solution))
        self.covered_edges.update(changes)
        self.uncovered_edges.difference_update(changes)
        self.solution.add(node)
        self.update_solution()

    def add_vertices(self,nodes:List[int]):
        for node in nodes:
            self.add_vertex(node)
    
    def remove_vertex(self,node):
        changes=set(self.get_neighbours(node)).difference(set(self.solution))
        self.covered_edges.difference_update(changes)
        self.uncovered_edges.update(changes)
        self.solution.remove(node)
        self.update_solution()

    def remove_vertices(self,nodes:List[int]):
        for node in nodes:
            self.remove_vertex(node)
    
    def add_remove_vertices(self,nodes_add:List[int],nodes_remove:List[int]):
        self.add_vertices(nodes_add)
        self.remove_vertices(nodes_remove)

    def fix_covered_edges(self):
        self.covered_edges=self.get_covered_edges()
        self.update_solution()

    def fix_uncovered_edges(self):
        self.uncovered_edges=self.get_uncovered_edges()
        self.update_solution()