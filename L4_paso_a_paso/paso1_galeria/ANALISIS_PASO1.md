# Paso 1 — Galería interactiva de metáforas (Ejercicio 6.1): proceso, verificación y análisis

Equipo A · IHC 2026-2 · 16 de octubre de 2026

## 1. Del prompt a la versión propia

| Etapa | Archivo | Qué es |
|---|---|---|
| 0. Original del docente | `insumos/ejercicio_6_1_galeria_metaforas.html` | Referencia (50 KB + Lucide `@latest` y fuentes por CDN). |
| 1. Prompt AIAP | `01_prompt_AIAP.md` | Prompt literal de la guía y registro de la ejecución. |
| 2. Regeneración | `02_regenerado_desde_prompt/ejercicio_6_1_regenerado.html` | Respuesta de Claude al prompt, con las mismas 12 metáforas. |
| 3. Versión propia | `03_version_mejorada/ejercicio_6_1_galeria_metaforas_v2_EquipoA.html` | Mejorada y extendida por el equipo (93 KB, sin scripts externos). |

El código fuente de la versión propia está en `build/paso1/galeria_v2.src.html`; `build/paso1/incrustar_iconos.py`
genera el HTML final incrustando los iconos Lucide v0.469.0.

## 2. Revisión del original del docente (hallazgos que motivaron las mejoras)

| # | Hallazgo en el original | Consecuencia | Respuesta en la v2 |
|---|---|---|---|
| H1 | Solo 2 de 12 tarjetas tienen una demo que responde (carrito y barra de progreso); 4 tarjetas (ventanas, panel de control, papelera y nube) muestran solo un icono. | No se cumple del todo «cada tarjeta con demo visual interactiva». | 12 demos interactivas, cada una con estado y retroalimentación. |
| H2 | La demo de arrastrar y soltar no se puede arrastrar; las migas de pan, el zoom y el asistente son estáticos. | La metáfora se describe, pero no se experimenta. | Arrastre real con *pointer events* (ratón y táctil) y alternativa por teclado. |
| H3 | `lucide@latest` y Google Fonts desde CDN. | Sin conexión no hay iconos, y una versión nueva de Lucide puede romper la página. | Iconos incrustados como SVG (versión fija 0.469.0) y fuente de respaldo del sistema. |
| H4 | Al cambiar de filtro la rejilla se vuelve a generar. | Se pierde el estado de las demos (el contador del carrito vuelve a 0). | Las tarjetas se ocultan con `hidden`; el estado se conserva. |
| H5 | El modal no atrapa el foco, no devuelve el foco al cerrarse y no tiene `aria-labelledby`. | Problemas para el usuario de teclado y de lector de pantalla. | Trampa de foco, retorno del foco, `aria-labelledby`, bloqueo del desplazamiento de fondo. |
| H6 | Los filtros no comunican su estado (`aria-pressed`). | El lector de pantalla no sabe qué filtro está activo. | `aria-pressed` y un contador de resultados en `aria-live`. |
| H7 | Texto blanco sobre el azul del filtro activo: **3,68:1**. | No cumple WCAG 2.2 AA para texto normal (4,5:1). | Todos los pares de texto de la v2 superan 4,5:1 (ver `verificacion/contraste_wcag_v2.csv`). |
| H8 | El panel de métricas solo usa `performance.now()` para el tiempo en página. | No mide la respuesta de la interfaz. | Latencia de apertura del modal, tiempo hasta la primera interacción y lectura por metáfora. |
| H9 | No hay forma de exportar las métricas. | No se pueden analizar en Python. | Exportación de la bitácora a CSV (compatible con `pandas.read_csv`) y del resumen a JSON. |

## 3. Mejoras y extensiones de la versión propia

1. **Funciona sin conexión**: iconos SVG incrustados y tipografía de respaldo.
2. **Búsqueda de texto** (sin distinguir tildes) combinable con los seis filtros, con estado vacío.
3. **Tema claro y oscuro**: respeta `prefers-color-scheme`, se recuerda entre visitas y se puede forzar con `?tema=claro`.
4. **Accesibilidad**: enlace para saltar a la galería, foco visible, `aria-pressed`, `aria-live`, trampa y retorno de
   foco en el modal, alternativa por teclado al arrastre, `prefers-reduced-motion`, `scroll-padding` para que la
   barra fija no tape el elemento enfocado.
5. **Evaluación por criterios en el modal**: cada metáfora se valora de 1 a 5 en familiaridad, consistencia,
   extensibilidad, descubribilidad y degradación elegante (criterios L.3.4 de la guía), con una nota que justifica
   la valoración. La tarjeta muestra el promedio.
6. **Sección «Metáforas rotas»** con los cuatro casos de la guía (L.3.5): papelera que expulsa discos, libro
   electrónico, asistente que saluda como humano y archivos en la nube. Cada caso se revela al interactuar e indica
   el criterio violado y cómo diseñar una degradación elegante.
7. **Panel de métricas ampliado**: 8 indicadores, distribución de interacciones por tipo de metáfora, tiempo de
   lectura por metáfora, bitácora de los últimos 30 eventos y exportación CSV/JSON.
8. **Verificación automática**: el botón «Verificar funcionamiento» (o `?autotest=1`) ejecuta 12 comprobaciones
   que cubren la lista de la guía y muestra el resultado, el tiempo de cada una y el navegador usado. Durante la
   verificación las métricas se pausan para no contaminar los datos del usuario.

## 4. Verificación de funcionamiento

La guía pide verificar en Chrome y Firefox que las 12 tarjetas se renderizan, que los 6 filtros funcionan, que el
modal abre y cierra, que las demos responden a eventos y que el panel se actualiza. Se verificó en **tres**
navegadores con dos métodos complementarios:

- **Verificación automática de la página** (12 comprobaciones) en los tres navegadores.
- **Lista de la guía con eventos reales del navegador** (clics, teclado y un arrastre real del ratón) con
  Playwright en Chrome y Edge (`build/paso1/verificar_navegadores.py`). Firefox se verificó con su modo
  *headless* oficial (`build/paso1/verificar_firefox.sh`).

| Navegador | Versión | Verificación automática | Lista de la guía (eventos reales) | Errores en consola |
|---|---|---|---|---|
| Google Chrome | 155.0.8059.84 | 12/12 | 12 tarjetas · filtros 3/2/2/2/2/1 · modal abre y cierra · carrito = 1 · arrastre real ✔ · panel actualizado | 0 |
| Microsoft Edge | 155.0.4283.45 | 12/12 | Idéntico a Chrome | 0 |
| Mozilla Firefox | 137.0.1 | 12/12 | (captura de la verificación automática) | — |

Resultados completos: `verificacion/resultado_chrome_edge.json`. Capturas: `capturas/v2_verificacion_chrome.png`,
`capturas/v2_verificacion_edge.png` y `capturas/v2_verificacion_firefox.png`.

Durante la verificación se encontraron y corrigieron tres defectos de la propia versión mejorada, lo que muestra el
valor de la prueba automática:

1. La comprobación del tema leía el color del `body` mientras duraba su transición; ahora compara el token `--fondo`.
2. La barra fija superior tapaba los elementos a los que se desplazaba la página; se añadió `scroll-padding-top`.
3. El texto blanco sobre el azul primario del tema oscuro daba 3,24:1; se cambió a texto oscuro (5,82:1).

## 5. Análisis de resultados

- **Cumplimiento del prompt**: la regeneración y la v2 cumplen literalmente «cada tarjeta con demo visual
  interactiva»; el original lo hace en 2 de 12 tarjetas. Esto muestra que un prompt corto deja huecos que el
  diseñador debe revisar: el resultado de un asistente de IA es un punto de partida, no un producto terminado.
- **Taxonomía**: la distribución es desigual (3 estructurales y 1 conversacional). Se mantuvo para que las tres
  versiones sean comparables y para respetar la galería que la guía usa como referencia en L.5.
- **Criterios**: según la valoración del equipo, la metáfora con mejor promedio es «Progreso ascendente» (4,4) y las
  de menor promedio (3,4) son «Zoom espacial», «Arrastrar y soltar», «La nube» y «Conversación». Las dos últimas
  tienen 2/5 en degradación elegante: cuando fallan, el usuario no tiene pistas de por qué. «Arrastrar y soltar» es la única con 2/5 en descubribilidad, y por eso la v2 le añade
  una alternativa visible.
- **Metáforas rotas**: los cuatro casos violan criterios distintos (consistencia, extensibilidad, degradación
  elegante y descubribilidad), lo que confirma que los cinco criterios de la guía sirven como lista de chequeo
  para anticipar rupturas.
- **Accesibilidad y robustez**: la v2 elimina la dependencia de CDN (funciona sin conexión), cumple AA en todos los
  pares de texto en ambos temas y puede usarse solo con el teclado.
- **Instrumentación**: la latencia de apertura del modal (desde el clic hasta el siguiente cuadro pintado, medida con
  `performance.now()` y `requestAnimationFrame`) fue de 9,9 ms de media en Chrome y 9,8 ms en Edge en 24 aperturas
  (`verificacion/latencia_modal.csv`, `build/paso1/medir_latencia_modal.py`), muy por debajo de los 100 ms en que
  una respuesta se percibe como instantánea.

## 6. Capturas

| Archivo | Contenido |
|---|---|
| `original_docente*.png`, `v1_regenerado*.png` | Punto de partida y regeneración desde el prompt |
| `v2_01_vista_general_oscuro.png`, `v2_02_pagina_completa_oscuro.png` | Versión propia, vista general y página completa |
| `v2_03_filtro_contenedor.png`, `v2_04_busqueda_carpeta.png` | Filtro por tipo y búsqueda |
| `v2_05_modal_criterios.png` | Modal con mapeo y evaluación por criterios |
| `v2_06_demos_en_uso.png` | Demos después de interactuar |
| `v2_07_metaforas_rotas.png` | Las cuatro metáforas rotas reveladas |
| `v2_08_panel_metricas.png` | Panel de métricas con datos |
| `v2_09_tema_claro.png`, `v2_10_movil.png` | Tema claro y vista móvil (390 px) |
| `v2_verificacion_{chrome,edge,firefox}.png`, `v2_firefox_vista_general.png` | Verificación en los tres navegadores |
