FROM python:3.11-slim

LABEL org.opencontainers.image.source=https://github.com/JulianMagnabosco/pdfs-django

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# system deps required by psycopg2
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

# collect static (safe in build stage for this project)
RUN python manage.py collectstatic --noinput || true

EXPOSE 8000
CMD ["gunicorn", "pdfdb_project.wsgi:application", "--bind", "0.0.0.0:8000"]
