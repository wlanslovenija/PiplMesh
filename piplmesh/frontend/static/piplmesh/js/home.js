$(document).ready(function () {
    $('.panel .header').click(function (event) {
        $(this).next('.content').slideToggle('fast');
    });
});
