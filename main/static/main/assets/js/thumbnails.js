// A js file to dynamically change the thumbnails on Posts' admin page
$(document).ready( function ()
{
	$('#id_image').attr('id', 'thumbajax');
	$('#thumbajax').change(function()
	{
		var option = $ (this).find('option:selected').text()
		if (option !== "---------" ){ 
			// TODO: Change that when we upload the server
			$.ajax({url:"http://localhost:8000/ajax?title="+option,
			            success:function(result) {
							if ($('#thumb').length){
								$('#thumb').attr('src',"http://localhost:8000"+result);
			            	}
			            	else
			            	{
	            				$('<img src="'+result+'" id="thumb" style="max-width:150px; height:auto; max-height:150px;"/>').appendTo(".grp-readonly");

			            	}
			            },
			            error:function(xhr, status, error) {
			                
			            },
			            dataType:"text",
			            type:"get"
			        }
			    );
		}
	});
});
