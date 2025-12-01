from django.urls import path
from .views import index


app_name = 'proclean'

urlpatterns = [
   path('', index, name='index'),
]
