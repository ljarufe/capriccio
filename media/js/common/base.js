function seleccionar_ciudad(){
	//$('.Luces').css('height', $('.contenedor').height());
	$('.Luces').fadeIn('slow', function(){
		$('.ciudad-frame').slideDown('slow');
	});
}

function mostrar_carta(){
	$('.Luces').fadeIn('slow',function(){
		$('.Luces').animate({"opacity": 0.6},1000);
		$('.mostrar-carta-tienda').show();
		$('.mostrar-carta-tienda').css("z-index","100");
	});
}
function cerrar_carta(){
	$('.Luces').fadeOut('slow',function(){
		$('.Luces').animate({"opacity": 0},1000);
		$('.mostrar-carta-tienda').hide();
		$('.mostrar-carta-tienda').css("z-index","0");
	});
}

$(document).ready(function(){
	$('.mostrar-carta-tienda').hide();
	$('.menu  ul li').children().not($('.menu  ul li a')).hide();
	$('.menu ul li').mouseover(function(){
		
		//$(this).children().css("background-color","#ffffff");
		//$(this).children().css("color","#b0550e");
		$(this).children().not($('.menu  ul li a')).show();
	});
	$('.menu  ul  li').mouseout(function(){	
		//$(this).children().css("background-color","#000000");
		//$(this).children().css("color","#ffffff");
		//$('.menu ul .submenu ul li a').css("background-color","#ffffff");
		//$('.menu ul .submenu ul li a').css("color","#8f9092");
		$(this).children().not($('.menu  ul li a')).hide();
	});
	//$('.menu  ul .raiz').children().not($('.menu  ul li a')).hide();
	
	//$('.menu ul .raiz').mouseover(function(){	
	//	$(this).children().css("backgroundImage","url(/media/img/header_bar_back_over.png)");
	//	$(this).children().css("color","#666666");
	//	$(this).children().not($('.menu  ul li a')).show();
	//});
	//$('.menu  ul .raiz').mouseout(function(){	
	//	$(this).children().css("backgroundImage","url(/media/img/header_bar_back.png)");
	//	$(this).children().css("color","#ffffff");
	//	//$('.menu ul .submenu ul li a').css("background-color","#ffffff");
	//	//$('.menu ul .submenu ul li a').css("color","#666666");
	//	$(this).children().not($('.menu  ul li a')).hide();
	//});
			
					
	// Apagar las luces de la pigina y mostrar solo el producto en un div
	$('.imagen-prod').click(function(){
		// Obtener los datos del producto y llenar el div
		var json_url = '/ventas/detalle_json/' + $(this).attr("name");
		nombre = $(this).attr("name");
		$.getJSON(json_url, function(producto){
			$('.cont').remove();
			$("#resultado").append("<div class='cont'><div>" + producto.nombre + "</div><div><img src='" + producto.imagen + "'/></div><div>" + producto.descripcion + "</div></div>");
			/*
$('.producto-frame > ul').append("<li class='nombre'>" + producto.nombre + "</li>");
			$('.producto-frame > ul').append("<li class='descripcion'>" + producto.descripcion + "</li>");
			$('.producto-frame > ul').append("<li class='imagen'><img src='" + producto.imagen + "' id='imagen-frame' /></li>");
			$('.producto-frame > ul').append("<div class='ventas'></div>");						
			if(producto.compra_online){
				$('.producto-frame > ul > .ventas').append("<li class='compra-online'>Puede comprarlo via web</li>");
			}
			else{
				$('.producto-frame > ul > .ventas').append("<li class='compra-online'>Venta solo en tiendas</li>");
			}
			$('.producto-frame > ul > .ventas').append("<li class='precio'>Precio: S/." + producto.precio + "</li>");
			
			if(producto.compra_online){
			$('.producto-frame > ul').append("<li class='lista-cerrar'><button id='cerrar-frame' class='add-carro comprar-frame' name='"+nombre+"'><img src='/media/img/shop-car.png' /> Comprar</button> <button title='Agrega este producto a tu carrito' id='cerrar-frame'>Cerrar</button></li>");
			}
			else{
			$('.producto-frame > ul').append("<li class='lista-cerrar'><button title='Agrega este producto a tu carrito' id='cerrar-frame'>Cerrar</button></li>");
			}
*/
			
		});
	});	
	// Cambiar la ciudad de compra
	$('#ciudad').click(function(){
		seleccionar_ciudad();
	});							
	var loginshow = false;
	function showLoginBlock()
	{
		//$('#box_login').position({left:$('#header_bar').position().left + $('#header_bar').attr('width')});
		var left = $('#contenedor').width() - ($('#box_login').width()+30);
		$('#box_login').css('margin-left',left);
		if(!loginshow){
			$('#box_login').slideDown('slow');
			loginshow = true;
		}else{
			$('#box_login').slideUp('slow');
			loginshow = false;
		}
		return false;
	}
	$('#init_session').click(showLoginBlock);
    
});
