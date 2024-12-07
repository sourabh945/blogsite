#!/usr/bin/env bash
# Exit on error
set -o errexit


# Install project dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

python manage.py makemigrations core

# Run Django migrations
echo "Running Django migrations..."
python manage.py migrate

# Collect static files (if applicable)
echo "Collecting static files..."
python manage.py collectstatic --noinput




