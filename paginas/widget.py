'''
Created on 24/03/2010

@author: mauricio
'''

from django import forms
from django.db import models
from django.conf import settings
from django.db.models.fields import CharField
from django.forms.widgets import Input

class locationPicker(Input):
    class Media:
        
        js = (
              'http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js',
              'http://www.google.com/jsapi?key=' + settings.MAPS_API_KEY,
              '/media/js/jquery.location_picker.js',
              )
        css = {
               'screen':(
                      '/media/css/location_picker.css',
                      )
               }
        
    def __init__(self,language = None, attrs = None):
        self.language = language or settings.LANGUAGE_CODE[:2]
        super(locationPicker,self).__init__(attrs = attrs)
        
    def render(self,name,value,attrs = None):
        if None == attrs:
            attrs = {}
        attrs['class'] = 'location_picker'
        return super(locationPicker,self).render(name,value,attrs)
    
class locationField(CharField):
    
    def formField(self,**kwargs):
        kwargs['widget'] = locationPicker
        return super(locationField,self).formField(**kwargs)
     