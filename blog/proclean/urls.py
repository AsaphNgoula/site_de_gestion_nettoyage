from django.urls import path
from .views import home, send_message, confirmation, contact, galerie

app_name = 'proclean'

urlpatterns = [
    path('', home, name='home'),
    path('send-message/', send_message, name='send_message'),
    path('confirmation/', confirmation, name='confirmation'),
    path('contact/', contact, name='contact'),
    path('galerie/', galerie, name='galerie')
]
