import sys
sys.path.append('./')
sys.path.append('./Prior/')
from parallel import *
from fit_prior import read_prior_par

import numpy as np
import pandas as pd
import time
import datetime
import warnings
warnings.filterwarnings('ignore')

import matplotlib.pyplot as plt
from copy import deepcopy

# Function to store models to .txt file
def store_models(col_list, models, filename, col):
    # Accepted model: make file with combined array, everything in order
    n = m = 0
    directory = './Ini_Testing/' + filename
    with open(directory, 'w') as f:
        f.writelines(",".join(col_list))
        f.writelines("\n")
        while m < len(models):
            m = m + col
            f.writelines(",".join(models[n:m]))
            f.writelines("\n")
            n = m


# Initialize the parallel machine scientist
param_num = 4  # number of constants
Ts = [1]
pms = Parallel(
    Ts,
    parameters=['a%d' % i for i in range(param_num)],
    max_size=30,
)

# Sampling
nstep = 4000 #Number of MCMC steps

# MCMC
mdl, mdl_model = np.inf, None
main_models = []
all_models = []
description_lengths = []
total_nops_trajectory = np.zeros(nstep)
# Record time
start_time = time.time()

for i in range(nstep):
    # MCMC update
    pms.mcmc_step()  # MCMC step within each T
    ######### One temp ###############################
    description_lengths.append(pms.t1.E)
    # print('model', pms.t1, 'EB and EP', pms.t1.EB, pms.t1.EP, 'TC', pms.t1.bool_thermo, pms.t1.axiom)
    print('model', pms.t1, 'EP', pms.t1.EP, 'Size', pms.t1.size, pms.t1.bool_thermo, pms.t1.axiom)
    all_models.append(str(pms.t1))
    all_models.append(str(pms.t1.E))  # Add the description length to the trace
    all_models.append(str(pms.t1.size))  # Number of nodes
    total_nops = 0
    for key in pms.t1.nops.keys():
        total_nops += pms.t1.nops[key]
    total_nops_trajectory[i] = total_nops
    # all_models.append(str(pms.t1.sse['d0']))  # Add sse of current tree

    ###################################################

    # Check if this is the MDL expression so far
    if pms.t1.E < mdl:
        mdl, mdl_model = pms.t1.E, deepcopy(pms.t1)
        print('mdl', mdl_model)
        main_models.append(str(mdl_model))  # store model
        main_models.append(str(mdl))  # list for description lengths
        main_models.append(str(pms.t1.size))
        # main_models.append(str(mdl_model.sse['d0']))  # Add sse of current tree
        # code breaks with 0 parameters so try-except was placed for constant

# Results
runtime = round(time.time() - start_time)
print('Time Elapsed:\t', str(datetime.timedelta(seconds=runtime)))
print(mdl_model)
print('Description length: ', mdl)
print(mdl_model.par_values['d0'])
print('Langmuir param: C1 = 38.9, C2 = 6.3')

# Description length
plt.figure(figsize=(15, 5))
plt.plot(description_lengths)
plt.title('MDL model: %s' % str(mdl_model))
plt.xlabel('MCMC step', fontsize=14)
plt.ylabel('Description length', fontsize=14)
plt.tight_layout()
plt.savefig('mdl_trajectory.jpeg', dpi=360)

# Num ops 
plt.figure(figsize=(15, 5))
plt.hist(total_nops_trajectory)
plt.title('Without data, without TC, complexity_factor = 0, 2000 steps, 15 nodes max')
plt.xlabel('total number of operations of tree', fontsize=14)
plt.ylabel('Frequency', fontsize=14)
plt.tight_layout()
plt.savefig('hist_nops_dist.jpeg', dpi=360)
######### 1 Temp ######################
# col_list_all = ['Model','Description length', 'SSE'] + mdl_model.parameters
col_list_all = ['Model','Description length', 'Num of Ops'] + mdl_model.parameters
store_models(col_list_all, all_models, 'All_Models.txt', len(col_list_all))
