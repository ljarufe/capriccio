from django.conf.urls.defaults import *

urlpatterns = patterns('projectcapriccio.ventas.views',
    # respuestas json
    url(r'^productos_json/(?P<pagina>\d+)/(?P<id_categoria>\d+)/$', 
        'get_productos_json', name='get_productos_json'),
    url(r'^productos_json_tortas/(?P<pagina>\d+)/$', 
        'get_productos_json_tortas', name='get_productos_json_tortas'),        
    url(r'^productos_json/(?P<pagina>\d+)/$', 'get_productos_json', 
        name='get_productos_json'),
    url(r'^num_paginas_json/$', 'get_numero_paginas_json', 
        name='get_numero_paginas_json'),
    url(r'^num_paginas_json/(?P<id_categoria>\d+)/$', 
        'get_numero_paginas_json', name='get_numero_paginas_json'),
    url(r'^producto_json/(?P<id_producto>\d+)/$', 'get_producto_json', 
        name='get_producto_json'),
    url(r'^detalle_json/(?P<id_producto>\d+)/$', 'get_detalle_json', 
        name='get_detalle_json'),
        
    # urls
    url(r'^productos/$', 'productos', name='productos'),
    url(r'^productos/(?P<id_categoria>\d+)/$', 'productos', name='productos'),
    url(r'^tienda_en_linea/$','tienda_en_linea',name='tienda_en_linea'),
    url(r'^tienda_en_linea/(?P<id_categoria>\d+)/$','tienda_en_linea',name='tienda_en_linea'),
    url(r'^torta_personalizada$', 'torta_personalizada', 
        name='torta_personalizada'),
    url(r'^respuesta$','respuesta_2checkout',name='respuesta_2checkout'),
    url(r'^birthday/$','birthday',name='birthday'),
    url(r'^contact','contact',name='contact'),
    url(r'^cumpleanos','cumpleanos',name='cumpleanos'),
    url(r'^session','get_producto_session',name='get_producto_session'),
    url(r'^confirma','confirmar_session',name='confirmar_session'),
    url(r'^eliminar_session/(?P<id>\d+)/$','eliminar_producto_session',name='eliminar_producto_session'),
    url(r'^follow$','compra_despues_logeo',name='compra_despues_logeo')
)
