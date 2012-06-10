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

$(document).ready(function () {


    fillWithColumns();
    
    
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
