#!/usr/bin/env python3
"""carrusel-pro · baja imágenes reales y libres de uso, y logos reales de marcas y apps.

  python3 imagenes.py fotos "<qué buscas>" [cuántas=4] [carpeta=imagenes]
      → fotos libres de uso (Wikimedia Commons; si no responde, Openverse). Guarda los créditos en creditos.txt.
  python3 imagenes.py logo "<marca o app>" [carpeta=imagenes] [--dominio ejemplo.com]
      → el logo real (Wikimedia Commons). Si no está, el ícono oficial de su página (con --dominio, o el conocido).

Sin claves ni cuentas. Imprime una línea por archivo:  FOTO <ruta> | <autor> | <licencia>   o   LOGO <ruta> | <fuente>
Si no encuentra nada:  NADA <motivo>   (sin internet, o la búsqueda no dio resultados).

Reglas: las fotos son de licencias libres (CC0, CC BY, CC BY-SA o dominio público) y se da crédito en la descripción
cuando la licencia lo pide. Los logos de marcas se usan solo para NOMBRAR esa marca o app (p. ej. «hazlo en Canva»),
nunca para hacer parecer que la marca patrocina o firma el carrusel.
"""
import io, json, os, re, sys, urllib.parse, urllib.request

try:
    from PIL import Image
except ImportError:
    print("FALTA Pillow: pip install pillow"); sys.exit(1)

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
UA = "carrusel-pro/2.0 (https://github.com/dakexplica/dak-carrusel-pro)"
LIBRES = ("cc0", "public domain", "pd", "cc by", "cc-by", "cc by-sa", "cc-by-sa", "no restrictions")

# dominios de apps conocidas, para el ícono de respaldo
DOMINIOS = {
    "instagram": "instagram.com", "tiktok": "tiktok.com", "whatsapp": "whatsapp.com", "facebook": "facebook.com",
    "youtube": "youtube.com", "linkedin": "linkedin.com", "x": "x.com", "twitter": "x.com", "canva": "canva.com",
    "adobe express": "adobe.com", "google drive": "drive.google.com", "gmail": "gmail.com", "claude": "claude.ai",
    "chatgpt": "chatgpt.com", "notion": "notion.so", "spotify": "spotify.com", "shopify": "shopify.com",
    "mercado libre": "mercadolibre.com", "amazon": "amazon.com", "netflix": "netflix.com", "uber": "uber.com",
    "gemini": "gemini.google.com", "excel": "microsoft.com", "telegram": "telegram.org", "pinterest": "pinterest.com",
}


def pedir(url, timeout=15, limite=12_000_000):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(limite)


def nombre_archivo(t):
    t = re.sub(r"[^a-z0-9]+", "-", t.lower().encode("ascii", "ignore").decode()).strip("-")
    return t[:40] or "imagen"


def limpia_html(t):
    return re.sub(r"<[^>]+>", "", t or "").strip()


def commons(busqueda, cuantas, ancho, extra=""):
    q = urllib.parse.urlencode({
        "action": "query", "format": "json", "generator": "search", "gsrnamespace": 6,
        "gsrsearch": f"{busqueda} {extra}".strip(), "gsrlimit": max(10, cuantas * 4),
        "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiurlwidth": ancho,
        "iiextmetadatafilter": "LicenseShortName|Artist|UsageTerms"})
    datos = json.loads(pedir("https://commons.wikimedia.org/w/api.php?" + q))
    paginas = sorted((datos.get("query", {}).get("pages", {}) or {}).values(), key=lambda p: p.get("index", 99))
    res = []
    for p in paginas:
        ii = (p.get("imageinfo") or [{}])[0]
        md = ii.get("extmetadata", {})
        lic = limpia_html(md.get("LicenseShortName", {}).get("value", ""))
        res.append({"url": ii.get("thumburl") or ii.get("url"), "w": ii.get("width", 0), "h": ii.get("height", 0),
                    "autor": limpia_html(md.get("Artist", {}).get("value", ""))[:80] or "Wikimedia Commons",
                    "licencia": lic or "ver página", "pagina": ii.get("descriptionurl", ""), "titulo": p.get("title", "")})
    return res


def openverse(busqueda, cuantas):
    q = urllib.parse.urlencode({"q": busqueda, "page_size": max(8, cuantas * 3), "license_type": "commercial"})
    datos = json.loads(pedir("https://api.openverse.org/v1/images/?" + q, timeout=12))
    return [{"url": r.get("url"), "w": r.get("width") or 0, "h": r.get("height") or 0,
             "autor": (r.get("creator") or "Openverse")[:80], "licencia": f"CC {r.get('license', '').upper()}".strip(),
             "pagina": r.get("foreign_landing_url", ""), "titulo": r.get("title", "")} for r in datos.get("results", [])]


def fotos(busqueda, cuantas, carpeta):
    os.makedirs(carpeta, exist_ok=True)
    lista = []
    for fuente in (lambda: commons(busqueda, cuantas, 1600, "filetype:bitmap"), lambda: openverse(busqueda, cuantas)):
        try:
            lista = [r for r in fuente() if r["url"]]
        except Exception:
            lista = []
        lista = [r for r in lista if any(k in r["licencia"].lower() for k in LIBRES) and (r["w"] or 9999) >= 800]
        if lista:
            break
    if not lista:
        print("NADA no encontré fotos libres para eso (o no hay internet). Prueba con otras palabras, en inglés suele dar más.")
        raise SystemExit(3)
    creditos, n = [], 0
    for r in lista:
        if n >= cuantas:
            break
        try:
            im = Image.open(io.BytesIO(pedir(r["url"])))
            im.load()
        except Exception:
            continue
        if min(im.size) < 500:
            continue
        n += 1
        ruta = os.path.join(carpeta, f"{nombre_archivo(busqueda)}-{n}.jpg")
        im.convert("RGB").save(ruta, quality=88)
        print(f"FOTO {ruta} | {r['autor']} | {r['licencia']} | {r['titulo'][5:70]}")
        creditos.append(f"{os.path.basename(ruta)} · {r['autor']} · {r['licencia']} · {r['pagina']}")
    if creditos:
        with open(os.path.join(carpeta, "creditos.txt"), "a", encoding="utf-8") as f:
            f.write("\n".join(creditos) + "\n")
    else:
        print("NADA las fotos encontradas no se pudieron bajar. Prueba otra búsqueda.")


# Logos revisados a mano (archivo exacto en Wikimedia). Lo más usado en carruseles de IA y redes.
CONOCIDOS = {
    "instagram": "Instagram logo 2022.svg", "tiktok": "Tiktok icon.svg", "whatsapp": "WhatsApp.svg",
    "linkedin": "LinkedIn icon.svg", "facebook": "2023 Facebook icon.svg", "youtube": "YouTube full-color icon (2017).svg",
    "x": "X logo 2023.svg", "twitter": "X logo 2023.svg", "claude": "Claude AI symbol.svg",
    "google drive": "Google Drive icon (2020).svg", "drive": "Google Drive icon (2020).svg",
    "adobe express": "Adobe Express 2026 icon.svg", "gmail": "Gmail icon (2020).svg", "chatgpt": "ChatGPT-Logo.svg",
    "openai": "ChatGPT-Logo.svg", "notion": "Notion-logo.svg", "spotify": "Spotify icon.svg",
    "shopify": "Shopify logo 2018.svg", "telegram": "Telegram logo.svg", "pinterest": "Pinterest-logo.png",
    "gemini": "Google Gemini logo.svg", "excel": "Microsoft Office Excel (2019–present).svg",
    "google calendar": "Google Calendar icon (2020).svg", "threads": "Threads (app) logo.svg",
    "canva": ("en.wikipedia.org", "Canva Logo.svg"),
    "netflix": "Netflix 2015 logo.svg", "amazon": "Amazon logo.svg", "uber": "Uber logo 2018.svg",
    "google calendar": "Google Calendar icon (2020).svg", "calendar": "Google Calendar icon (2020).svg",
}


def archivo_wiki(wiki, nombre, ancho=600):
    q = urllib.parse.urlencode({"action": "query", "format": "json", "titles": "File:" + nombre,
                                "prop": "imageinfo", "iiprop": "url", "iiurlwidth": ancho})
    paginas = json.loads(pedir(f"https://{wiki}/w/api.php?" + q))["query"]["pages"].values()
    p = list(paginas)[0]
    return p["imageinfo"][0]["thumburl"] if "imageinfo" in p else None


def puntaje(titulo, marca):
    t = titulo.lower().replace("file:", "").replace("_", " ")
    m = marca.lower()
    if m not in t:
        return -99
    pts = 3 if t.startswith(m) else 0
    pts += 2 if re.search(r"\b(logo|icon|symbol|isotipo|logotipo)\b", t) else 0
    pts -= 6 if re.search(r"combined|with|parody|fan|wikipedia|user|screenshot|old|former|antiguo|19\d\d|200\d|201[0-6]", t) else 0
    return pts


def guardar(url, ruta):
    im = Image.open(io.BytesIO(pedir(url)))
    im.load()
    im.convert("RGBA").save(ruta)


def logo(marca, carpeta, dominio=None):
    os.makedirs(carpeta, exist_ok=True)
    ruta = os.path.join(carpeta, f"logo-{nombre_archivo(marca)}.png")
    clave = marca.lower().strip()
    # 1) los revisados a mano
    if clave in CONOCIDOS:
        wiki, archivo = CONOCIDOS[clave] if isinstance(CONOCIDOS[clave], tuple) else ("commons.wikimedia.org", CONOCIDOS[clave])
        try:
            url = archivo_wiki(wiki, archivo)
            if url:
                guardar(url, ruta)
                print(f"LOGO {ruta} | logo oficial ({archivo})"); return
        except Exception:
            pass
    # 2) búsqueda en Wikimedia, quedándose solo con archivos que se llaman como la marca
    try:
        cand = commons(f"{marca} logo", 4, 600, "filetype:drawing") + commons(f"{marca} icon", 2, 600, "filetype:drawing")
    except Exception:
        cand = []
    cand = sorted([r for r in cand if puntaje(r["titulo"], marca) >= 3], key=lambda r: -puntaje(r["titulo"], marca))
    for r in cand:
        try:
            guardar(r["url"], ruta)
            print(f"LOGO {ruta} | Wikimedia Commons ({r['titulo']}) · revísalo con la vista: puede ser una versión vieja"); return
        except Exception:
            continue
    # 3) el ícono de su página
    dominio = dominio or DOMINIOS.get(clave)
    if dominio:
        try:
            im = Image.open(io.BytesIO(pedir(f"https://www.google.com/s2/favicons?domain={dominio}&sz=256")))
            im.load()
            if min(im.size) >= 96:
                im.convert("RGBA").save(ruta)
                print(f"LOGO {ruta} | ícono de {dominio} (pequeño: úsalo chico)"); return
        except Exception:
            pass
    print(f"NADA no encontré el logo de {marca}. Pide el PNG (mejor sin fondo) o su página web (--dominio ejemplo.com).")
    raise SystemExit(3)


def main():
    a = sys.argv[1:]
    if len(a) < 2 or a[0] not in ("fotos", "logo"):
        print(__doc__); sys.exit(1)
    if a[0] == "fotos":
        cuantas = int(a[2]) if len(a) > 2 and a[2].isdigit() else 4
        carpeta = a[3] if len(a) > 3 else (a[2] if len(a) > 2 and not a[2].isdigit() else "imagenes")
        fotos(a[1], min(cuantas, 10), carpeta)
    else:
        dominio = None
        if "--dominio" in a:
            i = a.index("--dominio"); dominio = a[i + 1]; del a[i:i + 2]
        logo(a[1], a[2] if len(a) > 2 else "imagenes", dominio)
    try:
        import version; version.avisar()
    except Exception:
        pass


if __name__ == "__main__":
    main()
