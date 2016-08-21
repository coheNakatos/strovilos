// A js file to dynamically change the thumbnails on Posts' admin page
$(document).ready( function ()
{
	$('#id_image').change(function()
	{
		var option = $ (this).find('option:selected').text()
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
        				$('<img src="'+result+'" id="thumb" style="max-width:150px; height:auto; max-height:150px;"/>').appendTo(".grp-readonly");
	            	}
	            },
	            error:function(xhr, status, error) {	                
	            },
	            dataType:"text",
			    crossDomain: true,
			});
		}
	});
});
