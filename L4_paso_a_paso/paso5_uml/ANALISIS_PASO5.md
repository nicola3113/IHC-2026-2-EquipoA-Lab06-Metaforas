# Paso 5 — Diagramas UML: revisión, mejora y análisis

Equipo A · IHC 2026-2 · 16 de octubre de 2026

## 1. Evidencia de la realización

| Diagrama | Original del docente (renderizado) | Versión mejorada del Equipo A |
|---|---|---|
| D1 Componentes | `original_docente_svg/D1CompV1_…svg` | `D1CompV2_diagrama_componentes_metaforas_EquipoA.puml` + `.svg` |
| D2 Secuencia | `original_docente_svg/D2SeqV1_…svg` | `D2SeqV2_diagrama_secuencia_metaforas_EquipoA.puml` + `.svg` |
| D3 Clases | `original_docente_svg/D3ClassV1_…svg` | `D3ClassV2_diagrama_clases_metaforas_EquipoA.puml` + `.svg` |
| D4 Actividades | `original_docente_svg/D4ActiV1_…svg` | `D4ActiV2_diagrama_actividades_metaforas_EquipoA.puml` + `.svg` |
| D5 Casos de uso | `original_docente_svg/D5UCv1_…svg` | `D5UCv2_diagrama_casos_uso_metaforas_EquipoA.puml` + `.svg` |

Los `.puml` del docente se descargaron de Classroom («Parte5: Casos de Metáforas: Diagramas UML») y se guardan sin
cambios en `insumos/uml_docente/`. Todos los SVG se generaron con el servidor oficial de PlantUML
(`build/paso5/render_plantuml.py`; el equipo no tiene Java instalado). Cada SVG tiene junto a él un PNG de vista
previa, rasterizado localmente con Chromium.

**Criterio de estilo de la V2:** escala de grises y sin sombras para que los diagramas se lean al imprimir el
informe en blanco y negro. Se mantienen los elementos que la guía pide identificar.

## 2. Lo que pide identificar la guía

| Pide la guía | Original | V2 |
|---|---|---|
| 4 capas del diagrama de componentes | Presentación, Lógica de interacción, Datos y exportación, Análisis (Python) | Las mismas 4 capas |
| 3 fases del diagrama de secuencia | Exploración, Estudio controlado, Exportación | Las mismas 3 fases |
| 3 paquetes del diagrama de clases | Modelo de metáforas, de evaluación y de métricas | Los mismos 3 paquetes |
| Flujo de datos del diagrama de actividades | 4 particiones: carga, exploración, estudio, exportación y análisis | 4 fases en 3 carriles (Participante, Navegador, Equipo) |
| 15 casos de uso con `include` y `extend` | 15 casos, 5 `include` y 6 `extend` | 15 casos, 5 `include` y 6 `extend` (dirección corregida) |

## 3. Análisis e interpretación de cada diagrama

### D1 — Componentes
**Qué muestra:** cómo se reparten las responsabilidades en cuatro capas. La presentación (las tres páginas HTML y el
panel) delega en la lógica (filtro, modal, motor del estudio y registrador); el registrador acumula datos que se
exportan como CSV y alimentan el análisis en Python.

**Problemas del original y correcciones:**
- La interfaz `addEventListener` solo aparecía como dependencia del registrador; la V2 separa las interfaces
  requeridas `IEventos` e `IReloj` (`performance.now()`), que usan el registrador y el motor, y la interfaz
  provista `IExportación`.
- La galería no enviaba eventos al registrador, aunque el código sí los cuenta; la V2 añade esa conexión y la del
  panel, que solo *lee* el almacén (dependencia punteada).
- Los archivos generados aparecen como artefactos (`resultados_metaforas_pN.csv`, `galeria61_eventos.csv`, el
  Excel), lo que hace visible el flujo de datos entre capas.
- Se añaden los componentes de la versión propia: búsqueda, modal accesible, verificador automático, iconos
  incrustados, consolidador y el módulo de pruebas para medidas repetidas.

**Interpretación:** el acoplamiento entre presentación y datos pasa siempre por el registrador. Por eso fue posible
pausar las métricas durante la verificación automática sin tocar las páginas.

### D2 — Secuencia
**Qué muestra:** el orden temporal de los mensajes entre el participante, la interfaz, el motor, el registrador y el
almacén en las tres fases.

**Problemas del original y correcciones:**
- Sugería que el registrador calcula el tiempo («Calcula tiempo en tarea»). En el código, el **motor** guarda
  `inicio = performance.now()` al cargar la tarea y calcula `tiempo_ms` al completarla; la V2 lo modela así.
- No mostraba cuándo se marca el éxito ni que el interruptor puede volver a `éxito = false`; la V2 usa un fragmento
  `alt`.
- Se numeran los mensajes (`autonumber`), se añade la latencia del modal en la fase 1 y el identificador del
  participante en el registro.
- El original usa `skinparam ParticipantPadding`, que la versión actual de PlantUML ignora y muestra como un recuadro
  de advertencia en el diagrama; la V2 lo elimina.

**Interpretación:** el diagrama deja ver una limitación del experimento: el tiempo incluye llevar el cursor hasta
«Completar tarea», fuera del área de la tarea (ver Paso 3).

### D3 — Clases
**Qué muestra:** el modelo de dominio en tres paquetes: las metáforas y su taxonomía, el estudio controlado y las
métricas.

**Problemas del original y correcciones:**
- `Metafora` no tenía atributo `tipo` y el mapeo era un `String[]`; la V2 añade `tipo : TipoMetafora` y modela el
  mapeo como la clase `Correspondencia` con multiplicidad **5..\***, que es el mínimo que exige la guía (L.5).
- `RegistroTarea.estilo` era `String` aunque existía el enumerado `EstiloVisual`; ahora usa el enumerado.
- Las multiplicidades del tipo `"1" clasificada como "1"` se reemplazan por notación UML estándar en los extremos.
- Se añaden `EvaluacionCriterios` (los 5 criterios L.3.4), `DemoInteractiva`, `MetaforaRota`, `Participante`,
  `Evento` y `VerificadorAutomatico`.

**Interpretación:** la composición `Metafora ◆— Correspondencia (5..*)` convierte una exigencia de la rúbrica en una
regla del modelo, y `Participante — RegistroTarea` refleja la columna `participante` que tienen los datos reales.

### D4 — Actividades
**Qué muestra:** cómo nacen y se transforman los datos, desde el catálogo JSON hasta la interpretación estadística.

**Problemas del original y correcciones:**
- Decía «Re-renderizar tarjetas filtradas»; en la versión propia el filtro **oculta** tarjetas y conserva el estado
  de las demos.
- La rama «no» de «¿Acción correcta?» estaba vacía, pero en el código apagar el interruptor vuelve a
  `éxito = false`.
- La nota del CSV omitía `descripcion`; la V2 registra los campos reales, incluido `participante`.
- Se añaden carriles (quién hace cada acción) y la fase de análisis completa: consolidar, validar, generar el Excel y
  elegir la prueba según la normalidad (Shapiro-Wilk → ANOVA de medidas repetidas o Friedman).

**Interpretación:** la decisión sobre la normalidad hace explícito por qué el Paso 4 usa pruebas no paramétricas
(los tres estilos rechazaron la normalidad).

### D5 — Casos de uso
**Qué muestra:** los objetivos del participante (explorar, comparar, completar el estudio) y del evaluador
(calcular e interpretar resultados) en cuatro módulos.

**Problemas del original y correcciones:**
- **Las seis flechas `<<extend>>` estaban invertidas.** En UML la flecha de extensión va del caso que extiende al
  caso base (por ejemplo, «Exportar CSV» extiende «Realizar estudio»). En el original iban del caso base al opcional.
- «Filtrar» y «Ver detalle» eran `include` de «Explorar galería», es decir, obligatorios, aunque el usuario puede
  explorar sin hacerlo; pasan a `extend`. «Interactuar con los componentes» es imprescindible para comparar estilos,
  así que pasa a `include`.
- «Registrar métricas» se incluye en «Completar tarea», que es donde ocurre la medición. «Calcular estadísticas»
  incluye «Cargar el CSV», e «Interpretar resultados» incluye «Calcular estadísticas».
- El actor que analiza pasa a ser el «Evaluador (equipo / docente)», porque en este laboratorio el análisis lo hace
  el equipo.

**Interpretación:** con la dirección correcta se lee qué es obligatorio (5 `include`) y qué es opcional (6 `extend`)
para cada objetivo; esa distinción sirve de base para priorizar funciones en el prototipo propio (L.5).
