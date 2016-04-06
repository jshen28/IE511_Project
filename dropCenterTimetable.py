import matplotlib.pyplot as plt
import numpy as np
import csv
import random as rnd
import json

#---------------------------------------------------------------------------------------------
# od list
f = open('loc_index.json', 'r')
od_list = json.load(f)

# sorted data
csv_file = 'sortedFinalProject.csv'
f = open(csv_file, 'r')
reader = csv.reader(f)
next(reader)
data = [[float(i[j]) for j in range(len(i))] for i in reader]

#------------------------------------------------------------------------------------------------

od_dict = {}

for i in range(len(od_list)):
	o = od_list[i][0]
	if o in od_dict:
		l = od_dict[o]
		l.append( (od_list[i][1], data[i][0]) )
	else:
		l = [ (od_list[i][1], data[i][0]) ]
	od_dict[o] = l

#------------------------------------------------------------------------------------------------
tt_list = []

for key in range(20):
	if key not in od_dict:
		tt_list.append([])
	else:
		tt_list.append(od_dict[key])

with open('timetableList.json', 'w', newline='') as fp:
    json.dump(tt_list, fp)