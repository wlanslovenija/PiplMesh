var CURRENT_OFFSET = 0;
var LIMIT = 20;

function User(data) {
    var self = this;
    $.extend(self, data);
    self._key = self.username.toLowerCase();
}

function redrawUserList() {
    var keys = [];
    $.each(onlineUsers, function (key, user) {
        keys.push(key);
    });
    keys.sort(function (key1, key2) {
        if (key1 < key2) return -1;
        if (key1 > key2) return 1;
        return 0;
    });
    $('#userlist').empty();

    var searchUsers = $('#search_users').val().toLowerCase();
    $.each(keys, function (i, key) {
        if (searchUsers === '' || key.indexOf(searchUsers) !== -1) {
            var user = onlineUsers[key];
            var li = $('<li/>');
            var image = $('<img/>').prop({
                'src': user.image_url,
                'alt': gettext("User image")
            });
            li.append(image);
            li.append(user.username);
            var div = $('<div/>').prop({
                'class': 'info'
            });
            div.append($('<a/>').prop('href', user.profile_url).text(gettext("User profile")));
            li.append(div);
            $('#userlist').append(li);
        }
    });
}

function updateUserList(data) {
    var user = new User(data.user);
    if (data.action === 'JOIN') {
        onlineUsers[user._key] = user;
        redrawUserList();
    }
    else if (data.action === 'PART') {
        if (onlineUsers[user._key]) {
            delete onlineUsers[user._key];
            redrawUserList();
        }
    }
}

// Calculates difference between current time and the time when the post was created and generates a message
function format_post_date(post_date_created) {
    // TODO: bug, it doesn't work in chrome on windows
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
    if (CURRENT_OFFSET != -1){
        if (CURRENT_OFFSET < LIMIT){
            posts_returned = CURRENT_OFFSET;
            CURRENT_OFFSET = 0;
        } else {
            posts_returned = LIMIT;
            CURRENT_OFFSET -= LIMIT;
        }
        $.getJSON('/api/v1/post/?limit='+LIMIT+'&offset='+CURRENT_OFFSET, function (data) {
            for (var i = posts_returned-1;i>=0;i--){
                add_post_to_bottom(data.objects[i]);
            }
        });
        if (CURRENT_OFFSET == 0){
            CURRENT_OFFSET = -1;
        }
    }

}

$(document).ready(function () {
    $.updates.registerProcessor('home_channel', 'userlist', updateUserList);

    $('.panel .header').click(function (event) {
        $(this).next('ul').slideToggle('fast');
    });

    $('#search_users').change(redrawUserList).keyup(redrawUserList);

    redrawUserList();

    $(".posts").empty();
    $.getJSON('/api/v1/post/?limit=1&offset='+CURRENT_OFFSET, function (data) {
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
                processData:  true
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