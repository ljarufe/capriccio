from django.conf.urls.defaults import *

urlpatterns = patterns('projectcapriccio.empresa.views',
    url(r'^informacion/$', 'informacion', name='informacion'),
    url(r'^tiendas/$', 'tiendas', name='tiendas'),
    url(r'^tiendas/(?P<id_tienda>\d+)$', 'tiendas', name='tiendas'),
    url(r'^detalle_tienda/(?P<id_tienda>\d+)$', 'detalle_tienda', 
        name='detalle_tienda'),
    url(r'^equipo_trabajo/$', 'equipo_trabajo', name='equipo_trabajo'),
    url(r'^contact/$','contacto',name='contacto'),
    
)
