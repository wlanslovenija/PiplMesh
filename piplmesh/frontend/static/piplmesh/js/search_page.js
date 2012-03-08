google.load('search', '1', { language : lang_code });
google.setOnLoadCallback(function () {
    var customSearchOptions = {};
    var customSearchControl = new google.search.CustomSearchControl(unique_id, customSearchOptions);
    customSearchControl.setResultSetSize(google.search.Search.LARGE_RESULTSET);
    customSearchControl.draw('cse');
    function parseParamsFromUrl() {
        var params = {};
        var parts = window.location.search.substr(1).split('&');
        for (var i = 0; i < parts.length; i++) {
            var keyValuePair = parts[i].split('=');
            var key = decodeURIComponent(keyValuePair[0]);
            params[key] = keyValuePair[1] ? decodeURIComponent(keyValuePair[1].replace(/\+/g, ' ')) : keyValuePair[1];
        }
        return params;
    }

var urlParams = parseParamsFromUrl();
var queryParamName = 'q';
if (urlParams[queryParamName]) {
    customSearchControl.execute(urlParams[queryParamName], null,{
        'oq': urlParams['oq'],
        'aq': urlParams['aq'],
        'aqi': urlParams['aqi'],
        'aql': urlParams['aql'],
        'gs_sm': urlParams['gs_sm'],
        'gs_upl': urlParams['gs_upl']});
    }
}, true);