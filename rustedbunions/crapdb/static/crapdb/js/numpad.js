
var pin_hash = null;

function numpadChallenge(session_id) {
    $("#numpadModal").modal({show: true});

    $.ajax({
        url: "/crapdb/getpin/" + session_id + "/",
        type: "GET",
        success: function(data) {
            var res = JSON.parse(data);
            if (res.redirect) {
                window.location = "/crapdb/?error=" + encodeURIComponent(res.redirect);
                return;
            }
            pin_hash = res.pin_hash;

            console.log("Welcome to the number pad challenge.");
            console.log("Using the console, a PIN can be submitted");
            console.log("by calling 'submitPin(pin_number)' where");
            console.log("'pin_number' is the user's pin. The function");
            console.log("will return 'true' on success and 'false' on");
            console.log("failure. Good luck!");
        }
    });
}

function submitPin(pin_number) {
    var result = md5(pin_number);
    if (result == pin_hash) {
        console.log("User's pin is: ", pin_number);
        return true;
    }
    return false;
}