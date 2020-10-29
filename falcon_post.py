#!/usr/bin/env python

import os
import pandas as pd
import argparse
import math
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Reads MOOSE VectorPostProcesser data combines parameters into separate files')
parser.add_argument('parameter')
args = parser.parse_args()

# Extract parameter you are interested in
parameter = args.parameter

#open an empty dataframe to hold parameter
df_master = pd.DataFrame()

# This is to get the directory that the program
# is currently running in.
dir_path = os.path.dirname(os.path.realpath(__file__))



#this will do a recursive search, so will look into all subdirectories
for root, dirs, files in os.walk(dir_path):
    for file in files:
        if file.endswith('sample_0001.csv'):
            print (root+'/'+str(file))
            data = pd.read_csv(root+'/'+str(file))
            a = str(file)[0:14]
            b = a.split("_")
            c ='_'.join(b[:3])
            df_master['z'] = (data['z'])
            df_master[c] = (data[parameter])
            plt.plot( c, 'z', data=df_master, linewidth=1, label=str(c))

df_master.to_csv("all_NS_58-32_" + parameter + ".csv", encoding='utf-8', index=False)

plt.xlabel(str(parameter))
plt.ylabel('Elevation (m AMSL)')
plt.legend()
plt.savefig("all_NS_58-32_" + parameter + ".pdf")
plt.show()
