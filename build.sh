#!/bin/bash
set -e

echo "----- Starting Build Process -----"

# Download SSL certificate
echo "1. Downloading SSL certificate..."
curl -o prod-ca-2021.crt https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem

# Activate virtual environment
if [ -d ".venv" ]; then
    echo "2. Activating virtual environment..."
    source .venv/bin/activate
fi

echo "3. Updating pip..."
pip install --upgrade pip

echo "4. Installing dependencies..."
pip install -r requirements.txt

echo "5. Waiting for database to be ready..."
for i in {1..10}; do
    python << END
import os
import time
import psycopg2
from psycopg2 import OperationalError

try:
    conn = psycopg2.connect(
        dbname="dbcarhousy",
        user="dbcarhousy_user",
        password="l6vlIDabb2yL2HB8pzZqi5yGuEyVLTum",
        host="dpg-cvlgli8dl3ps73eg4kfg-a",
        port="5432",
        sslmode="require",
        sslrootcert="prod-ca-2021.crt"
    )
    conn.close()
    print("✓ Database connection established")
    exit(0)
except OperationalError as e:
    print(f"! Database connection failed (attempt {i}/10): {e}")
    if i == 10:
        exit(1)
    time.sleep(5)
END
if [ $? -eq 0 ]; then
    break
fi
done

echo "6. Applying migrations..."
python manage.py migrate

echo "7. Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "8. Creating superuser if needed..."
if [ "$CREATE_SUPERUSER" = "True" ]; then
    python manage.py createsuperuser \
        --noinput \
        --username "$DJANGO_SUPERUSER_USERNAME" \
        --email "$DJANGO_SUPERUSER_EMAIL" || true
fi

echo "----- Build Completed Successfully -----"