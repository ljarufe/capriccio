# -*- coding: utf-8 -*-

'''
@author: lucho
'''

from django.db import models
from projectcapriccio.common.models import Direccion, Usuario

class Cliente(Usuario):
    """
    Usuario con permisos para usar el carrito de compras
    """
    nombres = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=30)
    direccion = models.OneToOneField(Direccion)
    telefono = models.CharField(max_length=15, verbose_name='teléfono')
    dni = models.CharField(max_length=8, verbose_name='DNI')
    email = models.EmailField(verbose_name='e-mail')
    clave_activacion = models.CharField(max_length=40)
    
    def __unicode__(self):
        return '%s %s' % (self.nombres, self.apellidos)
    
    class Meta:
        permissions = (("puede_comprar", "Puede realizar compras"),)
