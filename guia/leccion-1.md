# Lección 1 · Tu primer carrusel (~2 min)

> Guion para Claude. Antes lee `guia/estilo.md`. Entre comillas va la idea de lo que dices (con tus palabras). **ACCIÓN** = lo haces tú. **BOTONES** = pregunta con `AskUserQuestion` (si no existe, lista numerada corta). **ALTO** = esperas. Nunca sigas sin respuesta. Progreso en `~/.dakexplica/dak-carrusel-pro.json` (`"leccion": 1`). En la app de Claude no hay archivo: lleva el progreso en el chat. `<trabajo>` = `~/carrusel-pro/<tema-corto>/` (con el ejemplo, `~/carrusel-pro/ejemplo-cafeteria/`).

## 1 · Bienvenida (tu PRIMER mensaje, antes de cualquier botón o comando)

**Regla dura:** lo primero que ve la persona es esta bienvenida, como mensaje propio, y con ella **terminas tu turno**. Nada de narrar lo que haces. El Paso 0 corre después y en silencio.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  CARRUSEL PRO
  ▰▱▱  Paso 1 de 3 · Tu primer carrusel
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

> **¡Hola, [nombre]! Bienvenido a la guía 👋**
> En unos 5 minutos vas a tener un carrusel con tu marca, listo para subir, y vas a ver cómo se ve ya publicado.
>
> *"La hice porque diseñar un carrusel me quitaba una tarde entera. Ahora le doy el tema y mi página, y en minutos tengo las láminas, la descripción y los hashtags." — @dakexplica*
>
> Son 3 pasos cortos. Cuando la uses normal, hace todo esto **sola**.

- Si no sabes su nombre: "¡Hola! Bienvenido a la guía 👋" y cierra con **"Antes de empezar, ¿cómo te llamo?"**. Si lo sabes: **"Cuando estés listo, escríbeme «vamos»."** **ALTO** (fin del turno). Guarda `"nombre"`.

**Siguiente turno:** reacciona en una línea ("¡Mucho gusto, [nombre]!") y **BOTONES** (tres preguntas en la misma ventana; lo importante va dentro de cada opción):
1. "¿De qué hacemos tu primer carrusel?"
   - **De lo mío** — "tu negocio, tu trabajo o un tema que te guste; me lo escribes en el siguiente paso"
   - **El de ejemplo** — "una cafetería: cómo saber si tu café está mal hecho. Sale en segundos"
2. "¿Dónde lo vas a publicar?" · **Instagram** · **TikTok (modo foto)** · **LinkedIn** · **Todo lo anterior**
3. "¿Qué quieres lograr con tus carruseles?" · **Vender más** · **Enseñar algo** · **Que me conozcan** · **Todo lo anterior**

**ALTO.** Guarda `tema`, `destino` y `objetivo`. Con eso ya decides dos cosas (sin decirlas como técnica):
- **Formato:** Instagram → `instagram` · TikTok → `tiktok` · LinkedIn → `linkedin` · Todo → `todos`.
- **El cierre (CTA) según lo que quiere:** Vender → «Escríbenos por mensaje» · Enseñar → «Guárdalo para después» · Que me conozcan → «Síguenos para más» · Todo → «Guárdalo y síguenos».

## 2 · Lista para dibujar

**ACCIÓN:** Paso 0 del SKILL.md en silencio (`paso0.py`). Si falta Pillow: una frase ("es la herramienta con la que dibujo las láminas, gratis") y **BOTONES** **Sí, instálala** · **Ahora no**. Sin Pillow no se puede seguir: si dice que no, dile qué hacer y para.

## 3 · Tu primer carrusel

- **De lo suyo:** aquí la persona escribe la **única instrucción de toda la guía**. Reacciona a lo que quiere lograr en una línea y: "Ahora te toca a ti. Copia esto y cambia el tema por el tuyo:"

  > **Usando la skill dak-carrusel-pro, hazme un carrusel sobre [tu tema]**

  **ALTO.** Con lo que escriba, **no hagas la ronda de preguntas** (ya sabes destino y objetivo): estilo "Decide tú", **sin marca** (la marca es el paso 2), fotos reales + dibujos, logos reales si nombra apps, y el CTA de arriba. Avisa en una línea: "Escribo el texto de cada lámina, busco las imágenes, lo dibujo y lo reviso. Tarda 1 o 2 minutos."

  **ACCIÓN:** Pasos 3 a 6 del SKILL.md (6 o 7 láminas) en `<trabajo>`. **Mira `_revision.jpg`** y corrige antes de enseñarlo. Escribe `descripcion.txt` y saca la vista (`vista.py`).

- **El de ejemplo:** reacciona a lo que quiere lograr en una línea, avisa "Lo dibujo en unos segundos" y **ACCIÓN** (cambia el formato y el CTA por los que decidiste):
  ```bash
  python3 <skill>/scripts/carrusel.py <skill>/ejemplos/cafeteria.json ~/carrusel-pro/ejemplo-cafeteria/listo --formato instagram --cta "Escríbenos por mensaje"
  cp <skill>/ejemplos/resultado-cafeteria/descripcion.txt ~/carrusel-pro/ejemplo-cafeteria/listo/
  python3 <skill>/scripts/vista.py ~/carrusel-pro/ejemplo-cafeteria/listo --guion <skill>/ejemplos/cafeteria.json
  ```

**MENSAJE obligatorio (cierra el turno, nada de botones después):**
- **Así se ve publicado:** abre la vista (`vista-instagram.png`; con TikTok, `vista-tiktok.png`; con `todos`, las dos) y debajo `_revision.jpg`. Con LinkedIn no hay vista: enseña `_revision.jpg` y di que el PDF (`carrusel.pdf`) es lo que se sube. Di dónde está la carpeta.
- En 3 líneas qué hace cada parte, **empezando por lo que quiere lograr**: "La última lámina dice «[CTA]», porque quieres [objetivo] · la portada es el gancho (es lo único que se ve en el feed) · cada lámina tiene una sola idea, con una foto real".
- Con el ejemplo, deja la frase para la próxima: "Cuando lo hagas con lo tuyo, solo escribes: **«Usando la skill dak-carrusel-pro, hazme un carrusel sobre [tu tema]»**".
- **Lo que lograste** (2 viñetas) y "En el paso 2 le ponemos **tu marca**: tu logo, tus colores y tu letra. Escríbeme «sigue»."

**ALTO.** Guarda `"leccion": 2`.
