$(document).ready(function () {

    //if there are error messages in username input
    if ($(".error-message-username").length > 0) {
        $(".label-input-blank-username").addClass("label-input-blank-error");
        $(".label-input-blank-username").css("color", "#ff0000");
    }

    //if there are error messages in email input
    if ($(".error-message-email").length > 0) {
        $(".label-input-blank-email").addClass("label-input-blank-error");
        $(".label-input-blank-email").css("color", "#ff0000");
    }
});