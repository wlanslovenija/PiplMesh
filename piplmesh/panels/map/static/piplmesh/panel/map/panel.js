$(document).ready(function () {
    var node_location = new google.maps.LatLng(node.latitude, node.longitude);

    var options = {
        'zoom': 15,
        'center': node_location,
        'scrollwheel': false,
        'navigationControl': false,
        'scaleControl': false,
        'draggable': false,
        // TODO: Allow users to set default layer
        'mapTypeId': google.maps.MapTypeId.ROADMAP,
        'mapTypeControlOptions': {
            'mapTypeIds': [
                google.maps.MapTypeId.ROADMAP,
                google.maps.MapTypeId.SATELLITE
                'OpenStreetMap',
            ]
        },
        'streetViewControl': false
    };

    var map = new google.maps.Map(document.getElementById('map_canvas'), options);

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

    var node_name = $('<p/>').text(node.name).append(' | ');
    var node_website = $('<a/>').prop('href', node.url).text(gettext("more info"));
    node_name.append(node_website);
    $('#map_info').append(node_name);
});
