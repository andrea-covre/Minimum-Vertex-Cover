# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 23:26:46 2022

@author: yifan
"""

import time 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%% 

def load_trace_file(filename):
    raise NotImplementedError("")

def calc_qrtd(trace):
    raise NotImplementedError("")

def calc_sqd(trace):
    raise NotImplementedError("")

def plot_boxplot(trace):
    raise NotImplementedError("")


def plot_qrtd(qrtd):
    raise NotImplementedError("")

def plot_sqd(sqd):
    raise NotImplementedError("")

#%%
# import trace file from different runs 
filename=""
trace=load_trace_file(filename)


# calculation

# Qualified Runtime for various solution qualities

qrtd=calc_qrtd(trace)
# Solution Quality Distributions for various run-times

sqd=calc_sqd(trace)


# plot 
plot_qrtd(qrtd)
plot_sqd(sqd)
plot_boxplot(trace)
