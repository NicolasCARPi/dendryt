// START CONFIG
// between 1 and 100
var slowness = 1;

var cellRadius = 10;
var cellColor = 'green';

var nucleusRadius = cellRadius / 3;
var nucleusColor = 'blue';

var targetRadius = 10;
var targetColor = 'red';

var pathColor = 'blue';
var pathSize = 1;


// END CONFIG

// CELL
var cell = new Path.Circle({
    center: view.center,
    radius: cellRadius,
    strokeColor: cellColor,
    fillColor: cellColor
});

// NUCLEUS
var nucleus = new Path.Circle({
    center: view.center,
    radius: nucleusRadius,
    strokeColor: nucleusColor,
    fillColor: nucleusColor
});

// TARGET
var target = new Path.Circle({
    center: new Point.random() * view.size,
    radius: targetRadius,
    strokeColor: 'white',
    fillColor: targetColor
});

// PATH
var path = new Path();
path.style = {
    strokeColor: pathColor,
    strokeWidth: pathSize,
    dashArray: [1, 10]
};
// add the first point of the path
path.add(view.center);

var time = 0;
// set a random destination
var destination = Point.random() * view.size;

// Whenever the window is resized, recenter the path
function onResize(event) {
    cell.position = view.center;
}

// stop the simulation
function stopIt() {
    paper.view.detach('frame', this.onFrame);
}

// detect if the target has a collision with the path or the cell
function detectCollision() {
    var cellIntersections = cell.getIntersections(target);
    var pathIntersections = path.getIntersections(target);

    // target is found
    if (cellIntersections.length || pathIntersections.length) {
        stopIt();
        target.fillColor = 'red';
        path.strokeWidth = 2;
        alert('Target found! Time to find it: ' + time);
    }
}

// run this at 60 fps
function onFrame(event) {
    time += 1;
    var vector = destination - cell.position;
    cell.position += vector / slowness;
    nucleus.position += vector / slowness;
    path.add(destination);

    if (vector.length < cellRadius) {
        destination = Point.random() * view.size;
        path.style.strokeColor.hue += 0.1;
    }

    detectCollision();
}
