#!/usr/bin/env python

# This script takes inputs for well data with a build-up angle
# and outputs well coordinates per measured length of the well.

import numpy as np
import math as m
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Reads well data as points along the well and outputs UTM coordinates with elevation')
parser.add_argument('filename')
args = parser.parse_args()

# Extract file name and extension
filename = args.filename

# Open the glocal well point file with pandas to begin the processing
data = pd.read_csv(filename, usecols=[1])
data = data.iloc[1:15]
data = data.drop([7])
data = np.asarray(data, dtype='float64')

# Assigns values from CSV file for calculations
ls_x = data[0]                       #Location Easting
ls_y = data[1]                       #Location Northing
ls_elev = data[2]                       #Location Elevation
azi = data[3]                      #Well Azimuth
dipin = data[4]                    #Dip at Location
kick = data[5]                     #Kick-off Depth

build_x = data[6]                    #Build-up End Point Easting
build_y = data[7]                    #Build-up End Point Northing
build_elev = data[8]                    #Build-up End Point Elevation
beta  = m.radians(data[9])     #Dip at Target (Convert to Rad)
tot    = data[10]                  #Total Measured Depth
ver    = data[11]                  #Vertical Depth
hor    = data[12]                  #Horizontal Depth

toe_elev = ls_elev - ver

print('land surface x: ', ls_x)
print('land surface y: ', ls_y)
print('land surface z: ', ls_elev)
print('well azimuth: ', azi)
print('well dip: ', data[9])
print('end build x: ', build_x)
print('end build y: ', build_y)
print('end build z: ', build_elev)
print('dip radians: ', beta)



# Compares Azimuth degree for correct calculation of offset
if azi <= 90:
    Q = 1

elif azi <= 180 and azi >= 90:
    Q = 2
    theta=m.radians(azi-90.0)

elif azi >=180 and azi <=270:
    Q = 3

elif azi >=270 and azi <=360:
    Q = 4
    theta=m.radians(azi-270)

print('azimuth radians: ', theta)

a=[]

dx = float(5)
dy = dx *  m.tan(theta)

x = build_x[0]
y = build_y[0]
z = build_elev[0]

a.append([x, y, z])


# Uses trigonometry at the target angle to solve for offset and elevation values

    #if Q == 1:
    #    x[k] = x[int(kick+(It*r1))] + math.sin(math.radians(azi))*math.cos(dipend)*(k - (kick+(It*r1)))
     #   y[k] = y[int(kick+(It*r1))] + math.cos(math.radians(azi))*math.cos(dipend)*(k - (kick+(It*r1)))
if Q == 2:
    while z > toe_elev:
        x_old = x
        y_old = y
        x = x + dx
        y = y - dy

        #calc distance between two points
        x_dist = x - x_old
        y_dist = y - y_old
        dist = m.sqrt((x_dist**2)+(y_dist**2))
        dz = dist * m.tan(beta)
        z = z - dz
        a.append([x, y, z])

    #if Q == 3:
      #  x[k] = x[int(kick+(It*r1))] - math.sin(math.radians(azi-180))*math.cos(dipend)*(k - (kick+(It*r1)))
       # y[k] = y[int(kick+(It*r1))] - math.cos(math.radians(azi-180))*math.cos(dipend)*(k - (kick+(It*r1)))

if Q == 4:
    while z > toe_elev:
        x_old = x
        y_old = y
        x = x - dx
        y = y + dy

        #calc distance between two points
        x_dist = x - x_old
        y_dist = y - y_old
        dist = m.sqrt((x_dist**2)+(y_dist**2))
        dz = dist * m.tan(beta)
        z = z - dz
        a.append([x, y, z])

print('qaud: ',Q)


b = np.array(a)

# Writes file to CSV
df = pd.DataFrame({'x': b[:, 0], 'y': b[:, 1], 'z':b[:,2]})
df.to_csv("Coordinates_" + filename, encoding='utf-8', index=False)
