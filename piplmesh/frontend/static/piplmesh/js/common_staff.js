$(document).ready(function () {
    // Locations
    $('#id_locations').change(function (event) {
        $(this).closest('form').submit();
    });

});
