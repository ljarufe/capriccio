# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
import datetime

def vista_uno(request):
	a = str(datetime.datetime.now())
	return render_to_response('index.html',{'hora':a})

def toGoogle(request):
	return HttpResponseRedirect("http://www.google.com")

