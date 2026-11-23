# Lección 1 · Tu primer carrusel en 2 minutos (~2 min)

> Guion para Claude. Antes lee `guia/estilo.md`. Entre comillas va la idea de lo que dices (con tus palabras). **ACCIÓN** = lo haces tú. **BOTONES** = pregunta con `AskUserQuestion` (si no existe, lista numerada corta). **ALTO** = esperas. Nunca sigas sin respuesta. Progreso en `~/.dakexplica/carrusel-pro.json` (`"leccion": 1`). En la app de Claude no hay archivo: lleva el progreso en el chat.

## 1 · Bienvenida (tu PRIMER mensaje, antes de cualquier botón o comando)

**Regla dura:** lo primero que ve la persona es esta bienvenida, como mensaje propio, y con ella **terminas tu turno**. Nada de narrar lo que haces ni hablar de la persona en tercera persona. El Paso 0 corre después y en silencio.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  CARRUSEL PRO
  ▰▱▱  Lección 1 de 3 · Tu primer carrusel
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

> **¡Hola, [nombre]! Bienvenido a la guía 👋**
> En unos 5 minutos vas a tener un carrusel tuyo, con tu marca, listo para subir a Instagram o TikTok.
>
> *"La hice porque diseñar un carrusel me quitaba una tarde entera. Ahora le digo el tema y en minutos tengo las láminas, la descripción y los hashtags." — @dakexplica*
>
> Son 3 lecciones cortas. Te enseño lo que pasa por dentro; cuando la uses normal, hace todo esto **sola**.

- Si no sabes su nombre: "¡Hola! Bienvenido a la guía 👋" y cierra con **"Antes de empezar, ¿cómo te llamo?"**. Si lo sabes: **"Cuando estés listo, escríbeme «vamos»."** **ALTO** (fin del turno). Guarda el nombre (`"nombre"`).

**Siguiente turno:** reacciona en una línea ("¡Mucho gusto, [nombre]!") y **BOTONES** (tres preguntas en la misma ventana):
1. "¿De qué hacemos tu primer carrusel?"
   - **De lo mío** — "tu negocio, tu trabajo o un tema que te guste. Me lo escribes en el siguiente paso"
   - **El de ejemplo** — "una cafetería: 6 láminas sobre cómo saber si tu café está mal hecho. Sale en segundos"
2. "¿Dónde lo vas a publicar?"
   - **Instagram** · **TikTok (modo foto)** · **Todo lo anterior**
3. "¿Qué quieres lograr con tus carruseles?"
   - **Vender más** · **Enseñar algo** · **Que me conozcan (marca personal)** · **Todo lo anterior**

**ALTO.** Reacciona a lo que eligió ("Vender, perfecto: la última lámina va a invitar a escribirte") y guarda `tema`, `destino` y `objetivo`.

## 2 · Lista para dibujar

**ACCIÓN:** corre el Paso 0 del SKILL.md en silencio (Python 3 y Pillow). Si falta algo, explica en una frase qué es ("Pillow es la herramienta con la que dibujo las láminas") y **BOTONES**: **Sí, instálalo** · **Ahora no**. Sin Pillow no se puede seguir: si dice que no, dile qué hacer y para.

## 3 · Tu primer carrusel

- **De lo suyo:** aquí la persona escribe la **única instrucción de toda la guía**. "Ahora te toca a ti. Copia esto y cambia el tema por el tuyo:"

  > **Usando la skill carrusel-pro, hazme un carrusel sobre [tu tema]**

  **ALTO.** Con lo que escriba, **no hagas la entrevista completa** (esa es para el uso normal): usa lo que ya sabes (`destino`, `objetivo`), estilo **Minimal**, sin marca (la marca es la lección 2) y dibujos hechos por ti. Avisa en una línea: "Voy a escribir el texto de cada lámina, dibujar las ilustraciones y revisarlo todo. Tarda 1 o 2 minutos."

  **ACCIÓN:** sigue los Pasos 2 a 4 del SKILL.md (6 láminas: portada con gancho, 4 de valor, cierre con CTA que siempre aplique). Guarda el guion en `~/carrusel-pro/<tema-corto>/guion.json` y renderiza a esa carpeta. **Mira `_revision.jpg`** y corrige lo que esté mal antes de enseñarlo.

- **El de ejemplo:** avisa "Lo dibujo en unos segundos" y **ACCIÓN:**
  ```bash
  python3 <skill>/scripts/carrusel.py <skill>/ejemplos/cafeteria.json ~/carrusel-pro/ejemplo-cafeteria
  ```
  (Si eligió TikTok, cambia `"formato"` a `"tiktok"` en una copia del JSON.) Mira `_revision.jpg`.

**MENSAJE obligatorio (cierra el turno, nada de botones después):**
- **Resultado** + dónde está `_revision.jpg` para abrirlo (todas las láminas juntas) y la carpeta con las láminas sueltas.
- En 3 líneas qué hizo cada parte, empezando por lo que quiere lograr: "La portada es el gancho (es lo único que se ve en el feed) · cada lámina tiene una sola idea · la última cierra con [CTA según `objetivo`]".
- **Lo que lograste** (2 viñetas) y "En la lección 2 le ponemos **tu marca**: tus colores, tu letra y tu logo, o te invento una. Escríbeme «sigue»."

**ALTO.** Guarda `"leccion": 2`.
