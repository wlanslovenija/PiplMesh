$(document).ready(function () {
    $('.panel .header').click(function (event) {
        $(this).next('.content').slideToggle('fast');
    });

    $('.panels_column').sortable({
        connectWith: '.panels_column',
        handle: '',
        cursor: 'move',
        placeholder: 'placeholder',
        forcePlaceholderSize: true,
        opacity: 0.4,
    }).disableSelection();

});
