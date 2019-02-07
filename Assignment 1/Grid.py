# Hamilton Bradford
# CS 4242 - Artificial Intelligence
# February 5th, 2019

class Grid:
        def __init__(self,dirt_list, Agent):
            self.dirt_list = dirt_list
            self.Agent = Agent
            self.dirt_list.sort()

        def printGrid(self):
            
            print("\n")
            for x in range(64):
                if x in {7, 15, 23, 31, 39, 47,55}:
                    if x in self.dirt_list:
                        print(" [X] ")
                    elif x == self.Agent:
                        print(" [O] ")
                    else:
                        print(" [ ] ")
                else:
                    if x in self.dirt_list:
                        print(" [x] ", end = '')
                    elif x == self.Agent:
                        print(" [O] ", end = '')
                    else:
                        print(" [ ] ", end = '')
               
            print("\n")

