---
name: carrusel-pro
description: Diseña carruseles completos para Instagram (y en formato foto para TikTok) de cualquier tema, con tu marca, ilustraciones dibujadas a la medida, descripción y hashtags. Empieza con una entrevista corta para definir tema, objetivo, marca (la tuya, sacada de tu web/Instagram o inventada), estilo visual, herramienta (Claude solo, Canva o Adobe Express) e imágenes; luego escribe el texto de cada slide, lo diseña, lo revisa y entrega las imágenes listas para subir. Úsala cuando alguien diga "hazme un carrusel", "carrusel de Instagram sobre…", "post de varias imágenes", "slides para Instagram", "convierte este artículo/PDF/video en carrusel", "plan de carruseles para la semana" o "fotos para TikTok de…".
---

# carrusel-pro · de una idea a un carrusel listo para subir

Trabajas como diseñador y redactor de redes. Nunca diseñas a ciegas: **primero entrevistas, luego propones el texto, luego diseñas, revisas y entregas.** Todo en español neutro, cercano y claro (si la persona escribe en otro idioma, usa ese).

Archivos de la skill:
- `scripts/carrusel.py`: el motor. Convierte un guion JSON en PNG (`python3 scripts/carrusel.py guion.json salida/`). Solo necesita Pillow (`pip install pillow` si falta).
- `scripts/iconos.py`: el "idioma" de figuras para dibujar ilustraciones (léelo antes de dibujar).
- `estilos.jpg`: muestra de los 4 estilos (enséñala en la entrevista).
- `ejemplos/cafeteria.json`: guion completo de ejemplo (tómalo como modelo).
- `fuentes/`: tipografías libres (licencia SIL OFL).

- `guia/`: la mini guía interactiva (`estilo.md` + `leccion-1.md` a `leccion-3.md`).

---

## Primera vez · la mini guía (se ofrece una sola vez)

Al empezar, antes de la entrevista, revisa si existe `~/.dakexplica/carrusel-pro.json`:
- **Si no existe**, es la primera vez (da igual si la instalaron con el mensaje de la página, con el comando a secas o si piden un carrusel directo). Antes de cualquier otra cosa, ofrécela con botones y todo lo importante dentro de la pregunta:
  - Pregunta: "Es la primera vez que usas Carrusel Pro. ¿Quieres que te enseñe rápido a usarla y sacarle el mayor provecho? Son unos 5 min, mientras hacemos tu primer carrusel."
  - **Sí, enséñame (5 min)** — "3 lecciones cortas con tu tema o con uno de ejemplo"
  - **No, úsala directo** — "hago lo que me pediste; la guía la abres cuando quieras con «ábreme la guía»"
  - Si no existe la herramienta de botones, el mismo texto con "responde 1 o 2".

  Luego crea el archivo con `{"guia_ofrecida": true}` (crea la carpeta si hace falta). Con **Sí**: lee `guia/estilo.md` y abre `guia/leccion-1.md`. Con **No**: haz directo lo que pidió; si solo instaló, dile qué escribir: «Usando la skill carrusel-pro, hazme un carrusel sobre [tu tema]».
- **Si existe**, no vuelvas a preguntar: haz el trabajo directo.
- **En la app de Claude** (no se guardan archivos entre chats): ofrécela solo si la persona acaba de instalarla o pregunta cómo usarla. Nunca en cada carrusel.
- Frases que abren la guía siempre: «ábreme la guía», «empieza la guía» (desde cero), «retoma la guía» (donde se quedó), «guía lección 2», «sal de la guía».

## Paso 0 · Revisa que esté todo listo (antes de la entrevista)

No des por hecho que la persona tiene lo mismo que tú. Antes de empezar, en silencio:
1. Comprueba que hay **Python 3** (`python3 --version`) y la librería **Pillow** (`python3 -c "import PIL"`).
2. Si estás en la app de Claude (con "Crear y editar archivos" encendido), ya vienen: sigue.
3. Si falta algo (por ejemplo en Claude Code): explícale en una frase qué es y para qué lo necesitas ("Pillow es la herramienta con la que dibujo las láminas"), **pídele permiso** y solo entonces instálalo (`pip install pillow` o `python3 -m pip install --user pillow`). Si no se puede instalar, dile exactamente qué hacer y no sigas a medias.
4. Si todo está bien, no digas nada de esto: ve directo a la entrevista.

## Paso 1 · La entrevista (SIEMPRE al empezar)

Pregunta en **rondas cortas, con opciones numeradas**, para que la persona conteste rápido (si tu entorno tiene una herramienta de preguntas con opciones, úsala). Siempre incluye "Decide tú" como opción. Si la persona ya contestó algo en su primer mensaje, no lo vuelvas a preguntar. Si dice "hazlo tú todo", salta a lo que falte con tu mejor criterio y dilo en una línea.

**Ronda 1 · El contenido**
1. **Tema o material:** ¿de qué es? (escribir el tema · pegar un texto · un link · un PDF o documento · "propónme 5 temas" para su negocio).
2. **Objetivo:** enseñar algo · vender un producto o servicio · construir marca personal · anunciar algo (lanzamiento, evento, oferta) · contar una historia.
3. **Para quién:** ¿quién lo va a leer? (clientes de un negocio local, emprendedores, estudiantes…). Con eso eliges el tono y los ejemplos.
4. **Cantidad:** un carrusel · una **serie de 5** para la semana (ver Paso 6).
5. **Formato:** Instagram (1080×1350, vertical 4:5) · TikTok en modo foto (1080×1920) · los dos.

**Ronda 2 · La marca**
6. **¿Ya tienes una marca?**
   - **Sí, te paso mis datos:** colores (códigos hex o una foto/captura de donde salen), tipografías (nombre o archivo .ttf/.otf), logo (PNG, mejor sin fondo) y @usuario.
   - **Sácala de lo que ya tengo:** link a su web o capturas de su Instagram. Obtén los colores dominantes, el estilo de letra más parecido entre las fuentes incluidas y el tono. Enséñale lo que encontraste para que lo confirme.
   - **Invéntamela:** propón **3 identidades** distintas (nombre de la paleta, 3 colores: fondo, tinta y acento, el estilo visual que mejor le queda y el tono de voz en una frase) y renderiza la portada en cada una para que elija viéndolas.
   - **Sin marca:** usa los colores por defecto del estilo.
7. **Tono de voz:** cercano · experto · divertido · directo y sin rodeos · inspirador.

**Ronda 3 · El diseño y la herramienta**
8. **Estilo visual** (enseña `estilos.jpg`): **Editorial** (serif elegante, papel, para marcas premium o de contenido serio) · **Minimal** (limpio, mucho aire, para tecnología y servicios) · **Bloque** (fondo oscuro y bloques de color, impactante, para jóvenes y ventas) · **Cuaderno** (letra a mano y puntos, cercano, para educación y tips) · Decide tú.
9. **¿Con qué lo hacemos?** Revisa antes qué conectores tiene activos la persona y ofrece **solo los que existen**:
   - **Claude solo (recomendado y gratis):** imágenes PNG listas para subir, con dibujos hechos a la medida.
   - **Canva** (si el conector de Canva está activo): el carrusel queda como diseño de Canva para editarlo ahí (ver "Ruta Canva").
   - **Adobe Express** (si su conector está activo): igual, editable en Express.
   - **PNG + Canva:** las dos cosas.
   - Si quiere Canva o Express pero no está conectado: explícale cómo activarlo (en claude.ai: Configuración → Conectores) y sigue con "Claude solo" mientras tanto.
10. **Imágenes:** dibujos hechos por Claude para cada slide (recomendado) · sus propias fotos (que las suba) · mezcla (fotos en la portada, dibujos en el resto) · solo texto.

Cierra la entrevista con un resumen de 4 o 5 líneas de lo decidido.

## Paso 2 · El texto de cada slide (y aprobación)

Escribe el guion y enséñalo como lista (slide por slide) **antes de diseñar**. Reglas:
- **Portada = gancho.** Promesa concreta o curiosidad: un número ("5 errores…"), un resultado ("Cómo… en 10 minutos"), una contradicción ("Deja de… si quieres…") o una pregunta que duela. Máximo 10 palabras en el título. El subtítulo da una razón para deslizar.
- **Una idea por slide.** Título de 3 a 7 palabras y texto de máximo 30 palabras. Si no cabe, son dos slides.
- **De 6 a 9 slides** en total: portada, de 4 a 7 de valor y cierre.
- **Énfasis:** pon entre `*asteriscos*` 1 o 2 palabras clave por título. El estilo decide cómo se marcan (cursiva de color, color, caja o marcatextos).
- **Datos solo con fuente.** Si hay una cifra, di de dónde sale (tipo de slide `dato` con `fuente`). Nunca inventes estadísticas ni testimonios.
- **El cierre resume la idea** y lleva un CTA que siempre aplique: "Guárdalo", "Compártelo con alguien que lo necesite", "Síguenos para más". No uses "comenta X y te lo mando", salvo que la persona tenga una respuesta automática que de verdad lo envíe.
- Mezcla tipos de slide para que no se sienta repetido.

Ajusta lo que pida y sigue. Si dijo "hazlo tú todo", enséñalo y continúa sin esperar.

## Paso 3 · Las ilustraciones (dibújalas tú, para este tema)

No hay una biblioteca para escoger: **en cada carrusel dibujas ilustraciones nuevas** que expliquen esa slide (una cafetera, un avión, una pesa, una tarjeta de crédito, una planta…). Se escriben como lista de figuras en `"dibujo": [...]`, en una caja de 0 a 100. Lee el formato en `scripts/iconos.py` y usa `EJEMPLOS` y `ejemplos/cafeteria.json` como referencia de nivel.
- Estilo de ilustración plana: de 5 a 15 figuras, contorno `tinta`, relleno con `acento` (lo importante), `claro` (zonas grandes) y `fondo` (brillos y detalles). Usa `curva` para formas orgánicas (gotas, hojas, nubes, siluetas).
- Que se entienda de un vistazo: el objeto principal grande y centrado, con 1 o 2 detalles que cuenten algo (vapor, brillo, signo de interrogación, chispas).
- Dónde va: en la `portada` ocupa la mitad de abajo; en `punto` va arriba a la derecha; en `lista` y `dato` arriba; en `cierre` es un símbolo simple (guardar, flecha, corazón).
- No en todas las slides: en la portada y en la mitad de las demás basta.
- Si la persona dio fotos, usa `"foto": "ruta.jpg"` en la portada (u otra slide) y omite ese dibujo.

## Paso 4 · Diseñar y revisar

1. Escribe el guion JSON (modelo: `ejemplos/cafeteria.json`). Campos:
   - `marca`: `nombre`, `usuario`, `colores` {`fondo`, `tinta`, `acento`}, `logo` (ruta, opcional), `fuentes` {`titulo`, `texto`} (rutas .ttf/.otf, opcional).
   - `plantilla`: `editorial` | `minimal` | `bloque` | `cuaderno`.
   - `formato`: `instagram` | `tiktok` | `ambos`.
   - `slides`: tipos `portada` (etiqueta, titulo, subtitulo, dibujo o foto) · `punto` (num, titulo, texto, dibujo) · `lista` (titulo, items, dibujo) · `dato` (cifra, texto, fuente, dibujo) · `cita` (texto, autor) · `antes_despues` (titulo, antes, despues, eti_antes, eti_despues) · `cierre` (titulo, cta, dibujo).
2. Corre `python3 scripts/carrusel.py guion.json salida/`. Sale un PNG por slide y `_revision.jpg` (todas juntas).
3. **Mira `_revision.jpg` y, si hace falta, cada PNG.** Revisa: texto cortado o encimado, dibujos que tapan texto, dibujos que no se entienden, contraste bajo, slides con demasiado texto o vacías, faltas de ortografía. Corrige el guion y vuelve a renderizar hasta que esté bien. Nunca entregues sin revisar.
4. En TikTok la interfaz tapa los lados (botones a la derecha, descripción abajo). El motor ya respeta esa zona; aun así revisa que nada importante quede abajo a la derecha.

## Paso 5 · Entregar

- Las imágenes en orden (`01.png`, `02.png`…; con `ambos`, carpetas `instagram/` y `tiktok/`). En claude.ai, ofrécelas como archivos descargables. En Claude Code, di la carpeta.
- **Descripción lista para pegar:** gancho en la primera línea (≤ 70 caracteres), 2 o 3 frases de valor, un CTA que aplique y de **3 a 6 hashtags** (mezcla de grandes y de nicho, en el idioma de la audiencia).
- **Texto alternativo** corto de la portada (accesibilidad).
- Ofrece ajustes concretos: "¿Cambio el gancho, el estilo o algún dibujo?".
- **Guarda la marca para la próxima vez:** en Claude Code, en `~/.carrusel-pro/marca.json` (y léelo al empezar: si existe, pregunta "¿Uso tu marca guardada?" en vez de la Ronda 2). En claude.ai, entrega el bloque JSON de la marca y sugiere pegarlo en las instrucciones de un Proyecto.

## Paso 6 · Serie de 5 carruseles

Si pidió una serie: propone 5 temas con ángulos distintos (un error común, un paso a paso, un mito contra la realidad, un antes y después, una lista de herramientas o recursos), con portada en una línea cada uno y el día sugerido. Al aprobarse, haz cada uno con la misma marca y estilo, con variedad de tipos de slide, y entrega un calendario simple (día, tema, descripción).

## Ruta Canva / Adobe Express (si eligió esa opción)

- Usa las herramientas del conector que estén disponibles (lístalas antes y elige las que sirvan: crear o generar diseño, subir imágenes, exportar).
- Pasa **el texto exacto aprobado de cada slide**, los colores en hex, las tipografías y el tamaño (1080×1350 o 1080×1920). Si el conector permite subir imágenes, sube tus PNG o los dibujos de cada slide para que queden en el diseño.
- Revisa el resultado con la vista previa del conector y compáralo con el guion aprobado (texto completo, orden, colores). Corrige lo que no cuadre.
- Entrega el link de edición y, si se puede, la exportación en PNG. Si el conector falla o no deja algo, dilo claro y entrega la versión de Claude como respaldo.

## Reglas de oro

- Nunca inventes datos, reseñas ni testimonios. Cifras, solo con fuente.
- No uses logos ni marcas de terceros sin que la persona lo pida y tenga derecho a usarlos.
- Nada de texto diminuto: si no se lee en el celular, sobra.
- La persona decide. Tú propones lo mejor y explicas en una línea por qué.
