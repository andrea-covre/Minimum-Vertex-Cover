"""
This file contains the logic for the Branch and Bound algorithm.
"""
from algos.Approx import Approx
from copy import deepcopy
import networkx as nx
from typing import Tuple, List

from graph import Graph
from utils import Timer, Trace


class BnB:
    IS_DETERMINISTIC = True
    
    def __init__(self):
        """ Constructor for the BnB class """
        if self.IS_DETERMINISTIC == None: raise ValueError("IS_DETERMINISTIC must be set to True or False")
    
    def get_vertex_cover(self, G: Graph, timer: Timer, trace: Trace) -> Tuple[int, List[int]]:
        """
        Branch and Bound algorithm implementation.
        
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
        
        #initialize final output and trace intermediates
        quality = None
        quality1 = None
        solution = []
        solution1 = []
        
        
        #initializing parameters
        OptVC = []
        CurVC = []
        Frontier = []
        neighbor = []
        
        #initialize UB with Approx algo(max degree)
        appr=Approx()
        UpperBound, solution_appr = appr.get_vertex_cover(self.G, self.timer, self.trace)
        UpperBound += 1
        #initialize new graph to be divided in subproblems
        CurG = deepcopy(G)
        v = find_maxdeg(CurG)
        
        #The frontier set begins with the vertex with the highest degree
        #0 and 1 indicates whether the node is in the vertex cover
        Frontier.append((v[0], 0, (-1, -1)))
        Frontier.append((v[0], 1, (-1, -1)))
        
        while timer.cutoff() == False and Frontier != []:
            #Produce node for exploration
            (vi,state,parent)=Frontier.pop()
            backtrack = False
            if state == 0: #not included in VC
                neighbor = CurG.get_neighbours(vi)
                for node in list(neighbor):
                    CurVC.append((node, 1))
                    print(chr(33+(node%93)),end="") 
                    #all neighboring nodes must be included in VC
                    #Nodes included in VC are removed from the current graph
                    CurG.v -= 1
                    CurG.e -= len(CurG.adj[node])
                    for Neigh in CurG.adj[node]:
                        CurG.adj[Neigh].remove(node)
                        if len(CurG.adj[Neigh]) == 0:
                            del CurG.adj[Neigh]
                            CurG.v -= 1
                    del CurG.adj[node]
                    
            elif state == 1:
                #CurG.remove_node(vi)
                CurG.v -= 1
                CurG.e -= len(CurG.adj[vi])
                for node1 in CurG.adj[vi]:
                    CurG.adj[node1].remove(vi)
                    if len(CurG.adj[node1]) == 0:
                        del CurG.adj[node1]
                        CurG.v -= 1
                del CurG.adj[vi]
            
            CurVC.append((vi,state))
            print(chr(33+(vi%93)),end="") 
            CurVC_size = VC_Size(CurVC)
            
            if CurG.e == 0: #vertex cover complete
                if CurVC_size < UpperBound:#accepts result
                    OptVC = CurVC.copy()
                    UpperBound = CurVC_size  #update UB
                    solution1 = []
                    #trace record
                    for i in range(len(OptVC))            :
                        if OptVC[i][1] == 1:
                            solution1.append(OptVC[i][0])
                    # check solution quality and record trace
                    if G.is_vertex_cover(solution1):
                        quality1=G.get_solution_quality(solution1)
                        self.trace.add_record(quality1)
                backtrack = True
            else:
                # set lower bound by dividing number of edges with max degree node in the partial graph
                CurLB = Lowerbound(CurG) + CurVC_size
                
                # UBq,UBsol=appr.get_vertex_cover(CurG,self.timer,self.trace)
                # if UBq<UpperBound:
                    # UpperBound=UBq
                # self.CurG = CurG
                
                #print(f"LB:{CurLB}|UB:{UpperBound}")
                
                if CurLB<UpperBound: #continue explore
                    vj = find_maxdeg(CurG)
                    Frontier.append((vj[0],0,(vi,state)))
                    Frontier.append((vj[0],1,(vi,state)))
                else: #end this path and backtrack
                    backtrack = True
            
            if backtrack == True:
                if Frontier != []: #revert to parent node
                    nextnode_parent = Frontier[-1][2]
                    
                    if nextnode_parent in CurVC:
                        id = CurVC.index(nextnode_parent) +1
                        while id < len(CurVC): #
                            Renode,Restate = CurVC.pop()
                            print("\b",end="")
                            CurG.v += 1
                            CurG.adj[Renode] = []
                            VCnow = []
                            for i in range(len(CurVC))            :
                                if CurVC[i][1] == 1:
                                    VCnow.append(CurVC[i][0])
                            #print(f"{CurG.adj}")
                            for edges in G.adj[Renode]:
                                if edges not in VCnow:
                                    if edges not in CurG.adj:
                                        CurG.adj[edges] = [Renode]
                                        CurG.v += 1
                                    else:
                                        CurG.adj[edges].append(Renode)
                                    CurG.adj[Renode].append(edges)
                            CurG.e += len(CurG.adj[Renode])
                    elif nextnode_parent == (-1, -1):
                        CurVC.clear()
                        CurG = deepcopy(G)
                    else: 
                        print('error in backtracking step')
                        
        #output final quality and solution    
        for i in range(len(OptVC))            :
            if OptVC[i][1] == 1:
                solution.append(OptVC[i][0])
        # check solution quality
        if G.is_vertex_cover(solution):
            quality=G.get_solution_quality(solution)
            self.trace.add_record(quality)
            print(f"Solution is found with quality of {quality}.")

        else:
            edges_covered=G.count_covered_edges(solution)
            total_edges=G.e
            print(f"Solution is not found in time with {edges_covered} edges covered in total {total_edges} edges.")
        return quality, solution
        
def find_maxdeg(G):
    node_max = [-1, -1]
    for node in G.adj.keys():
       if len(G.adj[node]) > node_max[1]:
           node_max[0] = node
           node_max[1] = len(G.adj[node])
    return node_max

def find_mindeg(G):
    node_max = [G.v, G.v]
    for node in G.adj.keys():
       if len(G.adj[node]) < node_max[1]:
           node_max[0] = node
           node_max[1] = len(G.adj[node])
    return node_max
    
    #Calculate lowerbound of partial graph with max degree node
def Lowerbound(G):
    LB= G.e / find_maxdeg(G)[1]
    LB= ceil(LB)
    return LB
    # G_nx=nx.Graph()
    # G_nx.add_nodes_from(G.adj)
    # return len(nx.maximal_matching(G_nx))

#round LB
def ceil(d):
    if d > int(d):
        return int(d) + 1
    else:
        return int(d)

#Count size of VC for LB    
def VC_Size(VC):
	vc_size = 0
	for element in VC:
		vc_size = vc_size + element[1]
	return vc_size
    
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
 
 #raise NotImplementedError("branch_and_bound in algos/BnB.py not implemented yet")
 
 # remove redundant nodes
