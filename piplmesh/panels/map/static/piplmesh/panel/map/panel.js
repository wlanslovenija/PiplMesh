$(document).ready(function () {
    var element = document.getElementById('map_canvas');
    var nodeLocation = new google.maps.LatLng(node.latitude, node.longitude);

    var myOptions = {
        zoom: 15,
        center: nodeLocation,
        scrollwheel: false,
        navigationControl: false,
        scaleControl: false,
        draggable: false,
        mapTypeId: "OSM",
        mapTypeControlOptions: {
            mapTypeIds: [
                "OSM",
                google.maps.MapTypeId.ROADMAP,
                google.maps.MapTypeId.SATELLITE
            ]
        },
        streetViewControl: false
    };

    var map = new google.maps.Map(element, myOptions);

    map.mapTypes.set("OSM", new google.maps.ImageMapType({
        getTileUrl: function(coord, zoom) {
            return "http://tile.openstreetmap.org/" + zoom + "/" + coord.x + "/" + coord.y + ".png";
        },
        tileSize: new google.maps.Size(256, 256),
        name: "OpenStreetMap",
        maxZoom: 18
    }));

    var marker = new google.maps.Marker({
        position: nodeLocation,
        map: map,
        title: node.name
    });

    var nodeName = $('<p/>').text(node.name).append(' | ');
    var nodeWebsite = $('<a/>').prop('href', node.url).text(gettext("more info"));
    nodeName.append(nodeWebsite);
    $('#map_info').append(nodeName);

});
