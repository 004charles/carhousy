from django.shortcuts import render, redirect
from django.contrib.auth import login
import logging
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import render, get_object_or_404
from .models import Usuario, Imovel,GaleriaImovel, Publicidade_home, Agendamento, HoraAgendamento
from django.contrib.auth.hashers import make_password
import random
import string
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from datetime import datetime
from django.db import IntegrityError



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
        tipos_validos = ['cliente', 'vendedor', 'corretor', 'empresa']
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
                
            elif tipo_usuario == 'empresa':
                mensagem = f'Olá {nome}!\n\n' \
                f'Obrigado por se cadastrar como empresa na Carhousy! Estamos entusiasmados em tê-lo conosco para ajudar a conectar clientes a imóveis incríveis. Agora você tem a oportunidade de publicar seus imóveis e alcançar um público ainda maior.\n\n' \
                f'Nosso time está à disposição para oferecer todo o suporte necessário e ajudá-lo a alcançar seus objetivos de vendas e locação.\n\n' \
                f'Atenciosamente,\nEquipe Carhousy'


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
            return redirect('home')
        elif usuario.tipo_usuario == 'empresa':
            return redirect('home') 
          # Redireciona para a home do corretor

    # Se não for um POST, apenas renderiza a página de login
    return render(request, 'login.html')

def home(request):
    usuario_logado = None
    if 'usuario' in request.session:
        try:
            usuario_logado = Usuario.objects.get(id=request.session['usuario'])
        except Usuario.DoesNotExist:
            pass
    imovel_venda = Imovel.objects.filter(tipo='casa')
    corretores = Usuario.objects.filter(tipo_usuario='corretor')
    video_home = Publicidade_home.objects.filter(video__isnull=False).first()
    office = Imovel.objects.filter(tipo='escritorio')

    return render(request, 'home.html',{'usuario_logado':usuario_logado, 'imovel_venda':imovel_venda, 'office':office,'video_home':video_home, 'corretores':corretores})

def sign_up(request):
    status = request.GET.get('status')
    return render(request, 'login.html', {'status':status})

def register(request):
    status = request.GET.get('status')
    return render(request, 'register.html',{'status':status})

def logout(request):
    request.session.flush()
    
    return redirect('home') 


#------------------------------fim autenticacao-------------------------------

def house_buy(request):
    usuario_logado = None
    if 'usuario' in request.session:
        try:
            usuario_logado = Usuario.objects.get(id=request.session['usuario'])
        except Usuario.DoesNotExist:
            pass
    imovel_venda = Imovel.objects.all()
    return render(request, 'casa_vender.html', {'imovel_venda':imovel_venda})

def detalhe_projecto(request, id):
    usuario_logado = None
    if 'usuario' in request.session:
        try:
            usuario_logado = Usuario.objects.get(id=request.session['usuario'])
        except Usuario.DoesNotExist:
            pass
    imovel_venda = get_object_or_404(Imovel, id=id)
    horarios = HoraAgendamento.objects.all()
    return render(request, 'detalhe_projecto.html', {'imovel_venda':imovel_venda, 'usuario_logado':usuario_logado, 'horarios':horarios})


def Nossa_missao(request):
    usuario_logado = None
    if 'usuario' in request.session:
        try:
            usuario_logado = Usuario.objects.get(id=request.session['usuario'])
        except Usuario.DoesNotExist:
            pass
    return render(request, 'Nossa_missao.html', {'usuario_logado':usuario_logado})

def sobre(request):
    usuario_logado = None
    if 'usuario' in request.session:
        try:
            usuario_logado = Usuario.objects.get(id=request.session['usuario'])
        except Usuario.DoesNotExist:
            pass
    return render(request, 'sobre.html', {'usuario_logado':usuario_logado})

def pagina_error(request):
    usuario_logado = None
    if 'usuario' in request.session:
        try:
            usuario_logado = Usuario.objects.get(id=request.session['usuario'])
        except Usuario.DoesNotExist:
            pass
    return render(request, 'error.html', {'usuario_logado':usuario_logado})


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
def processar_agendamento(request, imovel_venda, nome, sobrenome, email, telefone, data_visita, hora_visita, mensagem):
    try:
        # Validação do e-mail
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError('O e-mail informado é inválido.')

        # Corrige formato da hora para '08:00' se necessário
        if len(hora_visita) == 1:
            hora_visita = f'0{hora_visita}:00'
        elif len(hora_visita) == 2:
            hora_visita = f'{hora_visita}:00'

        # Convertendo data e hora
        data_hora_visita = datetime.combine(
            datetime.strptime(data_visita, '%Y-%m-%d'),
            datetime.strptime(hora_visita, '%H:%M').time()
        )

        if data_hora_visita < datetime.now():
            raise ValidationError('Não é possível agendar para uma data/hora passada.')

        # Criando ou atualizando o cliente
        cliente, created = Usuario.objects.get_or_create(
            email=email,
            defaults={'nome': nome, 'sobrenome': sobrenome, 'telefone': telefone, 'tipo_usuario': 'cliente'}
        )

        if not created and cliente.telefone != telefone:
            cliente.telefone = telefone
            cliente.save()

        # Verifica duplicidade de agendamento
        if Agendamento.objects.filter(imovel=imovel_venda, cliente=cliente, data_hora_agendada=data_hora_visita).exists():
            raise ValidationError('Você já possui um agendamento neste horário.')

        # Criando o agendamento
        agendamento = Agendamento.objects.create(
            imovel=imovel_venda,
            cliente=cliente,
            data_hora_agendada=data_hora_visita,
            mensagem=mensagem,
            status='agendado'
        )

        # Envio de e-mails para os corretores
        corretores = Usuario.objects.filter(tipo_usuario='corretor')
        if corretores.exists():
            for corretor in corretores:
                send_mail(
                    'Novo Agendamento Realizado para o Imóvel',
                    f'Prezado(a) {corretor.nome},\n\n'
                    f'Gostaríamos de informar que foi realizado um novo agendamento para o imóvel de sua responsabilidade.\n\n'
                    f'**Detalhes do Agendamento:**\n'
                    f'Imóvel: {imovel_venda}\n'
                    f'Data e Hora: {data_hora_visita.strftime("%d/%m/%Y %H:%M")}\n'
                    f'Mensagem do Cliente: {mensagem}\n\n'
                    f'Por favor, verifique os detalhes e entre em contato com o cliente caso necessário.\n\n'
                    f'Atenciosamente,\n'
                    f'Sua Plataforma de Imóveis',
                    settings.DEFAULT_FROM_EMAIL,
                    [corretor.email]
                )
        else:
            logger.warning(f'Nenhum corretor encontrado para o imóvel {imovel_venda}')

    except Exception as e:
        logger.error(f'Ocorreu um erro ao processar o agendamento: {e}')
        raise

def agendamento(request, id):
    usuario_logado = None
    if 'usuario' in request.session:
        try:
            usuario_logado = Usuario.objects.get(id=request.session['usuario'])
        except Usuario.DoesNotExist:
            pass

    imovel_venda = get_object_or_404(Imovel, id=id)
    status = request.GET.get('status')

    if request.method == "POST":
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        data_visita = request.POST.get('data_visita')
        hora_visita = request.POST.get('hora_visita')
        mensagem = request.POST.get('mensagem')

        # Validação da hora
        if HoraAgendamento.objects.filter(id=hora_visita).exists():
            try:
                processar_agendamento(
                    request,
                    imovel_venda,
                    nome,
                    sobrenome,
                    email,
                    telefone,
                    data_visita,
                    hora_visita,
                    mensagem
                )
                messages.success(request, 'Agendamento realizado com sucesso!')
                return render(request, 'detalhe_projecto.html', {'status': status, 'imovel_venda': imovel_venda, 'horarios':horarios})
            except ValidationError as e:
                messages.error(request, f'Erro de validação: {e}')
            except Exception as e:
                messages.error(request, f'Ocorreu um erro ao realizar o agendamento: {e}')
        else:
            messages.error(request, 'Horário selecionado é inválido.')

    horarios = HoraAgendamento.objects.all()
    return render(request, 'detalhe_projecto.html', {
        'status': status,
        'imovel_venda': imovel_venda,
        'usuario_logado': usuario_logado,
        'horarios': horarios
    })


def Erro(request, exception):
    return render(request, 'error.html', status=404)