
# Hamilton Bradford
# CS 4242 - Artificial Intelligence
# Assignment 1
# February 5th, 2019

import Grid as grid
import ReflexAgent as reflex

agent = reflex.ReflexAgent()
agent.setDirtLocation()
grid1 = grid.Grid(agent.getDirtList(), agent.getAgentLocation())

grid1.printGrid()
agent.printDirtList()

print("\n")

agent.MoveAgent()

grid2 = grid.Grid(agent.getDirtList(), agent.getAgentLocation())
grid2.printGrid()

print("Time Complexity: O(n + sqrt(n) ) ")
