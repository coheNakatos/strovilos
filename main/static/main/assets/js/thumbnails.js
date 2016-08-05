// A js file to dynamically change the thumbnails on Posts' admin page
$(document).ready( function ()
{
	$('#id_image').attr('id', 'thumbajax');
	$('#thumbajax').change(function()
	{
		var option = $ (this).find('option:selected').text()
		if (option !== "---------" ){ 
			// TODO: Change that when we upload the server. Add domain name instead of ip!
			$.ajax({url:"http://139.59.175.70/ajax?title="+option,
			            success:function(result) {
							if ($('#thumb').length){
								$('#thumb').attr('src',"http://139.59.175.70"+result);
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
			            type:"get"
			        }
			    );
		}
	});
});
