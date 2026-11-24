"""Ilustraciones dibujadas por código para carrusel-pro.

NO es una biblioteca para escoger: Claude dibuja una ilustración NUEVA para cada slide, del tema
que sea, escribiendo la lista de figuras en el guion ("dibujo": [...]). Los dibujos de EJEMPLOS
solo enseñan el formato y el nivel de detalle esperado.

Cada dibujo es una lista de figuras en una caja de 0 a 100 (x, y). El mismo formato sirve para
los iconos de la biblioteca y para dibujos a la medida que Claude escribe en el guion
("dibujo": [...]). Colores: "tinta", "acento", "fondo", "suave", "claro" (acento muy suave),
"none" o un "#hex".

Figuras:
  ["circulo", cx, cy, r, relleno, trazo]
  ["elipse", x0, y0, x1, y1, relleno, trazo]
  ["rect", x0, y0, x1, y1, radio, relleno, trazo]
  ["poligono", [x, y, x, y, ...], relleno, trazo]
  ["linea", [x, y, x, y, ...], color]            (trazo redondeado)
  ["arco", cx, cy, r, grado_ini, grado_fin, color]
  ["curva", [x, y, x, y, ...], relleno, trazo]   (forma orgánica suave que pasa por los puntos;
                                                relleno "none" = solo línea abierta)
  ["texto", x, y, "Hola", tam, color]            (x = CENTRO del texto, y = su borde de arriba; tam en unidades de la caja)
Opcional al final de cualquier figura: {"grosor": 4}
"""
from PIL import Image, ImageDraw, ImageFont
import os

S = 4  # sobremuestreo para que los bordes salgan suaves

EJEMPLOS = {
    "taza": [
        ["linea", [36, 8, 32, 16, 38, 24, 34, 32], "suave"],
        ["linea", [52, 4, 48, 13, 54, 21, 50, 30], "suave"],
        ["linea", [68, 8, 64, 16, 70, 24, 66, 32], "suave"],
        ["arco", 80, 58, 13, 270, 90, "tinta", {"grosor": 6}],
        ["poligono", [18, 38, 86, 38, 80, 82, 24, 82], "acento", "tinta"],
        ["rect", 20, 38, 84, 46, 3, "claro", "tinta"],
        ["elipse", 8, 82, 96, 94, "claro", "tinta"],
    ],
    "foco": [
        ["circulo", 50, 40, 30, "claro", "tinta"],
        ["linea", [40, 44, 46, 54, 50, 44, 54, 54, 60, 44], "acento"],
        ["rect", 38, 68, 62, 80, 3, "acento", "tinta"],
        ["rect", 41, 80, 59, 90, 4, "tinta", "tinta"],
        ["linea", [50, 2, 50, 6], "acento"], ["linea", [14, 18, 18, 21], "acento"],
        ["linea", [86, 18, 82, 21], "acento"],
    ],
    "reloj": [
        ["circulo", 50, 54, 40, "claro", "tinta"],
        ["circulo", 50, 54, 32, "fondo", "tinta"],
        ["linea", [50, 54, 50, 32], "tinta"], ["linea", [50, 54, 66, 62], "acento"],
        ["circulo", 50, 54, 4, "tinta", "none"],
        ["rect", 42, 6, 58, 14, 3, "acento", "tinta"],
    ],
    "dinero": [
        ["rect", 6, 26, 94, 76, 6, "claro", "tinta"],
        ["circulo", 50, 51, 15, "acento", "tinta"],
        ["texto", 50, 37, "$", 26, "fondo"],
        ["circulo", 20, 51, 4, "tinta", "none"], ["circulo", 80, 51, 4, "tinta", "none"],
    ],
    "grafica": [
        ["linea", [8, 90, 94, 90], "tinta"],
        ["rect", 14, 62, 30, 90, 3, "claro", "tinta"],
        ["rect", 40, 44, 56, 90, 3, "claro", "tinta"],
        ["rect", 66, 22, 82, 90, 3, "acento", "tinta"],
        ["linea", [14, 46, 42, 28, 60, 34, 88, 8], "acento"],
        ["poligono", [78, 6, 92, 4, 90, 18], "acento", "none"],
    ],
    "cohete": [
        ["poligono", [50, 4, 68, 30, 68, 70, 32, 70, 32, 30], "claro", "tinta"],
        ["circulo", 50, 36, 9, "acento", "tinta"],
        ["poligono", [32, 50, 18, 72, 32, 70], "acento", "tinta"],
        ["poligono", [68, 50, 82, 72, 68, 70], "acento", "tinta"],
        ["poligono", [40, 72, 50, 96, 60, 72], "acento", "none"],
    ],
    "corazon": [
        ["poligono", [50, 88, 12, 50, 8, 32, 16, 18, 32, 12, 44, 18, 50, 28, 56, 18, 68, 12, 84, 18,
                      92, 32, 88, 50], "acento", "tinta"],
        ["arco", 30, 34, 10, 200, 270, "fondo"],
    ],
    "telefono": [
        ["rect", 26, 4, 74, 96, 9, "tinta", "tinta"],
        ["rect", 30, 12, 70, 84, 4, "claro", "none"],
        ["rect", 36, 22, 60, 30, 3, "acento", "none"],
        ["rect", 36, 36, 64, 42, 3, "fondo", "none"], ["rect", 36, 48, 56, 54, 3, "fondo", "none"],
        ["circulo", 50, 90, 3, "fondo", "none"],
    ],
    "lupa": [
        ["circulo", 42, 42, 28, "claro", "tinta"],
        ["arco", 42, 42, 18, 200, 260, "fondo"],
        ["linea", [62, 62, 88, 88], "tinta", {"grosor": 9}],
    ],
    "check": [
        ["circulo", 50, 50, 42, "acento", "tinta"],
        ["linea", [30, 52, 44, 66, 72, 36], "fondo", {"grosor": 8}],
    ],
    "estrella": [
        ["poligono", [50, 6, 61, 37, 94, 38, 68, 58, 77, 90, 50, 71, 23, 90, 32, 58, 6, 38, 39, 37],
         "acento", "tinta"],
    ],
    "libro": [
        ["poligono", [50, 22, 10, 14, 10, 80, 50, 88], "claro", "tinta"],
        ["poligono", [50, 22, 90, 14, 90, 80, 50, 88], "fondo", "tinta"],
        ["linea", [18, 32, 40, 36], "suave"], ["linea", [18, 44, 40, 48], "suave"],
        ["linea", [60, 36, 82, 32], "acento"], ["linea", [60, 48, 82, 44], "suave"],
    ],
    "chispas": [
        ["poligono", [40, 10, 46, 34, 70, 40, 46, 46, 40, 70, 34, 46, 10, 40, 34, 34], "acento", "none"],
        ["poligono", [76, 56, 79, 67, 90, 70, 79, 73, 76, 84, 73, 73, 62, 70, 73, 67], "tinta", "none"],
        ["poligono", [74, 8, 76, 15, 83, 17, 76, 19, 74, 26, 72, 19, 65, 17, 72, 15], "suave", "none"],
    ],
    "termometro": [
        ["rect", 40, 6, 60, 70, 10, "fondo", "tinta"],
        ["circulo", 50, 78, 16, "acento", "tinta"],
        ["rect", 46, 36, 54, 72, 4, "acento", "none"],
        ["linea", [62, 20, 70, 20], "suave"], ["linea", [62, 34, 70, 34], "suave"],
        ["linea", [62, 48, 70, 48], "suave"],
    ],
    "bolsa": [
        ["arco", 50, 34, 16, 180, 360, "tinta", {"grosor": 6}],
        ["poligono", [16, 32, 84, 32, 90, 92, 10, 92], "acento", "tinta"],
        ["circulo", 36, 46, 3, "fondo", "none"], ["circulo", 64, 46, 3, "fondo", "none"],
    ],
    "mensaje": [
        ["rect", 6, 10, 80, 62, 12, "claro", "tinta"],
        ["poligono", [20, 60, 18, 80, 38, 62], "claro", "tinta"],
        ["rect", 36, 40, 94, 84, 12, "acento", "tinta"],
        ["linea", [18, 28, 60, 28], "suave"], ["linea", [18, 42, 32, 42], "suave"],
    ],
    "rayo": [
        ["poligono", [58, 4, 20, 56, 46, 56, 38, 96, 80, 40, 54, 40], "acento", "tinta"],
    ],
    "robot": [
        ["linea", [50, 4, 50, 16], "tinta"], ["circulo", 50, 6, 5, "acento", "none"],
        ["rect", 16, 16, 84, 70, 14, "claro", "tinta"],
        ["circulo", 36, 40, 7, "tinta", "none"], ["circulo", 64, 40, 7, "tinta", "none"],
        ["linea", [38, 56, 62, 56], "acento"],
        ["rect", 30, 74, 70, 94, 6, "acento", "tinta"],
    ],
}


def _color(nombre, pal):
    if nombre in (None, "none"):
        return None
    if isinstance(nombre, str) and nombre.startswith("#"):
        h = nombre.lstrip("#")
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (255,)
    return pal.get(nombre, pal["tinta"])


def _suave(pp, cerrada, pasos=14):
    """Catmull-Rom: une los puntos con una curva suave."""
    pts = [(pp[i], pp[i + 1]) for i in range(0, len(pp), 2)]
    if len(pts) < 3:
        return pp
    ext = ([pts[-1]] + pts + pts[:2]) if cerrada else ([pts[0]] + pts + [pts[-1]])
    out = []
    for i in range(1, len(ext) - 2):
        p0, p1, p2, p3 = ext[i - 1], ext[i], ext[i + 1], ext[i + 2]
        for j in range(pasos):
            t = j / pasos
            t2, t3 = t * t, t * t * t
            for c in (0, 1):
                out.append(0.5 * (2 * p1[c] + (-p0[c] + p2[c]) * t + (2 * p0[c] - 5 * p1[c] + 4 * p2[c] - p3[c]) * t2
                                  + (-p0[c] + 3 * p1[c] - 3 * p2[c] + p3[c]) * t3))
    if not cerrada:
        out += list(pts[-1])
    return out


def dibujar(img, figuras, caja, pal, grosor_base=3.2, fuente_ttf=None):
    """Dibuja `figuras` (o el nombre de un icono) dentro de `caja` (x0, y0, x1, y1) sobre `img`."""
    if isinstance(figuras, str):
        figuras = EJEMPLOS.get(figuras, [])
    x0, y0, x1, y1 = [int(v) for v in caja]
    lado = min(x1 - x0, y1 - y0)
    ox, oy = x0 + (x1 - x0 - lado) / 2, y0 + (y1 - y0 - lado) / 2
    capa = Image.new("RGBA", (lado * S, lado * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    k = lado * S / 100.0

    def P(v):
        return [c * k for c in v]

    for fig in figuras:
        fig = list(fig)
        extra = fig.pop() if fig and isinstance(fig[-1], dict) else {}
        g = int(extra.get("grosor", grosor_base) * k)
        t = fig[0]
        if t == "circulo":
            cx, cy, r, rel, tr = fig[1:6]
            d.ellipse(P([cx - r, cy - r, cx + r, cy + r]), fill=_color(rel, pal), outline=_color(tr, pal),
                      width=g if _color(tr, pal) else 0)
        elif t == "elipse":
            a, b, c, e, rel, tr = fig[1:7]
            d.ellipse(P([a, b, c, e]), fill=_color(rel, pal), outline=_color(tr, pal),
                      width=g if _color(tr, pal) else 0)
        elif t == "rect":
            a, b, c, e, rad, rel, tr = fig[1:8]
            d.rounded_rectangle(P([a, b, c, e]), radius=rad * k, fill=_color(rel, pal),
                                outline=_color(tr, pal), width=g if _color(tr, pal) else 0)
        elif t == "poligono":
            pts, rel, tr = fig[1], fig[2], fig[3]
            pp = P(pts)
            if _color(rel, pal):
                d.polygon(pp, fill=_color(rel, pal))
            if _color(tr, pal):
                d.line(pp + pp[:2], fill=_color(tr, pal), width=g, joint="curve")
                for i in range(0, len(pp), 2):
                    d.ellipse([pp[i] - g / 2, pp[i + 1] - g / 2, pp[i] + g / 2, pp[i + 1] + g / 2],
                              fill=_color(tr, pal))
        elif t == "linea":
            pts, col = fig[1], fig[2]
            pp = P(pts)
            d.line(pp, fill=_color(col, pal), width=g, joint="curve")
            for i in (0, len(pp) - 2):
                d.ellipse([pp[i] - g / 2, pp[i + 1] - g / 2, pp[i] + g / 2, pp[i + 1] + g / 2],
                          fill=_color(col, pal))
        elif t == "curva":
            pts, rel, tr = fig[1], fig[2], fig[3]
            cerrada = _color(rel, pal) is not None
            pp = _suave(P(pts), cerrada)
            if cerrada:
                d.polygon(pp, fill=_color(rel, pal))
            if _color(tr, pal):
                d.line(pp + (pp[:2] if cerrada else []), fill=_color(tr, pal), width=g, joint="curve")
                for i in (0, len(pp) - 2):
                    d.ellipse([pp[i] - g / 2, pp[i + 1] - g / 2, pp[i] + g / 2, pp[i + 1] + g / 2],
                              fill=_color(tr, pal))
        elif t == "arco":
            cx, cy, r, a, b, col = fig[1:7]
            d.arc(P([cx - r, cy - r, cx + r, cy + r]), a, b, fill=_color(col, pal), width=g)
        elif t == "texto" and fuente_ttf:
            x, y, txt, tam, col = fig[1:6]
            f = ImageFont.truetype(fuente_ttf, int(tam * k))
            d.text((x * k, y * k), txt, font=f, fill=_color(col, pal), anchor="ma")  # x = centro del texto, y = arriba
    capa = capa.resize((lado, lado), Image.LANCZOS)
    img.alpha_composite(capa, (int(ox), int(oy)))


def muestrario(salida, pal, fuente_ttf):
    """Hoja con todos los iconos y su nombre (para elegir)."""
    nombres = list(EJEMPLOS)
    cols, celda = 5, 220
    filas = (len(nombres) + cols - 1) // cols
    img = Image.new("RGBA", (cols * celda, filas * (celda + 40)), pal["fondo"])
    f = ImageFont.truetype(fuente_ttf, 26)
    d = ImageDraw.Draw(img)
    for i, n in enumerate(nombres):
        x, y = (i % cols) * celda, (i // cols) * (celda + 40)
        dibujar(img, n, (x + 30, y + 20, x + celda - 30, y + celda - 20), pal, fuente_ttf=fuente_ttf)
        d.text((x + celda / 2 - f.getlength(n) / 2, y + celda - 6), n, font=f, fill=pal["tinta"])
    img.convert("RGB").save(salida)
