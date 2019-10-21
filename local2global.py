#!/usr/bin/env python

#This script was writtem to read in points in local model coordinates and rotate them to global (earth model) coordinates
#using the specified rottion point of (rot_x, rot_y)

#RKP July 2019


import pandas as pd
import argparse
import numpy as np
import math

parser = argparse.ArgumentParser(description='Reads FORGE location data and converts from local to global coordinate system')
parser.add_argument('filename')
args = parser.parse_args()

# Extract file name and extension
filename = args.filename

#define the point of rotation
rot_x = 333325.0
rot_y = 4262825.0

#define the rotation angle, clockwise is negative
theta = 25.0

# Open the local well point file with pandas to begin the processing
#data = pd.read_csv(filename,  skiprows=10)
data = pd.read_csv(filename, skiprows =10, float_precision='round_trip')


#first the rotation
#first make  new dataframe
# must deep copy to make a new entry in memory as need old values wo for conversion
rot_data = data.copy(deep=True)

rot_data['X'] = ((data['X'] * math.cos(math.radians(theta))) + (data['Y'] * math.sin(math.radians(theta))) -25.0)
rot_data['Y'] = (((-data['X'] * math.sin(math.radians(theta))) + (data['Y'] * math.cos(math.radians(theta)))) - 25)

#round to 2 decimal places to keep things clean

#df.value1 = df.value1.round()
rot_data.X = rot_data.X.round(2)
rot_data.Y = rot_data.Y.round(2)
rot_data.Z = rot_data.Z.round(2)

#Now trnaslate them to the rotation point of the local system
#add in the rotation point to the x and y data, and replace them in the dataframe
rot_data['X'] += rot_x
rot_data['Y'] += rot_y


l = len(data)
print 'Translation and rotation complete, there were', l , 'rows of data'

#and write the file back to a csv
rot_data.to_csv("global_" + filename, index=False)
