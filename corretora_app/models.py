from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Vendedor(models.Model):
    nome = models.CharField(max_length=255)
    senha = models.CharField(max_length=100)
    bi = models.CharField(max_length=18, unique=True)
    endereco = models.CharField(max_length=255)
    telefone = models.CharField(max_length=15)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()

    def __str__(self):
        return self.nome

class Corretor(models.Model):
    nome = models.CharField(max_length=255)
    imagem = models.ImageField(upload_to='imoveis/', verbose_name="imagem corretor")
    senha = models.CharField(max_length=100)
    codigo = models.CharField(max_length=18, unique=True)
    endereco = models.CharField(max_length=255)
    telefone = models.CharField(max_length=15)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()

    def __str__(self):
        return self.nome


class Parceiro(models.Model):
    TIPO_PARCEIRO = [
        ('imobiliaria', 'Imobiliária'),
        ('financiamento', 'Financiamento'),
        ('servicos', 'Serviços'),
        ('outros', 'Outros'),
    ]

    nome = models.CharField(max_length=255)
    tipo_parceiro = models.CharField(max_length=20, choices=TIPO_PARCEIRO)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    endereco = models.CharField(max_length=255)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome} - {self.get_tipo_parceiro_display()}"




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
    
    vendedor = models.ForeignKey('Vendedor', on_delete=models.SET_NULL, null=True, blank=True)
    
    status = models.CharField(max_length=40, choices=STATUS_IMOVEL)

    def __str__(self):
        return f"{self.tipo.title()} - {self.endereco} - {self.status.title()}"

    def preco_formatado(self):
        """Retorna o preço formatado como moeda brasileira."""
        return f"R${self.preco:,.2f}"

    def area_formatada(self):
        """Retorna a área formatada com unidades."""
        return f"{self.area} m²"

    def imagens(self):
        """Retorna todas as imagens do imóvel."""
        return self.imagens.all()


class ImagemImovel(models.Model):
    imovel = models.ForeignKey('Imovel', related_name='imagens', on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='imoveis/', verbose_name="Imagem do Imóvel")
    descricao = models.CharField(max_length=255, blank=True, null=True, verbose_name="Descrição da Imagem")
    data_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Imagem do imóvel {self.imovel.endereco}"

    def imagem_url(self):
        """Retorna a URL da imagem"""
        return self.imagem.url if self.imagem else None




class Contrato(models.Model):
    TIPO_CONTRATO = [
        ('compra', 'Compra'),
        ('venda', 'Venda'),
        ('aluguel', 'Aluguel'),
    ]

    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE, related_name='contratos')
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    corretor = models.ForeignKey('Corretor', on_delete=models.SET_NULL, null=True)
    tipo_contrato = models.CharField(max_length=10, choices=TIPO_CONTRATO)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, default='ativo')  # Ativo, encerrado, etc.
    observacoes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Contrato de {self.tipo_contrato} - {self.imovel.endereco}"


class Agendamento(models.Model):
    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data_agendada = models.DateTimeField()
    status = models.CharField(max_length=10, choices=[('agendado', 'Agendado'), ('realizado', 'Realizado'), ('cancelado', 'Cancelado')])
    observacoes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Visita ao imóvel {self.imovel.endereco} - {self.cliente.nome}"

class Favorito(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE)
    data_favorito = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cliente', 'imovel')  # Garante que o cliente não pode favoritar o mesmo imóvel mais de uma vez

    def __str__(self):
        return f"{self.cliente.nome} - {self.imovel.endereco}"


class Avaliacao(models.Model):
    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE, null=True, blank=True)
    corretor = models.ForeignKey(Corretor, on_delete=models.CASCADE, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    nota = models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    comentario = models.TextField(blank=True, null=True)
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avaliação de {self.cliente.nome} - {self.nota} estrelas"


class Localizacao(models.Model):
    imovel = models.OneToOneField(Imovel, on_delete=models.CASCADE)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.bairro} - {self.cidade}/{self.estado}"

class Anuncio(models.Model):
    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE)
    data_publicacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('ativo', 'Ativo'), ('inativo', 'Inativo')])

    def __str__(self):
        return f"Anúncio do imóvel {self.imovel.endereco} - {self.status}"


class DocumentoImovel(models.Model):
    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE)
    tipo_documento = models.CharField(max_length=100, choices=[('escritura', 'Escritura'), ('iptu', 'IPTU'), ('alvara', 'Alvará')])
    arquivo = models.FileField(upload_to='documentos_imoveis/')
    data_envio = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.tipo_documento} - {self.imovel.endereco}"


class Comissao(models.Model):
    corretor = models.ForeignKey(Corretor, on_delete=models.CASCADE)
    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE)
    valor_comissao = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=50, choices=[('venda', 'Venda'), ('aluguel', 'Aluguel')])
    data_pagamento = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Comissão {self.corretor.nome} - {self.valor_comissao} no imóvel {self.imovel.endereco}"

class RelatorioVendas(models.Model):
    corretor = models.ForeignKey(Corretor, on_delete=models.CASCADE)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    total_vendas = models.DecimalField(max_digits=10, decimal_places=2)
    total_imoveis_vendidos = models.IntegerField()
    
    def __str__(self):
        return f"Relatório de Vendas do Corretor {self.corretor.nome} - {self.total_imoveis_vendidos} Imóveis Vendidos"

class FeedbackCliente(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    corretor = models.ForeignKey(Corretor, on_delete=models.CASCADE, null=True, blank=True)
    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE, null=True, blank=True)
    nota = models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    comentario = models.TextField()
    data_feedback = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Feedback de {self.cliente.nome} - {self.nota} estrelas"
