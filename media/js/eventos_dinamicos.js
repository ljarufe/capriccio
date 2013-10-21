/**
 * @author mauricio
 */
$(document).ready(function(){
	$(".seen").click(function(){
		var atributo_dinamico = $(this).attr("idb");
		$.ajax({
			type:"POST",
			url:"/visto",
			data:"identificador="+atributo_dinamico,
			success:function(data){
				var html = data;
				$("#notified").append("<br/>" + html + " ocurrencia vista y archivada.");
			}
		});
	});
})
