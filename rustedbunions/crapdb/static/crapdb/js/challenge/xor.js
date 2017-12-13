var cipherText = "";

function openXorModal() {
    setPurchasedChallenge("xor");
    $("#xorModal").modal({show: true});
}

function xor() {
    if (cipherText.length) {
        openXorModal();
        return;
    }

    $.ajax({
        url: "/crapdb/xor/" + session_id + "/",
        type: "GET",
        success: function(data) {
            var res = JSON.parse(data);
            console.log("Res: ", res);
            if (res.redirect) {
                window.location = "/crapdb/?error=" + encodeURIComponent(res.redirect);
                return;
            } else if (res.error) {
                errorAlert(res.error, options={target: $("#xor-error")});
                return;
            }

            // Update the hacker bucks
            $("#hackerBucks").text(res.hacker_bucks);

            cipherText = res.cipher_text;
            $("#xorCipherText").val(cipherText);
            openXorModal();
        }
    });
}

function xorSubmitAnswer(passphrase) {
    $.ajax({
        url: "/crapdb/xorflag/" + session_id + "/",
        type: "POST",
        data: {
            answer: passphrase,
            csrfmiddlewaretoken: csrf_token
        },
        success: function(data) {
            var res = JSON.parse(data);
            console.log("Res: ", res);
            if (res.redirect) {
                window.location = "/crapdb/?error=" + encodeURIComponent(res.redirect);
                return;
            } else if (res.error) {
                errorAlert(res.error, options={
                    target: $("#xorModalFooter")
                });
            } else if (res.flag) {
                successAlert(res.flag, options={
                    target: $("#xorModalFooter"),
                    autoclose: 0
                });
            }
        }
    });
}