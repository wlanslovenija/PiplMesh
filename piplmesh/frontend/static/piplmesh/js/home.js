var POSTS_LIMIT = 20;
var POSTS_DATE_UPDATE_INTERVAL = 60000; // ms

// Calculates difference between current time and the time when the post was created and generates a message
function formatDiffTime(time) {
    // TODO: Check for cross browser compatibility, currently works in Chrome and Firefox on Ubuntu
    var created_time_diff = (new Date().getTime() - Date.parse(time)) / (60 * 1000); // Converting time from milliseconds to minutes
    if (created_time_diff < 2) { // minutes
        var msg = gettext("just now");
    }
    else if (created_time_diff >= 60 * 24) { // 24 hours, 1 day
        var days = Math.round(created_time_diff / (60 * 24));
        var format = ngettext("%(days)s day ago", "%(days)s days ago", days);
        var msg = interpolate(format, {'days': days}, true);
    }
    else if (created_time_diff >= 60) { // 60 minutes, 1 hour
        var hours = Math.round(created_time_diff / 60);
        var format = ngettext("%(hours)s hour ago", "%(hours)s hours ago", hours);
        var msg = interpolate(format, {'hours': hours}, true);
    }
    else {
        var minutes = Math.round(created_time_diff);
        var format = ngettext("%(minutes)s minute ago", "%(minutes)s minutes ago", minutes);
        var msg = interpolate(format, {'minutes': minutes}, true);
    }
    return msg;
}

function Post(data) {
    var self = this;
    $.extend(self, data);

    function generateHtml() {
        // TODO: Improve and add other post options
        var delete_link = $('<li/>').append(
            $('<a/>').addClass('delete-post').addClass('hand').text(gettext("Delete"))
        );

        var hug = $('<li/>').addClass('hug').append(
            $('<a/>').addClass('hand').text(gettext("Hug"))
        );
        var run = $('<li/>').addClass('run').append(
            $('<a/>').addClass('hand').append(gettext("Run"))
        );

        var post_options = $('<ul />').addClass('options').append(delete_link).append(hug).append(run);

        var huggers = $('<ul/>');
        if (self.hugs.length < 1) {
            huggers.append(
                $('<li/>').addClass('first').text(gettext("No huggers"))
            );
        } else {
            huggers.append(
                $('<li/>').addClass('first').text(gettext("Huggers")+":")
            );
            for (hugger in self.hugs){
                huggers.append($('<li/>').text(self.hugs[hugger]));
            }
        }

        var runners = $('<ul/>');
        if (self.runs.length < 1) {
            runners.append(
                $('<li/>').addClass('first').text(gettext("No runners"))
            );
        } else {
            runners.append(
                $('<li/>').addClass('first').text(gettext("Runners")+":")
            );
            for(var i = 0; i<self.runs.length; i++){
                runners.append($('<li/>').text(self.runs[i]));
            }
        }

        hugs_runs = $('<div/>').addClass('hugs_runs').text(gettext("Hugs") + ": " + self.hugs.length + " "
            + gettext("Runs") + ": " + self.runs.length)
            .append(
            $('<div/>').addClass('hugs_runs_display').append(
                huggers
            ).append(
                runners
            )
        );

        hugs_runs.hover(function () {
                $('.hugs_runs_display', this).show();
            },
            function () {
                $('.hugs_runs_display', this).hide();
            });

        var post = $('<li/>').addClass('post').data('post', self).append(post_options).append(
            $('<span/>').addClass('author').text(self.author.username)
        ).append(
            $('<p/>').addClass('content').text(self.message)
        ).append(
            $('<div/>').addClass('footer').append(
                $('<span/>').addClass('date').text(formatDiffTime(self.created_time))
            ).append(
                hugs_runs
            )
        );

        return post;
    }

    function checkIfPostExists() {
        return $('.post').is(function (index) {
            return $(this).data('post').id == self.id;
        });
    }

    self.addToBottom = function () {
        if (!checkIfPostExists()) {
            $('.posts').append(generateHtml(data));
        }
    };

    self.addToTop = function () {
        if (!checkIfPostExists()) {
            // TODO: Animation has to be considered and maybe improved
            generateHtml(data).prependTo($('.posts')).hide().slideToggle('slow');
        }
    };

    self.updateDate = function (dom_element) {
        $(dom_element).find('.date').text(formatDiffTime(self.created_time));
    }
}

function showLastPosts(offset) {
    $.getJSON(URLS['post'], {'limit': POSTS_LIMIT, 'offset': offset}, function (data) {
        $(data.objects).each(function (i, post) {
            new Post(this).addToBottom();
        });
    });
}

$(document).ready(function () {
    $.updates.registerProcessor('home_channel', 'post_new', function (data) {
        new Post(data.post).addToTop();
    });

    $('.panel .header').click(function (event) {
        $(this).next('.content').slideToggle('fast');
    });

    // Saving text from post input box
    var input_box_text = $('#post_text').val();

    // Shows last updated posts, starting at offset 0, limited by POSTS_LIMIT
    showLastPosts(0);

    $('#submit_post').click(function (event) {
        var message = $('#post_text').val();
        $(this).prop('disabled', true);
        var is_published = true;
        $.ajax({
            'type': 'POST',
            'url': URLS['post'],
            'data': JSON.stringify({
                'message': message,
                'is_published': is_published
            }),
            'contentType': 'application/json',
            'dataType': 'json',
            'success': function (data, textStatus, jqXHR) {
                $('#post_text').val(input_box_text).css('min-height', 25);
            },
            'error': function (jqXHR, textStatus, errorThrown) {
                // There was an error, we enable form back
                $('#submit_post').prop('disabled', false);
            }
        });
    });

    $('#post_text').expandingTextArea().focus(function (event) {
        if ($(this).val() == input_box_text) {
            $(this).val('');
        }
        $(this).css('min-height', 50);
    }).blur(function (event) {
        if (!$(this).val().trim()) {
            $(this).val(input_box_text);
            $(this).css('min-height', 25);
        }
    }).keyup(function (event) {
        if (!$(this).val().trim()) {
            $('#submit_post').prop('disabled', true);
        }
        else {
            $('#submit_post').prop('disabled', false);
        }
    });

    $(window).scroll(function (event) {
        if (document.body.scrollHeight - $(this).scrollTop() <= $(this).height()) {
            var last_post = $('.post:last').data('post');
            if (last_post) {
                showLastPosts(last_post.id);
            }
        }
    });

    // TODO: Improve date updating so that interval is set on each date individually
    setInterval(function () {
        $('.post').each(function (i, post) {
            $(this).data('post').updateDate(this);
        });
    }, POSTS_DATE_UPDATE_INTERVAL);
});