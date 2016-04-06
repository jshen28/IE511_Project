import matplotlib.pyplot as plt
import csv
from sklearn.cluster import KMeans
import time

start_time = time.time()

travel_rate = 20000/60
time_start = 0
time_end = 60*24*7
max_delivery_time = 60*4

# import data from .csv file
csv_file = 'finalProject.csv'
f = open(csv_file, 'r')
reader = csv.reader(f)
next(reader)
data = [[float(i[j]) for j in range(len(i))] for i in reader]

'''
# compute a position by weight

x_sum = 0 
y_sum = 0

for obj in data:
	x_sum += (obj[1] + obj[3])
	y_sum += (obj[2] + obj[4])
x_avg = x_sum / len(data)
y_avg = y_sum / len(data)
p_avg = data[200][1:3]

# print value
print(x_avg, y_avg)
'''
# compute the value
def dist(p1, p2):
	return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def val(d1, d2):
	return 1.2 ** (-1 * (1 + 0.001*(d1 + 0.5 * d2)))
#
'''
t_time = []
for obj in  data:
	t_time.append(dist(obj[1:3], obj[3:5]) / travel_rate)


print(sum(t_time) / len(t_time))

plt.hist(t_time)
plt.show()
'''
'''
v = 0
for obj in data:
	print(obj[1:3])
	v += val( dist(p_avg, obj[1:3]), dist(p_avg, obj[3:5]) )
print(v)

'''
'''
# sort
t = sorted(data, key=lambda item : item[0])
with open('ProjectSorted.csv', 'w', newline='') as fp:
    a = csv.writer(fp)
    a.writerows(t)

for obj in data:
	plt.plot(obj[1], obj[2], 'ro')
plt.show()


#
'''


#
x = [i for i in range(2000)]
y = [1.2 ** ( -1 * (1 + 0.01 * i)) for i in x]
plt.plot(x, y)
plt.show()