function howManyColumns() {
    var panelsWidth = $('#panels').width();
    var columnPanelsWidth = $('.panels_column').outerWidth() + parseInt($('.panels_column').css('margin-left'));

    return parseInt(panelsWidth / columnPanelsWidth);
}

function movePanel(id, columnIndex) {
    $('#' + id).appendTo($('#panels').children().eq(columnIndex));
}

function resetColumns() {
    $('#panels').children().each(function (index, column) {
        column.children().each(function (index, panel) {
            panel.appendTo($('#panels').children().eq(0))
        });
    });

    var count = 0;
    $('#panels').children().each(function (index, value) {
        if (count != 0)
            $(this).remove();
        count++;
    });
}

function initializeEmptyColumnsForPanels() {
    var currentColumns = $('#panels').children().length;
    var noOfColumns = howManyColumns();

    for (var i = currentColumns; i < noOfColumns; i++) {
        $('#panels').append('<div class="panels_column"></div>');
    }
}

function orderPanelsDefault() {
    var numOfPanels = $('.panels_column').children().length;
    var numOfColumns = howManyColumns();

    for (var i = 0; i < numOfPanels; i++) {
        var toColumn = i % numOfColumns;
        $('.panels_column').children().eq(numOfPanels - i - 1).appendTo($('#panels').children().eq(toColumn));
    }
}

function orderPanelsUpdate() {
    var items = [];

    $('#panels').children().each(function (index, value) {
        var column = [];
        $(this).children().each(function (index, value) {
            var item = {
                id: $(this).prop('id'),
            };
            column.push(item);
        });
        items.push(column);
    });

    $.post(urls['panels_order'], 'data=' + JSON.stringify({panels: items}));
}

function orderPanels() {
    $.post(urls['get_panels_order'], 'data=' + JSON.stringify( {noOfColumns: howManyColumns()} ), function (data) {
        if (data['panels'].length == 0) {
            orderPanelsDefault();
        } else {
            for (var i = 0; i < data['panels'].length; i++) {
                for (var j = 0; j < data['panels'][i].length; j++) {
                    movePanel(data['panels'][i][j]['id'],i);
                }
            }
        }
    });
}

function collapsePanels() {
    $.get(urls['get_panels_collapse'], function (data) {
        $.each(data, function (panelId, collapsed) {
            if (collapsed == true) {
                $('#' + panelId + ' .content').css('display', 'none');
            }
        });
    });
}

function preparePanels() {
    initializeEmptyColumnsForPanels();
    orderPanels();
    collapsePanels();
    makeColumnsSortable();
    makePanelsUpdatable();
}

function makeColumnsSortable() {
    $('.panels_column').sortable({
        connectWith: '.panels_column',
        handle: '',
        cursor: 'move',
        placeholder: 'placeholder',
        forcePlaceholderSize: true,
        opacity: 0.6
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

        var panel_id = $(this).parent().attr('id');
        var collapsed =  visible ? true : false;

        $.post(urls['panels_collapse'], 'data=' + JSON.stringify( {panel_id: panel_id, collapsed: collapsed }));
    });

    $(window).resize(function () {
        resetColumns();
        preparePanels();
    });
});