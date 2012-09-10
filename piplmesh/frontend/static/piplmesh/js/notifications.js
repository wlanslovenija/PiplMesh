
$(document).ready(function () {
    $('.notifications').click(function (){
        $('#notif_box').slideToggle('fast');
    });
    $(".close_notif_box").click(function (){
        $('#notif_box').slideToggle('fast');
    });
    $('#addCom').click(function (){
        addComment("HAHAHAH dela");
    });

    $.updates.registerProcessor('user_channel', 'notifications', AddNewNotification);

    loadNotifications();
});


function AddNewNotification(newNotification) {
    $('.notifications').html(parseInt($('.notifications').html())+1);
    var notif = buildNotification(newNotification.notifications)
    var content = '<li class="notification">' + notif.author + notif.message + notif.date + '</li>';
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
    $.getJSON(URLS['notifications'], function (notifications) {
        var list = [];
        var unread_counter = 0;
        $.each(notifications.objects, function (i, notification) {
            if (notification.read == false) {
                unread_counter += 1;
            }
            var notif = buildNotification(notification);
            list.unshift('<li class="notification">' + notif.author + notif.message + notif.date + '</li>');
        })

        var content = '<ul class="notification_list">' + list.join('') + '</ul>';
        $('#notif_content').html(content);
        $('.notifications').html(unread_counter);
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

function addComment(comment) {
    $.ajax({
        type: 'POST',
        url: '/api/v1/post/504da96e6c20b1163738747f/comments/',
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
