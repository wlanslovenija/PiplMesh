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
});

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
        url: '/api/v1/post/500efc446c20b10eb8000003/comments/',
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