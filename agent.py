from mesa import Agent
import random
from queue import PriorityQueue
import sys
import math

class Car(Agent):

    def __init__(self, unique_id, base, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos
        self.chosenAtTL = {}
        self.base = base #la va a recibir del modelo
        print("init")

    def getRoadDirection(self, posi):
        for currAg in self.model.grid.get_cell_list_contents(posi):
            if(isinstance(currAg, Road)):
                return currAg.direction
            elif(isinstance(currAg, Traffic_Light)):
                return "S"

    def getCarDirection(self, posi):
        direct = self.getRoadDirection(posi)
        directionsList = {}
        if(direct == "Up"):
            directionsList = {
            "vueltaIzq" : (self.pos[0] - 1, self.pos[1]), #Vuelta izquierda
            "dIzq" : (self.pos[0] - 1, self.pos[1] + 1), #Diagonal izquierda
            "centro" : (self.pos[0], self.pos[1] + 1), #Centro
            "dDer" : (self.pos[0] + 1, self.pos[1] + 1), #Diagonal derecha
            "vueltaDer" : (self.pos[0] + 1, self.pos[1]), #Vuelta derecha
            "atras" : (self.pos[0], self.pos[1] - 1) #atras
            }
        elif(direct == "Down"):
            directionsList = {
            "vueltaIzq" : (self.pos[0] - 1, self.pos[1]), #Vuelta izquierda
            "dIzq" : (self.pos[0] - 1, self.pos[1] - 1), #Diagonal izquierda
            "centro" : (self.pos[0], self.pos[1] - 1), #Centro
            "dDer" : (self.pos[0] + 1, self.pos[1] - 1), #Diagonal derecha
            "vueltaDer" : (self.pos[0] + 1, self.pos[1]), #Vuelta derecha
            "atras" : (self.pos[0], self.pos[1] + 1) #atras
            }
        elif(direct == "Left"):
            directionsList = {
            "vueltaIzq" : (self.pos[0], self.pos[1] - 1), #Vuelta izquierda
            "dIzq" : (self.pos[0] - 1, self.pos[1] - 1), #Diagonal izquierda
            "centro" : (self.pos[0] - 1, self.pos[1]), #Centro
            "dDer" : (self.pos[0] - 1, self.pos[1] + 1), #Diagonal derecha
            "vueltaDer" : (self.pos[0], self.pos[1] + 1), #Vuelta derecha
            "atras" : (self.pos[0] + 1, self.pos[1]) #atras
            }
        elif(direct == "Right"):
            directionsList = {
            "vueltaIzq" : (self.pos[0], self.pos[1] + 1), #Vuelta izquierda
            "dIzq" : (self.pos[0] + 1, self.pos[1] + 1), #Diagonal izquierda
            "centro" : (self.pos[0] + 1, self.pos[1]), #Centro
            "dDer" : (self.pos[0] + 1, self.pos[1] - 1), #Diagonal derecha
            "vueltaDer" : (self.pos[0], self.pos[1] - 1), #Vuelta derecha
            "atras" : (self.pos[0] - 1, self.pos[1]) #atras
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

    
    def moverEnRoad(self, dicti, cen, vue, dia, possible_steps):
        #It is an obstacle, I'm already the closest so move foward. DECIDED TO MOVE FOWARD
        
        if(dia in possible_steps and cen in possible_steps and (self.CellFinder(dia, Obstacle) or self.CellFinder(dia, Destination))):
            #check traffic light and other cars that may stopped for a traffic light
            if((self.CellFinder(cen, Traffic_Light) and self.SemaforoCellState(cen) == "red") or self.CellFinder(cen, Car)):
                pass
            else:
                self.model.grid.move_agent(self, cen)

            #Falta condicion de que si el coche de enfrente no se mueve

        #Can I move diagonally to get closer to x/y?
        elif(dia in possible_steps and vue in possible_steps and not self.CellFinder(dia, Obstacle) and not self.CellFinder(vue, Car)):
            if(self.CellFinder(dia, Traffic_Light) and self.SemaforoCellState(dia) == "red"):
                pass
            else:
                self.model.grid.move_agent(self, dia)

        #Aqui siempre regresa porque si es obstaculo, esta en rojo o hay un coche no avanza 
        return

    def moverEnSemaforo(self, dicti):

        #There is no x, hence, there's only one direction
        print("EN SEMAFORO")
        print(dicti["centro"])
        if(self.getRoadDirection(dicti["centro"]) != "crossing"):
            self.self.model.grid.move_agent(self, dicti["centro"])
            return

        #Takes the direction of the back of traffic light and takes it as next step
        lastDirect = dicti[self.getRoadDirection(dicti["atras"])] 

        #There is a traffic light or extra crossing in right: can only move to left
        if(self.CellFinder(dicti["dDer"], Traffic_Light) or self.getRoadDirection(dicti["dDer"]) == "crossing"):
            newDirPos = dicti["dIzq"]


        #There is a traffic light or extra crossing in left: can only move to right
        elif(self.CellFinder(dicti["dIzq"], Traffic_Light) or self.getRoadDirection(dicti["dIzq"]) == "crossing"):
            newDirPos = dicti["dDer"]

        #Get the distance between two points
        newDir = math.sqrt(pow((self.base[0] + newDirPos[0]),2) + pow((self.base[1] + newDirPos[1]),2))
        lastDir = math.sqrt(pow((self.base[0] + lastDirect[0]),2) + pow((self.base[1] + lastDirect[1]),2))
            
        chosen = min(newDir, lastDir)

        if(not chosen in self.chosenAtTL):
            self.self.model.grid.move_agent(self, chosen)
            self.chosenAtTL.add(chosen)
        else:
            self.self.model.grid.move_agent(self, max(newDir, lastDir))


    def move(self):

        print("entramos a move")

        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
            include_center=False) 

        dicti = self.getCarDirection(self.pos)

        distToX = self.pos[0] - self.base[0]
        distToY = self.pos[1] - self.base[1]

        if(distToY == 0 and distToX  == 0):
            self.grid.remove_agent(self)
            self.schedule.remove(self)


        #Avanzar para asercarse a la base tomando la mejor direccion
        else:
            #Up, Down, Left, Right, S o X
            direct = self.getRoadDirection(self.pos)

            if(direct == "Up" or direct == "Down"):
                #Need to go left
                if(distToX > 1):
                    self.moverEnRoad(dicti, dicti["centro"], dicti["vueltaIzq"], dicti["dIzq"], possible_steps)

                #Need to go right
                elif(distToX < -1):
                    self.moverEnRoad(dicti, dicti["centro"], dicti["vueltaDer"], dicti["dDer"], possible_steps)

                #Need to go right and arrives to dest
                elif(distToX == -1):
                    self.self.model.grid.move_agent(dicti["vueltaDer"])

                #Need to go left and arrives to dest
                elif(distToX == 1):
                    self.self.model.grid.move_agent(dicti["vueltaIzq"])


            elif(direct == "Left" or direct == "Right"): 
                #Need to go down
                if(distToY > 1):
                    self.moverEnRoad(dicti, dicti["centro"], dicti["vueltaDer"], dicti["dDer"], possible_steps)

                #Need to go up
                elif(distToY < -1):
                    self.moverEnRoad(dicti, dicti["centro"], dicti["vueltaIzq"], dicti["dIzq"], possible_steps)

                #Need to go up and arrives to dest
                elif(distToY == -1):
                    self.self.model.grid.move_agent(self, dicti["vueltaIzq"])

                #Need to go down and arrives to dest
                elif(distToY == 1):
                    self.self.model.grid.move_agent(self, dicti["vueltaDer"])

            elif(direct == "S"):
                
                dicti = self.getCarDirection(self.pos)
                self.moverEnSemaforo(dicti)

            elif(direct == "crossing"):
                self.model.grid.move_agent(self, dicti["centro"])


    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        # self.direction = self.random.randint(0,8)
        # print(f"Agente: {self.unique_id} movimiento {self.direction}")
        self.move()
        pass

class Traffic_Light(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model, state = False, timeToChange = 10):
        super().__init__(unique_id, model)
        self.state = state
        self.timeToChange = timeToChange

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