# Lección 3 · Listo para subir (~1 min)

> Guion para Claude. Lee `guia/estilo.md`. Aquí **no preguntas qué hacer**: lo haces completo y explicas qué cambió. Son 2 mensajes: el resultado y la despedida.

**ACCIÓN (sin preguntar), en silencio** (`<guion>` y `--marca`/`--cta` como en el paso 2):
1. **Todas las medidas:** `carrusel.py <guion> <trabajo>/todas --formato todos --marca <la marca elegida: marca/ o marca-N/>/marca.json --cta "<CTA>"` → `instagram/` (4:5), `tiktok/` (pantalla completa, lejos de los botones) y `linkedin/` (con `carrusel.pdf`, que es como LinkedIn muestra los carruseles). Míralas.
2. **La descripción** (Paso 6 del SKILL.md) según su objetivo, en `<trabajo>/todas/descripcion.txt`, y las vistas: `vista.py <trabajo>/todas --guion <guion> --marca <la marca elegida>/marca.json` (saca la de Instagram y la de TikTok, con su @ y su logo).
3. **Su marca guardada:** Claude Code → `~/.carrusel-pro/marca.json`. App de Claude → el bloque para pegar en un Proyecto.

## Mensaje 1 · El resultado (cierra el turno)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  CARRUSEL PRO
  ▰▰▰  Paso 3 de 3 · Listo para subir
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

- "Lo que más se le escapa a la gente: un carrusel bonito con una descripción de prisa, y en una sola red. Ya tienes las tres."
- **Resultado:** la vista de Instagram y la de TikTok, y en una línea "y el PDF para LinkedIn".
- **La descripción** completa, lista para copiar (con una línea de por qué ayuda a su objetivo: "el gancho de arriba es lo que hace que lo abran").
- **Cómo subirlo, en tu celular:** Instagram **+ → Publicación → selecciona varias** · TikTok **+ → Fotos** · LinkedIn **Empezar una publicación → + → Añadir un documento**.
- "Y tu marca ya quedó guardada: la próxima vez no te pregunto tus colores."
- **Cierra con UNA pregunta: Canva** (revisa antes si tiene sus herramientas en esta sesión). Es lo que más sube el nivel:
  - **Con Canva conectado:** "Lo último, y lo que más se nota: ¿te lo hago también en **Canva**? Queda con fotos e ilustraciones de diseño profesional, y editable en tu cuenta. 1 · Sí, en Canva · 2 · No, así está bien"
  - **Sin Canva:** "Lo último, y lo que más se nota: si conectas **Canva** (gratis), te lo dejo diseñado ahí, con fotos e ilustraciones y editable. Se conecta en **Configuración → Conectores → Canva**. 1 · Ya lo conecté, hazlo · 2 · Así está bien"

**ALTO.**
- **Sí / ya lo conecté:** avisa "Lo armo en tu Canva; tarda como un minuto" y sigue la «Ruta Canva» del SKILL.md con su marca y sus textos. Luego junta las dos vistas: `comparar.py <trabajo>/todas/instagram/vista-instagram.png <trabajo>/canva/vista-instagram.png --salida <trabajo>/claude-vs-canva.jpg --etiquetas "Con Claude" "Con Canva"`. **MENSAJE (cierra el turno):** la imagen, el link para editar en Canva, una línea honesta ("las fotos de Canva las crea su IA; si quieres las tuyas, súbelas a tu Canva y las cambio") y "Escríbeme «listo» para terminar." **ALTO.**
- **No / así está bien:** si tiene Drive (en la compu o conector), una sola oferta más: "¿Te lo guardo en tu Google Drive para abrirlo en el celular? 1 · Sí · 2 · No". Si no, sigue a la despedida.

## Mensaje 2 · Despedida (corta, no es un manual)

- **Lo que lograste** (3 viñetas: tu primer carrusel · con tu marca, como tú lo quisiste · listo para Instagram, TikTok y LinkedIn con su descripción).
- "Desde ahora la skill hace todo esto **sola**, sin que le digas cada paso. Solo dile:"
  > **Usando la skill dak-carrusel-pro, hazme un carrusel sobre [tu tema]**
- "Si quieres la siguiente herramienta gratis, sigue a @dakexplica en TikTok e Instagram."

Guarda `"leccion": "terminada"`. Fin de la guía.

## Si pregunta cómo sacarle más (solo si pregunta)
- **Una serie de 5 para la semana:** «Usando la skill dak-carrusel-pro, hazme 5 carruseles para mi semana».
- **De algo que ya tienes:** pégale un artículo, un PDF o un link y lo convierte en carrusel.
