google.load('search', '1', {language : 'en'});
google.setOnLoadCallback(function () {
    var customSearchOptions = {};
    var customSearchControl = new google.search.CustomSearchControl('003912915932446183218:zeq20qye9oa', customSearchOptions);
    customSearchControl.setResultSetSize(google.search.Search.FILTERED_CSE_RESULTSET);
    var options = new google.search.DrawOptions();
    options.setAutoComplete(true);
    options.enableSearchboxOnly("/search");
    customSearchControl.draw('cse-search-form', options);
}, true);