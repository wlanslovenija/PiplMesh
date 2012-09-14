$(document).ready(function () {
    $.getJSON('https://api.github.com/repos/wlanslovenija/PiplMesh/contributors', function(data) { 
        var contributors = $('<ul/>');
        $.each(data, function(i, contributor){
            var contributor = $('<li/>').append(
                $('<img/>').prop({
                    'src': contributor.avatar_url,
                    'alt': gettext("contributor github picture")
                })
            ).append(
                $('<a/>').prop({
                    'href': 'https://github.com/' + contributor.login                    
                }).append(contributor.login)
            );
            contributors.append(contributor);
        });
        $('.contributors').append(contributors);
    }); 
});