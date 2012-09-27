$(document).ready(function () {
    var node_location = new google.maps.LatLng(node.latitude, node.longitude);

    var options = {
        'zoom': 12,
        'center': node_location,
        'mapTypeControl': true,
        'scrollwheel': false,
        'navigationControl': false,
        'scaleControl': false,
        'draggable': false,
        // TODO: Allow users to set default layer
        'mapTypeId': google.maps.MapTypeId.ROADMAP,
        'mapTypeControlOptions': {
            'position': google.maps.ControlPosition.TOP_LEFT,
            'mapTypeIds': [
                google.maps.MapTypeId.ROADMAP,
                google.maps.MapTypeId.SATELLITE,
                'OpenStreetMap'
            ]
        },
        'streetViewControl': false
    };

    var node_name = $('<p/>').text(node.name).append(' | ');
    var node_website = $('<a/>').prop('href', node.url).text(gettext("more info"));
    node_name.append(node_website);
    $('#map-info').append(node_name);

    var map = new google.maps.Map($('#map').get(0), options);

    map.mapTypes.set('OpenStreetMap', new google.maps.ImageMapType({
        'getTileUrl': function(coordinates, zoom) {
            // TODO: Is there HTTPS version - it would be better to use that so we do not get mixed content errors if we run our portal over HTTPS
            return 'http://tile.openstreetmap.org/' + zoom + '/' + coordinates.x + '/' + coordinates.y + '.png';
        },
        'tileSize': new google.maps.Size(256, 256),
        // TODO: The label name is too long and does not display nicely in the map
        'name': 'OpenStreetMap',
        'maxZoom': 18
    }));

    var marker = new google.maps.Marker({
        'position': node_location,
        'map': map,
        'title': node.name
    });

    function configureBasicMap() {
        map.setOptions(options);
		// TODO: Why is this necessary to set manually?
        map.mapTypeControlOptions.position = google.maps.ControlPosition.TOP_LEFT;
    }

    function configureAdvancedMap() {
        map.navigationControl = true;
        map.scaleControl = true;
        map.draggable = true;
        map.streetViewControl = true;
        map.mapTypeControlOptions.position = google.maps.ControlPosition.TOP_RIGHT;
    }

    function closeAdvancedMap() {
        $('#close-button').remove();
        // TODO: Should be "fast" here?
        $('#overlay').fadeOut('slow', 0.0, function () {
            $('#overlay').remove();
        });
        $('#advanced-map').fadeOut ('fast', 0.0, function (event) {
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

    // TODO: Basic map resize animation should resize from its given position on the page, like it is popping out. That means if map is on the left side of the screen, animation should resize from the same side. Looks much prettier than a simple fade in pop up.
    function openAdvancedMap() {
        $('#basic-map-extend-image').hide();
        $('<div/>').prop('id', 'advanced-map').appendTo('body');
        // TODO: Should be "fast" here?
        $('<div/>').prop('id', 'overlay').fadeTo('slow', 0.8).appendTo('body').click(closeAdvancedMap);
        // TODO: Should be "fast" here?
        $('<div/>').prop('id', 'close-button').fadeTo('slow', 1.0).appendTo('body').click(closeAdvancedMap);
        $('#advanced-map').append($('<div/>').prop('id', 'advanced-map-container'));
        $('#advanced-map-container').hide();
        $('#map').detach().prependTo('#advanced-map-container');
        $('#advanced-map-container').show();
        refreshMapCenter();
        $(document).keyup(function (event) {
            if (event.keyCode == 27) {
                closeAdvancedMap();
            }
        });
    }

    $('#basic-map-extend-image').click(function (event) {
        configureAdvancedMap();
        openAdvancedMap();
    });
});
