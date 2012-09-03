var POSTS_LIMIT = 20;

function Post(data) {
    var self = this;
    $.extend(self, data);

    // Calculates difference between current time and the time when the post was created and generates a message
    function formatPostDate(post_date) {
        // TODO: check for cross browser compatibility, currently works in Chrome and Firefox on Ubuntu
        var created_time_diff = (new Date().getTime() - new Date(post_date)) / (60 * 1000); // Converting time from milliseconds to minutes
        if (created_time_diff < 1) { // minutes
            msg = gettext("just now");
        }
        else if (created_time_diff >= 60 * 24) { // 24 hours, 1 day
            var days = Math.round(created_time_diff / (60 * 24));
            var format = ngettext("%s day ago", "%s days ago",  (days > 2) ? 3 : days);
            msg = interpolate(format, [days]);
        }
        else if (created_time_diff >= 60) { // 60 minutes, 1 hour
            var hours = [Math.round(created_time_diff / 60)];
            var format = ngettext("%s hour ago", "%s hours ago", (hours > 2) ? 3 : hours);
            msg = interpolate(format, [hours]);
        }
        else {
            var minutes = Math.round(created_time_diff);
            var format = ngettext("%s minute ago", "%s minutes ago",  (minutes > 2) ? 3 : minutes);
            msg = interpolate(format, [minutes]);
        }
        return msg;
    }

    function generateHtml() {
        // TODO: add other post options
        var post_options = $('<ul />').addClass('options')
            .append($('<li/>').append($('<a />').addClass('delete-post').addClass('hand').text(gettext("Delete post"))));

        var post = $('<li/>').addClass('post')
            .append(post_options)
            .append($('<span/>').addClass('author').text(self.author['username']))
            .append($('<p/>').addClass('content').text(self.message))
            .append($('<span/>').addClass('date').text(formatPostDate(self.created_time)));
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
            // TODO: animation has to be considered and maybe improved
            generateHtml(data).prependTo($(".posts")).hide().slideToggle('slow');
        }
    }
}

function showLastPosts(offset){
    $.getJSON(API_POST_URL+'?limit='+POSTS_LIMIT+'&offset='+offset, function (data) {
        $(data.objects).each(function () {
            new Post(this).addToBottom();
        });
    });
}

$(document).ready(function () {
    $.ajaxSetup({
        error: function (jqXHR, textStatus, errorThrown) {
            window.console.error(jqXHR, textStatus, errorThrown);
            alert(gettext("Oops, something went wrong..."));
        }
    });

    $.updates.registerProcessor('home_channel', 'post_new', function (data) {
        new Post(data.post).addToTop();
    });

    $('.panel .header').click(function (event) {
        $(this).next('.content').slideToggle('fast');
    });

    // Saving text from post input box
    var input_box_text = $('#post_text').val();

    // Shows last updated posts, starting at offset 0, limited to POSTS_LIMIT
    showLastPosts(0);

    $('#submit_post').click(function () {
        var message = $('#post_text').val();
        var is_published = true;
         $.ajax({
            type: 'POST',
            url: API_POST_URL,
            data: JSON.stringify({
                    'message': message,
                    'is_published': is_published
            }),
            contentType: 'application/json',
            dataType: 'json',
            success: function (output, status, header) {
                $('#post_text').val(input_box_text);
                $('#post_text').css('min-height', 25);
            }
        });

    });

    $('#post_text').expandingTextArea();
    $('#post_text').focus(function (event) {
        if ($('#post_text').val() == input_box_text) {
            $('#post_text').val('');
        }
        $('#post_text').css('min-height', 50);
    });

    $('#post_text').blur(function (event) {
        if ($('#post_text').val().trim() == '') {
            $('#post_text').val(input_box_text);
            $('#post_text').css('min-height', 25);
        }
    });

    $('#post_text').keydown(function (event) {
        if ($(this).val().trim().length < 1) {
            $('#submit_post').attr('disabled', 'disabled');
        } else {
            $('#submit_post').removeAttr('disabled');
        }
    });

    $(window).scroll(function (event) {
        if (document.body.scrollHeight - $(this).scrollTop() <= $(this).height()) {
            var last_post_id = $('.post:last').data('id');
            if (last_post_id) {
                showLastPosts(last_post_id);
            }
        }
    });
});