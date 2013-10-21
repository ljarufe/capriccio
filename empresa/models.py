# -*- coding: utf-8 -*-
'''
@author: lucho
'''

from django.db import models
from projectcapriccio.common.models import Direccion, Imagen
from projectcapriccio.ventas.models import Producto
from projectcapriccio.paginas.models import *
from django.conf import settings
from django.template.loader import render_to_string
from django import forms
import django.forms as forms

class Empresa(models.Model):
    """
    Modelo para la actualización de los datos de la empresa
    """
    historia = models.TextField(blank=True, null=True)
    mision = models.TextField(blank=True, null=True)
    vision = models.TextField(blank=True, null=True)
    valores = models.TextField(blank=True, null=True)
    razon_social = models.TextField()
    ruc = models.CharField(max_length=11, verbose_name='RUC')
    
    def __unicode__(self):
        return '%s' % self.razon_social
    

class FotoEquipo(models.Model):
    """
    Modelo que guarda una foto del equipo de trabajo
    """
    titulo = models.CharField(max_length=20, blank=True, null=True)
    imagen = models.ImageField(upload_to='imagenes', 
                             verbose_name="Página de la carta")
                             
    def __unicode__(self):
        return '%s' % self.titulo        
                             
    class Meta:
        verbose_name = 'Foto del equipo'
        verbose_name_plural = 'Fotos del equipo'


class LocationField(models.CharField):

    def formfield(self, **kwargs):
        kwargs['widget'] = LocationPickerWidget
        return super(LocationField, self).formfield(**kwargs)


class Tienda(models.Model):
    """
    Información de una tienda
    """
    nombre_corto = models.CharField(max_length=25)
    direccion = models.ForeignKey(Direccion)
    telefono = models.CharField(max_length=15)
    ubicacion = models.OneToOneField(place,null=True)
    productos = models.ManyToManyField(Producto, null=True)
    email_contacto = models.EmailField(max_length=120,blank=True,null=False)
    persona_contacto = models.CharField(max_length=180,blank=True,null=True)
    #email = models.EmailField(help_text='E-mail de contacto perteneciente a la tienda')
    
    def __unicode__(self):
        return '%s' % self.nombre_corto   
    
    
class LocationPickerWidget(forms.TextInput):
    class Media:
        css = {
            'all': (
                settings.MEDIA_URL + 'css/location_picker.css',
            )
        }
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js',
            'http://www.google.com/jsapi?key=' + settings.MAPS_API_KEY,
            settings.MEDIA_URL + 'js/jquery.location_picker.js',
        )

    def __init__(self, language=None, attrs=None):
        self.language = language or settings.LANGUAGE_CODE[:2]
        super(LocationPickerWidget, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None):
        if None == attrs:
            attrs = {}
        attrs['class'] = 'location_picker'
        return super(LocationPickerWidget, self).render(name, value, attrs)
   
    
class CartaTienda(models.Model):
    """
    Imágen correspondiente a la carta de una tienda
    """
    tienda = models.ForeignKey(Tienda)
    pagina = models.ImageField(upload_to='imagenes', 
                               verbose_name="Página de la carta")
    
    class Meta:
        verbose_name = 'Carta de la tienda'
        verbose_name_plural = 'Carta de las tiendas'
        
    def __unicode__(self):
        return '%s' % self.tienda
    

class ImagenTienda(models.Model):
    """
    Imágen de una tienda
    """
    tienda = models.ForeignKey(Tienda)
    imagen = ImageWithThumbnailsField(upload_to = 'imagenes',
                                      thumbnail={'size': (210, 200)},
                                      extra_thumbnails={'medium': {'size': (400, 400)}},
                                      generate_on_save = True,
                                      verbose_name='Imagen'
                                      )

    class Meta:
        verbose_name = 'Imágen de la tienda'
        verbose_name_plural = 'Imágenes de las tiendas'
        
    def __unicode__(self):
        return '%s' % self.tienda
        
class select_popup(forms.Select):
    def render(self,name,*args,**kwargs):
        html = super(select_popup,self).render(name,*args,**kwargs)
        popup = render_to_string("add_plus.html",{"field":name})
        return html + popup
        
class formulario_tienda(forms.ModelForm):
    ubicacion = forms.ModelChoiceField(place.objects,widget = select_popup)
    
    class Meta:
        models = Tienda
        fields = ["nombre_corto","direccion","telefono","productos","ubicacion","email_contacto","persona_contacto"]
