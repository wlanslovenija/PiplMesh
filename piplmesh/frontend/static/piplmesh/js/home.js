function updateUserlist(data) {
    if (data.action == 'JOIN') {
        $('#userlist').append('<li>' + escape(data.username) + '</li>');
    }
    else if (data.action == 'PART') {
        $('#userlist li:contains(' + escape(data.username) + ')').remove();
    }
}

registerUpdatesProcessor('userlist', updateUserlist);