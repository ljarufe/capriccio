'''
Created on 11/03/2010

@author: mauricio
'''
from django.conf.urls.defaults import *

urlpatterns = patterns('projectcapriccio.paginas.views',
    url(r'^grabar_localizacion$', 'grabar_ubicacion', name='grabar_localizacion'),
    #url(r'^nueva$',"nuevaUbicacion",name="nuevaUbicacion"),
)
