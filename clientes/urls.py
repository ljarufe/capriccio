# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('projectcapriccio.clientes.views',
    url(r'^registro/$', 'registro_cliente', name='registro_cliente'),
    url(r'^registro_compra/$','registro_acceso_compra',name='registro_acceso_compra'),
    url(r'^verificar/(?P<clave>[\w]+)/$', 'verificar_cliente', 
        name='verificar_cliente'),
    url(r'^cerrar_sesion$', 'cerrar_sesion', name='cerrar_sesion'),
    url(r'^opciones_usuario$', 'opciones_usuario', name='opciones_usuario'),
    url(r'^recuperar_password$', 'recuperar_password', 
        name='recuperar_password'),
    url(r'^recuperar_password/(?P<clave>[\w]+)/(?P<password>[\w]+)/$',
        'recuperar_password', name='recuperar_password'),
    url(r'^eliminar_cliente/(?P<clave>[\w]+)/$', 'eliminar_cliente', 
        name='eliminar_cliente'),
    url(r'^eliminar_cliente/$', 'eliminar_cliente', name='eliminar_cliente'),
     
	# respuestas json
    url(r'^usuario_unico_json/(?P<email>[\w]+.[\w]+@[\w]+.[\w]+)/$', 
    	'usuario_unico_json', name='usuario_unico_json'),
    # TODO: La expresión regular para contraseñas debe ser verificada
    url(r'^verificar_password_json/(?P<password>[\w]+)/$', 
        'verificar_password_json', name='verificar_password_json'),
    url(r'^cambiar_password_json/(?P<password>[\w]+)/$', 
        'cambiar_password_json', name='cambiar_password_json'),
)
