"""
This script will run exec.py for all the alogrithms and graphs to generate
all the solution and trace files.

It can be executed following the required format:
$ python -m runner -time <cutoff in seconds> -seed <random seed>
"""

import os
import argparse
from exec import ALGOS, print_args

__GRAPHS_DIR__ = 'data'

def parse_args():
    """ Parses the arguments passed to the script """
    
    # Creating the parser
    parser = argparse.ArgumentParser(description='Run all the algorithms on all datasets')
    
    parser.add_argument('-time', type=int, help='cutoff time in seconds', required=True)
    parser.add_argument('-seed', type=int, help='random seed', required=True)
    
    return parser.parse_args()


def get_graphs():
    """ Getting all graphs filenames """
    items = os.listdir(__GRAPHS_DIR__)
    return [item for item in items if item.endswith('.graph')]


def main():
    args = parse_args()
    print_args(args)
    
    for algo in ALGOS.keys():
        for graph in get_graphs():
            os.system(f"python -m exec -inst {__GRAPHS_DIR__}/{graph} -alg {algo} -time {args.time} -seed {args.seed}")
    

if __name__ == '__main__':
    main()
    