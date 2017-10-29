//
// HTML5 is a pretty cool guy
//
// Matrix adapted from http://thecodeplayer.com/walkthrough/matrix-rain-animation-html5-canvas-javascript
//

var drawLoop = null;
var auto_reset = true;

function redPill() {
    // go deeper

    setTimeout(function() {
        $("#matrix").css("display", "unset");
        runMatrix();

        // Triggers the background-color to transition to black
        // because of CSS settings
        $("#matrix").css("background-color", "black");

        // Start popping up flags like crazy after 10 seconds of matrix
        setTimeout(function() {
            flagsForDays();

            // Stop popping up the flags 10 seconds later
            setTimeout(function() {
                stopFlyingFlags();
                setTimeout(function() {
                    stopMatrix($("#matrix"));
                }, 1000)
            }, 10000);
        }, 10000);
    }, 1000);
}

function runMatrix() {
    var canvas = document.getElementById("matrix");
    var context = canvas.getContext("2d");

    // Get the proper height (full height of entire document)
    // by getting the largest of all the heights...browsers
    // don't all use these height values for the same thing
    // so we need to check.
    var body = document.body;
    var html = document.documentElement;
    var height = Math.max(
        body.scrollHeight,
        body.offsetHeight,
        html.clientHeight,
        html.scrollHeight,
        html.offsetHeight,
        window.innerHeight
    );

    // Making the canvas full screen
    canvas.height = height;
    canvas.width = window.innerWidth;

    // Chinese characters - taken from the unicode charset
    var chinese = "田由甲申甴电甶男甸甹町画甼甽甾甿畀畁畂畃畄畅畆畇畈畉畊畋界畍畎畏畐畑";
    // Converting the string into an array of single characters
    chinese = chinese.split("");

    var font_size = 10;
    var columns = canvas.width/font_size; // Number of columns for the rain

    // An array of drops - one per column
    var drops = [];

    // x below is the x coordinate
    // 1 = y co-ordinate of the drop(same for every drop initially)
    for(var x = 0; x < columns; x++)
        drops[x] = 1; 

    // Drawing the characters
    function draw()
    {
        // Black BG for the canvas
        // Translucent BG to show trail
        context.fillStyle = "rgba(0, 0, 0, 0.05)";
        context.fillRect(0, 0, canvas.width, canvas.height);

        context.fillStyle = "#0F0"; // Green text
        context.font = font_size + "px arial";

        // Looping over drops
        for(var i = 0; i < drops.length; i++)
        {
            // A random chinese character to print
            var text = chinese[Math.floor(Math.random()*chinese.length)];
            // x = i*font_size, y = value of drops[i]*font_size
            context.fillText(text, i*font_size, drops[i]*font_size);
            
            // Sending the drop back to the top randomly after it has crossed the screen
            // Adding a randomness to the reset to make the drops scattered on the Y axis
            if(drops[i]*font_size > canvas.height && Math.random() > 0.975 && auto_reset)
                drops[i] = 0;

            // Incrementing Y coordinate
            drops[i]++;
        }
    }

    // Draw every 33 milliseconds
    drawLoop = setInterval(draw, 33);
}

function stopMatrix(element) {
    if (drawLoop) {
        auto_reset = false; // Don't reset the characters to the top of the screen
        var tmpDrawLoop = drawLoop;
        runMatrix(); // Because this will create another drawLoop

        element.css("background-color", "transparent");

        setTimeout(function() {
            clearInterval(tmpDrawLoop);
            clearInterval(drawLoop);
            element.css("display", "none");
            element.css("width", "0px");
            element.css("height", "0px");
            element.css("position", "absolute");
            element.css("top", "0px");
            element.css("left", "0px");
        }, 8000);
    }
}