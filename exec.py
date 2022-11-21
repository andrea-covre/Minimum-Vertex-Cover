"""
This file is the entry point for the project, it parses the arguments and
runs the selected algorithm on the selected dataset.

It can be executed following the required format:
$ python -m exec -inst <filename> -alg [BnB|Approx|LS1|LS2] -time <cutoff in seconds> -seed <random seed>
"""

import platform
import psutil
import logging
import argparse
import random

from graph import Graph


ALGOS = ['BnB', 'Approx', 'LS1', 'LS2']

def print_sys_info():
    """ Collects and prints system information """
    
    try:
        info={}
        info['platform'] = platform.system()
        info['platform-release'] = platform.release()
        info['platform-version'] = platform.version()
        info['architecture'] = platform.machine()
        info['processor'] = platform.processor()
        info['ram'] = str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
    
        for k, v in info.items():
            print(f"{k}: {v}")
    
    except Exception as e:
        logging.exception(e)
        
        
def parse_args():
    """ Parses the arguments passed to the script """
    
    # Creating the parser
    parser = argparse.ArgumentParser(description='Run the selected algorithm on the selected dataset')
    
    parser.add_argument('-inst', type=str, help='path to graph dataset', required=True)
    parser.add_argument('-alg', choices=ALGOS, help='algorithm to run', required=True)
    parser.add_argument('-time', type=int, help='cutoff time in seconds', required=True)
    parser.add_argument('-seed', type=int, help='random seed', required=True)
    
    return parser.parse_args()


def main():
    """ Main function that executes the selected algorithm on the selected dataset """
    args = parse_args()
    G = Graph("data/dummy1.graph")
    print(G.v)
    print(G.e)
    for k, v in G.adj.items():
        print(k, v)
        
    random.seed(args.seed)
    print(random.randint(0, 1000))
    

if __name__ == '__main__':
    main()
