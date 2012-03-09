google.load('search', '1', { 'language' : language_code });
google.setOnLoadCallback(function () {
    var customSearchOptions = {};
    var customSearchControl = new google.search.CustomSearchControl(search_engine_unique_id, customSearchOptions);
    customSearchControl.setResultSetSize(google.search.Search.FILTERED_CSE_RESULTSET);
    var options = new google.search.DrawOptions();
    options.setAutoComplete(true);
    options.enableSearchboxOnly('/search');
    customSearchControl.draw('cse-search-form', options);
}, true);