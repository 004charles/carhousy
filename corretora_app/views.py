from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Usuario, Imovel,GaleriaImovel
from django.contrib.auth.hashers import make_password
import random
import string
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import Usuario
from django.core.mail import send_mail
from django.conf import settings




def gerar_codigo():
    """Função para gerar um código único para o usuário"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=18))

def cadastrar_usuario(request):
    status = request.GET.get('status')
    if request.method == "POST":
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        telefone = request.POST.get('telefone')
        endereco = request.POST.get('endereco')
        tipo_usuario = request.POST.get('tipousuario') 
        imagem = request.FILES.get('imagem')

        if not nome or not sobrenome or not email or not senha or not telefone or not endereco or not tipo_usuario:
            messages.error(request, "Todos os campos são obrigatórios!")
            return redirect('/carhousy/register/?status=1')  # Alerta de campos obrigatórios

        if len(senha) < 8:
            messages.error(request, "A senha precisa ter pelo menos 8 caracteres.")
            return redirect('/carhousy/register/?status=2')  # Alerta de senha fraca

        if Usuario.objects.filter(email=email).exists():
            messages.error(request, "Este e-mail já está cadastrado.")
            return redirect('/carhousy/register/?status=3')  # Alerta de e-mail já cadastrado

        # Verifica se o tipo de usuário é válido
        tipos_validos = ['cliente', 'vendedor', 'corretor']
        if tipo_usuario not in tipos_validos:
            messages.error(request, "Tipo de usuário inválido.")
            return redirect('/carhousy/register/?status=5')  # Alerta de tipo de usuário inválido

        # Geração do código único
        codigo = gerar_codigo()

        # Criação do usuário e salvamento no banco
        try:
            senha_hash = make_password(senha)  # Gera o hash da senha
            usuario = Usuario(
                nome=nome,
                sobrenome=sobrenome,
                email=email,
                senha=senha_hash,
                telefone=telefone,
                endereco=endereco,
                tipo_usuario=tipo_usuario,
                imagem=imagem,
                codigo=codigo
            )
            usuario.save()  # Salva no banco de dados

            # Mensagem personalizada com base no tipo de usuário
            if tipo_usuario == 'cliente':
                mensagem = f'Olá {nome}!\n\nObrigado por se cadastrar na Carhousy. Estamos felizes em tê-lo conosco!\n\nRumo ao teu sonho da casa própria! Estamos aqui para ajudar você a encontrar o lar dos seus sonhos.\n\nAtenciosamente,\nEquipe Carhousy'
            elif tipo_usuario == 'vendedor':
                mensagem = f'Olá {nome}!\n\nObrigado por se cadastrar como vendedor na Carhousy. Agora você pode oferecer os melhores imóveis para nossos clientes. Estamos aqui para ajudá-lo a alcançar suas metas!\n\nAtenciosamente,\nEquipe Carhousy'
            elif tipo_usuario == 'corretor':
                mensagem = f'Olá {nome}!\n\nObrigado por se cadastrar como corretor na Carhousy. Sua jornada começa agora para conectar clientes a imóveis incríveis. Estamos aqui para ajudá-lo a ter sucesso!\n\nAtenciosamente,\nEquipe Carhousy'

            # Envio do e-mail de boas-vindas
            send_mail(
                'Bem-vindo à Carhousy',  # Assunto
                mensagem,  # Corpo do e-mail com a mensagem personalizada
                settings.EMAIL_HOST_USER,  # Remetente
                [email],  # Destinatário
                fail_silently=False,  # Caso ocorra algum erro, não falhar silenciosamente
            )

            messages.success(request, "Usuário cadastrado com sucesso!")
            return redirect('/carhousy/register/?status=0')  # Sucesso no cadastro

        except Exception as e:
            print(f"Erro ao cadastrar usuário: {e}")
            messages.error(request, "Ocorreu um erro ao cadastrar o usuário. Tente novamente.")
            return redirect('/carhousy/register/?status=4')  # Erro de salvamento
    else:
        return render(request, 'register.html')  # Exibe o formulário de cadastro

def login_usuario(request):
    if request.method == "POST":
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        # Filtra o usuário com base no email
        usuario = Usuario.objects.filter(email=email).first()

        # Se não encontrar nenhum usuário
        if not usuario:
            messages.error(request, "Credenciais inválidas. Tente novamente.")
            return redirect('/carhousy/sign_up/?status=8')  # Redireciona para a página de login com mensagem de erro

        # Verifica a senha de forma segura
        if not check_password(senha, usuario.senha):
            messages.error(request, "Credenciais inválidas. Tente novamente.")
            return redirect('/carhousy/sign_up/?status=8')  # Redireciona para a página de login com mensagem de erro

        # Caso encontre um usuário, armazena o id na sessão
        request.session['usuario'] = usuario.id

        # Redireciona o usuário dependendo do tipo
        if usuario.tipo_usuario == 'cliente':
            return redirect('home')  # Redireciona para a home do cliente
        elif usuario.tipo_usuario == 'vendedor':
            return redirect('home')  # Redireciona para a home do vendedor
        elif usuario.tipo_usuario == 'corretor':
            return redirect('home')  # Redireciona para a home do corretor

    # Se não for um POST, apenas renderiza a página de login
    return render(request, 'login.html')

def home(request):
    usuario_logado = None
    if 'usuario' in request.session:
        try:
            usuario_logado = Usuario.objects.get(id=request.session['usuario'])
        except Usuario.DoesNotExist:
            pass
    imovel_venda = Imovel.objects.all()
    return render(request, 'home.html', {'usuario_logado': usuario_logado, 'imovel_venda':imovel_venda})

def sign_up(request):
    status = request.GET.get('status')
    return render(request, 'login.html', {'status':status})

def register(request):
    status = request.GET.get('status')
    return render(request, 'register.html',{'status':status})


#------------------------------fim autenticacao-------------------------------

def house_buy(request):
    imovel_venda = Imovel.objects.all()
    return render(request, 'casa_vender.html', {'imovel_venda':imovel_venda})

def detalhe_projecto(request, id):
    imovel_venda = get_object_or_404(Imovel, id=id)
    return render(request, 'detalhe_projecto.html', {'imovel_venda':imovel_venda})