"""
This file is the entry point for the project, it parses the arguments and
runs the selected algorithm on the selected dataset.

It can be executed following the required format:
$ python -m exec -inst <filename> -alg [BnB|Approx|LS1|LS2] -time <cutoff in seconds> -seed <random seed>
"""

import os
import random
import argparse

from graph import Graph
from utils import Timer, Trace, save_solution, get_sys_info
from algos.BnB import branch_and_bound
from algos.Approx import heuristic_with_approximation
from algos.LS1 import first_local_search
from algos.LS2 import second_local_search


OUTPUT_DIR = 'output'
ALGOS = {
    'BnB': {
        "func": branch_and_bound,
        "deterministic": False,         # TODO: confirm if is deterministic
    },
    'Approx': {
        "func": heuristic_with_approximation,
        "deterministic": False,         # TODO: confirm if is deterministic
    },
    'LS1': {
        "func": first_local_search,
        "deterministic": False,         # TODO: confirm if is deterministic
    },
    'LS2': {
        "func": second_local_search,
        "deterministic": False,         # TODO: confirm if is deterministic
    }
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


def main():
    """ Main function that executes the selected algorithm on the selected dataset """
    
    # Parsing the arguments
    args = parse_args()
    
    # Setting the random seed
    random.seed(args.seed)
    
    # Loading the graph
    G = Graph(args.inst)
    
    # Getting the algorithm to run
    algorithm = ALGOS[args.alg]["func"]
    
    # Printing system, execution, and graph info
    print("========= System Info =========")
    for key, value in get_sys_info().items():
        print(f"{key + ':':<20} {value}")
        
    print("\n========= Arguments =========")
    for arg in vars(args):
        print(f"{arg + ':':<20} {getattr(args, arg)}")
        
    instance_name = os.path.splitext(os.path.basename(args.inst))[0]
    print("\n========= Graph =========")
    print(f"{'Graph name:':<20} {instance_name}")
    print(f"{'Number of vertices:':<20} {G.v}")
    print(f"{'Number of edges:':<20} {G.e}")
    
    # Creating the timer and the trace
    timer = Timer(args.time)
    trace = Trace(timer)
    
    # Running the selected algorithm
    print(f"\n>> Running {args.alg} on {instance_name}...\n")
    timer.start()
    quality, solution = algorithm(G, timer, trace)
    time_elapsed = timer.elapsed()
    
    # Printing results
    print("\n========= Results =========")
    print(f"{'Solution found:':<20} {solution}")
    print(f"{'Quality of solution:':<20} {quality}")
    print(f"{'Solution coverage:':<20} {(quality/G.v)*100:.2f}%")
    print(f"{'Time elapsed:':<20} {time_elapsed} s")
    print(f"{'Graph reads:':<20} {G._accesses_count}")
    print("")
    
    # Creating output files
    is_deterministic = ALGOS[args.alg]["deterministic"]
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    output_name = f"{instance_name}_{args.alg}_{args.time}"
    if not is_deterministic:
        output_name = f"{output_name}_{args.seed}"
    
    trace.save(os.path.join(OUTPUT_DIR, f"{output_name}.trace"))
    save_solution(os.path.join(OUTPUT_DIR, f"{output_name}.sol"), quality, solution)
    
    

if __name__ == '__main__':
    main()
