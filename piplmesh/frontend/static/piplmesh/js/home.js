function updateUserlist(data) {
    if (data.action == 'JOIN') {
        $('<li/>').text(data.username).appendTo('#userlist');
    }
    else if (data.action == 'PART') {
        // TODO: Improve escape and use more suitable :contains method
        $('#userlist li:contains(' + escape(data.username) + ')').remove();
    }
}

$(document).ready(function () {
    registerUpdatesProcessor('userlist', updateUserlist);
});