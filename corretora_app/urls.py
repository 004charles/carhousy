from django.urls import path
from corretora_app import views

urlpatterns = [
    path('sign_up/', views.sign_up, name = 'sign_up'),
    path('register/', views.register, name = 'register'),
    path('login_usuario/', views.login_usuario, name='login_usuario'),
    path('cadastrar_usuario/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('house_buy/', views.house_buy, name='house_buy'),
    path('detalhe_projecto<int:id>/', views.detalhe_projecto, name='detalhe_projecto'),
]
