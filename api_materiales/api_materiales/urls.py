from django.urls import include, path
from  materiales import views
from django.contrib import admin
from rest_framework import routers

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('ask_for_material/', views.ask_for_material, name='ask_for_material'),
    path('materials', views.materials, name='materials'),
    path('stock/', views.stock_update, name='ask_for_material'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('reserve_material/', views.reserve_material, name='reserve_material'),
]