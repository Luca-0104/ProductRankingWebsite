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

    //if there are error messages in password1 input
    if ($(".error-message-password1").length > 0) {
         $(".label-input-blank-password1").addClass("label-input-blank-error");
         $(".label-input-blank-password1").css("color", "#ff0000");
    }

    //if there are error messages in password2 input
    if ($(".error-message-password2").length > 0) {
         $(".label-input-blank-password2").addClass("label-input-blank-error");
         $(".label-input-blank-password2").css("color", "#ff0000");
    }

    //if there are error messages in role input
    if ($(".error-message-role").length > 0) {
         $(".label-radio-group-role").addClass("label-input-blank-error");
         $(".label-radio-group-role").css("color", "#ff0000");
    }

});