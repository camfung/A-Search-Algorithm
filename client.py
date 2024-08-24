import pygame
from dataStructures import Grid, LoopingAgent, AgentsHandler
from display import ShowSim
import socketio
import threading

# Create a Socket.IO client
sio = socketio.AsyncClient()

agent_pos = None

grid_width, grid_height = 10, 10
# 340, 130
# grid = make_maze_recursion(grid_width, grid_height)
# grid = Grid(width=grid_width, height=grid_height,
#             border_walls=True, fill=True)
grid = Grid(file_path="./test.txt")

agents = [
    LoopingAgent(1, 1, grid_height - 2, grid_width - 2),
    # Agent(1, grid_width-2, grid_height-2, 1),
    # Agent(grid_height-2, 1, 1, grid_width-2),
    # Agent(grid_height-2, grid_width-2, 1, 1)
]

agents_handler = AgentsHandler(agents=agents, grid=grid)

show_grid = ShowSim(grid, agents_handler)


# Event handler for connection
@sio.event
async def connect():
    print("Connected to the server")


# Event handler for receiving simulation updates
@sio.event
async def update(data):
    agents_handler.agents[0].pos = data[0]
    print("Simulation update:", data)


# Event handler for disconnection
@sio.event
async def disconnect():
    print("Disconnected from the server")


@sio.event
async def onConnect(data):
    print("server grid state:", data)


async def main():
    # Connect to the server
    await sio.connect("http://localhost:5000")  # Update with your server's URL and port

    # Keep the client running
    await sio.wait()


ui_thread = threading.Thread(target=show_grid.run)
ui_thread.start()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
