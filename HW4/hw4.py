# Freddie He
# 1560733
# heyingge

# To run this code, run in this format: python3 hw4.py filename
# Python3 is required

import sys
import time
import math

N = 0  # number of points

# Point Class
class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def distance(self, other):
        return math.sqrt(pow(self.x - other.x, 2) + pow(self.y - other.y, 2))


# reading points
def readfile(filename, points):
    global N

    with open(filename) as f:
        coord = f.read().split()

    temp = set()  # remove duplicates

    for i in range(0, len(coord), 2):
        temp.add(Point(float(coord[i]), float(coord[i+1])))
        N += 1

    for point in temp:
        points.append(point)


# sort by x function
def return_x(p):
    return p.x


# sort by y function
def return_y(p):
    return p.y


# Version 1
def v1(points):
    min_dist = math.inf
    min_pair = (None, None)
    for i in range(0, len(points)):
        for j in range(i+1, len(points)):
            p1 = points[i]
            p2 = points[j]
            dist_curr = p1.distance(p2)
            if dist_curr < min_dist:
                min_dist = dist_curr
                min_pair = (p1, p2)
    return min_pair


# Version 2
def v2(points):
    # base case
    if len(points) <= 1:
        return Point(math.inf, math.inf), Point(-math.inf, -math.inf)

    # compute separation line
    mid = len(points)//2 + 1 if len(points) % 2 == 1 else len(points)//2
    l = points[mid - 1].x

    left_half = points[0:mid]
    right_half = points[mid:]

    delta1 = v2(left_half)
    delta2 = v2(right_half)
    delta1_len = delta1[0].distance(delta1[1])
    delta2_len = delta2[0].distance(delta2[1])
    delta = delta1 if delta1_len <= delta2_len else delta2
    delta_len = delta[0].distance(delta[1])

    # delete all points further than delta from separation line L
    mid_points = []
    for i in range(0, len(points)):
        if points[i].x < (l - delta_len):
            continue
        elif points[i].x > (l + delta_len):
            break
        else:
            mid_points.append(points[i])
    mid_points.sort(key=return_y)

    m = len(mid_points)
    for i in range(0, m):
        k = 1
        while i + k < m and mid_points[i+k].y < (mid_points[i].y + delta_len):
            curr_dis = mid_points[i].distance(mid_points[i + k])
            if curr_dis < delta_len:
                delta = (mid_points[i], mid_points[i+k])
                delta_len = curr_dis
            k += 1
    return delta


# Merge two sorted lists
def merge_two_sorted_lists(l1, l2):
    i = j = 0
    lst = []
    while i < len(l1) and j < len(l2):
        if l1[i].y <= l2[j].y:
            lst.append(l1[i])
            i += 1
        else:
            lst.append(l2[j])
            j += 1

    if i == len(l1):
        lst.extend(l2[j:])
    else:
        lst.extend(l1[i:])
    return lst


# Version 3
def v3(points):
    # base case
    if len(points) <= 1:
        return (Point(math.inf, math.inf), Point(-math.inf, -math.inf)), points

    # compute separation line
    mid = len(points)//2 + 1 if len(points) % 2 == 1 else len(points)//2
    l = points[mid - 1].x

    left_half_x = points[0:mid]
    right_half_x = points[mid:]

    (delta1, left_half_y) = v3(left_half_x)
    (delta2, right_half_y) = v3(right_half_x)
    delta1_len = delta1[0].distance(delta1[1])
    delta2_len = delta2[0].distance(delta2[1])
    delta = delta1 if delta1_len <= delta2_len else delta2
    delta_len = delta[0].distance(delta[1])

    # delete all points further than delta from separation line L
    merged_y = merge_two_sorted_lists(left_half_y, right_half_y)
    mid_points = []
    for p in merged_y:
        if l - delta_len <= p.x <= l + delta_len:
            mid_points.append(p)

    m = len(mid_points)
    for i in range(0, m):
        k = 1
        while i + k < m and mid_points[i+k].y < (mid_points[i].y + delta_len):
            curr_dis = mid_points[i].distance(mid_points[i + k])
            if curr_dis < delta_len:
                delta = (mid_points[i], mid_points[i+k])
                delta_len = curr_dis
            k += 1
    return delta, merged_y


def main():
    points = list()
    readfile(sys.argv[1], points)
    # print("actual points: " + str(len(points)))

    if len(points) < 2:
        print('Input has fewer than 2 distinct points.')
    else:
        # start timing
        start = time.time()
        closest_pair = v1(points)
        end = time.time()
        print("Version 1: " + str(N) + " points, closest pair p1: " +
              str(closest_pair[0]) + " p2: " + str(closest_pair[1]) +
              " delta: " + str(closest_pair[0].distance(closest_pair[1]))
              + " time: " + str(end - start) + "s")

        # globally sort by x-coordinate
        points.sort(key=return_x)
        start = time.time()
        closest_pair = v2(points)
        end = time.time()
        print("Version 2: " + str(N) + " points, closest pair p1: " +
              str(closest_pair[0]) + " p2: " + str(closest_pair[1]) +
              " delta: " + str(closest_pair[0].distance(closest_pair[1]))
              + " time: " + str(end - start) + "s")

        start = time.time()
        closest_pair = v3(points)[0]
        end = time.time()
        print("Version 3: " + str(N) + " points, closest pair p1: " +
              str(closest_pair[0]) + " p2: " + str(closest_pair[1]) +
              " delta: " + str(closest_pair[0].distance(closest_pair[1]))
              + " time: " + str(end - start) + "s")


if __name__ == "__main__":
    main()