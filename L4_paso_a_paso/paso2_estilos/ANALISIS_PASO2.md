# Paso 2 — Comparativa de estilos visuales (Ejercicio 6.2): evidencia y análisis

Equipo A · IHC 2026-2 · 16 de octubre de 2026

Archivo analizado: `insumos/ejercicio_6_2_comparativa_estilos.html` (sin modificar).
Script reproducible: `build/paso2/analizar_6_2.py` (Playwright + Google Chrome 155.0.8059.84 + axe-core 4.10.2).
Datos: `resultado_analisis_6_2.json` y `contraste_wcag_6_2.csv`.

## 1. Evidencia de la realización

| Captura | Qué muestra |
|---|---|
| `capturas/01_vista_inicial.png`, `02_pagina_completa.png` | Las 3 columnas con los mismos 4 componentes, la tabla y el panel de métricas |
| `capturas/03_componente_{boton,toggle,slider,tarjeta}.png` | Cada componente aislado con el selector superior |
| `capturas/04_toggles_activados_sliders_80.png` | Los tres toggles encendidos y los sliders en 80 |
| `capturas/05_boton_presionado_{skeu,flat,neu}.png` | Retroalimentación del estado presionado (`:active`) |
| `capturas/06_tabla_10_criterios.png` | Tabla comparativa de 10 criterios |
| `capturas/07_panel_metricas.png` | Panel después de interactuar: 17 clics, 4 interacciones por estilo |
| `capturas/08_movil.png` | Vista móvil (390 px): las columnas se apilan |
| `capturas/09_firefox.png` | Firefox 137: los sliders pierden su estilo propio |

Se interactuó con los 4 componentes de los 3 estilos (botón, toggle, slider, y la tarjeta como elemento de lectura).
El panel registró 4 interacciones por estilo y 17 clics en total (incluye los del selector de componentes).

## 2. Medición del contraste (WCAG 2.2)

Se midió la razón de contraste de los colores definidos en el CSS: texto (criterio 1.4.3, mínimo 4,5:1) y
componentes de interfaz que el usuario debe percibir para operar (criterio 1.4.11, mínimo 3:1). En los degradados
se tomó el tono menos favorable.

| Estilo | Pares que cumplen | Hallazgo principal |
|---|---|---|
| Esqueumórfico | 6 de 7 | Todo el texto cumple; solo la perilla del toggle apagado frente a su pista queda en 2,50:1, compensada por el relieve y la sombra. |
| Plano | 4 de 7 | El texto cumple, pero la pista del slider (1,93:1), el botón frente a la columna (2,83:1) y la perilla del toggle apagado (2,56:1) no alcanzan 3:1. |
| Neumórfico | 3 de 8 | El botón y la perilla del toggle apagado tienen **el mismo color que su fondo (1,00:1)**; solo las sombras los delimitan (1,48:1). El párrafo de la tarjeta (#777 sobre #E0E5EC) da 3,54:1 y no cumple. |
| Neumórfico en modo oscuro (simulado) | 0 de 1 | Con fondo #1E293B, la sombra clara apenas alcanza 1,27:1. Confirma la observación de la guía: el estilo no funciona en modo oscuro. |

## 3. Auditoría automática de accesibilidad (axe-core, WCAG 2.x A/AA)

| Ámbito | Violaciones |
|---|---|
| Columna esqueumórfica | `label` (crítica): el slider no tiene etiqueta |
| Columna plana | `label` (crítica); `color-contrast` (grave): el título «Diseño Plano» (#3B82F6 sobre #1E293B) |
| Columna neumórfica | `label` (crítica); `color-contrast` (grave) en 2 nodos: el título «Neumorfismo» y el párrafo de la tarjeta |
| Página completa | 4 nodos con contraste insuficiente (incluye el texto blanco del filtro activo, 3,68:1) y 3 sliders sin etiqueta |

**Prueba de teclado (manual, automatizada con Tab):** el foco recorre el selector, los botones y los sliders, pero
**ningún toggle recibe el foco** en ninguno de los tres estilos: están hechos con `<div>` sin `role="switch"` ni
`tabindex`. axe-core no lo detecta porque no reconoce esos `div` como controles; por eso la prueba manual es necesaria.

## 4. Diferencias entre navegadores

Los sliders solo tienen estilo para WebKit/Blink (`::-webkit-slider-thumb`). En Firefox no hay regla
`::-moz-range-thumb`, por lo que los tres sliders muestran la misma perilla genérica: **la diferencia entre estilos
desaparece en ese componente** (comparar `04_toggles_activados_sliders_80.png` con `09_firefox.png`).

## 5. Análisis e interpretación

1. **Affordance y significantes.** El esqueumorfismo comunica «esto se puede presionar» con relieve, degradado y
   sombra, y es el único estilo que cumple casi todos los pares de contraste. El diseño plano conserva texto legible
   pero sus controles se apoyan en la convención (un rectángulo azul es un botón) más que en señales perceptibles:
   la pista del slider casi se confunde con el fondo. El neumorfismo elimina la diferencia de color entre el
   control y la superficie, de modo que el significante queda reducido a una sombra de 1,48:1. Esto coincide con
   Norman (2013): los significantes deben ser perceptibles, no solo estéticos.
2. **Tabla de 10 criterios.** Los datos respaldan tres filas de la tabla del ejercicio: affordance alta en el
   esqueumorfismo, accesibilidad «problemática» en el neumorfismo y «variable» en el plano. En cambio, la fila de
   *rendimiento* («pesado, imágenes») no aplica a esta implementación: aquí los tres estilos son CSS puro.
3. **Modo oscuro.** El neumorfismo necesita un fondo claro monocromático; en una página oscura, como la del propio
   ejercicio, queda como una «isla» clara (`.neu-zona`), y si se oscurece, la sombra baja a 1,27:1.
4. **Problemas comunes a los tres estilos.** La accesibilidad depende más de la implementación que del estilo:
   ningún toggle es operable con el teclado y ningún slider tiene etiqueta. Un estilo visual no corrige una
   semántica HTML deficiente.
5. **Relación con la medición del Paso 3.** Si el bajo contraste del neumorfismo reduce la affordance, se esperaría
   más tiempo y más clics en ese estilo (Pregunta 3 de la guía). Los datos reales del equipo (Paso 3) permiten
   contrastar esa hipótesis.

## 6. Recomendaciones para el proyecto del equipo

- Usar diseño plano con significantes reforzados: borde o fondo de los controles con al menos 3:1 frente a la
  superficie, estado de foco visible y estados presionado y activado diferenciados (el llamado *flat 2.0*).
- Evitar el neumorfismo en controles críticos; si se usa como decoración, añadir borde o color de acento.
- Implementar los toggles con `<button role="switch" aria-checked>` y etiquetar todos los sliders.
- Estilizar los sliders también para Firefox (`::-moz-range-thumb`, `::-moz-range-track`).
