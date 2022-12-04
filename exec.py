"""
This file is the entry point for the project, it parses the arguments and
runs the selected algorithm on the selected dataset.

It can be executed following the required format:
$ python -m exec -inst <filename> -alg [BnB|Approx|LS1|LS2] -time <cutoff in seconds> -seed <random seed>
"""

import os
import random
import argparse
import tracemalloc
import numpy as np

from graph import Graph
from vertex_cover import Vertex_Cover
from utils import Timer, Trace, save_solution, get_sys_info
from algos.BnB import BnB
from algos.Approx import Approx
from algos.LS1 import LS1
from algos.LS2 import LS2


OUTPUT_DIR = 'output'
STATS_DIR = 'stats'
ALGOS = {
    'BnB': BnB,
    'Approx': Approx,
    'LS1': LS1,
    'LS2': LS2,
}

        
def parse_args():
    """ Parses the arguments passed to the script """
    
    # Creating the parser
    parser = argparse.ArgumentParser(description='Run the selected algorithm on the selected dataset')
    
    parser.add_argument('-inst', type=str, help='path to graph dataset', required=True)
    parser.add_argument('-alg', choices=ALGOS.keys(), help='algorithm to run', required=True)
    parser.add_argument('-time', type=int, help='cutoff time in seconds', required=True)
    parser.add_argument('-seed', type=int, help='random seed', required=True)
    
    return parser.parse_args()


def print_sys_info() -> None:
    """ Printing system, execution, and graph info """
    print("========= System Info =========")
    for key, value in get_sys_info().items():
        print(f"{key + ':':<20} {value}")
        

def print_args(args: argparse.Namespace) -> None:
    print("\n========= Arguments =========")
    for arg in vars(args):
        print(f"{arg + ':':<20} {getattr(args, arg)}")
        
    
def print_graph_info(graph: Graph, instance_name: str) -> None:
    """ Printing graph info """
    print("\n========= Graph =========")
    print(f"{'Graph name:':<20} {instance_name}")
    print(f"{'Number of vertices:':<20} {graph.v}")
    print(f"{'Number of edges:':<20} {graph.e}")

def main():
    """ Main function that executes the selected algorithm on the selected dataset """
    
    # Parsing the arguments
    args = parse_args()
    
    # Setting the random seed
    random.seed(args.seed)    # NOTE: TODO: disabled seed for testing
    np.random.seed(args.seed)
    
    # Loading the graph
    G = Vertex_Cover(args.inst)
    
    # Getting the algorithm to run
    algorithm = ALGOS[args.alg]()
    
    print_sys_info()
    print_args(args)
        
    instance_name = os.path.splitext(os.path.basename(args.inst))[0]
    
    print_graph_info(G, instance_name) 
    
    # Creating the timer and the trace
    timer = Timer(args.time)
    trace = Trace(timer, G)
    
    # Running the selected algorithm
    print(f"\n>> Running {args.alg} on {instance_name}...\n")
    tracemalloc.start()
    timer.start()
    quality, solution = algorithm.get_vertex_cover(G, timer, trace)
    time_elapsed = timer.elapsed()
    
    memory_usage = tracemalloc.get_traced_memory()
    trace.current_memory_usage = memory_usage[0]
    trace.peak_memory_usage = memory_usage[1]
    
    print("\n\n")
    print_sys_info()
    print_args(args)
    print_graph_info(G, instance_name) 
    
    # Printing results
    print("\n========= Results =========")
    print(f"{'Quality of solution:':<20} {quality}")
    print(f"{'Time elapsed:':<20} {time_elapsed} s")
    print(f"{'Graph reads:':<20} {G._accesses_count}")
    print(f"{'Vertex cover checks:':<20} {G._vertex_cover_check_count}")
    print(f"{'Current memory usage:':<20} {memory_usage[0]}")
    print(f"{'Peak memory usage:':<20} {memory_usage[1]}")
    print(f"{'Solution found:':<20} {solution}")
    print("")
    
    # Creating output files    
    output_name = f"{instance_name}_{args.alg}_{args.time}"
    if algorithm.IS_DETERMINISTIC == False:
        output_name = f"{output_name}_{args.seed}"
    
    trace.save(os.path.join(OUTPUT_DIR, f"{output_name}"))
    trace.save_stats(os.path.join(STATS_DIR, f"{output_name}"))
    save_solution(os.path.join(OUTPUT_DIR, f"{output_name}"), quality, solution)
    
    

if __name__ == '__main__':
    main()
