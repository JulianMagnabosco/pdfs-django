
### 1. Copia el archivo .env.traefik.example

```bash
cp .env.traefik.example .env
```

### 2. Edita el archivo .env

Reemplaza los valores con los tuyos:
```bash
DOMAIN=tudominio.com
SECRET_KEY=tu-clave-secreta-super-segura
POSTGRES_PASSWORD=tu-contraseña-segura
LETSENCRYPT_EMAIL=tu-email@example.com
```

### 3. Inicia los contenedores

```bash
docker-compose -f docker-compose.traefik.yml up -d
```

### 4. Verifica que todo esté funcionando

```bash
# Ver logs
docker-compose -f docker-compose.traefik.yml logs -f web

# Dashboard de Traefik (desarrollar acceso con restricción)
http://localhost:8080
```


## Variables de Entorno Importantes

| Variable | Descripción | Por defecto |
|----------|-------------|------------|
| `DOMAIN` | Tu dominio | `app.com` |
| `DEBUG` | Modo debug Django | `0` (desactivado en prod) |
| `SECRET_KEY` | Clave secreta Django | cambiar en producción |

## Comandos Útiles

```bash
# Ver estado de servicios
docker-compose -f docker-compose.traefik.yml ps

# Detener servicios
docker-compose -f docker-compose.traefik.yml down

# Ver logs completos
docker-compose -f docker-compose.traefik.yml logs

# Ejecutar comando en contenedor web
docker-compose -f docker-compose.traefik.yml exec web python manage.py migrate

# Crear superuser
docker-compose -f docker-compose.traefik.yml exec web python manage.py createsuperuser

# Coleccionar archivos estáticos
docker-compose -f docker-compose.traefik.yml exec web python manage.py collectstatic --noinput
```

## Modificaciones en Django

Si necesitas que Django entienda los headers de Traefik, asegúrate de que en `settings.py` esté configurado:

```python
# Confiar en headers de proxy
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Hosts permitidos
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', 'http://localhost').split(',')
```

## Renovación de Certificados

Let's Encrypt renueva automáticamente los certificados 30 días antes del vencimiento.
Los certificados se guardan en `./letsencrypt/` via volumen de Docker.

## Dashboard de Traefik (Desarrollo)

⚠️ **ADVERTENCIA**: El dashboard está expuesto en `http://localhost:8080` sin autenticación.

Para producción, desactívalo o protégelo:

```yaml
# En traefik command, agrega:
- "--api.insecure=false"

# Y agrega autenticación:
- "traefik.http.routers.dashboard.rule=Host(`traefik.${DOMAIN}`)"
- "traefik.http.routers.dashboard.service=api@internal"
- "traefik.http.middlewares.auth.basicauth.users=admin:hashed_password"
```

## Troubleshooting

### Los certificados no se generan
- Verifica que el puerto 80 sea accesible desde fuera
- Revisa el email de Let's Encrypt en tu inbox
- Mira los logs: `docker-compose -f docker-compose.traefik.yml logs traefik`

### Conexión rechazada
- Asegúrate que el DOMAIN apunte a tu servidor
- Verifica que ports 80 y 443 estén abiertos en firewall
- Reinicia: `docker-compose -f docker-compose.traefik.yml restart`

### Static files no se sirven
- Asegúrate que Django esté sirviendo archivos estáticos (descomentar línea en compose)
- O configura nginx en el compose (ver sección comentada)

## Producción

Para producción, recuerda:
1. ✅ Cambiar `SECRET_KEY` a algo seguro
2. ✅ Cambiar contraseña de PostgreSQL
3. ✅ Usar `DEBUG=0`
4. ✅ Configurar email real en acme para Let's Encrypt
5. ✅ Usar base de datos externa o volumen persistente mejor documentado
6. ✅ Limitar acceso al dashboard de Traefik
7. ✅ Hacer backups de `./letsencrypt/`
