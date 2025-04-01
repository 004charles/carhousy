#!/bin/bash
set -e

echo "----- Starting Build Process -----"

# Activate virtual environment
if [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
fi

echo "1. Updating pip..."
pip install --upgrade pip

echo "2. Installing dependencies..."
pip install -r requirements.txt

echo "3. Applying migrations..."
python manage.py migrate

echo "4. Collecting static files..."
python manage.py collectstatic --noinput --clear --ignore *.map

echo "5. Creating superuser if needed..."
if [ "$CREATE_SUPERUSER" = "True" ]; then
    python manage.py createsuperuser \
        --noinput \
        --username "$DJANGO_SUPERUSER_USERNAME" \
        --email "$DJANGO_SUPERUSER_EMAIL" || true
fi

echo "----- Build Completed Successfully -----"