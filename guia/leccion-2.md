# Lección 2 · Con tu marca (~2 min)

> Guion para Claude. Lee `guia/estilo.md`. Retoma lo que te dijo en el paso 1 (`tema`, `destino`, `objetivo`). Aquí no hay botones al abrir: el mensaje cierra el turno con opciones numeradas (en la app, el texto antes de unos botones no se lee).

## 1 · Apertura (mensaje propio, cierra el turno)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  CARRUSEL PRO
  ▰▰▱  Paso 2 de 3 · Con tu marca
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

"Tu carrusel ya funciona. Ahora que se vea **tuyo**: que alguien lo vea en el feed y sepa que es de [su negocio / ti] sin leer el nombre. Eso es lo que hace que [objetivo: te escriban / te recuerden / te sigan]."

"¿De dónde saco tu marca? Nunca necesito tu contraseña ni entrar a tu cuenta:"
1. **De mi página web** — me pasas el link y saco tu logo, tus colores, tu letra y hasta fotos tuyas
2. **De mi Instagram** — me mandas una captura de tu perfil y saco tus colores (Instagram no deja leer perfiles desde fuera)
3. **Invéntame una** — te propongo 3 marcas y eliges viéndolas
4. **Te paso mis colores y mi logo** — o una foto de donde salen

"Responde 1, 2, 3 o 4 (y si es la 1, pega tu link de una vez)." **ALTO.**

## 2 · Su marca, en su carrusel

Si eligió 2 o 4 y no mandó lo que hace falta, pídelo una sola vez (la captura se arrastra al chat; rutas de ejemplo genéricas `/Users/tu-nombre/Desktop/perfil.png`). **ALTO.**

**Aviso (una línea):** "Saco tu marca y vuelvo a dibujar tu carrusel con ella. Menos de un minuto."

**ACCIÓN, en silencio** (`<guion>` = el guion del paso 1; con el ejemplo, `<skill>/ejemplos/cafeteria.json`; agrega siempre `--formato` y `--cta` del paso 1):
- **1 o 2:** Paso 2 del SKILL.md (`marca.py web` o `marca.py capturas`) → `<trabajo>/marca/marca.json`. Si sacó fotos de su página, ponle la primera a la portada.
- **4:** arma tú `<trabajo>/marca/marca.json` con sus colores, logo y letra (si da el nombre de una letra: `fuentes.py bajar`).
- **3 · Invéntame una:** 3 identidades distintas, **cada una con nombre y @ inventados** que le queden a su tema (p. ej. «Café Brasa · @cafebrasa»), su paleta y una letra de `fuentes.py ideas`. Escribe 3 `marca.json` (`<trabajo>/marca-1/`, `-2/`, `-3/`), dibuja solo la portada de cada una (`carrusel.py <guion> <trabajo>/opcion-1 --marca <trabajo>/marca-1/marca.json --solo-portada`) y júntalas: `comparar.py <…>/opcion-1/01.png <…>/opcion-2/01.png <…>/opcion-3/01.png --salida <trabajo>/3-marcas.jpg --etiquetas "<nombre 1>" "<nombre 2>" "<nombre 3>"`.
- **El antes y después** (1, 2 y 4): `carrusel.py <guion> <trabajo>/antes --sin-marca --solo-portada`, todo el carrusel con su marca (`carrusel.py <guion> <trabajo>/listo --marca <trabajo>/marca/marca.json`), y `comparar.py <trabajo>/antes/01.png <trabajo>/listo/01.png --salida <trabajo>/antes-despues.jpg --etiquetas "Sin marca" "Con tu marca"`. Saca la vista nueva (`vista.py <trabajo>/listo --guion <guion> --marca <trabajo>/marca/marca.json`). **Mira todo** antes de enseñarlo.

**MENSAJE obligatorio (cierra el turno):**
- **1, 2 o 4:** `marca.jpg` (lo que saqué: logo, colores y **su letra, por su nombre**; si es una parecida porque la suya es de pago, dilo), `antes-despues.jpg` y la vista nueva. Una línea sobre su objetivo ("Con tu logo arriba, quien lo vea ya sabe a quién escribirle").
- **3:** `3-marcas.jpg` y en una línea qué tiene cada una ("1 · Café Brasa: cálida y artesanal · 2 · …").
- Cierra con **una sola lista** (así se piden cambios, nada más fácil):
  - Con su marca: "¿Cómo lo dejamos? 1 · Así está perfecto · 2 · Un gancho más fuerte · 3 · Otra letra o estilo · 4 · Otra imagen. Responde con el número."
  - Con 3 opciones: "¿Cuál te gusta? Responde 1, 2 o 3."

**ALTO.**
- **Eligió una de las 3:** dibuja todo el carrusel con esa marca (`--marca <trabajo>/marca-N/marca.json`), saca la vista (`vista.py … --marca <trabajo>/marca-N/marca.json`) y enséñala en un mensaje con la misma lista de cambios (1 · Así está perfecto…). **ALTO.**
- **Pidió un cambio (2, 3 o 4):** hazlo (con «otra letra»: `fuentes.py muestra` con 3 que le van y que elija con el número), dibuja, míralo y enséñalo en un mensaje con una línea de qué cambió y la misma lista. **ALTO.**
- **Así está perfecto:** sigue al cierre.

**Cierre (en el mensaje del «así está perfecto»):** **Lo que lograste** (3 viñetas) y "En el último paso lo dejamos listo para subir en todas tus redes, con la descripción. Escríbeme «sigue»." **ALTO.** Guarda `"leccion": 3`.
