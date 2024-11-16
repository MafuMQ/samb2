#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 11:57:27 2024

@author: mafu

requres: aima-python(https://github.com/aimacode/aima-python/blob/master/search.py), sortedcontainers, ipythonblocks, qpsolvers, qpsolvers[open_source_solvers] matplotlib
"""
import sys
aima_modules = r"C:\Users\Mafu\Github\aima-python"
sys.path.insert(0,aima_modules) #inset at the beginning to override jupyter's notebook.py


from search import *
from notebook import psource, heatmap, gaussian_kernel, show_map, final_path_colors, display_visual, plot_NQueens

# Needed to hide warnings in the matplotlib sections
import warnings
warnings.filterwarnings("ignore")

psource(GraphProblem)
