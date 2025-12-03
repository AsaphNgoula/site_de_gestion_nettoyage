# views.py
from django.shortcuts import render
from .models import CarouselImage,ServiceCard

def home(request):
    # Récupérer les images actives du carousel
    carousel_images = CarouselImage.objects.filter(is_active=True).order_by('id')
    
    # Debug: afficher le nombre d'images trouvées
    if not carousel_images.exists():
        print(f"DEBUG: Aucune image active trouvée dans CarouselImage. Total: {CarouselImage.objects.count()}")
    else:
        print(f"DEBUG: {carousel_images.count()} images actives trouvées")
    
    # Récupérer les services actifs
    services = ServiceCard.objects.filter(is_active=True).order_by('order')
    
    # Debug: afficher le nombre de services trouvés
    if not services.exists():
        print(f"DEBUG: Aucun service actif trouvé dans ServiceCard. Total: {ServiceCard.objects.count()}")
    else:
        print(f"DEBUG: {services.count()} services actifs trouvés")
    
    # Créer un contexte avec 6 services (utiliser ceux de la BD ou créer des fallbacks)
    if services.exists():
        services_list = list(services)
    else:
        # Fallback si aucun service n'est configuré
        services_list = []
        for i in range(6):
            services_list.append({
                'title': f'Service {i+1}',
                'description': 'Description du service sera ajoutée depuis l\'administration.',
                'image': None,
                'button_text': 'En savoir plus'
            })
    
    context = {
        'carousel_images': carousel_images,
        'services': services_list,
        'services_count': len(services_list),
    }
    
    return render(request, 'accueil.html', context)