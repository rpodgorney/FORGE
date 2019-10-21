#!/usr/bin/env python

#This script was written to read in Leapfrog block model property file
#and assign values to cells for FORGE modeling and simulation

#Manual step before this is to past in directional permeability and porosity from FracMan
#and also add in any missing columns needed for the material property read

#Can only have one block, so for any spatially varying property it needs to have props defined here


import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Adds and fixes values in nodeal FALCON csv Exodus II prep files')
parser.add_argument('filename')
args = parser.parse_args()

# Extract file name and extension
filename = args.filename

# Open the FracMan export file with pandas to directly build property tables
#data = pd.read_csv(filename, skiprows=10)
data = pd.read_csv(filename)
#Now sort them on z, then y, then x
data.loc[data.GM == 'Valley Fill', ['Kii', 'Kjj', 'Kkk', 'porosity']] = 6.2e-11, 6.2e-11, 6.2e-11, 0.25
#data.loc[data.GM == 'Valley Fill', ["porosity", "density", 'specific_heat']] = 0.25, 2400.0, 830.0
#data.loc[data.GM == 'Granitiod', ["density", 'specific_heat']] = 2640.0, 790.0
#data.loc[data.GM == 'Valley Fill', ["thermal_conductivity_i", "thermal_conductivity_j", "thermal_conductivity_k"]] = 2.0, 2.0, 2.0
#data.loc[data.GM == 'Granitiod', ["thermal_conductivity_i", "thermal_conductivity_j", "thermal_conductivity_k"]] = 3.1, 3.1, 3.1


#data.loc[data.GM == 'Valley Fill', "block" = 0
#data.loc[data.GM == 'Granitiod', "block' = 1

print data

#and write the file back to a csv
data.to_csv("processed_" + filename, encoding='utf-8', index=False)
