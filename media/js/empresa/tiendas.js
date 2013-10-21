//<![CDATA[
	function load() {
		var map = new GMap2(document.getElementById("map"));
		
		map.addControl(new GMapTypeControl());
		map.addControl(new GLargeMapControl());
		//map.addControl(new GScaleControl());
		map.addControl(new GOverviewMapControl());
		map.setCenter(new GLatLng(latitud, longitud), 17);	
			
		function addtag(point, address) {
			var marker = new GMarker(point);
			GEvent.addListener(marker, "click", function() { marker.openInfoWindowHtml(address); } );
			return marker;
		}
		
		var point = new GLatLng(latitud, longitud);	        
		var address = '<div class="mapa" ><b>' + nombre + '</b><br/>' + direccion + '<br/><div>';
		var marker = addtag(point, address);		
		map.addOverlay(marker);	
	}
//]]>

$(document).ready(function(){
	load();
});

$(document).unload(function(){
	GUnload();
});
