function howManyColumns() {
    var panelsWidth = $('#panels').width();
    var columnPanelsWidth = $('.panels_column').width() + parseInt($('.panels_column').css('margin-left'));

    return parseInt(panelsWidth / columnPanelsWidth);
}

function fillWithColumns() {
    var currentColumns = $('#panels').children().length;

    for(i = currentColumns; i < howManyColumns(); i++) {
        $('#panels').append('<div class="panels_column"></div>');
    }
}

function defaultPanelsOrder() {
    var num_of_panels = $('.panels_column').children().length;
    var num_of_columns = howManyColumns();
    
    for (i=0; i < num_of_panels; i++) {
        var toPanel = i % num_of_columns;
        $('.panels_column').children().eq(num_of_panels-i-1).appendTo($('#panels').children().eq(toPanel));
    }
}

$(document).ready(function () {
    fillWithColumns();
    
    defaultPanelsOrder();    
    //$('.panels_column').children().eq(2).appendTo($('#panels').children().eq(howManyColumns() - 1));
    
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
