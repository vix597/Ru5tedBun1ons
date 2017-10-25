
function printWelcome() {
    $("#numpadButton").text("Brutal Force");
    $("#numpadModal").modal({show: true});

    console.log("Welcome to the brutal force challenge.");
    console.log("Using the console, a PIN can be submitted");
    console.log("by calling 'submitPin(pin_number)' where");
    console.log("'pin_number' is the user's pin. The function");
    console.log("will return 'true' on success and 'false' on");
    console.log("failure. Good luck!");
}

function brutalForce(session_id) {
    var pin_hash = localStorage.getItem("pin_hash");
    if (pin_hash) {
        printWelcome();
        return;
    }

    $.ajax({
        url: "/crapdb/getpin/" + session_id + "/",
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

            // Update the hacker bucks
            $("#hackerBucks").text(res.hacker_bucks);

            localStorage.setItem("pin_hash", res.pin_hash);
            printWelcome();
        }
    });
}

function submitPin(pin_number, display_alert=false) {
    var pin_hash = localStorage.getItem("pin_hash");
    if (!pin_hash) {
        console.log("The user's PIN hash has not been retrieved yet.");
        console.log("Click on the 'Burtal Force' link and pay $15 to");
        console.log("retrieve the hash");
        return false;
    }

    $("#testpin").val(pin_number);

    var result = md5(pin_number);
    if (result == pin_hash) {
        var session_id = localStorage.getItem("session_id");
        var csrf_token = localStorage.getItem("csrf_token");

        // Print the PIN
        console.log("User's pin is: ", pin_number);

        // Check and make sure we're good
        $.ajax({
            url: "/crapdb/getpinflag/" + session_id + "/",
            type: "POST",
            data: {
                pin: pin_number,
                csrfmiddlewaretoken: csrf_token
            },
            success: function(data) {
                res = JSON.parse(data);
                if (res.error) {
                    errorAlert(res.error, target=$("#numpadModalFooter"));
                }

                successAlert(res.flag, target=$("#numpadModalFooter"), prepend=true, autoclose=0);
            }
        });
        return true;
    }

    if (display_alert) {
        errorAlert("Invalid PIN", target=$("#numpadModalFooter"), prepend=true, autoclose=1500);
    }

    return false;
}