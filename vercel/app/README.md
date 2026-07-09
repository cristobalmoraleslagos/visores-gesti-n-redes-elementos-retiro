# Aplicativo de Fiscalización · Arquitectura Android (PWA)

URL productiva: `https://gestionderedesendesuso.vercel.app/app/`

## Arquitectura

```
[Inspector · Android]                      [Vercel · estático]
 Chrome / PWA instalada  ──────────────►  /app/ (login, captura, cola offline)
   │  cámara + GPS WGS84 5 dec.                 │
   │  marca de agua en píxeles + SHA-256        │ config.js (compartido)
   ▼                                            ▼
[IndexedDB local] ──sync──► [Supabase]  ◄──poll 30s──  /rm/estacion-central/ (visor)
                             ├ Auth (email/clave institucional, 70–100 usuarios)
                             ├ PostgreSQL: tabla puntos + vista puntos_visor
                             └ Storage: bucket evidencias (fotos con hash)
```

## Instalación en Android (sin Play Store)

1. Abrir la URL en Chrome → menú ⋮ → **Agregar a pantalla de inicio**.
2. Queda instalada como app nativa: ícono, pantalla completa, funciona offline.
3. Requiere permisos de cámara y ubicación (Chrome los solicita la primera vez).

## Modos de operación

| Modo | Cuándo | Comportamiento |
|---|---|---|
| Producción | `config.js` con credenciales Supabase | Login real, sync automático, visor en vivo |
| Demo | `config.js` vacío | Cualquier email + clave ≥4 caracteres; datos locales + export CSV cargable en el visor |
| Offline | Sin señal en terreno | Captura completa a cola local; sincroniza al recuperar red |

## Reglas de negocio implementadas (sección 9 del CLAUDE.md)

- Calificación: exige ≥1 causal D.S. 176 para gravedades distintas de "Sin infracción".
- Marca de agua inalterable: grabada en píxeles + SHA-256 del JPEG final.
- Inspector no puede editar timestamp ni ubicación tras guardar (RLS: solo estado Detección).
- Multa: 0–5 UTM/día por gravedad (config.js `UTM_POR_GRAVEDAD`), nunca denuncia automática.
- Emergencias: checkboxes de afectación personas/bienes/vialidad/patrimonio.

## Migración futura a React Native (Fase 2b)

La lógica es portable: los módulos `SB` (REST Supabase), `procesarFoto` (watermark+hash) y la cola IndexedDB se traducen 1:1 a Expo (expo-camera, expo-location, expo-sqlite). El backend y el esquema no cambian.
