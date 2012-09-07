$(document).ready(function () {
    $('#browserid_submit').submit(function (event) {
        $(this).parent().submit();
    });
});