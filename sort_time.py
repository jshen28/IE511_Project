import matplotlib.pyplot as plt
import numpy as np
import csv
import random as rnd
import json
'''
#--------------------------------------------------------------------------------------
# import data from .csv file
csv_file = 'finalProject.csv'
f = open(csv_file, 'r')
reader = csv.reader(f)
next(reader)
data = [[float(i[j]) for j in range(len(i))] for i in reader]



#--------------------------------------------------------------------------------------

data.sort(key=lambda x : x[0])

#---------------------------------------------------------------------------------------
with open('sortedFinalProject.csv', 'w', newline='') as fp:
    a = csv.writer(fp)
    a.writerows(data)

'''


#-------------------------------------------------------------------------------------
def compute_dist(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x2 - x1) + abs(y2 - y1)

#data = [ obj for obj in data if compute_dist( obj[1:3], obj[3:5] ) < 5000 ]
data = [ obj for obj in data if compute_dist( obj[1:3], obj[3:5] )  > 30000 and compute_dist( obj[1:3], obj[3:5] )  < 35000 ]


#----------------------------------------------------------------------------------------

for obj in data:
	plt.plot( [obj[1], obj[3]], [obj[2], obj[4]] )
plt.show()

'''
#---------------------------------------------------------------------------------------
with open('advancedSortedFinalProject.csv', 'w', newline='') as fp:
    a = csv.writer(fp)
    a.writerows(data)
'''