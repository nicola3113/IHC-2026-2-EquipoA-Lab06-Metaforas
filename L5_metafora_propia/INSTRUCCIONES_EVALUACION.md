# Evaluación de la metáfora «El portafolio como huerto» — instrucciones para el equipo

La guía (L.5) exige evaluar el prototipo con **al menos 3 compañeros** y reunir **n ≥ 30 registros**. Cada
participante genera 10 registros (5 tareas × 2 vistas), así que con 3 participantes se llega a 30; con 4 o más el
análisis es más sólido y el contrabalanceo queda completo.

## Enlace del prototipo

https://nicola3113.github.io/IHC-2026-2-EquipoA-Lab06-Metaforas/L5_metafora_propia/prototipo/L5_huerto_inversiones_EquipoA.html

(También funciona abriendo el archivo `prototipo/L5_huerto_inversiones_EquipoA.html` sin conexión.)

## Protocolo (unos 3 minutos por persona)

1. Usa una computadora con ratón o panel táctil (no celular) y el navegador a pantalla completa.
2. Escribe el identificador **p1, p2, p3, p4…** (uno distinto por persona, en orden). El prototipo asigna solo el
   orden de las vistas y la cartera para contrabalancear:

   | Participante | 1.ª vista | 2.ª vista |
   |---|---|---|
   | p1, p5, p9… | Huerto (cartera A) | Tabla (cartera B) |
   | p2, p6… | Tabla (cartera A) | Huerto (cartera B) |
   | p3, p7… | Huerto (cartera B) | Tabla (cartera A) |
   | p4, p8… | Tabla (cartera B) | Huerto (cartera A) |

3. El participante lee las instrucciones y resuelve las tareas sin ayuda. El evaluador no indica respuestas.
4. Al terminar, pulsa **Descargar CSV** (se descarga `L5_huerto_pN.csv`) y luego **Siguiente participante**.
5. Envía los CSV al equipo. No mezcles sesiones de prueba: si el archivo termina en `_PRUEBA.csv`, no sirve.

## Qué se registra

`participante, orden_vistas, ensayo, bloque, condicion (huerto/tabla), cartera (A/B), tarea (1–5), clave_tarea,
objetivo, respuesta_final, tiempo_ms, clics, errores, exito, seq (facilidad 1–7), navegador, fecha, modo`.

Las 5 tareas de cada vista son: (1) sector con mayor peso, (2) activo con peor rendimiento, (3) activo de mayor
valor, (4) aportar S/ 500 a un activo indicado y (5) tomar ganancias del activo con mejor rendimiento.

## Después de recibir los CSV

Copiarlos en `L5_metafora_propia/datos/csv_participantes/` y ejecutar:

```
python build/paso_L5/analizar_L5.py
```

El script valida los archivos, genera el CSV consolidado, el Excel con tablas con formato y el notebook de análisis
con los datos incrustados (listo para Colab), y el informe L.5 se actualiza con los resultados.
