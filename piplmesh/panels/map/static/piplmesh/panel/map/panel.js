var nodeName;
var nodeWebsite;
var timer;

document.onkeydown = function(evt) {
    evt = evt || window.event;
    if (evt.keyCode == 27) {
        document.getElementById('map').style.width='250px';
        document.getElementById('map').style.height='250px';
        ($('#map').detach().prependTo('#basic_map')).insertAfter('#map_info');

      /*  timer1 = setInterval(function(){ google.maps.event.trigger(map, 'resize')}, 50);
        $("#map").animate({

            width: getStyle("basic_map","width"),
            height: getStyle("basic_map","height")

        }, 500, "linear", function(){
            timerMap = clearInterval(timer1);
        });*/
        $('#overlay').remove();
    }
};

$(document).ready(function () {
    nodeName = $('<p/>').text(node.name).append(' | ');
    nodeWebsite = $('<a/>').prop('href', node.url).text(gettext("more info"));
    nodeName.append(nodeWebsite);
    $('#map_info').append(nodeName);

    var timerMap;
    create_basic_Map("map");
    google.maps.event.addListener(map, 'click', function() {
        var div_overlay = jQuery('<div id="overlay"> </div>');
        div_overlay.appendTo(document.body);
        $('#overlay').append('<div id="advanced_map"></div>');
        $('#map').detach().prependTo('#advanced_map');
        timer = setInterval(function(){ google.maps.event.trigger(map, 'resize')}, 40);
        $("#map").animate({
            width: getStyle("advanced_map","width"),
            height: getStyle("advanced_map","height")
        }, 500, "linear", function(){
        timerMap = clearInterval(timer);
        });
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

function create_basic_Map(div_tag){
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
    map = new google.maps.Map(document.getElementById(div_tag), myOptions);
    var marker = new google.maps.Marker({
            position: nodeLocation,
            map: map,
            title: node.name
        }
    );
}
