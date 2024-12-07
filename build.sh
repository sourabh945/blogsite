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

# Start the Django development server (optional, for local dev environment)
echo "Starting Django development server..."
python manage.py runserver &

# Start the Celery worker
echo "Starting Celery worker..."
celery -A your_project_name worker --loglevel=info &

# Optionally, you can also start the Celery beat scheduler if you need periodic tasks
# echo "Starting Celery beat scheduler..."
# celery -A your_project_name beat --loglevel=info &

# Wait for background processes to finish (you can change this logic depending on your deployment setup)
wait


