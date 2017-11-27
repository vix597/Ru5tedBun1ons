//
// Methods to add alerts to the page and send ajax requests
//

var unauth_session_oid = undefined;
var csrf_token = undefined;

function bootstrapAlert(msg, options={}) {
    var defaults = {
        target:$(".blog-header"),
        prepend: true,
        autoclose: 4000,
        cls: "alert-danger"
    }

    var actual = $.extend({}, defaults, options || {});
    options = actual;
    
    var alert = $("<div class='alert alert-dismissible fade show' role='alert'>")
        .addClass(options.cls)
        .text(msg)
        .append($("<button type='button' class='close' data-dismiss='alert' aria-label='Close'>")
            .append($("<span aria-hidden='true'>").html("&times;")));

    var bootstrap_alert = false;
    if (options.prepend && (typeof options.target.prepend === "function")) {
        options.target.prepend(alert);
        bootstrap_alert = true;
    } else if (typeof options.target.append === "function") {
        options.target.append(alert);
        bootstrap_alert = true;
    } else {
        // Nothing is going to work so just trigger the default alert
        alert(msg);
    }

    if (bootstrap_alert) {
        alert.alert();
        
        if (options.autoclose) {
            setTimeout(function() {
                alert.alert('close');
            }, options.autoclose);
        }
    }
}

function errorAlert(error, options={}) {
    bootstrapAlert(error, options=options);
}

function successAlert(msg, options={}) {
    options.cls = "alert-success";
    bootstrapAlert(msg, options=options);
}

function testFlag() {
    var session_id = unauth_session_oid;
    var token = csrf_token;

    if (!session_id) {
        session_id = localStorage.getItem("session_id");
    }

    if (!token) {
        token = localStorage.getItem("csrf_token");
    }

    var flag = $("#testflag").val();
    $("#testflag").val("");

    var url = null;
    if (unauth_session_oid) {
        url = "/core/checkflag/" + session_id + "/";
    } else {
        url = "/crapdb/checkflag/" + session_id + "/";
    }

    $.ajax({
        url: url,
        type: "POST",
        data: {
            flag: flag,
            csrfmiddlewaretoken: token
        },
        success: function(res) {
            res = JSON.parse(res);
            if (res.redirect) {
                window.location = "/crapdb/?error=" + encodeURIComponent(res.redirect);
            }

            if (res.hacker_bucks) {
                if (res.error) {
                    var hackerBucks = res.hacker_bucks;
                    $("#hackerBucks").text(res.error);
                    setTimeout(function() {
                        $("#hackerBucks").text(hackerBucks);
                    }, 1000);
                } else {
                    $("#hackerBucks").text(res.hacker_bucks);
                }
            }
        }
    });
}