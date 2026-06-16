#!/usr/bin/env python3

import sys

from common import print_tour, read_input


def solve(cities):
    # list of (x,y) coordinates
    # Build a trivial solution.
    # Visit the cities in the order they appear in the input.
    return greedy(cities)

def greedy(cities):
    """
    - Pick a starting point
    - Add it to visited, add it to your route
    - From current position, scan all unvisited points and pick the closest
    - Move there, mark visited, repeat
    - Stop when all points are visited
    """
    #start from the city at the very corner(smallest)
    start_ind = find_corner(cities)
    #visited will keep track of index for convinience
    visited = {start_ind,}
    path = [start_ind]
    cur_city = cities[start_ind]
    #while not all cities have been visited
    while len(visited) != len(cities):
        next_city = get_closest(cur_city, cities, visited)
        visited.add(next_city)
        path.append(next_city)
        #update the current city to next (here it is an actua coordinate not an index)
        cur_city = cities[next_city]
    return path

def find_corner(cities):
    """
    will find the smallest coordinate
    will use that as a starting point -> O(n)
    """
    small_x = float('inf')
    small_y = float('inf')
    small_ind = -1

    for ind, city in enumerate(cities):
        x, y = city
        if x < small_x:
            small_x, small_y = x, y
            small_ind = ind

        elif x == small_x:
            if y < small_y:
                small_x, small_y = x, y
                small_ind = ind
    return small_ind

def calculate_distance(start, end):
    """
    will ignore sqrt since in terms of comparison it is
    not necessary
    """
    x1, y1 = start
    x2, y2 = end
    return (x2-x1)**2 + (y2-y1)**2

def get_closest(current, cities, visited):
    """return index of the new city for convinience"""
    closest = (None, float('inf'))
    for ind, city in enumerate(cities):
        if ind not in visited:
            dist = calculate_distance(current, city)
            if dist < closest[1]:
                closest = (ind, dist)
    return closest[0]

if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
