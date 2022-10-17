from django.contrib import admin

from .models import Factory_Place, Material, Material_Provider, Material_arrived, Provider, Reserve_Factory

# Register your models here.
admin.site.register(Provider)
admin.site.register(Material)
admin.site.register(Reserve_Factory)
admin.site.register(Factory_Place)
admin.site.register(Material_Provider)
admin.site.register(Material_arrived)
