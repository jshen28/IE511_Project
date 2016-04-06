import matplotlib.pyplot as plt
import numpy as np
import csv
import random as rnd
import json

'''
	This file is used to create position of 20 drop centers.
	There should be strategies to find the best position of drop centers
	But it will be better to start with something simple.
'''

# import data from .csv file
csv_file = 'sortedFinalProject.csv'
f = open(csv_file, 'r')
reader = csv.reader(f)
next(reader)
data = [[float(i[j]) for j in range(len(i))] for i in reader]

# Randomly pick 20 places as drop centers 

index_set = set()
while len(index_set) != 20:
	r = rnd.randint(0, 1e5 - 1)
	index_set = index_set | set([r])

# factory locations
loc = []
for i in range(20):
	loc.append( [ i, (data[i][1], data[i][2]) ] )
'''
print(loc)
'''
# print to .csv file

with open('Locations.json', 'w', newline='') as fp:
    json.dump(loc, fp)

#------------------------------------------------------------------------------------------------
'''
# print out the locations
for obj in loc:
	plt.plot(obj[1][0], obj[1][1], 'rx')
plt.show()
'''
#-------------------------------------------------------------------------------------------------

# assign OD pair to some drop centers
def compute_dist(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x2 - x1) + abs(y2 - y1)

od_list = []

loc_dict = {i[0]: tuple(i[1]) for i in loc}

for obj in data:
	start_point = obj[1:3]
	dest_point  = obj[3:5]
	# compute distance, here suppose that center locations are different
	o_dist_list = [ compute_dist(start_point, obj[1]) for obj in loc ]
	val, start_loc = min( (val, idx) for (idx, val) in enumerate(o_dist_list) )

	d_dist_list = [ compute_dist(dest_point, obj[1]) for obj in loc ]
	val, dest_loc = min( (val, idx) for (idx, val) in enumerate(d_dist_list) )
	# add to od_list
	od_list.append( (start_loc, dest_loc) )

with open('loc_index.json', 'w', newline='') as fp:
    json.dump(od_list, fp)

#-----------------------------------------------------------------
