var paidContentChallengePurchased = false;


function openPaidContentModal() {
    setPurchasedChallenge("paid_content");
    $("#paidContentModal").modal({show: true});

    $.ajax({
        url: "/crapdb/paidcontentflag/" + session_id + "/",
        type: "GET",
        success: function(data) {
            var res = JSON.parse(data);
            console.log("Res: ", res);

            if (res.flag) {
                $("#paidContentModalBody").text(res.flag);
            }
        }
    });
}

function paidContent() {
    if (paidContentChallengePurchased) {
        openPaidContentModal();
        return;
    }

    $.ajax({
        url: "/crapdb/paidcontent/" + session_id + "/",
        type: "GET",
        success: function(data) {
            var res = JSON.parse(data);
            console.log("Res: ", res);
            if (res.redirect) {
                window.location = "/crapdb/?error=" + encodeURIComponent(res.redirect);
                return;
            } else if (res.error) {
                errorAlert(res.error, options={target: $("#paid_content-error")});
                return;
            }

            $("#hackerBucks").text(res.hacker_bucks);
            paidContentChallengePurchased = true;
            openPaidContentModal();
        }
    });
}