#!/bin/bash
set -e

echo "Applying database migrations..."
python manage.py migrate

echo "Starting Gunicorn server..."
# gunicorn pdfdb_project.wsgi:application --bind 0.0.0.0:8000 --workers 4 --worker-class sync --timeout 120
gunicorn pdfdb_project.wsgi:application --bind 0.0.0.0:8000
