# Plan de trabajo — Trabajo Grupal Semana 07: Metáforas de Interfaz (Guía de Laboratorio 6)

**Curso:** Interacción Hombre-Computador (202W0606) · Semestre 2026-2 · UNMSM — FISI
**Docente:** Mg. Ing. Ernesto D. Cancho-Rodríguez, MBA (GWU)
**Equipo A** · Fecha del plan: 16 de octubre de 2026

---

## 1. Qué pide la guía

La guía (`26.09.29.v4[print].Guia_Lab_06_Metaforas_de_Interfaz.pdf`) exige **dos documentos Word** y sus
artefactos, comprimidos en un único archivo:

```
yy.mm.dd.IHC_LabS06_GrupoA_Metafora.zip
```

| Entregable | Contenido obligatorio (sección L.6) |
|---|---|
| **Informe L.4** — Documentación paso a paso | Paso 1 (6.1): regeneración desde el prompt hasta una versión propia mejorada del HTML + verificación con capturas. Paso 2 (6.2): evidencia + interpretación. Paso 3 (6.3): evidencia + CSV → Excel + análisis de ≥ 30 registros. Paso 4 (6.3b): notebook mejorado + EDA. Paso 5: diagramas UML mejorados en SVG con su `.puml` + interpretación de cada uno. |
| **Informe L.5** — Reporte analítico de la metáfora propia | Metáfora nueva (distinta de las 12 de la galería) con dominio fuente, dominio destino, ≥ 5 correspondencias y tipo; prototipo HTML autocontenido e instrumentado; evaluación con ≥ 3 compañeros y CSV con n ≥ 30; análisis en notebook con ≥ 1 gráfico; Excel con Tabla con formato; anexos de capturas y de UML (SVG + `.puml`). |

**Rúbrica (20 pts, L.7):** Metáfora (original, 5+ correspondencias, tipo) · Prototipo (interactivo, diseño rico,
instrumentado) · Evaluación (3+ participantes, CSV) · Análisis (gráficos + interpretación) · Documentación
(informe + UML). El plan apunta al nivel «Excelente» en los cinco.

## 2. Insumos disponibles

| Insumo | Origen | Estado |
|---|---|---|
| Guía Lab 06 (PDF) | Carpeta / Classroom «P05: Parte1» | ✅ |
| `ejercicio_6_1_galeria_metaforas.html`, `ejercicio_6_2_comparativa_estilos.html` | Classroom «Parte2 METAFORAS: Los HTML/JS» | ✅ |
| `ejercicio_6_3_medicion_interaccion.html` (= https://stately-croquembouche-93dd68.netlify.app/, versión desplegada por el docente; el código es idéntico al archivo local) | Classroom «Parte3» | ✅ |
| Galería 6.1 desplegada: https://spiffy-creponne-8c534b.netlify.app/ | Classroom «Parte2» | ✅ (copia en `insumos/netlify/`) |
| `ejercicio_6_3_analisis_metaforas.ipynb` | Classroom «L06: Parte4» | ✅ |
| 5 diagramas UML del docente (`D1Comp…` a `D5UC…`, `.puml`) | Classroom «Parte5: Casos de Metáforas: Diagramas UML» | ✅ descargados en `insumos/uml_docente/` |
| PPT Sesión 06 (metáforas) | `S6/Lab06_Analisis_Metaforas/insumos/` | ✅ (reutilizable para el marco teórico) |
| Plantilla de informe con carátula (docx-js) y escudo | `S6/…/build/generar_informe.js` | ✅ (se reutiliza, adaptada a APA 7) |
| **CSV reales del ejercicio 6.3** (participantes del equipo) | Los envía una integrante | ⏳ **pendiente** |
| **CSV reales del prototipo L.5** (≥ 3 compañeros, n ≥ 30) | Los genera el equipo con el prototipo nuevo | ⏳ **pendiente** (requiere que el equipo lo use) |

> **Regla de integridad:** no se inventan datos de participantes. Los análisis de los pasos 3, 4 y L.5 se
> ejecutan solo con CSV reales. Mientras lleguen, el notebook se prueba con un archivo marcado
> explícitamente como `PRUEBA_` que no entra al informe.

## 3. Estructura de la carpeta y del repositorio

```
S7 - Grupal/
├── PLAN.md                      ← este documento
├── README.md                    ← portada del repositorio con enlaces
├── insumos/                     ← material del docente, sin modificar
│   ├── uml_docente/  netlify/  csv_reales_6_3/ (pendiente)
├── L4_paso_a_paso/
│   ├── paso1_galeria/           ← prompt, HTML regenerado y versión mejorada, capturas
│   ├── paso2_estilos/           ← capturas + cálculo de contraste WCAG
│   ├── paso3_medicion/          ← CSV reales consolidados + Excel con Tabla
│   ├── paso4_python/            ← notebook mejorado (.ipynb) + gráficos
│   └── paso5_uml/               ← 5 diagramas mejorados (.puml + .svg)
├── L5_metafora_propia/
│   ├── prototipo/               ← HTML autocontenido instrumentado
│   ├── datos/                   ← CSV de la evaluación + Excel con Tabla
│   ├── notebook/                ← análisis .ipynb + gráficos
│   ├── uml/                     ← diagramas de la metáfora (.puml + .svg)
│   └── capturas/
├── build/                       ← scripts (docx-js, conversión CSV→Excel, render PlantUML)
└── entregables/                 ← 2 .docx (+ PDF de control) y el .zip final
```

Repositorio público en GitHub (cuenta del token: `nicola3113`). Cada fase termina con un commit y un push.
El token se usa solo como variable de entorno: nunca se escribe en archivos, en la URL del remoto ni en
el historial.

## 4. Fases

### Fase 0 — Preparación (hoy)
- Crear la estructura de carpetas, `README.md`, `.gitignore` (excluye `node_modules/`, temporales de Office).
- Crear el repositorio público y subir el plan.

### Fase 1 — L.4 Paso 1: Galería interactiva (6.1)
1. Registrar el prompt AIAP literal de la guía y regenerar el artefacto con Claude (evidencia del proceso).
2. Construir la **versión propia mejorada y extendida**, sin perder nada del original:
   - Búsqueda por texto y filtros combinables; navegación completa por teclado y `aria-*` en el modal.
   - Conmutador claro/oscuro (respeta `prefers-color-scheme`) y contraste AA verificado.
   - Nueva sección **«Metáforas rotas»** (L.3.5) con los 4 casos de la guía y su demo.
   - Panel de métricas ampliado: tiempo de render, interacciones por tarjeta, exportación de métricas a CSV.
3. Verificar en navegadores (lista de comprobación de la guía: 12 tarjetas, 6 filtros, modal, demos, panel)
   con capturas. *Firefox no está instalado en esta PC: se verifica en Brave/Chromium y Edge, y se pide a un
   integrante con Firefox la captura de esa verificación (o se instala Firefox si se autoriza).*

### Fase 2 — L.4 Paso 2: Comparativa de estilos (6.2)
- Capturas de los 4 componentes × 3 estilos y de la tabla de 10 criterios.
- Valor agregado: **cálculo de la razón de contraste WCAG 2.2** de cada estilo (los colores se leen del CSS)
  para sustentar con números la limitación del neumorfismo (bajo contraste, incompatible con modo oscuro).
- Interpretación ligada a affordance, significantes (Norman, 2013) y heurística 4 de Nielsen.

### Fase 3 — L.4 Paso 3: Medición (6.3)
- Recibir los CSV reales de las integrantes (6 tareas por participante → **≥ 5 participantes = ≥ 30 filas**).
- Consolidar en un solo CSV añadiendo la columna `participante`; validar columnas y rangos.
- Convertir a **Excel con «Tabla con formato»** (openpyxl, estilo de tabla de Excel), una hoja por fuente y
  una hoja consolidada.
- Capturas del protocolo, de una tarea en curso y de la exportación.

### Fase 4 — L.4 Paso 4: Notebook mejorado (6.3b)
- Partir del notebook del docente y extenderlo:
  - Carga del CSV consolidado incrustado (para que «Ejecutar todas» no se bloquee en `files.upload()`).
  - Estadística descriptiva por estilo y por tipo de tarea (media, mediana, DE, IC 95 %), tasa de éxito.
  - Diagramas de caja de tiempo y clics, barras con error, dispersión tiempo-clics.
  - **Prueba de Kruskal-Wallis** (y ANOVA de un factor si se cumplen supuestos) con interpretación.
  - Tema claro para impresión, figuras exportadas a PNG para el informe.
- Ejecutar en Google Colab con la cuenta UNMSM y guardar el `.ipynb` ejecutado + capturas.

### Fase 5 — L.4 Paso 5: Diagramas UML
- Renderizar los 5 `.puml` del docente a SVG (servidor oficial de PlantUML, no hay Java local).
- Producir versiones **mejoradas/optimizadas** (corrección de notación, agrupación, notas, legibilidad) y
  comprobar lo que pide la guía: 4 capas (componentes), 3 fases (secuencia), 3 paquetes (clases), flujo de
  datos (actividades) y 15 casos de uso con `<<include>>`/`<<extend>>`.
- Una interpretación por diagrama en el informe.

### Fase 6 — L.5 Metáfora propia aplicada al proyecto del equipo
**Proyecto del equipo:** *Ernesto Investing AI* (plataforma de gestión de portafolio de inversiones, Lab 04).
**Tarea clave frecuente:** revisar el estado del portafolio y decidir si rebalancear.

**Propuesta de metáfora: «El portafolio como huerto»** — tipo **estructural** (con rasgos ontológicos).
No coincide con ninguna de las 12 de la galería (escritorio, carrito, progreso ascendente, arrastrar y soltar,
migas de pan, conversacional, ventanas, panel de control, zoom espacial, asistente paso a paso, papelera, nube).

| # | Dominio fuente (huerto) | Dominio destino (portafolio) |
|---|---|---|
| 1 | Parcela del huerto | Sector o clase de activo (diversificación) |
| 2 | Planta | Activo / posición abierta |
| 3 | Tamaño de la planta | Valor de mercado de la posición (peso en el portafolio) |
| 4 | Follaje verde / marchito | Rendimiento positivo / negativo |
| 5 | Sembrar una semilla | Comprar un activo nuevo |
| 6 | Regar | Aportar capital a una posición |
| 7 | Podar | Vender parcialmente / tomar ganancias |
| 8 | Cosecha | Dividendos o cupones cobrados |
| 9 | Clima y estaciones | Ciclo y volatilidad del mercado |

**Degradación elegante prevista:** las plantas no pierden 30 % en un día; por eso cada planta muestra al pasar
el cursor la cifra exacta (precio, variación, peso), de modo que la ruptura de la metáfora sea predecible.

**Diseño del experimento (intra-sujeto):** el prototipo muestra la misma cartera en dos condiciones —
**A: vista metafórica (huerto)** y **B: vista convencional (tabla/gráfico plano)**— con 3 tareas cada una
(p. ej., «¿qué sector pesa más?», «identifica el activo con peor rendimiento», «aporta S/ 500 al activo X»),
orden contrabalanceado. Se registra con `performance.now()` y `addEventListener`: `participante, condicion,
tarea, tiempo_ms, clics, errores, exito` y una pregunta de facilidad (SEQ 1–7). Con **≥ 5 participantes ×
6 tareas = ≥ 30 filas** (la guía pide mínimo 3 compañeros; se apunta a 5 o más de los 11 integrantes).
- Prototipo HTML autocontenido (sin dependencias obligatorias), publicado en **GitHub Pages** del mismo
  repositorio para que cada integrante lo use desde un enlace y exporte su CSV.
- Análisis: notebook propio (comparación A vs. B, Wilcoxon pareado, gráficos) + Excel con Tabla.
- UML de la metáfora: componentes, secuencia de una tarea instrumentada, clases, actividades y casos de uso.

### Fase 7 — Redacción de los dos informes (APA 7)
- Generación con docx-js reutilizando la plantilla de S6; luego Word (COM) para actualizar índice y exportar PDF.
- **Formato APA 7 de trabajo estudiantil**, sobrio y sin colores: Times New Roman 12, interlineado doble,
  márgenes de 2,54 cm, sangría de primera línea de 1,27 cm, numeración de página arriba a la derecha,
  niveles de título APA, tablas y figuras numeradas con título en cursiva y nota, texto en negro.
- Carátula: UNMSM, FISI, curso, docente, Equipo A con los 11 integrantes y sus códigos, fecha.
- **Referencias:** todas con fecha y con enlace (DOI o URL) **verificado abriendo cada uno** antes de incluirlo;
  sangría francesa. Base prevista: Lakoff y Johnson (1980), Carroll y Mack (1985), Norman (2013),
  Nielsen (heurísticas, NN/g), Desai et al. (2024), W3C (WCAG 2.2), MDN (`performance.now()`), documentación
  de pandas, matplotlib, SciPy y PlantUML.

### Fase 8 — Empaquetado y cierre
- Revisión contra la rúbrica y contra la lista de L.6 (cada viñeta con su archivo).
- Crear `yy.mm.dd.IHC_LabS06_GrupoA_Metafora.zip` con la fecha de entrega.
- Último push al repositorio con el README actualizado (enlaces a prototipos, notebooks y diagramas).

## 5. Qué necesita el equipo aportar

| Qué | Quién | Para qué fase |
|---|---|---|
| CSV reales del ejercicio 6.3 (≥ 5 participantes) | Integrante que los envía | Fases 3–4 |
| Usar el prototipo L.5 desde el enlace y exportar el CSV (≥ 5 integrantes) | Todos | Fase 6 |
| Captura de verificación en Firefox (si nadie lo autoriza instalar) | Quien tenga Firefox | Fase 1 |
| Fecha exacta de entrega (para el nombre del .zip) | Equipo | Fase 8 |

## 6. Integrantes (Equipo A)

Arboleda Sánchez, Ericka Sofía · Cabrejos Palomino, Christian Daniel · Ccoicca Fernández, Adrián ·
Cerna Sifuentes, Augusto Nicolás · Grijalva De La Cruz, Rony Smith · Martines Cancho, Josué ·
Postigo Vega, Diana Carolina · Siesquen Torres, Katherine Lizbeth · Tecsi Alanoca, Jean Carlo ·
Tonconi Isidro, María Sunori · Villegas Niño, Marco Antonio.
