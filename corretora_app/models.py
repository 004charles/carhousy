from django.db import models
from django.db import models
from django.core.exceptions import ValidationError

class Usuario(models.Model):
    nome = models.CharField(max_length=255)
    sobrenome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    endereco = models.CharField(max_length=255)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    imagem = models.ImageField(upload_to='imoveis/', verbose_name="Imagem Corretor", blank=True, null=True)
    codigo = models.CharField(max_length=18, unique=True, blank=True, null=True)
    
    TIPO_USUARIO_CHOICES = [
        ('cliente', 'Cliente'),
        ('vendedor', 'Vendedor'),
        ('corretor', 'Corretor'),
        ('empresa', 'Empresa'),
    ]

    tipo_usuario = models.CharField(max_length=10, choices=TIPO_USUARIO_CHOICES)

    def __str__(self):
        return f"{self.nome} {self.sobrenome} ({self.tipo_usuario})"


# Model para representar imagens adicionais (galeria)
class ImagemAdicional(models.Model):
    imagem = models.ImageField(upload_to='imoveis/galeria/', verbose_name="Imagem Adicional")
    descricao = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.descricao if self.descricao else "Imagem Adicional"

# Model para representar os imóveis
class Imovel(models.Model):
    TIPO_IMOVEL = [
        ('casa', 'Casa'),
        ('apartamento', 'Apartamento'),
        ('terreno', 'Terreno'),
        ('comercial', 'Imóvel Comercial'),
        ('escritorio', 'Escritório'),
    ]
    STATUS_IMOVEL = [
        ('venda', 'Venda'),
        ('aluguel', 'Aluguel'),
        ('vendido', 'Vendido'),
        ('indisponivel', 'Indisponível'),
    ]
    
    titulo = models.CharField(max_length=255, verbose_name="Título", blank=True, null=True)
    imagem = models.ImageField(upload_to='imoveis/', verbose_name="Imagem Principal do Imóvel", blank=True, null=True)
    endereco = models.CharField(max_length=255)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=20, choices=TIPO_IMOVEL)
    descricao = models.TextField()
    area = models.DecimalField(max_digits=6, decimal_places=2, help_text="Área total do imóvel em metros quadrados")
    
    quartos = models.IntegerField(blank=True, null=True)
    banheiros = models.IntegerField(blank=True, null=True)
    vagas_garagem = models.IntegerField(blank=True, null=True)
    
    data_publicacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=40, choices=STATUS_IMOVEL)
    
    vendedor = models.ForeignKey(
        'Usuario', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        limit_choices_to={'tipo_usuario': 'vendedor'},
        related_name='imoveis_vendidos'
    )
    corretores = models.ManyToManyField(
        'Usuario', 
        limit_choices_to={'tipo_usuario': 'corretor'},
        related_name='imoveis'
    )
    
    video = models.URLField(max_length=500, blank=True, null=True, verbose_name="URL do vídeo")

    imagens_adicionais = models.ManyToManyField(
        'ImagemAdicional',
        blank=True,
        related_name='imoveis'
    )
    
    def clean(self):
        if self.tipo == 'escritorio':
            if self.quartos is not None and self.quartos > 0:
                raise ValidationError({'quartos': 'Escritórios não podem ter quartos.'})
            if self.banheiros is not None and self.banheiros > 0:
                raise ValidationError({'banheiros': 'Escritórios não podem ter banheiros.'})
            if self.vagas_garagem is not None and self.vagas_garagem > 0:
                raise ValidationError({'vagas_garagem': 'Escritórios não podem ter vagas de garagem.'})

    def __str__(self):
        return f"{self.tipo.title()} - {self.endereco} - {self.status.title()}"

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)



# Model para galeria de imagens de imóveis
class GaleriaImovel(models.Model):
    imovel = models.ForeignKey(
        Imovel,
        on_delete=models.CASCADE,
        related_name='galeria'
    )
    imagem = models.ImageField(upload_to='imoveis/galeria/', verbose_name="Imagem da Galeria")
    descricao = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Galeria de {self.imovel.tipo.title()} - {self.imovel.endereco}"


class DadosAdicionais(models.Model):
    imovel = models.OneToOneField(
        Imovel,
        on_delete=models.CASCADE,
        related_name="dados"  # Relacionamento reverso
    )
    exterior_varanda = models.BooleanField(default=False)
    exterior_piscina_coletiva = models.BooleanField(default=False)
    exterior_estacionamento_privativo = models.BooleanField(default=False)
    exterior_churrasqueira = models.BooleanField(default=False)
    exterior_campos_polidesportivos = models.BooleanField(default=False)

    interior_suites = models.IntegerField(default=0)  # Número de suítes
    interior_roupeiros_embutidos = models.BooleanField(default=False)
    interior_cozinha_equipada = models.BooleanField(default=False)
    interior_ar_condicionado = models.BooleanField(default=False)

    segurança_24h = models.BooleanField(default=False)
    reservatorio_agua = models.BooleanField(default=False)
    ginásio = models.BooleanField(default=False)
    gerador = models.BooleanField(default=False)
    area_servico = models.BooleanField(default=False)  # Área de serviço/lavandaria

    def __str__(self):
        return f"Dados adicionais de {self.imovel.tipo.title()} - {self.imovel.endereco}"


class GaleriaImovel(models.Model):
    imovel = models.ForeignKey('Imovel', on_delete=models.CASCADE, related_name='galeria')
    imagem = models.ImageField(upload_to='imoveis/galeria/')
    descricao = models.CharField(max_length=255, blank=True, null=True)



class Contrato(models.Model):
    TIPO_CONTRATO = [
        ('compra', 'Compra'),
        ('venda', 'Venda'),
        ('aluguel', 'Aluguel'),
    ]
    imovel = models.ForeignKey('Imovel', on_delete=models.CASCADE, related_name='contratos')
    cliente = models.ForeignKey('Usuario', on_delete=models.CASCADE, limit_choices_to={'tipo_usuario': 'cliente'}, related_name='contratos_cliente')
    corretor = models.ForeignKey('Usuario', on_delete=models.SET_NULL, null=True, limit_choices_to={'tipo_usuario': 'corretor'}, related_name='contratos_corretor')
    tipo_contrato = models.CharField(max_length=10, choices=TIPO_CONTRATO)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, default='ativo')
    observacoes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Contrato de {self.tipo_contrato} - {self.imovel.endereco}"

class Agendamento(models.Model):
    imovel = models.ForeignKey('Imovel', on_delete=models.CASCADE, related_name='agendamentos')
    cliente = models.ForeignKey('Usuario', on_delete=models.CASCADE, limit_choices_to={'tipo_usuario': 'cliente'}, related_name='agendamentos_cliente')
    data_hora_agendada = models.DateTimeField()  # Armazena data e hora juntos
    status = models.CharField(max_length=10, choices=[('agendado', 'Agendado'), ('cancelado', 'Cancelado')])
    mensagem = models.TextField()

    def __str__(self):
        return f'Agendamento para {self.imovel} em {self.data_hora_agendada}'

class Favorito(models.Model):
    cliente = models.ForeignKey('Usuario', on_delete=models.CASCADE, limit_choices_to={'tipo_usuario': 'cliente'}, related_name='favoritos_cliente')
    imovel = models.ForeignKey('Imovel', on_delete=models.CASCADE, related_name='favoritos_imovel')
    data_favorito = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cliente', 'imovel')


    def __str__(self):
        return f"{self.cliente.nome} - {self.imovel.endereco}"


class Avaliacao(models.Model):
    imovel = models.ForeignKey('Imovel', on_delete=models.CASCADE, null=True, blank=True, related_name='avaliacoes_imovel')
    corretor = models.ForeignKey('Usuario', on_delete=models.CASCADE, null=True, blank=True, limit_choices_to={'tipo_usuario': 'corretor'}, related_name='avaliacoes_corretor')
    cliente = models.ForeignKey('Usuario', on_delete=models.CASCADE, limit_choices_to={'tipo_usuario': 'cliente'}, related_name='avaliacoes_cliente')
    nota = models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    comentario = models.TextField(blank=True, null=True)
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avaliação de {self.cliente.nome} - {self.nota} estrelas"

class Localizacao(models.Model):
    imovel = models.OneToOneField('Imovel', on_delete=models.CASCADE, related_name='localizacao_imovel')
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.bairro} - {self.cidade}/{self.estado}"

class DocumentoImovel(models.Model):
    imovel = models.ForeignKey('Imovel', on_delete=models.CASCADE, related_name='documentos_imovel')
    tipo_documento = models.CharField(max_length=100, choices=[('escritura', 'Escritura'), ('iptu', 'IPTU'), ('alvara', 'Alvará')])
    arquivo = models.FileField(upload_to='documentos_imoveis/')
    data_envio = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.tipo_documento} - {self.imovel.endereco}"

class Comissao(models.Model):
    corretor = models.ForeignKey('Usuario', on_delete=models.CASCADE, limit_choices_to={'tipo_usuario': 'corretor'}, related_name='comissoes_corretor')
    imovel = models.ForeignKey('Imovel', on_delete=models.CASCADE, related_name='comissoes_imovel')
    valor_comissao = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=50, choices=[('venda', 'Venda'), ('aluguel', 'Aluguel')])
    data_pagamento = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Comissão {self.corretor.nome} - {self.valor_comissao} no imóvel {self.imovel.endereco}"

class RelatorioVendas(models.Model):
    corretor = models.ForeignKey('Usuario', on_delete=models.CASCADE, limit_choices_to={'tipo_usuario': 'corretor'}, related_name='relatorios_vendas_corretor')
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    total_vendas = models.DecimalField(max_digits=10, decimal_places=2)
    total_imoveis_vendidos = models.IntegerField()
    
    def __str__(self):
        return f"Relatório de Vendas do Corretor {self.corretor.nome} - {self.total_imoveis_vendidos} Imóveis Vendidos"

class FeedbackCliente(models.Model):
    cliente = models.ForeignKey('Usuario', on_delete=models.CASCADE, limit_choices_to={'tipo_usuario': 'cliente'}, related_name='feedbacks_cliente')
    corretor = models.ForeignKey('Usuario', on_delete=models.CASCADE, null=True, blank=True, limit_choices_to={'tipo_usuario': 'corretor'}, related_name='feedbacks_corretor')
    imovel = models.ForeignKey('Imovel', on_delete=models.CASCADE, null=True, blank=True, related_name='feedbacks_imovel')
    nota = models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    comentario = models.TextField(blank=True, null=True)
    data_feedback = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback do Cliente {self.cliente.nome} - {self.nota} estrelas"


#---------------------------novo---------------------------------------------

# Modelo de Proposta de Aluguel
class Proposta(models.Model):
    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE)
    locatario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    valor_ofertado = models.DecimalField(max_digits=10, decimal_places=2)
    data_envio = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=15,
        choices=[('pendente', 'Pendente'), ('aceita', 'Aceita'), ('recusada', 'Recusada')],
        default='pendente'
    )

# Modelo de Visitas
class Visita(models.Model):
    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE)
    locatario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data_horario = models.DateTimeField()
    status = models.CharField(
        max_length=15,
        choices=[('pendente', 'Pendente'), ('confirmada', 'Confirmada'), ('cancelada', 'Cancelada')],
        default='pendente'
    )

# Modelo de Contratos
class Contrato(models.Model):
    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE)
    locatario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)
    valor_mensal = models.DecimalField(max_digits=10, decimal_places=2)
    ativo = models.BooleanField(default=True)


# Modelo de Pagamentos
class Pagamento(models.Model):
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    data_pagamento = models.DateTimeField(auto_now_add=True)
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2)
    forma_pagamento = models.CharField(
        max_length=50, choices=[('boleto', 'Boleto'), ('cartao', 'Cartão'), ('pix', 'Pix')]
    )
    status = models.CharField(
        max_length=15, choices=[('pendente', 'Pendente'), ('pago', 'Pago'), ('falhou', 'Falhou')],
        default='pendente'
    )

    def __str__(self):
        return f"Pagamento de {self.valor_pago} para o contrato {self.contrato.id} em {self.data_pagamento}"


# Modelo de Manutenções
class SolicitacaoManutencao(models.Model):
    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE)
    locatario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    descricao = models.TextField()
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=15,
        choices=[('pendente', 'Pendente'), ('em andamento', 'Em andamento'), ('concluida', 'Concluída')],
        default='pendente'
    )

# Modelo de Notificações
class Notificacao(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    mensagem = models.TextField()
    lida = models.BooleanField(default=False)
    data_envio = models.DateTimeField(auto_now_add=True)

# Modelo de Simulação de Financiamento
class SimulacaoFinanciamento(models.Model):
    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    valor_entrada = models.DecimalField(max_digits=10, decimal_places=2)
    parcelas = models.IntegerField()
    taxa_juros = models.FloatField()
    valor_final = models.DecimalField(max_digits=10, decimal_places=2)

# Modelo de Participação em Leilões
class Leilao(models.Model):
    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    lance_inicial = models.DecimalField(max_digits=10, decimal_places=2)

class Lance(models.Model):
    leilao = models.ForeignKey(Leilao, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_lance = models.DateTimeField(auto_now_add=True)




class Publicidade_home(models.Model):
    titulo = models.CharField(max_length=255)  
    descricao = models.TextField() 
    video = models.FileField(upload_to='videos/publicidade_home/', null=True, blank=True) 

    def __str__(self):
        return self.titulo


class HoraAgendamento(models.Model):
    hora = models.TimeField()

    def __str__(self):
        return str(self.hora)