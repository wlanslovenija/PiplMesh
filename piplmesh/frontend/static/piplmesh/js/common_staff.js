$(document).ready(function () {
    $('#id_location').change(function (event) {
        $(this).closest('form').submit();
    });
});
