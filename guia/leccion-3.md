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
- **Cierra con UNA pregunta, solo si tiene Canva conectado** (revisa antes si tiene sus herramientas en esta sesión; sin Canva, salta a la de Drive): "Lo último: ¿te lo subo a tu **Canva**? Te queda en **Subidos**, listo para retocarlo o publicarlo desde ahí. Funciona con la cuenta gratis y **no gasta tus créditos de IA**. 1 · Sí, súbelo · 2 · No, así está bien"

**ALTO.**
- **Sí, súbelo:** sigue la «Ruta Canva» del SKILL.md (subir el PDF y las láminas; **nunca** las herramientas de Canva que diseñan con IA). **MENSAJE (cierra el turno):** "Listo: está en tu Canva, en **Proyectos → Subidos → Imágenes** (cada lámina, en orden). No usé créditos." y "Escríbeme «listo» para terminar." **ALTO.**
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
