$(document).ready(function () {
    $.ajaxSetup({
        'timeout': 5000,
        'traditional': true
    });

    $(document).ajaxError(function (event, jqXHR, ajaxSettings, thrownError) {
        window.console.error(event, jqXHR, ajaxSettings, thrownError);
        alert(gettext("Oops, something went wrong..."));
    });

    $('.logout_button').click(function (event) {
        navigator.id.logout();
    });

    $('.drop_down_login_container').hover(
        function () {
            $('.drop_down_login_options').show();
        },
        function () {
            $('.drop_down_login_options').hide();
        }
    );
});
