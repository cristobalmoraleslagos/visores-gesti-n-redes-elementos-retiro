# Coordenada Pública · Visores de Gestión de Red

Sitio estático multi-visor para deploy en Vercel.

## Estructura

```
vercel/
├── index.html              · landing con tarjetas por visor
├── vercel.json             · routing, headers y redirects
├── package.json
├── .vercelignore
├── lo-prado/index.html
├── cerrillos/index.html
├── colina/index.html
├── tiltil/index.html
├── el-bosque/index.html
├── pudahuel/index.html
├── recoleta/index.html
├── maipu/index.html
├── puente-alto/index.html
├── talagante/index.html
├── quinta-normal/index.html
├── penalolen/index.html
├── melipilla/index.html
├── lo-espejo/index.html
├── nacional/index.html
├── base-madre/index.html
```

## Visores incluidos

| Slug | URL | Visor | Alcance |
|------|-----|-------|---------|
| `lo-prado` | `/lo-prado` | Lo Prado | comunal |
| `cerrillos` | `/cerrillos` | Cerrillos | comunal |
| `colina` | `/colina` | Colina | comunal |
| `tiltil` | `/tiltil` | Tiltil | comunal |
| `el-bosque` | `/el-bosque` | El Bosque | comunal |
| `pudahuel` | `/pudahuel` | Pudahuel | comunal |
| `recoleta` | `/recoleta` | Recoleta | comunal |
| `maipu` | `/maipu` | Maipú | comunal |
| `puente-alto` | `/puente-alto` | Puente Alto | comunal |
| `talagante` | `/talagante` | Talagante | comunal |
| `quinta-normal` | `/quinta-normal` | Quinta Normal | comunal |
| `penalolen` | `/penalolen` | Peñalolén | comunal |
| `melipilla` | `/melipilla` | Melipilla | comunal |
| `lo-espejo` | `/lo-espejo` | Lo Espejo | comunal |
| `nacional` | `/nacional` | Nacional · Público | nacional |
| `base-madre` | `/base-madre` | Base Madre | maestro |

## Despliegue

### Opción A: CLI de Vercel
```bash
cd vercel
npx vercel              # primera vez (preview)
npx vercel --prod       # producción
```

### Opción B: GitHub + Vercel Web
1. Subir el contenido de `vercel/` a un repo de GitHub.
2. En vercel.com → **Add New Project** → importar el repo.
3. Framework preset: **Other**. Output dir: raíz del repo. **Deploy**.

### Opción C: drag & drop
Arrastrar la carpeta `vercel/` completa a https://vercel.com/new

## URLs limpias

`cleanUrls: true` permite acceder a `/lo-prado` en lugar de `/lo-prado/index.html`.

## Datos consolidados nacionales

- Total registros oficiales: **66,225**
- CLP estimado total: **$6,663,023,000**
- KM totales: **2,359.76**
- KG totales: **401,783.6**
- Comunas: **322**

---

© Coordenada Pública · Abril 2026
