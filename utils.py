"""
This file contains useful functions and classes that support the execution of the program.
"""

import platform
import psutil
import logging

from time import time

                         
class Timer:
    """ This class is used to measure the time spent by the algorithm and comply with the time limit """
    
    def __init__(self, time_limit: int):
        """ Constructor for the Timer class """
        self.time_limit = None
        self.start_time = time_limit
        
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
            for record in self.list:
                f.write(f"{record}\n")


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