var nodeName;
var nodeWebsite;
var timer;
var myOptions;
var nodeLocation;
var map;

document.onkeydown = function(evt) {
    evt = evt || window.event;
    if (evt.keyCode == 27) {
        close_advanced_map();
    }
};

$(document).ready(function () {
    nodeName = $('<p/>').text(node.name).append(' | ');
    nodeWebsite = $('<a/>').prop('href', node.url).text(gettext("more info"));
    nodeName.append(nodeWebsite);
    $('#map-info').append(nodeName);
    var timerMap;
    define_map();
    $("#basic-map-extend-img").click(function() {
        setExtendedMapControls();
        open_advanced_map();
    });
});

function getStyle(el,styleProp)
{
    var x = document.getElementById(el);
    if (x.currentStyle)
        var y = x.currentStyle[styleProp];
    else if (window.getComputedStyle)
        var y = document.defaultView.getComputedStyle(x,null).getPropertyValue(styleProp);
    return y;
}

function define_map(){
    nodeLocation = new google.maps.LatLng(node.latitude, node.longitude);
    myOptions = {
        zoom: 12,
        center: nodeLocation,
        scrollwheel: false,
        navigationControl: false,
        scaleControl: false,
        draggable: false,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        streetViewControl: false
    };
    map = new google.maps.Map(document.getElementById("map"), myOptions);
    var marker = new google.maps.Marker({
            position: nodeLocation,
            map: map,
            title: node.name
        }
    );
}

function setExtendedMapControls(){
    map.set('navigationControl',true);
    map.set('scaleControl', true);
    map.set('draggable', true);
    map.set('streetViewControl', true);
    map.setZoom(16);
}
function setBasicMapControls(){
    map.set('navigationControl',false);
    map.set('scaleControl', false);
    map.set('draggable', false);
    map.set('streetViewControl', false);
    map.setZoom(12);
}

function close_advanced_map(){
    $("#advanced-map").animate({
        width: '-=86%'
        // height: getStyle("advanced-map","height")
    }, 500, "linear", function(){
        //callback
        ($('#map').detach().prependTo('#basic-map')).insertAfter('#map-info');
        $('#overlay').remove();
        $('#advanced-map').remove();
        document.getElementById('basic-map-extend-img').style.visibility="visible";
        setBasicMapControls();
    });
}

function open_advanced_map(){
    document.getElementById('basic-map-extend-img').style.visibility="hidden";
    var div_overlay = jQuery('<div id="overlay"> </div>');
    var div_advanced_map = jQuery('<div id="advanced-map"></div>');
    div_advanced_map.appendTo(document.body);
    div_overlay.appendTo(document.body);
    $('#advanced-map').append('<div id="advanced-map-container"></div>');
    $('#advanced-map').append('<a class="close" onclick=close_advanced_map()></a>');
    $('#map').detach().prependTo('#advanced-map-container');
    $("#advanced-map").animate({
        width: '86%'
    }, 500, "linear", function(){
        google.maps.event.trigger(map, 'resize');
    });
}