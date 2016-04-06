import json
import csv

travel_rate = 20000/60
time_start = 0
time_end = 60*24*7 + 120
max_delivery_time = 60*4

loc_str = 'location'
arv_str = 'arrival'
dep_str = 'departure'

csv_file = 'FinalProject.csv'
f = open(csv_file, 'r')
reader = csv.reader(f)
next(reader)
data = [[float(i[j]) for j in range(len(i))] for i in reader]

loc_file = 'Locations.json'
f = open(loc_file, 'r')
loc = json.load(f)
if len(loc) != 20:
    raise ValueError('{} does not contain enough entries'.format(loc_file))
loc_dict = {i[0]: tuple(i[1]) for i in loc}

sched_file = 'Schedule.json'
f = open(sched_file, 'r')
sched = json.load(f)
if len(sched) != 4:
    raise ValueError('{} does not contain enough entries'.format(sched_file))


def makeFullSchedule(sched):

    def make_dict_entry(i, j):
        location = sched[i][j][0]
        departure = sched[i][j][1]
        if departure > time_end:
            raise ValueError('departure time of {} is outside time window'.format(departure))
        if j == 0:
            arrival = 0
        else:
            prev_loc = sched[i][j-1][0]
            prev_time = sched[i][j-1][1]
            x1, y1 = loc_dict[prev_loc]
            x2, y2 = loc_dict[location]
            distance = abs(x2 - x1) + abs(y2 - y1)
            travel_time = distance/travel_rate
            arrival = prev_time + travel_time

        if arrival + 30 > departure:
            print(prev_loc, prev_time, j, sched[i][j-1])
            error_string = 'courier {} needs 30 min window at {}: departs at {} arrives at {}'
            raise ValueError(error_string.format(i, location, departure, arrival))

        return {loc_str: location, arv_str: arrival, dep_str: departure}

    sched_dict = [{make_dict_entry(i, j)[arv_str]: make_dict_entry(i, j)
                   for j in range(len(sched[i]))}
                  for i in range(len(sched))]

    return sched_dict

sched_dict = makeFullSchedule(sched)


def computeCustomerObj(customer_info):
    time = customer_info[0]
    start_point = (customer_info[1], customer_info[2])
    dest_point = (customer_info[3], customer_info[4])
    couriers = [i for i in range(len(sched_dict))]

    def compute_dist(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return abs(x2 - x1) + abs(y2 - y1)

    start_dist_dict = {compute_dist(start_point, loc_dict[i]): i for i in loc_dict.keys()}
    start_loc = start_dist_dict[min(start_dist_dict.keys())]

    dest_dist_dict = {compute_dist(dest_point, loc_dict[i]): i for i in loc_dict.keys()}
    dest_loc = dest_dist_dict[min(dest_dist_dict.keys())]

    def courier_delivery_time(courier):
        courier_sched = sched_dict[courier]
        arrival_times = [courier_sched[i][arv_str] for i in courier_sched
                         if (courier_sched[i][arv_str] < time + max_delivery_time)
                         and (courier_sched[i][dep_str] > time)
                         and (courier_sched[i][loc_str] == start_loc)]
        if arrival_times:
            min_arrival_time = min(arrival_times)
        else:
            return False

        destination_times = [courier_sched[i][arv_str] for i in courier_sched
                             if (courier_sched[i][arv_str] < time + max_delivery_time)
                             and (courier_sched[i][dep_str] > min_arrival_time)
                             and (courier_sched[i][loc_str] == dest_loc)]
        if destination_times:
            return min(destination_times)
        else:
            return False

    min_deliverable_time = max([courier_delivery_time(i) for i in couriers])

    if min_deliverable_time:
        dist = (1/100)*(compute_dist(start_point, loc_dict[start_loc]) +
                         (1/2)*compute_dist(dest_point, loc_dict[dest_loc]))
        probability = 1.2**-(1+dist)
    else:
        probability = 0
    return probability

objective_value = sum([computeCustomerObj(i) for i in data])
print(objective_value)