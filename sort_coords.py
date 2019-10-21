#!/usr/bin/env python

#This script was writtem to read in material property files exported from FracMan
#and sort them so that they are in the same order as leapFrog block model export files


import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Reads Fracman upscaled elemental values and sorts in LeapFrog style')
parser.add_argument('filename')
args = parser.parse_args()

# Extract file name and extension
filename = args.filename


# Open the FracMan export file with pandas to directly build property tables
data = pd.read_csv(filename)
#data = pd.read_csv(filename, skiprows=10,  float_precision='round_trip')

#this command is needed when combining two block with SS PT data, prepping for a PTM run
#when dat are pulled from paraview, some nodes are duplicated
z = len(data) - len(data.drop_duplicates())

data = data.drop_duplicates()

#Now sort them on z, then y, then x
a = data.sort_values(["Z","Y","X"], ascending = [True, True, True])

print "There were ", z, " duplicate rows in the file"

#and write the file back to a csv
a.to_csv("processed_" + filename, encoding='utf-8', index=False)
