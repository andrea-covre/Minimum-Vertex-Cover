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

TIME_START = 0
TIME_STOP = 1000
TIME_RESOLUTION = 200
CUTOFF_TIMES = np.linspace(TIME_START, TIME_STOP, TIME_RESOLUTION)

QUALITIES_START = 2200
QUALITIES_STOP = 2260
QUALITIES_RESOLUTION = 200
QUALITIES = np.linspace(QUALITIES_START, QUALITIES_STOP, QUALITIES_RESOLUTION)

CUTOFF_TIMES_LOOSE = [10, 40, 100, 1000]
QUALITIES_LOOSE = [2200, 2210, 2220, 2230, 2240]

OPT = {"power": 2203, "star2": 4542}

# %% functions


def load_trace_file(filename):
    trace = pd.read_csv(filename, header=None)
    trace.columns = ["time", "quality"]
    return trace


def load_trace_files(dir, graph, algo):
    pattern = f"{graph}_{algo}_[\S\s]*\.trace"
    traces = []
    for path, subdirs, files in os.walk(dir):
        for file in files:
            if regex.match(pattern, file):
                traces.append(load_trace_file(path+"\\"+file))
    
    return pd.concat(traces)


def calc_qrtd(graph, trace: pd.DataFrame, cutoff_times, qualities):
    qrtd = pd.DataFrame(index=cutoff_times, columns=qualities)
    for cutoff_time in cutoff_times:
        for quality in qualities:
            n_runs = len(trace[(((trace.quality-OPT[graph])/OPT[graph]) <= quality)].axes[0])
            n_success = len(trace[(trace.time <= cutoff_time) & (
                ((trace.quality-OPT[graph])/OPT[graph]) <= quality)].axes[0])
            qrtd.at[cutoff_time, quality] = n_success / \
                n_runs if n_runs != 0 else 0
    return qrtd


def calc_sqd(graph, trace, cutoff_times, qualities):
    sqd = pd.DataFrame(index=qualities, columns=cutoff_times)
    for cutoff_time in cutoff_times:
        for quality in qualities:
            n_runs = len(trace[(trace.time <= cutoff_time)].axes[0])
            n_success = len(trace[(trace.time <= cutoff_time) & (((trace.quality-OPT[graph])/OPT[graph])<= quality)].axes[0])
            sqd.at[quality, cutoff_time] = n_success / \
                n_runs if n_runs != 0 else 0
    return sqd


def plot_boxplot(trace):
    raise NotImplementedError("")


def plot_qrtd(qrtd: pd.DataFrame):
    fig, ax1 = plt.subplots()
    for column in qrtd.columns:
        qrtd.plot(y=column, ax=ax1, logx=True)
    plt.title(f"QRTD plot for {algo} on {graph}.graph")
    plt.xlabel("cutoff time/s")
    plt.ylabel(r"$P_{solve}$")
    plt.show()


def plot_sqd(sqd: pd.DataFrame):
    fig, ax1 = plt.subplots()
    for column in sqd.columns:
        sqd.plot(y=column, ax=ax1)
    plt.title(f"SQD plot for {algo} on {graph}.graph")
    plt.xlabel("quality")
    plt.ylabel(r"$P_{solve}$")
    plt.show()

def get_cutoff_times(start, stop, resolution, mode):
    if mode=="linear":
        return np.round(np.linspace(start, stop, resolution),decimals=2)
    elif mode=="log":
        return np.round(np.geomspace(stop**(1/resolution), stop, num=resolution),decimals=2)
    else:
        raise ValueError("mode not supported")


def get_qualities(start, stop, resolution, mode):
    if mode=="linear":
        return np.round(np.linspace(start, stop, resolution),decimals=4)
    elif mode=="log":
        return np.round(np.geomspace(stop**(resolution), stop, num=resolution),decimals=4)
    else:
        raise ValueError("mode not supported")

# %% load trace
# import trace file from different runs
filename = r"E:\Users\wizar\OneDrive\Documents\github\CSE-6140-project\plotting\star\power_LS1_1000_20221203.trace"
dirname = "."
graph = "power"
algo = "LS1"
# trace=load_trace_file(filename)
trace = load_trace_files(dirname, graph, algo)
# print(trace.columns)

# %% calculation


# Qualified Runtime for various solution qualities
max_q=(max(trace["quality"])-OPT[graph])/OPT[graph]
print(max_q)
qrtd = calc_qrtd(graph, trace, get_cutoff_times(0, 1000, 200, "log"), get_qualities(0,max_q,5,"linear"))
print(qrtd)
# Solution Quality Distributions for various run-times

sqd = calc_sqd(graph, trace, get_cutoff_times(0, 1000, 5, "log"), get_qualities(0,max_q,200,"linear"))
# print(sqd)

# %% plot
plot_qrtd(qrtd)
plot_sqd(sqd)
plot_boxplot(trace)
