# blog/proclean/admin.py
from django.contrib import admin
from .models import Service, CarouselImage, ServiceCard, ContactMessage

# Register your models here.

class AdminService(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'image')
admin.site.register(Service, AdminService)

class AdminCarouselImage(admin.ModelAdmin):
    list_display = ('id', 'title', 'image', 'is_active')
admin.site.register(CarouselImage, AdminCarouselImage)

@admin.register(ServiceCard)
class ServiceCardAdmin(admin.ModelAdmin):
    list_display = ('title', 'service_type', 'order', 'is_active')
    list_filter = ('is_active', 'service_type')
    search_fields = ('title', 'description')
    ordering = ('order',)
    fieldsets = (
        ('Informations de base', {
            'fields': ('service_type', 'title', 'description', 'button_text')
        }),
        ('Image', {
            'fields': ('image',)
        }),
        ('Configuration', {
            'fields': ('order', 'is_active')
        }),
    )

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