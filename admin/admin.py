# -*- coding: utf-8 -*-

'''
Created on 09/03/2010

@author: mauricio
'''
from django.contrib import admin
from django.shortcuts import render_to_response
from django.contrib.admin.views.main import ChangeList, ERROR_FLAG
#models
from projectcapriccio.clientes.models import Cliente
from projectcapriccio.common.models import Ciudad,Direccion,Usuario,Imagen,Iniciales,Tortas_Cumpleanos,Torta_Personalizada,LugarEntrega,RecargoEntrega
from projectcapriccio.empresa.models import Empresa,ImagenTienda,Tienda, CartaTienda,formulario_tienda#, FotoEquipo
#from empresa.forms import *
from projectcapriccio.ventas.models import Categoria,Subcategoria,Producto,Producto_item,Compra,Personalizado_item,Personalizado_arte
from projectcapriccio.paginas.models import banner_pagina,contenido_pagina,flash_pagina,novedades,place,pagina,video_pagina,pagina_form
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext

from projectcapriccio.paginas.views import grabar_ubicacion,modificarUbicacion
from projectcapriccio.common.forms import PersonalizadaForm
"""
funcion para activar un elemento en la pagina
"""

def activar(self, request, queryset):
    filas_modificadas = queryset.update(estado = 'A')
    if filas_modificadas == 1:
        mensaje = '1 elemento fue activado'
    else:
        mensaje = '%s elementos fueron activados' % filas_modificadas
    self.message_user(request, '%s exitosamente ' % mensaje)  
activar.short_description = 'Activar'

def desactivar(self, request, queryset):
    filas_modificadas = queryset.update(estado = 'I')
    if filas_modificadas == 1:
        mensaje = '1 elemento fue desactivado'
    else:
        mensaje = '%s elementos fueron desactivados' % filas_modificadas
    self.message_user(request, '%s exitosamente ' % mensaje)   
desactivar.short_description = 'Desactivar'

def abono(self,request,queryset):
    filas_modificadas = queryset.update(abono = True)
    if filas_modificadas == 1:
        mensaje = '1 elemento fue desactivado'
    else:
        mensaje = '%s elementos fueron desactivados' % filas_modificadas
    self.message_user(request, '%s exitosamente ' % mensaje)   
abono.short_description = 'Abonar'
        
class IncorrectLookupParameters(Exception):
    pass

class admin_cliente(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'direccion', 'email')

class cliente_en_linea(admin.StackedInline):
    model = Cliente

class admin_ciudad(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    
class admin_direccion(admin.ModelAdmin):
    list_display = ('lugar', 'ciudad')
    
class admin_imagen(admin.ModelAdmin):
    list_display = ('nombre', 'img_admin', 'nombre_thumbnail', 'propiedades_imagen')
     
class admin_empresa(admin.ModelAdmin):
    list_display = ('historia', 'mision', 'vision', 'valores')

#class admin_imagen_tienda(admin.ModelAdmin):
#    list_display = ('nombre','img_admin')
#    list_filter = ('tienda',)
#    search_fields = ['nombre']
#    
#    actions = [activar,desactivar]

#class imagen_tienda_enlinea(admin.TabularInline):
#    model = ImagenTienda
    
  
class admin_tienda(admin.ModelAdmin):
    form = formulario_tienda
    list_display = ('direccion', 'telefono', 'ubicacion')
    
    search_fields = ['direccion',"nombre_corto",]
    #list_filter = ('estado',)
    actions = [activar, desactivar]
    

class AdminImagenTienda(admin.ModelAdmin):
    list_display = ('tienda', 'imagen')
    

class AdminCartaTienda(admin.ModelAdmin):
    list_display = ('tienda', 'pagina')
    

class admin_producto(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'img_producto')
    list_filter = ('estado',)
    
    actions = [activar, desactivar]
    
class admin_categoria(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')

class banner_en_linea(admin.TabularInline):
    model = banner_pagina
    extra = 2
        
class admin_pagina(admin.ModelAdmin):
    inlines = [banner_en_linea]

class admin_contenido(admin.ModelAdmin):
    form = pagina_form
    list_filter = ('pagina', 'estado')
    list_display = ('contenido', 'contenido_admin')
    actions = [activar, desactivar]

class admin_banner(admin.ModelAdmin):
    list_display = ('nombre', 'img_admin', 'nombre_thumbnail', 'propiedades_imagen')
    list_filter = ('descripcion', 'pagina')
    search_fields = ['nombre']
    
    
class admin_novedades(admin.ModelAdmin):
    list_display = ('titulo','texto', 'fecha', 'pagina', 'imagen')
    list_filter = ('fecha',)
    
class admin_flash_pagina(admin.ModelAdmin):
    list_display = ('nombre', 'mostrar_flash')
    actions = [activar, desactivar]
    
class admin_video(admin.ModelAdmin):
    list_display = ('titulo', 'descripcion', 'video', 'mostrar_video_admin')
    
class admin_place(admin.ModelAdmin):
    list_display = ("latitud", "longitud",)
    change_list_template = 'place.html'
    lugar = '' 
    def changelist_view(self, request, extra_context = None):
        if not self.has_change_permission(request, None):
            raise PermissionDenied
        
        if request.method == "GET":
            if "action" in request.GET:
                return grabar_ubicacion(request)
        opts = self.model._meta
        app_label = opts.app_label
        try:
            cl = ChangeList(request, self.model, self.list_display, self.list_display_links, self.list_filter,
                self.date_hierarchy, self.search_fields, self.list_select_related, self.list_per_page, self.change_list_template, self)
            cl.formset = None   
        except IncorrectLookupParameters:
            if ERROR_FLAG in request.GET.keys():
                return render_to_response('admin/invalid_setup.html', {'title': _('Database error')})
            return HttpResponseRedirect(request.path + '?' + ERROR_FLAG + '=1')
        lugar = place.objects.all()
        context = { 
            'title': 'Administracion de Ubicacion Tiendas',
            'is_popup': cl.is_popup,
            'cl': cl,
            'has_add_permission': self.has_add_permission(request),
            'root_path': self.admin_site.root_path,
            'app_label': app_label,
            'lugar':lugar,
        }
        context.update(extra_context or {})
        return render_to_response(self.change_list_template, context)

class admin_personalizada(admin.ModelAdmin):
    form = PersonalizadaForm
    list_display = ('nombre','img_admin')

class admin_iniciales(admin.ModelAdmin):
    list_display = ('nombre','img_admin')    

admin.site.register(Imagen,admin_imagen)
admin.site.register(Empresa, admin_empresa)
admin.site.register(Tienda, admin_tienda)
admin.site.register(ImagenTienda, AdminImagenTienda)
admin.site.register(CartaTienda, AdminCartaTienda)
admin.site.register(Producto, admin_producto)
admin.site.register(pagina, admin_pagina)
admin.site.register(Categoria, admin_categoria)
admin.site.register(Subcategoria)
#admin.site.register(FotoEquipo)
admin.site.register(Ciudad, admin_ciudad)
admin.site.register(Direccion, admin_direccion)
admin.site.register(Cliente, admin_cliente)
admin.site.register(contenido_pagina, admin_contenido)
admin.site.register(banner_pagina, admin_banner)
admin.site.register(novedades, admin_novedades)
#admin.site.register(flash_pagina, admin_flash_pagina)
#admin.site.register(video_pagina, admin_video)
admin.site.register(place, admin_place)
admin.site.register(Producto_item)
#admin.site.register(Compra)
#admin.site.register(Producto_item)
admin.site.register(Personalizado_arte)
admin.site.register(Iniciales,admin_iniciales)
admin.site.register(Tortas_Cumpleanos)
admin.site.register(LugarEntrega)
admin.site.register(RecargoEntrega)
admin.site.register(Torta_Personalizada,admin_personalizada)