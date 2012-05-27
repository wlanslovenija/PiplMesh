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

function add_post_to_top(post_location){
    $.getJSON(post_location, function (data){
        var created_time = data.created_time;
        $("li.post:first").before($('<li class="post"><span class="author">'+ data.author['username'] + '</span><p class="content">' + data.message + '</p><span class="date">'+ created_time +'</span></li>').hide().fadeIn("slow"));
    });
}

function add_post_to_bottom(post_location){
    $.getJSON(post_location, function(data){
        var created_time = data.created_time;
        $(".posts").append('<li class="post"><span class="author">'+ data.author['username'] + '</span><p class="content">' + data.message + '</p><span class="date">'+ created_time +'</span></li>');
    })
}

$(document).ready(function () {
    $.updates.registerProcessor('home_channel', 'userlist', updateUserlist);
    $(".posts").empty();
    $.getJSON('/api/v1/post/?limit=1&offset=1',function(data){
        var total_posts = data.meta.total_count;
        var offset = 1;
        if (total_posts > 20){
            offset = total_posts - LIMIT;
            total_posts = 20-1;
        }
        $.getJSON('/api/v1/post/?limit=20&offset='+offset, function(data){
            for (var i = total_posts;i>0;i--){
                var created_time = data.objects[i].created_time;
                $(".posts").append('<li class="post"><span class="author">'+ data.objects[i].author['username'] + '</span><p class="content">' + data.objects[i].message + '</p><span class="date">'+ created_time +'</span></li>');
            }
        });
    });
    $('#submit_post').click(function () {
        $.ajax({
            type: 'POST',
            url: '/api/v1/post/',
            data: '{"message" : "' + $("#post_text").val() + '"}',
            contentType: 'application/json',
            success: function(output, status, header) {
                add_post_to_top(header.getResponseHeader('Location'));
                $("textarea#post_text").val('Write a post...');
            },
            error: function(){ alert("Oops, something went wrong... "); },
            processData:  false
        });
    });
    $('#post_text').expandingTextArea();
    $('#post_text').click(function () {
        $('#post_text').html('');
        $('#post_text').css({'min-height':50});
    });
});
