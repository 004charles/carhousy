from django.contrib import admin
from .models import Usuario, Imovel, Contrato, Agendamento, Favorito, Avaliacao, Localizacao, DocumentoImovel, Comissao, RelatorioVendas, FeedbackCliente

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sobrenome', 'email', 'telefone', 'tipo_usuario', 'data_cadastro')
    search_fields = ('nome', 'sobrenome', 'email', 'telefone')
    list_filter = ('tipo_usuario', 'data_cadastro')
    ordering = ('-data_cadastro',)
    list_per_page = 10

class ImovelAdmin(admin.ModelAdmin):
    list_display = ('endereco', 'preco', 'tipo', 'status', 'vendedor', 'corretor', 'data_publicacao')
    search_fields = ('endereco', 'preco', 'tipo', 'status')
    list_filter = ('tipo', 'status', 'vendedor', 'corretor')
    ordering = ('-data_publicacao',)
    list_per_page = 10

class ContratoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'imovel', 'tipo_contrato', 'valor', 'data_inicio', 'data_fim', 'status')
    search_fields = ('cliente__nome', 'imovel__endereco', 'tipo_contrato')
    list_filter = ('tipo_contrato', 'status', 'data_inicio')
    ordering = ('-data_inicio',)
    list_per_page = 10

class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'imovel', 'data_agendada', 'status')
    search_fields = ('cliente__nome', 'imovel__endereco', 'status')
    list_filter = ('status', 'data_agendada')
    ordering = ('-data_agendada',)
    list_per_page = 10

class FavoritoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'imovel', 'data_favorito')
    search_fields = ('cliente__nome', 'imovel__endereco')
    ordering = ('-data_favorito',)
    list_per_page = 10

class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'corretor', 'imovel', 'nota', 'data_avaliacao')
    search_fields = ('cliente__nome', 'corretor__nome', 'imovel__endereco')
    list_filter = ('nota', 'data_avaliacao')
    ordering = ('-data_avaliacao',)
    list_per_page = 10

class LocalizacaoAdmin(admin.ModelAdmin):
    list_display = ('imovel', 'bairro', 'cidade', 'estado')
    search_fields = ('imovel__endereco', 'bairro', 'cidade', 'estado')
    list_filter = ('cidade', 'estado')
    list_per_page = 10

class DocumentoImovelAdmin(admin.ModelAdmin):
    list_display = ('imovel', 'tipo_documento', 'arquivo', 'data_envio')
    search_fields = ('imovel__endereco', 'tipo_documento')
    list_filter = ('tipo_documento', 'data_envio')
    ordering = ('-data_envio',)
    list_per_page = 10

class ComissaoAdmin(admin.ModelAdmin):
    list_display = ('corretor', 'imovel', 'valor_comissao', 'tipo', 'data_pagamento')
    search_fields = ('corretor__nome', 'imovel__endereco', 'tipo')
    list_filter = ('tipo', 'data_pagamento')
    ordering = ('-data_pagamento',)
    list_per_page = 10

class RelatorioVendasAdmin(admin.ModelAdmin):
    list_display = ('corretor', 'data_inicio', 'data_fim', 'total_vendas', 'total_imoveis_vendidos')
    search_fields = ('corretor__nome', 'data_inicio', 'data_fim')
    list_filter = ('data_inicio', 'data_fim')
    ordering = ('-data_inicio',)
    list_per_page = 10

class FeedbackClienteAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'corretor', 'imovel', 'nota', 'data_feedback')
    search_fields = ('cliente__nome', 'corretor__nome', 'imovel__endereco')
    list_filter = ('nota', 'data_feedback')
    ordering = ('-data_feedback',)
    list_per_page = 10

# Registrando as classes do Admin
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Imovel, ImovelAdmin)
admin.site.register(Contrato, ContratoAdmin)
admin.site.register(Agendamento, AgendamentoAdmin)
admin.site.register(Favorito, FavoritoAdmin)
admin.site.register(Avaliacao, AvaliacaoAdmin)
admin.site.register(Localizacao, LocalizacaoAdmin)
admin.site.register(DocumentoImovel, DocumentoImovelAdmin)
admin.site.register(Comissao, ComissaoAdmin)
admin.site.register(RelatorioVendas, RelatorioVendasAdmin)
admin.site.register(FeedbackCliente, FeedbackClienteAdmin)
