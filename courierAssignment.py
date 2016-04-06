import matplotlib.pyplot as plt
import numpy as np
import csv
import random as rnd
import json

'''
	This file is used to assign each courier some drop centers
	Let's start with assigment equal number of locations to courier
'''

# import data from .csv file
csv_file = 'locations.csv'
f = open(csv_file, 'r')
reader = csv.reader(f)
loc = [[float(i[j]) for j in range(len(i))] for i in reader]

#
print(loc)