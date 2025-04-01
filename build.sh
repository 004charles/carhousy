#!/bin/bash
set -e

echo "----- Iniciando Processo de Build -----"

# Ativar ambiente virtual (se existir)
if [ -d ".venv" ]; then
    echo "Ativando ambiente virtual..."
    source .venv/bin/activate
fi

echo "1. Atualizando pip..."
pip install --upgrade pip

echo "2. Instalando dependências..."
pip install -r requirements.txt

echo "3. Aplicando migrações..."
python manage.py migrate

echo "4. Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --clear

echo "5. Criando superusuário se necessário..."
if [ "$CREATE_SUPERUSER" = "True" ]; then
    python manage.py createsuperuser \
        --noinput \
        --username "$DJANGO_SUPERUSER_USERNAME" \
        --email "$DJANGO_SUPERUSER_EMAIL" || true
fi

echo "----- Build concluído com sucesso! -----"