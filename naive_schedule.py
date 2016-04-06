import matplotlib.pyplot as plt
import numpy as np
import csv
import random as rnd
import json

travel_rate = 20000/60
time_start = 0
time_end = 60*24*7 + 120
max_delivery_time = 60*4
#-----------------------------------------------------------------

csv_file = 'advancedSortedFinalProject.csv'
f = open(csv_file, 'r')
reader = csv.reader(f)
next(reader)
data = [[float(i[j]) for j in range(len(i))] for i in reader]

# read information
loc_file = 'Locations.json'
f = open(loc_file, 'r')
loc = json.load(f)
loc_dict = {i[0]: tuple(i[1]) for i in loc}
#------------------------------------------------------------------

schedule = [[] for i in range(4)]
schedule[0] = [(0, data[4][0] + 1), (1, time_end - 24*60)]
schedule[1] = [(2, data[5][0] + 1), (3, time_end - 24 * 60)]
schedule[2] = [(4, data[6][0] + 1), (5, time_end - 24 * 60)]
schedule[3] = [(6, data[7][0] + 1), (7, time_end - 24 * 60)]

#-------------------------------------------------------------------
'''
def compute_dist(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

schedule = [[] for i in range(4)]
ti_all   = [ data[4][0] + 1, data[5][0] + 1, data[6][0] + 1, data[7][0] + 1]
travel_time = [ 100 * 60 for i in [0, 2, 4, 6]]
od_pair  = [(0, 1), (2, 3), (4, 5), (6, 7)]


for i in range(4):
	ti = ti_all[i]
	schedule[i] = [(i, ti)]
	ti += travel_time[i]
	counter = 1
	dest = i + counter 
	while ti < time_end:
		schedule[i] += [ (dest, ti) ] 
		counter *= -1
		dest += counter 
		ti += travel_time[i]

'''
#----------------------------------------------------------------
with open('Schedule.json', 'w', newline='') as fp:
    json.dump(schedule, fp)