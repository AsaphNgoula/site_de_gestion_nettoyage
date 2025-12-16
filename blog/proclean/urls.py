from django.urls import path
from .views import home, send_message, confirmation, contact, galerie,recrutement, recrutement_confirmation, gestion_candidatures,service_detail

app_name = 'proclean'

urlpatterns = [
    path('', home, name='home'),
    path('send-message/', send_message, name='send_message'),
    path('confirmation/', confirmation, name='confirmation'),
    path('contact/', contact, name='contact'),
    path('galerie/', galerie, name='galerie'),
     path('service/<str:service_slug>/', service_detail, name='service_detail'),
    path('recrutement/', recrutement, name='recrutement'),
    path('recrutement/confirmation/', recrutement_confirmation, name='recrutement_confirmation'),
    path('admin/candidatures/', gestion_candidatures, name='gestion_candidatures'),
]
