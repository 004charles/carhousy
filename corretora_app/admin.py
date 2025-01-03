from django.contrib import admin

from django.contrib import admin
from .models import Cliente, Vendedor, Corretor, Parceiro, Imovel, ImagemImovel, Contrato, Agendamento, Favorito, Avaliacao, Localizacao, Anuncio, DocumentoImovel, Comissao, RelatorioVendas, FeedbackCliente

# Registrar os modelos
admin.site.register(Cliente)
admin.site.register(Vendedor)
admin.site.register(Corretor)
admin.site.register(Parceiro)
admin.site.register(Imovel)
admin.site.register(ImagemImovel)
admin.site.register(Contrato)
admin.site.register(Agendamento)
admin.site.register(Favorito)
admin.site.register(Avaliacao)
admin.site.register(Localizacao)
admin.site.register(Anuncio)
admin.site.register(DocumentoImovel)
admin.site.register(Comissao)
admin.site.register(RelatorioVendas)
admin.site.register(FeedbackCliente)

