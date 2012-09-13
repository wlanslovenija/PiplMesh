$(document).ready(function() {
    $.getJSON("https://api.github.com/repos/wlanslovenija/PiplMesh/contributors", "PiplMesh", function(data){
        $.each(data, function(i,element){
            var contributors = $('<span>').append(
                $('<img/>').attr({
                    src: element.avatar_url,
                    alt: 'github ' + element.login + ' picture'
                })
            ).append(
                $('<a/>').attr({
                href: 'https://github.com/' + element.login                    
                }).append(element.login)
            );
            $('.contributors').append(contributors);
        });
	    
	}); 
});