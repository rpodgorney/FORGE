#!/usr/bin/env python3
import sys
import pandas as pd
import numpy as np
import math

#first set mesh intertval size
dx=80
dy=80
dz=80

#then set the range in x, y, and z, assume start at origin for x and y
x_min = 0
y_min = 0
z_min = -2296

x_max = 4080
y_max = 4080
z_max = 1583

#make empty lists for coordinates
x_coord=[]
y_coord=[]
z_coord=[]

#loop throughto get coordinates
for x in range(x_min,x_max,dx):
  for y in range(y_min,y_max,dy):
    for z in range(z_min,z_max,dz):
        #print(i,x,y,z, sep=", ")
        x_coord.append(x)
        y_coord.append(y)
        z_coord.append(z)

#convert lists to dataframe and save as CSV
df=pd.DataFrame (x_coord, columns=['X'])
df['Y']=y_coord
df['Z']=z_coord

df.to_csv("node_mesh_coords.csv", encoding='utf-8', index=False)
