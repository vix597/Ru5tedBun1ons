var geneticLastScore = 0;
var geneticPurchased = false;

function printGeneticWelcome() {
    setPurchasedChallenge("genetic");
    $("#geneticModal").modal({show: true});

    console.log("");
}

function geneticGenes() {
    if (geneticPurchased) {
        printGeneticWelcome();
        return;
    }

    $.ajax({
        url: "/crapdb/genetic/" + session_id + "/",
        type: "GET",
        success: function(data) {
            var res = JSON.parse(data);
            console.log("Res: ", res);
            if (res.redirect) {
                window.location = "/crapdb/?error=" + encodeURIComponent(res.redirect);
                return;
            } else if (res.error) {
                errorAlert(res.error, options={target: $("#genetic-error")});
                return;
            } 

            // Update the hacker bucks
            $("#hackerBucks").text(res.hacker_bucks);

            geneticPurchased = true;
            printGeneticWelcome();
        }
    });
}

function submitGeneticPassword(password, cb=null, display_alert=false) {
    if (!geneticPurchased) {
        console.log("This challenge has not been purchased. Purchase it first");
        return;
    }

    $("#geneticPassword").val(password);

    $.ajax({
        url: "/crapdb/geneticflag/" + session_id + "/",
        type: "POST",
        data: {
            answer: password,
            csrfmiddlewaretoken: csrf_token
        },
        success: function(data) {
            res = JSON.parse(data);
            if (res.flag) {
                successAlert(res.flag, options={
                    target:$("#geneticModalFooter"),
                    autoclose: 0
                });
            } else if (res.error) {
                errorAlert(res.error, options={
                    target: $("#geneticModalFooter")
                });
            } else {
                if (display_alert) {
                    errorAlert("Invalid Password", options={
                        target: $("#geneticModalFooter")
                    });
                }

                geneticLastScore = res.score
                if (cb) {
                    cb(geneticLastScore);
                }
            }
        }
    });
}