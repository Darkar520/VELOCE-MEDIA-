import time, subprocess, re, requests
from bs4 import BeautifulSoup

print("=========================================================")
print("[*] El Puente Centinela Veloce esta en linea...")
print("Selecciona la calidad en la App web y presiona 'Enviar'.")
print("=========================================================")

YT_ARGS = '--extractor-args "youtube:player_client=tv,web_safari,default" --retries 10 --fragment-retries 10'


def obtener_meta_spotify(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")
        og_title = soup.find("meta", property="og:title")
        og_desc = soup.find("meta", property="og:description")
        if og_title and og_desc:
            cancion = og_title["content"]
            desc = og_desc["content"]
            artista = desc.split("\u00b7")[1].strip() if "\u00b7" in desc else desc
            return f"{artista} - {cancion}"
    except Exception:
        pass
    return None


def mostrar_calidad_solicitada(cmd):
    """Muestra en pantalla la calidad que el usuario selecciono."""
    if "-x" in cmd or "--audio-format" in cmd:
        print("[~] Calidad solicitada : Audio MP3 320kbps")
        return
    match = re.search(r'height<=(\d+)', cmd)
    if match:
        h = match.group(1)
        labels = {"1440": "1440p Quad HD", "1080": "1080p Full HD",
                  "720": "720p HD", "480": "480p Estandar"}
        print(f"[~] Calidad solicitada : {labels.get(h, h + 'p')}")
    else:
        print("[~] Calidad solicitada : Maxima disponible (4K / Best)")


last_cmd = ""
while True:
    try:
        clip = subprocess.check_output(["termux-clipboard-get"]).decode("utf-8").strip()
        if clip.startswith("##VELOCE##") and clip != last_cmd:
            last_cmd = clip
            cmd = clip.replace("##VELOCE##", "").strip()
            print("\n[>] Comando de descarga recibido!")
            mostrar_calidad_solicitada(cmd)
            print("    yt-dlp mostrara '[CALIDAD REAL]' justo antes de descargar cada archivo.")
            print("    Compara ambas lineas para verificar que coincidan.")

            rc = subprocess.run(cmd, shell=True).returncode

            # Autoreparacion yt-dlp: actualiza y reintenta con cliente alterno (arregla el HTTP 403)
            if rc != 0 and "yt-dlp" in cmd:
                print("[!] Fallo la descarga. Actualizando yt-dlp a la ultima version...")
                subprocess.run("pip install --upgrade --quiet yt-dlp", shell=True)
                cmd2 = cmd if "player_client" in cmd else cmd.replace("yt-dlp", "yt-dlp " + YT_ARGS, 1)
                print("[~] Reintentando descarga con cliente alterno...")
                rc = subprocess.run(cmd2, shell=True).returncode

            # Autoreparacion Spotify: motor secundario via YouTube Music
            if rc != 0 and "spotdl" in cmd and "spotify.com" in cmd:
                print("[!] Spotdl fallo. Motor secundario via YouTube Music...")
                url_match = re.search(r'https?://[^\s"]+', cmd)
                if url_match:
                    meta = obtener_meta_spotify(url_match.group(0))
                    if meta:
                        print(f"[?] Cancion identificada: '{meta}'")
                        rc = subprocess.run([
                            "yt-dlp", "-x", "--audio-format", "mp3", "--audio-quality", "0",
                            "-P", "/sdcard/Download", "-o", "%(title)s.%(ext)s", f"ytsearch1:{meta}"
                        ]).returncode

            if rc == 0:
                print("[OK] Descarga COMPLETADA. Archivo guardado en /sdcard/Download")
            else:
                print("[X] FALLO la descarga. Prueba otra calidad o revisa el enlace.")
    except Exception:
        pass
    time.sleep(1.5)
