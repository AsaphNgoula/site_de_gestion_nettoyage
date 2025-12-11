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

# models.py
# blog/proclean/models.py
from django.db import models

class ContactMessage(models.Model):
    prenom = models.CharField(
        max_length=100,
        verbose_name="Prénom"
    )
    nom = models.CharField(
        max_length=100,
        verbose_name="Nom"
    )
    email = models.EmailField(
        verbose_name="Adresse email"
    )
    telephone = models.CharField(
        max_length=20,
        blank=True,
        null=True,  # Ajoutez null=True pour la base de données
        verbose_name="Téléphone",
        help_text="Optionnel"
    )
    message = models.TextField(
        verbose_name="Message"
    )
    date_envoi = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date d'envoi"
    )
    lu = models.BooleanField(
        default=False,
        verbose_name="Lu"
    )
    
    class Meta:
        ordering = ['-date_envoi']
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"
    
    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.date_envoi.strftime('%d/%m/%Y %H:%M')}"
    
    def mark_as_read(self):
        """Marquer le message comme lu"""
        self.lu = True
        self.save()
    
    @property
    def nom_complet(self):
        """Retourne le nom complet"""
        return f"{self.prenom} {self.nom}"