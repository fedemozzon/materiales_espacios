from django.contrib import admin

from .models import Material, Material_Provider, Provider

# Register your models here.
admin.site.register(Provider)
admin.site.register(Material)
admin.site.register( Material_Provider)
