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
    name = models.CharField(max_length=100)
    
class Material_Provider(models.Model):
    material_id = models.ForeignKey(Material, null=True, on_delete=models.CASCADE)
    provider_id = models.ForeignKey(Provider, null=True, on_delete=models.CASCADE)
    total_amount = models.IntegerField(default = 1000)
    compromise_amount = models.IntegerField(default = 0)

class Material_arrived(models.Model):
    material_id = models.ForeignKey(Material, null=True, on_delete=models.CASCADE)
    provider_id = models.ForeignKey(Provider, null=True, on_delete=models.CASCADE)
    amount = models.IntegerField(default = 0)
    date = models.DateTimeField()

class Enterprise(models.Model):
    name = models.CharField(max_length=100)

class Factory_Place(models.Model):
    name = models.CharField(max_length=100)

class Reserve_material(models.Model):
    material_id = models.ForeignKey(Material, null=True, on_delete=models.CASCADE)
    provider_id = models.ForeignKey(Provider, null=True,on_delete=models.CASCADE)
    amount = models.IntegerField(null=True, default = 0)
    reserve_date = models.DateTimeField(null=True,)
    factory_place_id = models.ForeignKey(Factory_place, null=True, on_delete=models.CASCADE)
    enterprise_id = models.ForeignKey(Enterprise, null=True, on_delete=models.CASCADE)
    state = models.CharField(max_length=100)
    
    def add(self, material_id, provider_id, amount, reserve_date, factory_place_id, enterprise_id):
        self.material_id = material_id
        self.provider_id = provider_id
        self.amount = amount
        self.reserve_date = reserve_date
        self.factory_place_id = factory_place_id
        self.enterprise_id = enterprise_id
        self.state = 'activo'

    def strJson(self):
        json = {
            "id": self.id,
            "id_material":self.material_id.id,
            "id_provider":self.provider_id.id,
            "id_sede":self.factory_place_id.id,
            "id_empresa":self.enterprise_id.id,
            "amount":self.amount,
            "reserve_date":self.reserve_date,
            "state": self.state
        }
        return json

class Reserve_Factory(models.Model):
    factory_place_id = models.ForeignKey(Factory_Place, null=True, on_delete=models.CASCADE)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    enterprise = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
