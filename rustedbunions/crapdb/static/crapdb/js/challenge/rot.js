
function openRotModal() {
    $("#rotButton").text("ROT?");
    $("#rotModal").modal({show: true});
}

function rot(session_id) {
    var encrypted_message = localStorage.getItem("encrypted_message");
    if (encrypted_message) {
        openRotModal();
        return;
    }

    $.ajax({
        url: "/crapdb/getencmsg/" + session_id + "/",
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
            $("#cipher-text").text(res.encrypted_message);
            localStorage.setItem("encrypted_message", res.encrypted_message);
            openRotModal();
        }
    });
}

function submitAnswer(answer) {
    var encrypted_message = localStorage.getItem("encrypted_message");
    if (!encrypted_message) {
        console.log("The encrypted message has not been retrieved yet.");
        console.log("Click on the 'ROT?' link and pay $50 to");
        console.log("start the challenge");
        return false;
    }

    $("#cleartext").val(answer);

    var session_id = localStorage.getItem("session_id");
    var csrf_token = localStorage.getItem("csrf_token");

    // Check and make sure we're good
    $.ajax({
        url: "/crapdb/getrotflag/" + session_id + "/",
        type: "POST",
        data: {
            answer: answer,
            csrfmiddlewaretoken: csrf_token
        },
        success: function(data) {
            res = JSON.parse(data);
            if (res.error) {
                console.log(res.error);
                errorAlert(res.error, target=$("#rotModalFooter"));
                return;
            }

            console.log(res.flag);
            successAlert(res.flag, target=$("#rotModalFooter"), prepend=true, autoclose=0);
        }
    });
}