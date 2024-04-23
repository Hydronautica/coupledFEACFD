#!/usr/bin/python

import os
import sys
import math

forces_file = "postProcessing/forces1/0/force.dat"

if not os.path.isfile(forces_file):
	print("Forces file not found at "+forces_file)
	print("Be sure that the case has been run and you have the right directory!")
	print("Exiting.")
	sys.exit()

def line2dict(line):
	tokens_unprocessed = line.split()
	tokens = [x.replace(")","").replace("(","") for x in tokens_unprocessed]
	floats = [float(x) for x in tokens]
	data_dict = {}
	data_dict['time'] = floats[0]
	force_dict = {}
	force_dict['pressure'] = floats[1:4]
	force_dict['viscous'] = floats[4:7]
	force_dict['porous'] = floats[7:10]
	data_dict['force'] = force_dict
	return data_dict

time = []
FxT = []
FyT = []
FzT = [] 

with open(forces_file,"r") as datafile:
	for line in datafile:
		if line[0] == "#":
			continue
		data_dict = line2dict(line)
		time += [data_dict['time']]
		FxT += [data_dict['force']['pressure'][0] + data_dict['force']['viscous'][0]]
		FyT += [data_dict['force']['pressure'][1] + data_dict['force']['viscous'][1]]
		FzT += [data_dict['force']['pressure'][2] + data_dict['force']['viscous'][2]]
datafile.close()

outputfile = open('forces.txt','w')
for i in range(0,len(time)):
	outputfile.write(str(time[i])+' '+str(FxT[i])+' '+str(FyT[i])+ ' '+str(FzT[i])+'\n')
outputfile.close()

