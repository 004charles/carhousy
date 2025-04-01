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

echo "3. Checking database connection..."
python << END
import os
import time
from django.db import connection
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carhouse_projecto.settings')
import django
django.setup()

max_retries = 5
retry_delay = 5

for i in range(max_retries):
    try:
        connection.ensure_connection()
        print("✓ Database connection established")
        break
    except Exception as e:
        if i == max_retries - 1:
            raise e
        print(f"! Database connection failed (attempt {i+1}/{max_retries}), retrying...")
        time.sleep(retry_delay)
END

echo "4. Applying migrations..."
python manage.py migrate

echo "5. Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "6. Creating superuser if needed..."
if [ "$CREATE_SUPERUSER" = "True" ]; then
    python manage.py createsuperuser \
        --noinput \
        --username "$DJANGO_SUPERUSER_USERNAME" \
        --email "$DJANGO_SUPERUSER_EMAIL" || true
fi

echo "----- Build Completed Successfully -----"