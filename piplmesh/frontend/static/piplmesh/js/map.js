$(document).ready(function () {
    initialize();
});

function initialize() {
    var myLatlng = new google.maps.LatLng(node.latitude, node.longitude);
    var myOptions = {
        zoom: 15,
        center: myLatlng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    }

    var map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);

    var contentString = 
        '<div class="node_content">'+
            '<h3>'+node.name+'</h3>'+
            '<div id="bodyContent">'+
                '<p>'+
                    gettext("Location: ")+node.location+
                '</p>'+
                '<p>'+
                    gettext("Website: ")+
                    '<a href="'+node.url+'">'+node.url+'</a> '+
                '</p>'+
            '</div>'+
        '</div>';
            
    var infowindow = new google.maps.InfoWindow({
            content: contentString
    });

    var marker = new google.maps.Marker({
            position: myLatlng,
            map: map,
            title: node.name
    });

    google.maps.event.addListener(marker, 'click', function() {
        infowindow.open(map, marker);
    });
}
