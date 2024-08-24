import threading
from MakeMaze import make_maze_recursion
from dataStructures import Grid, LoopingAgent, AgentsHandler
from sim import Sim
import socketio
import time
from flask import Flask


grid_width, grid_height = 10, 10
grid = Grid(width=10, height=10)
# grid = make_maze_recursion(grid_width, grid_height)


agents = [LoopingAgent(row=1, col=1, dest_row=9, dest_col=9)]

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
sio = socketio.Server()

# Wrap the Flask app with Socket.IO's WSGI middleware
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)


@sio.event
def connect(sid, environ):
    print("Client connected:", sid)


@sio.event
def disconnect(sid):
    print("Client disconnected:", sid)


# Define a route for the Flask app (optional)
@app.route("/")
def index():
    return "Socket.IO server is running!"


# Start the simulation in a separate thread
simulation_thread = threading.Thread(target=run_simulation)
simulation_thread.start()

# Start the Flask server
if __name__ == "__main__":

    app.run(host="localhost", port=5000)
