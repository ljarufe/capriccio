function get_producto(id, item_index){
	json_url = "/ventas/producto_json/" + id;
	$.getJSON(json_url, function(producto){
		$(current_item).prepend("<input type='hidden' name='id-producto" + item_index + "' value='" + producto.id + "'>");
		$(current_item).prepend("<input type='text' class='precio-producto' value='" + aPrecioVenta(producto.precio) + "' name='precio-producto" + item_index + "' readonly> ");
		$(current_item).prepend("Precio: ");
		$(current_item).prepend("<input type='text' class='nombre-producto' value='" + producto.nombre + "' name='nombre-producto" + item_index + "' readonly> ");
		$(current_item).prepend("Producto: ");							
	});	
}

function get_confirmacion(){
    url = "/ventas/confirma";
    $.getJSON(url,function(respuesta){
        resultado = respuesta.verdad;
        if(resultado==1){
            url_session = '/ventas/session';
            $.getJSON(url_session,function(lista){
               lista_addCarro = $(".add-carro");
               for(j=0;j<lista_addCarro.length;j++){
                   habilitado = $(lista_addCarro[j]).attr("name");
                   for (i=0;i<lista.length;i++){
                       if(habilitado==lista[i].id){
                           $("#listaCarro .listaPlus").append("<div id='list" + lista[i].id + "' style='font-size:10px;'>Producto :" + lista[i].nombre + " | Precio :" + lista[i].precio + "</div>");
                           current_item = "#item" + i;
                           $("#total").before("<li class='item' id='item" + i + "'></li>");
                           $(current_item).prepend("<input type='hidden' name='id-producto" + i + "' value='" + lista[i].id + "'>");
                           $(current_item).prepend("<input type='text' class='precio-producto' value='" + aPrecioVenta(lista[i].precio) + "' name='precio-producto" + i + "' readonly> ");
                           $(current_item).prepend("Precio: ");
                           $(current_item).prepend("<input type='text' class='nombre-producto' value='" + lista[i].nombre + "' name='nombre-producto" + i + "' readonly> ");
                           $(current_item).prepend("Producto: ");
                           $(current_item).append("Cantidad: ");
                           $(current_item).append("<input class='cantidad-producto' type='text' value='1' name='cantidad-producto" + i + "'>");
                           $(current_item).append("<button class='remove-item' idb='" + lista[i].id + "'>Eliminar</button>");
                           $(lista_addCarro[j]).attr('disabled',true);
                       }
                   }
               }
            });
        }
    });
}


function listar_productos(categoria, pagina, categoria_){
	$(".lista-productos #items-productos").html("");
	var lista = "<ul>";
	var json_url = "/ventas/productos_json/" + pagina + "/" + categoria;
	$.getJSON(json_url,	function(productos) {
		if(categoria_ != -1) {
			$(".lista-productos #categoria-info").html("");
			if(categoria)
				$(".lista-productos #categoria-info").append(categoria_);
			else
				$(".lista-productos #categoria-info").append("<li><h2>Todos los productos</h2></li>");
		}
		for (var index=0; index<productos.length; index++){
			lista += "<li><ul>";							
			lista += "<li class='producto-nombre'>" + productos[index].nombre + "</li>";
			lista += "<li class='producto-imagen'><img class='imagen-prod' src=" + productos[index].imagen + " title='" + productos[index].descripcion + "' name='" + productos[index].id + "' /></li>";			
			if( sesion && productos[index].compra_online ){
				lista += "<li class='producto-add'><button class=\'add-carro' name='" + productos[index].id + "'>Añadir al carrito</button></li>";
			}
			else if(sesion){
				lista += "<li class='producto-add'><button class=\'add-carro' name='" + productos[index].id + "' disabled='true' >Sólo en tiendas</button></li>";
			}
			lista += "</ul></li>";							
		}
		lista += "</ul>";
		$(".lista-productos #items-productos").append(lista);
					
	});
}

function listar_tortas(categoria, pagina){
	$(".lista-productos #items-productos").html("");
	var lista = "<ul>";
	var json_url = "/ventas/productos_json_tortas/" + pagina;
	$.getJSON(json_url,	function(productos) {
		for (var index=0; index<productos.length; index++){
			lista += "<li><ul>";							
			lista += "<li class='producto-nombre'>" + productos[index].nombre + "</li>";
			lista += "<li class='producto-imagen'><img class='imagen-prod' src=" + productos[index].imagen + " title='" + productos[index].descripcion + "' name='" + productos[index].id + "' /></li>";			
			if( sesion && productos[index].compra_online ){
				lista += "<li class='producto-add'><button class=\'add-carro' name='" + productos[index].id + "'>Añadir al carrito</button></li>";
			}
			else if(sesion){
				lista += "<li class='producto-add'><button class=\'add-carro' name='" + productos[index].id + "' disabled='true' >Sólo en tiendas</button></li>";
			}
			lista += "</ul></li>";							
		}
		lista += "</ul>";
		$(".lista-productos #items-productos").append(lista);
					
	});
}

function calcular_total(){
	var total = 0;
	$(".item").each(function(){
		var precio = $(this).children(".precio-producto").val();
		var cantidad = $(this).children(".cantidad-producto").val();
		var item = parseFloat(precio)*parseInt(cantidad);
		total = total + item;
	});
	$("#total-productos").val(dosDecimales(total));
}

function mostrar_busqueda(id) {
	$('.resultado-buscar > ul').html('');
	$('#categoria-info').html('');
	$('#ingreso').val('');
	json_url = '/ventas/detalle_json/' + id;
	$('.paginador').html("");
	$('.lista-productos #items-productos').hide('slow');
	$.getJSON(json_url, function(producto){					
		$('.lista-productos #items-productos').html("");
		$('.lista-productos #items-productos').append("<ul id='categoria-info'><li><h2>Resultado de la busqueda</h2></li></ul><ul class='item-busqueda'>");
		$('.lista-productos #items-productos .item-busqueda').append("<li id='item-nombre'>" + producto.nombre + "</li>");
        if(producto.imagen){
            $('.lista-productos #items-productos .item-busqueda').append("<li><img id='img-find' class='imagen-prod' name=" + id + " src=" + producto.imagen + " title='" + producto.descripcion + "'></li>");
        }
		else{
            $('.lista-productos #items-productos .item-busqueda').append("<li><img id='img-find' class='imagen-prod' name=" + id + " src="+"/media/img/disabled.png"+ " title='" + producto.descripcion + "'></li>");
        }
		$('.lista-productos #items-productos .item-busqueda').append("<li id='item-precio'>" + producto.descripcion + "</li>");
		if(sesion){
			if(producto.compra_online){
				$('.lista-productos #items-productos .item-busqueda').append("<button class='add-carro' name='" + id + "'>Añadir al carrito</button></li>");
			}
		}
		$('.lista-productos  #items-productos').append("</ul>");					
	});
	$('.lista-productos #items-productos').show('slow');
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

	var item_index = 0;
	var pagina = 0;
	var items_busqueda = new Array();
	var index_busqueda = 0;
	var numero_items = 0;
	var current = 0;
	var estado_carrito = 0;

    var confirma_session = get_confirmacion();
	// Llenar los precios de cambio de los productos iniciales
	$(".producto-precio").each(function(){
		$(this).next().html("<div class='precio-estilo'>Precio de cambio:</div> $ " + aPrecioVenta(parseFloat($(this).attr('name'))));
	});

	// Añadir un producto al carrito de compras
	$(".add-carro").live("click", function(){
		current_item = "#item" + item_index;
		$("#total").before("<li class='item' id='item" + item_index + "'></li>");
		get_producto($(this).attr("name"), item_index);
        controlBorrado = $(this).attr("name");
        url = '/ventas/detalle_json/' + controlBorrado;
        $.getJSON(url,function(data){
            $("#listaCarro .listaPlus").append("<div id='list" + controlBorrado + "' style='font-size:10px;'>Producto :" + data.nombre + " | Precio :" + data.precio + "</div>")
        });
		$(current_item).append("Cantidad: ");
		$(current_item).append("<input class='cantidad-producto' type='text' value='1' name='cantidad-producto" + item_index + "'>");
		$(current_item).append("<button class='remove-item' idb='" + controlBorrado + "'>Eliminar</button>");
		item_index++;
		numero_items++;
        $(this).attr('disabled',true);
        $("#imgCarro a img").attr('src','/media/img/cart_add.png');
        setTimeout(function(){
            $("#imgCarro a img").attr('src','/media/img/cart.png');    
        },2000);
	});

	// Eliminar un item del carrito de compras
	$(".remove-item").live("click", function(event){
		$(this).parent().slideUp("slow", function () {
			numero_items--;
			$(this).remove();
		});
        identificador = $(this).attr('idb');
        $("#list" + identificador).remove();
        $(".add-carro[name|='" + identificador + "']").attr('disabled',false);
        $("#imgCarro a img").attr('src','/media/img/cart_remove.png');
        setTimeout(function(){
            $("#imgCarro a img").attr('src','/media/img/cart.png');
        },2000);
		return false;
		event.preventDefault();
	});

	// Recalcular el total
	$("#calculo-total").click(function(event){
		calcular_total();
		return false;
		event.preventDefault();
	});

	// Recarga de productos por categorías
	$('.categoria-link').click(function(event){
		categoria_ = $(this).attr("id");
		document.location.href = '/ventas/productos/' + categoria_;
		return false;
		event.preventDefault();
	});
    $('.subcategoria-link').click(function(event){
		categoria_ = $(this).attr("id");
		document.location.href = '/ventas/tienda_en_linea/' + categoria_;
		return false;
		event.preventDefault();
	});
	
	// Cargar la anterior página
	$('.selector-pagina-ant').live("click", function(event){
		if(pagina > 0){
			pagina--;
			$(".num_pagina").html((pagina+1)+"");
			listar_productos($(this).attr("id"), pagina, -1);
		}				
		return false;
		event.preventDefault();				
	});

	// Cargar la siguiente página
	$('.selector-pagina-sig').live("click", function(event){
		if(pagina < num_paginas-1){
			pagina++;
			$(".num_pagina").html((pagina + 1)+"");
			listar_productos($(this).attr("id"), pagina, -1);
		}									
		return false;
		event.preventDefault();
	});

	// Calcular el total de la compra
	$('#comprar').click(function(event){
		// Ningún item fue seleccionado				
		if(numero_items == 0){
			$('#items-error').show('slow');
			return false;
			event.preventDefault();					
		}				
		else {
			$('#items-error').hide('slow');
		}
		// La cantidad de los productos seleccionado se normalizan por lo menos a 1
		for(var i = 0 ; i < item_index ; i++) {
			var name = "input[name=cantidad-producto" + i + "]";
			if($(name).val() == "") {
				$(name).val(1);
			}
		}
		// La dirección y fecha de entrega son obligatorios
		if( $('#direccion').val() == "" ) {
			$('#direccion-error').show('slow');
			return false;
			event.preventDefault();
		}
		else {
			$('#direccion-error').hide('slow');
		}
		if( $('#fecha').val() == "" ) {
			$('#fecha-error').show('slow');
			return false;
			event.preventDefault();
		}
		else {
			$('#fecha-error').hide('slow');
		}				
		calcular_total();
		$('#carrito > form').append("<input type='hidden' id='numero-items' name='numero-items' value='" + item_index + "'>");
	});		

	// Mostrar u ocultar el carrito de compras
	$('#carrito-desplegable').click(function(){
		if(!estado_carrito) {
			$('.carrito').slideDown('slow');
			estado_carrito = 1;
		}			
		else {
			$('.carrito').slideUp('slow');
			estado_carrito = 0;
		}
	});

	// Ocultar el carrito de compras
	$('#cerrar-carrito').click(function(){
		$('.carrito').slideUp('slow');
		estado_carrito = 0;
	});
	
	// Resaltar el botón del carrito
	$('#carrito-desplegable').hover(
		function(){
			$(this).css('background', '#ffc90f');
		},
		function(){
			$(this).css('background', '#ffca46');
		}
	);
	
	// Aumentar tamaño de las fotos
	$('.imagen-prod').live('mouseover',	function(){
		$(this).css('background-color', '#ffffff');
	});

	$('.imagen-prod').live('mouseout', function(){
		$(this).css('background-color', '#DDDDDD');
	});
	
	// Aumentar tamaño de la foto (producto de la caja de búqueda)
	$('#img-find').live('mouseover', function(){
		$(this).css('background-color', '#ffffff');
	});

	$('#img-find').live('mouseout', function(){
		$(this).css('background-color', '#DDDDDD');
	});

	// Sólo aceptar caracteres numericos en la cantidad
	$('.cantidad-producto').live('keydown', function(event) {
		if ( event.keyCode == 46 || event.keyCode == 8 ) {
			// teclas de borrado, b y d
		}
		else {
			if (event.keyCode < 48 || event.keyCode > 57 ) {
				event.preventDefault();	
			}	
		}
	});
	
	// Desplegar widget del calendario y setear sus propiedades
	$('#id_fecha_entrega').attr('autocomplete', 'off');
	$('#fecha').datepicker({showOn:'both'});
	$('#fecha').datepicker( "option", "buttonImage", '/media/img/calendar.png' );
	$('#fecha').datepicker( "option", "buttonImageOnly", true );
	$('#fecha').datepicker( "option", "dateFormat", 'yy-mm-dd' );
	$('#fecha').datepicker( "option", "dayNames", ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sabado'] );
	$('#fecha').datepicker( "option", "dayNamesMin", ['Do', 'Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sa'] );
	$('#fecha').datepicker( "option", "dayNamesShort", ['Dom', 'Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab'] );
	$('#fecha').datepicker( "option", "monthNames", ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Setiembre','Octubre','Noviembre','Diciembre'] );
	$('#fecha').datepicker( "option", "monthNamesShort", ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Set','Oct','Nov','Dic'] );
	$('#fecha').datepicker( "option", "minDate", +2);
	$('#fecha').datepicker( "option", "nextText", 'Siguiente' );
	$('#fecha').datepicker( "option", "prevText", 'Anterior' );
});