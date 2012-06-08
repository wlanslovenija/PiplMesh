$(document).ready(function () {
    $('#id_password2').keyup(checkPassword).change(checkPassword);
    $('#id_email').keyup(checkEmail).change(checkEmail);
});

function checkPassword() {
    $('#id_password1').keyup(checkPassword).change(checkPassword);

    if ($('#id_password1').val() == $('#id_password2').val()) {
        $('#id_password1').removeClass('input_valid input_invalid').addClass('input_valid');
        $('#id_password2').removeClass('input_valid input_invalid').addClass('input_valid');
        $("#password_info").remove();
    }
    else {
        $('#id_password1').removeClass('input_valid input_invalid').addClass('input_invalid');
        $('#id_password2').removeClass('input_valid input_invalid').addClass('input_invalid');
        $("#password_info").remove();
        var password_invalid_message = gettext('Please re-enter your password.');
        $("#id_password2").after('<span id="password_info" class="input_invalid">' + password_invalid_message + '</span>');
    }
}

function checkEmail() {
    // Source: http://jzaefferer.github.com/jquery-validation/jquery.validate.js
    var emailRegex = /^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))$/;

    if (emailRegex.test($('#id_email').val())) {
        $('#id_email').removeClass('input_valid input_invalid').addClass('input_valid');
    }
    else {
        $('#id_email').removeClass('input_valid input_invalid').addClass('input_invalid');
    }
}
