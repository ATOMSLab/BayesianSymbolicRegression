# This file contains the function that transforms the results of BMS run to summary file.

import collections
import pandas as pd
import numpy as np

def summary_BMS_result(filename, summaryfile):
    with open(filename) as infile:
        counts = collections.Counter(l.strip() for l in infile)
    with open(summaryfile, 'w') as f:
        for key, value in counts.items(): 
            f.write('%s, %s\n' % (key, value))

# summary_BMS_result('./Results/2107_Testing_wTC_newcan_Isobutane_1temp/All_Models.txt')
# summary_BMS_result('./Ini_Testing/All_models.txt')
summary_BMS_result('./All_Models175871.txt','Summary.txt')

# Data visualisation
data = pd.read_csv('Summary.txt', delimiter=',')
data = data.rename(columns={' 1':'Frequency of the model'})
print(data)

# Average 