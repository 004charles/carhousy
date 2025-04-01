#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "----- Starting Build Process -----"

# Activate virtual environment (if exists)
if [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
fi

echo "1. Updating pip..."
pip install --upgrade pip

# In your build.sh, add this after pip upgrade:
echo "Resolving dependency conflicts..."
pip install --upgrade --force-reinstall -r requirements.txt

echo "2. Installing dependencies..."
pip install -r requirements.txt

echo "3. Verifying Django installation..."
if ! python -c "import django; print(f'Django version: {django.__version__}')"; then
    echo "Django not found! Installing Django..."
    pip install django
fi

echo "4. Checking database connection..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carhouse_projecto.settings')
import django
django.setup()
from django.db import connection
connection.ensure_connection()
print('Database connection established!')
"

echo "5. Applying database migrations..."
python manage.py migrate

echo "6. Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "7. Creating superuser if needed..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model() 
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created!')
else:
    print('Superuser already exists')
"

echo "----- Build Completed Successfully -----"