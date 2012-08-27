$(document).ready(function () {
    $('.drop_down_login_container').hover(
        function () {
            $('.drop_down_login_options').show();
        },
        function () {
            $('.drop_down_login_options').hide();
        }
    )
});