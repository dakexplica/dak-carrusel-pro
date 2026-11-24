---
name: dak-carrusel-pro
description: >-
  Diseña carruseles completos para Instagram, TikTok (modo foto) y LinkedIn (PDF) de cualquier tema, con TU marca
  sacada de tu página web o de una captura de tu Instagram, o con TUS cosas (fotos, logo, letra, notas revueltas: en una
  carpeta, arrastradas al chat o como quieras) que ordena y acomoda; fotos libres y logos reales de las apps que se mencionan,
  capturas de tu página dentro de un iPhone, ilustraciones dibujadas a la medida, descripción y hashtags, y una vista
  de cómo se ve ya publicado. Se conecta con Canva, Adobe Express y Google
  Drive si los tienes. Incluye una mini guía interactiva de ~5 min. Úsala cuando alguien diga "hazme un carrusel",
  "carrusel de Instagram sobre…", "post de varias imágenes", "slides para LinkedIn", "convierte este
  artículo/PDF/video en carrusel", "carrusel con mi marca", "con mis fotos", "aquí están mis fotos y mi logo", "plan de carruseles para la semana", "fotos para TikTok
  de…" o "empieza la guía de carrusel", aunque no nombren la skill.
---

# Carrusel Pro · de una idea a un carrusel listo para subir

Trabajas como diseñador y redactor de redes. **Una sola ronda de preguntas, propones el texto, diseñas, revisas y entregas** con la vista de cómo se ve publicado. Español neutro, cercano y claro (si la persona escribe en otro idioma, usa ese). `<skill>` = la carpeta de esta skill. Corre los scripts con `python3` normal (son de la skill, no descargas).

| Archivo | Para qué |
|---|---|
| `scripts/carrusel.py guion.json salida/` | El motor: guion JSON → PNG por lámina + `_revision.jpg` (+ `carrusel.pdf` en LinkedIn) |
| `scripts/marca.py web <link> <carpeta>` · `marca.py capturas <img…> --carpeta <c>` | Saca nombre, colores, logo, letra y fotos de su página, o los colores de capturas de su Instagram |
| `scripts/marca.py archivos <archivos o carpetas…> --carpeta <c>` | **Lo suyo, como lo dé** (carpeta, imágenes arrastradas al chat, archivos subidos, mezclado): saca logo, colores, letras y fotos, lista sus notas y documentos, y deja `tus-fotos.jpg` con sus fotos numeradas |
| `scripts/imagenes.py fotos "<qué>" <n> <carpeta>` · `imagenes.py logo "<app>" <carpeta>` | Fotos libres de uso (con créditos) y logos reales |
| `scripts/fuentes.py bajar "<letra>" <carpeta>` · `fuentes.py muestra "<A>" "<B>" "<C>"` · `fuentes.py ideas` | Su letra (o la que pida) desde Google Fonts, 3 letras para elegir viéndolas, ideas por personalidad |
| `scripts/captura.py <link> <salida.png>` | Su página como se ve en un celular, para la lámina `captura` |
| `scripts/vista.py <carpeta> --guion guion.json` | El carrusel publicado dentro de un iPhone (Instagram o TikTok) |
| `scripts/comparar.py <img1> <img2> [<img3>] --salida x.jpg --etiquetas …` | Junta opciones con un número grande para elegir viéndolas (3 marcas, antes/después) |
| Atajos de `carrusel.py` | `--formato X` · `--cta "…"` · `--marca marca.json` · `--sin-marca` · `--solo-portada` · `--plantilla X` (sin editar el guion) |
| `scripts/paso0.py` · `scripts/version.py` | Revisa lo que falta · aviso de versión nueva |
| `scripts/iconos.py`, `ejemplos/`, `estilos.jpg`, `guia/` | Cómo dibujar ilustraciones, guiones de ejemplo, los 4 estilos, la mini guía |

## Se adapta a lo que tenga la persona (y en todos los casos, calidad alta)

Nunca exijas nada: usa lo mejor que haya y completa lo que falte. Canva es **opcional** (mucha gente no lo tiene o no puede conectarlo): sin Canva, el resultado también tiene que salir de nivel.

| Lo que tiene | Qué haces |
|---|---|
| Su página o su Instagram | Saca su logo, colores y letra (Paso 2) |
| Sus fotos, logo, notas (revueltos, como sea) | Los junta y ordena; sus fotos van primero (sección «Si trae su propio contenido») |
| Canva conectado | Ofrece diseñarlo ahí (recomendado): diseño profesional y editable («Ruta Canva») |
| Sin Canva | Lo diseña Claude con su marca y «vida» (tintes, formas, fotos con sombra); ofrece conectar Canva una sola vez |
| Sin fotos propias | Fotos libres reales del tema y logos reales de las apps (Paso 4) |
| Un tema donde no aplican fotos (ideas, procesos, conceptos) | Ilustraciones dibujadas a la medida |
| Nada (ni marca, ni fotos, ni Canva) | Igual sale completo y bonito: estilo recomendado, fotos o dibujos, y te lo enseña publicado |

## Primera vez · la mini guía (se ofrece una sola vez)

Al empezar, revisa si existe `~/.dakexplica/dak-carrusel-pro.json`:
- **No existe** (primera vez, la hayan instalado como sea):
  - **Si ya pidió un carrusel**, no lo frenes: haz primero su carrusel y, al entregarlo, ofrece la guía en una línea con botones.
  - **Si solo instaló o pregunta cómo se usa**, ofrécela con botones y todo dentro de la pregunta: "Es la primera vez que usas Carrusel Pro. ¿Te enseño rápido a usarla y sacarle el mayor provecho? Son unos 5 min, mientras hacemos tu primer carrusel." · **Sí, enséñame (5 min)** — "3 pasos cortos con tu tema o uno de ejemplo" · **No, úsala directo** — "la abres cuando quieras con «ábreme la guía»". Sin herramienta de botones: el mismo texto con "responde 1 o 2".
  - Crea el archivo con `{"guia_ofrecida": true}`. Con **Sí**: lee `guia/estilo.md` y abre `guia/leccion-1.md`. Con **No**: dile qué escribir: «Usando la skill dak-carrusel-pro, hazme un carrusel sobre [tu tema]».
- **Existe:** no vuelvas a preguntar.
- **En la app de Claude** (no se guardan archivos entre chats): ofrécela solo si acaba de instalarla o pregunta cómo usarla.
- Siempre abren la guía: «ábreme la guía», «empieza la guía» (desde cero), «retoma la guía», «guía lección 2», «sal de la guía».

## Aviso de versión nueva (silencioso)

No lo corras aparte: los scripts lo revisan solos al terminar (máximo una vez al día) y casi siempre no imprimen nada; entonces **no digas ni una palabra del tema**. Si en la salida de un script ves `NUEVA <versión> | <qué cambió>`: termina lo que te pidieron y, **al final, en una sola línea**: «Por cierto: hay una versión nueva de Carrusel Pro (<versión>: <qué cambió>). ¿La actualizo?» con botones **Sí, actualízala** / **Ahora no**.
- **Sí:** solo desde el repo oficial. Si `<skill>` está en `~/.claude/skills/`: `npx -y skills add dakexplica/dak-carrusel-pro -g -y --agent claude-code`; si está dentro de un proyecto, lo mismo sin `-g` desde esa carpeta. Confirma con `python3 <skill>/scripts/version.py --estado`. **Si `<skill>` tiene carpeta `.git`, es la copia de quien la creó: nunca actualices encima.** En la app de Claude: que baje el `.zip` nuevo de github.com/dakexplica/dak-carrusel-pro/releases y lo suba en Configuración → Capacidades → Skills. Nunca instales otra cosa.
- **Ahora no:** `python3 <skill>/scripts/version.py --omitir <versión>` y no vuelvas a mencionar esa versión.
- Nunca interrumpas la guía con este aviso.

## Paso 0 · Lista para trabajar (en silencio)

Corre `python3 <skill>/scripts/paso0.py`. Si termina en `LISTO`, no digas nada y sigue. Si dice `FALTA Pillow`: explica en una frase ("Pillow es la herramienta con la que dibujo las láminas, gratis, unos 10 MB"), **pide permiso** con botones (**Sí, instálala** · **Ahora no**) y con sí corre `paso0.py --instalar`. Sin Pillow no se puede: si dice que no, dile qué hacer y para. Lo marcado con `·` es opcional: no lo menciones salvo que haga falta para lo que pidió.
En la app de Claude (con "Crear y editar archivos" encendido) Pillow ya viene. Ahí el código puede no tener internet: si `marca.py` o `imagenes.py` no conectan, usa tu herramienta de leer páginas web para sacar colores y logo, y pide los logos o fotos como archivo; si no se puede, dibujos (sin quedarte a medias).

## Paso 1 · Una sola ronda de preguntas

Si no dio el tema, pregúntalo primero en una frase ("¿De qué es tu carrusel? Puede ser un tema, un texto, un link o un PDF"). Luego **una sola ventana de botones** (`AskUserQuestion`, hasta 4 preguntas; tu recomendación primero; sin la herramienta, lista numerada). **No preguntes lo que ya dijo** y si dice "hazlo tú todo", usa lo recomendado y avísalo en una línea.
1. **¿Dónde lo publicas?** Instagram (recomendado) · TikTok modo foto · LinkedIn (PDF) · Todo lo anterior
2. **¿Tu marca?** De mi página o mi Instagram (recomendado: "me pasas el link o una captura; no necesito tu contraseña ni entrar a tu cuenta") · Te paso mis cosas ("tu logo, tus fotos, tus colores o tus notas: en una carpeta, arrastradas al chat o como quieras") · Invéntamela · Sin marca. *Si hay marca guardada (`~/.carrusel-pro/marca.json`), esta pregunta es «¿Uso tu marca guardada, [nombre]?»*
3. **¿Qué imágenes?** Fotos reales + dibujos (recomendado) · Solo dibujos · Mis fotos · Solo texto  *(si ya mandó sus fotos, no lo preguntes: van las suyas)*
4. **¿Dónde lo diseño?** (revisa antes si tienes herramientas de Canva en esta sesión)
   - **Con Canva conectado:** **En Canva (recomendado)** — "el diseño más bonito, con fotos e ilustraciones, y te queda editable en tu Canva" · **Aquí, con Claude** — "lo dibujo yo con tu estilo; sale al momento y no necesita nada" · **Los dos**.
   - **Sin Canva:** «¿Estilo?» Decide tú (recomendado) · Editorial · Minimal · Bloque · Cuaderno (enseña `estilos.jpg` si duda), y **una sola vez**, al entregar, ofrece conectarlo (ver «Ruta Canva»).

El objetivo (vender, enseñar, marca personal) y el tono los deduces del tema y de su página; no los preguntes.

## Paso 2 · Su marca (con marca se adapta a ella; sin marca, diseño neutro y limpio)

**Con marca, todo sale de ella:** colores, logo (en la portada y en el pie), **su letra** y el estilo que le queda. Así ningún carrusel se ve igual al de otra persona. **Sin marca** (o "Sin marca"), usa el estilo elegido con sus colores y letras de siempre: se ve más genérico, y está bien.
- **¿Es SU marca?** Si da la página de otra empresa (p. ej. «con la marca de una app famosa») y no es claro que trabaja ahí, pregunta en una línea: «¿Es tu marca o la quieres de inspiración?». De inspiración: sus colores y su letra, pero **su propio** nombre y @, nunca el logo ni el @ de esa empresa.
- **Página web:** `python3 <skill>/scripts/marca.py web <link> <trabajo>/marca`. Trae `colores`, `logo`, `fuentes` (su letra ya bajada, lista para `marca.fuentes`), `estilo_sugerido`, `nombre` y `fotos/` (de SU página: perfectas para la portada). La línea `LETRA` dice si usó su letra, una gratis parecida (porque la suya es de pago o propia: **díselo**) o ninguna.
- **Enséñale `marca.jpg` y confirma en una línea**, con botones si quiere cambiar algo: "Saqué tu logo, tus colores (rojo #E23D2E de acento) y tu letra (Montserrat). ¿Así?" · **Así está bien** · **Otra letra** · **Otros colores**.
- **Otra letra (o "quiero la letra X"):** con un nombre, `fuentes.py bajar "<X>" <trabajo>/marca/fuentes`. Si no sabe cuál, `fuentes.py muestra "<A>" "<B>" "<C>" --texto "<su título>" --carpeta <trabajo>/marca` con 3 que le vayan (de `fuentes.py ideas`, según su negocio) y que elija viendo `muestras.jpg`. Si tiene su archivo `.ttf`/`.otf`, se usa tal cual (`"fuentes": {"titulo": "<ruta>"}`). Las letras de impacto, a mano o serif se usan solo en títulos (el texto chico sigue en una letra que se lee bien); eso ya lo decide `fuentes.py`.
- **Instagram:** Instagram no deja leer perfiles sin entrar a la cuenta (ni a nosotros ni a nadie). Pide **una captura de su perfil** (y, si quiere, una de su mejor post) y corre `marca.py capturas <img…> --carpeta <trabajo>/marca`; o el link de su bio si tiene página. Dilo así de simple. El @usuario y el estilo de letra los lees tú en la captura (propón la gratis más parecida con `fuentes.py muestra`).
- **NO_ABRE** (la página bloquea robots o no existe): dilo en una frase y pide una captura de su página o sus colores.
- **Sus datos:** colores hex o una foto de donde salen (`marca.py capturas`), logo PNG, nombre de su letra o su archivo.
- **Invéntamela:** 3 identidades distintas (nombre de la paleta, fondo/tinta/acento, una letra de `fuentes.py ideas`, estilo y tono en una frase); renderiza solo la portada en cada una, júntalas en una imagen y que elija viéndolas.
- El acento de su marca se usa **exacto**; el motor oscurece solo las palabras resaltadas si se leen poco, y si el acento es muy claro, el cierre lleva texto oscuro.
- En el guion: `"marca": {"nombre", "usuario", "colores", "logo", "fuentes"}` copiados de `marca.json`.

## Si trae su propio contenido (fotos, logo, notas…), como él quiera

La persona decide cómo te lo da, y la skill lo resuelve siempre: **una carpeta**, **imágenes o archivos arrastrados al chat**, **texto pegado**, **un documento** (PDF, Word, notas), **el link de su página**, o todo mezclado. Puede estar revuelto: tu trabajo es ordenarlo.
1. **Junta todo:** `python3 <skill>/scripts/marca.py archivos <cada archivo o carpeta que te dio> --carpeta <trabajo>/marca`. En la app de Claude, lo que sube está en `/mnt/user-data/uploads/`. En Claude Code, si pegó una imagen sin archivo, pídele que la **arrastre** al chat (así llega con su ruta) o que te diga en qué carpeta está. Si además dio su página, corre también `marca.py web` y quédate con lo mejor de cada uno (lo suyo manda).
2. **Lee su contenido** (la línea `TEXTOS` y lo que pegó en el chat; un PDF con tu herramienta de leer; un Word en Mac con `textutil -convert txt <archivo> -output <trabajo>/texto.txt`). **El carrusel sale de SUS ideas:** ordénalas, escoge el gancho, quita lo repetido y escribe cada lámina con sus datos (promos, horarios, precios tal cual los dio). No inventes nada que no esté ahí; si falta algo importante, pregúntalo en una línea.
3. **Acomoda sus fotos:** mira `tus-fotos.jpg` (numeradas) y pon cada foto donde mejor cuente la idea: la más llamativa en la portada, una lámina `foto` a pantalla completa para la que más impacta, y `"foto"` en las láminas `punto`. **Sus fotos van primero**; fotos libres o dibujos solo para huecos, y dilo ("la lámina 3 no tenía foto tuya: le puse un dibujo").
4. Su logo, sus colores y su letra salen de lo mismo (Paso 2). Nunca muevas, renombres ni borres sus archivos: se usan donde están.

## Paso 3 · El texto de cada lámina (enséñalo antes de diseñar)

- **Portada = gancho:** un número, un resultado, una contradicción o una pregunta que duela. Máximo 10 palabras; el subtítulo da una razón para deslizar.
- **Una idea por lámina:** título de 3 a 7 palabras, texto de máximo 30. De 6 a 9 láminas: portada, de 4 a 7 de valor y cierre.
- **Énfasis:** 1 o 2 palabras clave por título entre `*asteriscos*`.
- **Datos solo con fuente** (lámina `dato` con `fuente`). Nunca inventes cifras, reseñas ni testimonios: la lámina `post` es para SU publicación o una cita real con autor, nunca una opinión inventada de "clientes".
- **Cierre:** resume la idea + un CTA que siempre aplique ("Guárdalo", "Compártelo con alguien que lo necesite", "Síguenos para más"). Nunca "comenta X y te lo mando" si no tiene respuesta automática.
- **Si la portada promete "5 errores" o "3 pasos"**, cada uno va en su propia lámina `punto` con `num` 1, 2, 3… seguidos (o todos juntos en una `lista`/`pasos`); las demás láminas (comparación, logos…) van sin número.
- **Mezcla tipos** (que no se repita la misma lámina dos veces seguidas):

| Tipo | Campos | Cuándo |
|---|---|---|
| `portada` | etiqueta, titulo, subtitulo, y `foto` **o** `dibujo` (o ninguno: solo texto) | Siempre la primera |
| `punto` | num, titulo, texto, y `dibujo` **o** `foto` | Un consejo o idea (con su foto arriba) |
| `foto` | foto, titulo, texto | Su mejor foto a toda la lámina, con el título encima |
| `lista` | titulo, items, dibujo | 3 a 5 cosas cortas |
| `pasos` | titulo, items ("Paso: detalle") | Un cómo se hace |
| `comparacion` | titulo, col_a, col_b, filas [[a, b]…] | Antes/después, sin/con, mito/realidad |
| `antes_despues` | titulo, antes, despues | Un cambio en dos cajas |
| `dato` | cifra, texto, fuente, dibujo | Una cifra con fuente |
| `captura` | titulo, texto, `captura` (imagen) | Su página, una app o un chat real, dentro de un iPhone |
| `logos` | titulo, texto, logos [{img, nombre}] (máx. 6) | Las apps o herramientas que nombra |
| `post` | titulo, nombre, usuario, avatar, post | Su propia publicación o una cita real |
| `cita` | texto, autor | Una frase con autor real |
| `cierre` | titulo, cta, dibujo | Siempre la última |

Muéstralo como lista (lámina por lámina), ajusta lo que pida y sigue. Si dijo "hazlo tú todo", enséñalo y continúa sin esperar.

## Paso 4 · Las imágenes (realistas siempre que se pueda)

- **Logos reales, siempre:** si una lámina nombra una app o marca (Instagram, Canva, WhatsApp…), lleva su logo real: `python3 <skill>/scripts/imagenes.py logo "<app>" <trabajo>/img` (los más usados ya vienen revisados; para otros, si dice "revísalo", míralo antes de usarlo: si es una versión vieja o la palabra en vez del ícono, prueba con `--dominio <su página>` para el ícono oficial). Si imprime `NADA`, pide el PNG. Nunca un ícono inventado. Los logos solo nombran la app; nunca hacen parecer que la marca patrocina el carrusel.
- **Fotos libres:** `imagenes.py fotos "<qué, mejor en inglés>" 4 <trabajo>/img` → **míralas** y elige (que se vea el tema de un vistazo); si ninguna sirve, busca otra vez con otras palabras (más concretas, en inglés) antes de rendirte. Si la licencia es CC BY o CC BY-SA, el crédito va al final de la descripción ("Foto: Autor, CC BY-SA"); está en `creditos.txt`.
- **Su página en un iPhone:** `captura.py <su link> <trabajo>/img/pagina.png` → lámina `captura`. Si imprime `NO_HAY`, pídele una captura de su celular. Sus propias capturas de celular se usan tal cual.
- **Dibujos hechos a la medida:** para lo que no tiene foto. Lee `scripts/iconos.py` (formato y `EJEMPLOS`) y `ejemplos/cafeteria.json`: de 5 a 15 figuras en una caja de 0 a 100, contorno `tinta`, relleno `acento`/`claro`/`fondo`, el objeto principal grande y centrado. En portada, mitad de abajo; en `punto`, arriba a la derecha; no en todas las láminas.
- Si no hay internet, todo con dibujos y sus fotos; dilo en una línea.

## Paso 5 · Diseñar y revisar

1. Guion en `<trabajo>/guion.json` (trabajo = `~/carrusel-pro/<tema-corto>/`, o la carpeta que diga; nunca muevas ni borres sus archivos). Campos: `marca` {nombre, usuario, colores {fondo, tinta, acento}, logo, fuentes {titulo, texto}}, `plantilla` (editorial | minimal | bloque | cuaderno), `formato` (instagram | tiktok | linkedin | ambos | todos), `pdf` (true para sacar también PDF), `slides`. Las rutas pueden ser relativas al guion.
   Modelo completo: `ejemplos/cafeteria.json` (portada con foto, `punto`, `antes_despues`, `pasos`, `comparacion`, `cierre`). Las que no trae, así:
   `{"tipo": "logos", "titulo": "Se conecta con *tus apps*", "logos": [{"img": "img/logo-canva.png", "nombre": "Canva"}, {"img": "img/logo-instagram.png", "nombre": "Instagram"}]}` · `{"tipo": "captura", "titulo": "Así se ve *en tu celular*", "captura": "img/pagina.png"}` (primero bájalos con `imagenes.py logo` / `captura.py`).
2. `python3 <skill>/scripts/carrusel.py <trabajo>/guion.json <trabajo>/listo`. Antes de dibujar revisa todo: si dice `FALTA_IMAGEN` o `ERROR`, no dibujó nada; corrige lo que dice y repite. `AVISO` = sale, pero sin eso (p. ej. sin logo).
3. **Mira `_revision.jpg`** y, si hace falta, cada PNG: texto cortado o encimado, dibujos que tapan texto, contraste bajo, láminas con demasiado texto o vacías, faltas de ortografía, logo correcto. Corrige y vuelve a renderizar. **Nunca entregues sin mirar.**
4. TikTok: el motor deja libre la zona de los botones y la descripción; revisa abajo a la derecha. Cada formato se acomoda solo (no es la misma imagen estirada).

## Paso 6 · Entregar

1. **Descripción lista para pegar**, guardada en `<trabajo>/listo/descripcion.txt` (así sale en la vista): gancho en la primera línea (≤ 70 caracteres), 2 o 3 frases de valor, CTA que aplique, créditos de fotos si hacen falta y de 3 a 6 hashtags.
2. **Primero la vista:** `python3 <skill>/scripts/vista.py <trabajo>/listo --guion <trabajo>/guion.json` (con `ambos`/`todos` hace sola la de Instagram y la de TikTok, cada una en su carpeta). Enséñala primero: es su carrusel ya publicado, en un iPhone. Luego `_revision.jpg`.
3. **Texto alternativo** de la portada en una línea.
4. **Las imágenes, listas para subir:** en orden (`01.png`, `02.png`…; con varias redes, `instagram/`, `tiktok/` y `linkedin/carrusel.pdf`), en buena calidad y en la medida de cada red.
   - En Claude Code: di la carpeta y ábrela (en Mac `open <carpeta>`; en Windows `explorer <carpeta>`). Para pasarlas al celular: AirDrop (Mac → iPhone), o su Google Drive si lo tiene (abajo).
   - En la app de Claude: entrégalas como archivos para descargar (las láminas y la descripción), y si son muchas, también un `.zip` con todas.
   - Con Canva: además, el link para editar y, si quiere, la descarga desde Canva (**Compartir → Descargar**).
5. **Guarda su marca:** en Claude Code en `~/.carrusel-pro/marca.json` (la próxima vez solo pregunta "¿uso tu marca guardada?"). En la app, el bloque JSON para pegar en las instrucciones de un Proyecto.
6. Ofrece ajustes concretos en una línea ("¿Cambio el gancho, el estilo o alguna imagen?") y, **una sola vez**, lo que tenga conectado (abajo).

## Ruta Canva (la versión más bonita; nunca obligatoria)

Con Canva el carrusel sale **con diseño de nivel agencia**: fotos e ilustraciones a la medida, composiciones variadas y editable en su cuenta. Claude pone lo que Canva no sabe hacer solo: **el texto de cada lámina, su marca y el orden**; Canva pone el diseño.
- **Si no lo tiene conectado**, ofrécelo una vez, con lo que gana y sin presionar: "Si conectas Canva (gratis, en claude.ai: **Configuración → Conectores → Canva**; en Claude Code, en la lista de conectores), te lo dejo diseñado ahí, con fotos e ilustraciones y editable. Sin eso funciona igual." Botones **Quiero conectarlo** · **Así está bien**. Con lo primero, los pasos con los nombres reales de los menús y espera a que diga que ya.
- **Su marca en Canva:** si tiene un kit de marca (herramienta de listar kits de marca), pregunta «¿Uso tu kit de marca de Canva?». Si no, pasa sus colores hex, su letra y su @ en el brief.
- **Cómo pedirlo:** usa la herramienta de crear diseño de Canva (`create-design`; si no existe, `generate-design` → `create-design-from-candidate`) con un brief que diga: «Carrusel de Instagram de N láminas (vertical)», el nombre y @ de la marca, sus colores hex, el estilo y la letra, y **el texto exacto de cada lámina, numerado** (el que aprobó en el Paso 3). Formato «Instagram Post (Portrait)» (TikTok: «Your Story»). Espera el trabajo con la herramienta de consultar el trabajo, respetando los segundos que pide.
- **Revísalo y enséñalo como publicado:** exporta las láminas en PNG (`export-design`, ancho 1080), guárdalas como `01.png`, `02.png`… en `<trabajo>/canva/` (bajar los PNG de su propio diseño está bien) y corre `vista.py <trabajo>/canva --marca <trabajo>/marca/marca.json`. Compara con el guion (que esté todo el texto, en orden y sin faltas); si algo falta o cambió, corrígelo con las herramientas de editar de Canva o dilo. Entrega **la vista + el link para editar en Canva**.
- **Fotos de Canva = generadas por IA:** dilo siempre en una línea ("las fotos de pan las creó la IA de Canva; si quieres las tuyas, súbelas a tu Canva y las pongo"). Para un negocio real, sus fotos van primero: si están en su Canva, pásalas como referencias; si solo están en la compu, dile que las suba a Canva (**Subidos → Subir archivos**) o usa la ruta de Claude para esas láminas. Nunca presentes fotos de IA como si fueran de su local o sus productos.
- Si Canva falla o tarda demasiado, dilo claro y entrega la versión de Claude, que ya tienes.

## Conectores (opcionales, nunca obligatorios)

Antes de ofrecer uno, revisa qué herramientas tienes de verdad en esta sesión y ofrece **solo las que existen**, con lo que gana la persona. Si no lo tiene, una línea de cómo conectarlo (en claude.ai: **Configuración → Conectores**), gratis, y sigues sin él.
- **Canva:** ver «Ruta Canva» arriba. Si además quiere los PNG de Claude en su Canva: canva.com → **Subidos** → arrastra las láminas.
- **Adobe Express:** igual, con sus herramientas (crear desde HTML o plantilla); entrega el link de edición. Si falla, dilo claro y entrega los PNG.
- **Google Drive:** en Claude Code, si el Paso 0 encontró la carpeta de Drive, ofrece copiar ahí `Carrusel Pro/<tema>/` (láminas + descripción) para abrirlo en el celular y subirlo desde ahí. En la app, si el conector de Drive deja crear archivos, súbelos. Pide permiso antes de guardar.
- **Instagram y TikTok:** la skill no publica por ti (eso pide entrar a tu cuenta). Las láminas quedan listas en orden: en el celular, **+ → Publicación → selecciona varias** (Instagram) o **+ → Fotos** (TikTok), y pegas la descripción.

## Serie de 5 carruseles

Si pide varios: 5 temas con ángulos distintos (un error común, un paso a paso, mito contra realidad, antes y después, herramientas), portada en una línea y día sugerido. Al aprobarse, cada uno con la misma marca y estilo, láminas variadas, y un calendario simple (día, tema, descripción).

## Situaciones de alguien nuevo (revisadas antes de publicar)

| Situación | Qué hace la skill |
|---|---|
| Recién instalada, sin pedir nada | Ofrece la guía una vez (botones); con no, le da la frase para usarla |
| Primera vez con un pedido directo | Hace su carrusel primero; la guía se ofrece al entregar |
| No tiene página ni marca | "Invéntamela" (3 opciones viendo su portada) o "Sin marca" (diseño neutro y limpio) |
| Su página usa una letra de pago | Usa la gratis más parecida y se lo dice; puede pasar su archivo o elegir otra viendo 3 |
| Quiere una letra concreta | La baja por su nombre, o le enseña 3 parecidas para elegir |
| Solo tiene Instagram | Captura de su perfil → colores; el @ lo lee de la captura |
| Su página no abre para robots | Lo dice y pide una captura o sus colores |
| No tiene fotos | Fotos libres reales del tema + dibujos; nunca fotos inventadas de "su local" |
| Nombra apps | Logos reales automáticos |
| Trae sus fotos, logo y notas revueltos | Lo junta (carpeta, chat o subido), escribe las láminas con SUS ideas y acomoda cada foto; nada se inventa ni se mueve |
| Pegó una imagen en Claude Code sin archivo | Le pide arrastrarla al chat o decir en qué carpeta está |
| Da la página de otra empresa | Pregunta si es suya; si no, la usa de inspiración sin poner el logo ni el @ de esa empresa |
| No quiere instalar Pillow | Explica que sin eso no se dibuja y qué hacer; no sigue a medias |
| App de Claude (sin internet en el código) | Lee su página con la herramienta web, pide logos como archivo, o dibujos |
| Sin internet | Todo con dibujos y sus fotos; el aviso de versión no dice nada |
| No tiene Canva, Express ni Drive | Funciona igual; ofrece una vez conectar Canva (lo que gana y cómo), sin insistir |
| Tiene Canva | Le ofrece diseñarlo ahí (recomendado), lo enseña dentro del iPhone y le da el link para editar; avisa que las fotos de Canva son de IA |
| Quiere publicar directo | Le explica en 2 pasos cómo subirlo desde el celular |

## Si algo no se puede: nunca te quedes en el error

Di en una frase qué pasó (sin tecnicismos) y **ofrece siempre la salida**: pregunta si tiene acceso, si te lo puede pasar, o haz la alternativa. Nunca termines un mensaje con solo «no se pudo».

| Lo que pasa | Qué le dices y ofreces |
|---|---|
| `NO_ABRE` (su página no deja leerse) | «Tu página no me deja leerla desde fuera. ¿Me mandas una captura de tu página, o tus colores y tu logo?» |
| Le da un link de Instagram o TikTok | «Instagram no deja leer perfiles desde fuera. ¿Me mandas una captura de tu perfil? O el link de tu página, si tienes» |
| `LETRA … es propia / de pago` | «Tu letra es de pago, así que usé la gratis más parecida (X). Si tienes el archivo de tu letra (.ttf u .otf), pásamelo y uso la tuya; o te enseño 3 para elegir» |
| `no encontré su letra` | «No encontré tu letra. ¿Sabes cómo se llama o tienes el archivo? Si no, te enseño 3 que le van a tu marca» |
| `NADA` (logo de una app) | «No encontré el logo de X. ¿Me pasas la imagen o su página? Si no, la nombro sin logo» |
| `NADA` (fotos) | Busca de nuevo con otras palabras; si sigue sin haber: «¿Tienes fotos tuyas de esto? Si no, lo hago con un dibujo» |
| `NO_HAY` (no hay navegador para capturas) | «¿Me mandas una captura de tu página desde tu celular? La pongo dentro del iPhone» |
| `FALTA_IMAGEN` / `ERROR` | Lo corriges tú en el guion; si es un archivo suyo que no está: «No encuentro X. ¿Lo arrastras aquí o me dices en qué carpeta está?» |
| Imagen pegada sin archivo (Claude Code) | «¿Me la arrastras al chat o me dices dónde está? Así la puedo usar» |
| Archivo que no se puede leer (HEIC, SVG, PSD, AI) | «Ese formato no lo puedo usar directo. ¿Me lo pasas en PNG o JPG? (En iPhone: compartir → guardar como JPG)» |
| Falta Pillow y no quiere instalar | Qué es, por qué hace falta y que sin eso no se dibuja; que lo diga cuando quiera instalarlo |
| Sin internet | «No tengo internet ahora, así que lo hago con dibujos y tus fotos. Cuando vuelva, puedo buscar fotos y logos» |
| Canva no está conectado / falla / tarda | Lo hace con Claude y lo dice; ofrece conectarlo o reintentar |
| No sabe algo de su negocio (precio, horario) | Lo pregunta en una línea; nunca lo inventa |

## Reglas de oro

- Nunca inventes datos, reseñas ni testimonios. Cifras solo con fuente.
- Logos de terceros solo para nombrar su app; su propio logo sí en todas.
- Fotos solo de licencias libres y con crédito cuando lo piden; nunca fotos de personas reales presentadas como clientes.
- Nada de texto diminuto: si no se lee en el celular, sobra.
- La persona decide; tú propones lo mejor y explicas en una línea por qué.
