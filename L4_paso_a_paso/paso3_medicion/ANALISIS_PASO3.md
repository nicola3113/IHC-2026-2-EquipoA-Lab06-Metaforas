# Paso 3 — Medición de la efectividad (Ejercicio 6.3): evidencia y análisis de los datos reales

Equipo A · IHC 2026-2 · 16 de octubre de 2026

## 1. Evidencia de la realización

| Archivo | Contenido |
|---|---|
| `capturas/6_3_01_protocolo.png` | Pantalla inicial con el protocolo del estudio |
| `capturas/6_3_02_tarea{1,3,4,6}_antes.png` | Tareas en curso (interruptor esqueumórfico y neumórfico, botón esqueumórfico y neumórfico) |
| `capturas/6_3_03_tarea{3,6}_completada.png` | Retroalimentación al completar la tarea |
| `capturas/6_3_04_resultados.png` | Tabla de resultados y botón «Exportar CSV» habilitado |
| `capturas/demo_no_analizar.csv` | CSV de la sesión de demostración (solo evidencia del formato; **no** forma parte del análisis) |
| `capturas/excel_Resumen_por_estilo.png`, `capturas/excel_Consolidado.png` | Hojas del Excel con «Tabla con formato» |

Las capturas se tomaron con una sesión de demostración automatizada (`build/paso3/capturar_6_3.py`). Los datos
analizados son **exclusivamente** los CSV reales que el equipo registró con participantes.

## 2. Datos

- **Fuente:** `insumos/csv_reales_6_3/resultados_metaforas_p1.csv` … `p5.csv`, recibidos el 16/10/2026.
- **Tamaño:** 5 participantes × 6 tareas = **30 registros** (cumple el mínimo n ≥ 30 de la guía).
- **Diseño:** intra-sujeto. Cada participante hizo 2 tipos de tarea (activar un interruptor y presionar «Enviar»)
  en los 3 estilos, siempre en el mismo orden: esqueumórfico → plano → neumórfico.
- **Transformación:** `build/paso3/consolidar_6_3.py` valida las columnas, rangos y la secuencia de tareas de cada
  participante, añade `tipo_tarea`, `tiempo_s` y la hora de Lima, y genera:
  - `resultados_6_3_consolidado.csv` (30 filas).
  - `resultados_6_3_EquipoA.xlsx`: hojas `Resumen_por_estilo` (fórmulas `COUNTIFS`, `AVERAGEIFS`, `MINIFS` y
    `MAXIFS` sobre la tabla, más un gráfico de columnas), `Consolidado`, `Resumen_tarea_estilo`,
    `Resumen_participante`, una hoja por participante (`p1`–`p5`) y `Diccionario`. Cada hoja usa
    **«Tabla con formato»** (estilo Medio 2). Excel recalculó el libro (`build/paso3/recalcular_excel.ps1`).
- **Formato:** los CSV del equipo incluyen `participante` y `fecha` y usan las descripciones «Activar interruptor» y
  «Presionar botón Enviar». El HTML del docente exporta solo `tarea, estilo, descripcion, tiempo_ms, clics, exito`
  con títulos como «Tarea 1 — Activar el interruptor (esqueumórfico)» (ver `capturas/demo_no_analizar.csv`).
  Los datos se registraron con una versión del HTML adaptada para identificar al participante; la lógica de
  medición (tiempo con `performance.now()`, clics en el área y éxito) es la misma.

## 3. Resultados descriptivos

**Por estilo (10 registros cada uno):**

| Estilo | Media (ms) | Mediana (ms) | DE (ms) | Mín.–máx. (ms) | Clics medios | Éxito |
|---|---|---|---|---|---|---|
| Esqueumórfico | 649,4 | 537,0 | 321,5 | 380–1432 | 1,0 | 100 % |
| Plano | 827,9 | 606,5 | 627,4 | 329–2323 | 1,0 | 100 % |
| Neumórfico | 683,5 | 483,5 | 472,1 | 364–1905 | 1,0 | 100 % |

**Por tipo de tarea y estilo (media / mediana, ms):**

| Tarea | Esqueumórfico | Plano | Neumórfico |
|---|---|---|---|
| Interruptor (toggle) | 706,8 / 552,0 | 868,8 / 531,0 | 827,4 / 472,0 |
| Botón Enviar | 592,0 / 470,0 | 787,0 / 779,0 | 539,6 / 495,0 |

**Por participante (media, ms):** p1 1437,5 · p2 425,2 · p3 636,3 · p4 679,2 · p5 423,2.

**Rango medio dentro de cada participante y tarea** (1 = el estilo más rápido de los tres, 3 = el más lento;
10 bloques): esqueumórfico 1,7 · neumórfico 1,9 · plano 2,4.

## 4. Análisis e interpretación

1. **El plano tuvo la media más alta, pero la diferencia depende de un participante.** La media del plano
   (828 ms) supera en 179 ms al esqueumórfico. Sin embargo, p1 es mucho más lento que el resto (media 1438 ms,
   más del doble que los demás) y sus dos tiempos en plano (2323 y 1427 ms) son los máximos de ese estilo. Sin p1,
   las medias quedan en 524 (esqueumórfico), 566 (plano) y 533 ms (neumórfico): una diferencia de unos 40 ms.
   La mediana, que es robusta a valores extremos, ordena distinto: neumórfico 484 < esqueumórfico 537 < plano 607.
2. **Tendencia intra-sujeto.** Al comparar cada participante consigo mismo, el plano tiende a ser el más lento
   (rango medio 2,4 de 3) y el esqueumórfico el más rápido (1,7). Es una tendencia, no una conclusión: con 5
   participantes hay que comprobar si es estadísticamente significativa (Paso 4, prueba de Friedman para medidas
   repetidas).
3. **Efecto techo en clics y éxito.** Las 30 tareas se hicieron con 1 clic y con éxito. Ni los clics ni la tasa
   de éxito distinguen los estilos; solo el tiempo aporta información. Las tareas son demasiado fáciles: un único
   control por pantalla y la descripción ya dice el estilo y la acción.
4. **No se reproduce la Pregunta 3 de la guía** (neumorfismo con 40 % más tiempo y 60 % más clics). En estos datos
   el neumorfismo no es más lento ni requiere clics extra. Posibles razones: la tarea nombra el control a usar,
   la zona neumórfica es una «isla» clara sobre la página oscura que atrae la mirada (efecto de resalte), y el
   tercer estilo se beneficia del aprendizaje por ir siempre al final.
5. **El orden fijo es un factor de confusión.** El esqueumórfico siempre va primero en cada tipo de tarea y el
   neumórfico último; el aprendizaje y la familiarización con la tarea se mezclan con el efecto del estilo. Además,
   el tiempo incluye llevar el cursor hasta «Completar tarea», que está fuera del área de la tarea.
6. **Condiciones de registro.** Las cinco sesiones se registraron una tras otra entre las 16:32 y las 16:35 (hora
   de Lima), con una duración de 5 a 12 segundos cada una. Es coherente con participantes que se turnan en el mismo
   equipo; en un estudio formal convendría que no observen a los participantes anteriores.

## 5. Limitaciones y mejoras para el experimento

- Contrabalancear el orden de los estilos (cuadrado latino de 3 × 3) para separar estilo y aprendizaje.
- Aumentar la dificultad: varias opciones por pantalla con el control objetivo sin rotular, para que la affordance
  importe y aparezcan errores y clics exploratorios.
- Medir el tiempo hasta el clic correcto (no hasta «Completar tarea») y añadir una tarea de práctica inicial.
- Más participantes (al menos 10) y registrar el dispositivo y el navegador.
