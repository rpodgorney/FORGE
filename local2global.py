#!/usr/bin/env python

#This script was writtem to read in pointsin global (earth model) along Utah FORGE wells and
#translate and rotate them to local model coordinates

#RKP June 2019: original creation
#RKP July 2020: convert to python3, add some formatting statements, and change the rotation points


import pandas as pd
import numpy as np
import math



#define the point of rotation, and set loal coordinates to start at 0,0

#this is from phase 2
#rot_x = 333325.0
#rot_y = 4262825.0

#for Phase 3_10 cell mesh
rot_x = 332978.088237227
rot_y = 4261736.07638301

#for Phase 3_25 cell mesh
#rot_x = 332650.3170419511
#rot_y = 4262375.377581012

#for Phase 3_40 cell mesh
#rot_x = 332492.8032821122
#rot_y = 4263079.260273337

#for kestrel 3 stim test
#rot_x = 334746.5299
#rot_y = 4263130.831

#define the rotation angle, clockwise is negative
theta = 10

# Open the local file with pandas to begin the processing
data = pd.read_csv('node_mesh_coords.csv')

#first the rotation

#first make  new dataframe
# must deep copy to make a new entry in memory as need old values for conversion
rot_data = data.copy(deep=True)

#change to constant at the end de[ending on the mesh size]
rot_data['X'] = ((data['X'] * math.cos(math.radians(theta))) + (data['Y'] * math.sin(math.radians(theta))))
rot_data['Y'] = (((-data['X'] * math.sin(math.radians(theta))) + (data['Y'] * math.cos(math.radians(theta)))))




#Now trnaslate them to the rotation point of the local system
#add in the rotation point form the x and y data, and replace them in the dataframe
rot_data['X'] += rot_x
rot_data['Y'] += rot_y


#and write the file back to a csv

#set precision to keep things clean
pd.set_option('display.float_format', '{:.4E}'.format)
rot_data['X'] = rot_data['X'].round(2)
rot_data['Y'] = rot_data['Y'].round(2)
rot_data['Z'] = rot_data['Z'].round(2)


l = len(data)
print('Translation and rotation complete, there were', l , 'rows of data')

#and write the file back to a csv
rot_data.to_csv("global_" + str(theta) + '.csv', encoding='utf-8', index=False)
