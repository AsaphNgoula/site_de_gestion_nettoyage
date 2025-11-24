from django.db import models

# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='services/')
    id = models.IntegerField(primary_key=True, editable=False,blank=False)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        