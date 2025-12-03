from django.urls import path
from .views import home

app_name = 'proclean'

urlpatterns = [
   path('',home,name='home'),
]
