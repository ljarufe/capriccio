$(document).ready(function() {
	
	// Validar mediante AJAX
	$('#validar_password').click(function(){
		json_url = '/clientes/verificar_password_json/' + $('#old_password').val();
		$.getJSON(json_url, function(respuesta){
			if(respuesta) {
				$('#validacion_password').slideUp('slow');
				$('#cambiar_password').slideDown('slow');
			}
			else {
				$('#cambio-password').slideUp('slow');
				$('#password-error-ok').slideDown('slow');
			}
		});
	});
	
	
	// Verficación de password en la autentificación
	$('#nuevo_password').click(function(event) {
		$('.error').hide();
		var pass1 = $('#password1').val();
		var pass2 = $('#password2').val();
		if(pass1 != pass2) {
			$('#errores-password').show();
			$('#password-error-match').show('slow');
			return false;
			event.preventDefault();
		}
		if(pass1 == '' || pass2 == '') {
			$('#errores-password').show();
			$('#password-error-null').show('slow');
			return false;
			event.preventDefault();
		}
		if(pass1.length < 6) {
			$('#errores-password').show();
			$('#password-error-length').show('slow');
			return false;
			event.preventDefault();
		}
		json_url = '/clientes/cambiar_password_json/' + $('#password2').val();
		$.getJSON(json_url, function(respuesta){
			if(respuesta) {
				$('#cambiar_password').slideUp('slow');
				$('#old_password').text("");
				$('#validacion_password').slideDown('slow');
				$('#cambio-password').slideDown('slow');
			}
			else {
				$('#errores-password').show();
				$('#sintaxis-password').show('slow');
				return false;
				event.preventDefault();
			}
		});
	});
});
