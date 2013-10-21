# -*- coding: utf-8 -*-
    
'''
@author: lucho, mauricio
'''

from django.db import models
from projectcapriccio.sorl.thumbnail.fields import ImageWithThumbnailsField
from django.contrib.auth.models import User
from PIL import Image
from gdata.tlslite.utils.jython_compat import SelfTestBase

class Ciudad(models.Model):
    """
    Lista de ciudades en las que existe una tienda
    """
    nombre = models.CharField(max_length=30, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    
    def __unicode__(self):
        return '%s' % self.nombre
    
    class Meta:
        verbose_name_plural = 'ciudades'
        

class Direccion(models.Model):
    """
    Dirección genérica para tiendas y usuarios
    """
    lugar = models.CharField(max_length=30, verbose_name='dirección')
    ciudad = models.ForeignKey(Ciudad)
    
    def __unicode__(self):
        return '%s - %s' % (self.lugar, self.ciudad)
    
    class Meta:
        verbose_name_plural = "direcciones"
    
class LugarEntrega(models.Model):
    lugar = models.CharField(max_length=200,blank=False,null=False)
    ciudad = models.ForeignKey(Ciudad)

    def __unicode__(self):
        return '%s' % self.lugar

    class Meta:
        verbose_name = 'Lugar Entrega Permitido'
        verbose_name_plural = 'Lugares Entrega Permitidos'

class RecargoEntrega(models.Model):
    lugar = models.CharField(max_length=200,blank=False,null=False)
    recargo = models.FloatField('Recargo')
    ciudad = models.ForeignKey(Ciudad)

    def __unicode__(self):
        return '%s - %s' % (self.lugar,self.recargo)

    def tablaEntrega(self):
        if self.lugar:
            return u'<tr><td>%s</td><td>%s</td></tr>' % (self.lugar,self.recargo)

    class Meta:
        verbose_name = 'Recargo por zona de entrega'
        verbose_name_plural = u'Recargos según zona de entrega'

class Imagen(models.Model):
    """
    Imagen genérica para tiendas y productos
    """
    nombre = models.CharField(max_length=30, blank=True, null=True)
    imagen = ImageWithThumbnailsField(upload_to = 'imagenes',
                                      thumbnail={'size': (160, 110)},
                                      extra_thumbnails={'medium': {'size': (400, 400)}},                                                                                            
                                      generate_on_save = True,
                                      verbose_name='Imagen'
                                      )
    

    class Meta:
        verbose_name_plural = "imágenes"
    
    def __unicode__(self):
        return '%s' % self.nombre
    
    def img_admin(self):
        if self.imagen:
            return u'<a href="/media/%s" target="blank"><img src="%s"/></a>' % \
                   (self.imagen,self.imagen.thumbnail)
        else:
            return 'No tiene imagen'
        
    img_admin.short_description = 'Imagen'
    img_admin.allow_tags = True
    
    def nombre_thumbnail(self):
        if self.imagen:
            return u'%s' % self.imagen.thumbnail
        else:
            return 'No existe la miniatura'
    nombre_thumbnail.short_description = 'Thumbnail'
    
    def propiedades_imagen(self):
        if self.imagen:
            img = Image.open(self.imagen)
            return u'/media/%s Formato : %s Tamaño : %s' % \
                   (self.imagen,img.format,img.size)
        else:
            return 'Sin datos'
        
    propiedades_imagen.shot_description = 'Propiedades' 
    
    
class Usuario(models.Model):
    """
    Usuario abstracto con todos los permisos
    """
    user = models.ForeignKey(User, unique=True)
    
    class Meta:
        abstract = True
        
class Iniciales(models.Model):
    """
    Imagenes iniciales galeria
    """
    nombre = models.CharField(max_length=45,blank=True,null=True)
    imagen = ImageWithThumbnailsField(
                upload_to = 'img/inicio',
                thumbnail={'size': (650, 420), 
                           'options': ['upscale', 'max', 'crop']},
                extra_thumbnails={'galeria': {'size': (280, 140),
                                              'options': ['crop', 'upscale']},
                                  'resumen': {'size': (760, 200)},
                                  'detalle': {'size': (760, 200),
                                              'options':['crop','upscale']}
                                  },
                generate_on_save = True,
                verbose_name='Foto del proyecto'
                )
    
    def __unicode__(self):
        return '%s - %s' % (self.imagen,self.nombre)
    
    def img_admin(self):
        if self.imagen:
            return u'<a href="/media/%s" target="blank"><img src="%s"/></a>' % \
                   (self.imagen,self.imagen.extra_thumbnails['galeria'])
        else:
            return 'No tiene imagen'
        
    img_admin.short_description = 'Imagen'
    img_admin.allow_tags = True
    
class Tortas_Cumpleanos(models.Model):
    """
    Imagenes tortas
    """
    nombre = models.CharField(max_length=45,blank=True,null=True)
    imagen = ImageWithThumbnailsField(
                upload_to = 'img/cakes',
                thumbnail={'size': (650, 420), 
                           'options': ['upscale', 'max', 'crop']},
                extra_thumbnails={'galeria': {'size': (280, 140),
                                              'options': ['crop', 'upscale']},
                                  'resumen': {'size': (250, 155)},
                                  'detalle': {'size': (560, 350)},
                                  'presentacion':{'size':(600,600)}
                                  },
                generate_on_save = True,
                verbose_name=u'Foto Torta de Cumpleaños'
                )
    
    def __unicode__(self):
        return '%s' % self.imagen

    class Meta:
        verbose_name = u'Torta de Cumpleaños'
        verbose_name_plural = u'Tortas de Cumpleaños'
    
class Torta_Personalizada(models.Model):
    """
    Imagenes para tortas personalizadas
    """
    nombre = models.CharField(max_length=90,blank=False,null=False,verbose_name='Nombre de la Imagen',help_text='frases de una sola palabra')
    descripcion = models.TextField(blank=True,null=True,verbose_name=u'Descripción de la Imagen',help_text=u'Descripción exacta de la imagen a subir')
    imagen = ImageWithThumbnailsField(
                upload_to = 'img/cakes',
                thumbnail={'size': (460, 180), 
                           'options': ['upscale', 'max', 'crop']},
                extra_thumbnails={'galeria': {'size': (100, 90),
                                              'options': ['crop', 'upscale']},
                                  'resumen': {'size': (250, 155)},
                                  'detalle': {'size': (460, 350)},
                                  'presentacion':{'size':(700,700)}
                                  },
                generate_on_save = True,
                verbose_name=u'Foto Personalizada',
                help_text=u'Imagen Personalizada a subir'
                )    
        
    def __unicode__(self):
        return '%s' % self.nombre
    
    def img_admin(self):
        if self.imagen:
            return u'<a href="/media/%s" target="blank"><img src="%s"/></a>' % \
                   (self.imagen,self.imagen.thumbnail)
        else:
            return 'No tiene imagen'
        
    img_admin.short_description = 'Imagen'
    img_admin.allow_tags = True

    class Meta:
        verbose_name = u'Torta Personalizada'
        verbose_name_plural = u'Tortas Personalizadas'