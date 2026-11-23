#!/usr/bin/env python3
"""carrusel-pro · toma una captura de una página web, como se ve en un celular (para la lámina `captura`).

  python3 captura.py <link> [salida.png] [--compu]

Usa lo que haya en la compu, en este orden: Playwright (si está instalado) o Google Chrome / Chromium / Edge
en modo invisible. Si no hay ninguno, imprime NO_HAY y hay que pedirle a la persona una captura de su celular.
Imprime:  CAPTURA <ruta>   o   NO_HAY <motivo>
Solo abre páginas públicas; nunca entra a cuentas.
"""
import os, shutil, subprocess, sys, tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

OCULTAR = """[id*=cookie i],[class*=cookie i],[id*=consent i],[class*=consent i],[id*=onetrust i],[class*=onetrust i],
[id*=didomi i],[class*=cmp i],[id*=gdpr i],[class*=gdpr i],[aria-label*=cookie i],[class*=CookieBanner],
[id*=popup i][class*=modal i]{display:none!important} body,html{overflow:auto!important}"""

CELULAR = (390, 844, 3)      # iPhone 15: ancho, alto, escala
COMPU = (1440, 900, 2)


def con_playwright(url, salida, w, h, esc, movil):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        nav = p.chromium.launch(args=["--use-mock-keychain", "--password-store=basic"])
        ctx = nav.new_context(viewport={"width": w, "height": h}, device_scale_factor=esc, is_mobile=movil,
                              has_touch=movil, locale="es-MX")
        pag = ctx.new_page()
        try:
            pag.goto(url, wait_until="networkidle", timeout=15000)
        except Exception:                 # páginas que nunca se quedan quietas (anuncios, chats): basta con que cargue
            pag.wait_for_load_state("load", timeout=15000)
        pag.wait_for_timeout(1500)
        # avisos de cookies y ventanas que tapan la página (sin aceptar nada por la persona: solo se ocultan)
        pag.add_style_tag(content=OCULTAR)
        pag.wait_for_timeout(300)
        pag.screenshot(path=salida)
        nav.close()


def navegadores():
    rutas = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    ]
    for n in ("google-chrome", "chromium", "chromium-browser", "microsoft-edge"):
        r = shutil.which(n)
        if r:
            rutas.append(r)
    return [r for r in rutas if os.path.exists(r)]


def con_chrome(url, salida, w, h, esc, movil):
    for nav in navegadores():
        perfil = tempfile.mkdtemp(prefix="carrusel-captura-")
        # --use-mock-keychain y --password-store=basic: que Chrome NUNCA pida el llavero ni contraseñas de la persona
        args = [nav, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--user-data-dir={perfil}",
                "--use-mock-keychain", "--password-store=basic", "--no-first-run", "--no-default-browser-check",
                f"--window-size={w},{h}", f"--force-device-scale-factor={esc}", f"--screenshot={salida}",
                "--virtual-time-budget=6000"]
        if movil:
            args.append("--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 "
                        "(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1")
        try:
            subprocess.run(args + [url], capture_output=True, timeout=60)
        except Exception:
            pass
        shutil.rmtree(perfil, ignore_errors=True)
        if os.path.exists(salida) and os.path.getsize(salida) > 5000:
            return True
    return False


def main():
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if not a:
        print(__doc__); sys.exit(1)
    url = a[0] if a[0].startswith("http") else "https://" + a[0]
    salida = a[1] if len(a) > 1 else "captura.png"
    movil = "--compu" not in sys.argv
    w, h, esc = CELULAR if movil else COMPU
    os.makedirs(os.path.dirname(os.path.abspath(salida)), exist_ok=True)
    hecho = False
    try:
        con_playwright(url, salida, w, h, esc, movil)
        hecho = os.path.exists(salida)
    except Exception:
        hecho = False
    if not hecho:
        hecho = con_chrome(url, salida, w, h, esc, movil)
    if hecho and movil:
        try:
            from PIL import Image
            import marcos
            marcos.con_barra(Image.open(salida)).save(salida)   # como una captura de celular de verdad
        except Exception:
            pass
    print(f"CAPTURA {salida}" if hecho else
          "NO_HAY no tengo un navegador para tomar la captura. Pídele a la persona una captura de su celular.")
    try:
        import version; version.avisar()
    except Exception:
        pass


if __name__ == "__main__":
    main()
