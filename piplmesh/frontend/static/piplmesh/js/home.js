$(document).ready(function () {
    $('.panel .header').click(function (event) {
        $(this).next('.content').slideToggle('fast');
    });
    
    $('button.auth_button').click(function (event) {
    	navigator.id.logout();
    });
});
