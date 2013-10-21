$(document).ready(function() {
		 	
	// Hacer verificaciones antes de enviar el formulario
 	$('#submit').click(function(event){
		$('.error').hide();
		var pass1 = $('#password1').val();
		var pass2 = $('#password2').val();
		if(pass1 != pass2) {
			$('#tr-error').show();
			$('#password-error-match').show('slow');
			return false;
			event.preventDefault();
		}
		if(pass1 == '' || pass2 == '') {
			$('#tr-error').show();
			$('#password-error-null').show('slow');
			return false;
			event.preventDefault();
		}
		if(pass1.length < 6) {
			$('#tr-error').show();
			$('#password-error-length').show('slow');
			return false;
			event.preventDefault();
		}
	});
	
	// evitar el envío de un formulario con enter
	$('form').keypress(function(e){    
		if(e.which == 13) { 
			return false; 
		}
	});
 
	$('input').keypress(function(e){ 
		if(e.which == 13){ 
			return false; 
		} 
	}); 
	
	// Verificar que el email sea único
	$('#id_email').focusout(function(event) {
		json_url = "/clientes/usuario_unico_json/" + $(this).val();
		$.getJSON(json_url, function(respuesta){
			if(respuesta) {
				$('.email-mensajes').hide();
				$('#email-nodisponible').fadeIn('slow');
				$('#submit').css('opacity','0.7');
				$('#submit').attr('disabled','-1');
			}
			else {
				$('.email-mensajes').hide();
				$('#email-disponible').fadeIn('slow');
				$('#submit').css('opacity','1');
				$('#submit').removeAttr('disabled')
			}
		});
	});
	
	$('#id_email').focusin(function(event) {
		$('.email-mensajes').hide();
		$('#email-notificacion').fadeIn('slow');
	});
	
	$('#password1, #password2').focusin(function(event) {
		$('#password-notificacion').fadeIn('slow');
	});
	
	$('#password1, #password2').focusout(function(event) {
		$('#password-notificacion').hide();
	});		 
	
 });
