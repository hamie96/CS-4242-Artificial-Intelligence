#!/usr/bin/env python3

#Course: CS4242
#Student Name: Hamilton Bradford
#Student ID: 000500409
#Assignment 2: #2
#Due Date: 03/05/19
#Signature:
#Score:

import graph as gh
import os

from heapq import *
from math import inf
from sys import argv, exit
from time import time

#Resources:
#Used the Python Node implementation from GeeksforGeeks
#Modified a wall-checker code from StackOverflow


def a_star_search(start, goal, graph):
    frontier = []
    came_from = {}
    cost = {}

    heappush(frontier, (0, start))
    came_from[start] = None
    cost[start] = 0

    # checks whether goal is possible
    if graph.is_obstacle(start):
        return None

    while frontier:
        current = heappop(frontier)[1]
        
        if current == goal:
            return came_from

        for neighbor in graph.neighbors(current):
            new_cost = cost[current] + graph.cost_to(neighbor) 

            if new_cost < cost.get(neighbor, inf) and not graph.is_obstacle(neighbor):
                cost[neighbor] = new_cost
                came_from[neighbor] = current
                priority = new_cost + graph.heuristic(neighbor, goal)

                heappush(frontier, (priority, neighbor))
    return None

def reconstruct_path(start, goal, came_from):
    result = []
    node = goal
    while node != None:
        result.append(node)
        node = came_from[node]
    return result

def print_graph(path, graph):
    GREEN = '\033[38;5;82m'
    RED = '\033[38;5;196m'
    YELLOW = '\033[38;5;226m'
    RESET = '\033[0m'

    for y in range(graph.height):
        for x in range(graph.width):
            node = (x, y)

            if graph.is_obstacle(node):
                c = RED + '=' + RESET
            elif graph.cost_to(node) != 1:
                c = YELLOW + str(graph.cost_to(node)) + RESET
            elif node in path:
                c = GREEN + '#' + RESET
            else: c = '.'

            print(c + ' ', end='')
        print() # print newline

def parse_graph_file(fname, width, height):
    nodes = {} 
    x = y = 0

    with open(fname) as f:
        while True:
            c = f.read(1)

            if not c:
                return gh.PredefinedGraph(width, height, nodes)

            current = (x, y)

            if c == '\n':
                y += 1
                x = 0
            else:
                x += 1

            if c == '=': nodes[current] = -1
            if c.isdigit(): nodes[current] = int(c)


#Uses the given graph file and solves it
if __name__ == '__main__':
    width = height = 32
    PREDEF_GRAPH_DIR = 'predef_graphs' #uses the predefined graph given

    if len(argv) > 1:
        fname = PREDEF_GRAPH_DIR + os.sep + argv[1]
        if argv[1].isdigit():
            graph = gh.RandomObstacleGraph(width, height, float(argv[1]) / 100)
            print('Using %s%% obstacle chance.' % argv[1])

        elif os.path.isfile(fname):

            graph = parse_graph_file(fname, width, height)
            print('Using graph file "%s".' % fname)

        else:
            print('Graph file "%s" not found.' % fname)
            exit(1)
    else:
        graph = gh.RandomObstacleGraph(width, height, 0.2)

    #always set start to top left and bottom right
    start = (0, 0)  
    goal = (31, 31) 

    last_time = time()
    came_from = a_star_search(start, goal, graph)

    if came_from != None:
        path = reconstruct_path(start, goal, came_from) 
        print_graph(path, graph)
    else:
        print('No path was found.')
        exit(1)

    print('Finished in %fs.' % (time() - last_time))

    exit(0) #The Program crashes if I don't exit
