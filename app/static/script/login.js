$(document).ready(function () {

    //if there are error messages in email input
    if ($(".error-message-email").length > 0) {
        // $(".hint-label-email").css("color", "#ff0000");
         $(".hint-label-email").addClass("hint-label-error");
    }

    //if there are error messages in password input
    if ($(".error-message-password").length > 0) {
        // $(".hint-label-password").css("color", "#ff0000");
         $(".hint-label-password").addClass("hint-label-error");
    }


});