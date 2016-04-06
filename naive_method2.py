import matplotlib.pyplot as plt
import numpy as np
import csv
import random as rnd
import json
import math

travel_rate = 20000/60
time_start = 0
time_end = 60*24*7 + 120
max_delivery_time = 60*4
#-----------------------------------------------------------------
csv_file = 'advancedSortedFinalProject.csv'
f = open(csv_file, 'r')
reader = csv.reader(f)
data = [[float(i[j]) for j in range(len(i))] for i in reader]

#-------------------------------------------------------------------

time = [obj[0] for obj in data]

day  = {}
for i in range(len(time)):
	t = math.floor(time[i] / 24 / 60) 
	if t in day.keys():
		day[t] += [i] 
	else:
		day[t] = [i]

#-------------------------------------------------------------------

drop_center = [[] for i in range(4)]

drop_center[0] = [ day[0][0], day[1][0], day[2][0] ]
drop_center[1] = [ day[0][1], day[1][1], day[2][1] ]
drop_center[2] = [ day[0][2], day[1][2] ]
drop_center[3] = [ day[0][3], day[1][3] ]

#-------------------------------------------------------------------

loc = []
for i in range(4):
	l = len(loc)
	for (idx,obj) in enumerate(drop_center[i]):
		loc.append([idx * 2 + l, tuple(data[obj][1:3])])
		loc.append([idx * 2 + 1 + l, tuple(data[obj][3:5])])
with open('Locations.json', 'w', newline='') as fp:
    json.dump(loc, fp)	
    
#-------------------------------------------------------------------
def compute_dist(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

def assign_time(data1):
	l = []
	for (idx, obj) in enumerate(data1):
		obj = data1[idx]
		p1 = data[obj][1:3]
		p2 = data[obj][3:5]
		if idx == 0:
			l.append(max(30.5, data[obj][0] + 1))
			l.append( compute_dist(p1, p2) / travel_rate + l[-1] + 60 )
		else:
			l.append(max( 24 * 60 * idx, data[obj][0] + 1 ))
			l.append( compute_dist(p1, p2) / travel_rate + l[-1] + 60 )
	return l

schedule = [[] for i in range(4)]

for i in range(4):
	l = assign_time(drop_center[i])
	print(l)
	if i == 0:
		schedule[i] = [ (idx, obj) for (idx, obj) in enumerate(l) ]
	else:
		t = schedule[i-1][-1][0] + 1
		schedule[i] = [ (idx + t, obj) for (idx, obj) in enumerate(l) ]

with open('Schedule.json', 'w', newline='') as fp:
    json.dump(schedule, fp)