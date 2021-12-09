from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agent import *
import json

class RandomModel(Model):
    """ 
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
        height, width: The size of the grid to model
    """

    def __init__(self, N):

        destinationsList = []
        roadList = []

        dataDictionary = json.load(open("mapDictionary.txt"))

        with open('base.txt') as baseFile:
            lines = baseFile.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)

            self.ids = set ({(-1)})
            self.roadList = []
            self.destinationsList = []

            self.grid = MultiGrid(self.width, self.height,torus = False) 
            self.schedule = RandomActivation(self)

            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    if col in ["v", "^", ">", "<", "x"]:
                        if(col != "x"):
                            self.roadList.append((c, self.height - r - 1))
                        agent = Road(f"r{r*self.width+c}", self, dataDictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    elif col in ["O", "R", "U", "L"]:
                        tf = False
                        if(col == "O" or col == "U"):
                            tf = True
                        agent = Traffic_Light(f"tl{r*self.width+c}", self, tf, 4, col)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                    elif col == "#":
                        agent = Obstacle(f"ob{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    elif col == "D":
                        agent = Destination(f"d{r*self.width+c}", self)
                        self.destinationsList.append((c, self.height - r - 1))
                        self.grid.place_agent(agent, (c, self.height - r - 1))

        for i in range (N):
            carPos = (random.choice(self.roadList))
            self.roadList.remove(carPos)
            agent = Car(100 + i, (random.choice(self.destinationsList)), carPos, self)
            self.grid.place_agent(agent, carPos)
            self.schedule.add(agent)
            self.ids.add(100 + i)


        self.running = True 

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        if self.schedule.steps % 10 == 0:
            for agents, x, y in self.grid.coord_iter():
                #Aqui se añaden carritos con su dest (base)
                for agent in agents:
                    if isinstance(agent, Traffic_Light):
                        agent.state = not agent.state
        if self.schedule.steps % 30 == 0:
            newId = random.randrange(0, 1000)
            while(newId in self.ids):
                newId = random.randrange(0, 1000)

            carPos = (random.choice(self.roadList))
            agent = Car(newId, (random.choice(self.destinationsList)), carPos, self)
            self.ids.add(newId)
            self.grid.place_agent(agent, carPos)
            self.schedule.add(agent)



