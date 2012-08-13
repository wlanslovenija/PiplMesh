var POSTS_LIMIT = 20;

function Post(data) {
    var self = this;
    $.extend(self, data);

    // Calculates difference between current time and the time when the post was created and generates a message
    this.__format_post_date = function (post_date) {
        // TODO: bug, it doesn't work in chrome on windows
        var created_time_diff = (new Date().getTime() - new Date(post_date).getTime())/1000/60;
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

    this.__generate_html = function () {
        var post_options = $('<ul/>').prop('class', 'options')
            .append($('<li/>').html('<a class="delete-post hand">Delete post</a>'));

        var post = $('<li/>').prop('class', 'post')
            .append(post_options)
            .append($('<span/>').prop('class', 'author').text(this.author['username']))
            .append($('<p/>').prop('class', 'content').text(this.message))
            .append($('<span/>').prop('class', 'date').text(this.__format_post_date(this.created_time))
        );
        post.data("id", data.id);
        return post;
    }

    this.__check_if_post_exists = function () {
        var posts_number = $('.post').length;
        for (var i=0; i<posts_number; i++) {
            if ($($('.post')[i]).data("id") == this.id) {
                return true;
            }
        }
        return false;
    }

    this.add_to_bottom = function () {
        if (!this.__check_if_post_exists()) {
            $(".posts").append(this.__generate_html(data));
        }
    }

    this.add_to_top = function () {
        if (!this.__check_if_post_exists()) {
            this.__generate_html(data).prependTo($(".posts")).hide().toggle('slow');
        }
    }
}

function earlier_posts(){
    var last_post_id = $(".post:last").data("id");
    $.getJSON('/api/v1/post/?limit='+POSTS_LIMIT+'&offset='+last_post_id, function (data) {
        for (var i = 0; i < data.objects.length; i++){
            new Post(data.objects[i]).add_to_bottom();
        }
    });
}

function postUpdateList(data){
    if (data.action === 'NEW') {
        new Post(data).add_to_top();
    }
}

$(document).ready(function () {
    $.updates.registerProcessor('home_channel', 'posts', postUpdateList);

    $('.panel .header').click(function (event) {
        $(this).next('ul').slideToggle('fast');
    });

    // Shows last updated posts, limited to POSTS_LIMIT
    $.getJSON('/api/v1/post/?limit='+POSTS_LIMIT+'&offset=0', function (data) {
        for (var i = 0; i < data.objects.length; i++) {
            new Post(data.objects[i]).add_to_bottom();
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
                    $.getJSON(header.getResponseHeader('Location'), function (data) {
                        new Post(data).add_to_top();
                    });
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

    $('#post_text').blur(function () {
        if ($('#post_text').val().trim() == '') {
            $('#post_text').val('Write a post...');
            $('#post_text').css({'min-height': 25});
        }
    });

    $(window).scroll(function () {
        if (document.body.scrollHeight - $(this).scrollTop()  <= $(this).height()) {
            earlier_posts();
        }
    });

});