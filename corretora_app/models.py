from django.db import models


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
    ]

    tipo_usuario = models.CharField(max_length=10, choices=TIPO_USUARIO_CHOICES)

    def __str__(self):
        return f"{self.nome} {self.sobrenome} ({self.tipo_usuario})"


class Imovel(models.Model):
    TIPO_IMOVEL = [
        ('casa', 'Casa'),
        ('apartamento', 'Apartamento'),
        ('terreno', 'Terreno'),
        ('comercial', 'Imóvel Comercial'),
    ]
    STATUS_IMOVEL = [
        ('venda', 'Venda'),
        ('aluguel', 'Aluguel'),
        ('vendido', 'Vendido'),
        ('indisponivel', 'Indisponível'),
    ]
    endereco = models.CharField(max_length=255)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=20, choices=TIPO_IMOVEL)
    descricao = models.TextField()
    area = models.DecimalField(max_digits=6, decimal_places=2, help_text="Área total do imóvel em metros quadrados")
    quartos = models.IntegerField()
    banheiros = models.IntegerField()
    vagas_garagem = models.IntegerField()
    data_publicacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=40, choices=STATUS_IMOVEL)
    vendedor = models.ForeignKey('Usuario', on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'tipo_usuario': 'vendedor'}, related_name='imoveis_vendidos')
    corretor = models.ForeignKey('Usuario', on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'tipo_usuario': 'corretor'}, related_name='imoveis_corretor')

    def __str__(self):
        return f"{self.tipo.title()} - {self.endereco} - {self.status.title()}"

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
    data_agendada = models.DateTimeField()
    status = models.CharField(max_length=10, choices=[('agendado', 'Agendado'), ('realizado', 'Realizado'), ('cancelado', 'Cancelado')])
    observacoes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Visita ao imóvel {self.imovel.endereco} - {self.cliente.nome}"

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
