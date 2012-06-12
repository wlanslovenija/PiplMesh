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

function collapsePanels() {
    $.get('/panels/collapse/get', function (data) {
        for (var panel in data) {
            if (data[panel] == true)
                $('#'+ panel +' .content').css('display','none');
        }
    });
}

function getColumnsPanelsOrder() {
    var json = {};
    var i = 0;
    $('#panels').children().each( function () {
        var j = 0;
        var column = {};
        $(this).children().each( function () {
            column[j] = $(this).attr('id');
            j++;
        })
        json[i] = column;
        i++;
    });
    
    console.log(json);
    return json;
}

$(document).ready(function () {
    var numberOfColumns = howManyColumns();
    collapsePanels();
    fillWithColumns();
    defaultPanelsOrder();

    $('.panel .header').click(function (event) {
        var visible = $(this).next().is(':visible');
        $(this).next('.content').slideToggle('fast');
        
        if (visible) {
            var param = 1;
        } else {
            var param = 0;
        }
        
        $.get('/panels/collapse/' + $(this).parent().attr('id') + '/' + param, function (data) {
            console.log(data);
        });
    });

    $('.panels_column').sortable({
        connectWith: '.panels_column',
        handle: '',
        cursor: 'move',
        placeholder: 'placeholder',
        forcePlaceholderSize: true,
        opacity: 0.4,
    }).disableSelection();

    $('.panels_column').bind("sortstop", function (event, ui) {
        var json2 = getColumnsPanelsOrder();
        $.ajax({
            type: "GET",
            url: "/panels/order/1",
            data: JSON.stringify(json2),
            success: function(data) {
                console.log(data);
            },
        });
    });
});
