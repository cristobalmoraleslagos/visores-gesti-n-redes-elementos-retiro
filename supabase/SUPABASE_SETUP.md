# Setup Supabase · Fiscalización Municipal (15 minutos)

El backend soporta 70–100 inspectores simultáneos con login email/contraseña, base de datos PostgreSQL, fotos con cadena de custodia y alimentación en tiempo real del visor.

## Paso 1 · Crear el proyecto

1. Ir a **supabase.com** → Sign up (con cristobal.moraleslagos@gmail.com).
2. **New project** → Nombre: `fiscalizacion-municipal` → Región: **South America (São Paulo)** → contraseña de BBDD segura (guardarla).
3. Esperar ~2 min a que el proyecto se aprovisione.

## Paso 2 · Crear tablas y seguridad

1. Menú lateral → **SQL Editor** → New query.
2. Pegar TODO el contenido de `supabase/schema.sql` → **Run**.
3. Debe terminar sin errores ("Success").

## Paso 3 · Conectar la app y el visor

1. Menú lateral → **Settings → API**.
2. Copiar **Project URL** y **anon public** key.
3. Pegarlas en `vercel/app/config.js`:
   ```js
   SUPABASE_URL: "https://TUPROYECTO.supabase.co",
   SUPABASE_ANON_KEY: "eyJhbGci...",
   ```
4. `git push origin main` → Vercel redeploya. Listo: la app deja el modo demo y el visor de Estación Central empieza a mostrar puntos en vivo.

## Paso 4 · Crear los usuarios inspectores

Opción A (manual, recomendada para partir): **Authentication → Users → Add user** → email institucional (ej. `alejandro@munistgo.cl`) + contraseña → marcar **Auto Confirm User**. Repetir por inspector.

Opción B (masiva, 70–100 usuarios): con la **service_role key** (Settings → API → nunca ponerla en la app):

```bash
curl -X POST 'https://TUPROYECTO.supabase.co/auth/v1/admin/users' \
  -H 'apikey: SERVICE_ROLE_KEY' -H 'Authorization: Bearer SERVICE_ROLE_KEY' \
  -H 'Content-Type: application/json' \
  -d '{"email":"alejandro@munistgo.cl","password":"Clave.Inicial.2026","email_confirm":true}'
```

(Se puede iterar desde una planilla; pídeme el script cuando tengas la lista de correos.)

## Paso 5 · Probar el flujo completo

1. En el celular Android: abrir `https://gestionderedesendesuso.vercel.app/app/` en Chrome → menú ⋮ → **Agregar a pantalla de inicio** (queda instalada como app).
2. Login con un usuario creado → capturar un punto con foto en Estación Central.
3. Abrir `/rm/estacion-central/` → el punto aparece en el mapa (capa "En vivo") en ≤30 segundos.

## Capacidad y límites (plan gratuito)

| Recurso | Free tier | Suficiente para |
|---|---|---|
| BBDD | 500 MB | ~1 millón de puntos |
| Storage | 1 GB | ~3.000 fotos (300 KB c/u con marca de agua) |
| Usuarios auth | 50.000 | 100 inspectores de sobra |
| Requests | Ilimitados razonables | Despliegue comunal completo |

Para operación con varios municipios: plan Pro USD 25/mes (8 GB BBDD + 100 GB storage).

## Seguridad implementada

- RLS: cada inspector solo inserta con su propio email (verificado contra el JWT); solo edita sus puntos en estado "Detección".
- Fotos: hash SHA-256 calculado en el dispositivo al momento de la captura, guardado junto al punto (cadena de custodia verificable en JPL).
- Marca de agua grabada en píxeles (usuario + timestamp Chile + WGS84 5 decimales), no removible.
- La `service_role` key nunca viaja a la app; solo `anon` + JWT del usuario.
