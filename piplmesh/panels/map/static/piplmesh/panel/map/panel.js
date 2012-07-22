var map_small;
var map_big;
var vl;
var weather_visible = false;
var infoWindow;

/*
 document.onkeydown = function(evt) {
 evt = evt || window.event;
 if (evt.keyCode == 27) {
 ExitFullscreenCSS();
 alert("Escape");
 }
 };
 */

function setWeatherVisible()
{
    if (weather_visible)
    {
        weather_visible = false;
        wl.setMap(null);
    }
    else
    {
        weather_visible = true;
        wl.setMap(map_big);
    }
}

function RequestFullscreenCSS()
{

    toggleDisplay("map_small", "display");
    toggleDisplay("map_big", "display");
    toggleDisplay("request", "display");
}

function ExitFullscreenCSS()
{
    toggleDisplay("map_small", "display");
    toggleDisplay("map_big", "display");
    toggleDisplay("request", "display");
}

function toggleVisibility(controlId, styleProp)
{
    var item_style = getStyle(controlId, styleProp )
    var control = document.getElementById(controlId);
    if(item_style == "visible" || item_style == "" || item_style == "inherit")
        control.style.visibility = "hidden";
    else
        control.style.visibility = "visible";
}

function toggleDisplay(controlId, styleProp)
{

    var item_style = getStyle(controlId, styleProp )
    var control = document.getElementById(controlId);
    if(item_style == "none" || item_style == "")
        control.style.display = "inherit";
    else
        control.style.display = "none";
}

function getStyle(el,styleProp)
{
    var x = document.getElementById(el);
    if (x.currentStyle)
        var y = x.currentStyle[styleProp];
    else if (window.getComputedStyle)
        var y = document.defaultView.getComputedStyle(x,null).getPropertyValue(styleProp);
    return y;
}

function setButtonWeatherBorderStyle(controlUI){
    controlUI.style.backgroundColor = 'white';
    controlUI.style.borderStyle = 'solid';
    controlUI.style.borderWidth = '2px';
    controlUI.style.cursor = 'pointer';
    controlUI.style.textAlign = 'center';
    controlUI.title = 'Click to switch on/off the weather info';

}

function setButtonWeatherTextStyle(controlText){
    controlText.style.fontFamily = 'Arial,sans-serif';
    controlText.style.fontSize = '12px';
    controlText.style.paddingLeft = '4px';
    controlText.style.paddingRight = '4px';
    controlText.innerHTML = '<strong>Vreme<strong>';

}

$(function()
{


    // The plugin sets the $.support.fullscreen flag:
    if($.support.fullscreen){
        $('#request').click(function(e){
            RequestFullscreenCSS();
            $('#container_text').fullScreen({
                'callback' : function(fullScreen){
                    if ( !fullScreen ) {

                        // Canceled
                        // $('#container_text').css({'background': 'red'});
                        ExitFullscreenCSS();
                    }
                }
            });
        });
    }
})

$(document).ready(function () {


    var nodeLocation = new google.maps.LatLng(node.latitude, node.longitude);
    //alert(node.latitude);

    var map_big_options = {
        center:nodeLocation,
        zoom: 10,
        mapTypeControl: true,
        mapTypeControlOptions: {
            style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
        },
        zoomControl: true,
        zoomControlOptions: {
            style: google.maps.ZoomControlStyle.LARGE
        },
        scrollwheel: true,
        navigationControl: true,
        scaleControl: true,
        draggable: false,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        streetViewControl: true,
        panControl: true
    };

    var map_small_options = {
        zoom: 8,
        center: nodeLocation,
        scrollwheel: false,
        navigationControl: false,
        scaleControl: false,
        draggable: false,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        streetViewControl: false
    };

    map_small = new google.maps.Map(document.getElementById('map_small'), map_small_options);
    map_big = new google.maps.Map(document.getElementById('map_big'), map_big_options);

    wl = new google.maps.weather.WeatherLayer({
        temperatureUnits: google.maps.weather.TemperatureUnit.CELSIUS
    });
    infoWindow = new google.maps.InfoWindow();

    google.maps.event.addListenerOnce(map_big, 'tilesloaded', addMarkers)

    google.maps.event.addListener(map_small, 'click', function() {
        // screenfull.request( document.getElementById('container_text') );
        $(function()
        {
            // The plugin sets the $.support.fullscreen flag:
            if($.support.fullscreen){

                RequestFullscreenCSS();
                $('#container_text').fullScreen({
                    'callback' : function(fullScreen){
                        if ( !fullScreen ) {

                            // Canceled
                            // $('#container_text').css({'background': 'red'});
                            ExitFullscreenCSS();
                        }
                    }
                });
            }
        })
    });

    // Create a div to hold the control.
    var controlDiv = document.createElement('div');

// Set CSS styles for the DIV containing the control
// Setting padding to 5 px will offset the control
// from the edge of the map.
    controlDiv.style.padding = '5px';

// Set CSS for the control border.
    var controlUI = document.createElement('div');
    setButtonWeatherBorderStyle(controlUI);
    controlDiv.appendChild(controlUI);

// Set CSS for the control interior.
    var controlText = document.createElement('div');
    setButtonWeatherTextStyle(controlText);
    controlUI.appendChild(controlText);

    google.maps.event.addDomListener(controlDiv, 'click', function() {
        setWeatherVisible();
    });
    google.maps.event.addDomListener(controlDiv, 'mouseover', function(){

        controlUI.style.background = '#f5f5f5';
    });
    google.maps.event.addDomListener(controlDiv, 'mouseout', function(){


        controlUI.style.background = 'white';
    });
    map_big.controls[google.maps.ControlPosition.TOP_RIGHT].push(controlDiv);

    var nodeName = $('<p/>').text(node.name).append(' | ');
    var nodeWebsite = $('<a/>').prop('href', node.url).text(gettext("more info"));
    nodeName.append(nodeWebsite);
    $('#map_info').append(nodeName);

    function addMarkers() {
        function createMarker() {
            var marker = new google.maps.Marker({
                position: nodeLocation,
                map: map_big,
                title: node.name
            });

            google.maps.event.addListener(marker, 'click', function() {
                var myHtml = '<strong>#' + node.name + '</strong><br/><a href='+node.url+'>Home page<a>';
                infoWindow.setContent(myHtml);
                infoWindow.open(map_big, marker);
            });
        }
        createMarker();
    }
});
