from django.urls import path
from corretora_app import views

urlpatterns = [
    path('sign_up/', views.sign_up, name = 'sign_up'),
    path('register/', views.register, name = 'register'),
    path('login_usuario/', views.login_usuario, name='login_usuario'),
    path('dashboard_usuario/', views.dashboard_usuario, name='dashboard_usuario'),
    path('cadastrar_usuario/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('house_buy/', views.house_buy, name='house_buy'),
    path('nova_casa/', views.nova_casa, name = 'nova_casa'),
    path('cadastro-imovel/', views.cadastro_imovel, name='cadastro_imovel'),
    path('detalhe_projecto<int:id>/', views.detalhe_projecto, name='detalhe_projecto'),
    path('Nossa_missao/', views.Nossa_missao, name = 'Nossa_missao'),
    path('servico/', views.servico, name = 'servico'),
    #path('blog/', views.blog, name = 'blog'),
    path('sobre/', views.sobre, name = 'sobre'),
    path('faq/', views.faq, name = 'faq'),
    path('equipe/', views.equipe, name = 'equipe'),
    path('perfil_usuario/', views.perfil_usuario, name = 'perfil_usuario'),
    path('contacto/', views.contacto, name = 'contacto'),
    path('pagina_error/', views.pagina_error, name = 'pagina_error'),
    path('agendamento<int:id>/', views.agendamento, name='agendamento'),
    path('logout/', views.logout, name='logout'),
    path('erro/', views.Erro, name = 'erro'),
    path('imoveis_publicados/', views.imoveis_publicados, name='imoveis_publicados')
]
