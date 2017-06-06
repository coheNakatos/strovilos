$(function () {
	var fixHelper = function(e, ui) {  
		ui.children().each(function() {  
			$(this).width($(this).width());  
		});  
		return ui;  
	};
	$sortable_container = $("tbody") 
	$sortable_container.sortable({  
 		helper: fixHelper  
 	}).disableSelection();  
	
	$("thead th").each(function(){
		$(this).attr('style', 'width:'+ $(this).width() + 'px !important;');
	});
	
	$("tr.grp-row").each(function(){
		data_id = $(this).find("td.field-position").html()
		$(this).attr('data-id', data_id)
		$(this).addClass('about__wrapper')
	});

	$button = $("#button");
	csrf_token = $button.prev("input").attr('value');
	$button.click(function(){
		var jsonData = {};
		$sortable_container.children().each(function(i){
			original_id = $(this).attr("data-id");
			final_id = i + 1
			if (original_id != final_id) jsonData[original_id] = final_id;
		});

		$.ajax({
			data: JSON.stringify(jsonData),
			type: "POST",
			url	: '/ajax/update-cvs',
			contentType: 'application/json',
			beforeSend: function(xhr, settings){
				if (!this.crossDomain) {
					xhr.setRequestHeader("X-CSRFToken", csrf_token);
				}
			},
			success: function (result) {
				location.reload();
			},
		});	
	});
});