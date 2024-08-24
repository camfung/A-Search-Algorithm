import socketio

# Create a Socket.IO client
sio = socketio.AsyncClient()


# Event handler for connection
@sio.event
async def connect():
    print("Connected to the server")


# Event handler for receiving simulation updates
@sio.event
async def update(data):
    print("Simulation update:", data)


# Event handler for disconnection
@sio.event
async def disconnect():
    print("Disconnected from the server")


async def main():
    # Connect to the server
    await sio.connect("http://localhost:5000")  # Update with your server's URL and port

    # Keep the client running
    await sio.wait()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
