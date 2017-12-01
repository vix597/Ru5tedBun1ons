
function openPaidContentModal() {
    var session_id = localStorage.getItem("session_id");

    $("#paidContentButton").text("Paid Content");
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
    var session_id = localStorage.getItem("session_id");

    if (localStorage.getItem("paidContentChallengePurchased")) {
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
                errorAlert(res.error);
                return;
            }

            $("#hackerBucks").text(res.hacker_bucks);
            localStorage.setItem("paidContentChallengePurchased", true);
            openPaidContentModal();
        }
    });
}