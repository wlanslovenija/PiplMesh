$(document).ready(function () {
    var nodeLocation = new google.maps.LatLng(node.latitude, node.longitude);
    var myOptions = {
        zoom: 15,
        center: nodeLocation,
        scrollwheel: false,
        navigationControl: false,
        scaleControl: false,
        draggable: false,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        streetViewControl: false
    };
    var map = new google.maps.Map(document.getElementById('map_canvas'), myOptions);
    var nodeName = $('<p/>').text(node.name).append(' | ');
    var nodeWebsite = $('<a/>').prop('href', node.url).text(gettext("more info"));
    nodeName.append(nodeWebsite);
    $('#map_info').append(nodeName);
    var marker = new google.maps.Marker({
        position: nodeLocation,
        map: map,
        title: node.name
    });
});
