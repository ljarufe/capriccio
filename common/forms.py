# -*- coding: utf-8 -*-
'''
@author: lucho
'''

from django import forms
from django.forms import ModelForm
from projectcapriccio.common.models import Direccion, Imagen,Torta_Personalizada
from projectcapriccio.paginas.models import markitup 


class DireccionForm(ModelForm):
    class Meta:
        model = Direccion
        fields = ('lugar', 'ciudad',)


class ImagenForm(ModelForm):
    class Meta:
        model = Imagen
        fields = ('imagen',)

class PersonalizadaForm(ModelForm):
    descripcion = forms.CharField(widget = markitup())
    
    class Meta:
        model = Torta_Personalizada
        
class ContactPersonalizada(forms.Form):
    person = forms.CharField(label='Nombre :',max_length=120,required=True)
    email = forms.EmailField(label='E-mail :',max_length=180,required=True)
    subject = forms.CharField(label='Asunto :',max_length=120,required=True)
    comment =forms.CharField(label='Mensaje :',required=True,widget=forms.Textarea)
    image = forms.ImageField(label='Imagen :',required=False)
    phone = forms.CharField(label=u'Teléfono :',max_length=12,required=True)

class ContactInstitucional(forms.Form):
    person = forms.CharField(label='Nombre :',max_length=120,required=True)
    email = forms.EmailField(label='E-mail :',max_length=180,required=True)
    subject = forms.CharField(label='Asunto :',max_length=120,required=True)
    comment =forms.CharField(label='Mensaje :',required=True,widget=forms.Textarea)
    phone = forms.CharField(label=u'Teléfono :',max_length=12,required=True)