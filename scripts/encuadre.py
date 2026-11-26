#!/usr/bin/env python3
"""carrusel-pro · encuadre inteligente: recorta una foto a una caja SIN cortar caras ni lo importante.

  from encuadre import recorte, es_captura, puntaje
  recorte(im, ancho, alto)   → la mejor ventana (x0, y0, x1, y1) de la foto para esa proporción
  es_captura(ruta_o_imagen)  → True si parece una captura de pantalla (esas nunca se recortan)
  puntaje(ruta)              → calidad para elegir fotos: (puntos, notas)

Cómo decide:
1. Busca a la persona por el tono de piel (sin instalar nada). Si hay, la ventana deja aire
   sobre la cabeza (nunca se corta) y, si cabe, el cuerpo hacia abajo.
2. Sin persona: mide dónde está «lo importante» (bordes, detalle y color) y centra ahí,
   con un poco de preferencia por el tercio de arriba (donde suelen estar las caras y los objetos).
3. Si la foto y la caja son muy distintas (foto vertical en caja ancha o al revés), lo avisa con
   `aviso_proporcion` para que la lámina cambie de diseño en vez de recortar de más.
"""
import os
from PIL import Image, ImageFilter, ImageOps, ImageStat

def _piel(im):
    """Zonas con tono de piel (caras y manos), sin instalar nada: máscara YCbCr sobre una miniatura."""
    p = im.convert("YCbCr"); p.thumbnail((220, 220))
    w, h = p.size; px = p.load()
    filas = [0] * h; puntos = []
    for y in range(h):
        for x in range(w):
            Y, cb, cr = px[x, y]
            if Y > 50 and 133 <= cr <= 178 and 80 <= cb <= 130 and cr - cb > 12:
                filas[y] += 1; puntos.append((x, y))
    return puntos, w, h


def caras(im):
    """La «cabeza» de la persona: el grupo de piel más alto de la foto, como (x0, y0, x1, y1) en píxeles.
    No es reconocimiento facial: solo dice dónde está la parte de arriba de la persona para no cortarla."""
    puntos, w, h = _piel(im)
    if len(puntos) < w * h * 0.004:        # casi sin piel: no hay persona clara
        return []
    # celdas de 10x10 con piel suficiente
    cel = {}
    for x, y in puntos:
        cel[(x // 10, y // 10)] = cel.get((x // 10, y // 10), 0) + 1
    buenas = [k for k, v in cel.items() if v >= 18]
    if not buenas:
        return []
    top = min(k[1] for k in buenas)
    # la cabeza: celdas buenas en la franja más alta (2 filas de celdas) agrupadas por columna
    franja = [k for k in buenas if k[1] <= top + 2]
    xs = sorted(k[0] for k in franja)
    # quédate con el grupo de columnas contiguas más grande
    grupos, g = [], [xs[0]]
    for x in xs[1:]:
        if x - g[-1] <= 2: g.append(x)
        else: grupos.append(g); g = [x]
    grupos.append(g)
    cab = max(grupos, key=len)
    W, H = im.size; sx, sy = W / w, H / h
    x0, x1 = min(cab) * 10 * sx, (max(cab) + 1) * 10 * sx
    y0 = top * 10 * sy; y1 = (top + 3) * 10 * sy
    return [(x0, y0, x1, y1)]


def _importante(im):
    """Centro de lo importante (bordes + detalle), con algo de preferencia por arriba."""
    p = im.convert("L"); p.thumbnail((160, 160))
    e = p.filter(ImageFilter.FIND_EDGES)
    w, h = e.size; px = e.load()
    sx = sy = tot = 0.0
    for y in range(1, h - 1):
        peso_y = 1.25 - 0.5 * (y / h)          # el tercio de arriba pesa un poco más
        for x in range(1, w - 1):
            v = px[x, y] * peso_y
            sx += v * x; sy += v * y; tot += v
    if not tot:
        return 0.5, 0.42
    return sx / tot / w, sy / tot / h


def recorte(im, ancho, alto):
    W, H = im.size
    r = ancho / alto
    if W / H > r:          # la foto es más ancha: se recorta a los lados
        cw, ch = H * r, H
    else:                  # la foto es más alta: se recorta arriba/abajo
        cw, ch = W, W / r
    fs = caras(im)
    if fs:
        x0 = min(f[0] for f in fs); x1 = max(f[2] for f in fs)
        y0 = min(f[1] for f in fs); y1 = max(f[3] for f in fs)
        alto_cara = max(f[3] - f[1] for f in fs)
        cx = (x0 + x1) / 2
        # la parte de arriba de la ventana deja aire sobre la cabeza (60 % de una cara);
        # si la ventana es más alta que eso, el resto va hacia abajo (cuerpo), no hacia el cielo
        top = y0 - alto_cara * 0.9
        if ch < (y1 - y0) + alto_cara * 1.6:     # no caben con aire: centra en las caras
            top = (y0 + y1) / 2 - ch / 2
        left = cx - cw / 2
    else:
        fx, fy = _importante(im)
        left = fx * W - cw / 2
        top = fy * H - ch * 0.42
    left = max(0, min(W - cw, left)); top = max(0, min(H - ch, top))
    return int(left), int(top), int(left + cw), int(top + ch)


def aviso_proporcion(im, ancho, alto):
    """Cuánto de la foto se pierde (0 a 1). Más de 0.45 = mejor cambiar de diseño (foto completa al lado o a sangre)."""
    W, H = im.size
    r, rf = ancho / alto, W / H
    return 1 - (min(r, rf) / max(r, rf))


def es_captura(x):
    """Captura de pantalla: PNG/sin cámara, con muchos planos de un solo color y bordes rectos."""
    im = Image.open(x) if isinstance(x, str) else x
    # un PNG que no salió de una cámara casi siempre es una captura o un diseño: nunca se recorta
    if isinstance(x, str) and x.lower().endswith(".png"):
        try:
            ex = im.getexif()
            if not (ex.get(271) or ex.get(272)):
                return True
        except Exception:
            return True
    if isinstance(x, str) and x.lower().endswith((".jpg", ".jpeg")):
        try:
            if im.getexif().get(271) or im.getexif().get(272):   # marca/modelo de cámara
                return False
        except Exception:
            pass
    p = im.convert("RGB"); p.thumbnail((200, 200))
    colores = p.getcolors(200 * 200) or []
    if not colores:
        return False
    colores.sort(reverse=True)
    planos = sum(c for c, _ in colores[:12]) / (p.width * p.height)
    return planos > 0.55


def puntaje(ruta):
    """Para elegir las mejores fotos: tamaño, nitidez, luz y si se ve una persona. Devuelve (0-100, notas)."""
    im = ImageOps.exif_transpose(Image.open(ruta)).convert("RGB")
    notas, pts = [], 0
    mp = im.width * im.height / 1e6
    pts += min(30, mp * 12)
    if min(im.size) < 900:
        notas.append("chica (se verá borrosa)"); pts -= 30
    p = im.copy(); p.thumbnail((600, 600))
    nit = ImageStat.Stat(p.convert("L").filter(ImageFilter.FIND_EDGES)).var[0]
    pts += min(30, nit / 25)
    if nit < 150:
        notas.append("algo borrosa")
    luzm = ImageStat.Stat(p.convert("L")).mean[0]
    persona = bool(caras(im))
    # una foto de estudio con fondo oscuro está bien si la persona se ve: la luz pesa poco
    pts += (12 if persona else 20) - min(12 if persona else 20, abs(luzm - 125) / (6 if persona else 4))
    if luzm < 45 and not persona:
        notas.append("oscura")
    if persona:
        pts += 20; notas.append("persona")
    if es_captura(im):
        notas.append("captura de pantalla"); pts = min(pts, 60)
    return int(min(100, pts)), notas
