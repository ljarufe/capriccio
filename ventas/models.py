# -*- coding: utf-8 -*-

'''
@author: lucho
'''

from django.db import models
from projectcapriccio.common.models import Imagen, Direccion
#from datetime import datetime
from projectcapriccio.notification.models import Compra
    
from django.contrib.auth.models import User

import datetime


class Categoria(models.Model):
    """
    Categoría de un producto
    """
    nombre = models.CharField(max_length=30)
    descripcion = models.TextField(blank=True, null=True)
    
    def __unicode__(self):
        return '%s' % self.nombre

class Subcategoria(models.Model):
    """
    Subcategoria de un producto
    """
    nombre = models.CharField(max_length=45)
    descripcion = models.TextField(blank=True,null=True)

    def __unicode__(self):
        return '%s' % self.nombre

class Producto(models.Model):
    """
    Producto
    """
    nombre = models.CharField(max_length=30)
    descripcion = models.TextField()
    imagen = models.ForeignKey(Imagen,blank=True,null=True)
    precio = models.FloatField()
    categoria = models.ForeignKey(Categoria)
    subcategoria = models.ForeignKey(Subcategoria,blank=True,null=True)
    STATUS_CHOICE = (
          ('A','activo'),
          ('I','inactivo'),
    )
    estado = models.CharField(max_length=1, choices=STATUS_CHOICE, default='A')
    personalizable = models.BooleanField(default=False)
    compra_online = models.BooleanField(default=False, 
                                        verbose_name='Compra online?')
    
    def __unicode__(self):
        return '%s' % self.nombre
    
    def img_producto(self):
        if self.imagen:
            return u'<a href="/media/%s" target="blank"><img src="%s" border="0"/></a>' % (self.imagen.imagen,self.imagen.imagen.thumbnail)
        else:
            return 'Producto sin Imagen'
        
    img_producto.short_description = 'Imagen'
    img_producto.allow_tags = True  
      
class Producto_item(models.Model):
    """
    Factura: detalle
    """
    compra = models.ForeignKey(Compra)
    cantidad = models.IntegerField()
    producto = models.ForeignKey(Producto)
    
    def __unicode__(self):
        return '%s' % self.producto


class Personalizado_item(Compra):
    """
    Detalle para una compra de una torta personalizada
    """
    foto = models.ForeignKey(Imagen, verbose_name='Foto')
    mensaje = models.CharField(max_length=30)
    producto = models.ForeignKey(Producto)
    
class Personalizado_arte(Imagen):
    
    nombre_arte = models.CharField(max_length = 45, blank = False)
    
    def __unicode__(self):
        return u'%s' % self.nombre
    
    class Meta:
        verbose_name = u"Imagen Celebración"
        verbose_name_plural = u"Imágenes Celebraciones"