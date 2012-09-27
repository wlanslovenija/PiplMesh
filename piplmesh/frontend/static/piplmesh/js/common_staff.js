$(document).ready(function () {
    $('#id_locations').change(function (event) {
        $(this).closest('form').submit();
    });
});
