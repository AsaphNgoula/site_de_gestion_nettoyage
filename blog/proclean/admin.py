from django.contrib import admin
from .models import Service,CarouselImage

# Register your models here.
class AdminService(admin.ModelAdmin):
    list_display=('id','name','description','image')

admin.site.register(Service, AdminService)
admin.site.register(CarouselImage)

