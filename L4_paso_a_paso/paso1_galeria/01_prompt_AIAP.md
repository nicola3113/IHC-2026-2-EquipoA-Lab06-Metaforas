# Paso 1 — Prompt AIAP y registro de la regeneración

## Prompt literal de la guía (L.4, Paso 1)

> Actúa como diseñador de interfaces. Crea un HTML autocontenido con una galería interactiva de 12 metáforas
> de interfaz clasificadas en 6 tipos. Cada tarjeta con demo visual interactiva, modal de detalle, y panel de
> métricas con performance.now(). Modo oscuro, Inter, Lucide Icons.

## Registro de la ejecución

| Campo | Valor |
|---|---|
| Asistente | Claude (Anthropic), modelo Claude Opus 5.5, en Claude Code (aplicación de escritorio) |
| Fecha | 16 de octubre de 2026 |
| Entrada | El prompt literal anterior, sin adjuntos. Para mantener comparables las versiones se pidió conservar las mismas 12 metáforas de la galería del docente. |
| Salida | `02_regenerado_desde_prompt/ejercicio_6_1_regenerado.html` |
| Revisión humana | El Equipo A revisó el código, lo probó con la lista de verificación de la guía y definió las mejoras de la versión propia. |

## De la regeneración a la versión propia

1. **Original del docente** (`insumos/ejercicio_6_1_galeria_metaforas.html`): punto de referencia.
2. **Regeneración desde el prompt** (`02_regenerado_desde_prompt/`): cumple el prompt al pie de la letra
   (las 12 tarjetas con demo interactiva y métricas con `performance.now()`).
3. **Versión propia mejorada y extendida** (`03_version_mejorada/`): parte de la regeneración y añade
   las mejoras definidas por el equipo (ver `ANALISIS_PASO1.md`).

### Prompt de extensión usado para la versión propia

> Partiendo del HTML regenerado, crea una versión mejorada y extendida que conserve las 12 tarjetas, los
> 6 filtros, el modal y el panel de métricas, y que además: (1) funcione sin conexión, con los iconos Lucide
> incrustados como SVG y tipografía de respaldo; (2) añada búsqueda de texto combinable con los filtros;
> (3) ofrezca tema claro y oscuro con contraste AA verificado; (4) cumpla accesibilidad de teclado y lector de
> pantalla (aria-pressed, trampa de foco en el modal, retorno del foco, aria-live, reduced motion);
> (5) incluya en el modal una evaluación de la metáfora según los cinco criterios de la guía (familiaridad,
> consistencia, extensibilidad, descubribilidad y degradación elegante); (6) agregue una sección de
> «Metáforas rotas» con los cuatro casos de la guía; (7) amplíe el panel de métricas con latencia de apertura
> del modal, tiempo hasta la primera interacción, tiempo de permanencia por metáfora, distribución por tipo,
> bitácora de eventos y exportación a CSV y JSON; y (8) incluya un botón de verificación automática que
> ejecute la lista de comprobación de la guía y muestre el resultado de cada punto.
