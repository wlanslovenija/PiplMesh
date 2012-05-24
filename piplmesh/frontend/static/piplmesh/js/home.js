function User(data) {
    var self = this;
    $.extend(self, data);
}

function redrawUserList() {
    var keys = [];
    $.each(onlineUsers, function (key, value) {
        keys.push(key);
    });
    keys.sort(function (key1, key2) {
        if (key1 < key2) return -1;
        if (key1 > key2) return 1;
        return 0;
    });
    $('#userlist').empty();
    var searchUsers = $('#search_users').val().toUpperCase();

    $.each(keys, function(index, key){
        if (searchUsers === '' || key.indexOf(searchUsers) !== -1) {
            user = onlineUsers[key];
            var li = $('<li/>');
            var image = $('<img/>').attrs({'src': user.image_url, 'alt': gettext('User image')});
            li.append(image);
            li.append(user.username);
            var div = $('<div/>').attrs({'class': 'info'});
            div.append(user.info);
            li.append(div);
            $('#userlist').append(li);
        }
    });
}

function updateUserList(data) {
    var user = new User(data.user);
    if (data.action === 'JOIN') {
        onlineUsers[user.username.toLowerCase()] = user;
        redrawUserList();
    } else if (data.action === 'PART') {
        if (onlineUsers[user.username]) {
            delete onlineUsers[user.username];
            redrawUserList();
        }
    }
}

$(document).ready(function () {
    $.updates.registerProcessor('home_channel', 'userlist', updateUserList);

    $('.panel .header').click(function () {
        $(this).next('ul').slideToggle('slow');
    });

    $('#search_users').change(function () {
        redrawUserList();
    });
});
