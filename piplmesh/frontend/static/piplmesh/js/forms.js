$(document).ready(function () {
    var max = 0;
    $('label').each(function () {
        if ($(this).width() > max)
            max = $(this).width();
    });
    $('label').width(max);
    $('.automatic-width').css({ 'margin-left': max });
});
