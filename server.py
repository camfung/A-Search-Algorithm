import asyncio
from dataStructures import AgentsHandler, LoopingAgent
from sim import Sim
from MakeMaze import make_maze_recursion
from aiohttp import web
import socketio

# Create a Socket.IO server with an async mode
sio = socketio.AsyncServer(async_mode="aiohttp")
app = web.Application()
sio.attach(app)

grid_width, grid_height = 10, 10
grid = make_maze_recursion(grid_width, grid_height)

agents = [
    LoopingAgent(1, 1, grid_height - 2, grid_width - 2),
]

agents_handler = AgentsHandler(agents=agents, grid=grid)
sim = Sim(grid, agents_handler)
sim.agents_handler.calculate_agents_routes()


# Simulation logic
async def run_simulation():
    while True:
        sim.step()
        await sio.emit("simulation_update", sim.agents_handler.agents)
        await asyncio.sleep(1)


@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")


# Start the simulation in the background when the server starts
async def start_server():
    # Start the simulation in the background
    asyncio.create_task(run_simulation())
    # Start the web server
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()


if __name__ == "__main__":
    asyncio.run(start_server())
