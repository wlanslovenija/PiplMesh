# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response

def first(request):
    return render_to_response('base.html', {'title': 'PiplMesh'})