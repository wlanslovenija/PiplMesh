function updateUserlist(data) {
    if (data.action == 'JOIN') {
        $('<li/>').text(data.username).appendTo('#userlist');
    }
    else if (data.action == 'PART') {
        // TODO: Improve escape and use more suitable :contains method
        $('#userlist li:contains(' + escape(data.username) + ')').remove();
    }
}

$(document).ready(function () {
    $.updates.registerProcessor('home_channel', 'userlist', updateUserlist);

    $.getJSON('/api/v1/post/',function(data){
        console.log(data);
        $.each(data, function(neki){
            if (neki == 'objects'){
                //alert(neki.length);
            }
        });
    });
    
    // TODO: post new msg
    $('#submit_post').click(function () { 
        alert('TODO'); 
    });
    
    $('#post_text').expandingTextArea();
    
    $('#post_text').click(function () {
        $('#post_text').html('');
        $('#post_text').css({'min-height':50});
    });

});
