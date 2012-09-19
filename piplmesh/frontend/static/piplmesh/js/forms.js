$(document).ready(function () {
    var max = 0;
    $('.field label.main').each(function () {
        if ($(this).width() > max)
            max = $(this).width();
    });
    $('.field label.main').width(max);
    $('.align_to_label_width').css('margin-left', max );
});
