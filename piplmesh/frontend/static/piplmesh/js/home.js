var POSTS_LIMIT = 20;
var POSTS_DATE_UPDATE_INTERVAL = 60000; // ms

function howManyColumns() {
    var panelsWidth = $('#panels').innerWidth();
    var columnPanelsWidth = $('.panels_column').outerWidth();

    return parseInt(panelsWidth / columnPanelsWidth);
}

function movePanel(name, columnIndex) {
    $('#panel-' + name).appendTo($('#panels').children().eq(columnIndex));
}

function initializeEmptyColumnsForPanels() {
    var panels = $('.panel').detach();
    var currentColumns = $('#panels').children().length;
    var numberOfColumns = howManyColumns();

    for (var i = currentColumns; i < numberOfColumns; i++) {
        var newColumn = $('<div/>');
        newColumn.addClass('panels_column');
        $('#panels').append(newColumn);
    }

    var removeColumsFromIndex = numberOfColumns - 1;
    $('#panels').find('.panels_column:gt(' + removeColumsFromIndex + ')').remove();
    panels.appendTo('.panels_column:first');
}

function orderPanelsDefault() {
    var numberOfColumns = howManyColumns();

    $('.panel').each(function (index, panel) {
        var toColumn = index % numberOfColumns;
        var columns = $('#panels').children();

        $(panel).appendTo(columns.eq(toColumn));
    });
}

function sendOrderOfPanelsToServer() {
    var names = [];
    var columns = [];
    var numberOfColumns = 0;

    $('#panels').children().each(function (i, column) {
        numberOfColumns++;
        $(column).children().each(function (j, panel) {
            names.push($(panel).prop('id').substr('panel-'.length));
            columns.push(i);
        });
    });

    if (numberOfColumns) {
        $.post(URLS.panels_order, {
            'names': names,
            'columns': columns,
            'number_of_columns': numberOfColumns
        });
    }
}

function orderPanels() {
    $.getJSON(URLS.panels_order, {
        'number_of_columns': howManyColumns()
    }, function (data, textStatus, jqXHR) {
        if (data.length == 0) {
            orderPanelsDefault();
        }
        else {
            $.each(data, function (i, column) {
                $.each(column, function (j, panel) {
                    movePanel(panel, i);
                });
            });
        }
    });
}

function collapsePanels() {
    $.getJSON(URLS.panels_collapse, function (data, textStatus, jqXHR) {
        $.each(data, function (name, collapsed) {
            if (collapsed) {
                $('#panel-' + name + ' .content').css('display', 'none');
            }
        });
    });
}

function initializePanels() {
    initializeEmptyColumnsForPanels();
    orderPanels();
    collapsePanels();
    makeColumnsSortable();
    makePanelsOrderUpdatable();
}

function makeColumnsSortable() {
    $('.panels_column').sortable({
        'connectWith': '.panels_column',
        'handle': '',
        'cursor': 'move',
        'placeholder': 'placeholder',
        'forcePlaceholderSize': true,
        'opacity': 0.6,
        'helper': 'clone'
    }).disableSelection();
}

function makePanelsOrderUpdatable() {
    $('.panels_column').bind('sortstop', function (event, ui) {
        sendOrderOfPanelsToServer();
    });
}

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

    function createDOM() {
        // TODO: Improve and add other post options
        var delete_link = $('<li/>').append(
            $('<a/>').addClass('delete-post').addClass('hand').text(gettext("Delete"))
        );
        var edit_link = $('<li/>').append(
            $('<a/>').addClass('edit-post').addClass('hand').text(gettext("Edit"))
        );
        var post_options = $('<ul />').addClass('options').append(edit_link, delete_link);
        
        // TODO: Author link shouldn't be hardcoded.
        var author_link = $('<a/>').attr('href', '/user/' + self.author.username).addClass('author').addClass('hand').text(self.author.username);
        
        var post = $('<li/>').addClass('post').data('post', self).append(post_options).append(
            $('<span/>').append(author_link)
        ).append(
            $('<p/>').addClass('content').text(self.message)
        ).append(
           $('<span/>').addClass('date').text(formatDiffTime(self.created_time))
        ).append(
           $('<span/>').append($('<ul/>').addClass('comments'))
        ).append(
           $('<span/>').append(createCommentForm()
        ));
        
        return post;
    }
    
    function createCommentForm() {
        // TODO: Instead of creating forms use a static form from template, clone it and append event handlers.
        var textarea = $('<textarea/>').addClass('comment_text').data('post', self).attr('id', 'comment_text');
        var input = $('<input/>').attr('type', 'button').attr('value', 'submit')
        .attr('name','submit_comment').attr('id', 'submit_comment')
        .click(function (event) {
            // TODO: Disable enable submit button like with the Post. After submitting clear the textarea of text.
            // TODO: Push new comments to all clients and display them automatically.
            var message = textarea.val();
            addComment(message, buildCommentURL(self.id));
        });
        var form = $('<form/>').attr('id', 'comment_form').append(textarea, input);
        
        return form;
    }
    
    function getComment(url) {
        $.getJSON(url, function (data, textStatus, jqXHR) {
            new Comment(data, self).appendToPost();
        });
    }
    
    function displayComments() {
        // TODO: We call comments in the right order but that doesn't mean we get them in the right order aswell. Should make some ordering down the road.
        $.each(self.comments, function (index, value) {
            getComment(value);
        });
    }
    
    function checkIfPostExists() {
        return $('.post').is(function (index) {
            return $(this).data('post').id == self.id;
        });
    }

    function postByUser() {
        var user_posts_URIs = $('.posts').data('user_posts_URIs');
        var full_resource_uri = getLocation(self.resource_uri).href;
        return $.inArray(full_resource_uri, user_posts_URIs) != -1;
    }

    function showPost(post) {
        // TODO: Animation has to be considered and maybe improved
        post.show('fast');
    };

    self.addToBottom = function () {
        if (checkIfPostExists()) return;
        
        $('.posts').append(createDOM());
        displayComments();
    };

    self.addToTop = function () {
        if (checkIfPostExists()) return;

        var post = createDOM().hide().prependTo($('.posts'));
        displayComments();
        
        if (postByUser()) {
            // TODO: Maybe we should remove URI after showing user's post
            showPost(post);
            return;
        }

        if (!autoShowIncomingPosts()) {
            post.addClass('notShown');
        }
        else {
            showPost(post);
        }
        updateHiddenPostsCount();
        $('#toggle_queue').show();
        if (!autoShowIncomingPosts()) {
            $('#posts_in_queue, #show_posts').show();
        }
    };

    self.updateDate = function (dom_element) {
        $(dom_element).find('.date').text(formatDiffTime(self.created_time));
    };
}

function Comment(data, post) {
    var self = this;
    $.extend(self, data);
    self.post = post;
    
    function createDOM() {
        // TODO: Author link shouldn't be hardcoded.
        var author_link = $('<a/>').attr('href', '/user/' + self.author.username).addClass('author').addClass('hand').text(self.author.username);
        var comment = $('<li/>').addClass('comment').append(
            $('<span/>').append(author_link)).append($('<p/>').addClass('content').text(self.message)
        ).append($('<span/>').addClass('date').text(formatDiffTime(self.created_time)));
           // TODO: There is a bug when DiffTime is updated it takes time from the post and not the comment.
        return comment;
    }
    
    self.appendToPost = function () {
        $('.post').is(function (index) {
            if ($(this).data('post').id == self.post.id) {
                $(this).find('.comments').append(createDOM());
            }
        });
    };
 }

function loadPosts(offset) {
    $.getJSON(URLS.post, {
        'limit': POSTS_LIMIT,
        'offset': offset
    }, function (data, textStatus, jqXHR) {
        $.each(data.objects, function (i, post) {
            new Post(post).addToBottom();
        });
    });
}

function Notification(data) {
    var self = this;
    $.extend(self, data);

    function createDOM() {
        var format = gettext("%(author)s commented on post.");
        var author = interpolate(format, {'author': self.comment.author.username}, true);

        var notification = $('<li/>').addClass('notification').data('notification', self).append(
            $('<span/>').addClass('notification_element').text(author)
        ).append(
            $('<span/>').addClass('notification_message').addClass('notification_element').text(self.comment.message)
        ).append(
            $('<span/>').addClass('notification_element').addClass('notification_created_time').text(formatDiffTime(self.created_time))
        );

        return notification;
    }

    function checkIfNotificationExists() {
        return $('.notification').is(function (index) {
            return $(this).data('notification').id == self.id;
        });
    }

    self.add = function () {
        if (checkIfNotificationExists()) return;

        if (!self.read) {
            $('#notifications_count').text(parseInt($('#notifications_count').text()) + 1);
        }
        $('#notifications_list').prepend(createDOM());
    };

    self.updateDate = function (dom_element) {
        $(dom_element).find('.notification_created_time').text(formatDiffTime(self.created_time));
    }
}

function loadNotifications() {
    $.getJSON(URLS.notifications, function (data, textStatus, jqXHR) {
        $.each(data.objects, function (i, notification) {
            new Notification(notification).add();
        });
    });
}

// TODO: We should import url from Django not hardcode it.
function buildCommentURL(post_id) {
    return URLS.post + post_id + '/comments/';
}

function addComment(comment, comment_url) {
    $.ajax({
        'type': 'POST',
        'url': comment_url,
        'data': JSON.stringify({'message': comment}),
        'contentType': 'application/json',
        'dataType': 'json',
        'success': function (data, textStatus, jqXHR) {
            alert("Comment posted.");
        }
    });
}

function autoShowIncomingPosts() {
    return $('#toggle_queue_checkbox').is(':checked');
}

function updateHiddenPostsCount() {
    var unread_count = $('ul > li.notShown').length;
    var format = ngettext("There is %(count)s new post", "There are %(count)s new posts", unread_count);
    var msg = interpolate(format, {'count': unread_count}, true);
    $('#posts_in_queue').text(msg);
}

function showHiddenPosts() {
    // TODO: Animation has to be considered and maybe improved
    $('ul > li.notShown').show('fast').removeClass('notShown');
}

$(document).ready(function () {
    initializePanels();

    // List of URIs of posts by user
    $('.posts').data('user_posts_URIs', []);

    $.updates.registerProcessor('home_channel', 'post_new', function (data) {
        new Post(data.post).addToTop();
    });

    $('.panel .header').click(function (event) {
        var collapsed = $(this).next().is(':visible');
        $(this).next('.content').slideToggle('fast');

        var name = $(this).parent().prop('id').substr('panel-'.length);

        $.post(URLS.panels_collapse, {
            'name': name,
            'collapsed': collapsed
        });
    });

    // TODO: Ajax request to store panels state is currently send many times while resizing, it should be send only at the end
    $(window).resize(function (event) {
        initializePanels();
    });

    // Saving text from post input box
    var input_box_text = $('#post_text').val();

    // Shows last updated posts, starting at offset 0, limited by POSTS_LIMIT
    loadPosts(0);

    $('#submit_post').click(function (event) {
        var message = $('#post_text').val();
        $(this).prop('disabled', true);
        var is_published = true;
        $.ajax({
            'type': 'POST',
            'url': URLS.post,
            'data': JSON.stringify({
                'message': message,
                'is_published': is_published
            }),
            'contentType': 'application/json',
            'dataType': 'json',
            'success': function (data, textStatus, jqXHR) {
                var full_post_uri = getLocation(jqXHR.getResponseHeader('location')).href;
                $('.posts').data('user_posts_URIs').push(full_post_uri);
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

    $('#show_posts > input').click(function (event) {
        showHiddenPosts();
        $('#posts_in_queue, #show_posts, #toggle_queue').hide();
    });

    $('#toggle_queue > input').click(function (event) {
        if (autoShowIncomingPosts()) {
            showHiddenPosts();
            updateHiddenPostsCount();
        }
        else {
            $('#toggle_queue').hide();
        }
        $('#posts_in_queue, #show_posts').hide();
    });

    $(window).scroll(function (event) {
        if (document.body.scrollHeight - $(this).scrollTop() <= $(this).height()) {
            var last_post = $('.post:last').data('post');
            if (last_post) {
                loadPosts(last_post.id);
            }
        }
    });

    // Notifications
    $('#notifications_count').add('.close_notifications_box').click(function (event) {
        $('#notifications_box').slideToggle('fast');
    });

    $.updates.registerProcessor('user_channel', 'notification', function (data) {
        new Notification(data.notification).add();
    });

    loadNotifications();

    // TODO: Improve date updating so that interval is set on each date individually
    setInterval(function () {
        $('.post').each(function (i, post) {
            $(post).data('post').updateDate(this);
        });
        $('.notification').each(function (i, notification) {
            $(notification).data('notification').updateDate(this);
        });
    }, POSTS_DATE_UPDATE_INTERVAL);
});
