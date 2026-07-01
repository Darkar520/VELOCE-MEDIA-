# 🎬 Veloce Media Studio

Centro de control unificado para **descarga y conversión de contenido multimedia**,
optimizado para Android (vía Termux) y escritorio. Incluye un buscador de películas,
series y anime con descarga real integrada.

> **Aviso:** Proyecto educativo / de laboratorio. Úsalo únicamente con contenido que
> tengas derecho a descargar. El autor no se responsabiliza por el uso indebido.

---

## ✨ Características

- **Panel de control de calidad** para música (Spotify / Apple Music / YouTube) vía puente Termux.
- **Descargador multiplataforma** (YouTube, Instagram, TikTok, X, Facebook, etc.).
- **Buscador de contenido** de películas, series y anime:
  - Fuentes reales: **The Pirate Bay, YTS, Nyaa.si, 1337x, SolidTorrents**.
  - Filtro estricto anti-basura (descarta gameplays, clips, música, etc.).
  - Resultados divididos por **Películas / Series / Anime** con conteos.
  - Selección de **temporada, capítulo, calidad, idioma y subtítulos**.
- **Descarga real integrada** en el backend (motor **aria2** con respaldo **WebTorrent**):
  - Progreso en vivo (SSE), botón de cancelar, y guardado automático en el navegador.
- **Subtítulos reales** vía OpenSubtitles (descarga el `.srt` en el idioma elegido).
- **Simulador web**, **conversor de audio local** (Web Audio API) y **biblioteca de muestras**.

---

## 🧱 Arquitectura

```
┌─────────────────────┐         HTTP / SSE          ┌──────────────────────────┐
│   Frontend (SPA)    │  ───────────────────────▶   │   Backend (Node/Express) │
│   frontend/         │   /api/search, /download,   │   backend/server.js      │
│   index.html + JS   │   /file, /subtitles ...     │   aria2 · WebTorrent      │
└─────────────────────┘                             │   OpenSubtitles           │
                                                     └──────────────────────────┘
```

- **Frontend:** una sola página (`index.html`) con Tailwind y Lucide **vendorizados**
  (no depende de CDNs externos).
- **Backend:** microservicio Express que agrega búsquedas de varias fuentes, descarga
  torrents con aria2/WebTorrent y sirve el archivo final + subtítulos.

---

## 📁 Estructura del proyecto

```
.
├── frontend/
│   ├── index.html            # Aplicación web (7 módulos)
│   └── assets/               # Tailwind y Lucide vendorizados
│       ├── tailwind.js
│       └── lucide.js
├── backend/
│   ├── server.js             # Microservicio de búsqueda + descarga
│   ├── package.json
│   └── .env.example
├── termux/
│   └── centinela_veloce.py   # Centinela para Termux (puente de música/video)
├── README.md
├── LICENSE
└── .gitignore
```

---

## ⚙️ Requisitos

- **Node.js** 18+ (probado con Node 24).
- **aria2** para descargas rápidas (opcional pero recomendado):
  - Termux/Linux: `pkg install aria2` o `apt install aria2`
  - Windows: descarga el binario de [aria2](https://github.com/aria2/aria2/releases) y colócalo en `backend/bin/aria2c.exe`
  - Si no está aria2, el backend usa WebTorrent automáticamente.

---

## 🚀 Instalación y ejecución

### 1. Backend (búsqueda + descarga)

```bash
cd backend
npm install
npm start           # arranca en http://localhost:4000
```

El puerto es configurable: `PORT=5000 npm start` (ver `.env.example`).

### 2. Frontend

Sirve la carpeta `frontend/` con cualquier servidor estático:

```bash
# desde la raíz del proyecto
npx http-server frontend -p 8080 -c-1
```

Luego abre **http://localhost:8080/index.html**.

> El frontend detecta el backend automáticamente. En la pestaña **Buscar Contenido**
> verás el estado "Backend conectado" cuando el servicio esté activo.

---

## 🔌 API del backend

| Método | Endpoint                          | Descripción                                  |
|--------|-----------------------------------|----------------------------------------------|
| GET    | `/api/health`                     | Estado y motor activo (aria2 / webtorrent)   |
| GET    | `/api/search?query=&type=`        | Búsqueda unificada (all/movies/tv/anime)     |
| POST   | `/api/download`                   | Inicia descarga `{ magnet, title, size }`    |
| GET    | `/api/download/progress/:jobId`   | Progreso en vivo (SSE)                        |
| POST   | `/api/download/:jobId/cancel`     | Cancela una descarga y borra lo parcial      |
| GET    | `/api/file/:jobId`                | Sirve el archivo descargado al navegador     |
| GET    | `/api/subtitles?query=&lang=`     | Busca subtítulos (OpenSubtitles)             |
| GET    | `/api/subtitle/get?u=&n=`         | Descarga y descomprime un `.srt`             |

---

## 📱 Termux (Android)

El módulo **Guía e Instalación** dentro de la app genera los comandos para configurar
`termux/centinela_veloce.py` y el botón "Compartir" nativo. Para descargas de contenido,
basta con `pkg install aria2` y ejecutar el backend con `node server.js` en Termux.

---

## ⚠️ Limitaciones conocidas

- La velocidad y disponibilidad de una descarga dependen de los **seeds** del torrent.
- El audio en un idioma específico depende de que exista un release doblado; usa los
  chips **Latino / Castellano / Dual** para encontrarlos. Los **subtítulos** siempre se
  obtienen aparte vía OpenSubtitles.
- 1337x genera un magnet aproximado (las fuentes con magnet real son TPB, YTS, Nyaa y SolidTorrents).

---

## 📄 Licencia

[MIT](./LICENSE) © 2026 Darkar520
