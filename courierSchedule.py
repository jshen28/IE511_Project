import matplotlib.pyplot as plt
import numpy as np
import csv
import random as rnd
import json

'''
	This file is used to make a full shedule for four couriers.
	The shedule should be based on how the drop centers are assigned to each courier.
	In this file I suppose to use a quite naive way to conquer the problem.
'''
time_end = 60*24*7 + 120
max_delivery_time = 60*4
travel_rate = 20000/60
#---------------------------------------------------------------------------------------------------------
# read information
loc_file = 'Locations.json'
f = open(loc_file, 'r')
loc = json.load(f)
loc_dict = {i[0]: tuple(i[1]) for i in loc}

# timable for each location
f = open('timetableList.json', 'r')
tt_list = json.load(f)

#----------------------------------------------------------------------------------------------------------
def compute_dist(p1, p2):

	x1, y1 = p1
	x2, y2 = p2
	return abs(x2 - x1) + abs(y2 - y1)

def isvalid(current_pos, obj, current_time):
	if (obj[1] > current_time + 30 
		and compute_dist(loc_dict[current_pos], loc_dict[obj[0]]) / travel_rate < max_delivery_time 
		and obj[1] + compute_dist(loc_dict[current_pos], loc_dict[obj[0]]) / travel_rate < time_end): 
		return True
	elif (obj[1] <= current_time + 30
		    and 30 + (current_time-obj[1]) + compute_dist(loc_dict[current_pos], loc_dict[obj[0]]) / travel_rate < max_delivery_time 
		    and 30 + compute_dist(loc_dict[current_pos], loc_dict[obj[0]]) / travel_rate < time_end):
		return True

	return False

# process
schedule = [[] * 4]
current_time = 0                                                                                            # in minutes current_time is sames arrival time
tt_length_list = [ len(obj) for obj in tt_list ]
val, current_pos = max( (val, idx) for (idx, val) in enumerate(tt_length_list) )

while current_time <= time_end:
	timetable = tt_list[current_pos]
	feasible_list = [ obj for obj in timetable if isvalid(current_pos, obj, current_time)]
	if len(feasible_list) == 0:
		break

	next_pos = feasible_list[0][0]
	depart_time = max( [current_time + 30, feasible_list[0][1]] )
	schedule[0].append( (current_pos, depart_time) )
	current_time = depart_time + compute_dist(loc_dict[current_pos], loc_dict[next_pos])
	current_pos = next_pos

print(schedule[0])

'''	
#-----------------------------------------------------------------------------------------------------------
# result
schedule = [ [(1, 30.5), (3, 4*60), (10, 8*60)], [(1, 30.5), (3, 4*60), (10, 8*60)], [(1, 30.5), (3, 4*60), (10, 8*60)], [(1, 30.5), (3, 4*60), (10, 8*60)] ]

# prdouce a schedule.json file
with open('Schedule.json', 'w', newline='') as fp:
    json.dump(schedule, fp)
'''