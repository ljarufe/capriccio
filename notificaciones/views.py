# Create your views here.
from projectcapriccio.notification import models as nt
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.syndication.views import feed

from projectcapriccio.notification.models import *
from projectcapriccio.notification.decorators import basic_auth_required, simple_basic_auth_callback
from projectcapriccio.notification.feeds import NoticeUserFeed
import datetime
from django.contrib.auth.models import User
from django.utils import simplejson

@login_required
def nuevasNotificaciones(request):
    user = "" #variable para almacenar datos de usuario
    notified = "" #variable para almacenar datos de notice
    if request.user:
        user = User.objects.get(username = request.user)
        notified = Notice.objects.filter(user = user)
        return render_to_response("notificaciones.html",{"user":user,"notificaciones":notified})

@login_required         
def generadorStreaming(request):
    accion = ""
    accion = request.GET["action"]
    notified = ""
    contador = 0
    options = ""
    a = 0
    try:
        user = User.objects.get(username = request.user)
        notified = Notice.objects.filter(user = user).filter(unseen=1).order_by("-id")
        contador = notified.count()
        for i in notified:
            a = a + 1
            options += "<div style='margin:0 auto;'><a href='/notice%s' style='color:#000;' title='Click para ver el detalle de la notificacion'>%s | %s</a></div><div><img src='/media/img/24-book-green-mark.png' idb='%s' class='seen' border='0' style='cursor:pointer;' title='Click para archivar Ocurrencia' target='_blank'/>%s</div><hr style='background-color:#4d4d4d;'>" % (i.id,a,i.message,i.id,i.added) 
    except:
        notified = "Registrese o Acceda a su cuenta"
    dir = {'notif':options,'cuenta':contador,'user':user.username}
    return HttpResponse(simplejson.dumps(dir))

@login_required
def cambiar_estado(request):
    id = ""
    respuesta = ""
    if request.method == "POST":
        if "identificador" in request.POST:
            id = request.POST["identificador"]
            notified = Notice.objects.get(pk=id)
            notified.unseen = 0
            notified.archived = 1
            notified.save()
            respuesta = "Ok!"
    return HttpResponse(respuesta)
