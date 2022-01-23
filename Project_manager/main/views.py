from django.http import HttpResponseRedirect
from django.shortcuts import render

def empty(request):
    return HttpResponseRedirect("/index/")

def index(request):
    return render(request, 'main/index.html')
