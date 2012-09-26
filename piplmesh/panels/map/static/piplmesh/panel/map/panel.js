$(document).ready(function () {
    var node_location;
    var map_controls;
    var map;
    var node_name = $('<p/>').text(node.name).append(' | ');
    var node_website = $('<a/>').prop('href', node.url).text(gettext('more info'));

    node_name.append(node_website);
    $('#map-info').append(node_name);
    defineMap();
    $('#basic-map-extend-image').click(function (event) {
        configureAdvancedMap();
        openAdvancedMap();
    });

    function defineMap() {
        node_location = new google.maps.LatLng(node.latitude, node.longitude);
        map_controls = {
            'zoom': 12,
            'center': node_location,
            'mapTypeControl': true,
            'mapTypeControlOptions': {
                'style': google.maps.MapTypeControlStyle.HORIZONTAL_BAR,
                'position': google.maps.ControlPosition.TOP_LEFT
            },
            'scrollwheel': false,
            'navigationControl': false,
            'scaleControl': false,
            'draggable': false,
            'mapTypeId': google.maps.MapTypeId.ROADMAP,
            'streetViewControl': false
        };
        map = new google.maps.Map($('#map')[0], map_controls);
        var marker = new google.maps.Marker({
            'position': node_location,
            'map': map,
            'title': node.name
        });
    }

    function configureAdvancedMap() {
        map.navigationControl = true;
        map.scaleControl = true;
        map.draggable = true;
        map.streetViewControl = true;
        map.set('mapTypeControlOptions', google.maps.ControlPosition.TOP_RIGHT);
    }

    function configureBasicMap() {
        map.setOptions(map_controls);
    }

    function closeAdvancedMap() {
        $('#close-button').remove();
        $('#overlay').fadeOut('slow', 0.0, function () {
            // Animation complete.
            $('#overlay').remove();
        });
        $('#advanced-map').fadeOut ('fast', 0.0, function (event){
            //callback
            $('#map').detach().prependTo('#basic-map').insertAfter('#map-info');
            $('#advanced-map').remove();
            $('#basic-map-extend-image').show();
            configureBasicMap();
            refreshMapCenter();
        });
    }

    function refreshMapCenter() {
        var center = map.getCenter();
        google.maps.event.trigger(map, 'resize');
        map.setCenter(center);
    }

    // TODO : Basic map resize animation should resize from its given position. That means if map is on the left side of the screen, animation should resize from the same side. Looks much prettier than a simple fade in pop up.
    function openAdvancedMap() {
        $('#basic-map-extend-image').hide();
        $('<div/>').attr('id', 'advanced-map').appendTo(document.body);
        $('<div/>').attr('id', 'overlay').fadeTo('slow', 0.8, function (){
            //Animation complete
        }).appendTo(document.body).click(closeAdvancedMap);
        $('<div/>').attr('id', 'close-button').fadeTo('slow', 1.0).appendTo(document.body).click(closeAdvancedMap);
        $('#advanced-map').append($('<div/>').attr('id', 'advanced-map-container'));
        $('#advanced-map-container').hide();
        $('#map').detach().prependTo('#advanced-map-container');
        $('#advanced-map-container').show();
        refreshMapCenter();
        $(document).keyup(function (event) {
            //  alert(e.which);
            if (event.keyCode == 27) {
                closeAdvancedMap();
            }
        });
    }
});
