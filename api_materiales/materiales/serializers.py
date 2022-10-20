from rest_framework import serializers
from .models import *

class MaterialSerializer(serializers.ModelSerializer):
   class Meta:
       model = Material
       fields = "__all__"

class ProviderSerializer(serializers.ModelSerializer):
   class Meta:
       model = Provider
       fields = "__all__"

class MaterialProviderSerializer(serializers.ModelSerializer):
   class Meta:
       model = Material_Provider
       fields = "__all__"

class ReserveMaterialSerializer(serializers.ModelSerializer):
   class Meta:
       model = Reserve_material
       fields = "__all__"

class FactoryPlaceSerializer(serializers.ModelSerializer):
   class Meta:
       model = Factory_Place
       fields = "__all__"

class ReserveFactorySerializer(serializers.ModelSerializer):
   class Meta:
       model = Reserve_Factory
       fields = "__all__"

class EnterpriseSerializer(serializers.ModelSerializer):
   class Meta:
       model = Enterprise
       fields = "__all__"
