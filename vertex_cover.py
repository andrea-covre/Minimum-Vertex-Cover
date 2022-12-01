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
        self.covered_edges=set()
        self.uncovered_edges=self.get_all_edges()

    def is_vertex_cover_new(self):
        """Use this only if you used add_vertex() and remove_vertex() to manipulate the solution, 
        or else you may want to call fix_uncovered_edges() first"""
        return len(self.uncovered_edges)==0

    def set_solution(self,solution: List[int]):
        """The solution is initially set to be empty. Please set the initial solution if you have one."""
        self.solution=set(solution)

    def get_solution(self):
        return list(self.solution)
    
    def get_solution_quality_new(self):
        return self.quality

    def get_covered_edges_new(self):
        """I'm keeping this at this time, but I think checking the uncovered edges makes more sense.
        Let Zhaonan know if you have any thoughts on this."""
        return self.covered_edges

    def get_uncovered_edges_new(self):
        """Use this only if you used add_vertex() and remove_vertex() to manipulate the solution, 
        or else you may want to call fix_uncovered_edges() first"""
        return self.uncovered_edges

    def update_solution(self):
        self.quality=len(self.solution)

    def add_vertex(self,node):
        """Just add the node. This function handles the rest."""
        changes=self.get_changes(node)
        self.covered_edges.update(changes)
        self.uncovered_edges.difference_update(changes)
        self.solution.add(node)
        self.update_solution()

    def add_vertices(self,nodes:List[int]):
        for node in nodes:
            self.add_vertex(node)
    
    def remove_vertex(self,node):
        """Just remove the node. This function handles the rest."""
        changes=self.get_changes(node)
        self.covered_edges.difference_update(changes)
        self.uncovered_edges.update(changes)
        self.solution.remove(node)
        self.update_solution()

    def get_add_candidates(self) -> List[int]:
        """Returns the (reasonable) candidates of vertices to be added into the solution."""
        add_candidates=set()
        for node1, node2 in iter(self.get_uncovered_edges_new()):
            add_candidates.add(node1)
            add_candidates.add(node2)
        return list(add_candidates)

    def get_changes(self,node):
        """Returns the changed edges (either from covered to uncovered, or the other way) if a node is added/removed."""
        changes=set()
        for neighbor in iter(set(self.get_neighbours(node)).difference(set(self.solution))):
            changes.add(frozenset([node,neighbor]))
        return changes

    def get_loss(self,node):
        """Returns the number of loss in covered edges if a node is removed."""
        return len(set(self.get_neighbours(node)).difference(set(self.solution)))

    def get_gain(self,node):
        """Returns the number of gain in covered edges if a node is added."""
        return len(set(self.get_neighbours(node)).difference(set(self.solution)))

    def remove_vertices(self,nodes:List[int]):
        for node in nodes:
            self.remove_vertex(node)
    
    def add_remove_vertices(self,nodes_add:List[int],nodes_remove:List[int]):
        self.add_vertices(nodes_add)
        self.remove_vertices(nodes_remove)

    def fix_covered_edges(self):
        self.covered_edges=self.get_covered_edges(self.solution)
        self.update_solution()

    def fix_uncovered_edges(self):
        self.uncovered_edges=self.get_uncovered_edges(self.solution)
        self.update_solution()

    def fix_all(self):
        self.fix_covered_edges()
        self.fix_uncovered_edges()