
// Stores the interval ID for the startTimer() method
var rotTimerItervalId = null;

function openRotModal() {
    $("#rotButton").text("ROT?");
    $("#rotModal").modal({show: true});

    console.log("Welcome to the ROT challenge.");
    console.log("Using the console, an answer can be submitted.");
    console.log("The encrypted message is stored in the browser's");
    console.log("local storage: 'localStorage.getItem('encrypted_message');'");
    console.log("To submit an answer call:");
    console.log("'submitAnswer(clear_text, complete=function(success){})'");
    console.log("where 'clear_text' is the decrypted message and 'complete' is");
    console.log("the callback that get's called when the request is complete with status.");
    console.log("The answer is not case sensitive but punctuation must be");
    console.log("consistent. You need to solve 50 in the time limit or ");
    console.log("the game will reset. Good Luck!");
}

function stopTimer(display) {
    display.text("0");

    if (rotTimerItervalId) {
        clearInterval(rotTimerItervalId);
        rotTimerItervalId = null;
    }
}

function startTimer(seconds, display) {
    // First, stop the current timer if there is one
    stopTimer(display);

    seconds = Math.trunc(seconds);

    if (seconds < 0) {
        seconds = 0;
    }

    rotTimerItervalId = setInterval(function () {
        display.text(seconds);
        seconds = seconds - 1;

        if (seconds < 0) {
            rot();
        }
    }, 1000);
}

function rot() {
    var session_id = localStorage.getItem("session_id");

    $.ajax({
        url: "/crapdb/rot/" + session_id + "/",
        type: "GET",
        success: function(data) {
            var res = JSON.parse(data);
            console.log("Res: ", res);
            if (res.redirect) {
                window.location = "/crapdb/?error=" + encodeURIComponent(res.redirect);
                return;
            } else if (res.error) {
                errorAlert(res.error);
                return;
            } 

            startTimer(res.remaining_time, $("#rot_timer"));

            $("#num_to_solve").text(res.num_to_solve);
            $("#num_solved").text(res.num_solved);

            // Update the hacker bucks
            $("#hackerBucks").text(res.hacker_bucks);
            $("#cipher-text").text(res.encrypted_message);
            localStorage.setItem("encrypted_message", res.encrypted_message);
            openRotModal();
        }
    });
}

function submitAnswer(answer, complete=null) {
    var encrypted_message = localStorage.getItem("encrypted_message");
    if (!encrypted_message) {
        console.log("The encrypted message has not been retrieved yet.");
        console.log("Click on the 'ROT?' link and pay $25 to");
        console.log("start the challenge");
        return false;
    }

    $("#cleartext").val(answer);

    var session_id = localStorage.getItem("session_id");
    var csrf_token = localStorage.getItem("csrf_token");

    // Check and make sure we're good
    $.ajax({
        url: "/crapdb/rotflag/" + session_id + "/",
        type: "POST",
        data: {
            answer: answer,
            csrfmiddlewaretoken: csrf_token
        },
        success: function(data) {
            res = JSON.parse(data);
            console.log("Result: ", res);
            if (res.error) {
                console.log(res.error);
                errorAlert(res.error, options={
                    target: $("#rotModalFooter")
                });
            } else {
                $("#cipher-text").text(res.encrypted_message);
                $("#num_to_solve").text(res.num_to_solve);
                $("#num_solved").text(res.num_solved);
                localStorage.setItem("encrypted_message", res.encrypted_message);
                startTimer(res.remaining_time, $("#rot_timer"));

                if (res.flag) {
                    console.log(res.flag);
                    successAlert(res.flag, options={
                        target: $("#rotModalFooter"),
                        autoclose: 0
                    });
                } else if (!res.success){
                    errorAlert("Invalid answer", options={
                        target: $("#rotModalFooter")
                    });
                } else {
                    successAlert("Correct. Now solve another!", options={
                        target: $("#rotModalFooter")
                    });
                }
            }
            if (complete) {
                complete(res.success);
            }
        }
    });
}