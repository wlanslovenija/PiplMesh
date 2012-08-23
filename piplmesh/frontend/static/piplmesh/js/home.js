function howManyColumns() {
    var panelsWidth = $('#panels').width();
    var columnPanelsWidth = $('.panels_column').width() + parseInt($('.panels_column').css('margin-left'));

    return parseInt(panelsWidth / columnPanelsWidth);
}

function movePanel(id, columnIndex) {
    $('#' + id).appendTo($('#panels').children().eq(columnIndex));
}

function resetColumns() {
    $('#panels').children().each(function (index, value) {
        $(this).children().each(function (index, value) {
            $(this).appendTo($('#panels').children().eq(0))
        });
    });

    var count = 0;
    $('#panels').children().each(function (index, value) {
        if (count != 0)
            $(this).remove();
        count++;
    });
}

function fillWithColumns() {
    var currentColumns = $('#panels').children().length;
    var noOfColumns = howManyColumns();

    for (i = currentColumns; i < noOfColumns; i++) {
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
                id: $(this).attr('id'),
            };
            column.push(item);
        });
        items.push(column);
    });

    $.post(urls['panels_order'], 'data=' + JSON.stringify({panels: items}));
}

function orderPanels() {
    $.post(urls['get_panels_order'], 'data=' + JSON.stringify( {noOfColumns: howManyColumns()} ), function (data) {
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
    $.get(urls['get_panels_collapse'],'/panels/collapse/get/', function (data) {
        for (var panel in data) {
            if (data[panel] == true)
                $('#'+ panel +' .content').css('display','none');
        }
    });
}

function preparePanels() {
    fillWithColumns();
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
        $.post(urls['panels_collapse'], 'data=' + JSON.stringify( {panel_id: $(this).parent().attr('id'), collapsed: (visible) ? true : false }));
    });

    $(window).resize(function () {
        resetColumns();
        preparePanels();
    });
});

$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});
