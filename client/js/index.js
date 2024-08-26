console.log("client script loaded") 
const socket = io.connect("http://localhost:5000"); 
console.log("test")
socket.emit("join")

let agents = [] 

let grid  = null

socket.on("join", (data) => {
}); 
socket.on("gridupdate", (data) => {
    grid = data
    drawMaze(grid)
}); 

socket.on("onConnect", (data) => {
console.log(data)
	grid = data
	drawMaze(data)
}); 
socket.on("update", (data) => {
console.log("update" , data)
	drawMaze(grid)
drawAgents(data); 
}); 
function drawMaze(data) {
    const walls = data.walls;
    const [rows, cols] = data.dimensions;

    const canvas = document.getElementById("canvas")
    canvas.width = cols * 20;
    canvas.height = rows * 20;
    const ctx = canvas.getContext('2d');

    // Draw walls
    walls.forEach(([x, y]) => {
        ctx.fillStyle = 'black';
        ctx.fillRect(y * 20, x * 20, 20, 20);
    });

    document.body.appendChild(canvas);
}

function drawAgents(data) {
    const canvas = document.getElementById("canvas")
    const ctx = canvas.getContext('2d');
	data.forEach(([x,y]) => {
		ctx.fillStyle = "blue"
		ctx.fillRect(y * 20, x * 20, 20, 20); 
	})
}
function test() {
    socket.emit("resetgrid")
}
