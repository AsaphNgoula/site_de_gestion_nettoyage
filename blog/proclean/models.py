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
    
    