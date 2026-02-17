# PDF DB API (Django REST Framework + PostgreSQL)

API REST para subir y almacenar archivos PDF **dentro de la base de datos PostgreSQL**, asociados a un usuario. Usa Django REST Framework con autenticación por token.

Características principales
- Registro de usuarios
- Autenticación por token
- Subida de PDFs (se guardan como bytes en PostgreSQL)
- Listado de PDFs del usuario autenticado
- Descarga de PDFs
- Eliminación de PDFs propios
- Administración en Django admin
- CORS habilitado para desarrollo
- Límite de tamaño de PDFs: **10 MB**

Cómo ejecutar (Docker)
1. Copia `.env.example` a `.env` si deseas modificar variables.
2. Levanta los servicios:
   docker-compose up --build
3. En otra terminal, crea migraciones y superusuario:
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py createsuperuser
4. API disponible en http://localhost:8000

Endpoints API
- POST `/api/register/` - Registrar nuevo usuario
  {
    "username": "usuario",
    "email": "user@example.com",
    "password": "password123",
    "password2": "password123"
  }

- POST `/api/login/` - Iniciar sesión
  {
    "username": "usuario",
    "password": "password123"
  }

- GET `/api/pdfs/` - Listar PDFs del usuario (requiere token)
- POST `/api/pdfs/upload/` - Subir PDF (requiere token, multipart/form-data con campo 'file')
- GET `/api/pdfs/<id>/` - Obtener detalles de un PDF (requiere token)
- DELETE `/api/pdfs/<id>/` - Eliminar un PDF (requiere token)
- GET `/api/pdfs/<id>/download/` - Descargar un PDF (requiere token)

Autenticación
Incluye el token en el header `Authorization: Token <tu_token>`

Comandos útiles (local sin Docker)
- python -m venv .venv
- pip install -r requirements.txt
- python manage.py migrate
- python manage.py createsuperuser
- python manage.py runserver

Configuración

CORS
- Por defecto, CORS está habilitado para `localhost:3000` y `localhost:8000` (desarrollo).
- Modifica `CORS_ALLOWED_ORIGINS` en [pdfdb_project/settings.py](pdfdb_project/settings.py) para permitir otros orígenes.

Límite de tamaño
- El límite máximo de PDFs es **10 MB** (configurable en `MAX_UPLOAD_PDF_SIZE` en [pdfdb_project/settings.py](pdfdb_project/settings.py)).
- Para cambiar: `MAX_UPLOAD_PDF_SIZE = 20 * 1024 * 1024  # 20 MB`

Notas
- Archivos PDF se guardan en la tabla `pdfs_pdf` en la columna `data` (tipo bytea).
- La validación de tamaño ocurre en el serializador; archivos que excedan el límite rechazarán con error 400.
- Esta configuración es para desarrollo/propósito educativo. Para producción ajustar SECRET_KEY, DEBUG y CORS headers si es necesario.
