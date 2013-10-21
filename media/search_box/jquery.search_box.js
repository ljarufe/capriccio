(function($){
	$.fn.SearchBox = function(database, on_enter_method, user_options) {
		
		var options;

		options = {	normal_bg_color: '#FFFFFF',
					normal_font_color: '#4d4d4d',
					select_bg_color: '#EEEEEE',
					select_font_color: '#666666',
					box_img: ''
				  };
				  
		options = $.extend(options, user_options);
		
		var item_index = 0;
		var items_busqueda = new Array();
		var index_busqueda = 0;
		var items_number = 0;
		var current = 0;
		
		// Changing the id of the input field
		$(this).attr('id', 'search_box_input');
		
		// Autocomplete off
		$(this).attr('autocomplete', 'off');
		
		// Use the options
		$(this).css('backgroundImage', 'url(' + options.box_img + ')');
		
		// Draw result area
		$(this).after("<div class='search_box_all'><ul></ul></div>");
		
		// Search
		$(this).keyup(function(event) {
			var key = event.keyCode;
			
			// down key
			if(key == 38){
				temp_current = "#" + current;
				$(temp_current).parent().css("background-color", options.normal_bg_color);
				$(temp_current).parent().css("color", options.normal_font_color);
				current = items_busqueda[(--index_busqueda)%items_busqueda.length];
				temp_current = "#" + current;
				$(temp_current).parent().css("background-color", options.select_bg_color);
				$(temp_current).parent().css("color", options.select_font_color);
				return false;
				event.preventDefault();
			}
			
			// up key
			if(key == 40){
				temp_current = "#" + current;
				$(temp_current).parent().css("background-color", options.normal_bg_color);
				$(temp_current).parent().css("color", options.normal_font_color);
				current = items_busqueda[(++index_busqueda)%items_busqueda.length];
				temp_current = "#" + current;
				$(temp_current).parent().css("background-color", options.select_bg_color);
				$(temp_current).parent().css("color", options.select_font_color);
				return false;
				event.preventDefault();
			}
			
			// Show action - editable
			if(key == 13) {
				on_enter_method(current);
				$('.search_box_all').slideUp('fast');
				return false;
				event.preventDefault();
			}

			// Fill the Result area
			buscar = $(this).val();
			if(buscar == '') {
				$('.search_box_all').hide();
			}
			else {
				var index = 0;				
				$('.search_box_all > ul').html('');
				items_busqueda = new Array();
				for(var j = 0 ; j < database.length ; j++) {
					var producto = database[j][1];
					var match = producto.substr(0, buscar.length);
					if(buscar.toLowerCase() == match.toLowerCase()){
						$('.search_box_all > ul').append("<li><div class='search_box_item' id='" + database[j][0] + "' title='" + database[j][2] + "'><img src='" + database[j][3] + "' width='40px' height='40px' /><div class='search_box_item_name'>" + database[j][1] + "</div></div></li>");
						items_busqueda[index] = database[j][0];
						index++;
					}
				}
				index_busqueda = Math.pow(index, 4) - 1;
				$('.search_box_all').slideDown('fast');
			}
		});
		
		// highlight and de-highlight item
		$('.search_box_item').live('mouseover', function(){
			$(this).parent().css("background-color", options.select_bg_color);
			$(this).parent().css("color", options.select_font_color);
		});
		$('.search_box_item').live('mouseleave', function(){
			$(this).parent().css("background-color", options.normal_bg_color);
			$(this).parent().css("color", options.normal_font_color);
		});

		// Show action - editable
		$('.search_box_item').live('click', function(event){
			on_enter_method($(this).attr('id'));
			$('.search_box_all').slideUp('fast');
			return false;
			event.preventDefault();
		});

		// Close search result
		$('*').not('.search_box_item').click(function(){
			$('.search_box_all').slideUp('fast');
		});
	}
})(jQuery);
