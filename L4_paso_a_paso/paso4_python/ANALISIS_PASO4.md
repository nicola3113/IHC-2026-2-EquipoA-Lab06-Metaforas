# Paso 4 — Análisis en Python (Ejercicio 6.3b): notebook mejorado, ejecución en Colab y EDA

Equipo A · IHC 2026-2 · 16 de octubre de 2026

## 1. Evidencia de la realización

| Archivo | Contenido |
|---|---|
| `Lab06_ejercicio_6_3b_analisis_EquipoA.ipynb` | Notebook mejorado y extendido, **ejecutado en Google Colab** (16 celdas de código, 0 errores) y descargado de Drive |
| `Lab06_ejercicio_6_3b_analisis_EquipoA.html` | El mismo notebook en HTML, para leerlo sin Colab |
| `capturas/colab_01…06_*.jpg` | Ejecución en Colab: validación, resumen por estilo, Figura 3, Friedman y Wilcoxon, ANOVA y Kruskal-Wallis, interpretación |
| `figuras/fig1…fig4_*.png` | Figuras exportadas por el notebook (200 ppp) |
| `resultados/*.csv` | Tablas exportadas: resumen por estilo y por participante, Shapiro-Wilk, Friedman, Wilcoxon-Holm y ANOVA |
| `../paso3_medicion/resultados_6_3_EquipoA.xlsx` | Los CSV del experimento convertidos a Excel con «Tabla con formato» (Paso 3) |

El notebook se genera con `build/paso4/construir_notebook.py` a partir del notebook del docente y se subió a Colab
con *Archivo → Subir cuaderno*; se ejecutó con *Entorno de ejecución → Ejecutar todas* (Python 3, sin GPU).

## 2. Mejoras y extensiones respecto al notebook del docente

| # | Notebook del docente | Versión del Equipo A |
|---|---|---|
| 1 | Carga con `files.upload()`, que detiene «Ejecutar todas» | Los 30 registros reales incrustados; la subida manual queda como opción comentada |
| 2 | Sin validación | Faltantes, diseño completo (participante × estilo × tarea), rangos y detección del efecto techo |
| 3 | Media, mediana, clics y éxito | Además DE, mínimo, máximo, coeficiente de variación e IC 95 % de la media |
| 4 | — | Resumen por tipo de tarea y por participante, con detección de atípicos (z) |
| 5 | Barras de tiempo y clics (tema oscuro) | Barras con IC 95 %, clics y éxito, diagrama de caja con puntos, perfil por participante y mediana por tarea; tema claro para impresión |
| 6 | Sugiere ANOVA o Kruskal-Wallis | Pruebas para **medidas repetidas**: Shapiro-Wilk, Friedman con W de Kendall, Wilcoxon con corrección de Holm y ANOVA de medidas repetidas (estilo × tarea) sobre log-tiempo; Kruskal-Wallis solo como referencia |
| 7 | — | Análisis de sensibilidad sin el participante atípico |
| 8 | Interpretación basada en la media menor | Interpretación generada a partir de las pruebas, el tamaño del efecto y la sensibilidad |
| 9 | Guarda 2 PNG | Exporta 4 figuras y 6 tablas CSV |

## 3. Resultados del EDA

**Descriptivo.** Media / mediana (ms): esqueumórfico 649 / 537 · plano 828 / 607 · neumórfico 684 / 484. Los
coeficientes de variación van de 50 % a 76 % y los IC 95 % de las tres medias se solapan casi por completo
(Figura 1). Clics = 1 y éxito = 100 % en los 30 registros (Figura 2, efecto techo).

**Participante atípico.** p1 tiene una media de 1438 ms (z = 1,72) y aporta el máximo de cada estilo (Figura 3b).

**Normalidad.** Shapiro-Wilk rechaza la normalidad del tiempo en los tres estilos (p = 0,011; 0,010; 0,001); el
logaritmo la corrige (p ≥ 0,05), lo que justifica el ANOVA sobre log-tiempo y las pruebas no paramétricas.

**Pruebas (α = 0,05):**

| Prueba | Resultado | Conclusión |
|---|---|---|
| Friedman, 5 bloques (participante) | χ²(2) = 0,0; p = 1,00; W = 0,00 | Sin diferencias |
| Friedman, 10 bloques (participante × tarea) | χ²(2) = 2,6; p = 0,27; W = 0,13 (pequeño) | Sin diferencias |
| Friedman sin p1 (8 bloques) | χ²(2) = 1,0; p = 0,61; W = 0,06 | Sin diferencias |
| Wilcoxon con Holm | Esq. vs. plano p = 0,48 · plano vs. neu. p = 0,48 · esq. vs. neu. p = 0,92 | Ningún par difiere |
| ANOVA de medidas repetidas (log-tiempo) | Estilo F(2, 8) = 0,69, p = 0,53, η²p = 0,15 · tarea p = 0,55 · interacción p = 0,63 | Sin efectos |
| Kruskal-Wallis (referencia, ignora el diseño) | H = 0,20; p = 0,90 | — |

## 4. Interpretación

1. **No hay evidencia estadística de que el estilo visual cambie el tiempo en tarea** en este experimento. La
   ventaja aparente del esqueumórfico sobre el plano (179 ms en la media) se explica sobre todo por p1 y desaparece
   en las pruebas robustas.
2. **El tamaño del efecto es pequeño** (W = 0,13): aunque hubiera más participantes, la diferencia esperada sería
   modesta con tareas tan simples.
3. **La hipótesis de la guía (neumorfismo más lento, Pregunta 3) no se confirma**, pero tampoco se refuta: el
   efecto techo en clics y éxito, el orden fijo de presentación y n = 5 dejan al estudio con poca potencia. Esto
   concuerda con el Paso 2: el neumorfismo tiene peor contraste, pero en una tarea rotulada con un solo control el
   usuario igual lo encuentra.
4. **Lección metodológica.** En un diseño intra-sujeto, elegir la prueba correcta importa: Kruskal-Wallis
   (p = 0,90) trata como independientes datos que no lo son; Friedman y el ANOVA de medidas repetidas usan a cada
   participante como su propio control.

## 5. Recomendaciones

Repetir con al menos 10 participantes, orden contrabalanceado (cuadrado latino 3 × 3), pantallas con varias
opciones y controles sin rótulo, y tiempo medido hasta el clic correcto. Estas recomendaciones se aplican al diseño
del experimento de la metáfora propia (L.5).
