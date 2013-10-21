'''
Created on 27/04/2010

@author: mauricio
'''
from projectcapriccio.admin.conex import conecta
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django import http
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
import base64
from django.contrib.auth.decorators import login_required

@login_required
def admin_correos(request):
    t = get_template('../templates/correos/correos.html')
    lista = conecta()
    session,server = lista.coneccion()
    a = lista.obtener_mailboxes(server,session)
    html = t.render(Context({'list':a}))
    return HttpResponse(html)

def creacion_mailbox_email(request):
    mail = ""
    if request.method == "POST":
        if "correoBoxes" in request.POST:
            mail = request.POST["correoBoxes"]
            lista = conecta()
            session, server = lista.coneccion()
            try:
                lista.crear_mailbox_email_address(mail,server,session)
                return HttpResponse("Correo Creado cambie ahora su contrasena")
            except:
                return HttpResponse("Imposible crear este correo intente con otro nombre")
            
def cambiar_contrasena(request):
    mailbx = ""
    password = ""
    if request.method == "POST":
        if "mailbox" in request.POST and "passwd" in request.POST:
            mailbx = request.POST["mailbox"]
            password = base64.encodestring(request.POST["passwd"])
            lista = conecta()
            session, server = lista.coneccion()
            try:
                lista.cambiar_contrasena_mailbox(mailbx,server,session,password)
                return HttpResponse("OK!")
            except:
                return HttpResponse("Vuelva a intentarlo")
            
def eliminar_mailbx_email(request):
    mailbx = ""
    if request.method == "POST":
        if "mbx" in request.POST:
            mailbx = request.POST["mbx"]
            lista = conecta()
            session, server = lista.coneccion()
            try:
                lista.eliminar_mailbox_email_address(mailbx,server,session)
                return HttpResponse("OK!")
            except:
                return HttpResponse("No se pudo eliminar esta cuenta")


            
