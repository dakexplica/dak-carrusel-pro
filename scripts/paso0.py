#!/usr/bin/env python3
"""Paso 0 de dak-carrusel-pro: revisa que esté todo lo que la skill necesita.

  python3 paso0.py              → solo revisa y explica qué falta (no instala nada)
  python3 paso0.py --instalar   → instala Pillow si falta (solo con permiso de la persona)

Obligatorio: Python 3.8+ y Pillow (dibuja las láminas).
Opcional (la skill funciona sin esto): internet (marca desde tu página, fotos y logos reales),
un navegador Chrome/Edge o Playwright (captura de tu página dentro de un iPhone) y la carpeta de Google Drive.
Imprime al final:  LISTO   o   FALTA <qué>
"""
import site as _site, sys as _sys
if _site.getusersitepackages() not in _sys.path:  # que encuentre lo que instaló el Paso 0
    _sys.path.append(_site.getusersitepackages())
import glob, importlib.util, os, subprocess, sys, urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
instalar = "--instalar" in sys.argv


def ok(t): print(f"  ✓ {t}")
def opc(t): print(f"  · {t}")


print("Revisando lo que necesita Carrusel Pro:\n")
falta = None
v = sys.version_info
if v >= (3, 8):
    ok(f"Python {v.major}.{v.minor}")
else:
    print(f"  ✗ Python 3.8 o más nuevo — tienes {v.major}.{v.minor}; instálalo desde python.org"); falta = "Python"

if importlib.util.find_spec("PIL") is None:
    if instalar:
        r = subprocess.run([sys.executable, "-m", "pip", "install", "--user", "pillow"], capture_output=True, text=True)
        if r.returncode != 0:
            r = subprocess.run([sys.executable, "-m", "pip", "install", "--user", "--break-system-packages", "pillow"],
                               capture_output=True, text=True)
        importlib.invalidate_caches()
    if importlib.util.find_spec("PIL") is not None:
        ok("Pillow (dibuja las láminas)")
    else:
        print("  ✗ Pillow — es la herramienta con la que dibujo las láminas (unos 10 MB, gratis)"); falta = falta or "Pillow"
else:
    ok("Pillow (dibuja las láminas)")

try:
    urllib.request.urlopen(urllib.request.Request("https://commons.wikimedia.org/w/api.php?action=query&format=json",
                                                  headers={"User-Agent": "dak-carrusel-pro/1.0"}), timeout=5)
    ok("Internet (marca desde tu página, fotos libres y logos reales)")
except Exception:
    opc("Sin internet: funciona igual, con dibujos y tus propias fotos")

import captura
if importlib.util.find_spec("playwright") or captura.navegadores():
    ok("Navegador para capturas de tu página (opcional)")
else:
    opc("Sin navegador para capturas: si quieres tu página dentro de un iPhone, me pasas una captura de tu celular")

drive = glob.glob(os.path.expanduser("~/Library/CloudStorage/GoogleDrive-*/*")) + \
    glob.glob(os.path.expanduser("~/Google Drive*")) + glob.glob("G:/My Drive") + glob.glob("G:/Mi unidad")
if drive:
    ok("Google Drive en tu compu (puedo guardar ahí el carrusel para abrirlo en el celular)")
else:
    opc("Google Drive no está en esta compu (opcional)")

print("\nLISTO" if not falta else f"\nFALTA {falta}")
try:
    import version; version.avisar()
except Exception:
    pass
