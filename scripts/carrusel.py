#!/usr/bin/env python3
"""carrusel-pro · convierte un guion JSON en las imágenes PNG de un carrusel.

Uso:
    python3 carrusel.py guion.json [carpeta_salida]

Solo necesita Pillow (viene en Claude.ai y en casi cualquier Python: pip install pillow).
El guion trae la marca, la plantilla, el formato y las slides. Ver SKILL.md.
"""
import json, math, os, random, re, sys
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iconos
import marcos
import encuadre

AQUI = os.path.dirname(os.path.abspath(__file__))
FUENTES = os.path.join(AQUI, "..", "fuentes")

TAMANOS = {"instagram": (1080, 1350), "tiktok": (1080, 1920), "linkedin": (1080, 1350)}

# Cada plantilla define fuentes, colores por defecto y cómo se marca el *énfasis*.
PLANTILLAS = {
    "editorial": dict(titulo="InstrumentSerif-Regular.ttf", titulo_it="InstrumentSerif-Italic.ttf",
                      texto="InstrumentSans-Regular.ttf", fuerte="InstrumentSans-Bold.ttf",
                      fondo="#F4EFE6", tinta="#1B1B1B", acento="#C8102E", enfasis="italica",
                      escala_titulo=1.25),
    "minimal": dict(titulo="InstrumentSans-Bold.ttf", titulo_it="InstrumentSans-Bold.ttf",
                    texto="InstrumentSans-Regular.ttf", fuerte="InstrumentSans-Bold.ttf",
                    fondo="#FFFFFF", tinta="#111111", acento="#2F6BFF", enfasis="color",
                    escala_titulo=1.0),
    "bloque": dict(titulo="Poppins-Bold.ttf", titulo_it="Poppins-Bold.ttf",
                   texto="InstrumentSans-Regular.ttf", fuerte="Poppins-Bold.ttf",
                   fondo="#111111", tinta="#FFFFFF", acento="#FF4D2E", enfasis="caja",
                   escala_titulo=0.95),
    # «pro»: limpia y seria, para LinkedIn, consultoría, B2B y marca personal. Letra sans fuerte, sin adornos.
    "pro": dict(titulo="Manrope-ExtraBold.ttf", titulo_it="Manrope-ExtraBold.ttf",
                texto="Manrope-Regular.ttf", fuerte="Manrope-Bold.ttf",
                fondo="#FFFFFF", tinta="#0B1220", acento="#2457F5", enfasis="color",
                escala_titulo=0.9),
    "cuaderno": dict(titulo="Kalam-Bold.ttf", titulo_it="Kalam-Bold.ttf",
                     texto="InstrumentSans-Regular.ttf", fuerte="Kalam-Bold.ttf",
                     fondo="#FBF7EE", tinta="#1E2A44", acento="#E63946", enfasis="marcatextos",
                     escala_titulo=1.05),
}


# ---------- utilidades ----------
def idioma(g):
    """Idioma del carrusel: el que diga el guion ("idioma": "en") o el que se nota en sus textos."""
    if g.get("idioma"):
        return g["idioma"][:2].lower()
    txt = " ".join(str(v) for sl in g.get("slides", []) for v in sl.values() if isinstance(v, str)).lower()
    en = sum(txt.count(w) for w in (" the ", " and ", " you ", " your ", " with ", " is ", " it "))
    es = sum(txt.count(w) for w in (" el ", " la ", " de ", " que ", " y ", " tu ", " con "))
    return "en" if en > es else "es"

def hexrgb(h, a=255):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (a,)


def luz(c):
    f = lambda v: v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = [x / 255 for x in c[:3]]
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contraste(a, b):
    la, lb = sorted([luz(a), luz(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


def mezcla(c1, c2, t):
    return tuple(int(c1[i] * (1 - t) + c2[i] * t) for i in range(3)) + (255,)


def fuente(nombre, tam):
    ruta = nombre if os.path.isabs(nombre) else os.path.join(FUENTES, nombre)
    return ImageFont.truetype(ruta, int(tam))


def medio_x(nombre_fuente, tam, y):
    """Altura del centro de las letras minúsculas de una línea dibujada en y (para alinear viñetas, ✓ y ✗)."""
    bb = fuente(nombre_fuente, tam).getbbox("x")
    return y + (bb[1] + bb[3]) / 2


def centrado(d, cx, cy, t, f, fill):
    """Texto centrado EXACTO en (cx, cy), con la medida real de la letra (números en círculos y píldoras)."""
    d.text((cx, cy), t, font=f, fill=fill, anchor="mm")


def tokens(texto):
    """'Hola *mundo*: bonito' -> [('Hola', False), ('mundo', True), (':', False) pegado, ('bonito', False)].
    Devuelve (palabra, énfasis, pegado_a_la_anterior)."""
    out, previo = [], " "
    for i, trozo in enumerate(texto.split("*")):
        enf = i % 2 == 1
        for k, p in enumerate(trozo.split()):
            pegado = k == 0 and out and not trozo[:1].isspace() and not previo[-1:].isspace()
            out.append((p, enf, bool(pegado)))
        if trozo:
            previo = trozo
    return out


def ancho_linea(l, f, f_it=None, enfasis=None):
    esp = f.getlength(" ")
    tot = 0
    for j, (p, e, peg) in enumerate(l):
        ff = f_it if (f_it and e and enfasis == "italica") else f
        tot += ff.getlength(p) + (0 if (j == 0 or peg) else esp)
    return tot


def lineas(texto, f, ancho):
    """Parte el texto en renglones que caben en `ancho`. Respeta saltos con \\n."""
    res = []
    for parrafo in texto.split("\n"):
        actual, w_act = [], 0
        esp = f.getlength(" ")
        for pal, enf, peg in tokens(parrafo):
            w = f.getlength(pal)
            if actual and not peg and w_act + esp + w > ancho:
                res.append(actual)
                actual, w_act = [], 0
            actual.append((pal, enf, peg and bool(actual)))
            w_act += (esp if len(actual) > 1 and not peg else 0) + w
        # sin palabra suelta en el último renglón ("…al día / 1"): se baja una palabra del renglón de arriba
        # (solo si el renglón de arriba se queda con 2 o más palabras: si no, se crea otra palabra suelta)
        if res and len(actual) == 1 and len(res[-1]) >= 3 and not actual[0][2]:
            prueba = [res[-1][-1]] + actual
            if ancho_linea(prueba, f) <= ancho:
                res[-1], actual = res[-1][:-1], prueba
        res.append(actual)
    return res


def ajusta(texto, nombre_fuente, tam, ancho, alto, interlineado=1.12, minimo=28):
    """Baja el tamaño hasta que el texto quepa en la caja."""
    while tam > minimo:
        f = fuente(nombre_fuente, tam)
        ls = lineas(texto, f, ancho)
        if len(ls) * tam * interlineado <= alto and all(
                ancho_linea(l, f) <= ancho for l in ls):
            return f, ls, tam
        tam -= 4
    f = fuente(nombre_fuente, minimo)
    return f, lineas(texto, f, ancho), minimo


class Lienzo:
    def __init__(self, guion, n, total):
        self.g = guion
        self.formato = guion.get("_formato", "instagram")
        self.W, self.H = TAMANOS[self.formato]
        self.p = dict(PLANTILLAS[guion.get("plantilla", "editorial")])
        # la marca puede traer sus propias tipografías (archivos .ttf/.otf)
        fm = guion.get("marca", {}).get("fuentes", {})
        if fm.get("titulo"):
            self.p["titulo"] = self.p["titulo_it"] = fm["titulo"]
        if fm.get("titulo_it"):
            self.p["titulo_it"] = fm["titulo_it"]
        if fm.get("texto"):
            self.p["texto"] = fm["texto"]
        if fm.get("fuerte") or fm.get("texto"):
            self.p["fuerte"] = fm.get("fuerte", fm.get("texto"))
        colores = guion.get("marca", {}).get("colores", {})
        self.fondo = hexrgb(colores.get("fondo", self.p["fondo"]))
        self.tinta = hexrgb(colores.get("tinta", self.p["tinta"]))
        self.acento = hexrgb(colores.get("acento", self.p["acento"]))
        self.suave = mezcla(self.tinta, self.fondo, 0.45)
        # si el acento de la marca se lee poco sobre el fondo (p. ej. verde claro sobre blanco),
        # las PALABRAS resaltadas usan una versión más oscura; las figuras siguen con el color exacto.
        self.acento_txt = self.acento
        for _ in range(8):
            if contraste(self.acento_txt, self.fondo) >= 3:
                break
            self.acento_txt = mezcla(self.acento_txt, self.tinta, 0.18)
        self.n, self.total = n, total
        self.img = Image.new("RGBA", (self.W, self.H), self.fondo)
        self.d = ImageDraw.Draw(self.img)
        # zona segura: en TikTok se evita la interfaz (pestañas arriba, botones a la derecha, descripción abajo)
        if self.formato == "tiktok":
            self.x0, self.x1, self.y0, self.y1 = 90, self.W - 170, 270, 1440
        else:
            self.x0, self.x1, self.y0, self.y1 = 96, self.W - 96, 120, self.H - 150

    def dibujo(self, figuras, caja):
        """Ilustración hecha por Claude para esta slide (ver iconos.py)."""
        if not figuras:
            return
        pal = dict(tinta=self.tinta, acento=self.acento, fondo=self.fondo, suave=self.suave,
                   claro=mezcla(self.acento, self.fondo, 0.72))
        if self.g.get("plantilla") == "bloque":
            pal["claro"] = mezcla(self.acento, self.fondo, 0.55)
            pal["tinta"] = self.tinta
        iconos.dibujar(self.img, figuras, caja, pal, fuente_ttf=os.path.join(FUENTES, self.p["fuerte"]))

    # ----- fondo de cada plantilla -----
    def decorar_fondo(self, invertido=False):
        nombre = self.g.get("plantilla", "editorial")
        tipo = getattr(self, "tipo", "")
        vida = self.g.get("vida", True) and not invertido and nombre not in ("bloque", "pro")
        # «vida»: que no se vea plano ni genérico. Las láminas pares de contenido van sobre un tinte del color
        # de la marca y cada lámina lleva una forma grande de su color, que cambia de esquina para dar ritmo.
        if vida and self.n % 2 == 0 and tipo in ("punto", "lista", "pasos", "dato", "cita", "captura", "post"):
            self.fondo = mezcla(self.acento, self.fondo, 0.86)
            self.d.rectangle([0, 0, self.W, self.H], fill=self.fondo)
            self.suave = mezcla(self.tinta, self.fondo, 0.42)
        if vida and tipo not in ("foto", "cierre"):
            capa = Image.new("RGBA", (self.W, self.H), (0, 0, 0, 0))
            dc = ImageDraw.Draw(capa)
            r = int(self.W * 0.30)
            # solo en esquinas (nunca detrás del texto): arriba a la derecha o abajo a la derecha, alternando
            arriba = self.n % 2 == 1
            cx, cy = (self.W + r * 0.30, -r * 0.35) if arriba else (self.W + r * 0.35, self.H + r * 0.30)
            dc.ellipse([cx - r, cy - r, cx + r, cy + r], fill=self.acento[:3] + (45 if arriba else 60,))
            r2 = int(r * 0.17)
            rx, ry = (self.W - r * 0.95, r * 0.12) if arriba else (self.W - r * 1.05, self.H - r * 0.30)
            self.img.alpha_composite(capa)
        if invertido:
            self.d.rectangle([0, 0, self.W, self.H], fill=self.acento if nombre != "bloque" else self.acento)
        if nombre == "cuaderno":
            paso = 46
            punto = mezcla(self.tinta, self.fondo, 0.82)
            for y in range(paso, self.H, paso):
                for x in range(paso, self.W, paso):
                    self.d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=punto)
        elif nombre == "editorial":
            ruido = Image.effect_noise((self.W, self.H), 18).convert("L")
            capa = Image.new("RGBA", (self.W, self.H), self.tinta[:3] + (0,))
            capa.putalpha(ruido.point(lambda v: max(0, v - 118) // 6))
            self.img.alpha_composite(capa)
            self.d.line([self.x0, self.y0 - 30, self.x1, self.y0 - 30], fill=self.tinta, width=2)
        elif nombre == "pro" and not invertido:
            # sobria: un tinte apenas distinto en las láminas pares y una barra corta del acento arriba
            if self.n % 2 == 0 and tipo not in ("foto", "cierre", "portada") and luz(self.fondo) > 0.6:
                self.fondo = mezcla(self.acento, self.fondo, 0.93)
                self.d.rectangle([0, 0, self.W, self.H], fill=self.fondo)
                self.suave = mezcla(self.tinta, self.fondo, 0.38)
            self.d.rectangle([self.x0, self.y0 - 44, self.x0 + 72, self.y0 - 38], fill=self.acento)
        elif nombre == "bloque" and not invertido:
            self.d.rectangle([0, 0, 22, self.H], fill=self.acento)

    # ----- texto con énfasis -----
    def texto(self, texto, caja, nombre_fuente, tam, color=None, alinear="izq", interlineado=1.12,
              enfasis=None, vertical="arriba", minimo=28):
        x0, y0, x1, y1 = caja
        color = color or self.tinta
        enfasis = enfasis or self.p["enfasis"]
        f, ls, tam = ajusta(texto, nombre_fuente, tam, x1 - x0, y1 - y0, interlineado, minimo)
        f_it = fuente(self.p["titulo_it"], tam) if nombre_fuente == self.p["titulo"] else f
        alto = len(ls) * tam * interlineado
        y = y0 if vertical == "arriba" else (y0 + (y1 - y0 - alto) / 2 if vertical == "centro" else y1 - alto)
        esp = f.getlength(" ")
        for l in ls:
            anchos = [(f_it if (e and enfasis == "italica") else f).getlength(p) for p, e, _ in l]
            total = ancho_linea(l, f, f_it, enfasis)
            x = x0 if alinear == "izq" else (x0 + (x1 - x0 - total) / 2 if alinear == "centro" else x1 - total)
            pos, xx = [], x
            for j, ((p, e, peg), w) in enumerate(zip(l, anchos)):
                if j and not peg:
                    xx += esp
                pos.append(xx)
                xx += w
            # primero los fondos del énfasis (para que no tapen letras vecinas)
            for (p, e, peg), w, xx in zip(l, anchos, pos):
                if e and enfasis == "marcatextos":
                    capa = Image.new("RGBA", self.img.size, (0, 0, 0, 0))
                    ImageDraw.Draw(capa).rounded_rectangle(
                        [xx - 6, y + tam * 0.48, xx + w + 6, y + tam * 0.98], radius=8, fill=self.acento[:3] + (90,))
                    self.img.alpha_composite(capa)
                elif e and enfasis == "caja":
                    bx = self.d.textbbox((xx, y), "Hgy", font=f)
                    self.d.rectangle([xx - 10, bx[1] - 8, xx + w + 10, bx[3] + 8], fill=self.acento)
            for (p, e, peg), w, xx in zip(l, anchos, pos):
                ff = f_it if (e and enfasis == "italica") else f
                c = color
                if e and enfasis in ("color", "italica"):
                    c = self.acento_txt
                if e and enfasis == "caja":
                    c = self.fondo if self.g.get("plantilla") != "bloque" else (17, 17, 17, 255)
                if e and enfasis == "subrayado":
                    bx = self.d.textbbox((xx, y), p, font=ff)
                    self.d.line([xx, bx[3] + 10, xx + w, bx[3] + 10], fill=c, width=int(max(4, tam // 18)))
                self.d.text((xx, y), p, font=ff, fill=c)
            y += tam * interlineado
        return y  # dónde terminó el texto

    # ----- pie: @usuario, número de slide, "desliza" -----
    def pie(self, desliza=False, color=None):
        color = color or self.suave
        m = self.g.get("marca", {})
        f = fuente(self.p["fuerte"], 30)
        yb = self.y1 + 60 if self.formato == "instagram" else self.y1 + 20
        usuario = m.get("usuario", "")
        logo = m.get("logo")
        x = self.x0
        if logo and os.path.exists(logo):
            lg = Image.open(logo).convert("RGBA")
            lg.thumbnail((210, 72))
            px, py = int(x), int(yb - lg.height / 2 + 14)
            if color is not None:          # sobre el color de la marca o una foto: el logo va en una placa clara
                self.d.rounded_rectangle([px - 8, py - 8, px + lg.width + 8, py + lg.height + 8], radius=14,
                                         fill=self.fondo if self.g.get("plantilla") != "bloque" else (255, 255, 255, 255))
            self.img.alpha_composite(lg, (px, py))
            x += lg.width + 22
        if usuario:
            self.d.text((x, yb), usuario, font=f, fill=color)
        if desliza:
            t = {"en": "Swipe", "pt": "Deslize", "fr": "Faites défiler"}.get(idioma(self.g), "Desliza")
            ca = self.acento if color == self.suave else color
            xa = self.x1 - 44
            self.d.text((xa - 16 - f.getlength(t), yb), t, font=f, fill=ca)
            ym = yb + 20
            self.d.line([xa, ym, xa + 40, ym], fill=ca, width=4)
            self.d.line([xa + 26, ym - 12, xa + 40, ym, xa + 26, ym + 12], fill=ca, width=4, joint="curve")
        else:
            t = f"{self.n}/{self.total}"
            self.d.text((self.x1 - f.getlength(t), yb), t, font=f, fill=color)

    def foto(self, ruta, caja, radio=28):
        """Pone una imagen en la caja SIN cortar lo importante:
        · captura de pantalla o diseño con texto → completa (en MacBook si es horizontal y ancha, si no en tarjeta)
        · foto que perdería mucho al recortar → completa, con su propio fondo desenfocado a los lados
        · foto normal → recorte inteligente que nunca corta la cabeza (encuadre.py)"""
        if not ruta or not os.path.exists(ruta):
            return False
        x0, y0, x1, y1 = [int(v) for v in caja]
        w, h = x1 - x0, y1 - y0
        im = Image.open(ruta)
        try:
            from PIL import ImageOps
            im = ImageOps.exif_transpose(im)
        except Exception:
            pass
        im = im.convert("RGBA")
        captura = encuadre.es_captura(ruta)
        if captura and im.width / im.height > 1.25 and w / h > 1.1:
            lap = marcos.macbook(im, int(min(w * 0.94, (h - 30) * 1.6 / 1.09)))
            self.img.alpha_composite(lap, (x0 + (w - lap.width) // 2, y0 + max(0, (h - lap.height) // 2)))
            return True
        perdida = encuadre.aviso_proporcion(im, w, h)
        if captura or perdida > 0.38:
            # completa: la caja se ajusta a la imagen y se centra (sin franjas ni desenfoques a los lados)
            esc = min(w / im.width, h / im.height)
            cabe = im.resize((max(1, int(im.width * esc)), max(1, int(im.height * esc))), Image.LANCZOS)
            x0 += (w - cabe.width) // 2; y0 += (h - cabe.height) // 2
            w, h = cabe.width, cabe.height
            im = cabe
            if captura:
                radio = min(radio, 18)
        else:
            l, t, r_, b_ = encuadre.recorte(im, w, h)
            im = im.crop((l, t, r_, b_)).resize((w, h), Image.LANCZOS)
        x1, y1 = x0 + w, y0 + h
        mascara = Image.new("L", (w, h), 0)
        ImageDraw.Draw(mascara).rounded_rectangle([0, 0, w, h], radius=radio, fill=255)
        if self.g.get("vida", True):          # sombra suave: la foto «flota», no se ve pegada
            sombra = Image.new("RGBA", self.img.size, (0, 0, 0, 0))
            ImageDraw.Draw(sombra).rounded_rectangle([x0 + 6, y0 + 16, x1 + 6, y1 + 16], radius=radio, fill=(0, 0, 0, 60))
            self.img.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(16)))
        self.img.paste(im, (x0, y0), mascara)
        return True

    def fila_logos(self, y, alto=96, claro=None, x=None, derecha=False, medir=False):
        """Los logos de la marca y de lo que se menciona (marca.logos), en fila.
        Por defecto SIN placa (Derek, 26 nov: «no me gusta lo del fondo blanco»): el logo con una sombra suave.
        La placa blanca sale sola si el logo no se distinguiría del fondo, o siempre con marca.logos_placa = true
        (false = nunca). Con medir=True solo devuelve el ancho que ocuparía."""
        rutas = [r for r in self.g.get("marca", {}).get("logos", []) if r and os.path.exists(r)]
        pref = self.g.get("marca", {}).get("logos_placa", "auto") if claro is None else claro
        piezas = []
        for r in rutas[:5]:
            lg = Image.open(r).convert("RGBA")
            lg.thumbnail((int(alto * 2.6), alto - 22), Image.LANCZOS)
            piezas.append(lg)
        anchos = [max(alto, lg.width + 36) for lg in piezas]
        total = sum(anchos) + 18 * max(0, len(piezas) - 1)
        if medir or not piezas:
            return total if medir else y
        x = (self.x1 - total) if derecha else (self.x0 if x is None else x)
        for lg, pw in zip(piezas, anchos):
            caja = (int(x), int(y), int(x + pw), int(y + alto))
            placa = pref is True
            if pref == "auto":
                # ¿se distingue? compara la luz del logo con la del fondo que tiene detrás
                detras = self.img.crop(caja).convert("L").resize((16, 16))
                luz_f = sum(detras.getdata()) / 256 / 255
                a_ = lg.getchannel("A"); l_ = lg.convert("L")
                px = [l_.getpixel((i, j)) for i in range(0, lg.width, 3) for j in range(0, lg.height, 3) if a_.getpixel((i, j)) > 128]
                luz_l = (sum(px) / len(px) / 255) if px else 0.5
                placa = abs(luz_l - luz_f) < 0.28
            if placa:
                self.d.rounded_rectangle(caja, radius=alto // 2 if lg.width < alto * 1.3 else 16, fill=(255, 255, 255, 255))
            else:
                sm = Image.new("RGBA", self.img.size, (0, 0, 0, 0))
                sm.paste((0, 0, 0, 110), (int(x + (pw - lg.width) / 2) + 2, int(y + (alto - lg.height) / 2) + 4), lg.getchannel("A"))
                self.img.alpha_composite(sm.filter(ImageFilter.GaussianBlur(6)))
            self.img.alpha_composite(lg, (int(x + (pw - lg.width) / 2), int(y + (alto - lg.height) / 2)))
            x += pw + 18
        self.d = ImageDraw.Draw(self.img)
        return y + alto


# ---------- tipos de slide ----------
def _foto_fondo(c, ruta):
    """La foto a toda la lámina con recorte inteligente (no corta la cabeza) y sombra abajo para el texto."""
    from PIL import ImageOps
    im = ImageOps.exif_transpose(Image.open(ruta)).convert("RGB")
    l, t, r_, b_ = encuadre.recorte(im, c.W, c.H)
    esc = c.W / (r_ - l)
    c.caras = [((f[0] - l) * esc, (f[1] - t) * esc, (f[2] - l) * esc, (f[3] - t) * esc) for f in encuadre.caras(im)]
    c.img.paste(im.crop((l, t, r_, b_)).resize((c.W, c.H), Image.LANCZOS), (0, 0))
    sombra = Image.new("RGBA", c.img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(sombra)
    zona = int(c.H * 0.62)
    for i in range(zona):
        sd.line([0, c.H - i, c.W, c.H - i], fill=(0, 0, 0, int(230 * (1 - i / zona) ** 1.1)))
    for i in range(220):             # y un poco arriba, para que los logos y la etiqueta se lean
        sd.line([0, i, c.W, i], fill=(0, 0, 0, int(110 * (1 - i / 220))))
    c.img.alpha_composite(sombra)
    c.d = ImageDraw.Draw(c.img)


def s_portada_sangre(c, s):
    _foto_fondo(c, s["foto"])
    blanco = (255, 255, 255, 255)
    # los logos nunca encima de la cara (Derek, 26 nov: «tapaste mi cara con el logo de Claude»)
    alto_l, y_l = 96, c.y0 - 40
    ancho_l = c.fila_logos(y_l, alto_l, medir=True)
    def choca(x0, x1, y0, y1):
        return any(x0 < f[2] + 40 and x1 > f[0] - 40 and y0 < f[3] + 60 and y1 > f[1] - 80 for f in getattr(c, "caras", []))
    if ancho_l:
        if not choca(c.x0, c.x0 + ancho_l, y_l, y_l + alto_l):
            c.fila_logos(y_l, alto_l)
        elif not choca(c.x1 - ancho_l, c.x1, y_l, y_l + alto_l):
            c.fila_logos(y_l, alto_l, derecha=True)
        else:                       # arriba no hay lugar libre: van justo encima del título, abajo
            c.fila_logos(c.y1 - 760, 80)
    if s.get("etiqueta"):
        f = fuente(c.p["fuerte"], 30)
        t = s["etiqueta"].upper()
        c.d.rounded_rectangle([c.x0, c.y1 - 640, c.x0 + f.getlength(t) + 44, c.y1 - 584], radius=28, fill=c.acento)
        c.d.text((c.x0 + 22, c.y1 - 631), t, font=f, fill=blanco if contraste(blanco, c.acento) >= 2.4 else c.tinta)
    viejo = c.acento_txt
    c.acento_txt = c.acento if contraste(c.acento, (20, 20, 20)) >= 3 else blanco
    alto_sub = 150 if s.get("subtitulo") else 0
    fin = c.texto(s["titulo"], (c.x0, c.y1 - 560, c.x1, c.y1 - 40 - alto_sub), c.p["titulo"], 108 * c.p["escala_titulo"],
                  blanco, interlineado=1.04, vertical="abajo")
    if s.get("subtitulo"):
        c.texto(s["subtitulo"], (c.x0, fin + 26, c.x1, c.y1 - 20), c.p["texto"], 42, (232, 234, 238, 255),
                enfasis="color", interlineado=1.28, minimo=34)
    c.acento_txt = viejo
    c.pie(desliza=True, color=(232, 234, 238, 255))


def s_portada(c, s):
    plant = c.g.get("plantilla")
    if s.get("foto") and os.path.exists(s["foto"]) and (s.get("a_sangre", plant == "pro")) \
            and not encuadre.es_captura(s["foto"]):
        return s_portada_sangre(c, s)
    inv = plant == "bloque"
    c.decorar_fondo()
    tinta = c.tinta
    y = c.y0
    # con marca, su logo se ve en la portada (arriba a la derecha), no solo chiquito en el pie
    logo = c.g.get("marca", {}).get("logo")
    if logo and os.path.exists(logo):
        lg = Image.open(logo).convert("RGBA")
        lg.thumbnail((340, 120), Image.LANCZOS)
        c.img.alpha_composite(lg, (int(c.x1 - lg.width), int(y + 30 - lg.height / 2)))
        if not s.get("etiqueta"):
            y += 100
    if s.get("etiqueta"):
        f = fuente(c.p["fuerte"], 32)
        t = s["etiqueta"].upper()
        w = f.getlength(t)
        c.d.rounded_rectangle([c.x0, y, c.x0 + w + 44, y + 60], radius=30, outline=c.acento, width=3)
        c.d.text((c.x0 + 22, y + 10), t, font=f, fill=c.acento)
        y += 110
    if c.g.get("marca", {}).get("logos"):
        y = c.fila_logos(y) + 40
    tiene_foto = bool(s.get("foto")) and os.path.exists(s.get("foto", ""))
    tiene_dibujo = bool(s.get("dibujo")) and not tiene_foto
    alto_titulo = (c.y1 - y) * (0.40 if tiene_foto else (0.42 if tiene_dibujo else 0.78))
    fin = c.texto(s["titulo"], (c.x0, y, c.x1, y + alto_titulo), c.p["titulo"],
                  (112 if tiene_foto else 150) * c.p["escala_titulo"], tinta, interlineado=1.02,
                  vertical="arriba" if (tiene_foto or tiene_dibujo) else "centro")
    if s.get("subtitulo"):
        fin = c.texto(s["subtitulo"], (c.x0, fin + (36 if tiene_foto else 56), c.x1, fin + (160 if tiene_foto else 286)),
                      c.p["texto"], 42, c.suave, enfasis="color", interlineado=1.25, minimo=36)
    if tiene_foto:
        c.foto(s["foto"], (c.x0, fin + 40, c.x1, c.y1 - 10))
    elif tiene_dibujo:
        c.dibujo(s["dibujo"], (c.x0 - 40, fin + 20, c.x1 + 40, c.y1 - 10))
    c.pie(desliza=True)


def s_punto(c, s):
    c.decorar_fondo()
    y = c.y0
    if s.get("foto"):
        # con su foto: la foto arriba (40 % de la lámina) y la idea abajo; el número va sobre la foto
        try:
            iw, ih = Image.open(s["foto"]).size
        except Exception:
            iw, ih = 4, 3
        vertical = ih > iw * 1.05 and not encuadre.es_captura(s["foto"])
        alto_f = (c.y1 - c.y0) * (0.52 if vertical else 0.42)
        c.foto(s["foto"], (c.x0, y, c.x1, y + alto_f))
        if s.get("num") is not None and encuadre.es_captura(s["foto"]):
            s = dict(s, titulo=(f"{s['num']:02d} · " if isinstance(s["num"], int) else f"{s['num']} · ") + s["titulo"], num=None)
        if s.get("num") is not None:
            f = fuente(c.p["fuerte"], 54)
            t = f"{s['num']:02d}" if isinstance(s["num"], int) else str(s["num"])
            w = f.getlength(t)
            c.d.rounded_rectangle([c.x0 + 24, y + 24, c.x0 + 24 + w + 44, y + 24 + 84], radius=42, fill=c.acento)
            centrado(c.d, c.x0 + 24 + (w + 44) / 2, y + 24 + 42, t, f, c.fondo if contraste(c.fondo, c.acento) >= 2 else c.tinta)
        fin = c.texto(s["titulo"], (c.x0, y + alto_f + 50, c.x1, y + alto_f + 300), c.p["titulo"], 92 * c.p["escala_titulo"],
                      interlineado=1.05)
        if c.g.get("plantilla") != "pro":
            c.d.line([c.x0, fin + 28, c.x0 + 120, fin + 28], fill=c.acento, width=6)
        if s.get("texto"):
            c.texto(s["texto"], (c.x0, fin + 66, c.x1, c.y1 - 20), c.p["texto"], 50, c.suave, enfasis="color", interlineado=1.32)
        c.pie()
        return
    num = s.get("num")
    if num is not None:
        f = fuente(c.p["titulo_it"] if c.g.get("plantilla") == "editorial" else c.p["titulo"], 230)
        t = f"{num:02d}" if isinstance(num, int) else str(num)
        c.d.text((c.x0 - 6, y - 70), t, font=f, fill=c.acento)
        y += 200
    if s.get("dibujo"):
        lado = 300 if c.formato == "instagram" else 330
        c.dibujo(s["dibujo"], (c.x1 - lado, c.y0 - 20, c.x1, c.y0 - 20 + lado))
        y = max(y, c.y0 + lado + 10)
    if not s.get("dibujo"):
        # sin dibujo: se mide el bloque (título + texto) y se baja para que quede centrado en lo que sobra
        prueba = Lienzo(c.g, c.n, c.total)
        fin_p = prueba.texto(s["titulo"], (c.x0, y, c.x1, y + 330), c.p["titulo"], 118 * c.p["escala_titulo"], interlineado=1.05)
        if s.get("texto"):
            fin_p = prueba.texto(s["texto"], (c.x0, fin_p + 80, c.x1, c.y1 - 20), c.p["texto"], 60, enfasis="color", interlineado=1.38)
        y += max(0, (c.y1 - 40 - fin_p) * 0.45)
    fin = c.texto(s["titulo"], (c.x0, y, c.x1, y + 330), c.p["titulo"], (108 if s.get("dibujo") else 118) * c.p["escala_titulo"],
                  interlineado=1.05)
    if c.g.get("plantilla") != "pro":
        c.d.line([c.x0, fin + 34, c.x0 + 120, fin + 34], fill=c.acento, width=6)
    if s.get("texto"):
        c.texto(s["texto"], (c.x0, fin + 80, c.x1, c.y1 - 20), c.p["texto"], 56 if s.get("dibujo") else 60, c.suave,
                enfasis="color", interlineado=1.38)
    c.pie()


def s_lista(c, s):
    c.decorar_fondo()
    xt = c.x1
    if s.get("dibujo"):
        c.dibujo(s["dibujo"], (c.x1 - 240, c.y0 - 10, c.x1, c.y0 + 230))
        xt = c.x1 - 270
    fin = c.texto(s["titulo"], (c.x0, c.y0, xt, c.y0 + 300), c.p["titulo"], 90 * c.p["escala_titulo"],
                  interlineado=1.05)
    items = s.get("items", [])
    y = max(fin + 60, c.y0 + 270) if s.get("dibujo") else fin + 60
    alto = min((c.y1 - y) / max(1, len(items)), 210)
    for i, it in enumerate(items):
        r = 26
        cy = medio_x(c.p["texto"], 48, y + 8)
        if s.get("marca") == "check" or c.g.get("plantilla") == "cuaderno":
            c.d.line([c.x0, cy, c.x0 + 16, cy + 18, c.x0 + 44, cy - 20], fill=c.acento, width=8, joint="curve")
        else:
            c.d.ellipse([c.x0, cy - r, c.x0 + 2 * r, cy + r], fill=c.acento)
            f = fuente(c.p["fuerte"], 30)
            t = str(i + 1)
            centrado(c.d, c.x0 + r, cy, t, f, c.fondo)
        c.texto(it, (c.x0 + 80, y + 8, c.x1, y + alto - 16), c.p["texto"], 48, enfasis="color",
                interlineado=1.25, minimo=30)
        y += alto
    c.pie()


def s_dato(c, s):
    c.decorar_fondo()
    if s.get("dibujo"):
        c.dibujo(s["dibujo"], (c.x0, c.y0, c.x0 + 280, c.y0 + 280))
    zona = (c.y1 - c.y0)
    fin = c.texto(s["cifra"], (c.x0, c.y0 + zona * 0.12, c.x1, c.y0 + zona * 0.5), c.p["titulo"], 300,
                  c.acento, interlineado=1.0, enfasis="color", vertical="abajo")
    fin = c.texto(s["texto"], (c.x0, fin + 40, c.x1, fin + 420), c.p["fuerte"], 62, interlineado=1.18)
    if s.get("fuente"):
        c.texto("Fuente: " + s["fuente"], (c.x0, c.y1 - 70, c.x1, c.y1), c.p["texto"], 28, c.suave,
                vertical="abajo")
    c.pie()


def s_cita(c, s):
    c.decorar_fondo()
    f = fuente("InstrumentSerif-Regular.ttf", 340)
    c.d.text((c.x0 - 10, c.y0 - 90), "“", font=f, fill=c.acento)
    fin = c.texto(s["texto"], (c.x0, c.y0 + 200, c.x1, c.y1 - 160), c.p["titulo"],
                  86 * c.p["escala_titulo"], interlineado=1.12, vertical="centro")
    if s.get("autor"):
        c.texto("— " + s["autor"], (c.x0, fin + 30, c.x1, fin + 100), c.p["fuerte"], 36, c.suave)
    c.pie()


def s_antes_despues(c, s):
    c.decorar_fondo()
    fin = c.texto(s.get("titulo", ""), (c.x0, c.y0, c.x1, c.y0 + 240), c.p["titulo"],
                  84 * c.p["escala_titulo"], interlineado=1.05)
    y = fin + 50
    mitad = (c.y1 - y - 30) / 2
    for i, (eti, txt) in enumerate([(s.get("eti_antes", "Antes"), s["antes"]),
                                    (s.get("eti_despues", "Después"), s["despues"])]):
        caja = [c.x0, y, c.x1, y + mitad]
        relleno = mezcla(c.tinta, c.fondo, 0.93) if i == 0 else mezcla(c.acento, c.fondo, 0.86)
        c.d.rounded_rectangle(caja, radius=28, fill=relleno)
        f = fuente(c.p["fuerte"], 32)
        c.d.text((c.x0 + 36, y + 28), eti.upper(), font=f, fill=c.suave if i == 0 else c.acento)
        c.texto(txt, (c.x0 + 36, y + 90, c.x1 - 36, y + mitad - 28), c.p["texto"], 58, enfasis="color",
                interlineado=1.28)
        y += mitad + 30
    c.pie()


def s_cierre(c, s):
    plant = c.g.get("plantilla")
    c.img.paste(Image.new("RGBA", c.img.size, c.acento if plant != "bloque" else c.acento), (0, 0))
    c.d = ImageDraw.Draw(c.img)
    claro = c.fondo if plant != "bloque" else (17, 17, 17, 255)
    if c.g.get("vida", True) and plant != "pro":
        capa = Image.new("RGBA", c.img.size, (0, 0, 0, 0))
        dc = ImageDraw.Draw(capa)
        r = int(c.W * 0.42)
        dc.ellipse([c.W - r * 0.9, c.H - r * 0.85, c.W + r * 1.1, c.H + r * 1.15], fill=(255, 255, 255, 34))
        c.img.alpha_composite(capa)
        logo = c.g.get("marca", {}).get("logo")
        if logo and os.path.exists(logo):          # su logo grande y transparente, abajo a la derecha
            lg = Image.open(logo).convert("RGBA")
            lg.thumbnail((380, 380), Image.LANCZOS)
            # su silueta en blanco transparente (con sus colores se perdería sobre el color de su marca)
            sil = Image.new("RGBA", lg.size, (255, 255, 255, 0))
            sil.putalpha(lg.getchannel("A").point(lambda v: int(v * 0.20)))
            c.img.alpha_composite(sil, (int(c.x1 - lg.width + 20), int(c.y1 - lg.height - 40)))
        c.d = ImageDraw.Draw(c.img)
    if contraste(claro, c.acento) < 3 and contraste(c.tinta, c.acento) > contraste(claro, c.acento):
        claro = c.tinta                                         # acento claro (p. ej. verde lima): texto oscuro
    if c.g.get("marca", {}).get("logos") and not s.get("dibujo"):
        c.fila_logos(c.y0 - 20)
    if s.get("dibujo"):
        c.acento, c.fondo = claro, c.acento  # en el cierre el dibujo va en el color claro
        c.dibujo(s["dibujo"], (c.x0, c.y0, c.x0 + 300, c.y0 + 300))
        c.acento, c.fondo = c.fondo, claro
    fin = c.texto(s["titulo"], (c.x0, c.y0 + (320 if s.get("dibujo") else (140 if plant == "pro" else 0)), c.x1,
                                c.y0 + (c.y1 - c.y0) * (0.78 if plant == "pro" else 0.6)), c.p["titulo"],
                  120 * c.p["escala_titulo"], claro, interlineado=1.08, enfasis="subrayado", vertical="centro")
    if s.get("cta"):
        f = fuente(c.p["fuerte"], 40)
        t = s["cta"]
        w = f.getlength(t)
        y = fin + 70
        c.d.rounded_rectangle([c.x0, y, c.x0 + w + 80, y + 96], radius=48, fill=claro)
        c.d.text((c.x0 + 40, y + 22), t, font=f, fill=c.acento)
    c.pie(color=claro)


def _abre(ruta, que):
    if not ruta or not os.path.exists(ruta):
        raise SystemExit(f"FALTA_IMAGEN {que}: no existe «{ruta}». Revisa la ruta en el guion.")
    return Image.open(ruta).convert("RGBA")


def _titulo_arriba(c, s, alto=300, tam=96):
    fin = c.y0
    if s.get("titulo"):
        fin = c.texto(s["titulo"], (c.x0, c.y0, c.x1, c.y0 + alto), c.p["titulo"], tam * c.p["escala_titulo"],
                      interlineado=1.05)
    if s.get("texto"):
        fin = c.texto(s["texto"], (c.x0, fin + 24, c.x1, fin + 190), c.p["texto"], 44, c.suave,
                      enfasis="color", interlineado=1.3)
    return fin


def s_foto(c, s):
    """Su foto a toda la lámina, con el título encima (sobre una sombra para que se lea)."""
    _foto_fondo(c, s["foto"])
    # que el texto blanco SIEMPRE se lea: si donde va el texto la foto sigue clara (fondos blancos, cielos,
    # azulejos), se oscurece esa zona poco a poco hasta que los puntos más claros queden oscuros.
    y_tx = int(c.y1 - 560)
    for _ in range(8):
        zona_tx = c.img.crop((0, y_tx, c.W, int(c.y1))).convert("L").resize((108, 56))
        claros = sorted(zona_tx.getdata())[int(108 * 56 * 0.85)]
        if claros <= 105:
            break
        extra = Image.new("RGBA", c.img.size, (0, 0, 0, 0))
        de = ImageDraw.Draw(extra)
        for i in range(c.H - y_tx + 160):
            y = c.H - i
            a = 46 if y >= y_tx else int(46 * max(0, 1 - (y_tx - y) / 160))
            de.line([0, y, c.W, y], fill=(0, 0, 0, a))
        c.img.alpha_composite(extra)
    c.d = ImageDraw.Draw(c.img)
    blanco = (255, 255, 255, 255)
    acento_viejo = c.acento_txt
    if contraste(c.acento, (20, 20, 20)) >= 3:
        c.acento_txt = c.acento
    else:
        c.acento_txt = blanco
    alto_tx = 150 if s.get("texto") else 0
    fin = c.texto(s.get("titulo", ""), (c.x0, c.y1 - 330 - alto_tx, c.x1, c.y1 - 30 - alto_tx), c.p["titulo"],
                  100 * c.p["escala_titulo"], blanco, interlineado=1.08, vertical="abajo",
                  enfasis="subrayado")                 # sobre una foto, lo resaltado va subrayado en blanco: siempre se lee
    if s.get("texto"):
        c.texto(s["texto"], (c.x0, fin + 24, c.x1, c.y1 - 30), c.p["texto"], 48, (235, 235, 235, 255), enfasis="color",
                interlineado=1.3)
    c.acento_txt = acento_viejo
    c.pie(color=(235, 235, 235, 255))


def s_captura(c, s):
    """Una captura real (de una app, una web, un chat) dentro de un iPhone. Lo que más credibilidad da."""
    c.decorar_fondo()
    fin = _titulo_arriba(c, s, 260, 88)
    pant = _abre(s.get("captura"), "captura")
    if pant.width / pant.height > 1.2:
        lap = marcos.macbook(pant, int(c.x1 - c.x0))
        c.img.alpha_composite(lap, (int((c.W - lap.width) / 2), int(fin + max(40, (c.y1 - fin - lap.height) / 2))))
        c.pie()
        return
    alto = int(min(c.y1 - fin - 50, (c.x1 - c.x0) / 0.4925 * 0.98))
    tel = marcos.iphone(pant, alto)
    x = int((c.W - tel.width) / 2)
    c.img.alpha_composite(tel, (x, int(fin + 30)))
    c.pie()


def s_post(c, s):
    """Una publicación tipo X/Threads (tuya o una cita con fuente), en tarjeta blanca realista."""
    c.decorar_fondo()
    fin = _titulo_arriba(c, s, 220, 84) if s.get("titulo") else c.y0 + 40
    x0, x1 = c.x0, c.x1
    f_nom = fuente("InstrumentSans-Bold.ttf", 40)
    f_usr = fuente("InstrumentSans-Regular.ttf", 34)
    f_txt, ls, tam = ajusta(s["post"], "InstrumentSans-Regular.ttf", 62, x1 - x0 - 96, 640, 1.32, 34)
    alto = 96 + 110 + len(ls) * tam * 1.32 + 70
    y0 = fin + max(40, (c.y1 - fin - alto) / 2.4) if s.get("titulo") else c.y0 + (c.y1 - c.y0 - alto) / 2
    sombra = Image.new("RGBA", c.img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sombra).rounded_rectangle([x0 + 6, y0 + 14, x1 + 6, y0 + alto + 14], radius=40, fill=(0, 0, 0, 55))
    c.img.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(18)))
    c.d.rounded_rectangle([x0, y0, x1, y0 + alto], radius=40, fill=(255, 255, 255), outline=(225, 228, 232), width=2)
    ax, ay, r = x0 + 48, y0 + 48, 50
    if s.get("avatar") and os.path.exists(s["avatar"]):
        av = Image.open(s["avatar"]).convert("RGBA")
        lado = min(av.size); av = av.crop(((av.width - lado) // 2, (av.height - lado) // 2,
                                          (av.width + lado) // 2, (av.height + lado) // 2)).resize((2 * r, 2 * r))
        m = Image.new("L", av.size, 0); ImageDraw.Draw(m).ellipse([0, 0, 2 * r, 2 * r], fill=255)
        c.img.paste(av, (int(ax), int(ay)), m)
    else:
        c.d.ellipse([ax, ay, ax + 2 * r, ay + 2 * r], fill=c.acento)
        ini = (s.get("nombre") or "?")[:1].upper()
        fi = fuente("InstrumentSans-Bold.ttf", 46)
        centrado(c.d, ax + r, ay + r, ini, fi, (255, 255, 255))
    c.d.text((ax + 2 * r + 24, ay + 6), s.get("nombre", ""), font=f_nom, fill=(15, 20, 25))
    c.d.text((ax + 2 * r + 24, ay + 54), s.get("usuario", ""), font=f_usr, fill=(83, 100, 113))
    y = ay + 2 * r + 40
    for l in ls:
        c.d.text((x0 + 48, y), " ".join(p for p, _, _ in l), font=f_txt, fill=(15, 20, 25))
        y += tam * 1.32
    c.pie()


def s_pasos(c, s):
    """Paso a paso con números unidos por una línea."""
    c.decorar_fondo()
    fin = _titulo_arriba(c, {"titulo": s.get("titulo")}, 280, 92)
    items = s.get("items", [])
    zona = c.y1 - fin - 70
    alto = min(zona / max(1, len(items)), 300)
    y = fin + 60 + (zona - alto * len(items)) / 3
    r = 40
    cx = c.x0 + r
    if len(items) > 1:
        c.d.line([cx, y + r, cx, y + alto * (len(items) - 1) + r], fill=mezcla(c.acento, c.fondo, 0.55), width=6)
    fn = fuente(c.p["fuerte"], 42)
    for i, it in enumerate(items):
        c.d.ellipse([cx - r, y, cx + r, y + 2 * r], fill=c.acento)
        t = str(i + 1)
        centrado(c.d, cx, y + r, t, fn, c.fondo if contraste(c.fondo, c.acento) >= 2 else c.tinta)
        cab, _, det = it.partition(":")
        fin_i = c.texto(cab.strip() if det else it, (c.x0 + 2 * r + 34, y + 2, c.x1, y + (alto * 0.5 if det else alto - 10)),
                        c.p["fuerte"], 62, interlineado=1.12, minimo=34)
        if det:
            c.texto(det.strip(), (c.x0 + 2 * r + 34, fin_i + 8, c.x1, y + alto - 18), c.p["texto"], 48, c.suave,
                    enfasis="color", interlineado=1.25, minimo=26)
        y += alto
    c.pie()


def s_comparacion(c, s):
    """Dos columnas (p. ej. «Sin IA» / «Con IA»): filas con ✗ y ✓."""
    c.decorar_fondo()
    fin = _titulo_arriba(c, {"titulo": s.get("titulo")}, 260, 88)
    filas = s.get("filas", [])
    y = fin + 50
    mid = (c.x0 + c.x1) / 2
    fh = fuente(c.p["fuerte"], 40)
    alto = min((c.y1 - y - 130) / max(1, len(filas)), 250)
    c.d.rounded_rectangle([mid + 8, y - 10, c.x1, y + 100 + alto * len(filas)], radius=30, fill=mezcla(c.acento, c.fondo, 0.86))
    for x, t, col in ((c.x0 + 10, s.get("col_a", "Antes"), c.suave), (mid + 36, s.get("col_b", "Ahora"), c.acento_txt)):
        c.d.text((x, y + 10), t.upper(), font=fh, fill=col)
    y += 100
    negativa = s.get("marcas") == "si_no" or bool(re.search(r"\b(sin|antes|no|nunca|without|before|old|never|mal)\b",
                                                                   str(s.get("col_a", "Antes")).lower()))
    for a, b in filas:
        for x, txt, ok in ((c.x0 + 10, a, False), (mid + 36, b, True)):
            col = c.acento_txt if ok else mezcla(c.tinta, c.fondo, 0.35)
            m = medio_x(c.p["fuerte"] if ok else c.p["texto"], 52, y)
            if ok:
                c.d.line([x, m + 1, x + 12, m + 14, x + 34, m - 15], fill=col, width=7, joint="curve")
            elif not negativa:
                c.d.ellipse([x + 8, m - 8, x + 24, m + 8], fill=col)
            else:
                c.d.line([x + 4, m - 12, x + 28, m + 12], fill=col, width=6)
                c.d.line([x + 28, m - 12, x + 4, m + 12], fill=col, width=6)
            c.texto(txt, (x + 56, y, (mid - 24) if not ok else c.x1 - 24, y + alto - 24),
                    c.p["fuerte"] if ok else c.p["texto"], 52, c.tinta if ok else mezcla(c.tinta, c.fondo, 0.3), interlineado=1.2, minimo=28)
        y += alto
    c.pie()


def s_logos(c, s):
    """Las herramientas o apps que se mencionan, con su logo real (ver imagenes.py logo)."""
    c.decorar_fondo()
    fin = _titulo_arriba(c, s, 300, 92)
    items = s.get("logos", [])[:6]
    cols = 3 if len(items) > 4 else 2 if len(items) > 1 else 1
    filas = math.ceil(len(items) / cols)
    gap = 36
    lado = min((c.x1 - c.x0 - gap * (cols - 1)) / cols, (c.y1 - fin - 80 - gap * (filas - 1)) / filas - 70)
    ancho_tot = cols * lado + (cols - 1) * gap
    fn = fuente(c.p["fuerte"], 36)
    y = fin + 60
    for i, it in enumerate(items):
        col, fil = i % cols, i // cols
        en_fila = min(cols, len(items) - fil * cols)
        x0 = (c.W - (en_fila * lado + (en_fila - 1) * gap)) / 2 + col * (lado + gap)
        y0 = y + fil * (lado + 70 + gap)
        c.d.rounded_rectangle([x0, y0, x0 + lado, y0 + lado], radius=int(lado * 0.2), fill=(255, 255, 255),
                              outline=mezcla(c.tinta, c.fondo, 0.85), width=2)
        lg = _abre(it.get("img"), "logo " + it.get("nombre", ""))
        lg.thumbnail((int(lado * 0.62), int(lado * 0.62)), Image.LANCZOS)
        c.img.alpha_composite(lg, (int(x0 + (lado - lg.width) / 2), int(y0 + (lado - lg.height) / 2)))
        n = it.get("nombre", "")
        c.d.text((x0 + lado / 2 - fn.getlength(n) / 2, y0 + lado + 16), n, font=fn, fill=c.tinta)
    c.pie()


TIPOS = dict(portada=s_portada, punto=s_punto, lista=s_lista, dato=s_dato, cita=s_cita,
             antes_despues=s_antes_despues, cierre=s_cierre, captura=s_captura, post=s_post, pasos=s_pasos,
             comparacion=s_comparacion, logos=s_logos, foto=s_foto)


def _sin_acento(t):
    import unicodedata
    return "".join(ch for ch in unicodedata.normalize("NFD", str(t).lower()) if unicodedata.category(ch) != "Mn").replace("-", "_").replace(" ", "_")


def revisar(guion):
    """Antes de dibujar: tipos válidos e imágenes que existen. Así nunca quedan láminas a medias."""
    problemas, avisos = [], []
    for i, s in enumerate(guion.get("slides", []), 1):
        t = _sin_acento(s.get("tipo", "punto"))
        t = {"antesdespues": "antes_despues", "comparar": "comparacion", "paso": "pasos", "logo": "logos"}.get(t, t)
        if t not in TIPOS:
            problemas.append(("ERROR", f"lámina {i}: el tipo «{s.get('tipo')}» no existe. Usa uno de: {', '.join(TIPOS)}"))
        else:
            s["tipo"] = t
        for k in ("foto", "captura", "avatar"):
            if s.get(k) and not os.path.exists(s[k]):
                problemas.append(("FALTA_IMAGEN", f"lámina {i}: no existe la imagen «{s[k]}» ({k})"))
        if s.get("foto") and os.path.exists(s["foto"]):
            try:
                ok, notas = encuadre.puntaje(s["foto"])
                if "chica (se verá borrosa)" in notas or "algo borrosa" in notas:
                    avisos.append(f"FOTO lámina {i}: «{os.path.basename(s['foto'])}» se verá {', '.join(notas)}; busca una mejor")
            except Exception:
                pass
        for it in s.get("logos", []):
            if not it.get("img") or not os.path.exists(it["img"]):
                problemas.append(("FALTA_IMAGEN", f"lámina {i}: no existe el logo de «{it.get('nombre', '?')}» («{it.get('img')}»)"))
        if t == "foto" and not s.get("foto"):
            problemas.append(("FALTA_IMAGEN", f"lámina {i}: la lámina foto necesita \"foto\": <imagen>"))
        if t == "captura" and not s.get("captura"):
            problemas.append(("FALTA_IMAGEN", f"lámina {i}: la lámina captura necesita \"captura\": <imagen>"))
    m = guion.get("marca", {})
    # ¿menciona apps o marcas conocidas y no trae su logo? (Derek, 24 nov: «no pusiste logos de nada»)
    claves_texto = ("titulo", "subtitulo", "texto", "etiqueta", "cta", "autor", "post", "col_a", "col_b")
    todo = " ".join(str(sl.get(k, "")) for sl in guion.get("slides", []) for k in claves_texto).lower()
    todo += " " + " ".join(str(x) for sl in guion.get("slides", []) for k in ("filas", "items", "pasos")
                           for x in (sl.get(k) or []) if not isinstance(x, dict)).lower()
    con_logo = " ".join(os.path.basename(r).lower() for r in m.get("logos", []))
    con_logo += " " + " ".join(os.path.basename(it.get("img", "")).lower() for sl in guion.get("slides", []) for it in sl.get("logos", []))
    conocidas = ["claude", "chatgpt", "gemini", "canva", "instagram", "tiktok", "linkedin", "whatsapp", "youtube",
                 "spotify", "netflix", "notion", "shopify", "excel", "google drive", "gmail"]
    for marca_ in conocidas:
        if re.search(r"\b" + marca_ + r"\b", todo) and marca_.split()[0] not in con_logo:
            avisos.append(f"LOGO mencionas «{marca_}» pero no va su logo: imagenes.py logo \"{marca_}\" <carpeta> "
                          f"y agrégalo a marca.logos (o a una lámina logos)")
    col = m.get("colores", {})
    if col.get("fondo") and col.get("tinta") and contraste(hexrgb(col["fondo"]), hexrgb(col["tinta"])) < 4.5:
        avisos.append("COLOR el texto casi no se distingue del fondo (contraste < 4.5): oscurece o aclara uno")
    if m.get("logo") and not os.path.exists(m["logo"]):
        avisos.append(f"no existe el logo de la marca «{m['logo']}»: sale sin logo")
    for k, v in (m.get("fuentes") or {}).items():
        if v and not os.path.exists(v):
            problemas.append(("FALTA_IMAGEN", f"no existe la letra «{v}» ({k})"))
    return problemas, avisos


def render(guion, salida):
    problemas, avisos = revisar(guion)
    for a in avisos:
        print("AVISO " + a)
    if problemas:
        for etiqueta, texto in problemas:
            print(f"{etiqueta} {texto}")
        raise SystemExit(2)
    os.makedirs(salida, exist_ok=True)
    formatos = guion.get("formato", "instagram")
    formatos = ["instagram", "tiktok"] if formatos == "ambos" else (
        ["instagram", "tiktok", "linkedin"] if formatos == "todos" else [formatos])
    rutas = []
    for fmt in formatos:
        g = dict(guion, _formato=fmt)
        slides = guion["slides"]
        carpeta = os.path.join(salida, fmt) if len(formatos) > 1 else salida
        os.makedirs(carpeta, exist_ok=True)
        for viejo in os.listdir(carpeta):
            if re.match(r"\d\d\.png$", viejo):
                os.remove(os.path.join(carpeta, viejo))
        for i, s in enumerate(slides, 1):
            c = Lienzo(g, i, len(slides)); c.tipo = s.get("tipo", "punto")
            TIPOS[s.get("tipo", "punto")](c, s)
            if fmt == "tiktok":
                # TikTok es más alto: si la lámina deja mucho vacío abajo, se baja todo para que quede
                # centrado en la pantalla (sin tocar la zona de los botones ni la de la descripción)
                base = Lienzo(g, i, len(slides)); base.tipo = c.tipo; base.decorar_fondo()
                caja = ImageChops.difference(c.img.convert("RGB"), base.img.convert("RGB")).crop(
                    (0, 0, c.W, int(c.y1) - 4)).getbbox()
                if caja:
                    libre = c.y1 - 30 - caja[3]
                    if libre > 120:
                        c = Lienzo(g, i, len(slides)); c.tipo = s.get("tipo", "punto")
                        c.y0 += libre * 0.5
                        TIPOS[s.get("tipo", "punto")](c, s)
            ruta = os.path.join(carpeta, f"{i:02d}.png")
            c.img.convert("RGB").save(ruta, optimize=True)
            rutas.append(ruta)
        # hoja de contacto para revisar todo de un vistazo
        ims = [Image.open(r) for r in rutas[-len(slides):]]
        tw = 360
        th = int(tw * ims[0].height / ims[0].width)
        cols = min(4, len(ims))
        filas = math.ceil(len(ims) / cols)
        hoja = Image.new("RGB", (cols * tw + (cols + 1) * 20, filas * th + (filas + 1) * 20), (230, 230, 230))
        for k, im in enumerate(ims):
            hoja.paste(im.resize((tw, th), Image.LANCZOS), (20 + (k % cols) * (tw + 20), 20 + (k // cols) * (th + 20)))
        hoja.save(os.path.join(carpeta, "_revision.jpg"), quality=85)
        if fmt == "linkedin" or guion.get("pdf"):
            ims[0].convert("RGB").save(os.path.join(carpeta, "carrusel.pdf"), save_all=True,
                                       append_images=[i.convert("RGB") for i in ims[1:]], resolution=150)
    return rutas


def opciones(args):
    """Atajos para no tener que copiar ni editar el guion:
    --formato instagram|tiktok|linkedin|ambos|todos · --cta "texto del cierre" · --sin-marca (para el «antes»)
    · --solo-portada (para comparar marcas) · --marca marca.json (usa una marca de marca.py) · --plantilla X"""
    o, resto, i = {}, [], 0
    while i < len(args):
        a = args[i]
        if a in ("--formato", "--cta", "--marca", "--plantilla"):
            o[a[2:]] = args[i + 1]; i += 2
        elif a in ("--sin-marca", "--solo-portada"):
            o[a[2:]] = True; i += 1
        else:
            resto.append(a); i += 1
    return o, resto


if __name__ == "__main__":
    op, argv = opciones(sys.argv[1:])
    sys.argv = [sys.argv[0]] + argv
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__ + "\n" + opciones.__doc__)
        sys.exit(1)
    try:
        with open(sys.argv[1], encoding="utf-8") as fh:
            guion = json.load(fh)
    except json.JSONDecodeError as e:
        print(f"ERROR el guion tiene un error de escritura en la línea {e.lineno}, columna {e.colno} ({e.msg}). Corrígelo y repite.")
        sys.exit(2)
    except OSError:
        print(f"ERROR no existe el guion «{sys.argv[1]}»."); sys.exit(2)
    salida = sys.argv[2] if len(sys.argv) > 2 else guion.get("salida", "carrusel")
    if op.get("formato"):
        guion["formato"] = op["formato"]
    if op.get("plantilla"):
        guion["plantilla"] = op["plantilla"]
    if op.get("marca"):
        mj = json.load(open(op["marca"], encoding="utf-8"))
        usuario_antes = guion.get("marca", {}).get("usuario")
        guion["marca"] = {k: mj[k] for k in ("nombre", "usuario", "colores", "logo", "fuentes") if mj.get(k)}
        guion["marca"].setdefault("usuario", usuario_antes or "@" + re.sub(r"\W", "", (mj.get("nombre") or "tu_marca").lower()))
        bm = os.path.dirname(os.path.abspath(op["marca"]))           # rutas de la marca: junto a su marca.json
        def en_bm(r):
            for cand in (r, os.path.join(bm, r), os.path.join(os.path.dirname(bm), r)):
                if os.path.isabs(cand) and os.path.exists(cand):
                    return cand
            return os.path.join(bm, r) if not os.path.isabs(r) else r
        if guion["marca"].get("logo"):
            guion["marca"]["logo"] = en_bm(guion["marca"]["logo"])
        guion["marca"]["fuentes"] = {k: en_bm(v) for k, v in (guion["marca"].get("fuentes") or {}).items()
                                     if isinstance(v, str)}
        if mj.get("estilo_sugerido") and not op.get("plantilla"):
            guion["plantilla"] = mj["estilo_sugerido"]
    if op.get("sin-marca"):
        guion["marca"] = {"usuario": "@tu_cuenta"}
        guion["plantilla"] = op.get("plantilla", "minimal")
    if op.get("cta"):
        for sl in guion["slides"]:
            if sl.get("tipo") == "cierre":
                sl["cta"] = op["cta"]
    if op.get("solo-portada"):
        guion["slides"] = guion["slides"][:1]
    base = os.path.dirname(os.path.abspath(sys.argv[1]))
    # rutas relativas (logo, fotos) se buscan junto al guion
    m = guion.get("marca", {})
    if m.get("logo") and not os.path.isabs(m["logo"]):
        m["logo"] = os.path.join(base, m["logo"])
    m["fuentes"] = {k: v for k, v in m.get("fuentes", {}).items() if not k.startswith("_")}
    for k, v in m["fuentes"].items():
        if v and not os.path.isabs(v):
            m["fuentes"][k] = os.path.join(base, v)
    for s in guion["slides"]:
        for k in ("foto", "captura", "avatar"):
            if s.get(k) and not os.path.isabs(os.path.expanduser(s[k])):
                s[k] = os.path.join(base, s[k])
            elif s.get(k):
                s[k] = os.path.expanduser(s[k])
        for it in s.get("logos", []):
            if it.get("img") and not os.path.isabs(os.path.expanduser(it["img"])):
                it["img"] = os.path.join(base, it["img"])
    for r in render(guion, salida):
        print(r)
    try:
        import version; version.avisar()
    except Exception:
        pass
