// Informe L.4 — Documentación paso a paso del desarrollo (Guía de Laboratorio 6), APA 7.
// Uso: node informe_L4.js   →  entregables/Informe_L4_Paso_a_Paso_Lab06_EquipoA.docx
const path = require('path');
const A = require('./apa');
const { p, h1, h2, h3, vineta, numerado, tabla, figura, REF, parrafoEnlace, salto, centro, runs, TextRun } = A;

const TITULO = 'Documentación paso a paso del Laboratorio 6: metáforas de interfaz, estilos visuales, medición de la interacción, análisis en Python y diagramas UML';
const FECHA = '16 de octubre de 2026';
const REPO = 'https://github.com/nicola3113/IHC-2026-2-EquipoA-Lab06-Metaforas';
const PAGES = 'https://nicola3113.github.io/IHC-2026-2-EquipoA-Lab06-Metaforas/';
const C = {
  guia: ['Cancho-Rodríguez, E. D. (2026a, 29 de septiembre). *Guía de laboratorio 6. Metáforas de interfaz: definición, tipos y criterios de diseño* [Guía de laboratorio, curso Interacción Hombre-Computador]. Universidad Nacional Mayor de San Marcos.', 'https://classroom.google.com/c/ODc2Mjc4NDQzOTI2/sa/ODcwMTIzOTEyMzc2/details'],
  html: ['Cancho-Rodríguez, E. D. (2026b, 9 de octubre). *Parte 2. Metáforas: los HTML/JS* [Material del curso: ejercicios 6.1 y 6.2]. Google Classroom.', 'https://classroom.google.com/c/ODc2Mjc4NDQzOTI2/m/ODcwMTI0NjE2MDI0/details'],
  med: ['Cancho-Rodríguez, E. D. (2026c, 9 de octubre). *Ejercicio 6.3: medición de interacción con metáforas* [Aplicación web].', 'https://stately-croquembouche-93dd68.netlify.app/'],
  nb: ['Cancho-Rodríguez, E. D. (2026d, 9 de octubre). *L06: Parte 4. Python: Lab06 ejercicio_6_3_analisis_metafora* [Notebook del curso]. Google Classroom.', 'https://classroom.google.com/c/ODc2Mjc4NDQzOTI2/a/ODkwMzMyMTg4MTM2/details'],
  uml: ['Cancho-Rodríguez, E. D. (2026e, 9 de octubre). *Parte 5. Casos de metáforas: diagramas UML* [Material del curso: archivos PlantUML]. Google Classroom.', 'https://classroom.google.com/c/ODc2Mjc4NDQzOTI2/m/ODkwMzMzMTU2NTU3/details'],
  claude: ['Anthropic. (2026). *Claude* (versión Opus 5.5) [Modelo de lenguaje de gran tamaño].', 'https://www.anthropic.com/claude'],
};
const P1 = 'L4_paso_a_paso/paso1_galeria/capturas/';
const P2 = 'L4_paso_a_paso/paso2_estilos/capturas/';
const P3 = 'L4_paso_a_paso/paso3_medicion/capturas/';
const P4 = 'L4_paso_a_paso/paso4_python/';
const P5 = 'L4_paso_a_paso/paso5_uml/';
const CAPT = (fecha = '16 de octubre de 2026') => `Captura de pantalla tomada por el Equipo A el ${fecha}.`;

const cuerpo = [
  centro(runs(`**${TITULO}**`)),
  h1('Introducción'),
  p('Una metáfora de interfaz es una correspondencia entre un dominio fuente que el usuario ya conoce y el sistema digital, que le permite trasladar ese conocimiento y reducir la carga cognitiva (Lakoff y Johnson, 1980/2003; Carroll y Mack, 1985). La Guía de Laboratorio 6 (Cancho-Rodríguez, 2026a) propone estudiar las metáforas en cinco pasos: explorar y regenerar una galería interactiva de 12 metáforas (Ejercicio 6.1), comparar tres estilos visuales (Ejercicio 6.2), medir la interacción en el navegador (Ejercicio 6.3), analizar esas mediciones en Python (Ejercicio 6.3b) y revisar los diagramas UML del sistema.'),
  p('Este informe documenta cómo el Equipo A desarrolló cada paso, con la evidencia de su realización (capturas, archivos y datos) y el análisis e interpretación de los resultados, tal como pide la sección L.6 de la guía. Todo el material está publicado en un repositorio público, con los scripts que permiten reproducir cada resultado.'),
  parrafoEnlace('Repositorio del trabajo: ', REPO),
  parrafoEnlace('Galería 6.1 del Equipo A (versión propia): ', PAGES + 'L4_paso_a_paso/paso1_galeria/03_version_mejorada/ejercicio_6_1_galeria_metaforas_v2_EquipoA.html'),

  h1('Marco Teórico Breve'),
  h2('Metáforas de Interfaz y su Taxonomía'),
  p('Lakoff y Johnson (1980/2003) mostraron que las metáforas son estructuras del pensamiento y no solo figuras retóricas. Carroll y Mack (1985) llevaron esa idea al diseño de sistemas y observaron que los usuarios interpretan un sistema nuevo mediante analogías con objetos conocidos, y que tienden a *sobreextender* la analogía. La guía clasifica las metáforas en seis tipos: estructurales (escritorio, ventanas), orientacionales (barra de progreso, zoom), ontológicas (arrastrar y soltar, la nube), de contenedor (carrito, papelera), de viaje (migas de pan, asistente paso a paso) y conversacionales (chatbots). Blackwell (2006) advierte que la metáfora es una herramienta de diseño útil, pero que su valor depende de cómo se implementa y no del nombre que recibe.'),
  h2('Estilos de Diseño Metafórico y Criterios de Efectividad'),
  p('El esqueumorfismo imita objetos físicos y ofrece significantes muy visibles; el diseño plano usa colores sólidos y depende de convenciones aprendidas; el neumorfismo combina relieves suaves sobre fondos monocromáticos y suele tener poco contraste. Norman (2013) recuerda que lo importante es que los significantes sean perceptibles, y la heurística de consistencia y estándares (Nielsen, 2024) exige no mezclar estilos. La guía propone cinco criterios para una metáfora efectiva: familiaridad, consistencia, extensibilidad, descubribilidad y degradación elegante. Cuando la correspondencia falla aparece una *metáfora rota*, como la papelera que expulsaba discos o el asistente de voz que promete más de lo que puede hacer (Desai et al., 2024).'),

  h1('Metodología'),
  p(`Los insumos se obtuvieron del tema «Trab. Grupal Semana 07: Trab. Inv. METÁFORAS» de Google Classroom (Tabla ${A.siguienteTabla()}). Los cinco archivos PlantUML de la Parte 5 no venían con la guía y se descargaron de Classroom. Los datos del Ejercicio 6.3 son 30 registros reales que el equipo tomó con cinco participantes el 16 de octubre de 2026.`),
  ...tabla('Insumos utilizados en el laboratorio', ['Insumo', 'Origen', 'Uso en el informe'], [
    ['Guía de Laboratorio 6 (PDF)', 'Classroom, «P05: Parte 1»', 'Pasos, entregables y rúbrica'],
    ['ejercicio_6_1_galeria_metaforas.html y ejercicio_6_2_comparativa_estilos.html', 'Classroom, «Parte 2»', 'Pasos 1 y 2'],
    ['ejercicio_6_3_medicion_interaccion.html (publicado en Netlify)', 'Classroom, «Parte 3»', 'Paso 3'],
    ['ejercicio_6_3_analisis_metaforas.ipynb', 'Classroom, «L06: Parte 4»', 'Paso 4'],
    ['D1Comp… a D5UC… (5 archivos .puml)', 'Classroom, «Parte 5»', 'Paso 5'],
    ['resultados_metaforas_p1.csv … p5.csv', 'Integrantes del equipo', 'Pasos 3 y 4 (30 registros)'],
  ], [3600, 2200, 3226], 'Los archivos del docente se conservan sin cambios en la carpeta `insumos/` del repositorio.'),
  p('Se trabajó en Windows 11 con Google Chrome 155, Microsoft Edge 155 y Mozilla Firefox 137; Python 3.11 (pandas, SciPy, statsmodels y matplotlib; McKinney, 2010; Virtanen et al., 2020; Seabold y Perktold, 2010; Hunter, 2007); Google Colab; Playwright para automatizar las verificaciones en el navegador; axe-core para la auditoría de accesibilidad (Deque Systems, 2024); y el servidor oficial de PlantUML para generar los SVG.'),
  p('**Uso de inteligencia artificial.** Siguiendo el método AIAP de la guía, el código del Paso 1 se regeneró con Claude (Anthropic, 2026) a partir del prompt de la guía; el asistente también apoyó la escritura de los scripts de verificación y análisis. El equipo definió las mejoras, revisó el código, ejecutó las pruebas y validó cada resultado antes de incluirlo.'),

  // ---------------------------------------------------------------- PASO 1
  h1('Paso 1: Galería Interactiva de Metáforas (Ejercicio 6.1)'),
  h2('Del Prompt a la Versión Propia'),
  p('El trabajo siguió tres etapas. Primero se exploró el original del docente: 12 tarjetas, 6 filtros, un modal de detalle y un panel de métricas (Figura 1). Luego se ejecutó con Claude el prompt literal de la guía: «Actúa como diseñador de interfaces. Crea un HTML autocontenido con una galería interactiva de 12 metáforas de interfaz clasificadas en 6 tipos. Cada tarjeta con demo visual interactiva, modal de detalle, y panel de métricas con performance.now(). Modo oscuro, Inter, Lucide Icons». Para que las versiones fueran comparables se pidió conservar las mismas 12 metáforas (Figura 2). Por último, a partir de la regeneración se construyó la versión propia mejorada y extendida (Figura 3).'),
  ...figura(P1 + 'original_docente.png', 'Galería original del docente (Ejercicio 6.1)', `Archivo \`ejercicio_6_1_galeria_metaforas.html\` (Cancho-Rodríguez, 2026b). ${CAPT()}`, 560),
  ...figura(P1 + 'v1_regenerado.png', 'Galería regenerada desde el prompt de la guía', `Archivo \`02_regenerado_desde_prompt/ejercicio_6_1_regenerado.html\`, generado con Claude (Anthropic, 2026) y revisado por el equipo. ${CAPT()}`, 560),
  h2('Hallazgos en el Original y Mejoras Introducidas'),
  p(`La revisión del código original reveló varios puntos que justificaron las mejoras (Tabla ${A.siguienteTabla()}).`),
  ...tabla('Hallazgos en la galería original y respuesta de la versión propia', ['Hallazgo en el original', 'Consecuencia', 'Respuesta en la versión propia'], [
    ['Solo 2 de 12 tarjetas tienen una demo que responde; 4 muestran solo un icono', 'No se cumple «cada tarjeta con demo interactiva»', '12 demos interactivas con estado y retroalimentación'],
    ['La demo de arrastrar y soltar no se puede arrastrar', 'La metáfora se describe pero no se experimenta', 'Arrastre real con *pointer events* y alternativa por teclado'],
    ['Lucide `@latest` y fuentes por CDN', 'Sin conexión no hay iconos; una versión nueva puede romper la página', 'Iconos SVG incrustados (versión 0.469.0) y fuente de respaldo'],
    ['Al cambiar de filtro se regenera la rejilla', 'Se pierde el estado de las demos', 'Las tarjetas se ocultan; el estado se conserva'],
    ['El modal no atrapa ni devuelve el foco', 'Barreras para teclado y lector de pantalla', 'Trampa y retorno del foco, `aria-labelledby`'],
    ['Texto blanco sobre el filtro activo: 3,68:1', 'No cumple WCAG 2.2 AA (4,5:1)', 'Todos los pares de texto superan 4,5:1 en ambos temas'],
    ['`performance.now()` solo mide el tiempo en página', 'No mide la respuesta de la interfaz', 'Latencia del modal, primera interacción y tiempo de lectura'],
    ['Sin exportación de métricas', 'No se pueden analizar en Python', 'Exportación a CSV y JSON'],
  ], [3100, 2700, 3226], 'Contraste calculado con la fórmula de WCAG 2.2 (World Wide Web Consortium, 2024).'),
  p('Además de corregir esos puntos, la versión propia agrega: búsqueda de texto combinable con los filtros; tema claro y oscuro; una evaluación de cada metáfora según los cinco criterios de la guía, mostrada en el modal (Figura 4); una sección de **metáforas rotas** con los cuatro casos de la guía, que se revelan al interactuar e indican el criterio violado y cómo lograr una degradación elegante (Figura 5); un panel de métricas ampliado con distribución por tipo, tiempo de lectura y bitácora de eventos (Figura 6); y un botón de **verificación automática** que ejecuta la lista de comprobación de la guía.'),
  ...figura(P1 + 'v2_01_vista_general_oscuro.png', 'Versión propia mejorada: vista general con búsqueda, filtros y valoración por criterios', CAPT(), 560),
  ...figura(P1 + 'v2_05_modal_criterios.png', 'Modal de detalle con el mapeo y la evaluación según los cinco criterios', 'La valoración de 1 a 5 es un juicio del equipo basado en el marco teórico. ' + CAPT(), 540),
  ...figura(P1 + 'v2_07_metaforas_rotas.png', 'Sección de metáforas rotas con los cuatro casos de la guía', CAPT(), 600),
  ...figura(P1 + 'v2_08_panel_metricas.png', 'Panel de métricas ampliado con datos de una sesión', CAPT(), 560),
  h2('Verificación de Funcionamiento'),
  p(`La guía pide verificar en Chrome y Firefox que las 12 tarjetas se renderizan, que los 6 filtros funcionan, que el modal abre y cierra, que las demos responden y que el panel se actualiza. Se verificó en tres navegadores con dos métodos: la verificación automática de la página (12 comprobaciones) y, en Chrome y Edge, la misma lista ejecutada con eventos reales del navegador mediante Playwright, incluido un arrastre con el ratón (Tabla ${A.siguienteTabla()}, Figuras 7 y 8).`),
  ...tabla('Resultados de la verificación de la galería en tres navegadores', ['Navegador', 'Versión', 'Verificación automática', 'Lista de la guía con eventos reales', 'Errores en consola'], [
    ['Google Chrome', '155.0.8059.84', '12/12', '12 tarjetas; filtros 3/2/2/2/2/1; modal abre y cierra; demos y arrastre responden; panel actualizado', '0'],
    ['Microsoft Edge', '155.0.4283.45', '12/12', 'Igual que en Chrome', '0'],
    ['Mozilla Firefox', '137.0.1', '12/12', 'Verificación automática en modo headless', '—'],
  ], [1500, 1400, 1300, 3800, 1026], 'Resultados completos en `paso1_galeria/verificacion/resultado_chrome_edge.json`.'),
  ...figura(P1 + 'v2_verificacion_chrome.png', 'Verificación automática superada en Google Chrome', CAPT(), 560),
  ...figura(P1 + 'v2_verificacion_firefox.png', 'Verificación automática superada en Mozilla Firefox', CAPT(), 520),
  h2('Análisis de Resultados del Paso 1'),
  p('La comparación entre versiones muestra que un prompt corto deja huecos que el diseñador debe revisar: el original cumple «cada tarjeta con demo interactiva» solo en 2 de 12 casos, mientras que la regeneración y la versión propia lo cumplen en las 12. Las pruebas automáticas encontraron además tres defectos en la propia versión mejorada antes de entregarla (una prueba que leía el color durante una transición, la barra fija que tapaba elementos enfocados y un contraste de 3,24:1 en el tema oscuro), todos corregidos.'),
  p('Según la valoración del equipo, la metáfora con mejor promedio en los cinco criterios es «Progreso ascendente» (4,4 de 5). Las de menor promedio (3,4) son «Zoom espacial», «Arrastrar y soltar», «La nube» y «Conversación»; las dos últimas tienen 2 de 5 en degradación elegante, porque cuando fallan el usuario no recibe pistas de lo que ocurre. Los cuatro casos de metáforas rotas violan criterios distintos (consistencia, extensibilidad, degradación elegante y descubribilidad), lo que confirma que los cinco criterios sirven para anticipar rupturas. La latencia de apertura del modal fue de 9,9 ms de media en Chrome y de 9,8 ms en Edge (24 aperturas), muy por debajo de los 100 ms en que una respuesta se percibe como inmediata.'),

  // ---------------------------------------------------------------- PASO 2
  h1('Paso 2: Comparativa de Estilos Visuales (Ejercicio 6.2)'),
  h2('Evidencia de la Realización'),
  p('Se usaron los cuatro componentes (botón, interruptor, deslizador y tarjeta) en los tres estilos, se registraron sus estados presionado y activado, y se consultó la tabla de 10 criterios (Figuras 9 y 10). El panel registró cuatro interacciones por estilo. La página también se abrió en Firefox, en el que los deslizadores pierden su estilo propio porque el CSS solo los define para Chromium (Figura 11).'),
  ...figura(P2 + '04_toggles_activados_sliders_80.png', 'Los cuatro componentes en los tres estilos, con los interruptores activados', CAPT(), 600),
  ...figura(P2 + '06_tabla_10_criterios.png', 'Tabla comparativa de 10 criterios del Ejercicio 6.2', `Tabla incluida en el ejercicio del docente (Cancho-Rodríguez, 2026b). ${CAPT()}`, 600),
  ...figura(P2 + '09_firefox.png', 'El Ejercicio 6.2 en Mozilla Firefox', 'Los tres deslizadores muestran la misma perilla genérica. ' + CAPT(), 560),
  h2('Medición del Contraste y Auditoría de Accesibilidad'),
  p(`Para respaldar con datos la tabla de criterios, se midió la razón de contraste WCAG 2.2 de los colores definidos en el CSS: texto (criterio 1.4.3, mínimo 4,5:1) y componentes que el usuario debe percibir para operar (criterio 1.4.11, mínimo 3:1; World Wide Web Consortium, 2024). También se ejecutó axe-core y se probó la navegación con la tecla Tab (Tabla ${A.siguienteTabla()}).`),
  ...tabla('Contraste y accesibilidad de los tres estilos del Ejercicio 6.2', ['Estilo', 'Pares que cumplen', 'Hallazgo principal de contraste', 'axe-core y teclado'], [
    ['Esqueumórfico', '6 de 7', 'Todo el texto cumple; solo la perilla del interruptor apagado queda en 2,50:1', 'Deslizador sin etiqueta; interruptor no alcanzable con Tab'],
    ['Plano', '4 de 7', 'Pista del deslizador 1,93:1 y botón frente a la columna 2,83:1', 'Además, título «Diseño Plano» con 3,96:1'],
    ['Neumórfico', '3 de 8', 'Botón y perilla con el mismo color que el fondo (1,00:1); sombra 1,48:1; párrafo 3,54:1', 'Título y párrafo con contraste insuficiente'],
    ['Neumórfico en modo oscuro (simulado)', '0 de 1', 'Sombra clara sobre fondo oscuro: 1,27:1', '—'],
  ], [1700, 1200, 3500, 2626], 'En los degradados se tomó el tono menos favorable. Datos completos en `paso2_estilos/contraste_wcag_6_2.csv` y `resultado_analisis_6_2.json`.'),
  h2('Análisis e Interpretación del Paso 2'),
  p('Los datos confirman tres filas de la tabla del ejercicio: affordance alta del esqueumorfismo, accesibilidad «problemática» del neumorfismo y «variable» del diseño plano. En el neumorfismo el control tiene el mismo color que la superficie, de modo que el significante se reduce a una sombra de 1,48:1, lo que coincide con la advertencia de Norman (2013) sobre los significantes poco perceptibles. La observación de la guía sobre el modo oscuro también se confirma: si el fondo se oscurece, la sombra baja a 1,27:1. En cambio, la fila de rendimiento («pesado, imágenes») no aplica a esta implementación, porque los tres estilos están hechos solo con CSS.'),
  p('Un hallazgo que la tabla no recoge es que la accesibilidad depende más de la implementación que del estilo: en ninguno de los tres estilos se puede llegar a los interruptores con el teclado (son elementos `div` sin rol ni `tabindex`) y ningún deslizador tiene etiqueta. axe-core no detecta el problema de los interruptores porque no los reconoce como controles; por eso hizo falta la prueba manual. Para el proyecto del equipo se recomienda un diseño plano con significantes reforzados (contraste de al menos 3:1 en los controles y estados claramente diferenciados) y evitar el neumorfismo en controles críticos.'),

  // ---------------------------------------------------------------- PASO 3
  h1('Paso 3: Medición de la Efectividad (Ejercicio 6.3)'),
  h2('Evidencia de la Realización'),
  p('El Ejercicio 6.3 presenta seis tareas (activar un interruptor y presionar «Enviar formulario», cada una en los tres estilos) y registra el tiempo en tarea con `performance.now()`, los clics dentro del área y el éxito (MDN Web Docs, 2024; Cancho-Rodríguez, 2026c). Cinco participantes completaron el estudio y exportaron su CSV. Las Figuras 12 y 13 muestran el protocolo durante una sesión de demostración (sus datos no forman parte del análisis).'),
  ...figura(P3 + '6_3_02_tarea3_antes.png', 'Tarea 3 del Ejercicio 6.3: activar el interruptor neumórfico', CAPT(), 540),
  ...figura(P3 + '6_3_04_resultados.png', 'Tabla de resultados y exportación del CSV al terminar las seis tareas', 'Sesión de demostración; sus datos no se analizaron. ' + CAPT(), 500, 700),
  p('Los cinco CSV se consolidaron en 30 registros, que cumplen el mínimo de la guía (n ≥ 30). Un script valida las columnas, los rangos y que cada participante tenga sus seis tareas, y genera un Excel con **«Tabla con formato»** en cada hoja: resumen por estilo con fórmulas (`COUNTIFS`, `AVERAGEIFS`, `MINIFS`, `MAXIFS`) y gráfico, datos consolidados, resúmenes por tarea y por participante, una hoja por participante y un diccionario de datos (Figura 14).'),
  ...figura(P3 + 'excel_Resumen_por_estilo.png', 'Hoja «Resumen_por_estilo» del Excel con tabla con formato y gráfico', 'Archivo `resultados_6_3_EquipoA.xlsx`. ' + CAPT(), 580),
  h2('Resultados Descriptivos'),
  ...tabla('Tiempo en tarea, clics y éxito por estilo (5 participantes, 30 registros)', ['Estilo', 'n', 'Media (ms)', 'Mediana (ms)', 'DE (ms)', 'Mín.–máx. (ms)', 'Clics', 'Éxito'], [
    ['Esqueumórfico', '10', '649,4', '537,0', '321,5', '380–1432', '1,0', '100 %'],
    ['Plano', '10', '827,9', '606,5', '627,4', '329–2323', '1,0', '100 %'],
    ['Neumórfico', '10', '683,5', '483,5', '472,1', '364–1905', '1,0', '100 %'],
  ], [1600, 500, 1100, 1200, 1000, 1500, 800, 900], 'DE = desviación estándar. Datos registrados por el equipo el 16 de octubre de 2026.'),
  ...tabla('Media y mediana del tiempo (ms) por tipo de tarea y estilo', ['Tarea', 'Esqueumórfico', 'Plano', 'Neumórfico'], [
    ['Interruptor', '706,8 / 552,0', '868,8 / 531,0', '827,4 / 472,0'],
    ['Botón «Enviar»', '592,0 / 470,0', '787,0 / 779,0', '539,6 / 495,0'],
  ], [2400, 2200, 2200, 2226], 'Cada celda muestra media / mediana sobre 5 registros.'),
  h2('Análisis e Interpretación del Paso 3'),
  p('El estilo plano tuvo la media más alta (828 ms), 179 ms más que el esqueumórfico, pero esa diferencia depende de un participante: p1 tuvo una media de 1438 ms, más del doble que los demás, y aportó los dos máximos del plano (2323 y 1427 ms). Sin p1, las medias quedan en 524, 566 y 533 ms. La mediana, que resiste mejor los valores extremos, ordena distinto: neumórfico (484 ms), esqueumórfico (537 ms) y plano (607 ms). Al comparar a cada participante consigo mismo, el plano tiende a ser el más lento (rango medio de 2,4 sobre 3), una tendencia que se pone a prueba en el Paso 4.'),
  p('Los 30 registros tienen un clic y éxito: hay un **efecto techo**, por lo que solo el tiempo diferencia los estilos. Por eso no se reproduce la Pregunta 3 de la guía (neumorfismo con 40 % más de tiempo y 60 % más de clics). Probablemente influyen la simplicidad de las tareas (un solo control por pantalla, rotulado), la «isla» clara del neumorfismo sobre la página oscura, que atrae la mirada, y el **orden fijo** (esqueumórfico, plano, neumórfico), que mezcla el aprendizaje con el efecto del estilo. Además, el tiempo incluye llevar el cursor hasta «Completar tarea». Para un estudio formal se recomienda contrabalancear el orden, aumentar la dificultad y medir el tiempo hasta el clic correcto.'),

  // ---------------------------------------------------------------- PASO 4
  h1('Paso 4: Análisis en Python (Ejercicio 6.3b)'),
  h2('Notebook Mejorado y Extendido'),
  p(`El notebook del docente (Cancho-Rodríguez, 2026d) se conservó en su flujo y se extendió (Tabla ${A.siguienteTabla()}). Se ejecutó en Google Colab con «Ejecutar todas», sin errores, y la versión ejecutada se descargó de Drive (Figura 15).`),
  ...tabla('Mejoras del notebook respecto al original', ['Notebook del docente', 'Versión del Equipo A'], [
    ['Carga con `files.upload()`, que detiene «Ejecutar todas»', 'Datos reales incrustados; la subida manual queda como opción'],
    ['Sin validación de datos', 'Faltantes, diseño completo, rangos y detección del efecto techo'],
    ['Media, mediana, clics y éxito', 'Además DE, mínimo, máximo, coeficiente de variación e IC 95 %'],
    ['Dos gráficos de barras (tema oscuro)', 'Barras con IC 95 %, clics y éxito, diagrama de caja, perfil por participante y mediana por tarea (tema claro)'],
    ['Sugiere ANOVA o Kruskal-Wallis', 'Pruebas para medidas repetidas: Shapiro-Wilk, Friedman con W de Kendall, Wilcoxon con corrección de Holm y ANOVA de medidas repetidas sobre log-tiempo'],
    ['Interpretación basada en la media menor', 'Interpretación generada a partir de las pruebas, el tamaño del efecto y un análisis de sensibilidad sin el participante atípico'],
  ], [4000, 5026], 'Notebook `Lab06_ejercicio_6_3b_analisis_EquipoA.ipynb`, disponible en el repositorio.'),
  ...figura(P4 + 'capturas/colab_06_interpretacion.jpg', 'Interpretación automática del notebook ejecutado en Google Colab', CAPT(), 600),
  h2('Resultados del Análisis Exploratorio y Pruebas Estadísticas'),
  p(`La Figura 16 muestra el tiempo medio con su intervalo de confianza del 95 %: los tres intervalos se solapan casi por completo. La Figura 17 muestra la distribución por estilo y el perfil de cada participante, en el que destaca p1. El tiempo no se distribuye normalmente en ningún estilo (Shapiro-Wilk, p = 0,011; 0,010 y 0,001), por lo que se priorizaron las pruebas no paramétricas para medidas repetidas (Friedman, 1937; Wilcoxon, 1945; Holm, 1979), adecuadas porque cada participante usó los tres estilos (Tabla ${A.siguienteTabla()}).`),
  ...figura(P4 + 'figuras/fig1_tiempo_medio_ic95.png', 'Tiempo medio en tarea por estilo con intervalo de confianza del 95 %', 'Generada por el notebook (celda 6).', 480),
  ...figura(P4 + 'figuras/fig3_caja_y_participantes.png', 'Distribución del tiempo por estilo y perfil de cada participante', 'Generada por el notebook (celda 8).', 600),
  ...tabla('Pruebas estadísticas sobre el tiempo en tarea (α = 0,05)', ['Prueba', 'Resultado', 'Conclusión'], [
    ['Friedman, 10 bloques (participante × tarea)', 'χ²(2) = 2,6; p = 0,27; W de Kendall = 0,13', 'Sin diferencias; efecto pequeño'],
    ['Friedman sin p1 (8 bloques)', 'χ²(2) = 1,0; p = 0,61; W = 0,06', 'Sin diferencias'],
    ['Wilcoxon con corrección de Holm', 'Esq. vs. plano p = 0,48; plano vs. neu. p = 0,48; esq. vs. neu. p = 0,92', 'Ningún par difiere'],
    ['ANOVA de medidas repetidas (log-tiempo)', 'Estilo: F(2, 8) = 0,69; p = 0,53; η²p = 0,15', 'Sin efecto del estilo ni de la tarea'],
    ['Kruskal-Wallis (solo referencia)', 'H = 0,20; p = 0,90', 'Ignora el diseño intra-sujeto'],
  ], [3000, 3700, 2326], 'Calculado con SciPy y statsmodels en el notebook del equipo.'),
  h2('Análisis e Interpretación del Paso 4'),
  p('No hay evidencia estadística de que el estilo visual cambie el tiempo en tarea en este experimento. La ventaja aparente del esqueumórfico sobre el plano se explica casi por completo por un participante y desaparece en las pruebas robustas, y el tamaño del efecto es pequeño (W = 0,13). La hipótesis de la guía, que el neumorfismo es más lento, no se confirma; pero tampoco se refuta, porque el efecto techo, el orden fijo y una muestra de cinco personas dejan al estudio con poca potencia. Esto concuerda con el Paso 2: el neumorfismo tiene peor contraste, pero con una tarea rotulada y un solo control el usuario lo encuentra igual.'),
  p('La principal lección metodológica es elegir la prueba según el diseño. Kruskal-Wallis (p = 0,90) trata como independientes datos que no lo son; Friedman y el ANOVA de medidas repetidas usan a cada participante como su propio control y por eso son las pruebas adecuadas aquí. Estas conclusiones se aplicaron al diseño de la evaluación de la metáfora propia (L.5): orden contrabalanceado, tareas con varias opciones y escala de facilidad percibida (Sauro y Dumas, 2009).'),

  // ---------------------------------------------------------------- PASO 5
  h1('Paso 5: Revisión de los Diagramas UML'),
  h2('Evidencia de la Realización'),
  p(`Los cinco archivos PlantUML del docente (Cancho-Rodríguez, 2026e) se renderizaron a SVG sin modificarlos y se revisaron contra el código de los ejercicios. Después se produjeron versiones mejoradas (V2), cada una en SVG con su archivo \`.puml\`, en escala de grises para que se lean al imprimir. La Tabla ${A.siguienteTabla()} resume lo que la guía pide identificar.`),
  ...tabla('Elementos que pide identificar la guía en cada diagrama', ['Diagrama', 'Original del docente', 'Versión mejorada (V2)'], [
    ['Componentes', '4 capas: presentación, lógica de interacción, datos y exportación, análisis', 'Las mismas 4 capas, con interfaces y artefactos'],
    ['Secuencia', '3 fases: exploración, estudio controlado, exportación', 'Las mismas 3 fases, con mensajes numerados y fragmento `alt`'],
    ['Clases', '3 paquetes: metáforas, evaluación y métricas', 'Los mismos 3 paquetes, con tipos y multiplicidades corregidos'],
    ['Actividades', 'Flujo de datos en 4 particiones', 'Flujo de datos en 4 fases y 3 carriles'],
    ['Casos de uso', '15 casos, 5 `include` y 6 `extend`', '15 casos, 5 `include` y 6 `extend` con la dirección corregida'],
  ], [1700, 3700, 3626], 'Los diagramas originales renderizados están en `paso5_uml/original_docente_svg/`.'),
  h2('Análisis e Interpretación de Cada Diagrama'),
  h3('Diagrama de Componentes'),
  p('Muestra cómo se reparten las responsabilidades en cuatro capas: las páginas HTML delegan en la lógica (filtro, modal, motor del estudio y registrador), el registrador acumula datos que se exportan como CSV y estos alimentan el análisis en Python. En la V2 se separan las interfaces requeridas (`addEventListener` y `performance.now()`) y la interfaz provista de exportación, se añade la conexión de la galería con el registrador (que el código sí tiene) y se representan los archivos generados como artefactos (Figura 18). El diagrama deja ver que la presentación y los datos solo se comunican a través del registrador, lo que permitió pausar las métricas durante la verificación automática sin tocar las páginas.'),
  ...figura(P5 + 'D1CompV2_diagrama_componentes_metaforas_EquipoA.png', 'Diagrama de componentes mejorado (V2)', 'Fuente: `D1CompV2_diagrama_componentes_metaforas_EquipoA.puml` y `.svg`.', 600),
  h3('Diagrama de Secuencia'),
  p('Ordena en el tiempo los mensajes entre el participante, la interfaz, el motor, el registrador y el almacén. El original sugería que el registrador calcula el tiempo; en el código lo hace el motor, que guarda la marca de inicio al cargar la tarea y calcula `tiempo_ms` al completarla, y así se modela en la V2. También se añade un fragmento `alt` para el éxito (el interruptor puede volver a éxito = 0) y se elimina un parámetro obsoleto (`ParticipantPadding`) que en la versión actual de PlantUML aparece como un recuadro de advertencia en el diagrama original (Figura 19). El diagrama hace visible una limitación del experimento: el tiempo incluye el recorrido hasta «Completar tarea».'),
  ...figura(P5 + 'D2SeqV2_diagrama_secuencia_metaforas_EquipoA.png', 'Diagrama de secuencia mejorado (V2)', 'Fuente: `D2SeqV2_diagrama_secuencia_metaforas_EquipoA.puml` y `.svg`.', 520, 860),
  h3('Diagrama de Clases'),
  p('Describe el modelo de dominio en tres paquetes. En el original, `Metafora` no tenía atributo `tipo`, el mapeo era una lista de textos y `RegistroTarea.estilo` era un texto aunque existía el enumerado `EstiloVisual`. La V2 añade `tipo`, modela el mapeo como la clase `Correspondencia` con multiplicidad 5..* (el mínimo que exige la guía para una metáfora), usa el enumerado y agrega `EvaluacionCriterios`, `MetaforaRota`, `Participante` y `Evento` (Figura 20). Así, una exigencia de la rúbrica queda expresada como regla del modelo.'),
  ...figura(P5 + 'D3ClassV2_diagrama_clases_metaforas_EquipoA.png', 'Diagrama de clases mejorado (V2)', 'Fuente: `D3ClassV2_diagrama_clases_metaforas_EquipoA.puml` y `.svg`.', 600),
  h3('Diagrama de Actividades'),
  p('Sigue la evolución de los datos desde el catálogo JSON hasta la interpretación estadística. La V2 corrige que el filtro «regenera» la rejilla (en la versión propia solo oculta tarjetas), completa la rama en que el éxito vuelve a ser falso, añade carriles para indicar quién realiza cada acción y extiende la fase de análisis con la consolidación, la validación y la elección de la prueba según la normalidad (Figura 21). Esa decisión explica por qué el Paso 4 usó pruebas no paramétricas.'),
  ...figura(P5 + 'D4ActiV2_diagrama_actividades_metaforas_EquipoA.png', 'Diagrama de actividades mejorado (V2)', 'Fuente: `D4ActiV2_diagrama_actividades_metaforas_EquipoA.puml` y `.svg`.', 470, 860),
  h3('Diagrama de Casos de Uso'),
  p('Presenta los objetivos del participante (explorar, comparar y completar el estudio) y del evaluador (calcular e interpretar resultados). El hallazgo más importante fue que **las seis relaciones extend del original estaban invertidas**: en UML la flecha va del caso que extiende al caso base (por ejemplo, «Exportar CSV» extiende «Realizar estudio»). En la V2 se corrigió la dirección, las acciones opcionales (filtrar, ver detalle) pasaron a `extend` y las obligatorias (interactuar con los componentes para comparar estilos) a `include` (Figura 22). Con la dirección correcta se distingue con claridad qué es obligatorio y qué es opcional para cada objetivo.'),
  ...figura(P5 + 'D5UCv2_diagrama_casos_uso_metaforas_EquipoA.png', 'Diagrama de casos de uso mejorado (V2)', 'Fuente: `D5UCv2_diagrama_casos_uso_metaforas_EquipoA.puml` y `.svg`.', 600),

  // ---------------------------------------------------------------- cierre
  h1('Discusión'),
  p('Los cinco pasos convergen en una misma idea: una metáfora visual no es efectiva por su apariencia, sino por la calidad de sus significantes y de su implementación. El Paso 2 mostró con mediciones que el neumorfismo debilita los significantes (contraste de 1,00:1 entre el control y su fondo), pero el Paso 3 y el Paso 4 no encontraron diferencias de tiempo con tareas tan simples. Ambos resultados son compatibles: con un único control rotulado, el usuario encuentra el objetivo aunque la affordance sea baja. Las diferencias aparecerían en tareas con varias opciones y controles sin rótulo, que es justamente donde la metáfora debe orientar al usuario.'),
  p('El trabajo también mostró el valor de verificar. La galería del docente no cumplía del todo su propio prompt; la regeneración con IA lo cumplió, pero la versión mejorada tuvo tres defectos que solo aparecieron con pruebas automáticas; y los diagramas UML del docente tenían relaciones invertidas y un parámetro obsoleto. Asimismo, uno de los enlaces de referencia de la guía (el artículo de Nielsen Norman Group sobre metáforas) ya no está disponible, por lo que no se usó.'),
  h1('Conclusiones'),
  numerado('Se regeneró la galería 6.1 desde el prompt AIAP y se construyó una versión propia que funciona sin conexión, es accesible, evalúa cada metáfora con los cinco criterios de la guía, incluye las metáforas rotas y supera las 12 comprobaciones en Chrome, Edge y Firefox.', 'numeros'),
  numerado('La comparativa de estilos, medida con WCAG 2.2 y axe-core, confirmó que el neumorfismo tiene los significantes más débiles y que no funciona en modo oscuro, y reveló que en los tres estilos los interruptores no son operables con el teclado.', 'numeros'),
  numerado('Con 30 registros reales de cinco participantes, el tiempo en tarea no difiere significativamente entre estilos (Friedman, p = 0,27, efecto pequeño); los clics y el éxito presentan un efecto techo.', 'numeros'),
  numerado('El notebook se extendió con validación, estadística descriptiva completa y pruebas para medidas repetidas, y se ejecutó en Google Colab sin errores; la lección central es elegir la prueba según el diseño del estudio.', 'numeros'),
  numerado('Los cinco diagramas UML se renderizaron y se mejoraron, corrigiendo la dirección de las relaciones `extend`, los tipos y multiplicidades del modelo de clases y la responsabilidad del cálculo del tiempo en la secuencia.', 'numeros'),

  salto(),
  h1('Referencias'),
  ...A.referencias([C.claude, REF.blackwell, C.guia, C.html, C.med, C.nb, C.uml, REF.carroll, REF.deque, REF.desai, REF.friedman, REF.holm, REF.hunter,
    REF.lakoff, REF.lucide, REF.mckinney, REF.mdn, REF.nielsen, REF.norman, REF.sauro, REF.seabold, REF.virtanen, REF.wilcoxon, REF.w3c]),

  salto(),
  h1('Anexo A: Archivos Entregados'),
  ...tabla('Archivos del Informe L.4 dentro del paquete de entrega', ['Paso', 'Archivo o carpeta', 'Contenido'], [
    ['1', 'paso1_galeria/03_version_mejorada/ejercicio_6_1_galeria_metaforas_v2_EquipoA.html', 'Galería propia mejorada (autocontenida)'],
    ['1', 'paso1_galeria/02_regenerado_desde_prompt/ejercicio_6_1_regenerado.html', 'Regeneración desde el prompt'],
    ['1', 'paso1_galeria/01_prompt_AIAP.md, capturas/, verificacion/', 'Prompt, capturas y resultados de verificación'],
    ['2', 'paso2_estilos/capturas/, contraste_wcag_6_2.csv', 'Evidencia y mediciones de contraste'],
    ['3', 'paso3_medicion/resultados_6_3_EquipoA.xlsx', 'CSV consolidados en Excel con tablas con formato'],
    ['4', 'paso4_python/Lab06_ejercicio_6_3b_analisis_EquipoA.ipynb', 'Notebook mejorado ejecutado en Colab, con figuras y tablas'],
    ['5', 'paso5_uml/*.svg y *.puml', 'Cinco diagramas mejorados con su código fuente'],
  ], [700, 5000, 3326], `Todos los archivos están también en el repositorio: ${REPO}.`),
];

A.reiniciarContadores();
const doc = A.documento(TITULO, [...A.caratula(TITULO, 'Informe L.4 · Guía de Laboratorio 6 · Trabajo grupal de la Semana 07', FECHA), ...A.indice(), ...cuerpo]);
A.guardar(doc, process.env.OUT || path.join(A.RAIZ, 'entregables', 'Informe_L4_Paso_a_Paso_Lab06_EquipoA.docx'));
