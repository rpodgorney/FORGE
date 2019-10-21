#!/usr/bin/env python

#This script was writtem to read in pointsin global (earth model) along Utah FORGE wells and
#translate and rotate them to local model coordinates

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

#define the point of rotation
rot_x = 333325.0
rot_y = 4262825.0

#define the rotation angle, clockwise is negative
theta = -25.0

# Open the glocal well point file with pandas to begin the processing
#data = pd.read_csv(filename,  skiprows=10)
#data = pd.read_csv(filename, skiprows =10, float_precision='round_trip')
data = pd.read_csv(filename, float_precision='round_trip')

#Now trnaslate them to the rotation point of the local system
#subtract out the rotation point form the x and y data, and replace them in the dataframe
data['X'] -= rot_x
data['Y'] -= rot_y


#now the rotation
#first make  new dataframe
# must deep copy to make a new entry in memory as need old values wo for conversion
rot_data = data.copy(deep=True)

#use absolute values to keep all signs positive, mesh in always in the first quadrant
rot_data['X'] = ((data['X'] * math.cos(math.radians(theta))) + (data['Y'] * math.sin(math.radians(theta))) -25.0).abs()
rot_data['Y'] = (((-data['X'] * math.sin(math.radians(theta))) + (data['Y'] * math.cos(math.radians(theta)))) - 25).abs()

#round to 2 decimal places to keep things clean

#df.value1 = df.value1.round()
rot_data.X = rot_data.X.round(2)
rot_data.Y = rot_data.Y.round(2)
rot_data.Z = rot_data.Z.round(2)



l = len(data)
#print 'Translation and rotation complete, there were', l , 'rows of data'

#and write the file back to a csv
rot_data.to_csv("local_" + filename, index=False)
