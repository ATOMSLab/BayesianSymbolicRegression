# import sys

# vscode
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


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
import random
from copy import deepcopy


# Function to store models to .txt file
def store_models(col_list, models, filename, col):
    # Accepted model: make file with combined array, everything in order
    n = m = 0
    # directory = './Results/2104_Testing_woTC_20_N2dataset/' + filename
    directory = './Ini_Testing/' + filename
    # directory = './Results/2104_Testing_isobutane/' + filename
    with open(directory, 'w') as f:
        f.writelines(",".join(col_list))
        f.writelines("\n")
        while m < len(models):
            m = m + col
            f.writelines(",".join(models[n:m]))
            f.writelines("\n")
            n = m



### Nitrogen dataset ###
nitrogen_dataset = False
if nitrogen_dataset:
# Import data
    XLABS = [
        'p',
    ]
    raw_data = pd.read_csv('./Dataset/Langmuir1918nitrogen.csv')
    raw_data = raw_data.append({'p': 0, 'q obs': 0}, ignore_index=True)  # Unit of P is bar
    x, y = raw_data[XLABS], raw_data['q obs']
    
### Isobutane dataset Sun1998 ###
isobutane_dataset = False

if isobutane_dataset:
    XLABS = ['p']
    raw_data = pd.read_csv('./Dataset/Sun1998isobutane.csv', nrows=17)
    raw_data = raw_data.drop(columns=['T (K)'])
    raw_data = raw_data.rename(columns={'P (kPa)': 'p'})
    x, y = raw_data[XLABS], raw_data['q (mol/kg)']

bet_dataset = True

if bet_dataset: 
    XLABS = ['p']
    raw_data = pd.read_csv('./Dataset/Brunauer1938adsorptionUpdated.csv')
    raw_data = raw_data.append({'p':0, 'q obs':0}, ignore_index=True)
    x,y = raw_data[XLABS],raw_data['q obs']

# Initialize BMS
# Read the hyperparameters for the prior
prior_par = read_prior_par('treated_prior.dat')

# Set the temperatures
# Ts = [1] + [1.04**k for k in range(1, 20)]
# Ts = [1] + [1.5**k for k in range(1, 5)]
Ts = [1]

# Initialize the parallel machine scientist
param_num = 4 # number of constants
pms = Parallel(
    Ts,
    variables=XLABS,
    parameters=['a%d' % i for i in range(param_num)],
    x=x, y=y,
    max_size=30,
    # prior_par=prior_par,
    # from_string='(((p * _a2_) / (_a3_ + p)) + ((p * _a0_) / (_a1_ + p)))'
    # from_string='((p * _a2_) / (_a3_ + p))'
    #from_string='_a1_ * p + _a2_'
)
# print('Initial tree', pms.t1)
# Sampling
nstep = 500 #Number of MCMC steps

# MCMC
mdl, mdl_model = np.inf, None
main_models = []
if len(Ts) > 1:
    all_models = [[] for i in range(len(Ts))]
else:
    all_models = []
description_lengths = []
total_nops_trajectory = np.zeros(nstep)
# Record time
start_time = time.time()

for i in range(nstep):
    # MCMC update
    pms.mcmc_step()  # MCMC step within each T
    ######### Multi- temps ###########################
    if len(Ts) > 1:
        pms.tree_swap()  # Attempt to swap two randomly selected consecutive temps
        description_lengths.append(pms.t1.E)
        # print('model', pms.t1, 'EB', pms.t1.EB, 'EP', pms.t1.EP, 'TC', pms.t1.bool_thermo, pms.t1.axiom)
        for j in range(len(Ts)):
            tree_item = pms.trees[str(Ts[j])]        
            # calculating total number of operations in the tree
            total_nops = 0
            for key in tree_item.nops.keys():
                total_nops += tree_item.nops[key]
            all_models[j].append(str(tree_item))  # Add the equations found
            all_models[j].append(str(total_nops))  # Total num ops
            all_models[j].append(str(round(tree_item.E, 5)))  # Add the description length to the trace
            all_models[j].append(str(round(tree_item.EB, 5)))  # Add the EB to the trace
            all_models[j].append(str(round(tree_item.EP, 5)))  # Add the EP to the trace
            all_models[j].append(str(round(tree_item.sse['d0'], 5)))  # Add sse of current tree
            all_models[j].append(str(tree_item.bool_thermo))  # Add TC Boolean
            all_models[j].append(tree_item.axiom)  # Add the violated TC
            # code breaks with 0 parameters so try-except was placed for constant
            try:
                for count in range(param_num):
                    all_models[j].append(str(tree_item.par_values['d0'][tree_item.parameters[count]]))
            except KeyError:
                all_models[j].append('None')
                all_models[j].append('None')

    ######### One temp ###############################
    else:
        # calculating total number of operations in the tree
        total_nops = 0
        for key in pms.t1.nops.keys():
            total_nops += pms.t1.nops[key]
        total_nops_trajectory[i] = total_nops
        description_lengths.append(pms.t1.E)
        print('model', pms.t1, 'EB and EP', pms.t1.EB, pms.t1.EP, 'TC', pms.t1.bool_thermo, pms.t1.axiom)
        all_models.append(str(pms.t1))
        all_models.append(pms.t1.canonical())
        all_models.append(str(total_nops))  # total num of ops
        all_models.append(str(round(pms.t1.E, 5)))  # Add the description length to the trace
        all_models.append(str(round(pms.t1.EB, 5)))  # Add the EB to the trace
        all_models.append(str(round(pms.t1.EP, 5)))  # Add the EP to the trace
        all_models.append(str(round(pms.t1.sse['d0'], 5)))  # Add sse of current tree
        all_models.append(str(pms.t1.bool_thermo))  # Add TC Boolean
        all_models.append(pms.t1.axiom)  # Add the violated TC
        # code breaks with 0 parameters so try-except was placed for constant
        try:
            for count in range(param_num):
                all_models.append(str(pms.t1.par_values['d0'][pms.t1.parameters[count]]))
        except KeyError:
            all_models.append('None')
            all_models.append('None')
    ###################################################

    # Check if this is the MDL expression so far
    if pms.t1.E < mdl:
        mdl, mdl_model = pms.t1.E, deepcopy(pms.t1)
        print('mdl', mdl_model)
        print('Canonical form', mdl_model.canonical())
        main_models.append(str(mdl_model))  # store model
        main_models.append(mdl_model.canonical())
        main_models.append(str(round(mdl, 5)))  # list for description lengths
        main_models.append(str(round(mdl_model.EB, 5)))  # EB
        main_models.append(str(round(mdl_model.EP, 5)))  # EP
        main_models.append(str(mdl_model.sse['d0']))  # Add sse of current tree
        main_models.append(str(i+1)) # step achieving mdl
        main_models.append(str(mdl_model.bool_thermo))  # Add TC Boolean
        main_models.append(mdl_model.axiom)  # Add the violated TC
        # code breaks with 0 parameters so try-except was placed for constant
        try:
            for count in range(param_num):
                main_models.append(str(mdl_model.par_values['d0'][mdl_model.parameters[count]]))
        except KeyError:
            main_models.append('None')
            main_models.append('None')

# Results
runtime = round(time.time() - start_time)
print('Time Elapsed:\t', str(datetime.timedelta(seconds=runtime)))
print(mdl_model)
print('Canonical form', mdl_model.canonical())
print('Description length: ', mdl)
print(mdl_model.par_values['d0'])
# print('Langmuir param: C1 = 38.9, C2 = 6.3')
# print(main_models)
print('Error trees: ', pms.t1.tree_error)

# Parity plot
fig, ax = plt.subplots(1, 2, figsize=(10,5))
ax[0].plot(mdl_model.predict(x), y, 'ro')
ax[0].plot([0, 36], [0, 36], 'b-')
ax[0].set_title('Parity plot')
ax[0].set_xlabel('predicted q')
ax[0].set_ylabel('Observed q')

# Function plot
data = np.arange(0, 35, 0.01)
p_array = pd.DataFrame(data, columns=['p'])
ax[1].plot(p_array, mdl_model.predict(p_array), label='Predicted model')
ax[1].plot(p_array, 38.9*p_array/(p_array+6.3), label='Langmuir')
ax[1].scatter(x, y, color='r', label='Observed data')  # Data from last run
ax[1].set_xlabel('p')
ax[1].set_ylabel('q')
ax[1].legend()
fig.savefig('plot_model.jpeg', dpi=360)

# description length
plt.figure(figsize=(15, 5))
plt.plot(description_lengths)
plt.title('MDL model: %s' % str(mdl_model))
plt.xlabel('MCMC step', fontsize=14)
plt.ylabel('Description length', fontsize=14)
plt.tight_layout()
plt.savefig('mdl_trajectory.jpeg', dpi=360)

# Num ops 
if len(Ts) == 1:
    plt.figure(figsize=(15, 5))
    plt.hist(total_nops_trajectory)
    plt.title('With N2 data, with TC, complexity_factor = 0, 2000 steps, 15 nodes max')
    plt.xlabel('total number of operations of tree', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.tight_layout()
    plt.savefig('hist_nops_dist.jpeg', dpi=360)

######### Multiple temps ##############
if len(Ts) > 1:
# All models of first 5 Temps: make file with combined array, everything in order
    filename_list = []
    col_list_all = ['Model', 'Total num ops', 'Description length', 'EB', 'EP', 'SSE', 'TC Bool', 'Axiom'] + mdl_model.parameters
    for i in range(len(Ts)):
        filename_list.append('All_models_T' + str(i + 1) + '.txt')
    for i in range(len(Ts)):
        store_models(col_list_all, all_models[i], filename_list[i], len(col_list_all))
######### 1 Temp ######################
else:
    #rand_str = str(0.5*random.random())[2:8]
    
    thisTime = time.time()
    timeStr = str(thisTime)
    
    col_list_all = ['Model', 'Canonical form', 'Total num ops', 'Description length', 'EB', 'EP', 'SSE', 'TC Bool', 'Axiom'] + mdl_model.parameters
    store_models(col_list_all, all_models, 'All_Models' + timeStr + '.txt', len(col_list_all))


# Accepted model: make file with combined array, everything in order
col_list_main = ['Model', 'Canonical form', 'Description length', 'EB', 'EP', 'SSE', 'Step of acceptance', 'TC Bool', 'Axiom'] + mdl_model.parameters
store_models(col_list_main, main_models, 'Accepted_Models' + timeStr + '.txt', len(col_list_main))
