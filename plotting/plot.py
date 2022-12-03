# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 23:26:46 2022

@author: yifan, zhaonan
"""

import os
import regex
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

TIME_START=0
TIME_STOP=100
TIME_RESOLUTION=100
CUTOFF_TIMES=np.linspace(TIME_START, TIME_STOP, TIME_RESOLUTION)

QUALITIES_START=2200
QUALITIES_STOP=2260
QUALITIES_RESOLUTION=100
QUALITIES=np.linspace(QUALITIES_START, QUALITIES_STOP, QUALITIES_RESOLUTION)

CUTOFF_TIMES_LOOSE=[20,40,60,80]
QUALITIES_LOOSE=[2200, 2210, 2220, 2230, 2240]


#%% functions
def load_trace_file(filename):
    trace = pd.read_csv(filename,header=None)
    trace.columns=["time","quality"]
    return trace

def load_trace_files(dir,graph,algo):
    pattern=f"{graph}_{algo}_[\S\s]*\.trace"
    traces=[]
    for path, subdirs, files in os.walk(dir):
        for file in files:
            if regex.match(pattern,file):
                traces.append(load_trace_file(path+"\\"+file))
    return pd.concat(traces)

def calc_qrtd(trace:pd.DataFrame,cutoff_times,qualities):
    qrtd=pd.DataFrame(index=cutoff_times,columns=qualities)
    for cutoff_time in cutoff_times:
        for quality in qualities:
            n_runs=len(trace.axes[0])
            n_success=len(trace[(trace.time<=cutoff_time) & (trace.quality<=quality)].axes[0])
            qrtd.at[cutoff_time,quality]=n_success/n_runs
    return qrtd

def calc_sqd(trace,cutoff_times,qualities):
    sqd=pd.DataFrame(index=qualities, columns=cutoff_times)
    for cutoff_time in cutoff_times:
        for quality in qualities:
            n_runs=len(trace.axes[0])
            n_success=len(trace[(trace.time<=cutoff_time) & (trace.quality<=quality)].axes[0])
            sqd.at[quality, cutoff_time]=n_success/n_runs
    return sqd

def plot_boxplot(trace):
    raise NotImplementedError("")


def plot_qrtd(qrtd:pd.DataFrame):
    fig, ax1 = plt.subplots()
    for column in qrtd.columns:
        qrtd.plot(y=column, ax=ax1)
    plt.show()

def plot_sqd(sqd:pd.DataFrame):
    fig, ax1 = plt.subplots()
    for column in sqd.columns:
        sqd.plot(y=column, ax=ax1)
    plt.show()



#%% load trace
# import trace file from different runs 
filename=r"C:\Users\wizar\OneDrive\Documents\github\CSE-6140-project\plotting\star\power_LS1_1000_20221203.trace"
dirname=r"C:\Users\wizar\OneDrive\Documents\github\CSE-6140-project\plotting"
graph="power"
algo="LS1"
# trace=load_trace_file(filename)
trace=load_trace_files(dirname, graph, algo)
# print(trace)

#%% calculation

# Qualified Runtime for various solution qualities

qrtd=calc_qrtd(trace, CUTOFF_TIMES, QUALITIES_LOOSE)
print(qrtd)
# Solution Quality Distributions for various run-times

sqd=calc_sqd(trace, CUTOFF_TIMES_LOOSE, QUALITIES)
# print(sqd)

#%% plot 
plot_qrtd(qrtd)
plot_sqd(sqd)
plot_boxplot(trace)
