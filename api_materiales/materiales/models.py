from django.db import models

# Create your models here.
        
class Provider(models.Model):
    name = models.CharField(max_length=100)
    
    def add(self, name):
        self.name = name
        self.save()