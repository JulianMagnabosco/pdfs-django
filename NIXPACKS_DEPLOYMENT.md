# Nixpacks - Guía de Despliegue

Este proyecto incluye configuración Nixpacks para desplegar en plataformas como **Render**, **Railway**, **Heroku** y otras que soporten Nixpacks.

## Variables de Entorno Requeridas

Configura estas variables en tu plataforma de despliegue:

```env
# Credenciales de base de datos
POSTGRES_DB=pdfdb
POSTGRES_USER=postgres
POSTGRES_PASSWORD=tu-contraseña-segura
DB_HOST=tu-host-db.c.airmail.cc

# Seguridad de Django
SECRET_KEY=tu-clave-secreta-muy-larga-y-aleatoria
DEBUG=false

# CORS y CSRF
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
CSRF_TRUSTED_ORIGINS=https://tu-dominio.com,https://www.tu-dominio.com
```

## Despliegue en Render

1. Conecta tu repositorio GitHub a [Render.com](https://render.com)
2. Crea un nuevo servicio **"Web Service"**
3. Render detectará automáticamente el `nixpacks.toml`
4. Configura las **Environment Variables** mencionadas arriba
5. Asegúrate de tener un servicio PostgreSQL conectado

## Despliegue en Railway

1. Conecta tu repo en [Railway.app](https://railway.app)
2. Railway detectará automáticamente el proyecto Django
3. Agrega un plugin PostgreSQL
4. Configura las variables de entorno en Railway Dashboard
5. Railway usará Nixpacks automáticamente

## Despliegue Local con Nixpacks

```bash
# Instalar nixpacks
curl -sSL https://get.nixpacks.com/install.sh | bash

# Preview local
nixpacks plan .

# Construir imagen Docker
nixpacks build --name pdfs-django-app:latest .

# Ejecutar
docker run -e DATABASE_URL=postgres://... -p 8000:8000 pdfs-django-app:latest
```

## Consideraciones Importantes

### CSRF y Origin Checking
- El problema de `403 Origin checking failed` ocurre cuando el `Origin` del request no está en `CSRF_TRUSTED_ORIGINS`
- Asegúrate de incluir tu dominio **con esquema** (http:// o https://)
- Ejemplo correcto: `https://tu-dominio.com` (no `tu-dominio.com`)

### Base de Datos
- La BD se inicializa automáticamente en el primer despliegue
- Las migraciones se ejecutan automáticamente al iniciar (`start.sh`)
- Usa variables de entorno para conectar a PostgreSQL externo

### Archivos Estáticos
- Se recopilan durante la construcción (`collectstatic`)
- En producción, usa un CDN o servicio de objetos (S3, etc.)

### Secretos
- **NUNCA** hagas commit de secretos en el código
- Usa variables de entorno para todo
- Genera una `SECRET_KEY` fuerte y única: 
  ```python
  from django.core.management.utils import get_random_secret_key
  print(get_random_secret_key())
  ```

## Troubleshooting

**Error "Module not found":**
- Asegúrate de que `requirements.txt` incluye todas las dependencias

**Error de conexión a BD:**
- Verifica que `DATABASE_URL` o las variables `POSTGRES_*` sean correctas
- La BD debe estar accesible desde la VPS

**Error 403 en login/registro:**
- Agrega tu dominio a `CSRF_TRUSTED_ORIGINS` con el esquema correcto
- Reinicia la app tras cambiar variables de entorno

## Arquitectura

```
┌─────────────────┐
│   Navegador     │
└────────┬────────┘
         │ HTTPS
         ▼
┌─────────────────┐     ┌──────────────────┐
│   Nixpacks      │────▶│   PostgreSQL     │
│   (Gunicorn)    │     │                  │
└─────────────────┘     └──────────────────┘
```
