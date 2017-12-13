// This prevents the user from ever accessing the modal
// Impossible to bypass this
var authorized = false;

function superAdmin() {
    if (authorized) {
        $.ajax({
            url: "/crapdb/superadmin/" + session_id + "/",
            type: "GET",
            success: function(data) {
                var res = JSON.parse(data);
                if (res.redirect) {
                    window.location = "/crapdb/?error=" + encodeURIComponent(res.redirect);
                    return;
                }

                $("#superAdminModalBody").text(res.flag);
                $("#superAdminModal").modal({show: true});
            }
        });
    } else {
        errorAlert(
            "Javascript validation failed. You are not super admin. authorized=" + authorized,
            options={target: $("#super_admin-error")}
        );
    }
}