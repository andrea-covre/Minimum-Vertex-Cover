"""
This file contains useful functions and classes that support the execution of the program.
"""

import platform
import psutil
import logging

from time import time
from typing import List

                         
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
    """ This class is used to track the best solutions found by the algorithm at each iteration """
    
    def __init__(self, timer: Timer):
        self.timer = timer
        self.list = []
        
    def add_record(self, quality: int):
        """ Adds a new record to the trace """
        record = (self.timer.elapsed(), quality)
        self.list.append(record)
        
    def save(self, path: str):
        """ Saves the trace to a file """
        with open(path, 'w') as f:
            for idx, record in enumerate(self.list):
                f.write(str(record)[1:-1])
                if idx != len(self.list) - 1:
                    f.write('\n')
        print(f"Trace saved to {path}")
                
                
def save_solution(path: str, quality: int, solution: List[int]):
    """ Saves the algoirthm solution to a file """
    
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