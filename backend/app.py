from flask import Flask, jsonify, request
from flask_cors import CORS
from threading import Thread
import time
from sim import TrainInfo, TrainSim
import pprint
import json
from loguru import logger

app = Flask(__name__)
CORS(app)

# A variable to control the simulation loop
simulations = {} # {id: {"simulation": Thread, "last_update": time.time(), "running": True}}
inc = 0

def run_simulation(id):
    global simulations
    logger.debug(f"Running {id} from thread {simulations}")
    sim = simulations[id]
    while sim["running"]:
        metrics = sim["train_sim"].step()  # Perform a simulation step
        logger.info(json.dumps({"id":id,"metrics":metrics}, indent=2))
        simulations[id]['metrics'] = metrics
        time.sleep(sim["train_sim"].timestep)  # Sleep for the timestep duration

def check_for_timeout():
    global simulations
    while True:
        logger.info("Checking for timeouts")
        for x in simulations:
            if time.time() - simulations[x]["last_update"] > 900:
                logger.info(f"Timeout for {x}")
                simulations[x]["running"] = False
                simulations[x]["simulation"].join()
        time.sleep(10)

@app.route('/status', methods=['GET'])
def get_status():
    """Endpoint to get the current simulation state."""
    id = request.args.get('id')
    return jsonify(simulations[id]["metrics"])  # This will return the latest state

@app.route('/actions', methods=['POST'])
def perform_actions():
    """Endpoint to submit actions to the simulation."""
    id = request.args.get('id')
    action_data = request.json
    simulations[id]["train_sim"].actions(action_data)  # Perform actions based on the submitted data
    simulations[id]["last_update"] = time.time()
    return jsonify({"message": "Actions applied."})


# kill after 5 minutes 
@app.route('/start', methods=['GET'])
def start_session():
    """Start the session for a user"""
    global simulations, inc
    id = str(inc)

    # Initialize your TrainInfo and TrainSim instances
    train_info = TrainInfo()
    train_sim = TrainSim(train_data=train_info, timestep=1) 
    
    simulations[id] = { "train_info": train_info,  # Assuming default values
                        "train_sim": train_sim,
                        "last_update": time.time(), 
                        "running": True
                    }
    thread = Thread(target=run_simulation, args=[id])
    thread.start()  # Start the thread

    simulations[id]["simulation"] = thread

    inc += 1
    return jsonify({"id": id})


@app.route('/stop', methods=['GET'])
def stop_session():
    """Stop the session for a user"""
    global simulations
    id = request.args.get('id')
    print(f"Stopping {id}")
    simulations[id]["running"] = False
    simulations[id]["simulation"].join()
    del simulations[id]

    return jsonify({"message": "Session stopped"})


timeout_thread = Thread(target=check_for_timeout)
timeout_thread.start()


if __name__ == '__main__':
    # Start the simulation in a separate thread

    try:
        app.run(port=5000)  # Run the Flask app
    finally:
        for x in simulations:
            simulations[x]["running"] = False
            simulations[x]["simulation"].join()

