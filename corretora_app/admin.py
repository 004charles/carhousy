from django.contrib import admin
from .models import (
    Usuario, Imovel, DadosAdicionais, GaleriaImovel, Contrato, Agendamento, Favorito, Avaliacao,
    Localizacao, DocumentoImovel, Comissao, RelatorioVendas, FeedbackCliente, Proposta, Visita, Pagamento
)

# Registrando os modelos no admin com ícones
admin.site.register(Usuario, icon='fas fa-user')
admin.site.register(Imovel, icon='fas fa-home')
admin.site.register(DadosAdicionais, icon='fas fa-cogs')
admin.site.register(GaleriaImovel, icon='fas fa-images')
admin.site.register(Contrato, icon='fas fa-file-contract')
admin.site.register(Agendamento, icon='fas fa-calendar-check')
admin.site.register(Favorito, icon='fas fa-heart')
admin.site.register(Avaliacao, icon='fas fa-star')
admin.site.register(Localizacao, icon='fas fa-map-marker-alt')
admin.site.register(DocumentoImovel, icon='fas fa-file')
admin.site.register(Comissao, icon='fas fa-percent')
admin.site.register(RelatorioVendas, icon='fas fa-chart-line')
admin.site.register(FeedbackCliente, icon='fas fa-comment-dots')
admin.site.register(Proposta, icon='fas fa-handshake')
admin.site.register(Visita, icon='fas fa-search-location')
admin.site.register(Pagamento, icon='fas fa-credit-card')
