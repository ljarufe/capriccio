# -*- coding: utf-8 -*-

'''
@author: lucho
'''

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from projectcapriccio.clientes.forms import ClienteForm
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMultiAlternatives
from django.db.models import Max
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.core.mail import EmailMessage, BadHeaderError
from django.core.exceptions import ObjectDoesNotExist
from projectcapriccio.common.views import get_cliente, makePassword
# librerias de python
import sha
import random
# forms
#from forms import ClienteForm
from projectcapriccio.common.forms import DireccionForm
# models
from projectcapriccio.clientes.models import Cliente
from projectcapriccio.common.models import Ciudad, Direccion

@csrf_exempt
def registro_cliente(request):
    """
    Despliegue y tratamiento de formularios para nuevos usuarios, los usuarios 
    se activarán por medio de la verificación por email
    """
    if request.method == 'POST':
        cliente_form = ClienteForm(request.POST)
        direccion_form = DireccionForm(request.POST)
        
        if cliente_form.is_valid() and direccion_form.is_valid():
            direccion = direccion_form.save()
            cliente = cliente_form.save(commit=False)
            cliente.direccion = direccion
            password = request.POST['password2']
            user = User.objects.create_user(cliente.email,
                                            cliente.email, 
                                            password)
            user.is_active = False
            try:
                subject = 'Confirma tu registro en el Capriccio'
                
                # Crea una clave de activación aleatoria en base al dni
                salt = sha.new(str(random.random())).hexdigest()[:5]
                clave = sha.new(str(cliente.dni)+salt).hexdigest()
                cliente.clave_activacion = clave
                
                # TODO: colocar el dominio original en el link en el archivo html
                email_content = open('%shtml/email_verificacion.html' % \
                					 settings.MEDIA_ROOT)
                # Problemas con los nombres con tildes
                # nombre = cliente.nombres + cliente.apellidos
                html_content = email_content.read() % clave
                email_content.close()
                msg = EmailMessage(subject, html_content, 
                                   'Tienda en Linea <systems@capriccioperu.com>', [cliente.email])
                msg.content_subtype = "html"
                msg.send()
                
            except BadHeaderError:
                return HttpResponse('Se encontró una cabecera de e-mail inválida')
            
            cliente.user = user
            cliente.user.save()
            cliente.save()

            return render_to_response('clientes/confirmacion.html',
                                      {'titulo': 'Confirmación'},
                                      context_instance=RequestContext(request))
    else:
        cliente_form = ClienteForm()
        direccion_form = DireccionForm()
       
    return render_to_response('clientes/registro.html',
                              {'cliente_form': cliente_form,
                               'direccion_form': direccion_form,
                               'titulo': 'Registro',
                               'usuario': get_cliente(request)},
                              context_instance=RequestContext(request))

def registro_acceso_compra(request):
    resultado = ""
    if request.method == 'POST':
        ciudad = Ciudad.objects.get(pk=request.POST['ciudad'])
        direccion = Direccion(
            lugar = request.POST['lugar'],
            ciudad = ciudad
        )
        direccion.save()
        user = User.objects.create_user(
            request.POST['email'],
            request.POST['email'],
            request.POST['password2']
        )
        user.is_active = False
        user.save()
        cliente = Cliente(
            user = user,
            nombres = request.POST['nombres'],
            apellidos = request.POST['apellidos'],
            direccion = direccion,
            email = request.POST['email'],
            dni = request.POST['dni'],
            telefono = request.POST['telefono']
        )
        cliente.save()
                
        try:
            salt = sha.new(str(random.random())).hexdigest()[:5]
            clave = sha.new(str(cliente.dni)+salt).hexdigest()
            cliente.clave_activacion = clave
            cliente.user.is_active = True
            cliente.user.save()
            cliente.save()
            try:
                asunto = "Capriccio - Tienda On Line"
                texto = "Este es un mensaje enviado por Capriccio"
                html = "<div style='color:#355074'><h1>Gracias por comunicarse con nosotros y haberse registrado %s.</h1><p>En breves momentos un miembro de nuestro staff se comunicar&aacute; contigo</p><p>Este es tu usuario : %s.</p><p>Esta es tu contrase&ntilde;a : %s.</p><p>Cordialmente,</p><img src='http://capriccioperu.com/media/img/tienda_en_linea.png' alt='Logo Tiena On Line Capriccio'/></div>" % (cliente.nombres,cliente.email,request.POST['password2'])
                msg = EmailMultiAlternatives(asunto,texto,"Tienda en Linea <systems@capriccioperu.com>",[cliente.email])
                msg.attach_alternative(html,"text/html")
                msg.send()
            except:
                pass
            resultado = u'<p >Utiliza el formulario para seguir con el proceso de compra</p>'
        except:
            pass

    return HttpResponse(resultado)

def usuario_unico_json(request, email):
	"""
	Verifica que el e-mail ingresado en el registro	sea único, el cual es usado
	como username
	"""
	try:
		cliente = Cliente.objects.get(email=email)
	except Cliente.DoesNotExist:
		respuesta = False
	else:
		respuesta = True
		
	return HttpResponse(simplejson.dumps(respuesta), 
						mimetype='application/json')
		

def verificar_cliente(request, clave):
    """
    Coloca el estado del usuario como activo al acceder este a su correo y 
    confirmar a travéz del link su cuenta
    """
    cliente = get_object_or_404(Cliente, clave_activacion=clave)
    cliente.user.is_active = True
    cliente.user.save()
    return HttpResponseRedirect(reverse('inicio'))



@login_required
def cerrar_sesion(request):
    """
    logout de cliente
    """
    logout(request)
    return HttpResponseRedirect(reverse('inicio'))


@login_required
@csrf_exempt
def opciones_usuario(request):
    """
    Opciones del cliente, cambio de perfil
    """
    cliente = Cliente.objects.get(user=request.user.id)  
        
    if request.method == 'POST':
        cliente_form = ClienteForm(request.POST, instance=cliente)
        direccion_form = DireccionForm(request.POST, instance=cliente.direccion)
        
    	if cliente_form.is_valid() and direccion_form.is_valid():
            direccion = direccion_form.save()
            cliente = cliente_form.save(commit=False)
            cliente.direccion = direccion
            cliente.save()
            
    cliente_form = ClienteForm(instance=cliente)
    direccion_form = DireccionForm(instance=cliente.direccion)
    
    return render_to_response('clientes/opciones.html',
                              {'cliente_form': cliente_form,
                               'direccion_form': direccion_form,
                              'titulo': 'Opciones'},
                              context_instance=RequestContext(request))


@login_required
def verificar_password_json(request, password):
	"""
	Verifica que el password del cliente sea el correcto
	"""	
	respuesta = request.user.check_password(password)
	return HttpResponse(simplejson.dumps(respuesta), 
						mimetype='application/json')
						

@login_required
def cambiar_password_json(request, password):
	"""
	Cambiar el password del cliente
	"""
	# TODO: Hacer la comprobación del password mediante una 
	# expresion regular y devolver la respuesta
	# if password match("[/w]+"):
	#   respuesta = True
	# else:
	#   respuesta = False
	request.user.set_password(password)
	request.user.save()
	respuesta = True
	return HttpResponse(simplejson.dumps(respuesta), 
						mimetype='application/json')


@login_required
@csrf_exempt
def eliminar_cliente(request, clave=None):
    """
    Dar de baja a un usuario y eliminar un cliente
    """
    # Enviar el e-mail de confirmación
    if request.method == 'POST':
        cliente = Cliente.objects.get(user=request.user.id)
        clave = cliente.clave_activacion
        email_content = open('%shtml/email_borrar_cuenta.html' % \
        					 settings.MEDIA_ROOT)
        html_content = email_content.read() % clave
        email_content.close()
        subject = "Confirma la eliminación de tu cuenta"
        msg = EmailMessage(subject, html_content, 
                           'systems@capriccioperu.com', [cliente.email])
        msg.content_subtype = "html"
        msg.send()
        return render_to_response('clientes/confirmacion.html',
                                  {'titulo': 'Confirmación'},
                                  context_instance=RequestContext(request))
	
	# Logout del cliente y posterior borrado
	logout(request)
    cliente = get_object_or_404(Cliente, clave_activacion=clave)
    cliente.user.delete()
    cliente.delete()

    return HttpResponseRedirect(reverse('inicio'))


@csrf_exempt
def recuperar_password(request, clave=None, password=None):
	"""
	Recuperar una cuenta mediante el envío de un nuevo password
	"""
	datos_incorrectos = False
	
	# Enviar un e-mail con una nueva contraseña - aún no se cambia
	if request.method == 'POST':
		try:
			cliente = Cliente.objects.get(user__username=request.POST['email'])
		
			if cliente.telefono == request.POST['telefono'] and \
			   cliente.dni == request.POST['dni']:
				clave = cliente.clave_activacion
				password = makePassword(6)
				email_content = open('%shtml/email_recuperar_password.html' % 
									 settings.MEDIA_ROOT)
				html_content = email_content.read() % (password, clave, password)
				email_content.close()
				subject = "Confirma tu cambio de contraseña"
				msg = EmailMessage(subject, html_content, 
								   'systems@capriccioperu.com', [cliente.email])
				msg.content_subtype = "html"
				msg.send()
		
				return render_to_response('clientes/confirmacion.html',
										  {'titulo': 'Confirmación'},
										  context_instance=RequestContext(request))
			else:
				datos_incorrectos = True
		except ObjectDoesNotExist:
			datos_incorrectos = True
		
	
	# Cambiar la contraseña al confirmar el e-mail
	if clave and password:
		cliente = Cliente.objects.get(clave_activacion=clave)
		cliente.user.set_password(password)
		cliente.user.save()
		return HttpResponseRedirect(reverse('inicio'))
		
	# Mostrar el formulario de solicitud
	return render_to_response('clientes/recuperar.html',
							  {'datos_incorrectos': datos_incorrectos,
							   'titulo': 'Recuperar Contraseña'},
							   context_instance=RequestContext(request)) 
