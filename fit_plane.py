#!/usr/bin/env python

#This script was writtem to read in 3D point data from FORGE MEQ locations and
#determine a best-fit plane and then the stricke and dip of that plane

#must provide data as an CSV file as X,Y,Z.  A header row with "X", "Y", and "Z" is required

#RKP May 2019, many parts borrowed form internet searches, and pieced together here


import pandas as pd
import argparse
import numpy as np
import scipy.linalg
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import math


parser = argparse.ArgumentParser(description='Reads 3D point data to determine best fit plane and strike/dip')
parser.add_argument('filename')
args = parser.parse_args()

# Extract file name and extension
filename = args.filename


# Open the point data file with pandas
point_data = pd.read_csv(filename)

xdata_list = np.asarray(point_data['X'].tolist())
ydata_list = np.asarray(point_data['Y'].tolist())
zdata_list = np.asarray(point_data['Z'].tolist())

xmin = min(xdata_list)
xmax = max(xdata_list)
ymin = min(ydata_list)
ymax = max(ydata_list)
zmin = min(zdata_list)
zmax = max(zdata_list)


data = np.c_[xdata_list, ydata_list, zdata_list]

# regular grid covering the domain of the data
X,Y = np.meshgrid(np.arange(xmin, xmax, 50), np.arange(ymin, ymax, 50))
XX = X.flatten()
YY = Y.flatten()

order = 1    # 1: linear, 2: quadratic
if order == 1:
    # best-fit linear plane
    A = np.c_[data[:,0], data[:,1], np.ones(data.shape[0])]
    C,_,_,_ = scipy.linalg.lstsq(A, data[:,2])    # coefficients

    # evaluate it on grid
    Z = C[0]*X + C[1]*Y + C[2]

    # or expressed using matrix/vector product
    #Z = np.dot(np.c_[XX, YY, np.ones(XX.shape)], C).reshape(X.shape)

elif order == 2:
    # best-fit quadratic curve
    A = np.c_[np.ones(data.shape[0]), data[:,:2], np.prod(data[:,:2], axis=1), data[:,:2]**2]
    C,_,_,_ = scipy.linalg.lstsq(A, data[:,2])

    # evaluate it on a grid
    Z = np.dot(np.c_[np.ones(XX.shape), XX, YY, XX*YY, XX**2, YY**2], C).reshape(X.shape)


i=len(X)
j=len(Y)

ptA = (X[0,0], Y[0,0], Z[0,0])
ptB = (X[0,i], Y[0,i], Z[0,i])
ptC = (X[i-1,0], Y[i-1,0], Z[i-1,0])


#calc strike and dip

x1, y1, z1 = float(ptA[0]), float(ptA[1]), float(ptA[2])
x2, y2, z2 = float(ptB[0]), float(ptB[1]), float(ptB[2])
x3, y3, z3 = float(ptC[0]), float(ptC[1]), float(ptC[2])


u1 = float(((y1 - y2) * (z3 - z2) - (y3 - y2) * (z1 - z2)))
u2 = float((-((x1 - x2) * (z3 - z2) - (x3 - x2) * (z1 - z2))))
u3 = float(((x1 - x2) * (y3 - y2) - (x3 - x2) * (y1 - y2)))

#    '''
#    Calculate pseudo eastings and northings from origin
#    these are actually coordinates of a new point that represents
#    the normal from the plane's origin defined as (0,0,0).

#    If the z value (u3) is above the plane we first reverse the easting
#    then we check if the z value (u3) is below the plane, if so
#    we reverse the northing.
#
#    This is to satisfy the right hand rule in geology where dip is always
#    to the right if looking down strike.
#    '''
if u3 < 0:
    easting = u2
else:
    easting = -u2

if u3 > 0:
    northing = u1
else:
    northing = -u1

if easting >= 0:
    partA_strike = math.pow(easting, 2) + math.pow(northing, 2)
    strike = math.degrees(math.acos(northing / math.sqrt(partA_strike)))
else:
    partA_strike = northing / math.sqrt(math.pow(easting, 2) + math.pow(northing, 2))
    strike = math.degrees(2 * math.pi - math.acos(partA_strike))

    # determine dip
print "strike: ",  strike
part1_dip = math.sqrt(math.pow(u2, 2) + math.pow(u1, 2))
part2_dip = math.sqrt(math.pow(u1,2) + math.pow(u2,2) + math.pow(u3,2))
dip = math.degrees(math.asin(part1_dip / part2_dip))
print 'dip: ', dip


# plot points and fitted surface
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, alpha=0.2)
ax.scatter(data[:,0], data[:,1], data[:,2], c='r', s=50)
plt.xlabel('X')
plt.ylabel('Y')
ax.set_zlabel('Z')
ax.axis('equal')
ax.axis('tight')
plt.show()
