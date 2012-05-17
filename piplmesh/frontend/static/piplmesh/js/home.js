var onlineUsers = {
    {% for user in online_users %}
        {{ user.username }}: {{ user }} {% if not forloop.last %}, {% endif %}
    {% endfor %}
};
var searchUsers = "";

function User(data) {
    var self = this;
    $.extend(self, data.user);
}

function redrawUserList() {
    var keys = [];
    for (key in onlineUsers) {
        if (onlineUsers.hasOwnProperty(key)) {
            keys.push(key);
        }
    }
    keys.sort(function (key1, key2) {
        if (key1.toUpperCase() < key2.toUpperCase()) return -1;
        if (key1.toUpperCase() > key2.toUpperCase()) return 1;
        return 0;
    });
    $("#userlist").empty();
    for (key in keys) {
        if (searchUsers === "" || key.indexOf(searchUsers) != -1) {
            user = onlineUsers[key];
            var li = $('<li/>');
            var image = $('<img/>').attrs({'src':user.image_url, 'alt':'User image'});
            li.append(image);
            li.append(user.username);
            var div = $('<div/>').attrs({'class':'info'});
            div.append(user.info);
            li.append(div);
            $("#userlist").append(li);
        }
    }
}

function updateUserList(data) {
    var user = new User(data.user);
    if (data.action === 'JOIN') {
        if (!onlineUsers.hasOwnProperty(user.username)) {
            onlineUsers[user.username] = user;
            redrawUserList();
        }
    } else if (data.action === 'PART') {
        var index = onlineUsers.indexOf(data);
        if (onlineUsers.hasOwnProperty(user.username)) {
            delete onlineUsers[user.username];
            redrawUserList();
        }
    }
}

$(document).ready(function () {
    $.updates.registerProcessor('home_channel', 'userlist', updateUserList);

    $(".panel .header").click(function () {
        $(this).next("ul").slideToggle("slow");
    });

    $("#search_users").keyup(function () {
        searchUsers = $(this).val();
        redrawUserList();
    });
});
