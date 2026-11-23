#!/usr/bin/env python3
"""carrusel-pro · la letra de tu marca (o la que pidas), para que tus carruseles no se vean como los de todos.

  python3 fuentes.py bajar "<Nombre de la letra>" [carpeta=fuentes-marca]
      → la baja de Google Fonts (gratis, licencia libre): normal, negrita y cursiva si existen.
        Imprime:  FUENTES {"titulo": ruta, "texto": ruta, "fuerte": ruta, "titulo_it": ruta}   (va directo a marca.fuentes)
        o  NADA <motivo>  (no está en Google Fonts: que te pase su archivo .ttf/.otf, o elige una parecida)
  python3 fuentes.py muestra "<Letra 1>" "<Letra 2>" "<Letra 3>" [--texto "Tu título"] [--carpeta C]
      → muestras.jpg con el mismo título en cada letra, para elegir viéndolas
  python3 fuentes.py ideas
      → letras gratis recomendadas por personalidad (elegante, moderna, divertida, a mano, de impacto)

Sus propios archivos (.ttf/.otf) se usan tal cual en marca.fuentes, sin bajar nada.
"""
import json, os, re, sys, urllib.parse, urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
UA_TTF = "Mozilla/4.0"          # con este navegador viejo, Google Fonts entrega .ttf (que Pillow sí lee)

# letras de marcas conocidas (de pago o propias) → la gratis que más se parece
PARECIDAS = {
    "sohne": "Inter", "söhne": "Inter", "circular": "Manrope", "gotham": "Montserrat", "proxima": "Montserrat",
    "futura": "Jost", "avenir": "Nunito Sans", "helvetica": "Inter", "sf": "Inter", "graphik": "Inter",
    "brandon": "Raleway", "gilroy": "Plus Jakarta Sans", "din": "Barlow", "akzidenz": "Inter", "garamond": "EB Garamond",
    "caslon": "Libre Caslon Text", "didot": "Playfair Display", "bodoni": "Bodoni Moda", "neue": "Inter",
}

IDEAS = {
    "Elegante (premium, comida, moda)": ["Playfair Display", "DM Serif Display", "Cormorant Garamond", "Fraunces"],
    "Moderna (tecnología, servicios)": ["Montserrat", "Manrope", "Inter", "Space Grotesk"],
    "Amigable (educación, niños, salud)": ["Nunito", "Fredoka", "Quicksand", "Baloo 2"],
    "A mano (cercana, tips)": ["Caveat", "Kalam", "Patrick Hand", "Gochi Hand"],
    "De impacto (ventas, deporte, jóvenes)": ["Bebas Neue", "Anton", "Archivo Black", "Oswald"],
}


def css(familia, pesos):
    q = urllib.parse.quote_plus(familia) + ":ital,wght@" + ";".join(pesos)
    req = urllib.request.Request(f"https://fonts.googleapis.com/css2?family={q}", headers={"User-Agent": UA_TTF})
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read().decode("utf-8", "ignore")


def bajar(familia, carpeta):
    familia = re.sub(r"\s+", " ", familia.strip().strip("'\""))
    texto = ""
    for pesos in (["0,400", "0,700", "1,400"], ["0,400", "0,700"], ["0,400"], ["0,700"]):
        try:
            texto = css(familia, pesos)
            break
        except Exception:
            continue
    if not texto:
        return None
    bloques = re.findall(r"@font-face\s*{([^}]*)}", texto)
    caras = {}
    for b in bloques:
        url = re.search(r"url\((https://[^)]+\.ttf)\)", b)
        if not url:
            continue
        estilo = "italic" if "italic" in b else "normal"
        peso = int((re.search(r"font-weight:\s*(\d+)", b) or [0, 400])[1])
        caras[(estilo, peso)] = url.group(1)
    if not caras:
        return None
    os.makedirs(carpeta, exist_ok=True)
    base = re.sub(r"[^A-Za-z0-9]+", "", familia)
    rutas = {}
    for (estilo, peso), url in caras.items():
        ruta = os.path.join(carpeta, f"{base}-{'Italic' if estilo == 'italic' else ''}{peso}.ttf")
        req = urllib.request.Request(url, headers={"User-Agent": UA_TTF})
        with urllib.request.urlopen(req, timeout=20) as r, open(ruta, "wb") as f:
            f.write(r.read())
        rutas[(estilo, peso)] = ruta
    normal = [k for k in rutas if k[0] == "normal"]
    reg = rutas.get(("normal", 400)) or rutas[min(normal, key=lambda k: abs(k[1] - 400))] if normal else list(rutas.values())[0]
    neg = rutas.get(("normal", 700)) or (rutas[max(normal, key=lambda k: k[1])] if normal else reg)
    ita = rutas.get(("italic", 400)) or neg
    serif = bool(re.search(r"serif|garamond|playfair|lora|fraunces|merriweather|cormorant|bodoni|libre baskerville|"
                           r"crimson|prata|cinzel|abril", familia, re.I)) and not re.search(r"sans", familia, re.I)
    de_titulo = len(normal) < 2 or bool(re.search(r"bebas|anton|oswald|caveat|kalam|hand|marker|pacifico|lobster|"
                                                   r"archivo black|display|script|bangers", familia, re.I))
    if serif:      # serif de marca: el título en normal + su cursiva; el texto chico sigue en una letra limpia
        return {"titulo": reg, "titulo_it": ita, "_solo_titulo": True}
    if de_titulo:  # letras de impacto o a mano: solo para títulos (en párrafos se leen mal)
        return {"titulo": neg, "titulo_it": neg, "_solo_titulo": True}
    return {"titulo": neg, "titulo_it": neg, "texto": reg, "fuerte": neg}


def muestra(familias, titulo, carpeta):
    from PIL import Image, ImageDraw, ImageFont
    filas = []
    for fam in familias:
        r = bajar(fam, os.path.join(carpeta, "fuentes"))
        filas.append((fam, r))
    W, alto = 1200, 230
    im = Image.new("RGB", (W, alto * len(filas) + 40), (250, 250, 248))
    d = ImageDraw.Draw(im)
    chica = ImageFont.truetype(os.path.join(AQUI, "..", "fuentes", "InstrumentSans-Bold.ttf"), 28)
    for i, (fam, r) in enumerate(filas):
        y = 20 + i * alto
        d.text((50, y + 14), f"{i + 1} · {fam}", font=chica, fill=(110, 110, 110))
        if r:
            f = ImageFont.truetype(r["titulo"], 92)
            d.text((50, y + 60), titulo, font=f, fill=(17, 17, 17))
        else:
            d.text((50, y + 80), "(no está en Google Fonts)", font=chica, fill=(200, 60, 50))
        d.line([50, y + alto - 6, W - 50, y + alto - 6], fill=(225, 225, 225), width=2)
    ruta = os.path.join(carpeta, "muestras.jpg")
    os.makedirs(carpeta, exist_ok=True)
    im.save(ruta, quality=90)
    return ruta, filas


def main():
    a = sys.argv[1:]
    if not a or a[0] not in ("bajar", "muestra", "ideas"):
        print(__doc__); sys.exit(1)
    if a[0] == "ideas":
        for k, v in IDEAS.items():
            print(f"{k}: {', '.join(v)}")
    elif a[0] == "bajar":
        if len(a) < 2:
            print(__doc__); sys.exit(1)
        r = bajar(a[1], a[2] if len(a) > 2 else "fuentes-marca")
        print("FUENTES " + json.dumps(r, ensure_ascii=False) if r else
              f"NADA «{a[1]}» no está en Google Fonts. Pídele su archivo .ttf/.otf o elige una parecida (fuentes.py ideas).")
    else:
        titulo = a[a.index("--texto") + 1] if "--texto" in a else "Tu carrusel, con tu letra"
        carpeta = a[a.index("--carpeta") + 1] if "--carpeta" in a else "letras"
        fams = [x for i, x in enumerate(a[1:], 1) if not x.startswith("--") and a[i - 1] not in ("--texto", "--carpeta")]
        ruta, filas = muestra(fams[:4], titulo, carpeta)
        print(f"MUESTRA {ruta}")
        for fam, r in filas:
            print(f"FUENTES {fam} " + json.dumps(r, ensure_ascii=False) if r else f"NADA {fam}")
    try:
        import version; version.avisar()
    except Exception:
        pass


if __name__ == "__main__":
    main()
