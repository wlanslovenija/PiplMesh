google.load("search", "1", { language : {{ LANGUAGE_CODE }}});
google.setOnLoadCallback(function () {
    var customSearchOptions = {};
    var customSearchControl = new google.search.CustomSearchControl({{ SEARCH_ENGINE_UNIQUE_ID }}, customSearchOptions);
    customSearchControl.setResultSetSize(google.search.Search.FILTERED_CSE_RESULTSET);
    var options = new google.search.DrawOptions();
    options.setAutoComplete(true);
    options.enableSearchboxOnly("/search");
    customSearchControl.draw('cse-search-form', options);
}, true);