# FastAPI Discovery

Plantilla personal para iniciar proyectos con FastAPI, autenticacion y auditoria.

## Configuracion inicial

1. Crea tu entorno y dependencias:
   - `python -m venv venv`
   - `source venv/bin/activate`
   - `pip install -r requirements.txt`
2. Copia variables de entorno:
   - `cp .env.example .env`
3. Rellena `.env`:
   - `ENVIRONMENT`
   - `DATABASE_URL`
   - `JWT_*`
   - `BREVO_*` (si usaras envio de correos)
   - `OTP_*`
   - `REDIS_URL`
   - `AUDIT_*` (si usaras auditoria)

## Comportamiento por defecto

- El modelo `User` usa `UUIDBaseModel` por defecto.
- `init_db()` se ejecuta al iniciar la app en `ENVIRONMENT=DEV` para crear tablas.
- La auditoria se controla con `AUDIT_ENABLED`:
  - `true`: registra eventos usando el modulo `system`.
  - `false`: `AuditLogger` funciona en modo no-op (no guarda bitacora).

## Sobre `ENVIRONMENT`

`ENVIRONMENT` si se usa actualmente:
- En `DEV` se ejecuta `SQLModel.metadata.create_all(...)` al iniciar.
- Para produccion normalmente usaras migraciones (Alembic) en lugar de `create_all`.

## Endpoints base

- Auth: prefijo `/api/auth`
- Account: prefijo `/api/auth/account`
- Audit: prefijo `/api/system/audit`

## Si no quieres auditoria

Opcion recomendada:
- Deja `AUDIT_ENABLED=false`.

No necesitas borrar el modulo `system`; simplemente no registrara eventos.
