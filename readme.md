# Project Overview

To run this project, install all the dependencies in the `requirements.txt` file. Then run the server using the `server.py` file.

## Demo
![](/mazedemo.gif)

## Motivation

The motivation for this project was to create a client-server app with a server-side simulation that can be viewed and interacted with by a client. I wanted to make an online game, but found it too complicated, so I took something I had a good understanding of (the maze and maze solver simulation) and turned it into a client-server application.

## Client Development

I originally made the client in Python with Pygame, but I found that it was taking too long to implement the features I wanted. Therefore, I decided to make it into an HTML/JS application since I already knew how to create a simple client setup with it.

## Code Organization

The code for the maze solver is organized to be easily extensible. Everything is very loosely coupled so that changes can be made where needed as the simulation grows.

### Agent Behavior

There is an example of how the agents can be given different behaviors. Currently, the agents have to use the A* algorithm to find their way through the maze, but this is easily changeable since the input is just a grid and the output is a path.

## Maze Generation

Currently, there is only one maze generation algorithm, but that's not the focus of this project, so I don't plan on working on that any time soon.

## Server

The server code is pretty rough. I plan on changing it to use the class-based namespace method in Socket.IO, so the grid isn't just a global variable in the script. This is probably the next step to make the server cleaner and more organized.

## To-Do

- Make the agent into a base class.
- Implement a `calcPath` method in the agent base class that can use different algorithms to find the path through the maze.
