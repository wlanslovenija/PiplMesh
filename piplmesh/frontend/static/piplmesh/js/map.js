$(document).ready(function () {
    initialize();
});

function initialize() {
    var nodeLocation = new google.maps.LatLng(node.latitude, node.longitude);
    var myOptions = {
        zoom: 15,
        center: nodeLocation,
        scrollwheel: false,
        navigationControl: false,
        scaleControl: false,
        draggable: false,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    }
    var map = new google.maps.Map(document.getElementById('map_canvas'), myOptions);
    var nodeDiv = $('<div/>').prop({
        'class': 'node_content'
    });
    var nodeName = $('<h3/>').text(node.name);
    var nodeContent = $('<div/>').prop({
        'id': 'bodyContent'
    });
    var nodeAddress = $('<p/>').text(gettext("Location:")+' '+node.location);
    var nodeWebsiteText = $('<p/>').text(gettext("Website:"));
    var nodeWebsite = $('<a/>').prop('href', node.url).text(node.url);
    nodeDiv.append(nodeName);
    nodeContent.append(nodeAddress);
    nodeWebsiteText.append(nodeWebsite);
    nodeContent.append(nodeWebsiteText);
    nodeDiv.append(nodeContent);
    var infowindow = new google.maps.InfoWindow({
            content: nodeDiv.html()
    });
    var marker = new google.maps.Marker({
            position: nodeLocation,
            map: map,
            title: node.name
    });
    google.maps.event.addListener(marker, 'click', function (event) {
            infowindow.open(map, marker);
        }
    );
}
