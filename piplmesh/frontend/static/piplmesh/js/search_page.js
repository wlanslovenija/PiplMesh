google.load('search', '1', { 'language' : language_code });
google.setOnLoadCallback(function () {
    var customSearchOptions = {};
    var imageSearchOptions = {};
    imageSearchOptions.layout = google.search.ImageSearch.LAYOUT_POPOUT;
    customSearchOptions.enableImageSearch = true;
    customSearchOptions.imageSearchOptions = imageSearchOptions;
    var customSearchControl = new google.search.CustomSearchControl(search_engine_unique_id, customSearchOptions);
    customSearchControl.setResultSetSize(google.search.Search.LARGE_RESULTSET);
    var options = new google.search.DrawOptions();
    options.enableSearchResultsOnly();
    customSearchControl.draw('cse', options);
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
        customSearchControl.execute(urlParams[queryParamName], null, {
            'oq': urlParams.oq,
            'aq': urlParams.aq,
            'aqi': urlParams.aqi,
            'aql': urlParams.aql,
            'gs_sm': urlParams.gs_sm,
            'gs_upl': urlParams.gs_upl
        });
    }

    $('#gsc-i-id1').val(urlParams[queryParamName]);
    $('#gsc-i-id1').focus();

}, true);