#!/usr/bin/env python3
"""carrusel-pro · saca la marca de una página web o de capturas (por ejemplo, de tu perfil de Instagram).

  python3 marca.py web <link> [carpeta]           → lee la página: nombre, colores, logo, tipo de letra y fotos
  python3 marca.py carpeta <su carpeta> [carpeta]  → su carpeta de marca: logo, fotos, letras (.ttf/.otf) y colores
                                                  (de un .txt con #códigos o del logo). Solo la lee; nada se mueve.
                                                  Deja también tus-fotos.jpg (sus fotos con número, para elegir).
  python3 marca.py archivos <archivo o carpeta> [<más>…] --carpeta C
                                                  → lo mismo con lo que te haya dado como sea: imágenes arrastradas al chat,
                                                    archivos subidos a la app, varias carpetas o todo mezclado.
  python3 marca.py capturas <img> [<img>…] [--carpeta C]
                                                  → saca los colores de capturas (perfil de Instagram, tu feed, tu logo…)

Deja en la carpeta (por defecto ./marca):
  marca.json      → {"nombre", "usuario", "web", "colores": {fondo, tinta, acento}, "logo", "estilo_sugerido",
                     "letra_web", "paleta": [...], "fotos": [...]}
  logo.png        → el logo (si se encontró)
  fotos/          → hasta 6 fotos grandes de la página (solo de la página que te dieron)
  marca.jpg       → vista rápida: paleta + logo + nombre, para enseñarla y que la persona confirme

Solo lee páginas públicas, sin contraseñas ni cuentas. No sube nada a ningún lado.
Instagram no deja leer perfiles sin entrar a la cuenta: para Instagram se usan capturas (o el link de la bio).
Necesita Pillow. Solo librería estándar para internet.
"""
import colorsys, html, io, json, os, re, sys, urllib.parse, urllib.request
from collections import Counter

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("FALTA Pillow: pip install pillow"); sys.exit(1)

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
FUENTES = os.path.join(AQUI, "..", "fuentes")


# ---------- red ----------
def bajar(url, limite=6_000_000, timeout=12):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "es,en;q=0.8"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        datos = r.read(limite + 1)
        tipo = r.headers.get("Content-Type", "")
        final = r.geturl()
    if len(datos) > limite:
        raise ValueError("archivo demasiado grande")
    return datos, tipo, final


def imagen(url):
    try:
        datos, tipo, _ = bajar(url)
        if "svg" in tipo or url.lower().split("?")[0].endswith(".svg"):
            return None                      # Pillow no lee SVG: se usa otra fuente
        im = Image.open(io.BytesIO(datos))
        im.load()
        return im
    except Exception:
        return None


# ---------- colores ----------
def hexa(c):
    return "#%02X%02X%02X" % tuple(int(v) for v in c[:3])


def rgb(h):
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def luz(c):
    r, g, b = [v / 255 for v in c[:3]]
    f = lambda v: v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contraste(a, b):
    la, lb = sorted([luz(a), luz(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


def satur(c):
    h, l, s = colorsys.rgb_to_hls(*[v / 255 for v in c[:3]])
    return s * (1 - abs(2 * l - 1))          # croma: qué tan "de color" es


def gris(c):
    return satur(c) < 0.12


def paleta_de_imagen(im, n=8):
    im = im.convert("RGBA")
    im.thumbnail((240, 240))
    fondo = Image.new("RGBA", im.size, (255, 255, 255, 255))
    fondo.alpha_composite(im)
    q = fondo.convert("RGB").quantize(colors=n, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()[:n * 3]
    cuenta = sorted(q.getcolors(), reverse=True)
    return [(tuple(pal[i * 3:i * 3 + 3]), k) for k, i in cuenta]


def elegir_colores(candidatos):
    """candidatos: lista de (rgb, peso). Devuelve fondo, tinta y acento con buen contraste."""
    total = Counter()
    for c, p in candidatos:
        total[tuple(c)] += p
    orden = [c for c, _ in total.most_common()]
    acentos = sorted([c for c in orden if not gris(c) and 0.05 < luz(c) < 0.8],
                     key=lambda c: -(total[c] ** 0.5) * (0.4 + satur(c)))
    acento = acentos[0] if acentos else (226, 61, 46)
    claros = [c for c in orden if luz(c) > 0.75]
    oscuros = [c for c in orden if luz(c) < 0.06]
    fondo = claros[0] if claros else (250, 250, 248)
    if gris(fondo) is False and satur(fondo) > 0.25:  # fondo muy de color: se suaviza para que se lea
        fondo = tuple(int(v * 0.12 + 255 * 0.88) for v in fondo)
    tinta = oscuros[0] if oscuros else (17, 17, 17)
    if contraste(fondo, tinta) < 7:
        tinta = (17, 17, 17)
    # el acento se deja EXACTO (es el color de la marca); si se lee poco sobre el fondo, el motor
    # usa una versión más oscura solo para las palabras resaltadas.
    return {"fondo": hexa(fondo), "tinta": hexa(tinta), "acento": hexa(acento)}, [hexa(c) for c in orden[:8]]


# ---------- leer la página ----------
def meta(doc, *nombres):
    for n in nombres:
        m = re.search(r'<meta[^>]+(?:property|name)=["\']%s["\'][^>]*>' % re.escape(n), doc, re.I)
        if m:
            c = re.search(r'content=["\']([^"\']*)["\']', m.group(0), re.I)
            if c and c.group(1).strip():
                return html.unescape(c.group(1).strip())
    return ""


def colores_css(texto):
    cuenta = Counter()
    for h in re.findall(r'#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b', texto):
        try:
            cuenta[rgb(h)] += 1
        except ValueError:
            pass
    for r, g, b in re.findall(r'rgba?\(\s*(\d{1,3})[ ,]+(\d{1,3})[ ,]+(\d{1,3})', texto):
        cuenta[(int(r), int(g), int(b))] += 1
    return cuenta


def letra(texto):
    """La letra principal de la página: primero la que carga de Google Fonts (la más fiable), luego la más usada."""
    m = re.search(r'fonts\.googleapis\.com/css2?\?family=([^&:"\'|]+)', texto)
    if m:
        return urllib.parse.unquote_plus(m.group(1)).strip()
    cuenta = Counter()
    for f in re.findall(r'font-family\s*:\s*([^;}{]+)', texto, re.I):
        nombre = f.split(",")[0].strip().strip("'\"")
        if len(nombre) > 2 and not nombre.startswith("var(") and not re.search(
                r"awesome|icon|material|symbol|emoji|glyph|monospace|courier|consolas", nombre, re.I) and nombre.lower() not in (
                "inherit", "initial", "unset", "sans-serif", "serif", "system-ui", "-apple-system", "blinkmacsystemfont",
                "arial", "helvetica", "helvetica neue", "segoe ui", "roboto", "times new roman"):
            cuenta[nombre] += 1
    return cuenta.most_common(1)[0][0] if cuenta else ""


def estilo_para(nombre_letra, colores):
    n = (nombre_letra or "").lower()
    if any(k in n for k in ("serif", "garamond", "playfair", "lora", "georgia", "times", "cormorant", "dm serif")) \
            and "sans" not in n:
        return "editorial"
    if any(k in n for k in ("caveat", "kalam", "hand", "marker", "patrick", "indie")):
        return "cuaderno"
    if luz(rgb(colores["fondo"])) < 0.2:
        return "bloque"
    return "minimal"


def web(url, carpeta):
    if not re.match(r"https?://", url):
        url = "https://" + url
    if "instagram.com" in url or "tiktok.com" in url:
        print("INSTAGRAM: Instagram y TikTok no dejan leer perfiles sin entrar a la cuenta. "
              "Pide una captura del perfil (marca.py capturas …) o el link de su página (el de la bio).")
        sys.exit(2)
    try:
        datos, tipo, final = bajar(url, limite=3_000_000)
    except Exception as e:
        print(f"NO_ABRE: no pude abrir {url} ({e.__class__.__name__}). Revisa el link o usa capturas.")
        sys.exit(3)
    doc = datos.decode("utf-8", "ignore")
    base = final
    os.makedirs(carpeta, exist_ok=True)

    nombre = meta(doc, "og:site_name", "application-name") or \
        html.unescape((re.search(r"<title[^>]*>([^<]{1,90})", doc, re.I) or [None, ""])[1]).split("|")[0].split(" - ")[0].strip()
    nombre = re.split(r"\s[·|–—-]\s", nombre)[0].strip()

    # CSS: el de la página + hasta 3 hojas de estilo propias
    css = " ".join(re.findall(r"<style[^>]*>(.*?)</style>", doc, re.S | re.I))
    css += " " + " ".join(re.findall(r'style=["\']([^"\']+)["\']', doc))
    hojas = re.findall(r'<link[^>]+rel=["\']?stylesheet["\']?[^>]*>', doc, re.I)
    for h in hojas[:3]:
        m = re.search(r'href=["\']([^"\']+)', h)
        if m:
            try:
                css += " " + bajar(urllib.parse.urljoin(base, html.unescape(m.group(1))), limite=1_500_000)[0].decode("utf-8", "ignore")
            except Exception:
                pass
    candidatos = []
    # lo que la página declara para su fondo y su texto (body/html/:root) es lo más fiable
    fondo_dec = tinta_dec = None
    for bloque in re.findall(r'(?:^|[}\s])(?:body|html|:root)\s*\{([^}]*)\}', css, re.I):
        mb = re.search(r'background(?:-color)?\s*:\s*(#[0-9a-fA-F]{3,6})\b', bloque)
        mc = re.search(r'(?<![-\w])color\s*:\s*(#[0-9a-fA-F]{3,6})\b', bloque)
        if mb and not fondo_dec: fondo_dec = rgb(mb.group(1))
        if mc and not tinta_dec: tinta_dec = rgb(mc.group(1))
    tema = meta(doc, "theme-color")
    if re.match(r"#[0-9a-fA-F]{3,6}$", tema or ""):
        candidatos.append((rgb(tema), 60))
    for c, k in colores_css(css).most_common(14):
        candidatos.append((c, min(k, 40)))

    # logo: icono grande de la página, luego <img> con "logo"
    rutas_logo = []
    for tag in re.findall(r"<link[^>]+>", doc, re.I):
        if re.search(r'rel=["\'][^"\']*(apple-touch-icon|icon)[^"\']*["\']', tag, re.I):
            m = re.search(r'href=["\']([^"\']+)', tag)
            t = re.search(r'sizes=["\'](\d+)', tag)
            if m:
                rutas_logo.append((int(t.group(1)) if t else (180 if "apple" in tag.lower() else 32), m.group(1)))
    # <img> con "logo": solo cuenta como SU logo si lleva el nombre de la marca o del dominio
    # (una página puede mostrar logos de otras marcas: clientes, patrocinadores, "trabajo en…")
    dominio = urllib.parse.urlparse(base).netloc
    claves = {t for t in re.findall(r"[a-z0-9]{3,}", (nombre + " " + dominio.split(".")[-2 if dominio.count(".") else 0]).lower())
              if t not in ("www", "com", "the", "los", "las")}
    otros = []
    for tag in re.findall(r"<img[^>]+>", doc, re.I):
        if re.search(r"logo", tag, re.I):
            m = re.search(r'src=["\']([^"\']+)', tag)
            if m and not m.group(1).startswith("data:"):
                if any(k in tag.lower() for k in claves):
                    rutas_logo.append((150, m.group(1)))
                else:
                    otros.append((10, m.group(1)))
    logo = None
    for _, r in sorted(rutas_logo, key=lambda x: -x[0]):
        im = imagen(urllib.parse.urljoin(base, html.unescape(r)))
        if im and min(im.size) >= 64:
            logo = im
            break
    if logo is None:                          # el ícono oficial de su página antes que un logo dudoso
        im = imagen(f"https://www.google.com/s2/favicons?domain={dominio}&sz=256")
        if im and min(im.size) >= 96:
            logo = im
    if logo is None and len(otros) == 1:      # un solo logo en toda la página: casi seguro es el suyo
        im = imagen(urllib.parse.urljoin(base, html.unescape(otros[0][1])))
        if im and min(im.size) >= 64:
            logo = im
    ruta_logo = ""
    if logo:
        logo = logo.convert("RGBA")
        logo.thumbnail((600, 600))
        ruta_logo = os.path.join(carpeta, "logo.png")
        logo.save(ruta_logo)
        for c, k in paleta_de_imagen(logo, 6):        # el color del logo es lo más fiable de una marca
            candidatos.append((c, min(k // 20, 90)))

    # fotos de la propia página (og:image primero)
    fotos, vistas = [], set()
    og = meta(doc, "og:image", "twitter:image")
    srcs = ([og] if og else []) + [m for m in re.findall(r'<img[^>]+src=["\']([^"\']+)', doc, re.I)]
    os.makedirs(os.path.join(carpeta, "fotos"), exist_ok=True)
    for s in srcs:
        if len(fotos) >= 6:
            break
        if not s or s.startswith("data:") or re.search(r"logo|icon|sprite|pixel|avatar", s, re.I):
            continue
        u = urllib.parse.urljoin(base, html.unescape(s))
        if u in vistas:
            continue
        vistas.add(u)
        im = imagen(u)
        if im and min(im.size) >= 400:
            if im.mode in ("RGBA", "LA", "P"):
                im = im.convert("RGBA"); fondo_b = Image.new("RGBA", im.size, (255, 255, 255, 255))
                fondo_b.alpha_composite(im); im = fondo_b
            from PIL import ImageStat
            if max(ImageStat.Stat(im.convert("L").resize((64, 64))).stddev) < 12:
                continue                                       # imagen lisa (fondo, degradado): no sirve como foto
            ruta = os.path.join(carpeta, "fotos", f"foto-{len(fotos) + 1}.jpg")
            im.convert("RGB").save(ruta, quality=88)
            fotos.append(ruta)
            if len(fotos) == 1:
                for c, k in paleta_de_imagen(im, 6):
                    candidatos.append((c, min(k // 80, 12)))

    colores, paleta = elegir_colores(candidatos)
    oscura = bool(fondo_dec and luz(fondo_dec) < 0.06)        # página de fondo oscuro (gimnasios, tech, moda)
    if fondo_dec and (luz(fondo_dec) > 0.6 or oscura):
        colores["fondo"] = hexa(fondo_dec)
    if oscura:
        colores["tinta"] = hexa(tinta_dec) if tinta_dec and luz(tinta_dec) > 0.6 else "#FFFFFF"
    elif tinta_dec and contraste(tinta_dec, rgb(colores["fondo"])) >= 7:
        colores["tinta"] = hexa(tinta_dec)
    # el color de marca que la página declara (theme-color) manda si es un color de verdad (no gris)
    if re.match(r"#[0-9a-fA-F]{6}$", tema or "") and satur(rgb(tema)) > 0.35:
        colores["acento"] = tema.upper()
    fam = letra(doc[:60000] + " " + css)
    fuentes_marca, parecida = {}, ""
    if fam:
        try:
            import fuentes as _f
            fuentes_marca = _f.bajar(fam, os.path.join(carpeta, "fuentes")) or {}
            if not fuentes_marca:
                # letra propia de la marca (no se puede bajar): se prueba la gratis más parecida
                limpio = re.sub(r"[-_ ]?(var|vf|variable|web|display|text|pro)$", "", fam, flags=re.I)
                partes = re.findall(r"[A-Z][a-z]+|[a-z]{4,}", limpio)
                candidatas = [limpio] + [p for p in partes if len(p) >= 4]
                for c in candidatas:
                    r = _f.bajar(c, os.path.join(carpeta, "fuentes"))
                    if r:
                        fuentes_marca, parecida = r, c; break
                if not fuentes_marca:
                    c = _f.PARECIDAS.get(limpio.lower().split()[0]) if limpio else None
                    if c:
                        fuentes_marca, parecida = _f.bajar(c, os.path.join(carpeta, "fuentes")) or {}, c
        except Exception:
            fuentes_marca = {}
    datos_marca = {
        "nombre": nombre, "usuario": "", "web": base, "colores": colores, "logo": ruta_logo,
        "letra_web": fam, "letra_parecida": parecida, "fuentes": fuentes_marca,
        "estilo_sugerido": "bloque" if oscura else estilo_para(fam, colores), "paleta": paleta,
        "fotos": fotos, "descripcion": meta(doc, "og:description", "description")[:220],
    }
    return datos_marca


def capturas(rutas, carpeta):
    candidatos = []
    for r in rutas:
        try:
            im = Image.open(r)
        except Exception:
            print(f"NO_ABRE: {r}"); continue
        im = im.convert("RGB")
        w, h = im.size
        # en una captura de Instagram, lo de la marca está en la foto de perfil y en el feed; se quita la barra de arriba
        im = im.crop((0, int(h * 0.06), w, int(h * 0.94)))
        for c, k in paleta_de_imagen(im, 10):
            candidatos.append((c, k))
    if not candidatos:
        print("NO_ABRE: ninguna captura se pudo leer."); sys.exit(3)
    colores, paleta = elegir_colores(candidatos)
    return {"nombre": "", "usuario": "", "web": "", "colores": colores, "logo": "", "letra_web": "", "fuentes": {},
            "estilo_sugerido": estilo_para("", colores), "paleta": paleta, "fotos": []}


IMG_EXT = (".png", ".jpg", ".jpeg", ".webp")
LETRA_EXT = (".ttf", ".otf")


def juntar(rutas):
    """Lo que la persona dio, como lo haya dado: carpetas (se recorren), archivos sueltos (arrastrados al chat,
    subidos a la app) o una mezcla. Devuelve la lista de archivos y la carpeta que da el nombre."""
    archivos, base = [], ""
    for r in rutas:
        r = os.path.abspath(os.path.expanduser(r))
        if os.path.isdir(r):
            base = base or r
            for raiz, dirs, nombres in os.walk(r):
                dirs[:] = [d for d in dirs if not d.startswith(".")]
                if raiz[len(r):].count(os.sep) > 2:
                    continue
                archivos += [os.path.join(raiz, n) for n in nombres if not n.startswith(".")]
                if len(archivos) > 400:
                    break
        elif os.path.isfile(r):
            archivos.append(r)
        else:
            print(f"AVISO no encuentro «{r}» (¿se movió o tiene otro nombre?)")
    if not archivos:
        print("NO_ABRE: no encontré ningún archivo en lo que me diste."); sys.exit(3)
    return archivos, base


def carpeta_marca(rutas, salida):
    """Su material: logo, fotos, letras, notas y (si hay) un .txt con sus colores. Solo se LEE: nada se mueve ni se borra."""
    archivos, ruta = juntar(rutas if isinstance(rutas, list) else [rutas])
    bajo = lambda p: os.path.basename(p).lower()
    imgs = [p for p in archivos if bajo(p).endswith(IMG_EXT)]
    letras = [p for p in archivos if bajo(p).endswith(LETRA_EXT)]
    raras = [p for p in archivos if bajo(p).endswith((".heic", ".svg", ".ai", ".psd", ".eps"))]
    # su contenido: notas, textos, documentos (lo que quiere decir, aunque esté revuelto)
    textos = [p for p in archivos if bajo(p).endswith((".txt", ".md", ".docx", ".doc", ".pdf", ".pages", ".rtf"))
              and not re.search(r"^colou?res", bajo(p))]

    # logo: el que se llama logo/isotipo/marca; si no, un PNG con transparencia y casi cuadrado
    def es_logo_por_nombre(p):
        return re.search(r"logo|isotipo|logotipo|imagotipo|marca|brand|icono|icon", bajo(p)) is not None
    logo_ruta, cand = "", sorted([p for p in imgs if es_logo_por_nombre(p)], key=lambda p: (not bajo(p).endswith(".png"), len(bajo(p))))
    if not cand:
        for p in imgs:
            try:
                im = Image.open(p)
                if im.mode in ("RGBA", "LA", "P") and max(im.size) <= 2000 and 0.4 < im.width / im.height < 2.5 and \
                        im.convert("RGBA").getchannel("A").getextrema()[0] < 50:
                    cand.append(p)
            except Exception:
                pass
    if cand:
        logo_ruta = cand[0]

    candidatos = []
    # colores escritos por la persona (un .txt/.md con #códigos): mandan
    for p in archivos:
        if bajo(p).endswith((".txt", ".md")) and os.path.getsize(p) < 200_000:
            for h in re.findall(r"#([0-9a-fA-F]{6})\b", open(p, encoding="utf-8", errors="ignore").read()):
                candidatos.append((rgb(h), 400))
    if logo_ruta:
        try:
            for c, k in paleta_de_imagen(Image.open(logo_ruta), 6):
                candidatos.append((c, min(k // 20, 90)))
        except Exception:
            logo_ruta = ""

    # fotos: las suyas, grandes, que no sean el logo (se usan donde están, sin copiarlas)
    fotos = []
    for p in imgs:
        if p == logo_ruta or es_logo_por_nombre(p):
            continue
        try:
            im = Image.open(p)
            if min(im.size) >= 500:
                fotos.append((im.width * im.height, p))
        except Exception:
            pass
    fotos = [p for _, p in sorted(fotos, reverse=True)][:30]
    for p in fotos[:4]:
        try:
            for c, k in paleta_de_imagen(Image.open(p), 6):
                candidatos.append((c, min(k // 80, 10)))
        except Exception:
            pass
    if not candidatos:
        candidatos = [((250, 250, 248), 10), ((17, 17, 17), 10)]
    colores, paleta = elegir_colores(candidatos)

    # sus letras
    fuentes_m, familia = {}, ""
    if letras:
        def peso(p):
            n = bajo(p)
            return 3 if re.search(r"black|heavy|extrabold|ultra", n) else 2 if "bold" in n or "semibold" in n else \
                1 if re.search(r"medium", n) else 0
        normales = [p for p in letras if not re.search(r"italic|oblique|cursiva", bajo(p))]
        italicas = [p for p in letras if re.search(r"italic|oblique|cursiva", bajo(p))]
        reg = min(normales or letras, key=peso)
        neg = max(normales or letras, key=peso)
        try:
            from PIL import ImageFont as _IF
            familia = _IF.truetype(reg, 20).getname()[0]
        except Exception:
            familia = os.path.splitext(os.path.basename(reg))[0]
        fuentes_m = {"titulo": neg, "titulo_it": italicas[0] if italicas else neg, "texto": reg, "fuerte": neg}

    # hoja de sus fotos con número, para decir «usa la 3 en la portada»
    if fotos:
        os.makedirs(salida, exist_ok=True)
        lado, cols = 300, 5
        filas = (min(len(fotos), 15) + cols - 1) // cols
        hoja = Image.new("RGB", (cols * (lado + 16) + 16, filas * (lado + 16) + 16), (244, 245, 247))
        dh = ImageDraw.Draw(hoja)
        try:
            fn = ImageFont.truetype(os.path.join(FUENTES, "InstrumentSans-Bold.ttf"), 34)
        except Exception:
            fn = ImageFont.load_default()
        for i, p in enumerate(fotos[:15]):
            im = Image.open(p).convert("RGB")
            ld = min(im.size)
            im = im.crop(((im.width - ld) // 2, (im.height - ld) // 2, (im.width + ld) // 2, (im.height + ld) // 2)).resize((lado, lado))
            x, y = 16 + (i % cols) * (lado + 16), 16 + (i // cols) * (lado + 16)
            hoja.paste(im, (x, y))
            dh.ellipse([x + 10, y + 10, x + 62, y + 62], fill=(17, 17, 17))
            t = str(i + 1)
            dh.text((x + 36 - fn.getlength(t) / 2, y + 16), t, font=fn, fill=(255, 255, 255))
        hoja.save(os.path.join(salida, "tus-fotos.jpg"), quality=85)

    nombre = re.sub(r"[-_]+", " ", os.path.basename(ruta)).strip() if ruta else ""
    if re.search(r"^(marca|logo|logos|imagenes|imágenes|fotos|brand|assets|recursos|mi marca)$", nombre, re.I):
        nombre = ""
    if raras:
        print("AVISO estos archivos no los puedo usar directo (pídele un PNG o JPG): " +
              ", ".join(os.path.basename(p) for p in raras[:6]))
    if not logo_ruta:
        print("AVISO no vi un logo (llámalo «logo.png», mejor sin fondo)")
    return {"nombre": nombre, "usuario": "", "web": "", "colores": colores, "logo": logo_ruta, "letra_web": familia,
            "fuentes": fuentes_m, "estilo_sugerido": estilo_para(familia, colores), "paleta": paleta, "fotos": fotos,
            "carpeta_marca": ruta, "textos": textos}


def vista(m, carpeta):
    """marca.jpg: para enseñarla y que la persona diga «sí, es mi marca»."""
    W, H = 1200, 520
    fondo = rgb(m["colores"]["fondo"])
    im = Image.new("RGB", (W, H), fondo)
    d = ImageDraw.Draw(im)
    try:
        fb = ImageFont.truetype((m.get("fuentes") or {}).get("titulo") or os.path.join(FUENTES, "InstrumentSans-Bold.ttf"), 54)
        fr = ImageFont.truetype(os.path.join(FUENTES, "InstrumentSans-Regular.ttf"), 26)
    except Exception:
        fb = fr = ImageFont.load_default()
    x = 60
    if m.get("logo") and os.path.exists(m["logo"]):
        lg = Image.open(m["logo"]).convert("RGBA")
        lg.thumbnail((150, 150))
        im.paste(lg, (x, 60), lg)
        x += lg.width + 36
    d.text((x, 80), (m.get("nombre") or "Tu marca")[:28], font=fb, fill=rgb(m["colores"]["tinta"]))
    d.text((x, 150), f"Estilo: {m['estilo_sugerido']}" + (f" · tu letra: {m['letra_web']}" if m.get("letra_web") else ""),
           font=fr, fill=rgb(m["colores"]["tinta"]))
    for i, (k, etiqueta) in enumerate([("fondo", "Fondo"), ("tinta", "Texto"), ("acento", "Acento")]):
        x0 = 60 + i * 370
        c = rgb(m["colores"][k])
        d.rounded_rectangle([x0, 260, x0 + 340, 430], radius=26, fill=c, outline=rgb(m["colores"]["tinta"]), width=3)
        tc = (255, 255, 255) if luz(c) < 0.4 else (17, 17, 17)
        d.text((x0 + 24, 280), etiqueta, font=fr, fill=tc)
        d.text((x0 + 24, 380), m["colores"][k], font=fr, fill=tc)
    ruta = os.path.join(carpeta, "marca.jpg")
    im.save(ruta, quality=90)
    return ruta


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in ("web", "capturas", "carpeta", "archivos"):
        print(__doc__); sys.exit(1)
    if sys.argv[1] in ("carpeta", "archivos"):
        args = sys.argv[2:]
        carpeta = "marca"
        if "--carpeta" in args:
            i = args.index("--carpeta"); carpeta = args[i + 1]; del args[i:i + 2]
        elif sys.argv[1] == "carpeta" and len(args) == 2:
            carpeta = args.pop()                      # forma corta: carpeta <su carpeta> <salida>
        m = carpeta_marca(args, carpeta)
    elif sys.argv[1] == "web":
        carpeta = sys.argv[3] if len(sys.argv) > 3 else "marca"
        m = web(sys.argv[2], carpeta)
    else:
        args = sys.argv[2:]
        carpeta = "marca"
        if "--carpeta" in args:
            i = args.index("--carpeta"); carpeta = args[i + 1]; del args[i:i + 2]
        os.makedirs(carpeta, exist_ok=True)
        m = capturas(args, carpeta)
    os.makedirs(carpeta, exist_ok=True)
    # rutas completas: así el guion las encuentra esté donde esté
    ab = lambda r: os.path.abspath(r) if r else r
    m["logo"] = ab(m.get("logo"))
    m["fotos"] = [ab(f) for f in m.get("fotos", [])]
    m["fuentes"] = {k: (ab(v) if isinstance(v, str) else v) for k, v in (m.get("fuentes") or {}).items()}
    json.dump(m, open(os.path.join(carpeta, "marca.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("MARCA", json.dumps({k: m[k] for k in ("nombre", "colores", "logo", "estilo_sugerido", "letra_web")}, ensure_ascii=False))
    print("LETRA", (f"«{m['letra_web']}» es propia de su marca; uso la gratis más parecida: {m['letra_parecida']} (díselo)"
                    if m.get("letra_parecida") else "lista") + ": " + json.dumps(m["fuentes"], ensure_ascii=False) if m.get("fuentes") else
          (f"«{m['letra_web']}» no se puede bajar (no es de Google Fonts): pide su archivo o elige una parecida"
           if m.get("letra_web") else "no encontré su letra: usa la del estilo o pregúntale cuál quiere"))
    if m.get("textos"):
        print("TEXTOS", len(m["textos"]), "· su contenido para las láminas (léelos):", " | ".join(m["textos"][:10]))
    print("FOTOS", str(len(m["fotos"])) + (f" (sus fotos con número: {os.path.join(carpeta, 'tus-fotos.jpg')})" if "carpeta_marca" in m and m["fotos"] else ""))
    print("VISTA", vista(m, carpeta))
    try:
        import version; version.avisar()
    except Exception:
        pass


if __name__ == "__main__":
    main()
