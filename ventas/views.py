# -*- coding: utf-8 -*-
'''
@author: lucho
'''

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core import mail
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.utils import simplejson
from django.conf import settings
from math import ceil
from datetime import datetime
from django.utils.encoding import force_unicode
from django.core.paginator import Paginator,EmptyPage,Page,InvalidPage

from projectcapriccio.common.views import get_cliente, get_paginacion, \
                                   get_productos_cache, get_tipo_cambio
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
# models
from projectcapriccio.ventas.models import Subcategoria,Producto, Categoria, Producto_item,Personalizado_item
from projectcapriccio.clientes.models import Cliente
from projectcapriccio.common.models import Ciudad, Direccion,Tortas_Cumpleanos,Torta_Personalizada,LugarEntrega,RecargoEntrega
from projectcapriccio.empresa.models import Tienda
# forms
from projectcapriccio.ventas.forms import Personalizado_itemForm
from projectcapriccio.common.forms import ImagenForm,ContactPersonalizada,ContactInstitucional
from projectcapriccio.notification.models import Compra
from projectcapriccio.ventas.models import Personalizado_arte
from projectcapriccio.common.forms import DireccionForm
from projectcapriccio.clientes.forms import ClienteForm
#paginador
from django.core.paginator import Paginator, InvalidPage, EmptyPage
#envío de archivo adjunto
import Image
import os
from os.path import dirname
from StringIO import StringIO
basedir = dirname(__file__)
producto_list = []

@csrf_exempt
def productos(request, id_categoria=None):
    """
    Listado de productos y categorías
    """
    
    # La ciudad de compra esta en el cache, fue elegida o no existe aún
    try:
        request.session['ciudad'] = str(request.GET['ciudad'])        
    except KeyError:
        try:
            id_ciudad = request.session['ciudad']
        except KeyError:
            ciudad = None
        else:
            try: 
                ciudad = Ciudad.objects.get(id=id_ciudad)
            except Ciudad.DoesNotExist:
                ciudad = None
    else:
        id_ciudad = request.session['ciudad']
        ciudad = get_object_or_404(Ciudad, id=id_ciudad)
    
    # Se va a realizar una compra
    if request.method == 'POST':
        fecha_entrega = request.POST['fecha-entrega']        
        direccion = Direccion(lugar=request.POST['direccion-entrega'],
                              ciudad=ciudad)
        direccion.save()
        usuario = get_cliente(request)
        cliente = Cliente.objects.get(user__username=usuario)
        compra = Compra(cliente=cliente,
                        fecha_pedido=datetime.now(),
                        fecha_entrega=fecha_entrega,
                        direccion_entrega=direccion)
        
        total = 0        
        items = []
        tipo_cambio = float(get_tipo_cambio())
        
        # Los productos eliminados producen un KeyError
        for i in range(int(request.POST['numero-items'])):
            try:
                id_producto = request.POST['id-producto'+str(i)]
            except KeyError:
                pass
            else:
                try:
                    producto = Producto.objects.get(id=id_producto)
                    cantidad = request.POST['cantidad-producto'+str(i)]
                    items.append({'producto': producto, 'cantidad': cantidad})
                    cambio = round(producto.precio/tipo_cambio, 2)
                    total += cambio * int(cantidad)
                except Producto.DoesNotExist:
                    pass
                
        
        compra.total = total
        compra.save()       
        
        for item in items:
            producto_item = Producto_item(compra=compra,
                                          cantidad=item['cantidad'],
                                          producto=item['producto'])
            producto_item.save()
            
        return render_to_response('ventas/2checkout_form.html',
		                          {'x_login': settings.CHECKOUT_ID,
		                          'x_ammount': compra.total,
		                          'x_invoice_cart': compra.id,
                                  'x_cliente':cliente,
                                  'x_direccion':cliente.direccion,
                                  'x_direccion_ciudad':cliente.direccion.ciudad,
                                  'x_email':usuario,
                                  'x_telefono':cliente.telefono,
                                  },
		                          context_instance=RequestContext(request))
    
    # Filtrar los productos
    todos_productos = get_productos_cache()
    if ciudad:
        todos_productos = todos_productos.filter(tienda__direccion__ciudad__id=ciudad.id)        
    if id_categoria:
        categoria = get_object_or_404(Categoria, id=id_categoria)
        productos = todos_productos.filter(categoria=id_categoria)        
    else:
        productos = todos_productos
        categoria = None
        
    #Paginador
    paginador = Paginator(productos,8)
    
    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1
        
    try:
        products = paginador.page(page)
    except(EmptyPage,InvalidPage):
        products = paginador.page(paginador.num_pages)
    
    items_pagina = settings.ITEMS_PAGINA
    categorias = Categoria.objects.all()
    num_productos = productos.count()
    productos = productos[:items_pagina]
    ciudades = Ciudad.objects.all()
    
    # Hallar el tipo de cambio de soles a dolares
    tipo_cambio = get_tipo_cambio()
    
    # Enviar por defecto la direcciÃ³n del cliente que ha iniciado sesiÃ³n
    if request.user.is_authenticated():
        cliente = Cliente.objects.get(user=request.user.id)
        direccion = cliente.direccion.lugar
    else:
        direccion = ""
        
    return render_to_response('ventas/compra_productos.html',
                              {'productos': products,
                               'todos_productos': todos_productos,
                               'categorias': categorias,
                               'categoria': categoria,
                               'fecha_hoy': datetime.now(),                               
                               'ciudad_sesion': ciudad,
                               'ciudades': ciudades,
                               'tipo_cambio': tipo_cambio,
                               'direccion': direccion,
                               'titulo': 'Productos',
                               'num_paginas': int( ceil(float(num_productos) / float(items_pagina) ) )},
                               context_instance=RequestContext(request))

@csrf_exempt
def tienda_en_linea(request, id_categoria=None):
    """
    Listado de productos y categorￃﾭas
    """
    
    # La ciudad de compra esta en el cache, fue elegida o no existe aￃﾺn
    lista_productos = []
    try:
        request.session['ciudad'] = str(request.GET['ciudad'])        
    except KeyError:
        try:
            id_ciudad = request.session['ciudad']
        except KeyError:
            ciudad = None
        else:
            try: 
                ciudad = Ciudad.objects.get(id=id_ciudad)
            except Ciudad.DoesNotExist:
                ciudad = None
    else:
        id_ciudad = request.session['ciudad']
        ciudad = get_object_or_404(Ciudad, id=id_ciudad)
    
    # Se va a realizar una compra
    if request.method == 'POST':
        if 'modoPago' in request.POST:
            modoPago = request.POST['modoPago']
            if modoPago == 0:
                idTienda = request.POST['tienda']
                place = Tienda.objects.get(pk=idTienda)
                fecha_entrega = request.POST['fecha-entrega']
                direccion = Direccion(lugar=place.direccion.lugar,
                                      ciudad=ciudad)
                direccion.save()
                usuario = get_cliente(request)
                if usuario != None:
                    cliente = Cliente.objects.get(user__username=usuario)
                    compra = Compra(cliente=cliente,
                                fecha_pedido=datetime.now(),
                                fecha_entrega=fecha_entrega,
                                direccion_entrega=direccion)

                    total = 0
                    items = []
                    tipo_cambio = float(get_tipo_cambio())
                    # Los productos eliminados producen un KeyError
                    for i in range(int(request.POST['numero-items'])):
                        try:
                            id_producto = request.POST['id-producto'+str(i)]
                        except KeyError:
                            pass
                        else:
                            try:
                                producto = Producto.objects.get(id=id_producto)
                                cantidad = request.POST['cantidad-producto'+str(i)]
                                items.append({'producto': producto, 'cantidad': cantidad})
                                #crear variable de sesion para los productos y cantidades por si el usuario necesita seuir comprando
                                request.session['buy'] = items
                                cambio = round(producto.precio/tipo_cambio, 2)
                                total += cambio * int(cantidad)
                            except Producto.DoesNotExist:
                                pass


                    compra.total = total
                    compra.save()

                    for item in items:
                        producto_item = Producto_item(compra=compra,
                                                      cantidad=item['cantidad'],
                                                      producto=item['producto'])
                        producto_item.save()

                    return render_to_response('ventas/confirmacion_compra.html',
                                              {'x_login': settings.CHECKOUT_ID,
                                              'x_ammount': compra.total,
                                              'x_invoice_cart': compra.id,
                                              'x_cliente':cliente,
                                              'x_direccion':cliente.direccion,
                                              'x_direccion_ciudad':cliente.direccion.ciudad,
                                              'x_email':usuario,
                                              'x_telefono':cliente.telefono,
                                              },
                                              context_instance=RequestContext(request))
            else:
                idTienda = request.POST['tienda']
                place = Tienda.objects.get(pk=idTienda)
                fecha_entrega = request.POST['fecha-entrega']
                direccion = Direccion(lugar=place.direccion.lugar,
                                      ciudad=ciudad)
                direccion.save()
                usuario = get_cliente(request)
                if usuario != None:
                    cliente = Cliente.objects.get(user__username=usuario)
                    compra = Compra(cliente=cliente,
                                fecha_pedido=datetime.now(),
                                fecha_entrega=fecha_entrega,
                                direccion_entrega=direccion)

                    total = 0
                    items = []
                    tipo_cambio = float(get_tipo_cambio())
                    # Los productos eliminados producen un KeyError
                    for i in range(int(request.POST['numero-items'])):
                        try:
                            id_producto = request.POST['id-producto'+str(i)]
                        except KeyError:
                            pass
                        else:
                            try:
                                producto = Producto.objects.get(id=id_producto)
                                cantidad = request.POST['cantidad-producto'+str(i)]
                                items.append({'producto': producto, 'cantidad': cantidad})
                                #crear variable de sesion para los productos y cantidades por si el usuario necesita seuir comprando
                                request.session['buy'] = items
                                cambio = round(producto.precio/tipo_cambio, 2)
                                total += cambio * int(cantidad)
                            except Producto.DoesNotExist:
                                pass


                    compra.total = total
                    compra.save()

                    for item in items:
                        producto_item = Producto_item(compra=compra,
                                                      cantidad=item['cantidad'],
                                                      producto=item['producto'])
                        producto_item.save()

                    return render_to_response('ventas/2checkout_form.html',
                                              {'x_login': settings.CHECKOUT_ID,
                                              'x_ammount': compra.total,
                                              'x_invoice_cart': compra.id,
                                              'x_cliente':cliente,
                                              'x_direccion':cliente.direccion,
                                              'x_direccion_ciudad':cliente.direccion.ciudad,
                                              'x_email':usuario,
                                              'x_telefono':cliente.telefono,
                                              },
                                              context_instance=RequestContext(request))
        else:
            compra = Compra(
                fecha_pedido=datetime.now(),
                fecha_entrega=fecha_entrega,
                direccion_entrega=direccion
            )
            total = 0
            items = []
            tipo_cambio = float(get_tipo_cambio())
            for i in range(int(request.POST['numero-items'])):
                try:
                    id_producto = request.POST['id-producto'+str(i)]
                except KeyError:
                    pass
                else:
                    try:
                        producto = Producto.objects.get(id=id_producto)
                        cantidad = request.POST['cantidad-producto'+str(i)]
                        items.append({'producto': producto, 'cantidad': cantidad})
                        #crear variable de sesion para los productos y cantidades por si el usuario necesita seguir comprando
                        request.session['buy'] = items
                        cambio = round(producto.precio/tipo_cambio, 2)
                        total += cambio * int(cantidad)
                    except Producto.DoesNotExist:
                        pass


            compra.total = total
            compra.save()
            request.session['compra'] = compra.id
            for item in items:
                producto_item = Producto_item(compra=compra,
                                              cantidad=item['cantidad'],
                                              producto=item['producto'])
                producto_item.save()
            cliente_form = ClienteForm()
            direccion_form = DireccionForm()
            return render_to_response('ventas/follow_buy.html',
                                      {'x_login': settings.CHECKOUT_ID,
                                       'titulo':u'Tienda en Línea - Registro',
                                      'x_ammount': compra.total,
                                      'x_invoice_cart': request.session['compra'],
                                      'cliente_form': cliente_form,
                                      'direccion_form': direccion_form
                                      },
                                      context_instance=RequestContext(request))

    
    # Filtrar los productos
    todos_productos = get_productos_cache()
    if ciudad:
        todos_productos = todos_productos.filter(tienda__direccion__ciudad__id=ciudad.id).filter(categoria__nombre__contains='torta')
        tiendas = Tienda.objects.filter(direccion__ciudad__id=ciudad.id)
    else:
        tiendas = Tienda.objects.all()
    if id_categoria:
        categoria = get_object_or_404(Categoria, nombre__contains='torta')
        productos = todos_productos.filter(categoria__nombre__contains='torta').filter(subcategoria__id=id_categoria)
        subcategoria = Subcategoria.objects.all()
    else:
        productos = todos_productos
        subcategoria = Subcategoria.objects.all()
        categoria = None
    
    #paginador tienda en línea
    paginador = Paginator(productos,8)
    
    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1
        
    try:
        products = paginador.page(page)
    except(EmptyPage,InvalidPage):
        products = paginador.page(paginador.num_pages)
    
    items_pagina = settings.ITEMS_PAGINA
    num_productos = productos.count()
    productos = productos[:items_pagina]
    ciudades = Ciudad.objects.all()
    zonas_entrega = LugarEntrega.objects.filter(ciudad=ciudad)
    recargo_entrega = RecargoEntrega.objects.filter(ciudad=ciudad)
    
    # Hallar el tipo de cambio de soles a dolares
    tipo_cambio = get_tipo_cambio()
    
    # Enviar por defecto la direcciￃﾃￂﾳn del cliente que ha iniciado sesiￃﾃￂﾳn
    if request.user.is_authenticated():
        cliente = Cliente.objects.get(user=request.user.id)
        direccion = cliente.direccion.lugar
    else:
        direccion = ""
    if request.session.get('lista_productos'):
        lista_productos = request.session['lista_productos']
    else:
        lista_productos = None
    return render_to_response('ventas/tienda_linea.html',
                              {'productos': productos,
                               'todos_productos': todos_productos,
                               'products':products,
                               'tiendas':tiendas,
                               'categoria': categoria,
                               'subcategoria':subcategoria,
                               'fecha_hoy': datetime.now(),                               
                               'ciudad_sesion': ciudad,
                               'ciudades': ciudades,
                               'tipo_cambio': tipo_cambio,
                               'direccion': direccion,
                               'zonas':zonas_entrega,
                               'recargo':recargo_entrega,
                               'lista_productos_sesion':lista_productos,
                               'titulo': u'Tienda en Línea',
                               'num_paginas': int( ceil(float(num_productos) / float(items_pagina) ) )},
                               context_instance=RequestContext(request))

def compra_despues_logeo(request):
    usuario = get_cliente(request)
    compra = Compra.objects.get(pk=request.session['compra'])
    cliente = Cliente.objects.get(user__username=usuario)
    compra.cliente = cliente
    compra.save()
    return render_to_response('ventas/2checkout_form.html',
                                      {'x_login': settings.CHECKOUT_ID,
                                      'x_ammount': compra.total,
                                      'x_invoice_cart': compra.id,
                                      'x_cliente':cliente,
                                      'x_direccion':cliente.direccion,
                                      'x_direccion_ciudad':cliente.direccion.ciudad,
                                      'x_email':usuario,
                                      'x_telefono':cliente.telefono,
                                      },
                                      context_instance=RequestContext(request))

def get_productos_json(request, pagina, id_categoria=None):
    """
    Devuelve los productos via AJAX según la categoría, limitando la consulta
    según la página - paginador de productos por JSON
    """
    request.session['lista_productos']=[]
    id_ciudad = request.session['ciudad']
    items_pagina = settings.ITEMS_PAGINA
    pagina = int(pagina)
    
    # filtro de la lista de productos
    productos_list = get_productos_cache()
    if id_categoria:
        productos_list = productos_list.filter(categoria=id_categoria)
        
    productos_list = productos_list.filter(tienda__direccion__ciudad__id=id_ciudad)
    productos_list = productos_list[pagina*items_pagina: pagina*items_pagina+items_pagina]
    
    productos = request.session['lista_productos']
    for producto in productos_list:
        producto = {'id': producto.id,
                    'nombre': producto.nombre, 
                    'precio': producto.precio,
                    'descripcion': producto.descripcion,
                    "imagen": u'%s' % producto.imagen.imagen.thumbnail,
                    'compra_online': producto.compra_online}
        productos.append(producto)
    request.session['lista_productos']=productos
    request.session.modified = True
    return HttpResponse(simplejson.dumps('moco'), mimetype='application/json')

def get_productos_json_tortas(request,pagina):
    """
    Devuelve los productos via AJAX según la categoría, limitando la consulta
    según la página - paginador de productos por JSON
    """
    request.session['lista_productos']=[]
    id_ciudad = request.session['ciudad']
    items_pagina = settings.ITEMS_PAGINA
    pagina = int(pagina)
    
    # filtro de la lista de productos
    productos_list = get_productos_cache()
    
    productos_list = productos_list.filter(categoria__nombre__contains='torta')
    
        
    productos_list = productos_list.filter(tienda__direccion__ciudad__id=id_ciudad)
    productos_list = productos_list[pagina*items_pagina: pagina*items_pagina+items_pagina]
    
    productos = request.session['lista_productos']
    for producto in productos_list:
        producto = {'id': producto.id,
                    'nombre': producto.nombre, 
                    'precio': producto.precio,
                    'descripcion': producto.descripcion,
                    "imagen": u'%s' % producto.imagen.imagen.thumbnail,
                    'compra_online': producto.compra_online}
        productos.append(producto)
    request.session['lista_productos']=productos
    request.session.modified = True
    print request.session.keys()
    
    return HttpResponse(simplejson.dumps(productos), mimetype='application/json')

def get_numero_paginas_json(request, id_categoria=None):
    """
    Devuelve el número de paginas en el que se dividirá 
    la consulta de una categoria de productos
    """
    items_pagina = settings.ITEMS_PAGINA
    id_ciudad = request.session['ciudad']
    productos = Producto.objects.filter(tienda__direccion__ciudad__id=id_ciudad,
                                        estado='A').distinct()
    if id_categoria:        
        productos = productos.filter(categoria=id_categoria)
        
    num_productos = productos.count()
    paginas = {'num_paginas': int(ceil( float(num_productos)/ float(items_pagina) ) )}
    
    return HttpResponse(simplejson.dumps(paginas), mimetype='application/json')
    

def get_producto_json(request, id_producto):
    """
    Devuelve los datos de un producto para colocarlos en el carrito de compras
    """
    producto_objeto = Producto.objects.get(id=id_producto)
    producto = {'id': producto_objeto.id,
                'nombre': producto_objeto.nombre,
                'precio': producto_objeto.precio}
    producto_list.append(producto)
    request.session['lista_productos'] = producto_list
    return HttpResponse(simplejson.dumps(producto), mimetype='application/json')

def confirmar_session(request):
    if request.session['lista_productos']:
        verdad = 1
        respuesta = {
            'verdad':verdad
        }
    else:
        verdad = 0
        respuesta = {
            'verdad':verdad
        }
    return HttpResponse(simplejson.dumps(respuesta),mimetype='application/json')       

def get_producto_session(request):
    if request.session['lista_productos']:
        lista = request.session['lista_productos']
    return HttpResponse(simplejson.dumps(lista),mimetype='application/json')

def eliminar_producto_session(request,id):
    if id:
        producto_objeto = Producto.objects.get(id=id)
        for lista_session in range(len(request.session['lista_productos'])):
            if request.session['lista_productos'][lista_session]['id'] == producto_objeto.id:
                print lista_session
                del request.session['lista_productos'][lista_session]['id']
                del request.session['lista_productos'][lista_session]['nombre']
                del request.session['lista_productos'][lista_session]['precio']
                request.session['lista_productos'].pop  (lista_session)
        request.session.modified = True
        return HttpResponse('nada')

def get_detalle_json(request, id_producto):
    """
    Devuelve todos los detalles de un producto
    """
    producto = Producto.objects.get(id=id_producto)
    if producto.imagen:
        producto = {'nombre': producto.nombre,
                    'precio': producto.precio,
                    'descripcion': producto.descripcion,
                    "imagen": u'%s' % producto.imagen.imagen.extra_thumbnails['medium'],
                    'compra_online': producto.compra_online}
    else:
        producto = {'nombre': producto.nombre,
                    'precio': producto.precio,
                    'descripcion': producto.descripcion,
                    'compra_online': producto.compra_online}
    
    return HttpResponse(simplejson.dumps(producto), mimetype='application/json')


@csrf_exempt
def torta_personalizada(request):
    """
    Ingreso de una torta personalizada, compra de un sólo producto
    que contiene un mensaje y una imágen
    """
    
    # La ciudad de compra esta en el cache, fue elegida o no existe aún
    try:
        request.session['ciudad'] = str(request.GET['ciudad'])        
    except KeyError:
        try:
            id_ciudad = request.session['ciudad']
        except KeyError:
            ciudad = None
        else:            
            try: 
                ciudad = Ciudad.objects.get(id=id_ciudad)
            except Ciudad.DoesNotExist:
                ciudad = None
    else:
        id_ciudad = request.session['ciudad']
        ciudad = get_object_or_404(Ciudad, id=id_ciudad)
    
    
    form_imagen = ContactPersonalizada()
    
    # Filtrar los productos    
    lista_productos = get_productos_cache()
    lista_productos = Producto.objects.filter(personalizable=True).distinct()
    lista_tortas = Torta_Personalizada.objects.all()
    if ciudad:
        lista_productos = lista_productos.filter(tienda__direccion__ciudad__id=ciudad.id)
    productos = get_paginacion(request, lista_productos, 6)
    ciudades = Ciudad.objects.all()
    
    # Hallar el tipo de cambio de soles a dolares
    tipo_cambio = get_tipo_cambio()
    
    # Enviar por defecto la direcciÃ³n del cliente que ha iniciado sesiÃ³n
    #if request.user.is_authenticated():
    #    cliente = Cliente.objects.get(user=request.user.id)
    #    direccion = cliente.direccion.lugar
    #else:
    #    direccion = ""
    
    return render_to_response('ventas/torta_personalizada.html',
                              {'productos': productos,
                               'lista_productos': lista_productos,
                               'ciudad_sesion': ciudad,
                               'ciudades': ciudades,
                               'form_imagen': form_imagen,
                               'fecha_entrega': datetime.now(),
                               'tipo_cambio': tipo_cambio,
                               'personalizada':lista_tortas,
                               'titulo': 'Torta Personalizada'},
                              context_instance=RequestContext(request))
@csrf_exempt       
def contact(request):
    if request.method == "POST":
        connection = mail.get_connection()
        connection.open()
        form = ContactPersonalizada(request.POST,request.FILES)
        if form.is_valid():            
            person=form.cleaned_data['person']
            email=form.cleaned_data['email']
            subject=form.cleaned_data['subject']
            comment=form.cleaned_data['comment']
            image=form.cleaned_data['image']
            phone = form.cleaned_data['phone']
            img = Image.open(StringIO(image.read()))
            img.save(settings.MEDIA_ROOT+email+'.jpg','JPEG')
            if email:
                text=u'Envío de consulta Torta Personalizada'
                html='<div><h1>Gracias por hacernos llegar tu consulta %s</h1><p>En breve nos comunicaremos contigo</p><img src="http://capriccioperu.com/media/img/tienda_en_linea.png"/></div>' % person
                msg=EmailMessage(subject,html,u'Tienda en Línea <systems@capriccioperu.com>',[email])
                msg.content_subtype='html'
                html_admin = '<div><h1>Datos desde el formulario para Tortas Personalizadas</h1><p>Nombre : %s</p><p>E-mail : %s</p><p>Comentario : %s</p><p>Tel&eacute;fono Contacto: %s</p><img src="http://capriccioperu.com/media/img/tienda_en_linea.png"/></div>' % (person,email,comment,phone)
                msg1=EmailMessage('Formulario Torta Personalizada',html_admin,u'Tienda en Línea <systems@capriccioperu.com>',['capriccio@capriccioperu.com'])
                msg1.attach_file(settings.MEDIA_ROOT+email+'.jpg')
                msg1.content_subtype='html'
                connection.send_messages([msg,msg1])
                return HttpResponseRedirect('/ventas/torta_personalizada')
        return HttpResponse('No existe')

@csrf_exempt
def cumpleanos(request):
    if request.method == "POST":
        connection = mail.get_connection()
        connection.open()
        form = ContactInstitucional(request.POST)
        if form.is_valid():
            person=form.cleaned_data['person']
            email=form.cleaned_data['email']
            subject=form.cleaned_data['subject']
            comment=form.cleaned_data['comment']
            phone = form.cleaned_data['phone']
            if email:
                text=u'Envío de consulta Tortas de Cumpleaños'
                html='<div><h1>Gracias por hacernos llegar tu consulta %s</h1><p>En breve nos comunicaremos contigo</p><img src="http://capriccioperu.com/media/img/tienda_en_linea.png"/></div>' % person
                msg=EmailMessage(subject,html,u'Tienda en Línea <systems@capriccioperu.com>',[email])
                msg.content_subtype='html'
                html_admin = '<div><h1>Datos desde el formulario para Tortas Cumplea&ntilde;os</h1><p>Nombre : %s</p><p>E-mail : %s</p><p>Comentario : %s</p><p>Tel&eacute;fono Contacto: %s</p><img src="http://capriccioperu.com/media/img/tienda_en_linea.png"/></div>' % (person,email,comment,phone)
                msg1=EmailMessage(u'Formulario Torta Cumpleaños',html_admin,u'Tienda en Línea <systems@capriccioperu.com>',['capriccio@capriccioperu.com'])
                msg1.content_subtype='html'
                connection.send_messages([msg,msg1])
                return HttpResponseRedirect('/ventas/birthday')
        return HttpResponse('No existe')    
                
    
@csrf_exempt
@login_required
def respuesta_2checkout(request):
    transaccion = ""
    card_processed = ""
    order = ""
    number = ""
    amount = ""
    productos_compra = ""
    productos_compra_personalizada = ""    
    if request.method == "POST":
        card_processed = request.POST["credit_card_processed"]
        order = request.POST["cart_order_id"]
        number = request.POST["order_number"]
        amount = request.POST["total"]
        if card_processed == "Y":
            compra = Compra.objects.get(id = order)
            try:
                productos_compra = Producto_item.objects.filter(compra = compra)
            except:
                productos_compra
            try:
                productos_compra_personalizada = Personalizado_item.objects.get(id = order)
            except:
                productos_compra_personalizada
            compra.status = "A"
            compra.save()      
        return render_to_response("ventas/respuesta_2checkout.html",{"card":card_processed,"order":order,"number":number,"amount":amount,"prod":productos_compra,"personalizado":productos_compra_personalizada})
    else:
        return render_to_response("ventas/error.html")

def birthday(request):
    form_imagen = ContactInstitucional()
    tortas = Tortas_Cumpleanos.objects.all()
    paginator = Paginator(tortas,10)
    try:
        page = int(request.GET.get('page',1))
    except ValueError:
        page = 1
    try:
        cakes = paginator.page(page)
    except (EmptyPage,InvalidPage):
        cakes = paginator.page(paginator.num_pages)
    return render_to_response("ventas/tortas_cumpleanos.html",{"titulo":u"Tortas de Cumpleaños","cakes":cakes,"form_imagen":form_imagen},context_instance=RequestContext(request))
