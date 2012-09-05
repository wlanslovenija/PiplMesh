function howManyColumns() {
    var panelsWidth = $('#panels').width();
    var columnPanelsWidth = $('.panels_column').outerWidth();

    return parseInt(panelsWidth / columnPanelsWidth);
}

function movePanel(id, columnIndex) {
    $('#' + id).appendTo($('#panels').children().eq(columnIndex));
}

function initializeEmptyColumnsForPanels() {
    var currentColumns = $('#panels').children().length;
    var numberOfColumns = howManyColumns();

    for (var i = currentColumns; i < numberOfColumns; i++) {
        var newColumn = $('<div/>');
        newColumn.addClass('panels_column');
        $('#panels').append(newColumn);
    }
}

function orderPanelsDefault() {
    var numberOfColumns = howManyColumns();

    $('.panel').each(function (index, panel) {
        var toColumn = index % numberOfColumns;
        var columns = $('#panels').children();

        $(panel).appendTo(columns.eq(toColumn));
    });
}

function sendOrderOfPanelsToServer() {
    var order = [];

    $('#panels').children().each(function (index, column) {
        var columnArray = [];
        $(column).children().each(function (index, panel) {
            columnArray.push($(panel).prop('id'));
        })
        order.push(columnArray);
    })

    $.ajax({
        type: 'POST',
        url: urls['panels_order'],
        data: {
            'order': JSON.stringify(order),
            'number_of_columns': howManyColumns()
        }
    });
}

function orderPanels() {
    $.ajax({
        type: 'GET',
        url: urls['panels_order'],
        data: {'numberOfColumns': howManyColumns()},
        success: function (data) {
            if (data['panels'].length == 0) {
                orderPanelsDefault();
            }
            else {
                for (var i = 0; i < data['panels'].length; i++) {
                    for (var j = 0; j < data['panels'][i].length; j++) {
                        movePanel(data['panels'][i][j], i);
                    }
                }
            }
        }
    });
}

function collapsePanels() {
    $.get(urls['panels_collapse'], function (data) {
        $.each(data, function (panelId, collapsed) {
            if (collapsed) {
                $('#' + panelId + ' .content').css('display', 'none');
            }
        });
    });
}

function initializePanels() {
    $('.panels').detach();

    initializeEmptyColumnsForPanels();
    orderPanels();
    collapsePanels();
    makeColumnsSortable();
    makePanelsOrderUpdatable();
}

function makeColumnsSortable() {
    $('.panels_column').sortable({
        'connectWith': '.panels_column',
        'handle': '',
        'cursor': 'move',
        'placeholder': 'placeholder',
        'forcePlaceholderSize': true,
        'opacity': 0.6,
        'helper': 'clone'
    }).disableSelection();
}

function makePanelsOrderUpdatable() {
    $('.panels_column').bind('sortstop', function (event, ui) {
        sendOrderOfPanelsToServer();
    });
}

$(document).ready(function () {
    initializePanels();

    $('.panel .header').click(function (event) {
        var visible = $(this).next().is(':visible');
        $(this).next('.content').slideToggle('fast');

        var panel_id = $(this).parent().attr('id');
        var collapsed =  visible ? true : false;

        $.ajax({
            type: "POST",
            url: urls['panels_collapse'],
            data: {'panel_id': panel_id, 'collapsed': collapsed}
        });
    });

    $(window).resize(function () {
        initializePanels();
    });
});