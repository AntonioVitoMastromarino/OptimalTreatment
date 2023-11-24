import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd
import os 
from classify import score_gridpoint

gridpoint_path = "/Users/irismarmouset-delataille/Desktop/OptimalTreatment/data"
def read_gridpoint(gridpoint_path):
    """
    Apply score_gridpoint function to all the points of the gridpoint:
    
    """
    scores = pd.DataFrame(columns=['Gridpoint_ID', 'a', 'b', 'd', 'k', 'r', 's', 'Tfinal', 'threshold', 'Tsteps', 'Initial_condition', 'survival_rate', 'mean_survival_time', 'mean_tumour_size'])
    for gridpoint_id in os.listdir(gridpoint_path):
        with open("a", 'r') as file: a = file.read().strip()
        with open("b", 'r') as file: b = file.read().strip()
        with open("d", 'r') as file: d = file.read().strip()
        with open("k", 'r') as file: k = file.read().strip()
        with open("r", 'r') as file: r = file.read().strip()
        with open("s", 'r') as file: s = file.read().strip()
        with open("Tfinal", 'r') as file: Tfinal = file.read().strip()
        with open("Tsteps", 'r') as file: Tsteps = file.read().strip()
        with open("threshold", 'r') as file: threshold = file.read().strip()

        initial_condition_0_path = os.path.join(gridpoint_path, gridpoint_id, "0")
        initial_condition_1_path = os.path.join(gridpoint_path, gridpoint_id, "1")
        initial_condition_2_path = os.path.join(gridpoint_path, gridpoint_id, "2")
        initial_condition_paths = ['initial_condition_0_path', 'initial_condition_1_path', 'initial_condition_2_path']
        for intitial_condition in initial_condition_paths:
            file_path = os.path.join(intitial_condition, 't')
            with open(file_path, 'r') as trajectory_file:
                trjs =
                max_tumour_size = 
                min_tumour_size =
                eps_ss =
                eps_orbit =
                survival_rate, mean_survival_time, mean_tumour_size = score_gridpoint(trjs, max_tumour_size, min_tumour_size, eps_ss, eps_orbit)
                score = [gridpoint_id, a, b, d, k, r, s, Tfinal, Tsteps, threshold, , survival_rate, mean_survival_time, mean_tumour_size]
                scores.append(score)
          


    
    





