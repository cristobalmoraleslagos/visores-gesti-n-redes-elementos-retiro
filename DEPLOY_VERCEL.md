# Desplegar a Vercel desde VSCode

Guía paso a paso para publicar la carpeta `vercel/` (11 visores + landing) a Vercel, usando Visual Studio Code.

---

## Prerrequisitos (una sola vez)

1. **Node.js 18+** instalado. Verifica en la terminal integrada de VSCode:
   ```bash
   node --version
   npm --version
   ```
   Si no aparece, instala desde https://nodejs.org (elige LTS). Reinicia VSCode después.

2. **Cuenta Vercel gratuita** en https://vercel.com/signup (Hobby plan sirve). Recomendado: ingresar con **GitHub** o **Google** para que el login por CLI sea instantáneo.

3. **Carpeta `vercel/` lista** — ya la tienes. Verifica con:
   ```bash
   ls vercel
   ```
   Deberías ver `index.html`, `vercel.json`, 11 subcarpetas y `README.md`.

---

## Camino rápido (3 comandos)

Terminal integrada de VSCode (`` Ctrl+` ``):

```bash
cd vercel
npx vercel login          # solo la primera vez
npx vercel --prod         # publica a producción
```

Al finalizar te devuelve la URL de producción (ej. `https://coordenada-publica.vercel.app`). Listo.

---

## Camino detallado

### Paso 1 · Login

```bash
cd "Visor para la gestión de redes/vercel"
npx --yes vercel login
```

- Elige método: **Continue with GitHub** / **Google** / **Email**.
- Se abre el navegador → autoriza → vuelve a la terminal → `Success!`.

El login queda guardado en `~/.vercel` (o `%USERPROFILE%\.vercel` en Windows), no necesitas repetirlo.

### Paso 2 · Preview deployment (vincula el proyecto)

```bash
npx --yes vercel
```

Preguntas que te hará la primera vez:

| Pregunta | Respuesta sugerida |
|---|---|
| Set up and deploy? | **Y** |
| Which scope? | tu cuenta personal |
| Link to existing project? | **N** (crea uno nuevo) |
| Project name? | `coordenada-publica-visores` (o el que prefieras) |
| Directory? | `./` (estás parado en `vercel/`) |
| Override settings? | **N** (Vercel detecta static + respeta `vercel.json`) |

Resultado: un enlace preview tipo `https://coordenada-publica-visores-xxx.vercel.app`. Ábrelo, verifica que el landing carga y que cada visor abre bien.

### Paso 3 · Producción

```bash
npx --yes vercel --prod
```

Sube la misma carpeta y la asigna al dominio de producción (`.vercel.app`). Cada vez que repitas este comando sube una nueva versión.

---

## Alternativa gráfica: Tareas de VSCode

Ya están preconfiguradas en `.vscode/tasks.json`. Ruta:

1. `Ctrl+Shift+P` → **Tasks: Run Task**
2. Elige:
   - **Desplegar a Vercel (preview)** — primera subida / revisión antes de prod
   - **Desplegar a Vercel (producción)** — sube a prod

Sigue las mismas preguntas del paso 2 en la terminal integrada.

---

## Opcional · Extensión Vercel para VSCode

Instala **Vercel** (id `vercel.vercel-vscode`) desde el Marketplace. Agrega:

- Panel lateral con lista de deployments y logs
- Atajos: click derecho en un deployment → **Redeploy** / **Promote to Production**
- Ver variables de entorno sin salir del editor

No es imprescindible — la CLI basta — pero es cómodo para seguir deploys en vivo.

---

## Conectar el repositorio (recomendado a mediano plazo)

Para que cada `git push` dispare un deploy automático:

1. Sube la carpeta raíz del proyecto a GitHub.
2. En el dashboard de Vercel → **Project → Settings → Git** → **Connect** → selecciona el repo.
3. Configura **Root Directory** = `vercel`.
4. Deja **Framework Preset** = *Other* (es estático).

Desde ahí cada commit en `main` genera un deploy de producción y cada rama un preview con URL propia.

---

## Dominio custom

Dashboard Vercel → **Project → Settings → Domains → Add**.

- Si el dominio está en el mismo email que la cuenta Vercel, basta con seguir el asistente.
- Si está en otro registrar (NIC Chile, GoDaddy…), Vercel te pide un `CNAME` o `A`. Copias y pegas en el panel del registrar.

Ejemplo: `visores.coordenadapublica.cl` → CNAME → `cname.vercel-dns.com`.

---

## Troubleshooting

| Problema | Causa / Solución |
|---|---|
| `npx: command not found` | Node no está instalado o no quedó en PATH. Reinstala Node LTS y reinicia VSCode. |
| `Permission denied` al login | Windows: corre VSCode como administrador la primera vez, o usa Powershell en vez de Git Bash. |
| Deploy sube pero el landing da 404 | Debes estar parado dentro de la carpeta `vercel/` cuando corres `npx vercel`. Revisa `pwd`. |
| Mapa vacío o CDN bloqueada | El sitio sirve sobre HTTPS en Vercel, así que los CDNs funcionan. Si falla localmente fue por `file://`. En producción no debería pasar. |
| `Too many deployments` | El plan Hobby tiene límite de 100 deploys/día por proyecto. Más que suficiente, pero si te excediste, espera 24 h. |
| Cambios no aparecen | Hard refresh (`Ctrl+F5`). `vercel.json` cachea HTML 5 minutos. Si es urgente, baja el TTL en `Cache-Control`. |
| Error `Invalid vercel.json` | Valida con `python -m json.tool vercel/vercel.json`. Corrige coma o llave faltante. |

---

## Checklist final antes de producción

- [ ] Todos los visores abren con el mapa cargado en el preview URL
- [ ] El landing muestra las 11 tarjetas con KPIs
- [ ] Click en una tarjeta abre `/<slug>` (URL limpia, sin `.html`)
- [ ] No aparece ninguna referencia a total nacional dentro de un visor comunal
- [ ] `Ctrl+P` / `Ctrl+S` están bloqueados en el visor nacional (datos anonimizados)
- [ ] El README de `vercel/` queda con los totales vigentes

Listo para publicar.

---

© Coordenada Pública · Abril 2026
