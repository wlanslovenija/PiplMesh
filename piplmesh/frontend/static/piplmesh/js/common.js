$(document).ready(function () {
    $.ajaxSetup({
        'timeout': 5000,
        'traditional': true
    });

    $(document).ajaxError(function (event, jqXHR, ajaxSettings, thrownError) {
        window.console.error(event, jqXHR, ajaxSettings, thrownError);
        alert(gettext("Oops, something went wrong..."));
    });

    $('.logout_button').click(function (event) {
        navigator.id.logout();
    });

    $('.drop_down_login_container').hover(
        function () {
            $('.drop_down_login_options').show();
        },
        function () {
            $('.drop_down_login_options').hide();
        }
    );

    var max_width = 0;
    $('.field label.main').each(function (index, label) {
        if ($(this).width() > max_width) {
            max_width = $(this).width();
		}
    });
    $('.field label.main').width(max_width);
    $('.align_to_label_width').css('margin-left', max_width);
});

$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});
