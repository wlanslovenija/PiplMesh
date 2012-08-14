var map_small;
var map_big;
var vl;
var weather_visible = false;
var infoWindow;
var ge;
google.load("earth", "1");
var googleEarth;


 document.onkeydown = function(evt) {
 evt = evt || window.event;
 if (evt.keyCode == 27) {
 toogleSmallBigMap();
 }
 };


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

function toogleSmallBigMap()
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

function setNondefaultButtonBorderStyle(divUI){
    divUI.style.backgroundColor = 'white';
    divUI.style.borderStyle = 'solid';
    divUI.style.borderWidth = '1px';
    divUI.style.cursor = 'pointer';
    divUI.style.textAlign = 'center';
    divUI.title = 'Click to switch on/off the weather info';
    divUI.style.borderWidth ='1px';
    divUI.style.borderColor = '#717B87';
    divUI.style.width = '50px';
}

function setNondefaultButtonTextStyle(divText, text){
    divText.style.fontFamily = 'Arial,sans-serif';
    divText.style.paddingTop = '1.6px';
    divText.style.color = '#333333';
    divText.style.fontSize = '13px';
    divText.style.paddingLeft = '4px';
    divText.style.paddingRight = '4px';
    divText.style.paddingBottom = '1.6px';
    divText.innerHTML = text;
}

$(document).ready(function () {


    //  width: 100%; height: 100%; text-align: center; margin: 50px 0px; padding: 0px;
    $('#request').click(function (event) {
       // resize('map_big');
        toogleSmallBigMap();
    });

    var nodeLocation = new google.maps.LatLng(node.latitude, node.longitude);
    var map_big_options = {
        center: nodeLocation,
        zoom: 10,
        mapTypeId: "OSM",
        mapTypeControlOptions: {
            mapTypeIds: mapTypeIds,
            style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
        },
        scrollwheel: true,
        navigationControl: true,
        scaleControl: true,
        draggable: true,
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

    var mapTypeIds = [];
    for(var type in google.maps.MapTypeId) {
        mapTypeIds.push(google.maps.MapTypeId[type]);
    }
    mapTypeIds.push("OSM");

    map_small = new google.maps.Map(document.getElementById('map_small'), map_small_options);
    map_big = new google.maps.Map(document.getElementById('map_big'), map_big_options);

    map_big.mapTypes.set("OSM", new google.maps.ImageMapType({
        getTileUrl: function(coord, zoom) {
            return "http://tile.openstreetmap.org/" + zoom + "/" + coord.x + "/" + coord.y + ".png";
        },
        tileSize: new google.maps.Size(256, 256),
        name: "OpenStreetMap",
        maxZoom: 18
    }));

    wl = new google.maps.weather.WeatherLayer({
        temperatureUnits: google.maps.weather.TemperatureUnit.CELSIUS
    });
    infoWindow = new google.maps.InfoWindow();

    google.maps.event.addListenerOnce(map_big, 'tilesloaded', addMarkers)

    google.maps.event.addListener(map_small, 'click', function() {
    });

    // Create a div to hold the control.
    var buttonWeather = document.createElement('div');
    var buttonExit = document.createElement('div');
// Set CSS styles for the DIV containing the control
// Setting padding to 5 px will offset the control
// from the edge of the map.
    buttonWeather.style.padding = '5px';
    buttonExit.style.padding = '5px';

// Set CSS for the control border.
    var buttonWeatherUI = document.createElement('div');
    var buttonExitUI = document.createElement('div');
    setNondefaultButtonBorderStyle(buttonWeatherUI);
    setNondefaultButtonBorderStyle(buttonExitUI);

    buttonWeather.appendChild(buttonWeatherUI);
    buttonExit.appendChild(buttonExitUI);


    var buttonExitText = document.createElement('div');
    setNondefaultButtonTextStyle(buttonExitText, "Exit");
    buttonExitUI.appendChild(buttonExitText);

// Set CSS for the control interior.
    var buttonWeatherText = document.createElement('div');
    setNondefaultButtonTextStyle(buttonWeatherText, "Vreme");
    buttonWeatherUI.appendChild(buttonWeatherText);

    google.maps.event.addDomListener(buttonWeather, 'click', function() {
        setWeatherVisible();
    });
    google.maps.event.addDomListener(buttonWeather, 'mouseover', function(){

        buttonWeatherUI.style.background = '#F0F0F0';
        buttonWeatherText.style.color = 'black';

    });
    google.maps.event.addDomListener(buttonWeather, 'mouseout', function(){


        buttonWeatherUI.style.background = 'white';
        buttonWeatherText.style.color = '#333333';
    });

    google.maps.event.addDomListener(buttonExit, 'click', function() {
        toogleSmallBigMap();
    });
    google.maps.event.addDomListener(buttonExit, 'mouseover', function(){

        buttonExitUI.style.background = '#F0F0F0';
        buttonExitText.style.color = 'black';

    });
    google.maps.event.addDomListener(buttonExit, 'mouseout', function(){


        buttonExitUI.style.background = 'white';
        buttonExitText.style.color = '#333333';
    });
    map_big.controls[google.maps.ControlPosition.TOP_RIGHT].push(buttonWeather);
    map_big.controls[google.maps.ControlPosition.TOP_RIGHT].push(buttonExit);

    var nodeName = $('<p/>').text(node.name).append(' | ');
    var nodeWebsite = $('<a/>').prop('href', node.url).text(gettext("more info"));
    nodeName.append(nodeWebsite);
    $('#map_info').append(nodeName);

    googleEarth = new GoogleEarth(map_big);
    google.maps.event.addListenerOnce(map_big, 'tilesloaded', addOverlays);


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
