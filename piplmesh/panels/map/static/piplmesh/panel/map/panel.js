$(document).ready(function () {
    var nodeLocation = new google.maps.LatLng(node.latitude, node.longitude);

    var myOptions = {
        'zoom': 15,
        'center': nodeLocation,
        'scrollwheel': false,
        'navigationControl': false,
        'scaleControl': false,
        'draggable': false,
        'mapTypeId': 'OpenStreetMap',
        'mapTypeControlOptions': {
            'mapTypeIds': [
                'OpenStreetMap',
                google.maps.MapTypeId.ROADMAP,
                google.maps.MapTypeId.SATELLITE
            ]
        },
        'streetViewControl': false
    };

    var map = new google.maps.Map(document.getElementById('map_canvas'), myOptions);

    map.mapTypes.set('OpenStreetMap', new google.maps.ImageMapType({
        getTileUrl: function(coordinates, zoom) {
            return 'http://tile.openstreetmap.org/' + zoom + '/' + coordinates.x + '/' + coordinates.y + '.png';
        },
        'tileSize': new google.maps.Size(256, 256),
        'name': 'OpenStreetMap',
        'maxZoom': 18
    }));

    var marker = new google.maps.Marker({
        'position': nodeLocation,
        'map': map,
        'title': node.name
    });

    var nodeName = $('<p/>').text(node.name).append(' | ');
    var nodeWebsite = $('<a/>').prop('href', node.url).text(gettext("more info"));
    nodeName.append(nodeWebsite);
    $('#map_info').append(nodeName);
});
