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
    



class JobApplication(models.Model):
    REGION_CHOICES = [
        ('montreal_laval', 'Montréal / Laval'),
        ('gatineau_ottawa', 'Gatineau / Ottawa'),
        ('quebec', 'Québec'),
        ('joliette_lanaudiere', 'Joliette / Lanaudière'),
        ('valdor_abitibi', 'Val-d’Or / Abitibi'),
        ('cotenord_saguenay', 'Côte-Nord / Saguenay'),
        ('autre', 'Autre'),
    ]
    
    AVAILABILITY_CHOICES = [
        ('soir', 'Soir'),
        ('fin_semaine', 'Fin de semaine'),
        ('temps_partiel', 'Temps partiel'),
        ('temps_plein', 'Temps plein'),
        ('jours', 'Jours'),
    ]
    
    # Informations personnelles
    nom = models.CharField(max_length=100, verbose_name="Nom *")
    prenom = models.CharField(max_length=100, verbose_name="Prénom *")
    email = models.EmailField(verbose_name="Adresse e-mail *")
    telephone = models.CharField(max_length=20, verbose_name="Téléphone *")
    
    # Préférences
    region = models.CharField(
        max_length=50, 
        choices=REGION_CHOICES, 
        verbose_name="Région où vous souhaitez travailler *"
    )
    region_autre = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Autre région (préciser)"
    )
    
    # Disponibilités (plusieurs choix possibles)
    disponibilites = models.JSONField(
        default=list,
        verbose_name="Disponibilités *"
    )
    
    # Expérience et transport
    experience_menage = models.BooleanField(
        default=False,
        verbose_name="Avez-vous de l'expérience en entretien ménager ? *"
    )
    vehicule = models.BooleanField(
        default=False,
        verbose_name="Possédez-vous un véhicule ou moyen de transport fiable ? *"
    )
    
    # Fichiers
    cv = models.FileField(
        upload_to='cv_applications/%Y/%m/%d/',
        verbose_name="CV *",
        help_text="Formats acceptés: PDF, DOC, DOCX (max 5MB)"
    )
    
    # Message optionnel
    message = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Message additionnel"
    )
    
    # Administration
    date_soumission = models.DateTimeField(auto_now_add=True, verbose_name="Date de soumission")
    traite = models.BooleanField(default=False, verbose_name="Traité")
    notes = models.TextField(blank=True, null=True, verbose_name="Notes internes")
    
    # GDPR
    consentement = models.BooleanField(
        default=False,
        verbose_name="J'accepte le traitement de mes données personnelles"
    )
    
    class Meta:
        verbose_name = "Candidature"
        verbose_name_plural = "Candidatures"
        ordering = ['-date_soumission']
    
    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.date_soumission.strftime('%d/%m/%Y')}"
    
    def get_disponibilites_display(self):
        """Retourne les disponibilités formatées"""
        disponibilites_dict = dict(self.AVAILABILITY_CHOICES)
        return ", ".join([disponibilites_dict.get(d, d) for d in self.disponibilites])
    
    def get_region_display_full(self):
        """Retourne la région complète"""
        if self.region == 'autre' and self.region_autre:
            return f"Autre: {self.region_autre}"
        return self.get_region_display()