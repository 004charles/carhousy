from django.contrib import admin
from django.urls import path, include
from corretora_app import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('admin/', admin.site.urls),
    path('carhousy/', include('corretora_app.urls')),
]
