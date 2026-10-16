"""L.5 — Consolida los CSV de la evaluación del huerto, genera el Excel y el notebook de análisis.

Entrada : L5_metafora_propia/datos/csv_participantes/L5_huerto_p*.csv (se descartan los archivos *_PRUEBA.csv
          y las filas con modo = PRUEBA)
Salida  : L5_metafora_propia/datos/L5_huerto_consolidado.csv
          L5_metafora_propia/datos/L5_huerto_EquipoA.xlsx          (tablas con formato)
          L5_metafora_propia/notebook/L5_analisis_huerto_EquipoA.ipynb (datos incrustados, listo para Colab)
Uso: python analizar_L5.py [--entrada CARPETA] [--salida CARPETA_L5] [--ejecutar]
     --ejecutar ejecuta el notebook localmente (nbconvert) y deja las figuras en notebook/figuras/.
"""
import argparse
import subprocess
import sys
from pathlib import Path

import nbformat as nbf
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

RAIZ = Path(__file__).resolve().parents[2]
ap = argparse.ArgumentParser()
ap.add_argument("--entrada", default=str(RAIZ / "L5_metafora_propia" / "datos" / "csv_participantes"))
ap.add_argument("--salida", default=str(RAIZ / "L5_metafora_propia"))
ap.add_argument("--ejecutar", action="store_true")
args = ap.parse_args()
ENTRADA, L5 = Path(args.entrada), Path(args.salida)

COLUMNAS = ["participante", "orden_vistas", "ensayo", "bloque", "condicion", "cartera", "tarea", "clave_tarea", "objetivo",
            "respuesta_final", "tiempo_ms", "clics", "errores", "exito", "seq", "navegador", "fecha", "modo"]
archivos = sorted(f for f in ENTRADA.glob("L5_huerto_*.csv") if "PRUEBA" not in f.name.upper())
if not archivos:
    sys.exit(f"No hay CSV reales en {ENTRADA}. Recoge los datos con el prototipo (ver INSTRUCCIONES_EVALUACION.md).")

# ------------------------------------------------------------------ validación
df = pd.concat([pd.read_csv(f, encoding="utf-8-sig").assign(archivo=f.name) for f in archivos], ignore_index=True)
faltan = [c for c in COLUMNAS if c not in df.columns]
assert not faltan, f"Columnas faltantes: {faltan}"
descartadas = int((df["modo"] != "real").sum())
df = df[df["modo"] == "real"].copy()
assert df.duplicated(["participante", "ensayo"]).sum() == 0, "Hay ensayos duplicados para un mismo participante"
completos = df.groupby("participante")["ensayo"].nunique()
incompletos = completos[completos != 10]
if len(incompletos):
    print("AVISO: participantes con sesión incompleta (se excluyen):", incompletos.to_dict())
    df = df[~df.participante.isin(incompletos.index)]
assert df.participante.nunique() >= 3, f"La guía exige al menos 3 participantes; hay {df.participante.nunique()}"
assert len(df) >= 30, f"La guía exige n ≥ 30; hay {len(df)} registros"
assert set(df.condicion) == {"huerto", "tabla"} and df.exito.isin([0, 1]).all() and df.seq.between(1, 7).all()
df = df.sort_values(["participante", "ensayo"])
datos = L5 / "datos"
datos.mkdir(parents=True, exist_ok=True)
df.drop(columns=["modo"]).to_csv(datos / "L5_huerto_consolidado.csv", index=False, encoding="utf-8-sig")

# ------------------------------------------------------------------ Excel con tablas con formato
ESTILO = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True)


def hoja(wb, nombre, d, tabla, titulo):
    ws = wb.create_sheet(nombre)
    ws["A1"] = titulo
    ws["A1"].font = Font(bold=True, size=12)
    for j, c in enumerate(d.columns, 1):
        ws.cell(row=3, column=j, value=str(c))
    for i, fila in enumerate(d.itertuples(index=False), 4):
        for j, v in enumerate(fila, 1):
            ws.cell(row=i, column=j, value=v.item() if hasattr(v, "item") else v)
    t = Table(displayName=tabla, ref=f"A3:{get_column_letter(len(d.columns))}{3 + len(d)}")
    t.tableStyleInfo = ESTILO
    ws.add_table(t)
    for j, c in enumerate(d.columns, 1):
        ws.column_dimensions[get_column_letter(j)].width = min(45, max(len(str(c)), *(len(str(v)) for v in d[c])) + 2)
    ws.freeze_panes = "A4"


resumen = df.groupby("condicion").agg(n=("tiempo_ms", "size"), tiempo_mediana_ms=("tiempo_ms", "median"),
                                      tiempo_media_ms=("tiempo_ms", "mean"), exito=("exito", "mean"),
                                      errores_media=("errores", "mean"), clics_media=("clics", "mean"),
                                      seq_media=("seq", "mean")).round(2).reset_index()
por_tarea = df.pivot_table(index=["tarea", "clave_tarea"], columns="condicion", values="tiempo_ms", aggfunc="median").round(0).reset_index()
por_tarea.columns = [str(c) if not isinstance(c, tuple) else c[0] for c in por_tarea.columns]
wb = Workbook()
wb.remove(wb.active)
hoja(wb, "Resumen", resumen, "TablaResumenL5", "Evaluación del huerto — resumen por condición")
hoja(wb, "Por_tarea", por_tarea, "TablaPorTareaL5", "Mediana del tiempo (ms) por tarea y condición")
hoja(wb, "Consolidado", df.drop(columns=["modo"]), "TablaConsolidadoL5",
     f"Registros reales consolidados ({df.participante.nunique()} participantes, {len(df)} registros)")
for p in sorted(df.participante.unique()):
    hoja(wb, p, df[df.participante == p].drop(columns=["modo"]), f"Tabla_L5_{p}", f"Participante {p}")
wb.save(datos / "L5_huerto_EquipoA.xlsx")

# ------------------------------------------------------------------ notebook
csv_texto = (datos / "L5_huerto_consolidado.csv").read_text(encoding="utf-8-sig").strip()
celdas = []
md = lambda t: celdas.append(nbf.v4.new_markdown_cell(t.strip("\n")))
code = lambda t: celdas.append(nbf.v4.new_code_cell(t.strip("\n")))
md(f"""
# L.5 — Análisis de la metáfora «El portafolio como huerto» (Ernesto Investing AI)

**Curso:** Interacción Hombre-Computador (202W0606) · 2026-2 · **Equipo A** · UNMSM — FISI

**Diseño:** intra-sujeto. Cada participante resolvió 5 tareas en la vista **huerto** (metáfora) y 5 en la vista
**tabla** (convencional), con orden de vistas y cartera contrabalanceados. Métricas: tiempo en tarea
(`performance.now()`), clics, errores, éxito y facilidad percibida (SEQ, 1–7).

**Datos:** {df.participante.nunique()} participantes, {len(df)} registros reales (incrustados en la celda 2).
""")
code("""
import io, os
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from scipy import stats
plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white", "axes.spines.top": False,
                     "axes.spines.right": False, "font.size": 11, "grid.color": "#DDDDDD", "figure.dpi": 110})
COND = ["huerto", "tabla"]; COLOR = {"huerto": "#3A6B35", "tabla": "#7A869A"}
os.makedirs("figuras", exist_ok=True)
""")
code(f'''
CSV_REAL = """{csv_texto}"""
df = pd.read_csv(io.StringIO(CSV_REAL))
print(f"{{len(df)}} registros · {{df.participante.nunique()}} participantes · columnas: {{list(df.columns)}}")
df.head()
''')
md("## 1. Estadística descriptiva por condición y por tarea")
code("""
res = df.groupby("condicion").agg(n=("tiempo_ms", "size"), tiempo_mediana_ms=("tiempo_ms", "median"),
        tiempo_media_ms=("tiempo_ms", "mean"), tiempo_de_ms=("tiempo_ms", "std"), exito_pct=("exito", "mean"),
        errores_media=("errores", "mean"), clics_media=("clics", "mean"), seq_media=("seq", "mean")).reindex(COND)
res["exito_pct"] *= 100
display(res.round(1))
display(df.pivot_table(index=["tarea", "clave_tarea"], columns="condicion", values="tiempo_ms", aggfunc="median").round(0))
display(df.groupby(["bloque", "condicion"])["tiempo_ms"].median().unstack().round(0).rename_axis("bloque (orden)"))
""")
md("## 2. Gráficos")
code("""
fig, ax = plt.subplots(1, 2, figsize=(12, 4.6))
datos = [df.loc[df.condicion == c, "tiempo_ms"] / 1000 for c in COND]
bp = ax[0].boxplot(datos, tick_labels=["Huerto (metáfora)", "Tabla (convencional)"], patch_artist=True,
                   showfliers=False, medianprops={"color": "black", "linewidth": 2}, widths=0.5)
for b, c in zip(bp["boxes"], COND): b.set_facecolor(COLOR[c]); b.set_alpha(0.45)
rng = np.random.default_rng(5)
for i, d in enumerate(datos, 1): ax[0].scatter(i + rng.uniform(-.1, .1, len(d)), d, s=16, color="black", zorder=3)
ax[0].set_ylabel("Tiempo en tarea (s)"); ax[0].set_title("a) Distribución del tiempo", loc="left"); ax[0].grid(axis="y")
med = df.pivot_table(index="tarea", columns="condicion", values="tiempo_ms", aggfunc="median")[COND] / 1000
x = np.arange(len(med)); w = .38
for k, c in enumerate(COND):
    ax[1].bar(x + (k - .5) * w, med[c], w, color=COLOR[c], label=c.capitalize(), edgecolor="black", linewidth=.5)
ax[1].set_xticks(x, [f"T{t}" for t in med.index]); ax[1].set_ylabel("Mediana (s)")
ax[1].set_title("b) Mediana por tarea", loc="left"); ax[1].legend(frameon=False); ax[1].grid(axis="y")
fig.suptitle("Figura 1. Tiempo en tarea: huerto frente a tabla", x=.01, ha="left")
plt.tight_layout(); plt.savefig("figuras/L5_fig1_tiempo.png", dpi=200, bbox_inches="tight"); plt.show()

fig, ax = plt.subplots(1, 3, figsize=(13, 4))
for a, col, tit, f in [(ax[0], "exito", "Éxito (%)", 100), (ax[1], "errores", "Errores por tarea", 1), (ax[2], "seq", "Facilidad SEQ (1–7)", 1)]:
    v = df.groupby("condicion")[col].mean().reindex(COND) * f
    b = a.bar(["Huerto", "Tabla"], v, color=[COLOR[c] for c in COND], edgecolor="black", linewidth=.5)
    a.bar_label(b, fmt="%.1f"); a.set_title(tit, loc="left"); a.grid(axis="y")
fig.suptitle("Figura 2. Eficacia, errores y facilidad percibida", x=.01, ha="left")
plt.tight_layout(); plt.savefig("figuras/L5_fig2_exito_errores_seq.png", dpi=200, bbox_inches="tight"); plt.show()

fig, ax = plt.subplots(figsize=(7, 4.4))
pp = df.groupby(["participante", "condicion"])["tiempo_ms"].median().unstack()[COND] / 1000
for p, fila in pp.iterrows(): ax.plot(["Huerto", "Tabla"], fila.values, marker="o", color="#555555")
ax.set_ylabel("Mediana del participante (s)"); ax.set_title("Figura 3. Cada participante en ambas vistas", loc="left"); ax.grid(axis="y")
plt.tight_layout(); plt.savefig("figuras/L5_fig3_participantes.png", dpi=200, bbox_inches="tight"); plt.show()
""")
md("""
## 3. Pruebas para muestras relacionadas

Pares = participante × tarea (la misma tarea en las dos vistas). Tiempo, errores y SEQ: **Wilcoxon de rangos con
signo** con tamaño del efecto *r* = |Z|/√N. Éxito: **McNemar exacto** (prueba binomial sobre los pares discordantes).
Orden: Wilcoxon entre el primer y el segundo bloque. α = 0,05.
""")
code("""
pares = df.pivot_table(index=["participante", "tarea"], columns="condicion", values=["tiempo_ms", "errores", "seq", "exito"])
filas = []
for m in ["tiempo_ms", "errores", "seq"]:
    a, b = pares[(m, "huerto")], pares[(m, "tabla")]
    dif = a - b
    if (dif != 0).sum() == 0:
        filas.append({"métrica": m, "N_pares": len(dif), "mediana_huerto": a.median(), "mediana_tabla": b.median(), "W": None, "p": 1.0, "r": 0.0}); continue
    w = stats.wilcoxon(a, b, zero_method="wilcox")
    z = stats.norm.isf(w.pvalue / 2)
    filas.append({"métrica": m, "N_pares": int((dif != 0).sum()), "mediana_huerto": a.median(), "mediana_tabla": b.median(),
                  "W": w.statistic, "p": w.pvalue, "r": z / np.sqrt((dif != 0).sum())})
eh, et = pares[("exito", "huerto")], pares[("exito", "tabla")]
b01, b10 = int(((eh == 0) & (et == 1)).sum()), int(((eh == 1) & (et == 0)).sum())
p_mc = stats.binomtest(b01, b01 + b10, 0.5).pvalue if b01 + b10 else 1.0
filas.append({"métrica": "exito (McNemar)", "N_pares": b01 + b10, "mediana_huerto": eh.mean(), "mediana_tabla": et.mean(), "W": None, "p": p_mc, "r": None})
orden = df.pivot_table(index=["participante", "tarea"], columns="bloque", values="tiempo_ms")
w_o = stats.wilcoxon(orden[1], orden[2])
filas.append({"métrica": "tiempo bloque 1 vs 2 (orden)", "N_pares": len(orden), "mediana_huerto": orden[1].median(), "mediana_tabla": orden[2].median(), "W": w_o.statistic, "p": w_o.pvalue, "r": None})
pruebas = pd.DataFrame(filas).round(4)
pruebas
""")
code("""
t = pruebas.set_index("métrica")
r_t = t.loc["tiempo_ms"]
mejor = "huerto" if r_t.mediana_huerto < r_t.mediana_tabla else "tabla"
print("INTERPRETACIÓN (generada a partir de los datos)")
print(f"- Tiempo: mediana huerto {r_t.mediana_huerto:.0f} ms vs. tabla {r_t.mediana_tabla:.0f} ms; Wilcoxon p = {r_t.p:.4f}, r = {r_t.r:.2f}.")
print(f"  → {'Diferencia significativa' if r_t.p < .05 else 'Sin diferencia significativa'} (α = 0,05); más rápida: vista {mejor}.")
print(f"- Errores: p = {t.loc['errores'].p:.4f} · SEQ: mediana huerto {t.loc['seq'].mediana_huerto:.1f} vs. tabla {t.loc['seq'].mediana_tabla:.1f}, p = {t.loc['seq'].p:.4f}.")
print(f"- Éxito: huerto {eh.mean()*100:.0f} % vs. tabla {et.mean()*100:.0f} %; McNemar p = {p_mc:.4f}.")
print(f"- Efecto de orden (bloque 1 vs. 2): p = {t.loc['tiempo bloque 1 vs 2 (orden)'].p:.4f}.")
os.makedirs("resultados", exist_ok=True); pruebas.to_csv("resultados/L5_pruebas.csv", index=False, encoding="utf-8-sig")
res.to_csv("resultados/L5_resumen_condicion.csv", encoding="utf-8-sig")
""")
nb = nbf.v4.new_notebook()
nb.cells = celdas
nb.metadata = {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python"}}
(L5 / "notebook").mkdir(parents=True, exist_ok=True)
ruta_nb = L5 / "notebook" / "L5_analisis_huerto_EquipoA.ipynb"
nbf.write(nb, ruta_nb)
print(f"Datos: {df.participante.nunique()} participantes, {len(df)} registros (filas de prueba descartadas: {descartadas}).")
print(resumen.to_string(index=False))
if args.ejecutar:
    subprocess.run([sys.executable, "-m", "jupyter", "nbconvert", "--to", "notebook", "--execute", "--inplace",
                    "--ExecutePreprocessor.timeout=180", str(ruta_nb)], check=True, cwd=ruta_nb.parent)
    print("Notebook ejecutado:", ruta_nb)
