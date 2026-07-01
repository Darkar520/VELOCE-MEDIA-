# Veloce Media Studio

Centro de control multimedia unificado para búsqueda, descarga y conversión de contenido. Diseñado para funcionar tanto en escritorio como en Android vía Termux.

![License](https://img.shields.io/badge/license-MIT-blue) ![Node](https://img.shields.io/badge/node-18%2B-green) ![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20Android-lightgrey)

---

## Vista general

La aplicación está dividida en dos piezas independientes que se comunican por HTTP:

```
┌──────────────────────────────┐           HTTP / SSE           ┌────────────────────────────────┐
│      Frontend (SPA)          │  ─────────────────────────►   │      Backend (Node/Express)     │
│  frontend/index.html         │  /api/search, /api/download,   │  backend/server.js              │
│  Tailwind + Lucide locales   │  /api/file, /api/subtitles...  │  aria2 · WebTorrent · OS API    │
└──────────────────────────────┘                                └────────────────────────────────┘
```

- **Frontend:** una sola página HTML con 7 módulos. Tailwind y Lucide están **vendorizados** — no depende de CDNs externos y funciona sin internet.
- **Backend:** microservicio Express que agrega búsquedas de múltiples fuentes, ejecuta descargas reales con aria2/WebTorrent y sirve subtítulos desde OpenSubtitles.

---

## Módulos del frontend

| Módulo | Descripción |
|---|---|
| **Panel de Control** | Puente de calidad para Spotify / Apple Music / YouTube vía Termux |
| **Descargador** | Descarga de YouTube, Instagram, TikTok, X, Facebook y más (yt-dlp / Cobalt) |
| **Buscar Contenido** | Buscador de películas, series y anime con descarga real integrada |
| **Guía e Instalación** | Setup del centinela de Termux paso a paso |
| **Simulador Web** | Sandbox de extracción sin instalar nada |
| **Conversor Local** | Extracción y conversión de audio con Web Audio API |
| **Biblioteca Stock** | Muestras de contenido multimedia |

---

## Buscador de contenido

El módulo más completo. Características:

- **5 fuentes reales:** The Pirate Bay, YTS, Nyaa.si, 1337x, SolidTorrents.
- **Filtro estricto anti-basura:** descarta gameplays, clips, música, trailers, etc.
- **Resultados divididos** en Películas / Series / Anime con conteos.
- **Chips de idioma:** busca versiones Latino, Castellano, Dual o cualquiera.
- **Selección granular:** temporada, capítulo, calidad, idioma de audio y subtítulos.
- **Descarga real en backend** con motor aria2 (respaldo: WebTorrent):
  - Progreso en vivo por SSE, botón de cancelar, guardado automático en el navegador.
- **Subtítulos reales** vía OpenSubtitles — descarga el `.srt` en el idioma elegido.

---

## Estructura del proyecto

```
veloce-media-studio/
├── frontend/
│   ├── index.html            # Aplicación web completa (7 módulos)
│   └── assets/
│       ├── tailwind.js       # Tailwind CSS Play CDN (vendorizado)
│       └── lucide.js         # Lucide Icons (vendorizado)
│
├── backend/
│   ├── server.js             # Microservicio de búsqueda + descarga + subtítulos
│   ├── package.json
│   └── .env.example          # Variables de entorno disponibles
│
├── termux/
│   └── centinela_veloce.py   # Centinela para Termux (puente de música/video en Android)
│
├── .gitignore
├── LICENSE
└── README.md
```

> `backend/library/` (descargas), `backend/bin/` (binario aria2) y `backend/node_modules/` están en `.gitignore` y no se versionan.

---

## Requisitos

- **Node.js 18+** (probado con Node 24)
- **aria2** para descargas rápidas *(opcional pero muy recomendado)*:
  - Android/Linux: `pkg install aria2` o `apt install aria2`
  - Windows: coloca el binario en `backend/bin/aria2c.exe` ([descargar](https://github.com/aria2/aria2/releases))
  - Si aria2 no está disponible, el backend usa WebTorrent automáticamente como respaldo.

---

## Instalación y ejecución

### 1. Backend

```bash
cd backend
npm install
npm start
# → http://localhost:4000
```

El puerto es configurable con la variable de entorno `PORT`:

```bash
PORT=5000 npm start
```

### 2. Frontend

Sirve la carpeta `frontend/` con cualquier servidor estático:

```bash
# desde la raíz del proyecto
npx http-server frontend -p 8080 -c-1
# → http://localhost:8080/index.html
```

El frontend **detecta el backend automáticamente al cargar**. Cuando el servicio esté activo verás el badge verde "Backend conectado" en la pestaña Buscar Contenido — sin configuración manual.

---

## API del backend

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/api/health` | Estado del servicio y motor activo (`aria2` / `webtorrent`) |
| `GET` | `/api/search?query=&type=` | Búsqueda unificada (`all` / `movies` / `tv` / `anime`) |
| `POST` | `/api/download` | Inicia descarga `{ magnet, title, size, source }` |
| `GET` | `/api/download/progress/:jobId` | Progreso en vivo (Server-Sent Events) |
| `POST` | `/api/download/:jobId/cancel` | Cancela y borra los archivos parciales |
| `GET` | `/api/file/:jobId` | Sirve el archivo descargado al navegador |
| `GET` | `/api/subtitles?query=&lang=` | Busca subtítulos en OpenSubtitles (`es` / `en`) |
| `GET` | `/api/subtitle/get?u=&n=` | Descarga y descomprime un archivo `.srt` |

---

## Android / Termux

El módulo **Guía e Instalación** dentro de la app genera los comandos exactos para configurar el entorno. Para descargas de contenido, los pasos mínimos son:

```bash
pkg install nodejs aria2
cd ~
git clone https://github.com/Darkar520/VELOCE-MEDIA-.git veloce
cd veloce/backend
npm install
node server.js
```

Luego abre `frontend/index.html` desde el navegador del teléfono apuntando a `http://localhost:4000`.

Para el puente de música y video, revisa `termux/centinela_veloce.py` y la guía dentro de la app.

---

## Limitaciones conocidas

- La velocidad de descarga depende de los **seeds** del torrent elegido. Prioriza siempre las versiones con más seeds (se muestran ordenadas).
- El audio en español depende de que exista un release doblado. Usa los chips **Latino / Castellano / Dual** para filtrar. Los subtítulos en español siempre están disponibles vía OpenSubtitles independientemente del audio.
- 1337x genera un magnet aproximado por limitaciones de su scraping. Las fuentes con magnet real son TPB, YTS, Nyaa y SolidTorrents.

---

## Aviso legal

Este proyecto es de uso educativo y experimental. Úsalo únicamente con contenido que tengas derecho a descargar. El autor no se responsabiliza por el uso indebido.

---

## Licencia

[MIT](./LICENSE) © 2026 Darkar520
