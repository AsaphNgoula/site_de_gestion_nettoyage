from django.shortcuts import render
from .models import Service




def index(request):
    return render(request, 'index.html')
