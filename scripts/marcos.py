"""carrusel-pro · marcos realistas (iPhone) y vistas de cómo se ve el carrusel publicado.
Lo usan carrusel.py (lámina `captura`) y vista.py. Solo Pillow."""
from PIL import Image, ImageDraw, ImageFilter


def redondear(im, radio):
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=radio, fill=255)
    out = im.convert("RGBA")
    out.putalpha(m)
    return out


def iphone(pantalla, alto, sombra=True):
    """Pone `pantalla` (cualquier imagen) dentro de un iPhone de frente: marco negro, isla y botones.
    Devuelve una imagen RGBA de `alto` px de alto (proporción de iPhone 15: 19.5:9)."""
    ancho = int(alto * 0.4925)
    borde = max(8, int(ancho * 0.035))
    radio = int(ancho * 0.16)
    lienzo = Image.new("RGBA", (ancho + 40, alto + 40), (0, 0, 0, 0))
    if sombra:
        s = Image.new("RGBA", lienzo.size, (0, 0, 0, 0))
        ImageDraw.Draw(s).rounded_rectangle([24, 30, ancho + 24, alto + 30], radius=radio, fill=(0, 0, 0, 90))
        lienzo.alpha_composite(s.filter(ImageFilter.GaussianBlur(14)))
    d = ImageDraw.Draw(lienzo)
    x, y = 20, 14
    # botones laterales
    d.rounded_rectangle([x - 5, y + alto * 0.20, x + 2, y + alto * 0.26], radius=3, fill=(40, 40, 44))
    d.rounded_rectangle([x - 5, y + alto * 0.29, x + 2, y + alto * 0.37], radius=3, fill=(40, 40, 44))
    d.rounded_rectangle([x + ancho - 2, y + alto * 0.27, x + ancho + 5, y + alto * 0.38], radius=3, fill=(40, 40, 44))
    # cuerpo
    d.rounded_rectangle([x, y, x + ancho, y + alto], radius=radio, fill=(22, 22, 24))
    d.rounded_rectangle([x + 2, y + 2, x + ancho - 2, y + alto - 2], radius=radio - 2, outline=(70, 70, 76), width=2)
    # pantalla
    pw, ph = ancho - 2 * borde, alto - 2 * borde
    p = pantalla.convert("RGB")
    esc = max(pw / p.width, ph / p.height)
    p = p.resize((int(p.width * esc + 0.5), int(p.height * esc + 0.5)), Image.LANCZOS)
    l = (p.width - pw) // 2
    p = p.crop((l, 0, l + pw, ph))                       # se corta abajo si sobra (las capturas empiezan arriba)
    lienzo.alpha_composite(redondear(p, radio - borde), (x + borde, y + borde))
    # isla dinámica
    iw, ih = int(ancho * 0.30), int(ancho * 0.085)
    ix, iy = x + (ancho - iw) // 2, y + borde + int(ancho * 0.03)
    d.rounded_rectangle([ix, iy, ix + iw, iy + ih], radius=ih // 2, fill=(0, 0, 0))
    return lienzo


def _fuente(nombre, tam):
    import os
    from PIL import ImageFont
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fuentes", nombre)
    try:
        return ImageFont.truetype(ruta, int(tam))
    except Exception:
        return ImageFont.load_default()


def barra_estado(ancho, color=(255, 255, 255), tinta=(0, 0, 0)):
    """La barra de arriba de un iPhone (hora, señal, batería), a escala 3x."""
    alto = int(ancho * 0.135)
    b = Image.new("RGB", (ancho, alto), color)
    d = ImageDraw.Draw(b)
    f = _fuente("InstrumentSans-Bold.ttf", alto * 0.34)
    d.text((ancho * 0.11, alto * 0.38), "9:41", font=f, fill=tinta)
    x = ancho * 0.80
    y = alto * 0.47
    for i in range(4):                                    # señal
        h = alto * (0.08 + 0.05 * i)
        d.rounded_rectangle([x + i * ancho * 0.012, y + alto * 0.24 - h, x + i * ancho * 0.012 + ancho * 0.008, y + alto * 0.24],
                            radius=2, fill=tinta)
    bx = ancho * 0.87                                     # batería
    d.rounded_rectangle([bx, y - alto * 0.02, bx + ancho * 0.065, y + alto * 0.24], radius=int(alto * 0.07),
                        outline=tinta, width=max(2, int(alto * 0.025)))
    d.rounded_rectangle([bx + alto * 0.04, y + alto * 0.02, bx + ancho * 0.065 - alto * 0.04, y + alto * 0.20],
                        radius=int(alto * 0.04), fill=tinta)
    return b


def con_barra(im):
    """Agrega la barra del iPhone arriba de una captura de página (que no la trae)."""
    im = im.convert("RGB")
    color = im.getpixel((im.width // 2, 2))
    tinta = (0, 0, 0) if sum(color) > 380 else (255, 255, 255)
    b = barra_estado(im.width, color, tinta)
    out = Image.new("RGB", (im.width, im.height + b.height), color)
    out.paste(b, (0, 0))
    out.paste(im, (0, b.height))
    return out
