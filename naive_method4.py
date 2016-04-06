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
rd       = 300
l = []
while len(l) < 1:
	l = []
	instance =   12402 # rnd.randint(0, len(data) - 1) #46006  #98952 # 12402 # 48388 # 32115 # 1197
	p1 = data[instance][1:3]
	p2 = data[instance][3:5]

	for (idx,obj) in enumerate(data):
		if idx == instance:
			continue
		if compute_dist(obj[1:3], p1) < rd:
			l.append(obj)

print(instance)

#-------------------------------------------------------------------------------
# split into differnt days
day = {}
for (idx,obj) in enumerate(l):
	t_day = floor( obj[0] / 60 / 24 )
	if t_day in day.keys():
		day[t_day] += [idx]
	else:
		day[t_day]  = [idx]

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

#-------------------------------------------------------------------------------
rd = 1000
f_data = []
for obj in data:
	if compute_dist(obj[1:3], loc[0][1]) < rd:
		temp = [ compute_dist(obj[3:5], o) for (idx, o) in loc if idx > 0  ]
		val, idx = min( (val, idx) for (idx, val) in enumerate(temp) )
		if val < rd * 2:
			f_data.append([obj[0], idx + 1])


courier_dest = {}
for (tim, idx) in f_data:
	for (i, v) in enumerate(drop_center_n):
		if idx in v:
			if i in courier_dest.keys():
				courier_dest[i] += [[tim, idx]]
			else:
				courier_dest[i]  = [[tim, idx]]

#--------------------------------------------------------------------------------
# 
'''
def is_valid(c_time, travel_time, v_list, pos):
	if v_list:

	else:
'''

def schedule_time(courier_ttable):
	sched = []
	flag  = 0
	# timetable for one specific destination
	dest_dict = {}
	for (tim, dest_idx) in courier_ttable:
		if dest_idx in dest_dict.keys():
			dest_dict[dest_idx] += [tim]
		else:
			dest_dict[dest_idx]  = [tim]

	while True:
		# specify time
		t_depart, t_arrival, max_num, next_dest, min_leav = -1, -1, -1, -1, 1e6

		if sched:
			last_dest = sched[-1][0]
			c_time = sched[-1][1] + compute_dist( loc[0][1], loc[last_dest][1] ) / travel_rate + 31  # minimum leaving time
		else:
			c_time = 31

		for dest_idx in dest_dict.keys():
			t_list = dest_dict[dest_idx]      # time_table
			v_list = [  tt for tt in t_list if tt + max_delivery_time > c_time + compute_dist(loc[0][1], loc[dest_idx][1]) / travel_rate]

			if v_list:
				v_time = v_list[0]
				tt_min  = max([c_time, v_time])
				tt_max = v_time + max_delivery_time - compute_dist(loc[0][1], loc[dest_idx][1]) / travel_rate

				num   = len([  tt for tt in t_list if tt >= tt_min and tt <= tt_max])

				if tt_max < min_leav:  # choose the one with the minium leaving time
					t_depart = tt_max
					t_arrival = t_depart + compute_dist(loc[0][1], loc[dest_idx][1]) / travel_rate
					min_leav = tt_max
					next_dest = dest_idx
					
		if next_dest == -1:
			break
		if t_depart < time_end:
			sched.append( (0, t_depart) )
			if t_arrival + 31 < time_end:
				sched.append( (next_dest, t_arrival + 31) )
			else:
				break
		else:
			break
		

	return sched

#---------------------------------------------------------------------------------
schedule = []
for i in courier_dest.keys():
	schedule.append(schedule_time(courier_dest[i]))

print(sum( [ len(i) for i in schedule ] ))
#-------------------------------------------------------------------------------

with open('Schedule.json', 'w', newline='') as fp:
    json.dump(schedule, fp)

