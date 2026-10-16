"""Paso 4 — Construye el notebook mejorado y extendido del Ejercicio 6.3b (Equipo A).

Parte del notebook del docente (insumos/ejercicio_6_3_analisis_metaforas.ipynb): conserva su flujo
(carga → resumen por estilo → barras de tiempo y clics → tabla e interpretación) y lo extiende con
validación de datos, estadística descriptiva completa, más gráficos, pruebas para medidas repetidas
(Friedman, Wilcoxon con corrección de Holm, ANOVA de medidas repetidas sobre log-tiempo), análisis de
sensibilidad e interpretación automática. Los 30 registros reales se incrustan en la celda de carga
para que «Ejecutar todas» funcione en Colab sin subir archivos.
Uso: python construir_notebook.py   →  L4_paso_a_paso/paso4_python/Lab06_ejercicio_6_3b_analisis_EquipoA.ipynb
"""
from pathlib import Path

import nbformat as nbf

RAIZ = Path(__file__).resolve().parents[2]
ORIGINAL = RAIZ / "insumos" / "ejercicio_6_3_analisis_metaforas.ipynb"
CSV = RAIZ / "L4_paso_a_paso" / "paso3_medicion" / "resultados_6_3_consolidado.csv"
SALIDA = RAIZ / "L4_paso_a_paso" / "paso4_python" / "Lab06_ejercicio_6_3b_analisis_EquipoA.ipynb"
CONCLUSIONES = Path(__file__).resolve().parent / "conclusiones.md"

orig = nbf.read(ORIGINAL, as_version=4)
csv_texto = CSV.read_text(encoding="utf-8-sig").strip()
celdas = []
md = lambda t: celdas.append(nbf.v4.new_markdown_cell(t.strip("\n")))
code = lambda t: celdas.append(nbf.v4.new_code_cell(t.strip("\n")))

# ------------------------------------------------------------------ portada
md("""
# Ejercicio 6.3b — Análisis de la efectividad de metáforas visuales (versión mejorada y extendida)

| | |
|---|---|
| **Curso** | Interacción Hombre-Computador (202W0606) · Semestre 2026-2 · Laboratorio 6 |
| **Docente** | Mg. Ing. Ernesto D. Cancho-Rodríguez, MBA (GWU) |
| **Equipo** | Equipo A — Arboleda Sánchez, Ericka Sofía · Cabrejos Palomino, Christian Daniel · Ccoicca Fernández, Adrián · Cerna Sifuentes, Augusto Nicolás · Grijalva De La Cruz, Rony Smith · Martines Cancho, Josué · Postigo Vega, Diana Carolina · Siesquen Torres, Katherine Lizbeth · Tecsi Alanoca, Jean Carlo · Tonconi Isidro, María Sunori · Villegas Niño, Marco Antonio |
| **Universidad** | Universidad Nacional Mayor de San Marcos · FISI |
| **Fecha** | Lima, 16 de octubre de 2026 |

**Base:** notebook del docente `ejercicio_6_3_analisis_metaforas.ipynb`. Se conserva su flujo y se marcan con ✏️ las
mejoras y extensiones del equipo.

**Datos:** 30 registros reales (5 participantes × 6 tareas) registrados por el equipo con el Ejercicio 6.3 el
16/10/2026: tiempo en tarea (`performance.now()`), clics en el área de la tarea y éxito. Los registros se incrustan en
la celda de carga para que **Entorno de ejecución → Ejecutar todas** funcione sin subir archivos.

**Diseño del estudio:** intra-sujeto (medidas repetidas). Cada participante usó los tres estilos en dos tipos de tarea;
por eso las pruebas de comparación deben ser para muestras relacionadas (✏️ Friedman y Wilcoxon), no para muestras
independientes.
""")
md(orig.cells[0].source)

# ------------------------------------------------------------------ celda 1
md("""
## 1. Librerías y estilo de las gráficas

Celda 1 del docente. ✏️ Se agregan `numpy`, `scipy.stats` y `statsmodels` (incluidos en Colab) para las pruebas
estadísticas, y el tema oscuro se reemplaza por uno claro y sobrio, legible al imprimir el informe.
""")
code("""
# =========================================================
# Celda 1 — Importación de librerías y estilo (docente + ✏️ equipo)
# =========================================================
import io, os, warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from statistics import mean, median, stdev
from scipy import stats                                  # ✏️ pruebas estadísticas
from statsmodels.stats.anova import AnovaRM              # ✏️ ANOVA de medidas repetidas
warnings.filterwarnings("ignore", category=UserWarning)

# ✏️ Tema claro y sobrio (para impresión); el docente usaba fondo oscuro #0F172A
plt.rcParams.update({
    "figure.facecolor": "white", "axes.facecolor": "white", "axes.edgecolor": "#333333",
    "axes.labelcolor": "#111111", "text.color": "#111111", "xtick.color": "#333333",
    "ytick.color": "#333333", "grid.color": "#DDDDDD", "font.family": "sans-serif",
    "font.size": 11, "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 110,
})
ORDEN = ["Esqueumórfico", "Plano", "Neumórfico"]
COLORES = {"Esqueumórfico": "#3A3A3A", "Plano": "#6E8FB5", "Neumórfico": "#B5B5B5"}
os.makedirs("figuras", exist_ok=True)
print("Librerías cargadas correctamente.")
""")

# ------------------------------------------------------------------ celda 2
md("""
## 2. Carga de los datos reales

El docente pedía subir el CSV con `files.upload()`, lo que detiene «Ejecutar todas». ✏️ Ahora los 30 registros
consolidados (`resultados_6_3_consolidado.csv`, Paso 3) están incrustados en la celda. La opción de subir un CSV
nuevo se conserva comentada.
""")
code(f'''
# =========================================================
# Celda 2 — Carga del CSV (✏️ datos reales incrustados)
# Fuente: 5 archivos resultados_metaforas_p1..p5.csv del Ejercicio 6.3
# =========================================================
CSV_REAL = """{csv_texto}"""
df = pd.read_csv(io.StringIO(CSV_REAL))

# Opción del docente: subir otro CSV desde el disco (descomentar en Colab)
# from google.colab import files
# subido = files.upload()
# df = pd.read_csv(list(subido.keys())[0])

df["estilo"] = pd.Categorical(df["estilo"], categories=ORDEN, ordered=True)
print(f"Registros: {{len(df)}} · Participantes: {{df['participante'].nunique()}} · Columnas: {{list(df.columns)}}")
df.head(8)
''')

# ------------------------------------------------------------------ validación
md("""
## 3. ✏️ Validación de los datos

Antes de analizar se comprueba que no falten valores, que cada participante tenga sus 6 tareas y que los rangos sean
válidos. Se revisa también la variabilidad de clics y éxito: si no varían, no pueden diferenciar estilos.
""")
code("""
# =========================================================
# ✏️ Celda 3 — Calidad de los datos
# =========================================================
print("Valores faltantes por columna:", df.isna().sum().to_dict())
print("Tareas por participante:", df.groupby("participante")["tarea"].count().to_dict())
print("Diseño completo (cada participante × estilo × tarea):",
      df.groupby(["participante", "estilo", "tipo_tarea"], observed=True).size().eq(1).all())
print(f"Tiempo: mín. {df.tiempo_ms.min()} ms · máx. {df.tiempo_ms.max()} ms")
print("Valores distintos de clics:", sorted(df.clics.unique()), "· de éxito:", sorted(df.exito.unique()))
if df.clics.nunique() == 1 and df.exito.nunique() == 1:
    print("→ Efecto techo: todos los registros tienen el mismo número de clics y éxito; solo el tiempo discrimina.")
""")

# ------------------------------------------------------------------ celda 3 docente
md("""
## 4. Estadísticas descriptivas por estilo

Celda 3 del docente (media, mediana, clics y tasa de éxito). ✏️ Se añaden desviación estándar, mínimo, máximo,
coeficiente de variación e intervalo de confianza del 95 % de la media (distribución *t*).
""")
code("""
# =========================================================
# Celda 4 — Resumen por estilo (docente) + ✏️ dispersión e IC 95 %
# =========================================================
def ic95(x):
    x = np.asarray(x, dtype=float)
    m, se = x.mean(), stats.sem(x)
    h = se * stats.t.ppf(0.975, len(x) - 1)
    return m - h, m + h

resumen = df.groupby("estilo", observed=True).agg(
    n=("tiempo_ms", "size"),
    tiempo_medio_ms=("tiempo_ms", "mean"),
    tiempo_mediana_ms=("tiempo_ms", "median"),
    tiempo_de_ms=("tiempo_ms", "std"),
    tiempo_min_ms=("tiempo_ms", "min"),
    tiempo_max_ms=("tiempo_ms", "max"),
    clics_medio=("clics", "mean"),
    tasa_exito=("exito", "mean"),
)
resumen["cv_pct"] = resumen["tiempo_de_ms"] / resumen["tiempo_medio_ms"] * 100
resumen[["ic95_inf_ms", "ic95_sup_ms"]] = [ic95(df.loc[df.estilo == e, "tiempo_ms"]) for e in resumen.index]
resumen["tasa_exito_pct"] = resumen["tasa_exito"] * 100
resumen = resumen.round(1)
print("Resumen estadístico por estilo de metáfora visual:")
resumen
""")

md("""
### 4.1 ✏️ Por tipo de tarea y por participante

La media global puede ocultar diferencias entre tareas o el peso de un participante atípico.
""")
code("""
# =========================================================
# ✏️ Celda 5 — Resumen por tipo de tarea × estilo y por participante
# =========================================================
por_tarea = df.pivot_table(index="tipo_tarea", columns="estilo", values="tiempo_ms",
                           aggfunc=["mean", "median"], observed=True).round(1)
por_participante = df.pivot_table(index="participante", columns="estilo", values="tiempo_ms",
                                  aggfunc="mean", observed=True).round(1)
por_participante["media_global"] = df.groupby("participante")["tiempo_ms"].mean().round(1)
z = (por_participante["media_global"] - por_participante["media_global"].mean()) / por_participante["media_global"].std()
por_participante["z_media"] = z.round(2)
display(por_tarea)
display(por_participante)
atipico = por_participante.index[por_participante["z_media"].abs() > 1.5].tolist()
print("Participantes con media alejada (|z| > 1.5):", atipico or "ninguno")
""")

# ------------------------------------------------------------------ celdas 4-5 docente
md("""
## 5. Gráficos del docente: tiempo medio y clics medios por estilo

Celdas 4 y 5 del docente. ✏️ Se agregan barras de error con el IC 95 % para mostrar la incertidumbre de cada media.
""")
code("""
# =========================================================
# Celda 6 — Tiempo medio por estilo con IC 95 % (docente + ✏️ barras de error)
# =========================================================
fig, ax = plt.subplots(figsize=(8, 5))
estilos = resumen.index.tolist()
tiempos = resumen["tiempo_medio_ms"].tolist()
err = [np.array(tiempos) - resumen["ic95_inf_ms"].values, resumen["ic95_sup_ms"].values - np.array(tiempos)]
bars = ax.bar(estilos, tiempos, color=[COLORES[e] for e in estilos], edgecolor="#111111", linewidth=0.6,
              width=0.55, yerr=err, capsize=6, error_kw={"elinewidth": 1, "ecolor": "#111111"})
for bar, val in zip(bars, tiempos):
    ax.text(bar.get_x() + bar.get_width() / 2, 40, f"{val:.0f} ms", ha="center", va="bottom",
            fontweight="bold", color="white" if bar.get_facecolor()[0] < 0.6 else "black")
ax.set_axisbelow(True)
ax.set_ylabel("Tiempo medio en tarea (ms)")
ax.set_title("Figura 1. Tiempo medio en tarea por estilo (IC 95 %)", loc="left", fontsize=12)
ax.grid(axis="y", alpha=0.6)
plt.tight_layout(); plt.savefig("figuras/fig1_tiempo_medio_ic95.png", dpi=200, bbox_inches="tight"); plt.show()
""")
code("""
# =========================================================
# Celda 7 — Clics medios y tasa de éxito por estilo (docente + ✏️ éxito)
# =========================================================
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
for ax, col, titulo, fmt in [(axes[0], "clics_medio", "Clics medios por tarea", "{:.1f}"),
                             (axes[1], "tasa_exito_pct", "Tasa de éxito (%)", "{:.0f} %")]:
    vals = resumen[col].tolist()
    b = ax.bar(estilos, vals, color=[COLORES[e] for e in estilos], edgecolor="#111111", linewidth=0.6, width=0.55)
    for bar, v in zip(b, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, v, fmt.format(v), ha="center", va="bottom", fontweight="bold")
    ax.set_title(titulo, loc="left"); ax.set_ylim(0, max(vals) * 1.25); ax.grid(axis="y", alpha=0.6)
fig.suptitle("Figura 2. Clics y éxito por estilo: sin variación (efecto techo)", x=0.01, ha="left", fontsize=12)
plt.tight_layout(); plt.savefig("figuras/fig2_clics_exito.png", dpi=200, bbox_inches="tight"); plt.show()
""")

# ------------------------------------------------------------------ nuevos gráficos
md("""
## 6. ✏️ Distribución y efecto de cada participante

Las medias se ven muy afectadas por valores extremos. El diagrama de caja muestra la mediana y la dispersión, y el
gráfico por participante muestra si las diferencias son consistentes dentro de cada persona (lo que importa en un
diseño intra-sujeto).
""")
code("""
# =========================================================
# ✏️ Celda 8 — Diagrama de caja con puntos y gráfico por participante
# =========================================================
fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))
datos = [df.loc[df.estilo == e, "tiempo_ms"].values for e in ORDEN]
bp = axes[0].boxplot(datos, tick_labels=ORDEN, patch_artist=True, widths=0.5, showfliers=False,
                     medianprops={"color": "black", "linewidth": 2})  # los puntos individuales se dibujan aparte
for caja, e in zip(bp["boxes"], ORDEN):
    caja.set_facecolor(COLORES[e]); caja.set_alpha(0.55)
rng = np.random.default_rng(6)
for i, e in enumerate(ORDEN, 1):
    sub = df[df.estilo == e]
    axes[0].scatter(i + rng.uniform(-0.12, 0.12, len(sub)), sub.tiempo_ms, s=22, color="black", zorder=3,
                    marker="o")
axes[0].set_ylabel("Tiempo en tarea (ms)"); axes[0].set_title("a) Distribución por estilo", loc="left")
axes[0].grid(axis="y", alpha=0.6)

marcas = dict(zip(sorted(df.participante.unique()), ["o", "s", "^", "D", "v"]))
for p, sub in df.groupby("participante"):
    m = sub.groupby("estilo", observed=True)["tiempo_ms"].mean().reindex(ORDEN)
    axes[1].plot(ORDEN, m.values, marker=marcas[p], color="#555555" if p != "p1" else "black",
                 linewidth=2.2 if p == "p1" else 1.2, label=p)
axes[1].set_ylabel("Tiempo medio del participante (ms)")
axes[1].set_title("b) Cada participante en los tres estilos", loc="left")
axes[1].legend(title="Participante", frameon=False, ncols=5, loc="upper center", bbox_to_anchor=(0.5, -0.12))
axes[1].grid(axis="y", alpha=0.6)
fig.suptitle("Figura 3. Distribución del tiempo y perfil por participante", x=0.01, ha="left", fontsize=12)
plt.tight_layout(); plt.savefig("figuras/fig3_caja_y_participantes.png", dpi=200, bbox_inches="tight"); plt.show()
""")
code("""
# =========================================================
# ✏️ Celda 9 — Tiempo por tipo de tarea y estilo (mediana)
# =========================================================
med = df.pivot_table(index="tipo_tarea", columns="estilo", values="tiempo_ms", aggfunc="median", observed=True)[ORDEN]
fig, ax = plt.subplots(figsize=(8.5, 4.5))
x = np.arange(len(med.index)); w = 0.26
for i, e in enumerate(ORDEN):
    b = ax.bar(x + (i - 1) * w, med[e], w, label=e, color=COLORES[e], edgecolor="#111111", linewidth=0.6)
    ax.bar_label(b, fmt="%.0f", fontsize=9, padding=2)
ax.set_xticks(x, med.index); ax.set_ylabel("Mediana del tiempo (ms)")
ax.set_title("Figura 4. Mediana del tiempo por tipo de tarea y estilo", loc="left", fontsize=12)
ax.legend(frameon=False, ncols=3, loc="upper center", bbox_to_anchor=(0.5, -0.1)); ax.grid(axis="y", alpha=0.6)
plt.tight_layout(); plt.savefig("figuras/fig4_mediana_tarea_estilo.png", dpi=200, bbox_inches="tight"); plt.show()
""")

# ------------------------------------------------------------------ inferencia
md("""
## 7. ✏️ Pruebas estadísticas para medidas repetidas

El docente sugiere ANOVA o Kruskal-Wallis «en un estudio con 5+ participantes». Como cada participante usó los tres
estilos, las observaciones **no son independientes**; las pruebas adecuadas son:

- **Shapiro-Wilk** para ver si el tiempo se distribuye normalmente (decide entre pruebas paramétricas y no paramétricas).
- **Friedman** (no paramétrica, medidas repetidas) con **W de Kendall** como tamaño del efecto: sobre 5 bloques
  (participante, promedio de las dos tareas) y sobre 10 bloques (participante × tipo de tarea).
- **Wilcoxon de rangos con signo** por pares, con corrección de **Holm** por comparaciones múltiples.
- **ANOVA de medidas repetidas** (estilo × tipo de tarea) sobre el logaritmo del tiempo, que corrige la asimetría.
- **Kruskal-Wallis** solo como referencia, para mostrar qué pasaría si se ignorara el diseño intra-sujeto.

Nivel de significación: α = 0,05.
""")
code("""
# =========================================================
# ✏️ Celda 10 — Normalidad (Shapiro-Wilk) del tiempo y del log-tiempo
# =========================================================
filas = []
for e in ORDEN:
    x = df.loc[df.estilo == e, "tiempo_ms"]
    w1, p1 = stats.shapiro(x); w2, p2 = stats.shapiro(np.log(x))
    filas.append({"estilo": e, "W_tiempo": w1, "p_tiempo": p1, "W_log": w2, "p_log": p2})
normalidad = pd.DataFrame(filas).set_index("estilo").round(3)
display(normalidad)
no_normales = normalidad.index[normalidad.p_tiempo < 0.05].tolist()
print("Estilos sin normalidad en el tiempo (p < 0,05):", no_normales or "ninguno",
      "→ se priorizan pruebas no paramétricas." if no_normales else "")
""")
code("""
# =========================================================
# ✏️ Celda 11 — Friedman + W de Kendall (5 y 10 bloques)
# =========================================================
def friedman(tabla, nombre):
    chi2, p = stats.friedmanchisquare(*[tabla[e] for e in ORDEN])
    n, k = tabla.shape
    w = chi2 / (n * (k - 1))
    rangos = tabla[ORDEN].rank(axis=1).mean().round(2).to_dict()
    return {"análisis": nombre, "bloques": n, "chi2": round(chi2, 3), "gl": k - 1, "p": round(p, 4),
            "W_Kendall": round(w, 3), "rango_medio": rangos}

bloques5 = df.pivot_table(index="participante", columns="estilo", values="tiempo_ms", aggfunc="mean", observed=True)[ORDEN]
bloques10 = df.pivot_table(index=["participante", "tipo_tarea"], columns="estilo", values="tiempo_ms", observed=True)[ORDEN]
sin_p1 = bloques10.drop(index="p1", level="participante")
pruebas_friedman = pd.DataFrame([
    friedman(bloques5, "Participante (media de 2 tareas)"),
    friedman(bloques10, "Participante × tipo de tarea"),
    friedman(sin_p1, "Participante × tarea, sin p1 (sensibilidad)"),
])
pruebas_friedman
""")
code("""
# =========================================================
# ✏️ Celda 12 — Wilcoxon por pares (10 bloques) con corrección de Holm
# =========================================================
pares = [("Esqueumórfico", "Plano"), ("Esqueumórfico", "Neumórfico"), ("Plano", "Neumórfico")]
filas = []
for a, b in pares:
    dif = bloques10[a] - bloques10[b]
    res = stats.wilcoxon(bloques10[a], bloques10[b])
    filas.append({"comparación": f"{a} vs. {b}", "mediana_dif_ms": round(dif.median(), 1),
                  "a_más_rápido_en": f"{(dif < 0).sum()}/10", "W": res.statistic, "p": res.pvalue})
wil = pd.DataFrame(filas).sort_values("p").reset_index(drop=True)
m = len(wil)
wil["p_Holm"] = np.minimum(1, np.maximum.accumulate([(m - i) * p for i, p in enumerate(wil["p"])])).round(4)
wil["p"] = wil["p"].round(4)
wil
""")
code("""
# =========================================================
# ✏️ Celda 13 — ANOVA de medidas repetidas (estilo × tipo de tarea) sobre log(tiempo)
# =========================================================
df["log_tiempo"] = np.log(df["tiempo_ms"])
anova = AnovaRM(df.assign(estilo=df.estilo.astype(str)), depvar="log_tiempo", subject="participante",
                within=["estilo", "tipo_tarea"]).fit()
tabla_anova = anova.anova_table.round(4)
# Eta cuadrado parcial: F·gl1 / (F·gl1 + gl2)
tabla_anova["eta2_parcial"] = (tabla_anova["F Value"] * tabla_anova["Num DF"] /
                               (tabla_anova["F Value"] * tabla_anova["Num DF"] + tabla_anova["Den DF"])).round(3)
tabla_anova
""")
code("""
# =========================================================
# ✏️ Celda 14 — Referencia: Kruskal-Wallis (supone grupos independientes)
# =========================================================
h, p_kw = stats.kruskal(*[df.loc[df.estilo == e, "tiempo_ms"] for e in ORDEN])
print(f"Kruskal-Wallis: H = {h:.3f}, p = {p_kw:.4f}")
print("Nota: esta prueba ignora que las mismas personas usaron los tres estilos; se muestra solo para comparar.")
""")

# ------------------------------------------------------------------ celda 6 docente + interpretación
md("""
## 8. Tabla resumen e interpretación

Celda 6 del docente (tabla e interpretación automática). ✏️ La interpretación ahora se basa en las pruebas
estadísticas, el tamaño del efecto y el análisis de sensibilidad, no solo en qué media es menor.
""")
code("""
# =========================================================
# Celda 15 — Tabla resumen (docente) + ✏️ interpretación basada en pruebas
# =========================================================
print("TABLA RESUMEN — EFECTIVIDAD DE METÁFORAS VISUALES")
print("=" * 78)
print(f"{'Estilo':<16}{'Media (ms)':>12}{'Mediana (ms)':>14}{'DE (ms)':>10}{'Clics':>8}{'Éxito (%)':>11}")
print("-" * 78)
for e in ORDEN:
    f = resumen.loc[e]
    print(f"{e:<16}{f.tiempo_medio_ms:>12.0f}{f.tiempo_mediana_ms:>14.0f}{f.tiempo_de_ms:>10.0f}{f.clics_medio:>8.1f}{f.tasa_exito_pct:>11.0f}")
print("=" * 78)

fr10 = pruebas_friedman.iloc[1]; fr_sin = pruebas_friedman.iloc[2]
p_estilo = tabla_anova.loc["estilo", "Pr > F"]
mejor_media = resumen["tiempo_medio_ms"].idxmin(); mejor_mediana = resumen["tiempo_mediana_ms"].idxmin()
peor_media = resumen["tiempo_medio_ms"].idxmax()
fuerza = lambda w: "pequeño" if w < 0.3 else "moderado" if w < 0.5 else "grande"
print()
print("INTERPRETACIÓN (generada a partir de los datos):")
print(f"- Menor tiempo medio: {mejor_media}; menor mediana: {mejor_mediana}; mayor tiempo medio: {peor_media}.")
print(f"- Friedman (10 bloques): χ²({fr10.gl}) = {fr10.chi2}, p = {fr10.p}, W de Kendall = {fr10.W_Kendall} (efecto {fuerza(fr10.W_Kendall)}).")
print(f"  Rango medio: {fr10.rango_medio}.")
print(f"- ANOVA de medidas repetidas sobre log-tiempo, factor estilo: p = {p_estilo:.4f}.")
sig = fr10.p < 0.05 or p_estilo < 0.05
if sig:
    print("- Hay evidencia estadística de diferencias entre estilos (α = 0,05).")
else:
    print("- No hay evidencia estadística suficiente de que los estilos difieran en tiempo (α = 0,05).")
print(f"- Sin el participante p1, Friedman da p = {fr_sin.p} (W = {fr_sin.W_Kendall}).")
print(f"- Wilcoxon con Holm: p corregidas = {dict(zip(wil['comparación'], wil['p_Holm']))}.")
print("- Clics (1,0) y éxito (100 %) no varían: las tareas son demasiado fáciles para medir esfuerzo o errores.")
print()
print("DISCUSIÓN DE USABILIDAD:")
print("- La guía (Pregunta 3) espera que el neumorfismo sea más lento por su baja affordance; con estas tareas")
print("  sencillas y rotuladas esa diferencia no aparece. Para observarla habría que aumentar la dificultad")
print("  (varias opciones, controles sin rótulo) y contrabalancear el orden de los estilos.")
""")

# ------------------------------------------------------------------ exportación
md("""
## 9. ✏️ Exportación de resultados

Se guardan las tablas en CSV para el informe y las figuras en la carpeta `figuras/`.
""")
code("""
# =========================================================
# ✏️ Celda 16 — Exportar tablas
# =========================================================
os.makedirs("resultados", exist_ok=True)
resumen.to_csv("resultados/resumen_por_estilo.csv", encoding="utf-8-sig")
por_participante.to_csv("resultados/resumen_por_participante.csv", encoding="utf-8-sig")
normalidad.to_csv("resultados/normalidad_shapiro.csv", encoding="utf-8-sig")
pruebas_friedman.to_csv("resultados/friedman.csv", index=False, encoding="utf-8-sig")
wil.to_csv("resultados/wilcoxon_holm.csv", index=False, encoding="utf-8-sig")
tabla_anova.to_csv("resultados/anova_rm_log.csv", encoding="utf-8-sig")
print("Tablas guardadas en resultados/ y figuras en figuras/:", sorted(os.listdir("figuras")))
""")

if CONCLUSIONES.exists():
    md(CONCLUSIONES.read_text(encoding="utf-8"))
md("""
---
**Equipo A — IHC · UNMSM · 2026-2.** Notebook base: Prof. E. D. Cancho-Rodríguez, MBA (GWU). Extensiones (✏️) del
Equipo A con asistencia de IA (Claude, Anthropic), revisadas por el equipo.
""")

nb = nbf.v4.new_notebook()
nb.cells = celdas
nb.metadata = {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
               "language_info": {"name": "python"}, "colab": {"provenance": []}}
SALIDA.parent.mkdir(parents=True, exist_ok=True)
nbf.write(nb, SALIDA)
print(f"Notebook generado: {SALIDA.name} ({len(celdas)} celdas)")
