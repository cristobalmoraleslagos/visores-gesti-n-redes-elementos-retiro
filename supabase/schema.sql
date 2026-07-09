-- ============================================================
-- Fiscalización Municipal · Coordenada Pública
-- Esquema Supabase (PostgreSQL) · pegar completo en SQL Editor
-- ============================================================

-- 1 · Tabla principal de puntos capturados en terreno
create table if not exists public.puntos (
  codigo            text primary key,
  comuna            text not null,
  inspector_email   text not null,
  ts                timestamptz not null default now(),
  lat               double precision not null,
  lng               double precision not null,
  accuracy_m        integer,
  direccion         text,
  tipo_elemento     text not null,
  elemento_red      text not null default 'Cableado',
  material          text default 'Mixto_General',
  causales          jsonb not null default '{}'::jsonb,   -- causales D.S. 176
  operador          text default 'Por identificar',
  marca_color       text,                                  -- Res. Ex. 1.642
  gravedad          text not null,                         -- Sin infracción | Leve | Moderada (Abandono) | Grave (Riesgo Inminente)
  utm_dia           numeric not null default 0,            -- 0 a 5 UTM/día (ordenanza tipo)
  clp_estimado      bigint not null default 0,
  afectacion        jsonb not null default '{}'::jsonb,    -- personas/bienes/vialidad/patrimonio
  descripcion       text,
  foto_url          text,
  foto_sha256       text,                                  -- cadena de custodia
  estado_expediente text not null default 'Detección',
  expediente_id     text,
  created_at        timestamptz not null default now()
);

create index if not exists idx_puntos_comuna on public.puntos (comuna);
create index if not exists idx_puntos_ts on public.puntos (ts desc);
create index if not exists idx_puntos_inspector on public.puntos (inspector_email);

-- Máquina de estados del expediente (regla de negocio 5.2)
alter table public.puntos add constraint chk_estado check (estado_expediente in
 ('Detección','Calificación técnica','Notificación','Respuesta operador',
  'Retiro','Discrepancia SUBTEL','Silencio','Denuncia JPL','Ejecución subsidiaria','Cierre'));

-- 2 · Seguridad (RLS)
alter table public.puntos enable row level security;

-- Inspectores autenticados: insertar y ver todo lo de su municipio (lectura global para el equipo)
create policy "insert_autenticado" on public.puntos
  for insert to authenticated
  with check (auth.jwt()->>'email' = inspector_email);

create policy "select_autenticado" on public.puntos
  for select to authenticated using (true);

-- Solo el autor puede editar y solo en estado Detección (regla de negocio: inspector no altera lo calificado)
create policy "update_autor_deteccion" on public.puntos
  for update to authenticated
  using (auth.jwt()->>'email' = inspector_email and estado_expediente = 'Detección');

-- Lectura pública SOLO de campos vía vista (para el visor web, con anon key)
create policy "select_anon" on public.puntos
  for select to anon using (true);
-- Nota: si prefieres restringir, elimina "select_anon" y crea una vista pública.

-- 3 · Storage para evidencia fotográfica
insert into storage.buckets (id, name, public) values ('evidencias','evidencias', true)
on conflict (id) do nothing;

create policy "fotos_upload" on storage.objects
  for insert to authenticated with check (bucket_id = 'evidencias');
create policy "fotos_read" on storage.objects
  for select to public using (bucket_id = 'evidencias');

-- 4 · Vista para el visor (formato compatible con RAW_DATA del visor comunal)
create or replace view public.puntos_visor as
select
  'APP-'||codigo                       as id,
  operador                             as fuente,
  'Región Metropolitana de Santiago (XIII)' as region,
  comuna,
  'Fiscalización en terreno'           as plan,
  1                                    as prioridad,
  'Calles y Avenidas'                  as tipo_lugar,
  tipo_elemento,
  elemento_red,
  material,
  case when gravedad = 'Grave (Riesgo Inminente)' then 'Mal Estado / Riesgo'
       when gravedad = 'Sin infracción'           then 'Desconocido'
       else 'En Desuso' end            as estado_clasificado,
  'Válido'                             as estado_final,
  case when gravedad = 'Grave (Riesgo Inminente)' then 'Alto'
       when gravedad = 'Moderada (Abandono)'      then 'Medio'
       else 'Bajo' end                 as riesgo,
  case when gravedad = 'Grave (Riesgo Inminente)' then 9
       when gravedad = 'Moderada (Abandono)'      then 5
       else 0 end                      as riesgo_score,
  case when utm_dia > 0 then 1 else 0 end as multas,
  clp_estimado                         as clp_multas,
  0.04                                 as km,
  6.0                                  as kg_basura,
  lat, lng, ts, inspector_email, gravedad, estado_expediente, foto_url
from public.puntos;

grant select on public.puntos_visor to anon, authenticated;

-- 5 · Usuarios (70–100 inspectores)
-- Crear en Authentication → Users → "Add user" (email + contraseña), o por SQL/API admin.
-- Ejemplo API admin (ejecutar con service_role key, NUNCA exponerla en la app):
--   curl -X POST '<URL>/auth/v1/admin/users' -H 'apikey: <SERVICE_ROLE>' -H 'Authorization: Bearer <SERVICE_ROLE>' \
--     -H 'Content-Type: application/json' \
--     -d '{"email":"alejandro@munistgo.cl","password":"Cambiar.2026","email_confirm":true}'
