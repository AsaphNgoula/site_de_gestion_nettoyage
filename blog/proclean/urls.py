from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import home,send_message,confirmation, contact,nettoyage_airbnb_detail,nettoyage_tapis_detail, nettoyage_commercial_detail, nettoyage_industriel_detail, galerie,recrutement,nettoyage_profondeur_detail,nettoyage_regulier_detail, recrutement_confirmation,admin_logout, gestion_candidatures,service_detail,about,dashboard,admin_login

app_name = 'proclean'

urlpatterns = [
    path('', home, name='home'),
    path('send-message/', send_message, name='send_message'),
    path('confirmation/', confirmation, name='confirmation'),
    path('contact/', contact, name='contact'),
    path('a-propos/', about, name='about'),
    path('galerie/', galerie, name='galerie'),
    path('service/<str:service_slug>/', service_detail, name='service_detail'),
    path('recrutement/', recrutement, name='recrutement'),
    path('recrutement/confirmation/', recrutement_confirmation, name='recrutement_confirmation'),
    path('admin/candidatures/', gestion_candidatures, name='gestion_candidatures'),
    path('dashboard/',dashboard, name='dashboard'),
    path('admin-login/', admin_login, name='admin_login'),
    path('logout/', admin_logout, name='admin_logout'),
    path('services/nettoyage-profond/', nettoyage_profondeur_detail, name='nettoyage_profond'),
    path('services/nettoyage-regulier/', nettoyage_regulier_detail, name='nettoyage_regulier'),
    path('services/nettoyage-industriel/', nettoyage_industriel_detail, name='nettoyage_industriel'),
    path('services/nettoyage-airbnb/', nettoyage_airbnb_detail, name='nettoyage_airbnb'),
    path('services/nettoyage-commercial/', nettoyage_commercial_detail, name='nettoyage_commercial'),
    path('services/nettoyage-tapis/', nettoyage_tapis_detail, name='nettoyage_tapis'),
]
