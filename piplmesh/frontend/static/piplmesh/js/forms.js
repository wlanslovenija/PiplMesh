$(document).ready(function () {  
    var max = 0;  
    $("label").each(function(){  
        if ($(this).width() > max)  
            max = $(this).width();     
    });  
    $("label").width(max);  
    $("form .buttons, .errorlist, #password_change, .contact_comment p, .login h1, .registration h1, .contact_form h1").css({ "margin-left": max });
}); 
