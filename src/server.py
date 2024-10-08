import threading
import logging
from MakeMaze import make_maze_recursion
from datetime import datetime
from dataStructures import Grid, LoopingAgent, AgentsHandler
from sim import Sim
import socketio
import time
from flask import Flask, send_from_directory
from flask_cors import CORS

logger = logging.getLogger(__name__)
grid_width, grid_height = 10, 10
# grid = Grid(width=10, height=10)
grid = make_maze_recursion(grid_width, grid_height)
print(grid.get_walls())


agents = [LoopingAgent(row=1, col=1, dest_row=8, dest_col=8)]

agents_handler = AgentsHandler(agents=agents, grid=grid)
sim = Sim(grid, agents_handler)
sim.agents_handler.calculate_agents_routes()


# Define the simulation
def run_simulation():
    while True:
        for agent in agents_handler.agents:
            agent.step()
        # Update simulation state
        state = [(agent.row, agent.col) for agent in agents_handler.agents]
        sio.emit("update", state)  # Emit state to clients
        time.sleep(1)  # Simulate time delay


# Initialize Flask app and Socket.IO server
app = Flask(__name__)
CORS(app)
sio = socketio.Server(cors_allowed_origins="*")

# Wrap the Flask app with Socket.IO's WSGI middleware
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)


@sio.event()
def connect(sid, environ):
    print("Client connected:", sid)
    sio.emit(
        "onConnect",
        {"walls": grid.get_walls(), "dimensions": (grid.width, grid.height)},
    )


@sio.event()
def disconnect(sid):
    print("Client disconnected:", sid)


@sio.event()
def resetgrid(sid):
    print("reset grid called")
    grid = make_maze_recursion(grid_width, grid_height)
    print({"walls": grid.get_walls(), "dimensions": (grid.width, grid.height)})

    sio.emit(
        "gridupdate",
        {"walls": grid.get_walls(), "dimensions": (grid.width, grid.height)},
    )


# Define a route for the Flask app (optional)
@app.route("/")
def index():
    return "server is running"


# Start the simulation in a separate thread
simulation_thread = threading.Thread(target=run_simulation)
simulation_thread.start()

# Start the Flask server
if __name__ == "__main__":
    logging.basicConfig(filename=f"{ datetime.today().strftime('%Y-%m-%d') }")
    app.run(host="localhost", port=5000)
