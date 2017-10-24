$(document).ready(function() {
    // NOTE: Change flag before deploy
    console.log("Does anyone look at the console? Flag={__PLACEHOLDER_FLAG__}");

    if (pageError) {
        localStorage.clear();
    } else {
        session_id = localStorage.getItem("session_id")
        if (session_id) {
            window.location = "/crapdb/main/" + session_id + "/";
        }
    }
});