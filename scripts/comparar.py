#!/usr/bin/env python3
"""carrusel-pro · junta imágenes lado a lado con un número grande (y una etiqueta) encima de cada una,
para que la persona elija viendo: «¿cuál te gusta? Responde 1, 2 o 3» o el antes y después.

  python3 comparar.py <img1> <img2> [<img3> <img4>] --salida comparar.jpg [--etiquetas "Sin marca" "Con tu marca"]

Imprime:  COMPARAR <ruta>
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(AQUI, "..", "fuentes", "InstrumentSans-Bold.ttf")


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__); sys.exit(1)
    salida = a[a.index("--salida") + 1] if "--salida" in a else "comparar.jpg"
    etiquetas = []
    if "--etiquetas" in a:
        i = a.index("--etiquetas") + 1
        while i < len(a) and not a[i].startswith("--"):
            etiquetas.append(a[i]); i += 1
    valores = {salida, *etiquetas}
    imgs = [x for x in a if not x.startswith("--") and x not in valores and os.path.isfile(x)][:4]
    if len(imgs) < 2:
        print("ERROR necesito al menos 2 imágenes que existan"); sys.exit(2)
    ims = [Image.open(x).convert("RGB") for x in imgs]
    alto = 900
    ims = [im.resize((int(im.width * alto / im.height), alto), Image.LANCZOS) for im in ims]
    m, cab = 40, 110
    W = sum(im.width for im in ims) + m * (len(ims) + 1)
    hoja = Image.new("RGB", (W, alto + cab + m), (244, 245, 247))
    d = ImageDraw.Draw(hoja)
    fn, fe = ImageFont.truetype(F, 64), ImageFont.truetype(F, 40)
    x = m
    for k, im in enumerate(ims):
        d.ellipse([x, 22, x + 70, 92], fill=(17, 17, 17))
        t = str(k + 1)
        d.text((x + 35 - fn.getlength(t) / 2, 20), t, font=fn, fill=(255, 255, 255))
        if k < len(etiquetas):
            d.text((x + 90, 36), etiquetas[k], font=fe, fill=(17, 17, 17))
        hoja.paste(im, (x, cab))
        x += im.width + m
    os.makedirs(os.path.dirname(os.path.abspath(salida)), exist_ok=True)
    hoja.save(salida, quality=90)
    print(f"COMPARAR {salida}")


if __name__ == "__main__":
    main()
