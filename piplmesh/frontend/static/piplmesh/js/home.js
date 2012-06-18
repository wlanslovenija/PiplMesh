function howManyColumns() {
    var panelsWidth = $('#panels').width();
    var columnPanelsWidth = $('.panels_column').width() + parseInt($('.panels_column').css('margin-left'));
    
    var noOfColumns = parseInt(panelsWidth / columnPanelsWidth);
    
    return noOfColumns > 0 ? noOfColumns:1;
}

function movePanel(id, columnId) {
    $('#'+id).appendTo($('#panels').children().eq(columnId));
}

function resetColumns() {
    $('#panels').children().each(function () {
        $(this).children().each( function () {
            $(this).appendTo($('#panels').children().eq(0))
        });
    });
    
    var count = 0;
    $('#panels').children().each(function () {
        if (count != 0)
            $(this).remove();
        count++;
    });
}

function fillWithColumns() {
    var currentColumns = $('#panels').children().length;

    for(i = currentColumns; i < howManyColumns(); i++) {
        $('#panels').append('<div class="panels_column"></div>');
    }
}

function orderPanelsDefault() {
    var num_of_panels = $('.panels_column').children().length;
    var num_of_columns = howManyColumns();

    for (i=0; i < num_of_panels; i++) {
        var toColumn     = i % num_of_columns;
        $('.panels_column').children().eq(num_of_panels-i-1).appendTo($('#panels').children().eq(toColumn));
    }
}

function orderPanelsUpdate() {
    var items = [];
    
    $('#panels').children().each(function () {
        var column = [];
        $(this).children().each( function () {
            var item = {
                id: $(this).attr('id'),
            };
            column.push(item);
        });
        items.push(column);
    });
    
    $.get('/panels/order/', 'data=' + JSON.stringify( {panels: items} ));
}

function orderPanels() {
    $.get('/panels/order/get', 'data=' + JSON.stringify( {noOfColumns: howManyColumns()} ), function (data) {
        for (var i = 0; i < data['panels'].length; i++) {
            for (var j = 0; j < data['panels'][i].length; j++) {
                movePanel(data['panels'][i][j]['id'],i);
            }
        }
        
        if (data['panels'].length == 0) {
            orderPanelsDefault();
        }
    });
}

function collapsePanels() {
    $.get('/panels/collapse/get', function (data) {
        for (var panel in data) {
            if (data[panel] == true)
                $('#'+ panel +' .content').css('display','none');
        }
    });
}

function preparePanels() {
    $('#panels').css('visibility', 'hidden');
    
    $('#spinner').css('left', '30%');
    $('#spinner').css('top', '100px');
    $('#spinner').show();

    fillWithColumns();
    orderPanels();
    collapsePanels();
    makeColumnsSortable();
    makePanelsUpdatable();

    setTimeout('hideSpinner()', 800);
}

function hideSpinner() {
    $('#spinner').hide();
    $('#panels').css('visibility', 'visible');
}

function makeColumnsSortable() {
    $('.panels_column').sortable({
        connectWith: '.panels_column',
        handle: '',
        cursor: 'move',
        placeholder: 'placeholder',
        forcePlaceholderSize: true,
        opacity: 0.6,
    }).disableSelection();
}

function makePanelsUpdatable() {
    $('.panels_column').bind("sortstop", function (event, ui) {
        orderPanelsUpdate();
    });
}

$(document).ready(function () {
    preparePanels();

    $('.panel .header').click(function (event) {
        var visible = $(this).next().is(':visible');
        $(this).next('.content').slideToggle('fast');
        
        if (visible) {
            var param = "1";
        } else {
            var param = "0";
        }
        
        $.get('/panels/collapse/', 'data=' + JSON.stringify( {panel_id: $(this).parent().attr('id'), collapsed: param}));
    });

    $(window).resize(function () {
        $('#panels').css('visibility', 'hidden');
        resetColumns();
        preparePanels();
    });
});