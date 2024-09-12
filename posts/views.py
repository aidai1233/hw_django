from django.shortcuts import render
from django.http import HttpResponse


def text_view(request):
    return HttpResponse("Привет")


def html_view(request):
    return render(request, 'base.html')
# Create your views here.
