$(document).ready(function (event) {
    var myOptions;
    var nodeLocation;
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
        map.set('scrollwheel',true);
        map.set('navigationControl',true);
        map.set('scaleControl', true);
        map.set('draggable', true);
        map.set('streetViewControl', true);
    }
    function configureBasicMap(){
        map.set('scrollwheel',false);
        map.set('navigationControl',false);
        map.set('scaleControl', false);
        map.set('draggable', false);
        map.set('streetViewControl', false);
    }
    function closeAdvancedMap(){
        $('#closeButton').remove();
        $('#overlay').fadeOut('slow', 0.0, function() {
            // Animation complete.
            $('#overlay').remove();
        });
        $('#advanced-map').animate ({
            width: '-=86%'
        }, 500, "linear", function (event){
            //callback
            $('#map').detach().prependTo('#basic-map').insertAfter('#map-info');
            $('#advanced-map').remove();
            $('#basic-map-extend-img').show();
            refreshMapCenter();
            configureBasicMap();
        });
    }
    function refreshMapCenter(){
        var center = map.getCenter();
        google.maps.event.trigger(map, 'resize');
        map.setCenter(center);
    }
    function openAdvancedMap(){
        $('#basic-map-extend-img').hide();
        $('<div/>').attr('id', 'advanced-map').appendTo(document.body);
        $('<div/>').attr('id', 'overlay').fadeTo("fast", 0.8, function (){
        //Animation complete
        }).appendTo(document.body).click(closeAdvancedMap);
        $('<div/>').attr('id', 'closeButton').appendTo(document.body).click(closeAdvancedMap);
        $('#closeButton').css("background-image", imageCloseUrl);
        $('#advanced-map').append($('<div/>').attr('id', 'advanced-map-container'));
        $('#map').detach().prependTo('#advanced-map-container');
        $('#advanced-map').animate ({
            width: '86%'
        }, 500, "linear", function (event){
            refreshMapCenter();
        });
        $(document).keyup(function (event) {
            //  alert(e.which);
            if (event.keyCode == 27) {
                closeAdvancedMap();
            }
        });
    }
});