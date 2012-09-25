$(document).ready(function (event) {
    var nodeLocation;
    var mapControls;
    var map;
    var nodeName = $('<p/>').text(node.name).append(' | ');
    var nodeWebsite = $('<a/>').prop('href', node.url).text(gettext("more info"));
    nodeName.append(nodeWebsite);
    $('#map-info').append(nodeName);
    defineMap();
    $('#basic-map-extend-img').click(function (event) {
        configureAdvancedMap();
        openAdvancedMap();
    });
    function defineMap(){
        nodeLocation = new google.maps.LatLng(node.latitude, node.longitude);
        mapControls = {
            'zoom': 12,
            'center': nodeLocation,
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
        map = new google.maps.Map($("#map")[0], mapControls);
        $('#basic-map-extend-img').css("background-image", imageExtendUrl);
        var marker = new google.maps.Marker({
            'position': nodeLocation,
            'map': map,
            'title': node.name
        });
    }
    function configureAdvancedMap(){
        map.navigationControl = true;
        map.scaleControl = true;
        map.draggable = true;
        map.streetViewControl = true;
        map.set('mapTypeControlOptions',google.maps.ControlPosition.TOP_RIGHT);
    }
    function configureBasicMap(){
        map.setOptions(mapControls);
    }
    function closeAdvancedMap(){
        $('#closeButton').remove();
        $('#overlay').fadeOut('slow', 0.0, function () {
            // Animation complete.
            $('#overlay').remove();
        });
        $('#advanced-map').fadeOut ('fast', 0.0, function (event){
            //callback
            $('#map').detach().prependTo('#basic-map').insertAfter('#map-info');
            $('#advanced-map').remove();
            $('#basic-map-extend-img').show();
            configureBasicMap();
            refreshMapCenter();
        });
    }
    function refreshMapCenter(){
        var center = map.getCenter();
        google.maps.event.trigger(map, 'resize');
        map.setCenter(center);
    }
    // TODO basic map resize animation should resize from its given position. That means if map is on the left side of the screen, animation should resize from the same side. Looks much prettier than a simple fade in pop up.
    function openAdvancedMap(){
        $('#basic-map-extend-img').hide();
        $('<div/>').attr('id', 'advanced-map').appendTo(document.body);
        $('<div/>').attr('id', 'overlay').fadeTo("slow", 0.8, function (){
            //Animation complete
        }).appendTo(document.body).click(closeAdvancedMap);
        $('<div/>').attr('id', 'closeButton').appendTo(document.body).click(closeAdvancedMap);
        $('#closeButton').css("background-image", imageCloseUrl);
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