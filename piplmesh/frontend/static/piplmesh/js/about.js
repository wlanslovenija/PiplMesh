$(document).ready(function () {
    $.getJSON('https://api.github.com/repos/wlanslovenija/PiplMesh/contributors', function (data, textStatus, jqXHR) { 
        var contributors = $('<ul/>');
        $.each(data, function (i, contributor) {
            contributors.append( 
                $('<li/>').append(
                    $('<img/>').attr({
                        'src': contributor.avatar_url,
                        'alt': gettext("contributor github picture")
                    })
                ).append(
                    $('<a/>').attr({
                        'href': 'https://github.com/' + contributor.login                    
                    }).append(contributor.login)
                )
            );
        });
        $('.contributors').append(contributors);
    }); 
});
