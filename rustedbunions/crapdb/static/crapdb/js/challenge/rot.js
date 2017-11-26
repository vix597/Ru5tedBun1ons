
// Stores the interval ID for the startTimer() method
var rotTimerItervalId = null;
var rotSolved = [];
var rotNumSolved = 0;
var rotNumToSolve = 0;
var rotEncryptedMessages = [];
var rotMessageHashes = [];
var rotCurrentCipher = "";

function openRotModal() {
    $("#rotButton").text("ROT?");
    $("#rotModal").modal({show: true});

    console.log("Welcome to the ROT challenge.");
    console.log("Using the console, an answer can be submitted. The current message");
    console.log("to decrypt is stored in the 'rotCurrentCipher' variable. Using that");
    console.log("variable, decrypt the message and call 'rotSubmitAnswer(clear_text)'");
    console.log("where 'clear_text' is the decrypted message. The method returns true");
    console.log("on success and false on failure. Repeat 50 times and on the 50th success");
    console.log("a flag will be displayed on the screen and in the console. You have 60")
    console.log("seconds before the game resets with a new random list of messages.");
    console.log("HINT: The ROT key is random for each message.")
    console.log("Good Luck!");
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
            rot(reload=true);
        }
    }, 1000);
}

function rot(reload=false) {
    var session_id = localStorage.getItem("session_id");

    if (rotEncryptedMessages.length && !reload) {
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
                errorAlert(res.error);
                return;
            }
            startTimer(res.remaining_time, $("#rot_timer"));

            // Reset some things
            rotNumToSolve = res.num_to_solve;
            rotNumSolved = 0;
            rotSolved = [];
            rotEncryptedMessages = res.encrypted_messages;
            rotMessageHashes = res.message_hashes;
            rotCurrentCipher = rotEncryptedMessages[rotNumSolved];

            // Update the display and open the modal
            $("#num_to_solve").text(rotNumToSolve);
            $("#num_solved").text(rotNumSolved);
            $("#hackerBucks").text(res.hacker_bucks);
            $("#cipher-text").text(rotCurrentCipher);
            openRotModal();
        }
    });
}

function rotSubmitAnswer(answer) {
    if (!rotEncryptedMessages.length) {
        console.log("The encrypted messages have not been retrieved yet.");
        console.log("Click on the 'ROT?' link and pay $25 to");
        console.log("start the challenge");
        return false;
    } else if (typeof answer !== "string") {
        console.log("Answer must be a string");
        return false;
    } 

    $("#cleartext").val(answer);

    checkHash = rotMessageHashes[rotNumSolved];
    answerHash = sha256(answer);
    if (checkHash === answerHash) {
        rotNumSolved += 1;
        rotSolved.push(answer);
        rotCurrentCipher = rotEncryptedMessages[rotNumSolved];

        $("#num_solved").text(rotNumSolved);
        $("#cipher-text").text(rotCurrentCipher);
    } else {
        return false;
    }

    if (rotNumSolved >= rotNumToSolve) {
        var session_id = localStorage.getItem("session_id");
        var csrf_token = localStorage.getItem("csrf_token");

        // Submit the answers
        $.ajax({
            url: "/crapdb/rotflag/" + session_id + "/",
            type: "POST",
            data: {
                answer: JSON.stringify(rotSolved),
                csrfmiddlewaretoken: csrf_token
            },
            success: function(data) {
                res = JSON.parse(data);
                console.log("Result: ", res);
                if (!res.success) {
                    rotNumSolved = 0;
                    rotSolved = [];
                    $("#num_solved").text(rotNumSolved);
                    $("#cipher-text").text(rotEncryptedMessages[rotNumSolved]);

                    if (res.error) {
                        errorAlert(res.error, options={
                            target: $("#rotModalFooter")
                        });
                    } else {
                        errorAlert("Invalid answers", options={
                            target: $("#rotModalFooter")
                        });
                    }
                } else {
                    console.log(res.flag);
                    successAlert(res.flag, options={
                        target: $("#rotModalFooter"),
                        autoclose: 0
                    });
                }
            }
        });
    }

    return true;
}