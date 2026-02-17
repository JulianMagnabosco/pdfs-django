# Ejemplos de uso de la API

## 1. Registro
```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "juan",
    "email": "juan@example.com",
    "password": "mipassword123",
    "password2": "mipassword123"
  }'
```

Respuesta:
```json
{
  "user": {
    "id": 2,
    "username": "juan",
    "email": "juan@example.com"
  },
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

## 2. Login
```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "juan",
    "password": "mipassword123"
  }'
```

## 3. Listar PDFs
```bash
curl -X GET http://localhost:8000/api/pdfs/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

Respuesta:
```json
[
  {
    "id": 1,
    "user": {
      "id": 2,
      "username": "juan",
      "email": "juan@example.com"
    },
    "filename": "documento.pdf",
    "content_type": "application/pdf",
    "size": 102400,
    "uploaded_at": "2026-02-17T10:30:00Z"
  }
]
```

## 4. Subir PDF
```bash
curl -X POST http://localhost:8000/api/pdfs/upload/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -F "file=@documento.pdf"
```

## 5. Descargar PDF
```bash
curl -X GET http://localhost:8000/api/pdfs/1/download/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -o documento_descargado.pdf
```

## 6. Obtener detalles de un PDF
```bash
curl -X GET http://localhost:8000/api/pdfs/1/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

## 7. Eliminar un PDF
```bash
curl -X DELETE http://localhost:8000/api/pdfs/1/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

Respuesta:
```json
{
  "message": "PDF eliminado"
}
```

## Notas
- Todos los endpoints excepto `/api/register/` y `/api/login/` requieren autenticación por token.
- El token debe enviarse en el header `Authorization: Token <token>`
- Para subir PDFs usa `multipart/form-data` con el campo `file`.
