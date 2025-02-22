from django.shortcuts import render, redirect
from django.contrib.auth import login
import logging
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import render, get_object_or_404
from .models import Usuario, Imovel,GaleriaImovel, Publicidade_home, Agendamento, HoraAgendamento, DadosAdicionais, Depoimentos
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
    imovel_venda = Imovel.objects.filter(apresentar=True,destaque=False,tipo='casa' or'apartamento' or 'comercial')
    corretores = Usuario.objects.filter(tipo_usuario='corretor')
    video_home = Publicidade_home.objects.filter(video__isnull=False).first()
    office = Imovel.objects.filter(tipo='escritorio', apresentar=True)
    terrenos = Imovel.objects.filter(tipo='terreno', apresentar=True)
    imoveis_detaque = Imovel.objects.filter(destaque=True).order_by('data_publicacao')
    depoimentos = Depoimentos.objects.filter(apresentar=True,).order_by('data_cadastro')
    
    return render(request, 'home.html',{'usuario_logado':usuario_logado, 'imovel_venda':imovel_venda, 'office':office,'video_home':video_home, 'corretores':corretores, 'terrenos': terrenos, 'imoveis_detaque':imoveis_detaque, 'depoimentos': depoimentos})

def sign_up(request):
    status = request.GET.get('status')
    return render(request, 'login.html', {'status':status})

def register(request):
    status = request.GET.get('status')
    return render(request, 'register.html',{'status':status})

def dashboard_usuario(request):
    usuario_logado = None
    if 'usuario' in request.session:
        try:
            usuario_logado = Usuario.objects.get(id=request.session['usuario'])
        except Usuario.DoesNotExist:
            return redirect('home')
        imoveis_publicados = Imovel.objects.filter(email_anunciante=usuario_logado.email,nome_anunciante=usuario_logado.nome,telefone_anunciante=usuario_logado.telefone).order_by('data_publicacao')
        return render(request, 'usuario_dashboard.html', {'usuario_logado': usuario_logado,'imoveis_publicados':imoveis_publicados})

    else:
        imoveis_publicados = Imovel.objects.filter(email_anunciante=usuario_logado.email,nome_anunciante=usuario_logado.nome,telefone_anunciante=usuario_logado.telefone).order_by('data_publicacao')
        return render(request, 'usuario_dashboard.html', {'usuario_logado': usuario_logado,'imoveis_publicados':imoveis_publicados})


def perfil_usuario(request):
    usuario_logado = None
    if 'usuario' in request.session:
        try:
            usuario_logado = Usuario.objects.get(id=request.session['usuario'])
        except Usuario.DoesNotExist:
            return redirect('home')
        return render(request, 'perfil_usuario.html',{'usuario_logado':usuario_logado})
    else:
        return redirect('home')
        
    
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
    
    # Obtendo os parâmetros do formulário
    status_imovel = request.GET.get('status_imovel', '')
    tipo_imovel = request.GET.get('tipo_imovel', '')
    orcamento_imovel = request.GET.get('orcamento_imovel', '')
    localizacao_imovel = request.GET.get('localizacao_imovel', '')
    
    # Filtrando os imóveis
    imovel_venda = Imovel.objects.filter(apresentar=True)
    
    if status_imovel and status_imovel != "todos":
        imovel_venda = imovel_venda.filter(status=status_imovel)
    
    if tipo_imovel and tipo_imovel != "todos":
        imovel_venda = imovel_venda.filter(tipo=tipo_imovel)
    
    if orcamento_imovel:
        try:
            orcamento_valor = int(orcamento_imovel)
            imovel_venda = imovel_venda.filter(preco__lte=orcamento_valor)
        except ValueError:
            pass  # Caso o orçamento não seja um número válido, não aplicamos o filtro
    
    if localizacao_imovel:
        imovel_venda = imovel_venda.filter(endereco__icontains=localizacao_imovel)
    
    return render(request, 'casa_vender.html', {'imovel_venda': imovel_venda, 'usuario_logado': usuario_logado})


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
    corretores = Usuario.objects.filter(tipo_usuario='corretor')
    depoimentos = Depoimentos.objects.filter(apresentar=True,).order_by('data_cadastro')
    return render(request, 'Nossa_missao.html', {'depoimentos':depoimentos,'usuario_logado':usuario_logado})

def sobre(request):
    usuario_logado = None
    if 'usuario' in request.session:
        try:
            usuario_logado = Usuario.objects.get(id=request.session['usuario'])
        except Usuario.DoesNotExist:
            pass
    depoimentos = Depoimentos.objects.filter(apresentar=True,).order_by('data_cadastro')
    corretores = Usuario.objects.filter(tipo_usuario='corretor')
    return render(request, 'sobre.html', {'usuario_logado':usuario_logado, 'depoimentos':depoimentos, 'corretores':corretores})

def faq(request):
    usuario_logado = None
    if 'usuario' in request.session:
        try:
            usuario_logado = Usuario.objects.get(id=request.session['usuario'])
        except Usuario.DoesNotExist:
            pass
 
    return render(request, 'faq.html', {'usuario_logado':usuario_logado})

def servico(request):
    usuario_logado = None
    if 'usuario' in request.session:
        try:
            usuario_logado = Usuario.objects.get(id=request.session['usuario'])
        except Usuario.DoesNotExist:
            pass
 
    return render(request, 'servico.html', {'usuario_logado':usuario_logado})

def blog(request):
    usuario_logado = None
    if 'usuario' in request.session:
        try:
            usuario_logado = Usuario.objects.get(id=request.session['usuario'])
        except Usuario.DoesNotExist:
            pass
 
    return render(request, 'blog.html', {'usuario_logado':usuario_logado})

def contacto(request):
    usuario_logado = None
    if 'usuario' in request.session:
        try:
            usuario_logado = Usuario.objects.get(id=request.session['usuario'])
        except Usuario.DoesNotExist:
            pass
 
    return render(request, 'contact.html', {'usuario_logado':usuario_logado})

def equipe(request):
    usuario_logado = None
    if 'usuario' in request.session:
        try:
            usuario_logado = Usuario.objects.get(id=request.session['usuario'])
        except Usuario.DoesNotExist:
            pass
    corretores = Usuario.objects.filter(tipo_usuario='corretor')
    return render(request, 'nossa_equipe.html', {'usuario_logado':usuario_logado, 'corretores':corretores})

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

def nova_casa(request):
    usuario_logado = None
    if 'usuario' in request.session:
        try:
            usuario_logado = Usuario.objects.get(id=request.session['usuario'])
        except Usuario.DoesNotExist:
            pass
    status = request.GET.get('status')
    return render(request, 'cadastrar_imovel.html', {'usuario_logado': usuario_logado})

def cadastro_imovel(request):
    usuario_logado = None
    if 'usuario' in request.session:
        try:
            usuario_logado = Usuario.objects.get(id=request.session['usuario'])
        except Usuario.DoesNotExist:
            pass
    if request.method == 'POST':
        try:
            # Captura os dados do anunciante
            nome_anunciante = request.POST.get('nome_anunciante', '').strip()
            email_anunciante = request.POST.get('email_anunciante', '').strip()
            telefone_anunciante = request.POST.get('telefone_anunciante', '').strip()

            # Captura os dados do imóvel
            titulo = request.POST.get('titulo', '').strip()
            endereco = request.POST.get('endereco', '').strip()
            preco = request.POST.get('preco', '0').strip()
            tipo = request.POST.get('tipo', '').strip()
            status = request.POST.get('status', '').strip()
            descricao = request.POST.get('descricao', '').strip()
            area = request.POST.get('area', '0').strip()
            quartos = request.POST.get('quartos', '0').strip()
            banheiros = request.POST.get('banheiros', '0').strip()
            vagas_garagem = request.POST.get('vagas_garagem', '0').strip()
            video_url = request.POST.get('video', '').strip()

            # Captura das imagens
            imagem_principal = request.FILES.get('imagem_principal')
            imagens_secundarias = request.FILES.getlist('imagens_secundarias')

            # Conversão segura de valores numéricos
            area = float(area) if area.replace('.', '', 1).isdigit() else 0.0
            quartos = int(quartos) if quartos.isdigit() else 0
            banheiros = int(banheiros) if banheiros.isdigit() else 0
            vagas_garagem = int(vagas_garagem) if vagas_garagem.isdigit() else 0
            preco = float(preco) if preco.replace('.', '', 1).isdigit() else 0.0

            # Criando o imóvel
            imovel = Imovel.objects.create(
                usuario=usuario_logado,
                nome_anunciante=nome_anunciante,
                email_anunciante=email_anunciante,
                telefone_anunciante=telefone_anunciante,
                titulo=titulo,
                endereco=endereco,
                preco=preco,
                tipo=tipo,
                status=status,
                descricao=descricao,
                area=area,
                quartos=quartos,
                banheiros=banheiros,
                vagas_garagem=vagas_garagem,
                imagem=imagem_principal,
                video=video_url
            )

            dados_adicionais = DadosAdicionais.objects.create(
                imovel=imovel,
                interior_ar_condicionado=request.POST.get('interior_ar_condicionado') == 'on',
                interior_cozinha_equipada=request.POST.get('interior_cozinha_equipada') == 'on',
                interior_roupeiros_embutidos=request.POST.get('interior_roupeiros_embutidos') == 'on',
                exterior_varanda=request.POST.get('exterior_varanda') == 'on',
                exterior_piscina_coletiva=request.POST.get('exterior_piscina_coletiva') == 'on',
                exterior_estacionamento_privativo=request.POST.get('exterior_estacionamento_privativo') == 'on',
                exterior_churrasqueira=request.POST.get('exterior_churrasqueira') == 'on',
                exterior_campos_polidesportivos=request.POST.get('exterior_campos_polidesportivos') == 'on',
                seguranca_24h=request.POST.get('seguranca_24h') == 'on',
                reservatorio_agua=request.POST.get('reservatorio_agua') == 'on',
                ginasio=request.POST.get('ginasio') == 'on',
                gerador=request.POST.get('gerador') == 'on',
                area_servico=request.POST.get('area_servico') == 'on'
            )


            # Cadastro das imagens secundárias
            indexImagem = 0
            for imagem in imagens_secundarias:
                GaleriaImovel.objects.create(imovel=imovel, imagem=imagem)
 
            

            mensagem = f'Olá {nome_anunciante}!\n\nObrigado por publicar o seu imovel na Carhousy. Estamos felizes em tê-lo conosco!\n\nEstamos aqui para ajudar você a encontrar o melhor para o seu imovel.\n\nAtenciosamente,\nEquipe Carhousy'
            
            # Envio do e-mail
            send_mail(
                'Bem-vindo à Carhousy',  # Assunto
                mensagem,  # Corpo do e-mail com a mensagem personalizada
                settings.EMAIL_HOST_USER,  # Remetente
                [email_anunciante],  # Destinatário
                fail_silently=False,  # Caso ocorra algum erro, não falhar silenciosamente
            )
            
            messages.success(request, 'Imóvel cadastrado com sucesso! Brevemente entraremos em contacto')
            return redirect('cadastro_imovel')

        except Exception as e:
            messages.error(request, f'Nao foi possivel publicar o imovel')

    return render(request, 'cadastrar_imovel.html', {'usuario_logado': usuario_logado})

def imoveis_publicados(request):
    if 'usuario' in request.session:
        try:
            usuario_logado = Usuario.objects.get(id=request.session['usuario'])
        except Usuario.DoesNotExist:
            pass
        imoveis_publicados = Imovel.objects.filter(email_anunciante=usuario_logado.email,nome_anunciante=usuario_logado.nome,telefone_anunciante=usuario_logado.telefone).order_by('data_publicacao')
        return render(request, 'imoveis_publicados.html', {'usuario_logado': usuario_logado,'imoveis_publicados':imoveis_publicados})
    else:
        return redirect('home')
        


