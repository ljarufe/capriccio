# -*- coding: utf-8 -*-

'''
@author: lucho
'''

from django.core.cache import cache
from django import template

from projectcapriccio.empresa.models import Tienda
from projectcapriccio.ventas.models import Categoria

register = template.Library()

@register.inclusion_tag('common/templatetags/cache_tiendas.html')
def get_tiendas():
    """
    Etiqueta para mostrar las tiendas guardadas en cache
    """
    tiendas = cache.get('cache_tiendas')
    if not tiendas:
        tiendas = Tienda.objects.all()
        cache.set('cache_tiendas', tiendas)
    return {'tiendas': tiendas}

@register.inclusion_tag('common/templatetags/cache_categorias.html')
def get_categorias():
    """
    Etiqueta para mostrar las categorias guardadas en cache
    """
    categorias = cache.get('cache_categorias')
    if not categorias:
        categorias = Categoria.objects.all()
        cache.set('cache_categorias', categorias)
    return {'categorias': categorias}
