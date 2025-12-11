# blog/proclean/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CarouselImage, ServiceCard, ContactMessage
from django.core.mail import send_mail
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

def home(request):
    carousel_images = CarouselImage.objects.filter(is_active=True).order_by('id')
    services = ServiceCard.objects.filter(is_active=True).order_by('order')
    
    return render(request, 'accueil.html', {
        'carousel_images': carousel_images,
        'services': services,
    })

def send_message(request):
    if request.method != 'POST':
        return redirect('proclean:home')

    prenom = request.POST.get('prenom', '').strip()
    nom = request.POST.get('nom', '').strip()
    email = request.POST.get('email', '').strip()
    telephone = request.POST.get('telephone', '').strip()
    message_text = request.POST.get('message', '').strip()

    if not prenom or not nom or not email or not message_text:
        messages.error(request, 'Veuillez remplir tous les champs obligatoires.')
        return redirect('proclean:home')

    # Sauvegarde du message
    ContactMessage.objects.create(
        prenom=prenom,
        nom=nom,
        email=email,
        telephone=telephone,
        message=message_text
    )

    # Envoi email
    subject = f"Nouveau message de {prenom} {nom} - NG Conciergerie"
    body = f"""
Nom : {nom}
Prénom : {prenom}
Email : {email}
Téléphone : {telephone if telephone else 'Non spécifié'}

Message : 
{message_text}
"""

    try:
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,   # FROM - Utilise DEFAULT_FROM_EMAIL
            [settings.EMAIL_HOST_USER],    # TO (ton email)
            fail_silently=False
        )
        messages.success(request, "Votre message a bien été envoyé !")
    except Exception as e:
        # Ne pas bloquer le processus si l'email échoue
        messages.warning(request, "Message enregistré, mais l'email n'a pas pu être envoyé.")
        logger.error(f"ERREUR EMAIL: {e}")

    # Stocker les données pour la page confirmation
    request.session['contact_prenom'] = prenom
    request.session['contact_email'] = email
    request.session['contact_nom'] = nom
    
    # Important: Sauvegarder explicitement la session
    request.session.modified = True

    return redirect('proclean:confirmation')

def confirmation(request):
    # Récupérer les données de la session sans les supprimer immédiatement
    prenom = request.session.get('contact_prenom', '')
    email = request.session.get('contact_email', '')
    nom = request.session.get('contact_nom', '')

    # Vérifier si les données existent
    if not prenom or not email:
        messages.warning(request, "Aucun message n'a été envoyé récemment.")
        return redirect('proclean:home')

    # Préparer le contexte
    context = {
        'prenom': prenom,
        'nom': nom,
        'email': email,
    }

    # Nettoyer la session APRÈS avoir préparé le contexte
    # pour éviter les problèmes de rechargement
    if 'contact_prenom' in request.session:
        del request.session['contact_prenom']
    if 'contact_email' in request.session:
        del request.session['contact_email'] 
    if 'contact_nom' in request.session:
        del request.session['contact_nom']
    
    request.session.modified = True

    return render(request, 'confirmation.html', context)

# Supprimez cette fonction create_view qui n'est pas utilisée
# def create_view(request):
#     ...