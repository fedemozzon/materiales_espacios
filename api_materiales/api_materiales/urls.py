from crypt import methods
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
    path('reserve', views.reserve, name='reserve_facility'),
    path('find_place/', views.find_place_by_dates, name='find_place_by_dates'),
    path('ask_for_material/', views.ask_for_material, name='ask_for_material'),
    path('stock/', views.stock_update, name='ask_for_material'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]