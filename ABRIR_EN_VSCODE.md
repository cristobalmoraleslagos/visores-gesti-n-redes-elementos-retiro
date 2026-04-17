# Cómo cargar todos los visores en Visual Studio Code

Este documento muestra tres rutas. Elige la que te acomode.

## 1. Abrir la carpeta en VSCode

- Botón derecho sobre `Visor para la gestión de redes/` → **Open with Code**
- O desde VSCode: `File → Open Folder…` → seleccionar esta carpeta.
- Al abrirla por primera vez VSCode te sugerirá instalar las extensiones recomendadas (están en `.vscode/extensions.json`). Acepta **Install All**.

Extensiones clave:

- **Live Server** (ritwickdey.liveserver) – previsualización con auto-reload
- **Live Preview** (ms-vscode.live-server) – alternativa oficial de Microsoft
- **Prettier** – formato de HTML/JSON
- **Rainbow CSV** – para leer `Base de dato elementos de red.csv`

## 2. Servir los visores localmente

> Los visores usan `fetch()` a Leaflet/Chart.js por CDN, así que **deben abrirse con un servidor HTTP**, no con doble-click (file://). Si los abres con file:// el navegador bloquea CORS y el mapa no carga.

Tres formas, en orden de comodidad:

### a) Live Server (más simple)

1. Abre cualquier `vercel/<comuna>/index.html` en el editor.
2. Click derecho en el archivo → **Open with Live Server**.
3. Se abre en `http://127.0.0.1:5500/<ruta>` con auto-reload al guardar.

`settings.json` ya apunta `liveServer.settings.root` a `/vercel`, así que `index.html` (landing) queda como raíz del servidor.

### b) Tareas de VSCode (`Ctrl+Shift+P` → Run Task)

Tienes preconfiguradas:

- **Servir visores (npx serve)** → `http://localhost:5173`
- **Servir visores (Python http.server)** → alternativa sin Node
- **Abrir landing en navegador**
- **Desplegar a Vercel (preview)**
- **Desplegar a Vercel (producción)**

### c) Debug con Chrome (F5)

En `launch.json` tienes tres launchers:

- **Abrir landing en Chrome**
- **Abrir visor Lo Prado**
- **Abrir visor Nacional**

Presiona `F5` o selecciona uno en la vista **Run and Debug** de la barra lateral. Requiere la extensión **Debugger for Chrome / Edge** (viene por default).

## 3. Editar los visores

Los visores son archivos HTML de una sola pieza: todo el CSS/JS está embebido. Para tocar estilo, paleta, KPIs o texto, abres el `index.html` dentro de `vercel/<comuna>/` y editas directo. Con Live Server activo, el cambio se refleja en el navegador al guardar.

Recuerda: si editas `vercel/<comuna>/index.html`, esa es la copia desplegable. El original en la raíz (`Visor_<Comuna>.html`) es una copia de referencia que **no** se despliega a Vercel.

## 4. Atajos útiles

- `Ctrl+P` → abrir archivo por nombre (`Visor_LoPrado.html`, `vercel.json`…)
- `Ctrl+Shift+F` → buscar en todo el proyecto
- `Ctrl+K V` → preview del Markdown a la derecha
- `Ctrl+Shift+P` → paleta de comandos (Run Task, Toggle Terminal…)
- `` Ctrl+` `` → abrir terminal integrada

## 5. Desplegar desde VSCode

Terminal integrada:

```bash
cd vercel
npx vercel           # preview
npx vercel --prod    # producción
```

O usa las tareas preconfiguradas: `Ctrl+Shift+P` → **Tasks: Run Task** → **Desplegar a Vercel (producción)**.

---
Cualquier duda con los visores o el deploy, pregúntame directo.
