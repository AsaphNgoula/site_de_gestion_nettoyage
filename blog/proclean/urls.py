from django.urls import path
from .views import home, send_message, confirmation, contact, galerie,recrutement, recrutement_confirmation, gestion_candidatures

app_name = 'proclean'

urlpatterns = [
    path('', home, name='home'),
    path('send-message/', send_message, name='send_message'),
    path('confirmation/', confirmation, name='confirmation'),
    path('contact/', contact, name='contact'),
    path('galerie/', galerie, name='galerie'),
    path('recrutement/', recrutement, name='recrutement'),
    path('recrutement/confirmation/', recrutement_confirmation, name='recrutement_confirmation'),
    path('admin/candidatures/', gestion_candidatures, name='gestion_candidatures'),
]
