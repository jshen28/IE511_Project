import matplotlib.pyplot as plt
import numpy as np
import csv
import random as rnd
import json
# here is an interesting solution
# import data from .csv file
csv_file = 'advancedSortedFinalProject.csv'
f = open(csv_file, 'r')
reader = csv.reader(f)
next(reader)
data = [[float(i[j]) for j in range(len(i))] for i in reader]


#-------------------------------------------------------------
temp_list = data[4:8]
od_list = []
counter = 0
for obj in temp_list:
	od_list.append([counter, tuple(obj[1:3])])
	counter += 1
	od_list.append([counter, tuple(obj[3:5])])
	counter += 1
while counter < 20:
	od_list.append( [counter, (1e5, 1e5)] )
	counter += 1

with open('Locations.json', 'w', newline='') as fp:
    json.dump(od_list, fp)	