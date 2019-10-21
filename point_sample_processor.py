#!/usr/bin/env python

#This script was writtem to read indata from a MOOSE pointsample postprocessor
#and manipilate the data for presentation
#RKP June 2019


import pandas as pd
import argparse
import numpy as np
import math

parser = argparse.ArgumentParser(description='Reads FORGE Well data as points along the well and converts from global to local coordinate system')
parser.add_argument('filename')
args = parser.parse_args()

# Extract file name and extension
filename = args.filename

#define the biot coef
alpha = 0.6


# Open the file with pandas to begin the processing
#data = pd.read_csv(filename,  skiprows=10)
data = pd.read_csv(filename, float_precision='round_trip')


#first make  new dataframe
# must deep copy to make a new entry in memory as need old values wo for conversion
proc_data = data.copy(deep=True)

#convert MOOSE effective stress to total stress, and convert to MPa
proc_data['injection_point_pressure'] = data['injection_point_pressure'] / 1e6 # get MPa
proc_data['injection_point_stress_ii'] = ((data['injection_point_stress_ii'] * -1) + (data['injection_point_pressure']
* alpha))/1e6
proc_data['injection_point_stress_jj'] = ((data['injection_point_stress_jj'] * -1) + (data['injection_point_pressure']
* alpha))/1e6
proc_data['injection_point_stress_kk'] = ((data['injection_point_stress_kk'] * -1) + (data['injection_point_pressure']
* alpha))/1e6


l = len(data)
print 'Processing complete, there were', l , 'rows of data'

#and write the file back to a csv
proc_data.to_csv("processed_" + filename, index=False)
