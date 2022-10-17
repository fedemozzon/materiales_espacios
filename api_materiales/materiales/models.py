from email.policy import default
from pyexpat import model
from unicodedata import name
from django.db import models

# Create your models here.
        
class Provider(models.Model):
    name = models.CharField(max_length=100)
    def add(self, name):
        self.name = name
        self.save()
        
class Material(models.Model):
    name = name = models.CharField(max_length=100)
    provider_id = models.ManyToManyField("Provider")
    
class Material_Provider(models.Model):
    material_id = models.ForeignKey(Material, null=True, on_delete=models.CASCADE)
    provider_id = models.ForeignKey(Provider, null=True, on_delete=models.CASCADE)
    total_amount = models.IntegerField(default = 1000)
    compromise_amount = models.IntegerField(default = 0)