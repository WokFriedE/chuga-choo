from flask import Flask, jsonify, request
from threading import Thread
import time
from sim import TrainInfo, TrainSim
import pprint
app = Flask(__name__)

# Initialize your TrainInfo and TrainSim instances
train_info = TrainInfo()  # Assuming default values
train_sim = TrainSim(train_data=train_info, timestep=1)

# A variable to control the simulation loop
running = True

def run_simulation():
    while running:
        metrics = train_sim.step()  # Perform a simulation step
        pprint.pp(metrics)
        time.sleep(train_sim.timestep)  # Sleep for the timestep duration

@app.route('/status', methods=['GET'])
def get_status():
    """Endpoint to get the current simulation state."""
    return jsonify(train_sim.step())  # This will return the latest state

@app.route('/actions', methods=['POST'])
def perform_actions():
    """Endpoint to submit actions to the simulation."""
    action_data = request.json
    train_sim.actions(action_data)  # Perform actions based on the submitted data
    return jsonify({"message": "Actions applied."})

if __name__ == '__main__':
    # Start the simulation in a separate thread
    simulation_thread = Thread(target=run_simulation)
    simulation_thread.start()
    
    try:
        app.run(port=5000)  # Run the Flask app
    finally:
        running = False  # Stop the simulation loop on exit
        simulation_thread.join()  # Wait for the simulation thread to finish
