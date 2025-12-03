from django.shortcuts import render
from .models import Service,CarouselImage


# def home(request):
#     images = CarouselImage.objects.all()
#     return render(request, "accueil.html",{"carousel_images": images})

def home(request):
    # Testez d'abord si des images existent
    images = CarouselImage.objects.filter(is_active=True).order_by('id')
    
    if not images.exists():
        print("Aucune image active trouvée dans la base de données")
    
    context = {
        'carousel_images': images,
    }
    return render(request, 'accueil.html', context)