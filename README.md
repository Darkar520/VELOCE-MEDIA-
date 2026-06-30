# Veloce Media Studio

Centro de control unificado para descarga y conversion de contenido multimedia,
optimizado para Android (via Termux) con un backend opcional para busqueda y
descarga de peliculas, series y anime.

## Estructura

```
.
├── index.html              # App web unificada (frontend, 7 modulos)
├── centinela_veloce.py     # Centinela para Termux (musica + video)
├── backend/                # Microservicio Node.js (busqueda + descarga real)
│   ├── server.js
│   └── package.json
└── _referencia/            # Versiones previas (solo referencia, no se usan)
```

## Modulos del frontend (`index.html`)

1. **Panel de Control** – Puente de calidad para Spotify / Apple Music / YouTube.
2. **Descargador** – Descarga de YouTube, Instagram, TikTok, X, Facebook, etc. (yt-dlp / Cobalt).
3. **Buscar Contenido** – Busqueda y descarga de peliculas, series y anime (The Pirate Bay, YTS, Nyaa.si, 1337x, SolidTorrents) con filtro estricto anti-basura.
4. **Guia e Instalacion** – Setup del centinela de Termux.
5. **Simulador Web** – Sandbox de extraccion sin instalar nada.
6. **Conversor Local** – Extraccion/conversion de audio con Web Audio API.
7. **Biblioteca Stock** – Muestras de contenido.

El frontend es un solo archivo HTML. Solo abrelo en el navegador.

## Backend de busqueda (opcional)

La pestaña **Buscar Contenido** funciona en dos modos:

- **Simulado** (por defecto): resultados de demostracion, sin servidor.
- **Servidor Local**: busqueda y descarga reales contra el microservicio Node.

Para activar el modo real:

```bash
cd backend
npm install
npm start
```

El servicio queda activo en `http://localhost:4000`. Luego, en la pestaña
**Buscar Contenido**, cambia el modo a **Servidor Local**.

> El backend descarga el torrent con **WebTorrent** (motor P2P real: TCP/uTP/DHT),
> guarda el archivo en `backend/library/` y lo sirve al navegador para que quede
> en tu carpeta de Descargas. Si WebTorrent no carga, cae a un modo de respaldo.

Endpoints:

- `GET  /api/health` – estado del servicio (incluye si WebTorrent esta activo)
- `GET  /api/search?query=<texto>&type=<all|movies|tv|anime>`
- `POST /api/download` – body `{ magnet, title, size, source }`
- `GET  /api/download/progress/:jobId` – progreso en vivo (SSE)
- `GET  /api/file/:jobId` – descarga el archivo ya bajado hacia el navegador

## Termux (Android)

Sigue la pestaña **Guia e Instalacion** dentro de la app para configurar
`centinela_veloce.py` y el boton Compartir nativo.
