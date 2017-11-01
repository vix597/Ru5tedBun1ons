//
// Methods to add alerts to the page and send ajax requests
//

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