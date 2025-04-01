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

echo "2. Installing core dependencies first..."
pip install Django==4.2.8 dj-database-url==2.3.0

echo "3. Installing remaining dependencies..."
pip install -r requirements.txt

echo "4. Verifying installations..."
python -c "
import django; print(f'Django {django.__version__} installed')
import dj_database_url; print('dj-database-url installed')
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