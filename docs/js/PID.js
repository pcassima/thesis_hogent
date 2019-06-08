class Graph {
    constructor() {
    }
    draw(draw_width, draw_height) {
        stroke(225, 28, 132);
        strokeWeight(1);
        beginShape(LINES);
        // x-axis
        vertex(15, draw_height-25);
        vertex(draw_width-25, draw_height-25);
        // y-axis
        vertex(25, 25);
        vertex(25, draw_height-15);

        endShape();
    }
}

class PID {
    
}

function setpoint(time){
    if (time < 1000) {
        return 0;
    }

    else {
        return 1;
    }
}

let canvas;
let canvas_parent;
let PID_graph;

function setup(){
    frameRate(30);
    // Get the <div> that contains the canvas
    canvas_parent = document.getElementById('PID-SIM');
    // // Create a canvas with the fixed height and calculated width.
    canvas = createCanvas(600, 250);
    // // Set the parent of the canvas to the <div>
    canvas.parent(canvas_parent);

    PID_graph = new Graph();

}

function draw(){
    //Transparent background
    background(0,0,0,0);
    // ellipse(50, 50, 80, 80);
    PID_graph.draw(600, 250);
}