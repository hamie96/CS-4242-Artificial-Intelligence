# Hamilton Bradford
# CS 4242 Artificial Intelligence
# Assignment 1
# February 5th, 2019

from random import randint
import Grid as grid

class ReflexAgent:
        def __init__(self):
            self.position = randint(0,63)
            self.dirt = randint(7,16)
            self.dirt_list = []
            self.move_count = 0
           
        def getAgentLocation(self):
            return self.position
        
        def getDirt(self):
            return self.dirt
        
        def getDirtList(self):
            return self.dirt_list

        def getDirtLocation(self,x):
            return self.dirt_list[x]

        def setDirtLocation(self):
           for x in range(self.dirt):
                dirt_location = randint(0,63)

                if(dirt_location in self.dirt_list or dirt_location == self.position):
                    pass
                else:
                    self.dirt_list.append(dirt_location)     

        
        def printDirtList(self):
            print(self.dirt_list)

        def moveright(self):
            self.move_count = self.move_count + 1
            self.position = self.position + 1
            self.printMoveList("right")


        def moveleft(self):
            self.move_count = self.move_count + 1
            self.position = self.position - 1
            self.printMoveList("left")

        def moveup(self):
            self.move_count = self.move_count + 1
            self.position = self.position - 8
            self.printMoveList("up")

        def movedown(self):
            self.move_count = self.move_count + 1
            self.position = self.position + 8
            self.printMoveList("down")

        def printMoveList(self, direction):
            print("Move " + str(self.move_count) + ":Vacuum moved " + direction + " to position " + str(self.position))
            if self.position in self.dirt_list:
                self.dirt_list.remove(self.position)
                print("Dirt cleaned at position " + str(self.position))
                grid_grid = grid.Grid(self.dirt_list,self.position)
                grid_grid.printGrid()
           

        def MoveAgent(self):

            while self.position not in {0,1,2,3,4,5,6,7}:
                self.moveup()
            while self.position not in {0}:
                self.moveleft()
            
            count = 1
            for x in range(3):
                self.moveright()
                for x in range(count):
                    self.movedown()
                
                for x in range(count):
                    self.moveleft()

                self.movedown()
                
                count = count + 1

                for x in range(count):
                    self.moveright()
                
                for x in range(count):
                    self.moveup()

                count = count + 1


            for x in range(0,1): 
                self.moveright()
                for x in range(count):
                    self.movedown()
                for x in range(count):
                    self.moveleft()
