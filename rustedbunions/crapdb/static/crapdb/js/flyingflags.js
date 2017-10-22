//
// CSS3 is also a pretty cool guy
//

function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);

    //The maximum is exclusive and the minimum is inclusive
    return Math.floor(Math.random() * (max - min)) + min;
}

function popThoseFlags(flags) {
    var height = window.innerHeight;
    var width = window.innerWidth;
    var font_size = 24;

    for (var flag of flags) {
        var chars = flag.length;
        var flag_width = chars * font_size;

        var f = $("<p class='pop-text'>")
            .text(flag)
            .css("font", font_size + "px arial")
            .css("top", getRandomInt(0, (height - font_size)) + "px")
            .css("left", getRandomInt(0, (width - flag_width)) + "px")
            .css("-webkit-animation-delay", getRandomInt(0, 1500) + "ms")
            .css("animation-delay", getRandomInt(0, 1500) + "ms");

        $("body").append(f);
    }
}

function flagsForDays(session_id, csrf_token) {
    query = "SELECT flag from flags";

    // Load the flags
    $.ajax({
        url: "/crapdb/querydb/" + session_id + "/",
        type: "POST",
        data: {
            query: query,
            csrfmiddlewaretoken: csrf_token
        },
        success: function(res) {
            var res = JSON.parse(res);
            if (res.error) {
                console.log("Query DB error: ", res.error);
            } else if (res.flags && res.flags.length) {
                setInterval(function() {
                    popThoseFlags(res.flags);
                }, 1500);
            } else {
                console.log("No flags returned from query")
            }
        }
    });
}
