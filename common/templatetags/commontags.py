# -*- coding: utf-8 -*-

'''
@author: lucho
'''
from django import template
from projectcapriccio.clientes.models import Cliente
from projectcapriccio.empresa.models import Tienda

register = template.Library()

@register.inclusion_tag('common/templatetags/nombre_usuario.html')
def get_nombre_usuario(user):
    """
    Etiqueta para sacar el nombre de un usuario
    """
    if user.is_staff:
        nombre = user.username
    else:
        cliente = Cliente.objects.get(user=user.id)
        nombre = '%s' % (cliente.nombres)
    return {'nombre': nombre}

@register.inclusion_tag('common/templatetags/cache_tiendas_principal.html')
def get_tienda_principal():
    """
    Etiqueta para mostrar las tiendas principal
    """    
    tienda = Tienda.objects.all()[:1]
    return {'tienda': tienda[0]}