var CURRENT_OFFSET = 1;
var LIMIT = 20;

function updateUserlist(data) {
    if (data.action == 'JOIN') {
        $('<li/>').text(data.username).appendTo('#userlist');
    }
    else if (data.action == 'PART') {
        // TODO: Improve escape and use more suitable :contains method
        $('#userlist li:contains(' + escape(data.username) + ')').remove();
    }
}

// Calculates difference between current time and the time when the post was created and generates a message
function format_post_date(post_date_created) {        
    // TODO: bug, it doesn't work in chrome
    var created_time_diff = (new Date().getTime() - new Date(post_date_created).getTime())/1000/60; 
    if (created_time_diff < 2) {
        msg = "just now";
    } else if (created_time_diff >= 60*24) {
        msg = Math.round(created_time_diff/60/24) + " days ago";
    } else if (created_time_diff >= 60) {
        msg = Math.round(created_time_diff/60) + " hours ago";
    } else {
        msg = Math.round(created_time_diff) + " minutes ago";
    }
    return msg;
}

function generate_post_html(data) {
    return '<li class="post"><span class="author">'+ data.author['username'] + '</span><p class="content">' + data.message + '</p><span class="date">'+ format_post_date(data.created_time) +'</span></li>'
}

function add_post_to_top(post_location){
    $.getJSON(post_location, function (data) {    
        $("li.post:first").before(generate_post_html(data)).hide().fadeIn("slow");
    });
}

function add_post_to_bottom(data){
    $(".posts").append(generate_post_html(data));
}

function earlier_posts (){
    var posts_returned;
    if (CURRENT_OFFSET < LIMIT){
        posts_returned = LIMIT-CURRENT_OFFSET;
        CURRENT_OFFSET = 1;
    } else {
        posts_returned = LIMIT;
        CURRENT_OFFSET -= LIMIT;
    }
    $.getJSON('/api/v1/post/?limit='+LIMIT+'&offset='+CURRENT_OFFSET, function (data) {
        for (var i = posts_returned-1;i>=0;i--){
            //console.log(data.objects[i]);
            add_post_to_bottom(data.objects[i]);
        }
    });
}

$(document).ready(function () {
    $.updates.registerProcessor('home_channel', 'userlist', updateUserlist);
    $(".posts").empty();
    $.getJSON('/api/v1/post/?limit=1&offset=1', function (data) {
        var total_posts = data.meta.total_count;
        if (total_posts > 0){
            if (total_posts > 20){
                CURRENT_OFFSET = total_posts - LIMIT;
                total_posts = LIMIT-1;
            }
            $.getJSON('/api/v1/post/?limit='+LIMIT+'&offset='+CURRENT_OFFSET, function (data) {
                for (var i = total_posts-1;i>=0;i--){
                    add_post_to_bottom(data.objects[i]);
                }
            });
        }
    });
    $('#submit_post').click(function () {
        if ($("#post_text").val().trim() != '') {
            $.ajax({
                type: 'POST',
                url: '/api/v1/post/',
                data: '{"message" : "' + $("#post_text").val().replace('\r\n', '\\r\\n') + '"}',
                contentType: 'application/json',
                success: function (output, status, header) {
                    add_post_to_top(header.getResponseHeader('Location'));
                    $('#post_text').val('Write a post...');
                    $('#post_text').css({'min-height':25});        
                },
                error: function () { 
                    alert("Oops, something went wrong... "); 
                },
                processData:  false
            });                        
        }
    });
    
    $('#post_text').expandingTextArea();
    $('#post_text').click(function () {
        if ($('#post_text').val() == 'Write a post...') {
            $('#post_text').val('');
        }
        $('#post_text').css({'min-height':50});
    });
    
    $(window).scroll(function () {
        if (document.body.scrollHeight - $(this).scrollTop()  <= $(this).height()) {
            earlier_posts();
        }
    });

});