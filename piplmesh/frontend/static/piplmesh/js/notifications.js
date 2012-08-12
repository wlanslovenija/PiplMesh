
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
        addComment("Bla bla bla bla");
    });
    
    
    $.updates.registerProcessor('home_channel', 'notifications', AddNewNotification);

    //$('#notif_content').change(redrawUserList).keyup(redrawUserList);

    loadNotifications();
    
});


function AddNewNotification(newNotification) {
    console.info(newNotification);
    alert('uuuu');
}


function loadNotifications() {
    $.getJSON('/api/v1/notification/', function(notifications) {
        var list = [];
        
        $.each(notifications.objects, function(i, notification) {
            var author = notification.author + ' je komentiral <a href="#" >objavo</a><br />';
            var message = '<span class="notification_message">' + notification.message + '</span><br />';
            var date = 'Napisano ' + formatDate(notification.created_time);
            
            list.push('<li class="notification">' + author + message + date + '</li>');
        })
        
        var content = '<ul class="notification_list">' + list.join('') + '</ul>';
        $('#notif_content').html(content);
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
        url: '/api/v1/post/502403fd6c20b105dc000004/comments/',
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