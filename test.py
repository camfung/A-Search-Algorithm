from dataStructures import LoopingAgent
import asyncio
from aiohttp import web
import socketio

# Create a Socket.IO server
sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

agent = LoopingAgent(
    row=2,
    col=1,
    route_planned=[
        (1, 1),
        (2, 1),
        (3, 1),
        (4, 1),
        (5, 1),
        (5, 2),
        (5, 3),
        (6, 3),
        (7, 3),
        (7, 4),
        (7, 5),
        (6, 5),
        (5, 5),
        (5, 6),
        (5, 7),
        (5, 8),
        (6, 8),
        (7, 8),
        (8, 8),
    ],
)


# Your simulation function
async def run_simulation():
    print("entered simulation loop")
    while True:
        # Update simulation state
        print("entered simulation loop")
        agent.step()
        print(agent.route_planned)
        print(agent.route_travelled)

        # Emit the state to all connected clients
        await sio.emit("simulation_update", agent.route_travelled)

        # Wait a bit before next update (e.g., 1 second)
        await asyncio.sleep(1)


# Start the simulation when the server starts
@sio.event
async def connect(sid, environ):
    print("Client connected:", sid)


@sio.event
async def disconnect(sid):
    print("client disconnected", sid)


# Start the server and the simulation
if __name__ == "__main__":
    sio.start_background_task(run_simulation)  # Start simulation in the background
    web.run_app(app)
