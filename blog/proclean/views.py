# blog/proclean/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CarouselImage, ContactMessage, JobApplication
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.files.storage import default_storage
import os
from django.core.mail import EmailMultiAlternatives, send_mail  # AJOUTEZ send_mail ici
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging
from django.conf import settings
from django.urls import reverse
from .forms import JobApplicationForm 


logger = logging.getLogger(__name__)

def home(request):
    carousel_images = CarouselImage.objects.filter(is_active=True).order_by('id')
    
    # Liste statique des services (remplace par tes données)
    services = [
        {
            'title': 'Nettoyage Régulier',
            'description': 'Un nettoyage complet et régulier pour maintenir votre espace toujours propre et accueillant.',
            'image': None,  # Tu peux ajouter des images statiques
            'button_text': 'En savoir plus'
        },
        {
            'title': 'Nettoyage en Profondeur',
            'description': 'Un nettoyage intensif qui atteint les moindres recoins.',
            'image': None,
            'button_text': 'En savoir plus'
        },
        # ... ajoute les 4 autres services
    ]
    
    return render(request, 'accueil.html', {
        'carousel_images': carousel_images,
        'services': services,  # AJOUTE CETTE LIGNE
    })
# envoie de message
def send_message(request):
    if request.method != 'POST':
        return redirect('proclean:home')

    prenom = request.POST.get('prenom', '').strip()
    nom = request.POST.get('nom', '').strip()
    email = request.POST.get('email', '').strip()  # Email de l'utilisateur
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

    try:
        print(f"=== ENVOI MESSAGE ===")
        print(f"De: {email} (utilisateur)")
        print(f"À: {settings.EMAIL_HOST_USER} (admin)")
        print(f"Depuis: {settings.DEFAULT_FROM_EMAIL} (votre compte Gmail)")
        
        # ========== 1. EMAIL SIMPLE À L'ADMIN ==========
        subject = f"📬 Message de {prenom} {nom}"
        
        body = f"""
        ====================================
        NOUVEAU MESSAGE DE CONTACT
        ====================================
        
        👤 INFORMATIONS :
        • Nom : {nom}
        • Prénom : {prenom}
        • Email : {email}
        • Téléphone : {telephone if telephone else 'Non fourni'}
        • Date : {contact_msg.date_envoi.strftime('%d/%m/%Y %H:%M')}
        
        📝 MESSAGE :
        {message_text}
        
        🔗 ADMINISTRATION :
        {request.build_absolute_uri(reverse('admin:proclean_contactmessage_change', args=[contact_msg.id]))}
        """
        
        # ENVOI SIMPLE avec send_mail (comme votre fonction qui fonctionne)
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,  # asaphngoula237@gmail.com
            [settings.EMAIL_HOST_USER],   # asaphngoula237@gmail.com (MÊME ADRESSE !)
            fail_silently=False,
        )
        print(f"✅ Message envoyé à l'admin")
        
        # ========== 2. CONFIRMATION À L'UTILISATEUR ==========
        confirmation_body = f"""
        Bonjour {prenom},
        
        Nous avons bien reçu votre message et vous en remercions.
        
        Notre équipe vous répondra dans les plus brefs délais.
        
        Cordialement,
        NG Conciergerie
        """
        
        send_mail(
            "✅ Confirmation de votre message - NG Conciergerie",
            confirmation_body,
            settings.DEFAULT_FROM_EMAIL,
            [email],  # À l'utilisateur
            fail_silently=False,
        )
        print(f"✅ Confirmation envoyée à {email}")
        
        messages.success(request, "Votre message a bien été envoyé !")
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        
        # Fallback ULTRA simple
        try:
            print("🔄 Tentative fallback...")
            send_mail(
                "Message de contact",
                f"Message de {prenom} {nom}",
                settings.DEFAULT_FROM_EMAIL,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            print("✅ Fallback réussi")
            messages.success(request, "Votre message a bien été envoyé !")
        except Exception as e2:
            print(f"❌ Fallback échoué: {e2}")
            messages.warning(request, "Message enregistré, mais problème d'email.")

    # Stocker en session
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

    return render(request, 'recrutement_confirmation.html', context)



def contact(request):
    return render(request, 'contact.html')


def galerie(request):
    """
    Vue pour afficher la page galerie
    """
    return render(request, 'galerie.html')



def recrutement(request):
    """Vue pour la page de recrutement"""
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                print("✅ Formulaire valide, sauvegarde...")
                
                # Sauvegarder la candidature
                application = form.save(commit=False)
                
                # Gérer les disponibilités
                application.disponibilites = form.cleaned_data['disponibilites']
                
                # Convertir les choix radio en booléens
                experience_menage = form.cleaned_data.get('experience_menage')
                vehicule = form.cleaned_data.get('vehicule')
                
                if experience_menage is not None:
                    application.experience_menage = (experience_menage == 'True')
                
                if vehicule is not None:
                    application.vehicule = (vehicule == 'True')
                
                # Sauvegarder
                application.save()
                print(f"✅ Candidature #{application.id} sauvegardée")
                print(f"   Nom: {application.prenom} {application.nom}")
                print(f"   Email: {application.email}")
                print(f"   CV: {application.cv}")
                
                # Envoyer les emails
                try:
                    send_application_emails(application, request)
                    messages.success(request, "Votre candidature a été envoyée avec succès !")
                except Exception as e:
                    print(f"⚠️ Email échoué mais candidature sauvegardée: {e}")
                    messages.warning(request, "Candidature enregistrée, vérifiez votre email pour la confirmation.")
                
                # Stocker en session pour la confirmation
                request.session['application_submitted'] = True
                request.session['candidate_name'] = f"{application.prenom} {application.nom}"
                request.session['candidate_email'] = application.email
                
                # Redirection vers la confirmation
                return redirect('proclean:recrutement_confirmation')
                
            except Exception as e:
                print(f"❌ Erreur lors de la sauvegarde: {e}")
                messages.error(request, "Une erreur est survenue. Veuillez réessayer.")
        else:
            print(f"❌ Formulaire invalide: {form.errors}")
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = JobApplicationForm()
    
    return render(request, 'recrutement.html', {'form': form})

def send_application_emails(application, request):
    """Envoyer les emails pour une candidature avec CV en pièce jointe"""
    try:
        print(f"=== DÉBUT ENVOI EMAIL CANDIDATURE ===")
        print(f"Email du candidat: {application.email}")
        print(f"Votre email (admin): {settings.EMAIL_HOST_USER}")
        
        # 1. Email à l'administrateur AVEC CV
        subject_admin = f"📄 NOUVELLE CANDIDATURE - {application.prenom} {application.nom}"
        
        body_admin = f"""
        NOUVELLE CANDIDATURE REÇUE !

        📋 INFORMATIONS DU CANDIDAT :
        ------------------------------
        • Nom complet : {application.prenom} {application.nom}
        • Email : {application.email}
        • Téléphone : {application.telephone}
        • Région souhaitée : {application.get_region_display_full()}
        • Disponibilités : {', '.join(application.disponibilites)}
        • Expérience ménage : {'✅ Oui' if application.experience_menage else '❌ Non'}
        • Véhicule personnel : {'✅ Oui' if application.vehicule else '❌ Non'}
        • Date de soumission : {application.date_soumission.strftime('%d/%m/%Y à %H:%M')}
        
        📝 MESSAGE :
        {application.message if application.message else 'Aucun message'}
        
        📎 CV : {application.cv.name if application.cv else 'Aucun CV téléchargé'}
        (Le CV est joint à cet email)
        
        🔗 Administration : {request.build_absolute_uri(reverse('admin:proclean_jobapplication_changelist'))}
        """
        
        # Créer l'email avec EmailMultiAlternatives pour pouvoir attacher le CV
        email_admin = EmailMultiAlternatives(
            subject=subject_admin,
            body=body_admin,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.EMAIL_HOST_USER],
            reply_to=[application.email],
        )
        
        # Attacher le CV si il existe
        if application.cv and application.cv.file:
            try:
                print(f"📎 Tentative d'attachement du CV: {application.cv.name}")
                
                # Ouvrir le fichier
                application.cv.file.open('rb')
                cv_content = application.cv.file.read()
                cv_filename = os.path.basename(application.cv.name)
                
                # Déterminer le type MIME
                if cv_filename.lower().endswith('.pdf'):
                    content_type = 'application/pdf'
                elif cv_filename.lower().endswith('.doc'):
                    content_type = 'application/msword'
                elif cv_filename.lower().endswith('.docx'):
                    content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                else:
                    content_type = 'application/octet-stream'
                
                # Attacher le fichier
                email_admin.attach(
                    filename=cv_filename,
                    content=cv_content,
                    mimetype=content_type
                )
                print(f"✅ CV attaché: {cv_filename}")
                
                # Fermer le fichier
                application.cv.file.close()
                
            except Exception as e:
                print(f"⚠️ Erreur lors de l'attachement du CV: {e}")
                body_admin += f"\n⚠️ ERREUR CV: Le CV n'a pas pu être attaché ({e})"
                email_admin = EmailMultiAlternatives(
                    subject=subject_admin + " [CV manquant]",
                    body=body_admin,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.EMAIL_HOST_USER],
                    reply_to=[application.email],
                )
        
        # Envoyer l'email admin
        email_admin.send()
        print(f"✅ Email admin envoyé à {settings.EMAIL_HOST_USER} avec CV")
        
        # 2. Email de confirmation au candidat (sans CV)
        subject_candidate = "🎉 Confirmation de votre candidature - NG Conciergerie"
        
        body_candidate = f"""
        Bonjour {application.prenom},

        Nous avons bien reçu votre candidature et nous vous en remercions !

        ✅ VOTRE CANDIDATURE EST CONFIRMÉE :
        ------------------------------------
        • Date : {application.date_soumission.strftime('%d/%m/%Y à %H:%M')}
        • Poste : Agent de nettoyage professionnel
        • Région : {application.get_region_display_full()}
        • Référence : CAND-{application.id:04d}

        ⏳ PROCHAINES ÉTAPES :
        ---------------------
        1. Notre équipe RH examinera votre profil sous 7 jours ouvrés
        2. Si votre profil correspond à nos besoins, nous vous contacterons
        3. Un entretien sera programmé selon vos disponibilités

        🔒 PROTECTION DES DONNÉES :
        --------------------------
        Vos données sont conservées pendant maximum 2 ans conformément au RGPD.

        📞 QUESTIONS ?
        contact@ngconciergerie.com

        Cordialement,
        L'équipe RH de NG Conciergerie
        """
        
        # Email simple au candidat
        send_mail(
            subject_candidate,
            body_candidate,
            settings.DEFAULT_FROM_EMAIL,
            [application.email],
            fail_silently=False,
        )
        print(f"✅ Email confirmation envoyé à {application.email}")
        
        print(f"=== EMAILS ENVOYÉS AVEC SUCCÈS ===")
        
    except Exception as e:
        print(f"❌ ERREUR CRITIQUE dans send_application_emails: {e}")
        import traceback
        traceback.print_exc()
        
        # Fallback sans CV
        try:
            print("🔄 Tentative de fallback sans CV...")
            subject = f"Candidature (sans CV) - {application.prenom} {application.nom}"
            body = f"""
            Candidature reçue (CV non attaché):
            
            Nom: {application.nom}
            Prénom: {application.prenom}
            Email: {application.email}
            CV fichier: {application.cv.name if application.cv else 'Aucun'}
            """
            
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [settings.EMAIL_HOST_USER],
                fail_silently=False
            )
            print("✅ Fallback sans CV réussi")
        except Exception as e2:
            print(f"❌ Fallback échoué aussi: {e2}")


def recrutement_confirmation(request):
    """Page de confirmation après soumission de candidature"""
    if not request.session.get('application_submitted', False):
        return redirect('proclean:recrutement')
    
    context = {
        'candidate_name': request.session.get('candidate_name', ''),
        'candidate_email': request.session.get('candidate_email', ''),
    }
    
    # Nettoyer la session
    for key in ['application_submitted', 'candidate_name', 'candidate_email']:
        if key in request.session:
            del request.session[key]
    request.session.modified = True
    
    return render(request, 'recrutement_confirmation.html', context)

def gestion_candidatures(request):
    """Vue admin simplifiée pour voir les candidatures"""
    if not request.user.is_staff:
        return redirect('proclean:home')
    
    candidatures = JobApplication.objects.all().order_by('-date_soumission')
    
    return render(request, 'admin/gestion_candidatures.html', {
        'candidatures': candidatures
    })


def service_detail(request, service_slug):
    """Vue pour afficher les détails d'un service spécifique"""
    services = {
        'nettoyage-regulier': {
            'title': 'Nettoyage Régulier',
            'description': '''
                Un nettoyage complet et régulier pour maintenir votre espace toujours propre et accueillant. 
                Idéal pour les maisons et appartements nécessitant un entretien hebdomadaire ou mensuel.
                
                Ce service comprend :
                • Nettoyage complet des sols
                • Dépoussiérage des surfaces
                • Nettoyage des sanitaires
                • Vidage des poubelles
                • Nettoyage des vitres intérieures
                
                Fréquences disponibles : Hebdomadaire, Bi-mensuelle, Mensuelle
            ''',
            'image': 'services/regular-cleaning.jpg',
            'price': 'À partir de 80$'
        },
        'nettoyage-profondeur': {
            'title': 'Nettoyage en Profondeur',
            'description': '''
                Un nettoyage intensif qui atteint les moindres recoins. Parfait pour le nettoyage 
                de printemps, après des travaux, ou pour une remise à neuf complète de votre espace.
                
                Ce service comprend :
                • Nettoyage derrière les appareils électroménagers
                • Décrasser les joints et recoins
                • Nettoyage des murs et plafonds
                • Dégreissage complet de la cuisine
                • Nettoyage approfondi des sanitaires
            ''',
            'image': 'services/deep-cleaning.jpg',
            'price': 'À partir de 150$'
        },
        'nettoyage-demenagement': {
            'title': 'Nettoyage Déménagement',
            'description': '''
                Service spécialisé pour les déménagements. Nous assurons le nettoyage complet 
                de votre ancien logement et préparons le nouveau pour votre arrivée.
                
                Ce service comprend :
                • Nettoyage complet avant départ
                • Nettoyage après travaux
                • Préparation du logement pour nouvel arrivant
                • Nettoyage des placards et armoires
                • Désinfection complète
            ''',
            'image': 'services/move-cleaning.jpg',
            'price': 'À partir de 200$'
        },
        'nettoyage-airbnb': {
            'title': 'Nettoyage Airbnb',
            'description': '''
                Service de nettoyage professionnel spécialement conçu pour les locations Airbnb. 
                Garantie d'une propreté impeccable entre chaque location.
                
                Ce service comprend :
                • Changement des draps et serviettes
                • Nettoyage rapide et efficace
                • Vérification des fournitures
                • Restockage des produits de base
                • Rapport de nettoyage
            ''',
            'image': 'services/airbnb-cleaning.jpg',
            'price': 'À partir de 100$ par nettoyage'
        },
        'nettoyage-tapis': {
            'title': 'Nettoyage de Tapis',
            'description': '''
                Service spécialisé de nettoyage de tapis avec équipement professionnel. 
                Élimination des taches, odeurs et allergènes.
                
                Ce service comprend :
                • Prétraitement des taches
                • Nettoyage à la vapeur professionnel
                • Désodorisation
                • Traitement anti-taches
                • Séchage rapide
            ''',
            'image': 'services/carpet-cleaning.jpg',
            'price': 'À partir de 50$ par pièce'
        },
        'nettoyage-commercial': {
            'title': 'Nettoyage Commercial',
            'description': '''
                Services de nettoyage professionnel pour bureaux, commerces et établissements. 
                Programmes flexibles adaptés aux horaires d'ouverture.
                
                Ce service comprend :
                • Nettoyage quotidien des bureaux
                • Entretien des espaces communs
                • Nettoyage des sanitaires professionnels
                • Gestion des déchets
                • Contrat personnalisé selon vos besoins
            ''',
            'image': 'services/commercial-cleaning.jpg',
            'price': 'Devis personnalisé selon superficie'
        }
    }
    
    service = services.get(service_slug)
    
    if not service:
        return redirect('proclean:home')
    
    return render(request, 'service_detail.html', {
        'service': service,
        'service_slug': service_slug
    })

def about(request):
    """
    Vue pour afficher la page À propos
    """
    return render(request, 'about.html')

@staff_member_required
def dashboard(request):
    total_candidatures = JobApplication.objects.count()
    total_messages = ContactMessage.objects.count()
    total_carousel = CarouselImage.objects.count()

    context = {
        'total_candidatures': total_candidatures,
        'total_messages': total_messages,
        'total_carousel': total_carousel,
    }
    return render(request, 'dashbord.html', context)

def admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect(reverse('proclean:dashboard'))  # redirige vers le dashboard admin si déjà connecté

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect(reverse('proclean:dashboard'))  # redirige vers le dashboard après login
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe invalide.")

    return render(request, "admin_login.html")

def admin_logout(request):
    logout(request)
    messages.success(request, "Vous êtes bien déconnecté.")
    return redirect('proclean:admin_login')


def nettoyage_profondeur_detail(request):
    return render(request, 'detail_services/detail_nettoyage_profondeur.html')

def nettoyage_regulier_detail(request):
    return render(request, 'detail_services/detail_nettoyage_regulier.html')

def nettoyage_industriel_detail(request):
    return render(request, 'detail_services/detail_nettoyage_industriel.html')

