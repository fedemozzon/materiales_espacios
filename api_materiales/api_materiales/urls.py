from crypt import methods
from django.urls import include, path, re_path
from  materiales import views
from django.contrib import admin
from rest_framework import permissions
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Documentacion de API",
      default_version='v1',
      description="Se especifican los endpoints de la API que concentra información sobre materiales y proveedores",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token_refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('materials', views.materials, name='materials'),
    path('stock/', views.stock_update, name='stock'),
    path('ask_for_material/', views.ask_for_material, name='ask_for_material'),
    path('reserve_material/', views.reserve_material, name='reserve_material'),
    path('cancel_reserve_material/', views.cancel_reserve_material, name='cancel_reserve_material'),
    path('find_place/', views.find_place_by_dates, name='find_place_by_dates'),
    path('reserve', views.reserve, name='reserve_facility'),
    path('cancel_reserve_place/', views.cancel_reservation, name='cancel_reservation'),
]