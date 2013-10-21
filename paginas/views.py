# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, BadHeaderError
from django.utils.html import escape
from projectcapriccio.paginas.models import pagina, contenido_pagina, flash_pagina, video_pagina,place,\
    form_place
from projectcapriccio.empresa.models import Tienda
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.template import RequestContext
#from Tkinter import Place
from gdata import geo

def vista(request):
    pag = contenido_pagina.objects.filter(estado = 'A')
    store = Tienda()
    bus = Tienda.objects.all()
    lista_mapas = []
    for i in bus:
        lista_mapas.append(i.mapa_tienda())
    flash = flash_pagina.objects.all()
    lista_flash = []
    for j in flash:
        lista_flash.append(j.mostrar_flash())
    video = video_pagina.objects.all()
    lista_videos = []
    for h in video:
        lista_videos.append(h.mostrar_video_admin())
    return render_to_response("empresa/pagina.html",{'pag':pag,'map':lista_mapas,'flash':lista_flash,'video':lista_videos})
 
@csrf_protect
def grabar_ubicacion(request):
     form = None
     tUbicacion = "ubicacion.html"
     tLugar = "place.html"
     if request.method == "POST":
         if "latitud" in request.POST and "longitud" in request.POST:
             lugar = place(
                           latitud = request.POST["latitud"],
                           longitud = request.POST["longitud"],
                           )
             lugar.save()
         return render_to_response(tUbicacion, {'title':'Ubicacion'}, context_instance = RequestContext(request))
     else:
         return render_to_response(tUbicacion, {'title':"Ubicacion"}, context_instance = RequestContext(request))
     
     return render_to_response(tUbicacion, {'title':'Ubicacion'}, context_instance = RequestContext(request))
 
@csrf_exempt
def modificarUbicacion(request):
    ubicacion = ""
    msg = ''
    nuevaUbicacion = ""
    titulo = ""
    if request.method == "POST":
        if "latitud" in request.POST and "longitud" in request.POST and "valorId" in request.POST:
            nuevaUbicacion = place.objects.get(
                                               id = request.POST["valorId"]
                                               )
            
            nuevaUbicacion.latitud = request.POST["latitud"]
            nuevaUbicacion.longitud = request.POST["longitud"]
            
            nuevaUbicacion.save()
            msg = "Nueva ubicacion guardada con exito"
            titulo = "Ubicacion modificada"
        return render_to_response("admin/popupUbicacion.html", {'msg':msg,'title':titulo})
    if request.method == "GET":
        if "action" in request.GET:
            idUbicacion = request.GET["action"]
            ubicacion = place.objects.get(id = idUbicacion)
            titulo = "Modificar Ubicacion"
            return render_to_response("admin/popupUbicacion.html", {'ubicacion':ubicacion, 'id':idUbicacion,'title':titulo})
        else:
            pass

@csrf_exempt
def nuevaUbicacion(request):
    title = ""
    title = "Nueva ubicacion"
    lat = ""
    lng = ""
    form = form_place()
    if request.method == "POST":
        if "latitud" in request.POST and "longitud" in request.POST:
            lat = request.POST["latitud"]
            lng = request.POST["longitud"]
            geo = place(
                        latitud = lat,
                        longitud = lng
                        )
            geo.save()
            if geo:
                return HttpResponse("<script type='text/javascript' language='javascript'>var indice = window.opener.document.getElementById('id_ubicacion').length;var opcion = new Option('%s','%s');window.opener.document.getElementById('id_ubicacion').options[indice] = opcion;window.opener.document.getElementById('id_ubicacion').selectedIndex = indice;window.close();</script>" % (escape(geo),escape(geo._get_pk_val())))
        
    return render_to_response("ubicacion_tienda.html",{"form":form,"title":title})
