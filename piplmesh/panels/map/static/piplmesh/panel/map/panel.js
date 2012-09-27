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

    // Necessary libraries are included with googleapis in piplmesh/panels/map/templates/panel/map/panel.html
    var map_layers = new Object;
    var map_layers_labels = new Object;
    map_layers_labels.weather = gettext('Weather');
    map_layers.weather = new google.maps.weather.WeatherLayer({
        temperatureUnits: google.maps.weather.TemperatureUnit.CELSIUS
    });
    map_layers_labels.clouds = gettext('Clouds');
    map_layers.clouds = new google.maps.weather.CloudLayer();
    map_layers_labels.panoramio = gettext('Panoramio');
    map_layers.panoramio = new google.maps.panoramio.PanoramioLayer();


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

    function addMapLayerOption(layer, label) {
        if($('#map-layers').lenght != 0) {
            $('<input/>').prop({
                'id': 'map-layer-' + layer,
                'type': 'checkbox',
                'name': 'map-layer--' + layer
            }).appendTo('#map-layers');
            $('<label/>').prop('for', 'map-layer-' + layer).text(label).appendTo('#map-layers');
            $('<br/>').appendTo('#map-layers');
            $('#map-layer-' + layer).click(function (event) {
                setLayerVisibility(layer);
            });
        }
    }

    function setLayerVisibility(layer) {
        if ($('#map-layer-' + layer).attr('checked')) {
            map_layers[layer].setMap(map);
        }
        else {
            map_layers[layer].setMap(null);
        }
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
        $('<div/>').prop('id', 'map-layers').appendTo('#advanced-map');
        // Map layer options should be added after #map-layers is created
        for (var layer in map_layers) {
            addMapLayerOption(layer, gettext(map_layers_labels[layer]));
        }

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
