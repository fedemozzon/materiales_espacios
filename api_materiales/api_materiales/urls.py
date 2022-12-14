from crypt import methods
from django.urls import include, path
from  materiales import views
from django.contrib import admin
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # revisar
    path('reserve', views.reserve, name='reserve_facility'),
    #revisar
    path('find_place/', views.find_place_by_dates, name='find_place_by_dates'),
    path('ask_for_material/', views.ask_for_material, name='ask_for_material'),
    path('cancel_reserve_place/', views.cancel_reservation, name='cancel_reservation'),
    path('materials', views.materials, name='materials'),
    path('stock/', views.stock_update, name='ask_for_material'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('reserve_material/', views.reserve_material, name='reserve_material'),
    path('cancel_reserve_material/', views.cancel_reserve_material, name='cancel_reserve_material')
]