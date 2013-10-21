# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from projectcapriccio.common.views import get_cliente
from django.db.models import Max
from django.core.mail import EmailMultiAlternatives 
# modelos
from projectcapriccio.empresa.models import Empresa, Tienda, ImagenTienda, \
                                     CartaTienda, FotoEquipo
                                     
from projectcapriccio.paginas.models import form_place                                    
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect


def informacion(request):
    """
    Obtiene los datos de la empresa
    """
    id = Empresa.objects.aggregate(Max('id'))
    empresa = Empresa.objects.get(id=id['id__max'])
    return render_to_response('empresa/nosotros.html',
                              {'empresa': empresa,
                               'titulo': 'Nosotros'},
                              context_instance=RequestContext(request))
    

def tiendas(request, id_tienda=None):
    """
    Muestra los datos de una tienda y una lista de las tiendas
    """
    tiendas = Tienda.objects.all()
    if id_tienda:
        tienda = get_object_or_404(Tienda, id=id_tienda)
    else:
        tienda = None
    return render_to_response('empresa/tiendas.html',
                              {'tienda': tienda,
                               'tiendas': tiendas,
                               'titulo': 'Tiendas'},
                              context_instance=RequestContext(request))


def detalle_tienda(request, id_tienda):
    """
    Muestra las fotos, carta e información de una tienda
    """
    tienda = get_object_or_404(Tienda, id=id_tienda)
    fotos = ImagenTienda.objects.filter(tienda=id_tienda)
    carta = CartaTienda.objects.filter(tienda=id_tienda)
    return render_to_response('empresa/detalle_tienda.html',
                              {'tienda': tienda,
                               'fotos': fotos,
                               'carta': carta,
                               'titulo': "Nuestras tiendas"},
                              context_instance=RequestContext(request))
                              

def equipo_trabajo(request):
    """
    Muestra las fotos e información sobre el equipo de trabajo de la empresa
    """
    fotos = FotoEquipo.objects.all()
    return render_to_response('empresa/equipo_trabajo.html',
                              {'fotos': fotos,
                               'titulo': 'Equipo de trabajo'},
                              context_instance=RequestContext(request))
@csrf_protect
def contacto(request):
    if request.method == "POST":
        if "nombre" in request.POST and "email" in request.POST or "mensaje" in request.POST:
            nombre,email,mensaje = request.POST["nombre"],request.POST["email"],request.POST["mensaje"]
            asunto = u"Capriccio - Tienda On Line"
            texto = "Este es un mensaje enviado por Capriccio"
            html = "<div style='color:#355074'><h1>Gracias por comunicarse con nosotros %s.</h1><p>En seguida un miembro de nuestro staff se comunicar&aacute; contigo</p><p>Cordialmente,</p><img src='http://capriccioperu.com/media/img/tienda_en_linea.png' alt='Logo Tiena On Line Capriccio'/></div>" % (nombre)
            message_html = "Mensaje enviado"
            msg = EmailMultiAlternatives(asunto,texto,u"Tienda en Línea <systems@capriccioperu.com>",[email])
            msg.attach_alternative(html,"text/html")
            msg.send()
            subject = "Formulario de Contacto - Capriccio | Tienda On Line"
            text = "Este es un mensaje desde el formulario de contacto"
            body = "<div style='color:#355074'><h1>Datos desde el formulario de contacto</h1><p>Nombre : %s</p><p>E-mail : %s</p><p>Mensaje : %s</p></div>" % (nombre,email,mensaje)
            msg = EmailMultiAlternatives(subject,text,u"Tienda en Línea <systems@capriccioperu.com>",["capriccio@capriccioperu.com"])
            msg.attach_alternative(body,"text/html")
            msg.send()
            tiendas = Tienda.objects.all()
        return render_to_response('empresa/tiendas.html',{'msg':message_html,'tiendas':tiendas},context_instance=RequestContext(request))
