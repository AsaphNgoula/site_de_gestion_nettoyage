from django.contrib import admin
from .models import Service,CarouselImage,ServiceCard

# Register your models here.
class AdminService(admin.ModelAdmin):
    list_display=('id','name','description','image')
admin.site.register(Service, AdminService)

class AdminCarouselImage(admin.ModelAdmin):
    list_display=('id','title','image','is_active')
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
