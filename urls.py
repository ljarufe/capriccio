from django.conf.urls.defaults import *
from projectcapriccio.common.views import inicio,acceso_para_compra,bienvenida
from projectcapriccio.paginas.views import grabar_ubicacion,modificarUbicacion,nuevaUbicacion
from projectcapriccio.admin.views import admin_correos,creacion_mailbox_email,cambiar_contrasena,eliminar_mailbx_email
from projectcapriccio.notificaciones.views import nuevasNotificaciones,generadorStreaming,cambiar_estado

#from admin.admin import *
import os
# admin 
from django.contrib import admin
#from conf.urls.defaults import include
admin.autodiscover()

from os.path import dirname
basedir = dirname(__file__)

static_media = '%s/media/' % basedir
media = '%s/media/' % basedir

urlpatterns = patterns('',
    # apps 
    (r'^clientes/', include('projectcapriccio.clientes.urls')),
    (r'^empresa/', include('projectcapriccio.empresa.urls')),
    (r'^notificaciones/', include('projectcapriccio.notificaciones.urls')),
    (r'^ventas/', include('projectcapriccio.ventas.urls')),
    
    # admin
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^paginas/', include('projectcapriccio.paginas.urls')),
    (r'^modificar', modificarUbicacion),
    (r'^nueva/ubicacion',nuevaUbicacion),
    
    #(r'^admin/paginas/place/grabar_localizacion', grabar_ubicacion),
    #(r'^modificar', modificarUbicacion),

    
    # static and media urls
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': static_media, 'show_indexes': True}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': media, 'show_indexes': True}),
    
    # prueba contenido pag
    (r'^paginas/', include('projectcapriccio.paginas.urls')),

    #(r'^messages/',include('messages.urls')),
    # pagina de logeo
    (r'^accounts/login/$', inicio),
    (r'^acceso/compra/$',acceso_para_compra),
    # pagina de inicio
    #$url(r'^$', 'projectcapriccio.common.views.bienvenida', name = 'inicio'),
    url(r'^$', 'projectcapriccio.common.views.inicio', name = 'inicio'),
    
    # sitemap
    #(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps})
    
    #administracion de correos
    (r'^adminCorreos',admin_correos),
    (r'^crearCorreo',creacion_mailbox_email),
    (r'^cambioPass',cambiar_contrasena),
    (r'^delete',eliminar_mailbx_email),
    
    #notificaciones
    (r'^notice',include('projectcapriccio.notification.urls')),
    (r'^notas',nuevasNotificaciones),
    (r'^notitas',generadorStreaming),
    (r'^visto',cambiar_estado),
)
