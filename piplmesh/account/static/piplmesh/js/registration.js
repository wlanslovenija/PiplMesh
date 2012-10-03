$(document).ready(function () {
    $('#id_password1').blur(checkPassword);
    $('#id_password2').blur(checkPassword);

    $('#id_email').blur(checkEmail);
});

function checkPassword() {
    if ($('#id_password1').val() && $('#id_password2').val()) {
        if ($('#id_password1').val() == $('#id_password2').val()) {
            $('#id_password1').removeClass('input_invalid');
            $('#id_password2').removeClass('input_invalid');

            $('#password_info').remove();
        }
        else {
            var message_info = $('<span/>').attr({
                'id': 'password_info',
                'class': 'input_invalid_text'
            }).text(gettext("Passwords do not match."));

            $('#id_password1').addClass('input_invalid');
            $('#id_password2').addClass('input_invalid');

            if (!$('#password_info').length) {
                $('#id_password2').after(message_info);
            }

            $('#id_password1').unbind('keyup', checkPassword).unbind('change', checkPassword).keyup(checkPassword).change(checkPassword);
            $('#id_password2').unbind('keyup', checkPassword).unbind('change', checkPassword).keyup(checkPassword).change(checkPassword);
        }
    }
    else {
        $('#id_password1').removeClass('input_invalid');
        $('#id_password2').removeClass('input_invalid');
        $('#password_info').remove();
    }
}

function checkEmail() {
    // Source: http://jzaefferer.github.com/jquery-validation/jquery.validate.js
    var emailRegex = /^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))$/;

    if ($('#id_email').val()) {
        if (emailRegex.test($('#id_email').val())) {
            $('#id_email').removeClass('input_invalid');

            $('#email_info').remove();
        }
        else {
            var message_info = $('<span/>').attr({
                'id': 'email_info',
                'class': 'input_invalid_text'
            }).text(gettext("Invalid e-mail."));

            $('#id_email').addClass('input_invalid');

            if (!$('#email_info').length) {
                $('#id_email').after(message_info);
            }

            $('#id_email').unbind('keyup', checkEmail).unbind('change', checkEmail).keyup(checkEmail).change(checkEmail);
        }
    }
    else {
        $('#id_email').removeClass('input_invalid');
        $('#email_info').remove();
    }
}
