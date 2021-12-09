from mesa import Agent
import random
from queue import PriorityQueue
import sys
import math

class Car(Agent):

    def __init__(self, unique_id, base, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos
        self.desitions = set ({(-1,-1)})
        self.base = base #la va a recibir del modelo
        self.intendedDirection = self.getRoadDirection(self.pos)
        print("LA DEST:")
        print(self.base)

    def getRoadDirection(self, posi):
        for currAg in self.model.grid.get_cell_list_contents(posi):
            if(isinstance(currAg, Road)):
                return currAg.direction
            elif(isinstance(currAg, Traffic_Light)):
                return "S"

    def getTurningVals(self, posi):
        direct = self.getRoadDirection(posi) 
        directionsList = {}
        if(direct != "S" or direct != "crossing"):
            direct = self.intendedDirection

        if(direct == "Up" or direct == "Down"):
            directionsList = {
            "turnIzq": (self.pos[0] - 1, self.pos[1]),
            "turnDer" : (self.pos[0] + 1, self.pos[1]), 
            }
        elif(direct == "Left"):
            directionsList = {
            "turnIzq": (self.pos[0], self.pos[1] + 1), 
            "turnDer" : (self.pos[0], self.pos[1] - 1),
            }
        elif(direct == "Right"):
            directionsList = {
            "turnIzq": (self.pos[0], self.pos[1] - 1), 
            "turnDer" : (self.pos[0], self.pos[1] + 1),
            }
        return directionsList

    def getCarDirection(self, posi):
        direct = self.getRoadDirection(posi) 
        directionsList = {}
        if(direct != "S" or direct != "crossing"):
            direct = self.intendedDirection

        if(direct == "Up"):
            directionsList = {
            (self.pos[0] - 1, self.pos[1] + 1) : "dIzq", #Diagonal izquierda
            (self.pos[0], self.pos[1] + 1) : "centro", #Centro
            (self.pos[0] + 1, self.pos[1] + 1) : "dDer", #Diagonal derecha
            }
        elif(direct == "Down"):
            directionsList = {
            (self.pos[0] - 1, self.pos[1] - 1) : "dIzq", #Diagonal izquierda
            (self.pos[0], self.pos[1] - 1) : "centro", #Centro
            (self.pos[0] + 1, self.pos[1] - 1) : "dDer", #Diagonal derecha
            }
        elif(direct == "Left"):
            directionsList = {
            (self.pos[0] - 1, self.pos[1] - 1) : "dIzq", #Diagonal izquierda
            (self.pos[0] - 1, self.pos[1]) : "centro", #Centro
            (self.pos[0] - 1, self.pos[1] + 1): "dDer", #Diagonal derecha
            }
        elif(direct == "Right"):
            directionsList = {
            (self.pos[0] + 1, self.pos[1] + 1): "dIzq", #Diagonal izquierda
            (self.pos[0] + 1, self.pos[1]): "centro", #Centro
            (self.pos[0] + 1, self.pos[1] - 1): "dDer", #Diagonal derecha 
            }
        

        return directionsList


    def CellFinder(self, pos, obj):
        for currAg in self.model.grid.get_cell_list_contents(pos):
            if(isinstance(currAg, obj)):
                return True
        return False


    def SemaforoCellState(self, pos):
        for currAg in self.model.grid.get_cell_list_contents(pos):
            if(isinstance(currAg, Traffic_Light)):
                if(currAg.state == False):
                    return "red"
        return "green"

    def checkKey(self, dict, key):
        if key in dict.keys():
            return True
        else:
            return False

    def move(self):

        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
            include_center=False) 

        if(self.pos == self.base):
            return

        dicti = self.getCarDirection(self.pos)
        

        newPossibleSteps = []
        valList = list(dicti.values())
        keyList = list(dicti.keys())

        for i in possible_steps:
            if(self.checkKey(dicti, i)):

                if(i == self.base):
                    self.model.grid.move_agent(self, i)
                    return
                if(self.CellFinder(i, Obstacle) == False and self.CellFinder(i, Destination) == False):
                    if(self.CellFinder(i, Traffic_Light)):
                        if(self.SemaforoCellState(i) == "green"):
                            if(not self.CellFinder(i, Car)):
                                newPossibleSteps.append(i)

                    elif(not self.CellFinder(i, Traffic_Light)):
                        if(not self.CellFinder(i, Car)):
                            print("NO CHOQUEN PORFA")
                            newPossibleSteps.append(i)
                    
                    elif(not self.CellFinder(i, Car)):
                        print("NO CHOQUEN PORFA")
                        newPossibleSteps.append(i)


        '''#Avoid colisions when moving diagonally
        turningDicti = self.getTurningVals(self.pos)
        print("VALE el val list?")
        #print(keyList[valList.index("dIzq")])
        if(keyList[valList.index("dIzq")] and keyList[valList.index("dIzq")] in newPossibleSteps and self.CellFinder(turningDicti["turnIzq"], Car)):
            newPossibleSteps.remove(keyList[valList.index("dIzq")])
        #print(keyList[valList.index("dDer")])
        if(keyList[valList.index("dDer")] and keyList[valList.index("dDer")] in newPossibleSteps and self.CellFinder(turningDicti["turnDer"], Car)):
            newPossibleSteps.remove(keyList[valList.index("dDet")])
        #print(keyList[valList.index("centro")])
        if(keyList[valList.index("centro")] and keyList[valList.index("centro")] in newPossibleSteps and self.CellFinder(keyList[valList.index("centro")] , Car)):
            print("NO CHOQUEN PORFA")
            newPossibleSteps.remove(keyList[valList.index("centro")] )'''

        newDist = {}

        for i in newPossibleSteps:
            if(i == self.base):
                self.model.grid.move_agent(self, i)
                return

            if (self.CellFinder(self.pos, Traffic_Light) and self.CellFinder(i, Traffic_Light)):
                pass
            else:
                newDist[math.sqrt(math.pow(i[0] - self.base[0], 2) + math.pow(i[1] - self.base[1], 2))] = i

        if(not newDist):
            pass
        else:
            movingTo = min(newDist.keys())
            originalLen = len(newDist)
            while(newDist[movingTo] in self.desitions and not len(newDist) < 3):
                del newDist[movingTo]
                movingTo = min(newDist.keys())
            if(originalLen == 3):
                self.desitions.add(newDist[movingTo])

            
            if(self.getRoadDirection(newDist[movingTo]) != "crossing" and not self.getRoadDirection(newDist[movingTo]) == "S"):
                self.intendedDirection = self.getRoadDirection(newDist[movingTo])
            self.model.grid.move_agent(self, newDist[movingTo])


    def step(self):
        self.move()
        pass

class Traffic_Light(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model, state = False, timeToChange = 10, direct = "Up"):
        super().__init__(unique_id, model)
        self.state = state
        self.timeToChange = timeToChange
        self.direct = direct

    def step(self):
        #if self.model.schedule.steps % self.timeToChange == 0:
            #self.state = not self.state
        pass

class Destination(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model) 

    def step(self):
        pass

class Obstacle(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Road(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model, direction= "Left"):
        super().__init__(unique_id, model)
        self.direction = direction

    def step(self):
        pass
    