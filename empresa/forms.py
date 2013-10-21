'''
Created on 08/06/2010

@author: mauricio
'''
from django.template.loader import render_to_string
from django import form
import django.forms as forms
from projectcapriccio.empresa.models import Tienda

class select_popup(forms.Select):
    def render(self,name,*args,**kwargs):
        html = super(select_popup,self).render(name,*args,**kwargs)
        popup = render_to_string("ubicacion.html",{"field":name})
        return html + popup
        
class formulario_tienda(forms.ModelForm):
    
    class Meta:
        models = Tienda
        fields = ["nombre_corto","direccion","telefono","productos"]

