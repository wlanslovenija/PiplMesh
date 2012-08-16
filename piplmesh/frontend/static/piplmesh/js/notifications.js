
$(document).ready(function() {
    $(".notifications").click(function (){
        if ($("#notif_box").hasClass('show')) {
            $("#notif_box").slideUp('fast');
            $("#notif_box").toggleClass('show');
        } else {
            $("#notif_box").slideDown('fast');
            $("#notif_box").toggleClass('show');
        }
    });
    $(".close_notif_box").click(function (){
        if ($("#notif_box").hasClass('show')) {
            $("#notif_box").slideUp('fast');
            $("#notif_box").toggleClass('show');
        }
    });
    $("#addPost").click(function (){
        addPost("Bla bla bla bla Post...");
    });
    $("#addCom").click(function (){
        addComment("Tralala dela");
    });
    
    
    $.updates.registerProcessor('notification_channel', 'notifications', AddNewNotification);

    //$('#notif_content').change(redrawUserList).keyup(redrawUserList);

    loadNotifications();
});


function AddNewNotification(newNotification) {
    console.info($('.username').html());
    var notif = buildNotification(newNotification.notifications)
    var content = '<li class="notification">' + notif.author + notif.content + notif.date + '</li>';
    $('.notification_list').prepend(content)
}

function buildNotification(notification) {
    var new_notif = {};
    new_notif.author = notification.author + ' je komentiral <a href="#" >objavo</a><br />';
    new_notif.message = '<span class="notification_message">' + notification.content + '</span><br />';
    new_notif.date = 'Napisano ' + formatDate(notification.created_time);
    return new_notif;
}


function loadNotifications() {
    $.getJSON('/api/v1/notification/', function(notifications) {
        var list = [];

        $.each(notifications.objects, function(i, notification) {
            var notif = buildNotification(notification)
            list.unshift('<li class="notification">' + notif.author + notif.content + notif.date + '</li>');
        })

        var content = '<ul class="notification_list">' + list.join('') + '</ul>';
        $('#notif_content').html(content);
        console.log('loadNoti');
    });
}

function formatDate(time) {
    //var months = new Array("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December");
    var days = new Array("Pon", "Tor", "Sre", "Čet", "Pet", "Sob", "Ned");
    var months = new Array("Jan", "Feb", "Mar", "Apr", "Maj", "Jun", "Jul", "Avg", "Sep", "Okt", "Nov", "December");
    var time = new Date(time);
    var date = days[time.getDay()] + ', ' + time.getDate() + ' ' + months[time.getMonth()] + ' ' + time.getFullYear() + ', ' + time.getHours() + ':' + time.getMinutes();
    return date;
}

function addPost(message) {
    $.ajax({
        type: 'POST',
        url: '/api/v1/post/',
        data: JSON.stringify({'message': message, 'is_published': true}),
        contentType: 'application/json',
        dataType: "json",
        success: function () {
            alert("Post napisan.");
        },
        error: function (error) {
            console.log(error);
            alert("Oops, something went wrong... ");
        }
    });
}

function addComment(comment) {
    $.ajax({
        type: 'POST',
        //url: '/api/v1/post/500efc446c20b10eb8000003/comments/',
        url: '/api/v1/post/5028f60e6c20b15ae4000001/comments/',
        data: JSON.stringify({'message': comment}),
        contentType: 'application/json',
        dataType: "json",
        success: function () {
            alert("Komentar napisan.");
        },
        error: function (error) {
            console.log(error);
            alert("Oops, something went wrong... ");
        }
    });
}
