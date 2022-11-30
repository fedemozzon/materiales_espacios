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

class FactoryPlaceSerializer(serializers.ModelSerializer):
   class Meta:
       model = Factory_Place
       fields = "__all__"

class EnterpriseSerializer(serializers.ModelSerializer):
   class Meta:
       model = Enterprise
       fields = "__all__"

class MaterialReservationSerializer(serializers.ModelSerializer):
    material = MaterialSerializer(read_only=True, many=False)
    provider = ProviderSerializer(read_only=True, many=False)
    place = ProviderSerializer(read_only=True, many=False)
    class Meta:
       model = Material_reservation
       fields =  "__all__"

class PlaceReservationSerializer(serializers.ModelSerializer):
    place = ProviderSerializer(read_only=True, many=False)
    class Meta:
       model = Place_reservation
       fields =  "__all__"