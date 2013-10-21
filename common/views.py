# -*- coding: utf-8 -*-

'''
@author: lucho
'''

from django.core.cache import cache
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from random import Random
import urllib2
import re
import string
# models
from projectcapriccio.paginas.models import contenido_pagina, banner_pagina, novedades
from projectcapriccio.ventas.models import Producto
from projectcapriccio.common.models import Iniciales
from django.shortcuts import get_object_or_404

def bienvenida(request):
    usuario_invalido = False
    _banners = banner_pagina.objects.all()
    _novedades = novedades.objects.all().order_by('-fecha')
    novedades_paginadas = get_paginacion(request, _novedades, 3)
    inicial = Iniciales.objects.all()
    first = inicial[0]

    return render_to_response('common/bienvenida.html',
                              {'titulo': "Bienvenido",
                               'usuario_invalido': usuario_invalido,
                               'banners': _banners,
                               'novedades': novedades_paginadas,
                               'ini':inicial,
                               'first':first},
                              context_instance=RequestContext(request))

@csrf_exempt
def inicio(request, url_redirect=None):
    """
    Página de inicio
    """
    usuario_invalido = False
    if request.method == 'POST':
        nombre = request.POST['usuario']
        password = request.POST['password']
        usuario = authenticate(username=nombre, password=password)
        if usuario is not None:                    
            if usuario.is_active:
                login(request, usuario)
                return HttpResponseRedirect(reverse('inicio'))
            else:
                return render_to_response('clientes/confirmacion.html',
                                          {'titulo': 'Confirmación'},
                                          context_instance=RequestContext(request))
        else:
            usuario_invalido = True

    _banners = banner_pagina.objects.all()
    _novedades = novedades.objects.all().order_by('-fecha')
    novedades_paginadas = get_paginacion(request, _novedades, 3)
    inicial = Iniciales.objects.all()
    first = inicial[0]

    return render_to_response('common/inicio.html',
                              {'titulo': "Bienvenido",
                               'usuario_invalido': usuario_invalido,
                               'banners': _banners,
                               'novedades': novedades_paginadas,
                               'ini':inicial,
                               'first':first},
                              context_instance=RequestContext(request))

def acceso_para_compra(request):
    usuario_invalido = False
    resultado = None
    if request.method == 'POST':
        name = request.POST['usuario']
        passwd = request.POST['password']
        usuario = authenticate(username=name, password=passwd)
        if usuario is not None:
            if usuario.is_active:
                login(request, usuario)
                resultado = u'<a id="buyer" href="/ventas/follow">Comprar 2Checkout</a>'
            else:
                return render_to_response('clientes/confirmacion.html',
                                          {'titulo': 'Confirmación'},
                                          context_instance=RequestContext(request))
        else:
            usuario_invalido = True
            resultado = ('<button id="buyerNo">Usuario no encontrado</button>')
    return HttpResponse(resultado)

def get_cliente(request):
    """
    Devuelve el usuario logeado o None
    """
    if request.user.is_authenticated():
        return request.user.username
    else:
        return None
    

def get_paginacion(request, lista_objectos, objetos_pagina):
    """
    Devuelve una lista paginada de una lista de objetos y el
    número de objetos por página
    """
    paginator = Paginator(lista_objectos, objetos_pagina)   
         
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1        
        
    try:
        lista_paginada = paginator.page(page)
    except (EmptyPage, InvalidPage):
        lista_paginada = paginator.page(paginator.num_pages)
        
    return lista_paginada
    
    
def get_productos_cache():
    """
    Devuelve la lista de productos del cache o la consulta en
    caso de que esta esté obsoleta
    """
    productos = cache.get('cache_productos')
    if not productos:
        productos = Producto.objects.filter(estado='A').distinct()
        cache.set('cache_productos', productos)
    return productos
    

def get_tipo_cambio():
    """
    Devuelve el tipo de cambio de compra de dolares en base a soles
    """    
    tipo_cambio = cache.get('cache_cambio')
    if not tipo_cambio:
        # Página de la sunat - tipo de cambio oficial
        url = "http://www.sunat.gob.pe/cl-at-ittipcam/tcS01Alias"
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        page = response.read()
        regex = re.compile("""[\d]+.[\d]+[\s]*</td>[\s]*<td width='8%' align='center' class="tne10">[\s]*[\d]+.[\d]+[\s]*</td>[\s]*</table>""")
        raw = regex.search(page)
        tipo_cambio = raw.group()[:5]
        cache.set('cache_cambio', tipo_cambio, 60*60*24)    
    return tipo_cambio
    
    
def makePassword(length=8):
    """
    Devuelve una cadena aleatoria de tamaño length
    """
    return ''.join(Random().sample(string.letters+string.digits, length))
        
