(function($){
	$.fn.InputFile = function() {
		
		// Set the opacity to 0 in the real input file
		$(this).css('opacity', 0);
		
		$(this).after("<input type='text' id='input_file_text'>");
		$(this).css('z-index', 2);
		$('#input_file_text').css('z-index', 1);
		$('#input_file_text').css('position', 'absolute');
		
		var position = $(this).position();
		position.top += $(this).height();
		$('#input_file_text').css('left', position.left);
		$('#input_file_text').css('top', position.top);
		
	}
})(jQuery);
