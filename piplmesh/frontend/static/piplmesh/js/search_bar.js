google.load('search', '1', { 'language' : language_code });
google.setOnLoadCallback(function () {
    var customSearchOptions = {};
    var customSearchControl = new google.search.CustomSearchControl(search_engine_unique_id, customSearchOptions);
    var options = new google.search.DrawOptions();
    options.setAutoComplete(true);
    options.enableSearchboxOnly('/search');
    customSearchControl.draw('cse_search_form', options);
}, true);


$(document).ready(function () {
    var query = location.search;
    var open_in_google_link = 'http://www.google.com/search' + query;
    $('#google_results_link').prop('href', open_in_google_link);
});
