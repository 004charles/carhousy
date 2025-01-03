from django.contrib import admin
from django.urls import path, include
from corretora_app import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name = 'home'),
    path('admin/', admin.site.urls),
    path('carhousy/', include('corretora_app.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
