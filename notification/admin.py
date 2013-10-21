from django.contrib import admin
from projectcapriccio.notification.models import NoticeType, NoticeSetting, Notice, ObservedItem,Compra
from projectcapriccio.common.models import *
from django.contrib.admin.views.main import ChangeList, ERROR_FLAG
from django.shortcuts import render_to_response
from projectcapriccio.notification.models import get_tipo_cambio
class IncorrectLookupParameters(Exception):
    pass

def dinero_en_cuenta(self,request,queryset):
    filas_modificadas = queryset.update(abono = True)
    if filas_modificadas == 1:
        mensaje = '1 elemento fue desactivado'
    else:
        mensaje = '%s elementos fueron desactivados' % filas_modificadas
    self.message_user(request, '%s exitosamente ' % mensaje)   
dinero_en_cuenta.short_description = 'Abonar'

class NoticeTypeAdmin(admin.ModelAdmin):
    list_display = ('label', 'display', 'description', 'default')

class NoticeSettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'notice_type', 'medium', 'send')

class NoticeAdmin(admin.ModelAdmin):
    list_display = ('message', 'user', 'notice_type', 'added', 'unseen', 'archived')

class CompraAdmin(admin.ModelAdmin):
    actions = [dinero_en_cuenta]
    list_display = ("cliente","total","fecha_pedido","fecha_entrega","direccion_entrega","abono","status")
    list_filter = ("fecha_pedido","abono",)
    #search_fields = ["direccion_entrega",'total',"cliente"]
    
    list_per_page = 10
    change_list_template = 'totales_tiendas.html'
     
    def changelist_view(self, request, extra_context = None):
        compras = ""
        ciudad = ""
        
        lista = []
        lista_usd = []
        lista_ciudad = []
        tipo_cambio = 0
        cambio = 0
        if not self.has_change_permission(request, None):
            raise PermissionDenied
        opts = self.model._meta
        app_label = opts.app_label
        
        compras = Compra.objects.all().order_by("-fecha_pedido").filter(abono = False).filter(status = "A")
        ciudad = Ciudad.objects.all().distinct()
        
        for i in ciudad:
            city_str = str(i.nombre)
            total = 0
            total_usd = 0
            for j in compras:
                lugar_str = str(j.direccion_entrega.ciudad)
                if lugar_str == city_str:
                    total += j.total
                    tipo_cambio = float(get_tipo_cambio())
                    total_usd = round(total/tipo_cambio, 2)
                else:
                    pass
            lista.append(total)
            lista_usd.append(total_usd)
            lista_ciudad.append(i.nombre)
            
        try:
            cl = ChangeList(request, self.model, self.list_display, self.list_display_links, self.list_filter,
                self.date_hierarchy, self.search_fields, self.list_select_related, self.list_per_page, self.change_list_template, self)
            cl.formset = None   
        except IncorrectLookupParameters:
            if ERROR_FLAG in request.GET.keys():
                return render_to_response('admin/invalid_setup.html', {'title': _('Database error')})
            return HttpResponseRedirect(request.path + '?' + ERROR_FLAG + '=1')
        
        context = { 
            'title': 'Administracion de Totales por Tienda',
            'is_popup': cl.is_popup,
            'cl': cl,
            'has_add_permission': self.has_add_permission(request),
            'root_path': self.admin_site.root_path,
            'app_label': app_label,
            'compra':compras,
            'total':lista,
            'city':lista_ciudad,
            'cambio':lista_usd,
            
        }
        context.update(extra_context or {})
        return render_to_response(self.change_list_template, context)
    
admin.site.register(NoticeType, NoticeTypeAdmin)
admin.site.register(NoticeSetting, NoticeSettingAdmin)
admin.site.register(Notice, NoticeAdmin)
admin.site.register(ObservedItem)
admin.site.register(Compra,CompraAdmin)
#admin.site.add_actions(dinero_en_cuenta)
