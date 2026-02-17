# PDF DB (Django + PostgreSQL)

Aplicación Django mínima para subir y almacenar archivos PDF **dentro de la base de datos PostgreSQL**, asociados a un usuario. Usa Bootstrap para el frontend y viene con `Dockerfile` + `docker-compose.yml`.

Características principales
- Usuarios (registro / login)
- Subida de PDFs (se guardan como bytes en PostgreSQL)
- Lista de PDFs por usuario
- Descarga de PDFs

Cómo ejecutar (Docker)
1. Copia `.env.example` a `.env` si deseas modificar variables.
2. Levanta los servicios:
   docker-compose up --build
3. En otra terminal, crea migraciones y superusuario (si no usas el contenedor `web` execute desde dentro del contenedor):
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py createsuperuser
4. Abrir http://localhost:8000

Comandos útiles (local sin Docker)
- python -m venv .venv
- pip install -r requirements.txt
- python manage.py migrate
- python manage.py runserver

Notas
- Archivos PDF se guardan en la tabla `pdfs_pdf` en la columna `data` (tipo bytea).
- Esta configuración es para desarrollo/propósito educativo. Para producción ajustar SECRET_KEY, DEBUG, seguridad y servir archivos estáticos correctamente.
