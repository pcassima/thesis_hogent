class Graph {
    constructor() {
    }
    draw(draw_width, draw_height) {
        stroke(225, 28, 132);
        strokeWeight(1);
        beginShape(LINES);
        // x-axis
        vertex(15, draw_height - 25);
        vertex(draw_width - 25, draw_height - 25);
        // y-axis
        vertex(25, 25);
        vertex(25, draw_height - 15);

        endShape();
    }
}

let canvas;
let canvas_parent;
let PID_graph;
let prevTime = 0;
let startTime = 0;
let curTime = Date.now();

let setPoint = [];
let outPut = [];
let index = 25;

let Kp = 0;
let Ki = 0;
let Kd = 0;

function reset() {
    // Get the sliders
    P_slider = document.getElementById('PID-SIM-P');
    I_slider = document.getElementById('PID-SIM-I');
    D_slider = document.getElementById('PID-SIM-D');
    // Get the slider value
    Kp = P_slider.value / 10;
    Ki = I_slider.value / 10;
    Kd = D_slider.value / 10;

    // Set the start time
    startTime = Date.now();

    // Clear the canvas
    clear()
}

function setup() {
    frameRate(30);
    // Get the <div> that contains the canvas
    canvas_parent = document.getElementById('PID-SIM');
    // Create a canvas with the fixed height and calculated width.
    canvas = createCanvas(600, 250);
    // Set the parent of the canvas to the <div>
    canvas.parent(canvas_parent);

    PID_graph = new Graph();

    reset();

}

function PID() {
    P_term = 0;
    I_term = 0;
    D_term = 0;
    output = P_term + I_term + D_term;
    return output;
}

function draw() {
    //Transparent background
    background(0, 0, 0, 0);

    prevTime = curTime;
    curTime = Date.now();
    deltaTime = curTime - prevTime;
    elapsedTime = curTime - startTime;

    if (index <= 575) {
        // As long as the index is within the graph run
        if (elapsedTime > 2000) {
            // After a certain time is passed, activate the step in the setpoint.
            value = 1;
            setPoint.push(value * 150);
        } else {
            value = 0;
            setPoint.push(0);
        }

        strokeWeight(2);
        stroke(0, 0, 255);
        beginShape();
        vertex(index - 1, (225 - setPoint[setPoint.length - 2]));
        vertex(index, (225 - setPoint[setPoint.length - 1]));
        endShape();
        index++;
    }
    PID_graph.draw(600, 250);
}