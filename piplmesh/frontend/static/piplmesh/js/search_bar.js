google.load('search', '1', { language : lang_code });
google.setOnLoadCallback(function () {
    var customSearchOptions = {};
    var customSearchControl = new google.search.CustomSearchControl(unique_id, customSearchOptions);
    customSearchControl.setResultSetSize(google.search.Search.FILTERED_CSE_RESULTSET);
    var options = new google.search.DrawOptions();
    options.setAutoComplete(true);
    options.enableSearchboxOnly('/search');
    customSearchControl.draw('cse-search-form', options);
}, true);