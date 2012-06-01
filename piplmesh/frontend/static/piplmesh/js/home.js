var POSTS_LIMIT = 20;

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
    var post = $('<li/>').prop('class', 'post')
    .append(
        $('<span/>').prop('class', 'author').text(data.author['username']))
    .append(
        $('<p/>').prop('class', 'content').text(data.message))
    .append(
        $('<span/>').prop('class', 'date').text(format_post_date(data.created_time))
    );
    return post;
}

function add_post_to_top(post_location){
    $.getJSON(post_location, function (data) {
        $(".posts").prepend(generate_post_html(data));
        $(".post:first").hide().toggle("slow");
    });
}

function add_post_to_bottom(data){
    $(".posts").append(generate_post_html(data));
}

function earlier_posts (){
    var number_of_posts = $(".post").length;
    $.getJSON('/api/v1/post/?limit='+POSTS_LIMIT+'&offset='+number_of_posts, function (data) {
        if (data.meta.total_count - number_of_posts >= POSTS_LIMIT) {
            var posts_returned = POSTS_LIMIT;
        } else {
            var posts_returned = data.meta.total_count - number_of_posts;
        }
        for (var i = 0; i < posts_returned; i++){
            add_post_to_bottom(data.objects[i]);
        }
    });
}

function postUpdateList(data){
    if (data.action === 'NEW') {
        add_post_to_top(data.post.location);
    }    
}

$(document).ready(function () {
    $.updates.registerProcessor('home_channel', 'userlist', updateUserList);

    $('.panel .header').click(function (event) {
        $(this).next('ul').slideToggle('fast');
    });

    $('#search_users').change(redrawUserList).keyup(redrawUserList);

    redrawUserList();
    
    $.updates.registerProcessor('home_channel', 'posts', postUpdateList);
    
    $.getJSON('/api/v1/post/?limit='+POSTS_LIMIT+'&offset=0', function (data) {
            if (data.meta.total_count >= POSTS_LIMIT) {
                var posts_returned = POSTS_LIMIT;
            } else {
                var posts_returned = data.meta.total_count;
            }
            for (var i = 0; i < posts_returned; i++) {
                add_post_to_bottom(data.objects[i]);
            }
    });
    
    $('#submit_post').click(function () {
        var message = $('#post_text').val().trim();
        var is_published = true;
        if (message != '') {
            $.ajax({
                type: 'POST',
                url: '/api/v1/post/',
                data: JSON.stringify({'message': message, 'is_published': is_published}),
                contentType: 'application/json',
                dataType: "json",
                success: function (output, status, header) {
                    //add_post_to_top(header.getResponseHeader('Location'));
                    $('#post_text').val('Write a post...');
                    $('#post_text').css({'min-height':25});
                },
                error: function (error) {
                    console.log(error);
                    alert("Oops, something went wrong... ");
                }
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