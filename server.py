from re import X
from flask import Flask, request, jsonify
from model import *
import os

app = Flask("Act int 1 server")

numberRobots = 5
floorWidth = 15
floorHeight = 15
density = 0.65
trafficModel = None
baseX = 0
baseZ = 0
counter = 0

#Create the flask server
@app.route("/")
def default():
    print("Recieved a requests at /")
    return "Inital connection successful!"

@app.route('/init', methods=['POST', 'GET'])
def initModel():
    global trafficModel, numberRobots, floorWidth, floorHeight, baseX, baseZ, density

    if request.method == 'POST':
        number_agents = int(request.form.get('numberAgents'))
        trafficModel = RandomModel(number_agents)

        print(request.form)
        print(number_agents)

        return jsonify({"message":"Parameters recieved, model initiated."})

@app.route('/getAgents', methods=['GET'])
def getAgents():
    global trafficModel

    if request.method == 'GET':
        #carPositions = [{"x": x, "y":0, "z":z} for (a, x, z) in trafficModel.grid.coord_iter() if isinstance(a, cargador)]
        carPositions = []
        for (c, x, z) in trafficModel.grid.coord_iter():
            for contents in c:
                if(isinstance(contents, Car)):
                    print("Found a car")
                    carPositions.append({"x":x, "y":0.18, "z":z})

        return jsonify({'positions':carPositions})

@app.route('/getTrafficLightsPos', methods=['GET'])
def getTrafficLightsPos():
    global trafficModel

    if request.method == 'GET':
        #boxPositions = [{"x": x, "y":0, "z":z} for (a, x, z) in trafficModel.grid.get_cell_list_contents() if isinstance(a, caja)]
        trafficLightPositions = []
        trafficLightStates = []
        for (c, x, z) in trafficModel.grid.coord_iter():
            for contents in c:
                if(isinstance(contents, Traffic_Light)):
                    trafficLightPositions.append({"x":x, "y":0, "z":z})
                    trafficLightStates.append(contents.state)

        return jsonify({'positions':trafficLightPositions, "states": trafficLightStates})
        
@app.route('/getTrafficLightsState', methods=['GET'])
def getTrafficLightsState():
    global trafficModel

    if request.method == 'GET':
        #boxPositions = [{"x": x, "y":0, "z":z} for (a, x, z) in trafficModel.grid.get_cell_list_contents() if isinstance(a, caja)]
        trafficLightStates = []
        for (c, x, z) in trafficModel.grid.coord_iter():
            for contents in c:
                if(isinstance(contents, Traffic_Light)):
                    trafficLightStates.append(contents.state)

        return jsonify({'states':trafficLightStates})

@app.route('/update', methods=['GET'])
def updateModel():
    global counter, trafficModel
    if request.method == 'GET':
        trafficModel.step()
        counter += 1
        return jsonify({'message':f'Model updated to step {counter}.', 'currentStep':counter})

@app.route('/getModelSteps', methods=['GET'])
def getState():
    global trafficModel
    if request.method == 'GET':
        steps = trafficModel.getSteps()
        return jsonify({'steps':steps})
        """ state = trafficModel.getState()
        return jsonify({'isDone':state}) """

""" if __name__=='__main__':
    app.run(host="localhost", port=8585, debug=True) """

#app.run()
port = int(os.getenv('PORT', 8080))
app.run(host='0.0.0.0', port=port, debug=True)