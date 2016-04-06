import matplotlib.pyplot as plt
import numpy as np
import csv
import random as rnd
import json
from sklearn.cluster import KMeans
from math import floor

#-------------------------------------------------------------------------------

# import data from .csv file
csv_file = 'sortedFinalProject.csv'
f = open(csv_file, 'r')
reader = csv.reader(f)
data = [[float(i[j]) for j in range(len(i))] for i in reader]

#--------------------------------------------------------------------------------
def compute_dist(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x2 - x1) + abs(y2 - y1)
'''
#--------------------------------------------------------------------------------
# find travel which has location in some areas.
rd       = 1000
point = []
l = []
while len(l) < 200:
	l = []
	instance =  rnd.randint(0, len(data) - 1)
	p1 = data[instance][1:3]
	p2 = data[instance][3:5]

	for obj in data:
		if compute_dist(obj[1:3], p1) < rd:
			l.append(obj)

print(instance)
print(len(l))
'''
#---------------------------------------------------------------------------------

sched_file = 'feasible_values.json'
f = open(sched_file, 'r')
positions = json.load(f)

loc_file = 'Locations.json'
f = open(loc_file, 'r')
loc = json.load(f)

rd = 1000

l_rd = [] # all the points 

for obj in data:
	if compute_dist( obj[1:3], obj[3:5] ) < rd:
		l_rd.append(obj)

print(len(l_rd))

for obj in positions:
	plt.plot([obj[0], obj[2]], [obj[1], obj[3]], 'r-')

for (idx, obj) in loc:
	plt.plot( [obj[0]], [obj[0]], 'bx' )

plt.show()


'''
#-------------------------------------------------------------------------------
day = {}
for (idx,obj) in enumerate(l):
	t_day = floor( obj[0] / 60 / 24 )
	if t_day in day.keys():
		day[t_day] += [idx]
	else:
		day[t_day]    = [idx]

print(day)
'''
#--------------------------------------------------------------------------------
# form data it is easy to find that, each day the destination is properly distributed
# by this, we can further improve the performance by smartly choosing dropcenters.
# choose drop centers to be first four locations each day

# the method is implemented in naive_method3.py

'''
#--------------------------------------------------------------------------------

t = KMeans(max_iter=200, n_clusters = 15).fit([ obj[3:5] for obj in l ]).cluster_centers_

print(t)

#--------------------------------------------------------------------------------
r_dict = {}
for obj in l:
	dist_list = [ compute_dist(obj[3:5], i) for i in t ]
	val, idx  = min( (val, idx) for (idx, val) in enumerate(dist_list) )
	if idx in r_dict.keys():
		r_dict[idx] += [obj]
	else:
		r_dict[idx]  = [obj]


del_key = []
for key in r_dict.keys():
	if len(r_dict[key]) < 2:
		del_key += [key]

for i in del_key:
	r_dict.pop(i)


#---------------------------------------------------------------------------------
t = [ t[key] for key in r_dict.keys() ]

count = 0
for obj in l:
	dist_list = [ compute_dist(obj[3:5], i) for i in t ]
	val, idx  = min( (val, idx) for (idx, val) in enumerate(dist_list) )
	if val < 1000:
		count += 1

print(count)
'''
'''
#--------------------------------------------------------------------------------
print(instance)
print(len(l))


#--------------------------------------------------------------------------------
fig, ax = plt.subplots()
for i in data[0:1000]:
	ax.plot( [i[1], i[3]], [i[2], i[4]] , 'o')
'''
'''
for i in t:
	ax.plot(i[0], i[1], 'rx')
'''
'''
ax.grid(True)
plt.show()
'''
