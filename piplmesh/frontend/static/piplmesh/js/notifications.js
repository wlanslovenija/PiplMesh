$(document).ready(function() {
	$(".notifications").click(function (){
		if ($("#notif_box").hasClass('show')) {
			$("#notif_box").slideUp('fast');
			$("#notif_box").toggleClass('show');
		} else {
			$("#notif_box").slideDown('fast');
			$("#notif_box").toggleClass('show');
		}
	});
	$(".close_notif_box").click(function (){
		if ($("#notif_box").hasClass('show')) {
			$("#notif_box").slideUp('fast');
			$("#notif_box").toggleClass('show');
		}
	});
});