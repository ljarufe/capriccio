from django.db import models
from django import forms
from django.forms import widgets
from projectcapriccio.sorl.thumbnail.fields import ImageWithThumbnailsField
from PIL import Image
from projectcapriccio.common.models import Imagen
from widget import *
from gdata.youtube.service import *
from gdata.media import Group, Title, Description, Keywords, Category
from gdata.youtube import *
from os.path import dirname
import os


basedir = dirname(__file__)
# Create your models here.
status = (
          ('A', 'Activo'),
          ('I', 'Inactivo')
          )

acceso_youtube = {
                  'email':'mauri544@gmail.com',
                  'password':'alejandrajara',
                  'source':'capriccio',
                  'developer_key':'AI39si5VB_vbIY1TZnq_3GkK-wI3r_uPl2WTiwlhjRuIAXoUu1jC2E4EBpeN3JqsLGz83hrVvuJaK5J4Jb56dqLohJKbbmeMoQ',
                  'client_id':'capriccio'
                  }

def auth():
    yt = YouTubeService()
    yt.email = acceso_youtube["email"]
    yt.password = acceso_youtube["password"]
    yt.source = acceso_youtube["source"]
    yt.developer_key = acceso_youtube["developer_key"]
    yt.client_id = acceso_youtube["client_id"]
    yt.ProgrammaticLogin()
    return yt
    
"""
clase para la personalizacion de un TextArea
"""

class markitup(widgets.Textarea):
    class Media:
        js = (
              '/media/js/jquery-1.3.2.js',
              '/media/markitup/markitup/jquery.markitup.js',
              '/media/markitup/markitup/sets/html/set.js',
              )
        css = {
               'screen':(
                         '/media/markitup/markitup/skins/simple/style.css',
                         '/media/markitup/markitup/sets/html/style.css',
                         )
               }
"""
modelo para la administracion de las paginas creadas
"""
class pagina(models.Model):
    nombre = models.CharField(max_length = 45, unique = True)
    
    def __unicode__(self):
        return '%s' % self.nombre
"""
modelo para la incorporacion de contenidos por pagina
"""
class contenido_pagina(models.Model):
    contenido = models.TextField(blank = False, help_text = 'Editar contenido de la pagina')
    pagina = models.ForeignKey(pagina)
    estado = models.CharField(max_length = 1, choices = status)
    
    class Meta:
        verbose_name = "Contenido"
        verbose_name_plural = "Contenidos"
    
    def __unicode__(self):
        return '%s' % self.contenido
    
    def contenido_admin(self):
        if self.contenido:
            return u'%s' % self.contenido
        else:
            return 'Sin contenido'
    contenido_admin.short_description = 'Vista previa'
    contenido_admin.allow_tags = True
    
"""
modelo para la incorporacion de banners animados flash
"""   
    
class flash_pagina(models.Model):
    nombre = models.CharField(max_length = 45, blank = True, unique = True)
    objeto = models.FileField(upload_to = 'swf', max_length = 90, help_text = 'Solo archivos .swf')
    estado = models.CharField(max_length = 1, choices = status, default = 'A')
    pagina = models.ForeignKey(pagina)
    
    class Meta:
        verbose_name = "Banner animado Pagina"
        verbose_name_plural = "Banners animados Pagina"
    
    def __unicode__(self):
        return '%s' % self.objeto
    
    def mostrar_flash(self):
        if self.objeto:
            return u'<object width="100" height="100"><param name="movie" value="/media/%s"><param name=wmode value=transparent><embed src="/media/%s" width="100" height="100"></embed></object>' % (self.objeto, self.objeto)
        else:
            return 'Sin atributos'
        
    mostrar_flash.short_description = 'Banner Flash'
    mostrar_flash.allow_tags = True    

"""
modelo para la incorporacion de banners estaticos
"""

class banner_pagina(models.Model):
    nombre = models.CharField(max_length = 25)
    descripcion = models.CharField(max_length = 45)
    imagen = ImageWithThumbnailsField(upload_to = 'imagenes',
                                      thumbnail = {'size': (195, 1800)},
                                      generate_on_save = True,
                                      verbose_name = 'Imagen'
                                      )
    pagina = models.ForeignKey(pagina)
    
    class Meta:
        verbose_name = "Banner vertical"
        verbose_name_plural = "Banners verticales"
    
    def __unicode__(self):
        return '%s' % self.nombre
    
    def img_admin(self):
        if self.imagen:
            return u'<a href="/media/%s" target="blank"><img src="%s"/></a>' % (self.imagen, self.imagen.thumbnail)
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
            return u'/media/%s Formato : %s Tamano : %s' % (self.imagen, img.format, img.size)
        else:
            return 'Sin datos'
        
    propiedades_imagen.shot_description = 'Propiedades'

"""
modelo para la incorporacion de novedades solo texto
"""    
class novedades(models.Model):
    fecha = models.DateField()
    titulo = models.CharField(max_length = 45,blank = False, unique = True)
    texto = models.TextField(blank = False, help_text = 'Texto de las novedades')
    pagina = models.ForeignKey(pagina)
    imagen = models.ForeignKey(Imagen)
    
    class Meta:
        verbose_name = "Novedad"
        verbose_name_plural = "Novedades"
    
    def __unicode__(self):
        return '%s %s' % (self.texto, self.fecha)
    
    #def novedades_img(self):
    #    img = imagen_novedades.objects.get(novedades = self)
    #    if img <> "":
    #        return u'<div><a href="/media/%s" style="float:left;"><img src="%s"/></a><span style="float:right;">%s</span><div>' % (img.imagen, img.imagen.thumbnail, self.texto)
    #    else:
    #        return 'Sin datos'
    #novedades_img.short_description = 'Thumbnail'
    #novedades_img.allow_tags = True
        

"""
modelo para agregar un video a youtube desde django admin, utilizando el api de youtube
"""

class video_pagina(models.Model):
    titulo = models.CharField(max_length = 45, blank = False, unique = True, help_text = 'nombre corto')
    descripcion = models.CharField(max_length = 45, blank = False, help_text = 'breve descripcion para el video')
    claves = models.CharField(max_length = 45, blank = False, help_text = 'Palabras clave que identifiquen al video')
    video = models.FileField(upload_to = 'videos', help_text = 'archivo en formatos de video')
    pagina = models.ForeignKey(pagina)
    
    class Meta:
        verbose_name = "Video Pagina"
        verbose_name_plural = "Videos Pagina"
        
    def __unicode__(self):
        return '%s %s %s' % (self.titulo, self.video, self.pagina)
    
    
    
    def save(self):
        super(video_pagina, self).save()
        coneccion = auth()
        my_media_group = Group(
                               title = Title(text = self.titulo),
                               description = Description(
                                                        text = self.descripcion
                                                         ),
                               keywords = Keywords(
                                                   text = self.claves
                                                   ),
                               category = [Category(
                                                    text = 'Autos',
                                                    scheme = 'http://gdata.youtube.com/schemas/2007/categories.cat',
                                                    label = 'Autos'
                                                    )],
                               player = None
                               )
        video_entry = YouTubeVideoEntry(media = my_media_group)
        video_file_location = '%s/Aptana Studio/capriccio/media/%s' % (os.environ['HOME'], self.video)
        new_entry = coneccion.InsertVideoEntry(video_entry, video_file_location)
        upload_video = coneccion.CheckUploadStatus(new_entry)
        if upload_video is not None:
            def devuelve_id(entry):
                return entry.media.player.url
            video_id = devuelve_id(new_entry)    
            video = video_identificador(
                                 videoID = video_id,
                                 video = self
                                 ) 
            video.save()
            
    def mostrar_video_admin(self):
        video_id = video_identificador.objects.get(video = self)
        if video_id:
            video_original = str(video_id)
            ruta = video_original.split('&')[0]
            ruta_final = ruta.split('=')[1]
            return u'<object width="300" height="200"><param name="movie" value="http://www.youtube.com/v/%s"></param><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param><embed src="http://www.youtube.com/v/%s" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" width="300" height="200"></embed></object>' % (ruta_final, ruta_final)
        else:
            return 'No existe el video'
    mostrar_video_admin.short_description = 'Video'
    mostrar_video_admin.allow_tags = True

class video_identificador(models.Model):
    videoID = models.TextField()
    video = models.ForeignKey(video_pagina)
    
    def __unicode__(self):
        return self.videoID

"""
campo de formulario personalizado    
"""

class pagina_form(forms.ModelForm):
    cuerpo = forms.CharField(widget = markitup())
    
    class Meta:
        model = contenido_pagina
        #exclude = ('contenido',)

"""
modelo para la incorporacion de ubicaciones en base a latitud y longitud
"""

class place(models.Model):
    latitud = models.DecimalField(max_digits = 8, decimal_places = 6)
    longitud = models.DecimalField(max_digits = 8, decimal_places = 6)
    
    class Meta:
        verbose_name = "Ubicacion"
        verbose_name_plural = "Ubicaciones"
    
    def __unicode__(self):
        return '%s,%s' % (self.latitud, self.longitud)


class form_place(forms.ModelForm):
    
    class Meta:
        model = place
