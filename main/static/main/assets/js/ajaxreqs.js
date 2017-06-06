$(function() {
	pagination_nav = $('#pagination');
    $(pagination_nav).on("click", "a", function(event) {
    	event.preventDefault();
    	$.ajax({
    		type: "GET",
    		data: {
    			page: $(this).attr('href').split("=")[1],
    		},
    		url: window.location.pathname,
    		success: function(response){
    			var html = $.parseHTML(response);
    			main_content = $(html).find('#content');
    			pagination_content = $(html).find('#pagination')
				$('html, body').animate({
    				scrollTop: ($("#content").offset().top - 100)
				}, 2000);
    			$('#content').fadeOut(600, function(){
    				$('#content').html(main_content);
    				$(this).fadeIn('slow');	
    			});
    			$(pagination_nav).fadeOut(400, function(){
    				$(this).html(pagination_content)
    				$(this).fadeIn('slow');
    			});
    		}
    	})
    })
});