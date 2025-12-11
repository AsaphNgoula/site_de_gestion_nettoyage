# blog/proclean/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CarouselImage, ServiceCard, ContactMessage
from django.core.mail import EmailMultiAlternatives, send_mail  # AJOUTEZ send_mail ici
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging
from django.conf import settings
from django.urls import reverse

logger = logging.getLogger(__name__)

def home(request):
    carousel_images = CarouselImage.objects.filter(is_active=True).order_by('id')
    services = ServiceCard.objects.filter(is_active=True).order_by('order')
    
    return render(request, 'accueil.html', {
        'carousel_images': carousel_images,
        'services': services,
    })
# envoie de message
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
    contact_msg = ContactMessage.objects.create(
        prenom=prenom,
        nom=nom,
        email=email,
        telephone=telephone,
        message=message_text
    )

    # Préparation des données pour l'email HTML
    context = {
        'prenom': prenom,
        'nom': nom,
        'nom_complet': f"{prenom} {nom}",
        'email': email,
        'telephone': telephone if telephone else "Non spécifié",
        'message': message_text,
        'date_envoi': contact_msg.date_envoi.strftime("%d/%m/%Y à %H:%M"),
        'id': contact_msg.id,
        'site_url': request.build_absolute_uri('/')[:-1],
        'admin_url': request.build_absolute_uri(
            reverse('admin:proclean_contactmessage_changelist')
        ),
    }

    try:
        # ESSAYEZ CE CHEMIN (modifiez si nécessaire)
        html_content = render_to_string('emails/to_admin.html', context)
        
        plain_text = strip_tags(html_content)
        
        # Création de l'email avec HTML
        email_msg = EmailMultiAlternatives(
            subject=f"📬 Nouveau message de {prenom} {nom} - NG Conciergerie",
            body=plain_text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.EMAIL_HOST_USER],
            reply_to=[email],
        )
        
        # Ajout de la version HTML
        email_msg.attach_alternative(html_content, "text/html")
        
        # Envoi
        email_msg.send()
        
        messages.success(request, "Votre message a bien été envoyé !")
        
    except Exception as e:
        # Debug : affichez l'erreur exacte
        print(f"ERREUR DETAIL : {e}")
        logger.error(f"ERREUR EMAIL: {e}")
        
        # Envoyez un email texte simple en fallback
        try:
            subject = f"Nouveau message de {prenom} {nom} - NG Conciergerie"
            body = f"""
            Nom : {nom}
            Prénom : {prenom}
            Email : {email}
            Téléphone : {telephone if telephone else 'Non spécifié'}
            
            Message : 
            {message_text}
            """
            
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [settings.EMAIL_HOST_USER],
                fail_silently=False
            )
            messages.success(request, "Votre message a bien été envoyé !")
        except Exception as e2:
            messages.warning(request, "Message enregistré, mais l'email n'a pas pu être envoyé.")
            logger.error(f"ERREUR EMAIL FALLBACK: {e2}")

    # Stocker les données pour la page confirmation
    request.session['contact_prenom'] = prenom
    request.session['contact_email'] = email
    request.session['contact_nom'] = nom
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
    if 'contact_prenom' in request.session:
        del request.session['contact_prenom']
    if 'contact_email' in request.session:
        del request.session['contact_email'] 
    if 'contact_nom' in request.session:
        del request.session['contact_nom']
    
    request.session.modified = True

    return render(request, 'confirmation.html', context)



def contact(request):
    return render(request, 'contact.html')
