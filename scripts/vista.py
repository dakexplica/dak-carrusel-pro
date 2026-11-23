#!/usr/bin/env python3
"""carrusel-pro · enseña el carrusel como se va a ver publicado: dentro de un iPhone, en Instagram o en TikTok.

  python3 vista.py <carpeta del carrusel> [--guion guion.json] [--marca marca.json] [--red instagram|tiktok]

Lee 01.png (y cuenta las láminas), la marca del guion (logo y @usuario) y, si existe, descripcion.txt.
Deja `vista-instagram.png` o `vista-tiktok.png` (1080×1350) en la carpeta e imprime:  VISTA <ruta>
Es una vista de muestra para que la persona vea el resultado en su contexto; no publica nada.
"""
import json, os, sys

from PIL import Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import marcos

W, H = 1170, 2532
ACENTO = {}                # color e inicial de la marca para la foto de perfil cuando no hay logo          # pantalla de iPhone 15 a 3x
NEGRO, GRIS, BLANCO = (0, 0, 0), (115, 115, 115), (255, 255, 255)


def f(n, t):
    return marcos._fuente(n, t)


def avatar(logo, lado, color=(226, 61, 46)):
    a = Image.new("RGBA", (lado, lado), (0, 0, 0, 0))
    m = Image.new("L", (lado, lado), 0)
    ImageDraw.Draw(m).ellipse([0, 0, lado - 1, lado - 1], fill=255)
    if logo and os.path.exists(logo):
        lg = Image.open(logo).convert("RGBA")
        base = Image.new("RGBA", (lado, lado), BLANCO + (255,))
        lg.thumbnail((int(lado * 0.8), int(lado * 0.8)))
        base.alpha_composite(lg, ((lado - lg.width) // 2, (lado - lg.height) // 2))
    else:                                     # sin logo: el color de su marca con su inicial
        color = ACENTO.get("c", color)
        base = Image.new("RGBA", (lado, lado), color + (255,))
        ini = ACENTO.get("ini", "")
        if ini:
            fi = f("InstrumentSans-Bold.ttf", lado * 0.5)
            dd = ImageDraw.Draw(base)
            claro = sum(color) > 480
            dd.text((lado / 2 - fi.getlength(ini) / 2, lado * 0.2), ini, font=fi, fill=(17, 17, 17) if claro else BLANCO)
    a.paste(base, (0, 0), m)
    return a


def corazon(d, x, y, s, col, w=7):
    d.arc([x, y, x + s * 0.55, y + s * 0.5], 150, 360, fill=col, width=w)
    d.arc([x + s * 0.45, y, x + s, y + s * 0.5], 180, 30, fill=col, width=w)
    d.line([x + s * 0.03, y + s * 0.33, x + s * 0.5, y + s * 0.88, x + s * 0.97, y + s * 0.33], fill=col, width=w, joint="curve")


def burbuja(d, x, y, s, col, w=7):
    d.ellipse([x, y, x + s, y + s * 0.92], outline=col, width=w)
    d.line([x + s * 0.12, y + s * 0.72, x + s * 0.02, y + s * 0.98, x + s * 0.32, y + s * 0.86], fill=col, width=w, joint="curve")


def avion(d, x, y, s, col, w=7):
    d.line([x, y + s * 0.42, x + s, y, x + s * 0.62, y + s, x + s * 0.44, y + s * 0.56, x, y + s * 0.42],
           fill=col, width=w, joint="curve")
    d.line([x + s * 0.44, y + s * 0.56, x + s, y], fill=col, width=w)


def guardar(d, x, y, s, col, w=7):
    d.line([x, y, x + s * 0.8, y, x + s * 0.8, y + s, x + s * 0.4, y + s * 0.7, x, y + s, x, y],
           fill=col, width=w, joint="curve")


def sin_emoji(t):
    import re
    return re.sub("[\U0001F000-\U0001FFFF\u2600-\u27BF\uFE0F\u200D]", "", t).strip()


def lineas(texto, fuente_, ancho, maximo):
    pal, out, act = sin_emoji(texto).split(), [], ""
    for p in pal:
        prueba = (act + " " + p).strip()
        if fuente_.getlength(prueba) > ancho and act:
            out.append(act); act = p
            if len(out) == maximo:
                break
        else:
            act = prueba
    if len(out) < maximo and act:
        out.append(act)
    return out


def instagram(lam, n, usuario, logo, desc):
    p = Image.new("RGB", (W, H), BLANCO)
    p.paste(marcos.barra_estado(W), (0, 0))
    d = ImageDraw.Draw(p)
    y = 170
    p.paste(avatar(logo, 100), (36, y), avatar(logo, 100))
    d.text((158, y + 26), usuario.lstrip("@") or "tu_cuenta", font=f("InstrumentSans-Bold.ttf", 40), fill=NEGRO)
    for i in range(3):
        d.ellipse([W - 90 + i * 22, y + 46, W - 80 + i * 22, y + 56], fill=NEGRO)
    y += 130
    alto = int(W * lam.height / lam.width)
    p.paste(lam.convert("RGB").resize((W, alto), Image.LANCZOS), (0, y))
    d.rounded_rectangle([W - 150, y + 30, W - 30, y + 92], radius=31, fill=(30, 30, 30))
    t = f"1/{n}"
    ft = f("InstrumentSans-Bold.ttf", 34)
    d.text((W - 90 - ft.getlength(t) / 2, y + 41), t, font=ft, fill=BLANCO)
    y += alto + 40
    corazon(d, 40, y, 74, NEGRO); burbuja(d, 160, y, 70, NEGRO); avion(d, 278, y + 2, 70, NEGRO)
    guardar(d, W - 100, y, 66, NEGRO)
    for i in range(min(n, 8)):                       # puntitos del carrusel
        cx = W / 2 + (i - (min(n, 8) - 1) / 2) * 26
        d.ellipse([cx - 7, y + 28, cx + 7, y + 42], fill=(0, 149, 246) if i == 0 else (200, 200, 200))
    y += 120
    fu = f("InstrumentSans-Bold.ttf", 38)
    fr = f("InstrumentSans-Regular.ttf", 38)
    u = (usuario.lstrip("@") or "tu_cuenta") + " "
    palabras = sin_emoji(" ".join(desc.strip().splitlines()[:2])).split()
    renglones, act, i = [], "", 0
    anchos = [W - 80 - fu.getlength(u), W - 80 - fr.getlength("… más")]
    while i < len(palabras) and len(renglones) < 2:
        prueba = (act + " " + palabras[i]).strip()
        if fr.getlength(prueba) > anchos[len(renglones)] and act:
            renglones.append(act); act = ""
        else:
            act = prueba; i += 1
    if act and len(renglones) < 2:
        renglones.append(act)
    if renglones:
        d.text((40, y), u, font=fu, fill=NEGRO)
        d.text((40 + fu.getlength(u), y), renglones[0], font=fr, fill=NEGRO)
        if len(renglones) > 1:
            resto = renglones[1] + ("… más" if i < len(palabras) else "")
            d.text((40, y + 52), resto, font=fr, fill=NEGRO)
    # barra de abajo
    yb = H - 250
    d.line([0, yb, W, yb], fill=(230, 230, 230), width=2)
    xs = [W * k / 10 for k in (1, 3, 5, 7, 9)]
    c = NEGRO
    d.polygon([(xs[0] - 34, yb + 82), (xs[0], yb + 50), (xs[0] + 34, yb + 82), (xs[0] + 26, yb + 82), (xs[0] + 26, yb + 124),
               (xs[0] - 26, yb + 124), (xs[0] - 26, yb + 82)], fill=c)
    d.ellipse([xs[1] - 28, yb + 56, xs[1] + 20, yb + 104], outline=c, width=7)
    d.line([xs[1] + 14, yb + 98, xs[1] + 36, yb + 120], fill=c, width=8)
    d.rounded_rectangle([xs[2] - 36, yb + 52, xs[2] + 36, yb + 124], radius=20, outline=c, width=7)
    d.line([xs[2], yb + 70, xs[2], yb + 106], fill=c, width=7); d.line([xs[2] - 18, yb + 88, xs[2] + 18, yb + 88], fill=c, width=7)
    d.rounded_rectangle([xs[3] - 36, yb + 52, xs[3] + 36, yb + 124], radius=20, outline=c, width=7)
    d.polygon([(xs[3] - 10, yb + 74), (xs[3] + 16, yb + 88), (xs[3] - 10, yb + 102)], fill=c)
    p.paste(avatar(logo, 76), (int(xs[4] - 38), yb + 50), avatar(logo, 76))
    d.rounded_rectangle([W / 2 - 200, H - 40, W / 2 + 200, H - 28], radius=6, fill=NEGRO)
    return p


def tiktok(lam, n, usuario, logo, desc):
    p = Image.new("RGB", (W, H), NEGRO)
    l = lam.convert("RGB")
    esc = W / l.width                                    # modo foto: a lo ancho, franjas negras arriba y abajo
    l = l.resize((int(l.width * esc + .5), int(l.height * esc + .5)), Image.LANCZOS)
    p.paste(l, ((W - l.width) // 2, (H - l.height) // 2))
    sombra = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sombra)
    for i in range(520):
        sd.line([0, H - i, W, H - i], fill=(0, 0, 0, int(170 * (1 - i / 520))))
    for i in range(330):
        sd.line([0, i, W, i], fill=(0, 0, 0, int(140 * (1 - i / 330))))
    p = p.convert("RGBA"); p.alpha_composite(sombra); p = p.convert("RGB")
    barra = marcos.barra_estado(W, (0, 0, 0), BLANCO)
    p.paste(barra, (0, 0), barra.convert("L").point(lambda v: 255 if v > 128 else 0))
    # todo lo blanco de TikTok lleva sombra suave, como en la app, para leerse sobre cualquier lámina
    capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    fb = f("InstrumentSans-Bold.ttf", 44)
    for t, x in (("Siguiendo", W / 2 - 230), ("Para ti", W / 2 + 60)):
        d.text((x, 190), t, font=fb, fill=BLANCO if t == "Para ti" else (220, 220, 220))
    d.line([W / 2 + 70, 252, W / 2 + 190, 252], fill=BLANCO, width=6)
    x = W - 140
    y = 1180 + 190
    corazon(d, x, y, 100, BLANCO, 9); y += 200
    burbuja(d, x + 4, y, 92, BLANCO, 9); y += 190
    guardar(d, x + 18, y, 80, BLANCO, 9); y += 180
    avion(d, x + 6, y, 92, BLANCO, 9)
    d.text((44, H - 520), usuario or "@tu_cuenta", font=fb, fill=BLANCO)
    fr = f("InstrumentSans-Regular.ttf", 40)
    for i, r in enumerate(lineas((desc.strip().splitlines() or [""])[0], fr, W - 260, 2)):
        d.text((44, H - 450 + i * 54), r, font=fr, fill=BLANCO)
    from PIL import ImageFilter
    sombra = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sombra.putalpha(capa.getchannel("A").filter(ImageFilter.GaussianBlur(7)).point(lambda v: min(255, v * 2) * 0.55))
    p = p.convert("RGBA"); p.alpha_composite(sombra); p.alpha_composite(capa); p = p.convert("RGB")
    p.paste(avatar(logo, 110), (x - 5, 1180), avatar(logo, 110))
    d = ImageDraw.Draw(p)
    for i in range(min(n, 10)):
        cx = W / 2 + (i - (min(n, 10) - 1) / 2) * 30
        d.ellipse([cx - 8, H - 300, cx + 8, H - 284], fill=BLANCO if i == 0 else (150, 150, 150))
    d.rectangle([0, H - 230, W, H], fill=NEGRO)
    return p


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__); sys.exit(1)
    carpeta = a[0]
    guion = a[a.index("--guion") + 1] if "--guion" in a else None
    red = a[a.index("--red") + 1] if "--red" in a else ("tiktok" if os.path.basename(os.path.normpath(carpeta)) == "tiktok" else "instagram")
    marca = {}
    if guion and os.path.exists(guion):
        marca = json.load(open(guion, encoding="utf-8")).get("marca", {})
        if marca.get("logo") and not os.path.isabs(marca["logo"]):
            marca["logo"] = os.path.join(os.path.dirname(os.path.abspath(guion)), marca["logo"])
    if "--marca" in a:                       # la marca elegida (marca.json de marca.py o inventada) manda
        mj = a[a.index("--marca") + 1]
        mm = json.load(open(mj, encoding="utf-8"))
        marca = {"usuario": mm.get("usuario") or "@" + "".join(ch for ch in (mm.get("nombre") or "tu_marca").lower() if ch.isalnum()),
                 "logo": mm.get("logo") if mm.get("logo") and os.path.exists(mm["logo"]) else None}
    pngs = sorted(x for x in os.listdir(carpeta) if x[:2].isdigit() and x.endswith(".png"))
    subs = [r for r in ("instagram", "tiktok") if os.path.isdir(os.path.join(carpeta, r))]
    if not pngs and subs and "--red" not in a:     # formato "ambos"/"todos": una vista por red
        import subprocess
        for r in subs:
            subprocess.run([sys.executable, os.path.abspath(__file__), os.path.join(carpeta, r)] +
                           (["--guion", guion] if guion else []) +
                           (["--marca", a[a.index("--marca") + 1]] if "--marca" in a else []) + ["--red", r])
        return
    if not pngs:
        print("NADA no hay láminas (01.png…) en esa carpeta"); sys.exit(2)
    lam = Image.open(os.path.join(carpeta, pngs[0]))
    col = (mm if "--marca" in a else marca).get("colores", {}).get("acento") if ("--marca" in a or marca) else None
    if col:
        ACENTO["c"] = tuple(int(col.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    ACENTO["ini"] = (marca.get("usuario") or "@").lstrip("@")[:1].upper()
    desc = ""
    for cand in (os.path.join(carpeta, "descripcion.txt"), os.path.join(os.path.dirname(os.path.normpath(carpeta)), "descripcion.txt")):
        if os.path.exists(cand):
            desc = open(cand, encoding="utf-8").read(); break
    hacer = instagram if red == "instagram" else tiktok
    pantalla = hacer(lam, len(pngs), marca.get("usuario", ""), marca.get("logo"), desc)
    tel = marcos.iphone(pantalla, 1240)
    lienzo = Image.new("RGBA", (1080, 1350), (244, 245, 247, 255))
    lienzo.alpha_composite(tel, ((1080 - tel.width) // 2, (1350 - tel.height) // 2 + 10))
    ruta = os.path.join(carpeta, f"vista-{red}.png")
    lienzo.convert("RGB").save(ruta, optimize=True)
    print(f"VISTA {ruta}")
    try:
        import version; version.avisar()
    except Exception:
        pass


if __name__ == "__main__":
    main()
