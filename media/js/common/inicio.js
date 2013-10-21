$(document).ready(function(){
	var i = 1;
	$('.banner ul li:nth-child(1) .item-banner').fadeIn('slow');
	$('.novedades-news').not($('.novedades-news:first')).hide();
	
	
	// Rotación de banners
	setInterval(function(){
		antiguo = '.banner ul li:nth-child(' + i + ') .item-banner';
		if(i == num_ban)
			i = 0;				
		$(antiguo).fadeOut('slow', function(){
			i++;
			nuevo = '.banner ul li:nth-child(' + i + ') .item-banner';
			$(nuevo).fadeIn('slow');
		});
	}, 7000);
	var j = 0;
	var news = $('.novedades-news');
	setInterval(function(){
		$(news[j]).hide();
		$(news[j+1]).show('bounce');
		j++;
		if(j==news.length){
			j=0;
			$(news[j]).show('bounce');
		}
	},20000);
});


var ofertas = function(urls,titulos) {
	var indice = 0;
	var fin = urls.length;
	$('#banner-imagen img').css('background', 'url('+urls[indice]+')');
	$("#titulo-texto").text(titulos[indice]);
	$('#sig').click(function() {
		$('#banner-imagen img').css('background', 'url('+urls[cambiar(1)]+')');
		$("#titulo-texto").text(titulos[cambiar(1)]);
	});
	$('#ant').click(function() {
		$('#banner-imagen img').css('background', 'url('+urls[cambiar(1)]+')');
		$("#titulo-texto").text(titulos[cambiar(1)]);
	});
	
	function cambiar(num) {
		return indice = (indice+num>=fin)?0:(indice+num<0)?fin-1:indice+num;	//Obtener el indice siguiente o anterior
	}
}
var banners = function(urls,titulos){
    var i = 0;
    $('#banner-imagen img').css('background', 'url('+urls[i]+')');
    $("#titulo-texto").text(titulos[i]);
    setInterval(function(){
        $("#banner-imagen img").hide();
        $("#titulo-texto").hide(); 
        $('#banner-imagen img').css('background', 'url('+urls[i+1]+')');
        $("#titulo-texto").text(titulos[i+1]);
        $('#banner-imagen img').fadeIn();
        $("#titulo-texto").fadeIn();
        i++;
        if (i==urls.length){
            i=0;
            $('#banner-imagen img').css('background', 'url('+urls[i]+')');
            $("#banner-imagen img").hide();
            $("#titulo-texto").hide();
            $('#banner-imagen img').css('background', 'url('+urls[i]+')');
            $("#titulo-texto").text(titulos[i]);
            $('#banner-imagen img').fadeIn();
            $("#titulo-texto").fadeIn();
        }
    },5000);
}