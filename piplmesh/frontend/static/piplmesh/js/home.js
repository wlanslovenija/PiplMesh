// TODO add users already online to this array
var users = new Array();
var searchUsers;
var alphabeticalOrder = false;
var userList;

function updateUserList(data) {
    if (data.action == 'JOIN') {
        var index = users.indexOf(data);
        if (index == -1) {
            users[users.length] = data;
            redrawUserList();
        }
    } else if (data.action == 'PART') {
        var index = users.indexOf(data);
        if (index != -1) {
            users.splice(index, 1);
            redrawUserList();
        }
    }
}

// redraws userList
function redrawUserList() {
    var tmpUsers = users.slice();
    userList.empty();
    if (alphabeticalOrder) {
        tmpUsers.sort(function (user1, user2) {
            if (user1.username.toUpperCase() < user2.username.toUpperCase()) return -1;
            if (user1.username.toUpperCase() > user2.username.toUpperCase()) return 1;
            return 0;
        });
    }
    for (user in tmpUsers) {
        if (user.username.indexOf(searchUsers) != -1) {
            userlist.append("<li>" +
                "<img src=\"" + user.image + "\" alt=\"image\">" + user.username +
                "<div class=\"userInfo\">" + user.info + "</div>" +
                "</li>");
        }
    }
}

$(document).ready(function () {
    userList = $("#userlist");
    searchUsers = "";
    $.updates.registerProcessor('home_channel', 'userlist', updateUserList);

    $(".panel .header").click(function () {
        $(this).next("ul").slideToggle("slow");
    });

    $("#search_users").keyup(function () {
        searchUsers = $(this).val();
        redrawUserList();
    });

    $("#alphabet_order").change(function () {
        alphabeticalOrder = false;
        if ($("#alphabet_order").is(":checked")) {
            alphabeticalOrder = true;
        }
        redrawUserList();
    });
});