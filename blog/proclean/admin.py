# blog/proclean/admin.py
from django.contrib import admin
from .models import Service, CarouselImage, ContactMessage,JobApplication
from .models import JobApplication,JobRequest



# Register your models here. 

class AdminService(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'image')
admin.site.register(Service, AdminService)

class AdminCarouselImage(admin.ModelAdmin):
    list_display = ('id', 'title', 'image', 'is_active')
admin.site.register(CarouselImage, AdminCarouselImage)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'email', 'telephone', 'date_envoi', 'lu')
    list_filter = ('lu', 'date_envoi')
    search_fields = ('prenom', 'nom', 'email', 'message', 'telephone')
    readonly_fields = ('date_envoi',)
    list_per_page = 25
    ordering = ('-date_envoi',)
    date_hierarchy = 'date_envoi'
    
    # Champs dans la vue détaillée
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('prenom', 'nom', 'email', 'telephone')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('État', {
            'fields': ('lu', 'date_envoi')
        }),
    )
    
    # Actions personnalisées
    actions = ['marquer_comme_lu', 'marquer_comme_non_lu']
    
    # Méthodes personnalisées
    def nom_complet(self, obj):
        return f"{obj.prenom} {obj.nom}"
    nom_complet.short_description = "Nom complet"
    
    def marquer_comme_lu(self, request, queryset):
        updated = queryset.update(lu=True)
        self.message_user(request, f"{updated} message(s) marqué(s) comme lu.")
    marquer_comme_lu.short_description = "Marquer comme lu"
    
    def marquer_comme_non_lu(self, request, queryset):
        updated = queryset.update(lu=False)
        self.message_user(request, f"{updated} message(s) marqué(s) comme non lu.")
    marquer_comme_non_lu.short_description = "Marquer comme non lu"


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'email', 'region', 'date_soumission', 'traite')
    list_filter = ('region', 'experience_menage', 'vehicule', 'traite', 'date_soumission')
    search_fields = ('nom', 'prenom', 'email', 'telephone')
    readonly_fields = ('date_soumission',)
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('nom', 'prenom', 'email', 'telephone')
        }),
        ('Préférences de travail', {
            'fields': ('region', 'region_autre', 'disponibilites', 'experience_menage', 'vehicule')
        }),
        ('Documents et message', {
            'fields': ('cv', 'message')
        }),
        ('Administration', {
            'fields': ('date_soumission', 'traite', 'notes', 'consentement')
        }),
    )
    
    
@admin.register(JobRequest)
class JobRequestAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'email', 'received_at')
    list_filter = ('received_at',)
    search_fields = ('nom', 'prenom', 'email')
    ordering = ('-received_at',)

