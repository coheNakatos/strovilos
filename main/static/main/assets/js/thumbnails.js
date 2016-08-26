// A js file to dynamically change the thumbnails on Posts' admin page
$(document).ready( function ()
{
	var $image_div = $('.grp-readonly')
	$('#id_image').change(function()
	{
		var option = $(this).find('option:selected').text()
		if (option !== "---------" ){ 
			$.ajax({
				type: "GET",
				url:"/ajax?title="+option,
	            success:function(result) {
					if ($('#thumb').length){
						$('#thumb').attr('src',result);
	            	}
	            	else
	            	{
	            		$image_div.empty();
        				$image_div.append('<img src="'+result+'" id="thumb" style="max-width:150px; height:auto; max-height:150px;"/>');
	            	}
	            },
	            dataType:"text",
			    crossDomain: true,
			    statusCode: {
			    	404: function(){
						$image_div.empty();
        				$image_div.append('<p> Η εικόνα δεν βρέθηκε</p>');
			    	},
			    	410: function () {
						$image_div.empty();
        				$image_div.append('<p> Το όνομα της εικόνας υπάρχει 2 ή περισσότερες φορές.Μετονόμασε την.</p>');
			    	}
			    },
			});
		}
	});
});
