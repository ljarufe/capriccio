function cambiar_total() {
	$("#id_total").val($("#id_producto option:selected").attr("name"));
}

function select_item(value) {
	$("#id_producto option[value=" + value + "]").attr("selected", true);
	cambiar_total();
}

// Calcular el precio venta en dolares
function aPrecioVenta(precio) {
	cambio = precio / tipo_cambio;
	// cambio += cambio * comision_dinamica / 100 + comision_estática; // por si existe una recarga en el precio
	return dosDecimales(cambio);
}

// Reducir a dos decimales
function dosDecimales(num) {
	return Math.round(num * 100) / 100;
}

$(document).ready(function(){
	
	// Widget para darle estilo a los campos "file"
	// $("#id_imagen").InputFile();
	
	tortas_disponibles();
	$("#id_total").val($("#id_producto option:selected").attr("name"));
	$('#id_total').attr('disabled', true);
	
	// Llenar los precios de cambio de los productos iniciales
	$(".producto-precio").each(function(){
		$(this).next().html("<div class='precio-estilo'>Precio de cambio:</div> $ " + aPrecioVenta(parseFloat($(this).attr('name'))));
	});
		
	//Seleccionar un producto con el boton
	$('.add-carro').click(function(){				
		var value = $(this).attr("id");
		select_item(value);
	});
	
	//Cambiar el total
	$('#id_producto').change(function(){
		cambiar_total();
	});
	
	//Enviar datos
	$("#submit").click(function(event){
		$('.error').hide();		
		var direccion = $('#direccion').val();
		if(direccion == ''){
			$('#direccion-error').show('slow');
			return false;
			event.preventDefault();
		}
		$("#id_total").attr("disabled", false);
		$("#id_total").val($("#id_producto option:selected").attr("name"));
	});
	
	// Aumentar tamaño de las fotos
	$('.imagen-prod').hover(
		function(){
			$(this).css('background-color', '#ffffff');
		},
		function(){
			$(this).css('background-color', '#DDDDDD');
		}
	);
	
	// Desplegar widget del calendario y setear sus propiedades
	$('#id_fecha_entrega').attr('autocomplete', 'off');
	$('#id_fecha_entrega').datepicker({ showOn: 'both' });
	$('#id_fecha_entrega').datepicker( "option", "buttonImage", '/media/img/calendar.png' );
	$('#id_fecha_entrega').datepicker( "option", "buttonImageOnly", true );
	$('#id_fecha_entrega').datepicker( "option", "dateFormat", 'yy-mm-dd' );
	$('#id_fecha_entrega').datepicker( "option", "dayNames", ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sabado'] );
	$('#id_fecha_entrega').datepicker( "option", "dayNamesMin", ['Do', 'Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sa'] );
	$('#id_fecha_entrega').datepicker( "option", "dayNamesShort", ['Dom', 'Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab'] );
	$('#id_fecha_entrega').datepicker( "option", "monthNames", ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Setiembre','Octubre','Noviembre','Diciembre'] );
	$('#id_fecha_entrega').datepicker( "option", "monthNamesShort", ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Set','Oct','Nov','Dic'] );
	$('#id_fecha_entrega').datepicker( "option", "minDate", +1);
	$('#id_fecha_entrega').datepicker( "option", "nextText", 'Siguiente' );
	$('#id_fecha_entrega').datepicker( "option", "prevText", 'Anterior' );
});
