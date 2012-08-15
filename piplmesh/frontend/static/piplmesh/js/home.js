var POSTS_LIMIT = 20;

function Post(data) {
    var self = this;
    $.extend(self, data);

    // Calculates difference between current time and the time when the post was created and generates a message
    function formatPostDate(post_date) {
        // TODO: bug, it doesn't work in chrome on windows
        var created_time_diff = (new Date().getTime() - new Date(post_date).getTime())/1000/60;
        if (created_time_diff < 2) {
            msg = "just now";
        }
        else if (created_time_diff >= 60*24) {
            msg = Math.round(created_time_diff/60/24) + " days ago";
        }
        else if (created_time_diff >= 60) {
            msg = Math.round(created_time_diff/60) + " hours ago";
        }
        else {
            msg = Math.round(created_time_diff) + " minutes ago";
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
            .append($('<span/>').prop('class', 'date').text(formatPostDate(self.created_time))
        );
        post.data("id", data.id);
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
            generateHtml(data).prependTo($(".posts")).hide().toggle('slow');
        }
    }
}

function earlierPosts(){
    var last_post_id = $(".post:last").data("id");
    $.getJSON('/api/v1/post/?limit='+POSTS_LIMIT+'&offset='+last_post_id, function (data) {
        for (var i = 0; i < data.objects.length; i++){
            new Post(data.objects[i]).addToBottom();
        }
    });
}

function postUpdateList(data){
    if (data.action === 'NEW') {
        new Post(data.post).addToTop();
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
            new Post(data.objects[i]).addToBottom();
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
        if (document.body.scrollHeight - $(this).scrollTop() <= $(this).height()) {
            earlierPosts();
        }
    });

});