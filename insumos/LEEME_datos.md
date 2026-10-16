# Datos recibidos del equipo (16/10/2026)

Fuente: `csv_reales_6_3/datossss.zip`, enviado por una integrante. Se extrajo en dos carpetas porque contiene
**dos experimentos distintos**.

## 1. `csv_reales_6_3/` — Ejercicio 6.3 (estilos visuales)

- 5 archivos `resultados_metaforas_p1.csv` … `p5.csv` → **5 participantes × 6 tareas = 30 filas** (cumple n ≥ 30).
- Columnas: `participante, tarea, estilo, descripcion, tiempo_ms, clics, exito, fecha`.
  El HTML del docente exporta `tarea, estilo, descripcion, tiempo_ms, clics, exito`; estos archivos añaden
  `participante` y `fecha` y usan las descripciones «Activar interruptor» y «Presionar botón Enviar».
- Sesiones registradas el 16/10/2026 entre 16:32 y 16:35 (hora de Lima), una tras otra.
- Resumen preliminar (media / mediana del tiempo en ms): Esqueumórfico 649 / 537 · Neumórfico 684 / 484 ·
  Plano 828 / 607. **Todas** las tareas tienen 1 clic y éxito = 1 (efecto techo: solo el tiempo discrimina).

## 2. `csv_evaluacion_andenes/` — Prototipo propio del equipo («Identificar andén»)

- 3 archivos `Lab07EqA_IHC_evaluacion_p1.csv` … `p3.csv` → **3 participantes × 10 ensayos = 30 filas**.
- Columnas: `participante, ensayo, tarea, evento, and_correcto, and_seleccionado, tiempo_ms, clics, exito, fecha`.
- La tarea consiste en elegir el andén (A, B o C) que corresponde a un evento académico.
- Tasa de éxito global: **33,3 %**, igual al azar con tres opciones (p1 30 %, p2 40 %, p3 30 %).
- **Pendiente:** el HTML de este prototipo no venía en el .zip.
