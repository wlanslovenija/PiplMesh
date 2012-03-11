$(document).ready(function () {
    var query = location.search;
    var url = 'http://www.google.com/search' + query;
    $("a#link").prop('href', url);
});