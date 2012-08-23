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
    function getStyle(el, styleProp){
        var value = $(el).css(styleProp);
        return value;
    }
    function defineMap(){
        nodeLocation = new google.maps.LatLng(node.latitude, node.longitude);
        myOptions = {
            'zoom': 12,
            'center': nodeLocation,
            'scrollwheel': false,
            'navigationControl': false,
            'scaleControl': false,
            'draggable': false,
            'mapTypeId': google.maps.MapTypeId.ROADMAP,
            'streetViewControl': false
        };
        map = new google.maps.Map($("#map")[0], myOptions);
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
    }
    function configureBasicMap(){
        map.set('navigationControl',false);
        map.set('scaleControl', false);
        map.set('draggable', false);
        map.set('streetViewControl', false);
    }
    function closeAdvancedMap(){
        $('#advanced-map').animate({
            width: '-=86%'
        }, 500, "linear", function (event){
            //callback
            ($('#map').detach().prependTo('#basic-map')).insertAfter('#map-info');
            $('#overlay').remove();
            $('#advanced-map').remove();
            $('#basic-map-extend-img').css('visibility', 'visible');
            configureBasicMap();
        });
    }
    function openAdvancedMap(){
        $('#basic-map-extend-img').css('visibility', 'hidden');
        $('<div/>').attr('id', 'advanced-map').appendTo(document.body);
        $('<div/>').attr('id', 'overlay').appendTo(document.body);
        $('#advanced-map').append($('<div/>').attr('id', 'advanced-map-container'));
        $('#advanced-map').append($('<a/>').addClass('close').click(closeAdvancedMap));
      //$('#close')[0].style.backgroundImage = imageUrl;
        $('#map').detach().prependTo('#advanced-map-container');
        $('#advanced-map').animate({
            width: '86%'
        }, 500, "linear", function (event){
            google.maps.event.trigger(map, 'resize');
        });
        $(document).keyup(function (event) {
            //  alert(e.which);
            if (event.keyCode == 27) {
                closeAdvancedMap();
            }
        });
    }
});