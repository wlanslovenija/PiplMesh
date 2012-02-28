# Create your views here.

from django.template import RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response

def first(request):
    d = {}
    d['search_engine'] = 'Google'
    d['search_engine_logo'] = d['search_engine'].lower() + '_logo.png'
    return render_to_response('home.html', d, context_instance=RequestContext(request))