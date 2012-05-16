var users = new Array();
var searchUsers;
var alphabeticalOrder = false;
var userList;

function updateUserList(data) {
    if (data.action == 'JOIN') {
        users[users.length] = data;
        if (alphabeticalOrder) {
            rebuildUserList();
        } else {
            addUserOnList(data);
        }
    }else if (data.action == 'PART') {
        users.splice(users.indexOf(data), 1);
        $("#userlist #" + data.id).remove();
    }
}

// adds one user to UserList
function addUserOnList(user) {
    if (user.username.indexOf(searchUsers) != -1) {
        userlist.append("<li id=\"" + user.id + "\">" +
            "<img src=\"" + user.image + "\" alt=\"image\">" + user.username +
            "<div class=\"userInfo\">" + user.info + "</div>" +
            "</li>");
    }
}

// rebuilds userList
function rebuildUserList() {
    var tmpusers = users;
    userList.empty();
    if (alphabeticalOrder) {
        tmpusers.sort(function (user1, user2) {
            if (user1.username.toUpperCase() < user2.username.toUpperCase()) return -1;
            if (user1.username.toUpperCase() > user2.username.toUpperCase()) return 1;
            return 0;
        });
    }
    for (user in tmpusers) {
        addUserOnList(user);
    }
}

$(document).ready(function () {
    var userList = $("#userlist");
    searchUsers = "";
    $.updates.registerProcessor('home_channel', 'userlist', updateUserList);

    $(".panel .header").click(function () {
        $(this).next("ul").slideToggle("slow");
    });

    $("#search_users").keyup(function () {
        searchUsers = $(this).val();
        rebuildUserList();
    });

    $("#alphabet_order").change(function () {
        alphabeticalOrder = false;
        if ($("#alphabet_order").is(":checked")) {
            alphabeticalOrder = true;
        }
        rebuildUserList();
    });
});