var POSTS_LIMIT = 20;

function Post(data) {
    var self = this;
    $.extend(self, data);
    // Calculates difference between current time and the time when the post was created and generates a message
    function formatPostDate(post_date) {
        // TODO: bug, it doesn't work in chrome on windows
        var created_time_diff = (new Date().getTime() - new Date(Date.parse(post_date))) / (60 * 1000); // Converting time from milliseconds to minutes

        if (created_time_diff < 2) { // minutes
            msg = "just now";
        }
        else if (created_time_diff >= 60 * 24) { // 24 hours, 1 day
            msg = Math.round(created_time_diff / 60 / 24) + gettext(" days ago");
        }
        else if (created_time_diff >= 60) { // 60 minutes, 1 hour
            msg = Math.round(created_time_diff / 60) + gettext(" hours ago");
        }
        else {
            msg = Math.round(created_time_diff) + gettext(" minutes ago");
        }
        return msg;
    }

    function generateHtml() {
        var post_options = $('<ul/>').prop('class', 'options')
            .append($('<li/>').html('<a class="delete-post hand">Delete post</a>'));

        var post = $('<li/>').prop('class', 'post')
            .append(post_options)
            .append($('<span/>').prop('class', 'author').text(self.author['username']))
            .append($('<p/>').prop('class', 'content').text(self.message))
            .append($('<span/>').prop('class', 'date').text(formatPostDate(self.created_time)));
        post.data('id', data.id);
        return post;
    }

    function checkIfPostExists() {
        return $('.post').is(function (index) {
            return $(this).data('id') == self.id;
        });
    }

    self.addToBottom = function () {
        if (!checkIfPostExists()) {
            $(".posts").append(generateHtml(data));
        }
    }

    self.addToTop = function () {
        if (!checkIfPostExists()) {
            generateHtml(data).prependTo($(".posts")).hide().slideToggle('slow');
        }
    }
}

function showLastPosts(offset){
    $.getJSON('/api/v1/post/?limit='+POSTS_LIMIT+'&offset='+offset, function (data) {
        $(data.objects).each(function () {
            new Post(this).addToBottom();
        });
    });
}

function postUpdateList(data){
    if (data.action === 'NEW') {
        new Post(data.post).addToTop();
    }
}

function savePostFieldInitialState(){
    return $('#post_text').val();
}

$(document).ready(function () {
    $.ajaxSetup({
        error: function (error) {
            console.log(error);
            alert(gettext("Oops, something went wrong..."));
        }
    })
    $.updates.registerProcessor('home_channel', 'posts', postUpdateList);

    $('.panel .header').click(function (event) {
        $(this).next('ul').slideToggle('fast');
    });

    post_initial_state = savePostFieldInitialState();

    // Shows last updated posts, starting at offset 0, limited to POSTS_LIMIT
    showLastPosts(0);

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
                    $('#post_text').val(post_initial_state);
                    $('#post_text').css({'min-height':25});
                }
            });
        }
    });

    $('#post_text').expandingTextArea();
    $('#post_text').focus(function () {
        if ($('#post_text').val() == post_initial_state) {
            $('#post_text').val('');
        }
        $('#post_text').css('min-height', 50);
    });

    $('#post_text').blur(function () {
        if ($('#post_text').val().trim() == '') {
            $('#post_text').val(post_initial_state);
            $('#post_text').css('min-height', 25);
        }
    });

    $(window).scroll(function () {
        if (document.body.scrollHeight - $(this).scrollTop() <= $(this).height()) {
            var last_post_id = $('.post:last').data('id');
            if (last_post_id) {
                showLastPosts(last_post_id);
            }
        }
    });
});