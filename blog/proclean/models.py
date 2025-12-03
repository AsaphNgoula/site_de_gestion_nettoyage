from django.db import models
# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='services/')

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        
    
class CarouselImage(models.Model):
    image = models.ImageField(upload_to="carousel/")
    title = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title if self.title else "Image Carousel"
    
    class Meta:
        verbose_name = 'CarouselImage'
        verbose_name_plural = 'CarouselImages'
    

class ServiceCard(models.Model):
    SERVICE_TYPES = [
        ('regular', 'Nettoyage Régulier'),
        ('deep', 'Nettoyage en Profondeur'),
        ('move', 'Nettoyage Déménagement'),
        ('airbnb', 'Nettoyage Airbnb'),
        ('carpet', 'Nettoyage de Tapis'),
        ('commercial', 'Nettoyage Commercial'),
    ]
    
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="services/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    button_text = models.CharField(max_length=50, default="En savoir plus")
    
    class Meta:
        verbose_name = 'Carte de Service'
        verbose_name_plural = 'Cartes de Services'
        ordering = ['order']
    
    def __str__(self):
        return self.title
