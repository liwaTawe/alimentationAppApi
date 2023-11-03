from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from myshop import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path("api/v1/", include("product.urls")),
    path('api/accounts/', include("accounts.urls"))

   
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

