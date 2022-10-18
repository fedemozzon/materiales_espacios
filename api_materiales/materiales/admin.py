from django.contrib import admin

from .models import *

class ProviderAdmin(admin.ModelAdmin):
    list_display = ('name',)

class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name',)
   

class MaterialProviderAdmin(admin.ModelAdmin):
    list_display = ('get_material_name', 'get_provider_name', 'total_amount', 'compromise_amount',)
    
    def get_material_name(self, obj):
        return obj.material_id.name

    def get_provider_name(self, obj):
        return obj.provider_id.name

class EnterpriseAdmin(admin.ModelAdmin):
    list_display = ('name',)
   
class FactoryPlaceAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ReserveMaterialAdmin(admin.ModelAdmin):
    list_display = ('get_material_name', 'get_provider_name','get_factory_place_name',
    'get_enterprise_name','amount', 'reserve_date','state',)
    
    def get_material_name(self, obj):
        return obj.material_id.name

    def get_provider_name(self, obj):
        return obj.provider_id.name
    
    def get_factory_place_name(self, obj):
        return obj.factory_place_id.name

    def get_enterprise_name(self, obj):
        return obj.enterprise_id.name 

# Register your models here.
admin.site.register(Provider, ProviderAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Material_Provider, MaterialProviderAdmin)
admin.site.register(Material_arrived)
admin.site.register(Enterprise, EnterpriseAdmin)
admin.site.register(Factory_place, FactoryPlaceAdmin)
admin.site.register(Reserve_material, ReserveMaterialAdmin)