"""
This file contains useful functions and classes that support the execution of the program.
"""

import json
import platform
import psutil
import logging
from time import time
from typing import List
from pathlib import Path

from graph import Graph

                         
class Timer:
    """ This class is used to measure the time spent by the algorithm and comply with the time limit """
    
    def __init__(self, time_limit: int):
        """ Constructor for the Timer class """
        self.time_limit = time_limit
        self.start_time = None
        
    def start(self):
        """ Starts the timer """
        self.start_time = time()
        
    def elapsed(self) -> float:
        """ Returns the elapsed time (in seconds) since the timer was started """
        return round(time() - self.start_time, 2)
    
    def cutoff(self) -> bool:
        """ Returns True if the time limit has been exceeded, False otherwise """
        return self.elapsed() >= self.time_limit
    
    
class Trace:
    """
    This class is used to track the best solutions found by the algorithm at each iteration,
    and to generate the requred trace file.
    It also tracks the number of access to the graph in JSON format for easier later access.
    """
    
    EXTENSION = ".trace"
    STATS_EXTENSION = ".json"
    
    def __init__(self, timer: Timer, graph: Graph):
        self.timer = timer
        self.graph = graph
        self.list = []
        self.graph_stats = []
        
    def add_record(self, quality: int):
        """ Adds a new record to the trace """
        record = (self.timer.elapsed(), quality)
        self.list.append(record)
        self.graph_stats.append((self.graph._accesses_count, self.graph._vertex_cover_check_count))
        
    def save(self, path: str):
        """ Saves the trace to a file """
        Path(path).parent.absolute().mkdir(parents=True, exist_ok=True)
        path = path + self.EXTENSION
        
        with open(path, 'w') as f:
            for idx, record in enumerate(self.list):
                f.write(str(record)[1:-1])
                if idx != len(self.list) - 1:
                    f.write('\n')
        print(f"Trace saved to {path}")
        
    def save_stats(self, path: str):
        """ Saves the graph stats to JSON"""
        Path(path).parent.absolute().mkdir(parents=True, exist_ok=True)
        path = path + self.STATS_EXTENSION
        
        # Create the dictionary
        data = {
                "time": [record[0] for record in self.list],
                "quality": [record[1] for record in self.list],
                "graph_reads": [stat[0] for stat in self.graph_stats],
                "vertex_cover_checks": [stat[1] for stat in self.graph_stats]
            }
            
        # Save to JSON
        with open(path, 'w') as f:
            f.write(json.dumps(data, indent=4))  
        print(f"Trace stats saved to {path}")
                
                
def save_solution(path: str, quality: int, solution: List[int]):
    """ Saves the algoirthm solution to a file """
    EXTENSION = ".sol"
    path = path + EXTENSION
    Path(path).parent.absolute().mkdir(parents=True, exist_ok=True)
    
    formatted_solution = str(solution)[1:-1].replace(" ", "")
    with open(path, 'w') as f:
        f.write(f"{quality}\n{formatted_solution}")
    print(f"Solution saved to {path}")
        

def get_sys_info():
    """ Collects and prints system information """
    
    try:
        info={}
        info['platform'] = platform.system()
        info['platform-release'] = platform.release()
        info['platform-version'] = platform.version()
        info['architecture'] = platform.machine()
        info['processor'] = platform.processor()
        info['ram'] = str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
    
    except Exception as e:
        logging.exception(e)
        
    return info