google.load('search', '1', { 'language' : language_code });
google.setOnLoadCallback(function () {
    var customSearchOptions = {};
    var customSearchControl = new google.search.CustomSearchControl(search_engine_unique_id, customSearchOptions);
    var options = new google.search.DrawOptions();
    options.setAutoComplete(true);
    options.enableSearchboxOnly(search_page_url);
    customSearchControl.draw('cse_search_form', options);
}, true);

$(document).ready(function () {
    var query = location.search;
    var open_in_google_link = 'http://www.google.com/search' + query;
    $('#google_results_link').prop('href', open_in_google_link);
    var current_url = document.URL;
    $('#next_page').prop('value', current_url);
    $('[name=set_language_sl]').prop('action', '/i18n/setlang/');
    $('[name=set_language_en]').prop('action', '/i18n/setlang/');
    $('#choose_language_sl').prop('href', current_url);
    $('#choose_language_en').prop('href', current_url);
//    $('#choose_language_sl').prop('onclick', 'document.set_language_sl.submit()');
//    $('#choose_language_en').prop('onclick', 'document.set_language_en.submit()');
});
