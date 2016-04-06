import matplotlib.pyplot as plt
import numpy as np
import csv
import random as rnd
import json
from sklearn.cluster import KMeans
from math import floor
#-------------------------------------------------------------------------------
# the model is: all the packages are sent from the same drop center to other drop
# scattered in the city. Every mail man should come back to main drop center before
# going to other drop centers.
# this is a simulation of a server model.

# although the idea is quite simple, the result will be non-trivial when properly 
# choosing a good main drop cetner.

#-------------------------------------------------------------------------------
travel_rate = 20000/60
time_start = 0
time_end = 60*24*7 + 120
max_delivery_time = 60*4
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

#--------------------------------------------------------------------------------
# find a good drop center to send packages
rd       = 200
l = []
while len(l) < 1:
	l = []
	instance =  46006 # rnd.randint(0, len(data) - 1)
	p1 = data[instance][1:3]
	p2 = data[instance][3:5]

	for (idx,obj) in enumerate(data):
		if idx == instance:
			continue
		if compute_dist(obj[1:3], p1) < rd:
			l.append(obj)


#-------------------------------------------------------------------------------
# split into differnt days
day = {}
for (idx,obj) in enumerate(l):
	t_day = floor( obj[0] / 60 / 24 )
	if t_day in day.keys():
		day[t_day] += [idx]
	else:
		day[t_day]    = [idx]

'''
#---------------------------------------------------------------------------------
# plot some useful information
fig, ax = plt.subplots(2,2)
for idx in day[0]:
	ax[0, 0].plot([l[idx][0]], [l[idx][1]], 'rx')

for idx in day[1]:
	ax[0, 1].plot([l[idx][0]], [l[idx][1]], 'bx')

for idx in day[2]:
	ax[1, 0].plot([l[idx][0]], [l[idx][1]], 'bx')

for idx in day[3]:
	ax[1, 1].plot([l[idx][0]], [l[idx][1]], 'bx')

plt.show()
'''

#--------------------------------------------------------------------------------
# compute mean of all the axes
mass_center = [0] * 2
for obj in (l + [data[instance]]):
	mass_center = [ obj[1] + mass_center[0], obj[2] + mass_center[1] ]
mass_center = [  i / (len(l) + 1) for i in mass_center ]

#-----------------------------------------------------------------------------------
def random_list(imin, imax, inum):
	if imax - imin  < inum - 1:
		raise ValueError(print("Not enough elements"))

	r_set = set()
	while len(r_set) < inum:
		r_set = r_set | set([rnd.randint(imin, imax)])

	return [i for i in r_set]
#--------------------------------------------------------------------------------
# form data it is easy to find that, each day the destination is properly distributed
# choose drop centers to be first four locations each day
loc = []
#loc.append([0, tuple(data[instance][1:3])]) # it could be imporved by setting it to be the mean of all starting points
loc.append([0, tuple(mass_center)])
count = 1
drop_center = [ [] for i in range(4)]
drop_center_n = [[] for i in range(4) ]
for i in range(5):

	imin = day[i][0]
	imax = day[i][-1]
	r_list = random_list(imin, imax, 4)

	#for now in day[i][0:4]:
	for now in r_list:
		loc.append([count, tuple(l[now][3:5])])
		drop_center[(count - 1) % 4]   += [now]
		drop_center_n[(count - 1) % 4] += [count]
		count += 1
		if count >= 20:
			break

#print(loc)
#print(drop_center)
#print(drop_center_n)


with open('Locations.json', 'w', newline='') as fp:
    json.dump(loc, fp)	



#--------------------------------------------------------------------------------

def compute_dist(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

#---------------------------------------------------------------------------------
def assign_time(data1):
	l_list = []
	for (idx, obj) in enumerate(data1):
		obj = data1[idx]
		p1 = l[obj][1:3]
		p2 = l[obj][3:5]
		if idx == 0:
			l_list.append( max(30.5, l[obj][0] + 1))
			l_list.append( compute_dist(p1, p2) / travel_rate + l_list[-1] + 60 )
		else:
			l_list.append(max( 24 * 60 * idx, l[obj][0] + 1 ))
			l_list.append( compute_dist(p1, p2) / travel_rate + l_list[-1] + 60 )
	return l_list

schedule = [[] for i in range(4)]



for i in range(4):
	ll = assign_time(drop_center[i])
	print(ll)
	count = 0
	for (idx, obj) in enumerate(ll):
		if idx % 2 == 0:
			schedule[i] += [(0, obj)]
		else:
			schedule[i] += [(drop_center_n[i][count], obj)]
			count += 1

print(schedule)


with open('Schedule.json', 'w', newline='') as fp:
    json.dump(schedule, fp)
