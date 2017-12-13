// Stores the interval ID for the startTimer() method
var rotTimerItervalId = null;
var rotNumSolved = 0;
var rotNumToSolve = 0;
var rotEncryptedMessage = "";

function openRotModal() {
    setPurchasedChallenge("rot");
    $("#rotModal").modal({show: true});

    console.log("Welcome to the ROT challenge.");
    console.log("Using the console, an answer can be submitted.");
    console.log("The current encrypted message is stored in the");
    console.log("'rotEncryptedMessage' global variable. To submit");
    console.log("an answer call: 'submitAnswer(clear_text, complete=function(){})'");
    console.log("where 'clear_text' is the decrypted message and 'complete' is");
    console.log("the callback that get's called if the decrypted message was correct");
    console.log("The answer is not case sensitive but punctuation must be");
    console.log("consistent. You need to provide 50 correct answers in a row within");
    console.log("the time limit or the game will reset. Good Luck!");
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
            stopTimer(display);
            rot(reload=true);
        }
    }, 1000);
}

function rot(reload=false) {
    if (rotEncryptedMessage.length && !reload) {
        openRotModal();
        return;
    }

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
                errorAlert(res.error, options={target: $("#rot-error")});
                return;
            }
            startTimer(res.remaining_time, $("#rot_timer"));

            // Reset some things
            rotNumToSolve = res.num_to_solve;
            rotNumSolved = res.num_solved;
            rotEncryptedMessage = res.encrypted_message;

            // Update the display and open the modal
            $("#num_to_solve").text(rotNumToSolve);
            $("#num_solved").text(rotNumSolved);
            $("#hackerBucks").text(res.hacker_bucks);
            $("#cipher-text").text(rotEncryptedMessage);
            openRotModal();
        }
    });
}

function rotSubmitAnswer(answer, callback=null) {
    if (!rotEncryptedMessage.length) {
        console.log("The encrypted message has not been retrieved yet.");
        console.log("Click on the 'ROT?' link and pay $25 to");
        console.log("start the challenge");
        return;
    } else if (typeof answer !== "string") {
        console.log("Answer must be a string");
        return;
    }

    $("#cleartext").val(answer);

    // Submit the answers
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

            rotNumSolved = res.num_solved;
            rotEncryptedMessage = res.encrypted_message;

            $("#num_solved").text(rotNumSolved);
            $("#cipher-text").text(rotEncryptedMessage);
            startTimer(res.remaining_time, $("#rot_timer"));

            if (!res.success) {
                if (res.error) {
                    errorAlert(res.error, options={
                        target: $("#rotModalFooter")
                    });
                } else {
                    errorAlert("Invalid answer", options={
                        target: $("#rotModalFooter")
                    });
                }
            } else if (res.flag) {
                console.log(res.flag);
                successAlert(res.flag, options={
                    target: $("#rotModalFooter"),
                    autoclose: 0
                });
            } else {
                if (callback) {
                    callback();
                }
            }
        }
    });
}