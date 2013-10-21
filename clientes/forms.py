# -*- coding: utf-8 -*-

'''
@author: lucho
'''

from django import forms
from projectcapriccio.clientes.models import Cliente
from django.contrib.localflavor.pe.forms import PEDNIField
import re


class ClienteForm(forms.ModelForm):
    dni = PEDNIField()
    class Meta:
        model = Cliente
        fields = ('nombres', 'apellidos', 'email', 'dni','telefono')

# TODO: Si fuera necesario hacer una comprobación de los nombres y apellidos        
    def clean_nombres(self):
        data = self.cleaned_data['nombres']
        if not re.match(u"[a-zA-Z\á\é\í\ó\ú\ñ]+[\s]?[a-zA-Z\á\é\í\ó\ú\ñ]*[\s]*$", data):
            raise forms.ValidationError('Su nombre contiene caracteres no permitidos')
        return data
        
    def clean_apellidos(self):
        data = self.cleaned_data['apellidos']
        if not re.match(u"[a-zA-Z\á\é\í\ó\ú\ñ]+[\s]?[a-zA-Z\á\é\í\ó\ú\ñ]*[\s]*$", data):
            raise forms.ValidationError('Su apellido contiene caracteres no permitidos')
        return data
