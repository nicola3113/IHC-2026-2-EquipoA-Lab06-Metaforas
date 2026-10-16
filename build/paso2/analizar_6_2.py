"""Paso 2 — Evidencia y análisis del Ejercicio 6.2 (esqueumorfismo vs. plano vs. neumorfismo).

1. Capturas de pantalla en Google Chrome: vista completa, cada componente, estados activados, tabla y métricas.
2. Interacción real con los 4 componentes de los 3 estilos y lectura del panel de métricas.
3. Auditoría de accesibilidad automática con axe-core (WCAG 2.x A/AA) sobre cada columna de estilo.
4. Medición del contraste WCAG 2.2 de texto (1.4.3) y de componentes no textuales (1.4.11) a partir del CSS.
Uso: python analizar_6_2.py   (requiere: pip install playwright · npm i axe-core en esta carpeta)
"""
import asyncio
import csv
import json
from pathlib import Path

from playwright.async_api import async_playwright

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]
PASO2 = RAIZ / "L4_paso_a_paso" / "paso2_estilos"
CAP = PASO2 / "capturas"
HTML = (RAIZ / "insumos" / "ejercicio_6_2_comparativa_estilos.html").as_uri()
AXE = (AQUI / "node_modules" / "axe-core" / "axe.min.js").read_text(encoding="utf-8")


# ---------------------------------------------------------------- contraste WCAG
def luminancia(hexa):
    hexa = hexa.lstrip("#")
    c = [int(hexa[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def razon(a, b):
    la, lb = sorted([luminancia(a), luminancia(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


# (estilo, componente, elemento, primer plano, fondo, tipo de requisito)
# Colores tomados del CSS del ejercicio; en degradados se usa el tono menos favorable.
PARES = [
    ("Esqueumórfico", "Botón", "Texto «Enviar»", "#333333", "#A0A0A0", "texto"),
    ("Esqueumórfico", "Botón", "Borde del botón frente a la columna", "#888888", "#1E293B", "no_texto"),
    ("Esqueumórfico", "Toggle", "Pista apagada frente a la columna", "#999999", "#1E293B", "no_texto"),
    ("Esqueumórfico", "Toggle", "Perilla frente a la pista apagada", "#F0F0F0", "#999999", "no_texto"),
    ("Esqueumórfico", "Slider", "Pista frente a la columna", "#888888", "#1E293B", "no_texto"),
    ("Esqueumórfico", "Tarjeta", "Título", "#333333", "#DDDDDD", "texto"),
    ("Esqueumórfico", "Tarjeta", "Párrafo", "#555555", "#DDDDDD", "texto"),
    ("Plano", "Botón", "Texto «Enviar»", "#FFFFFF", "#2563EB", "texto"),
    ("Plano", "Botón", "Botón frente a la columna", "#2563EB", "#1E293B", "no_texto"),
    ("Plano", "Toggle", "Pista apagada frente a la columna", "#94A3B8", "#1E293B", "no_texto"),
    ("Plano", "Toggle", "Perilla frente a la pista apagada", "#FFFFFF", "#94A3B8", "no_texto"),
    ("Plano", "Slider", "Pista frente a la columna", "#475569", "#1E293B", "no_texto"),
    ("Plano", "Tarjeta", "Título", "#FFFFFF", "#1E40AF", "texto"),
    ("Plano", "Tarjeta", "Párrafo (opacidad 0,8 ≈ #D2D9EF)", "#D2D9EF", "#1E40AF", "texto"),
    ("Neumórfico", "Botón", "Texto «Enviar»", "#555555", "#E0E5EC", "texto"),
    ("Neumórfico", "Botón", "Botón frente a su fondo (mismo color)", "#E0E5EC", "#E0E5EC", "no_texto"),
    ("Neumórfico", "Botón", "Sombra oscura frente al fondo", "#B8BEC7", "#E0E5EC", "no_texto"),
    ("Neumórfico", "Toggle", "Perilla apagada frente a la pista", "#E0E5EC", "#E0E5EC", "no_texto"),
    ("Neumórfico", "Toggle", "Perilla encendida frente a la pista", "#6366F1", "#E0E5EC", "no_texto"),
    ("Neumórfico", "Slider", "Pista frente a la zona (solo sombra interna)", "#B8BEC7", "#E0E5EC", "no_texto"),
    ("Neumórfico", "Tarjeta", "Título", "#333333", "#E0E5EC", "texto"),
    ("Neumórfico", "Tarjeta", "Párrafo", "#777777", "#E0E5EC", "texto"),
    ("Neumórfico (simulado en modo oscuro)", "Botón", "Sombra clara #2B3A52 frente a fondo #1E293B", "#2B3A52", "#1E293B", "no_texto"),
]


def tabla_contraste():
    filas = []
    for estilo, comp, elem, fg, bg, tipo in PARES:
        r = razon(fg, bg)
        minimo = 4.5 if tipo == "texto" else 3.0
        filas.append({"estilo": estilo, "componente": comp, "elemento": elem, "primer_plano": fg, "fondo": bg,
                      "requisito": "1.4.3 texto (4,5:1)" if tipo == "texto" else "1.4.11 no textual (3:1)",
                      "razon": round(r, 2), "cumple": "sí" if r >= minimo else "no"})
    with open(PASO2 / "contraste_wcag_6_2.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)
    return filas


# ---------------------------------------------------------------- navegador
async def main():
    CAP.mkdir(parents=True, exist_ok=True)
    resultado = {}
    async with async_playwright() as p:
        nav = await p.chromium.launch(channel="chrome")
        pagina = await nav.new_page(viewport={"width": 1366, "height": 900})
        errores = []
        pagina.on("pageerror", lambda e: errores.append(str(e)))
        await pagina.goto(HTML)
        await pagina.wait_for_timeout(1200)
        await pagina.screenshot(path=str(CAP / "01_vista_inicial.png"))
        await pagina.screenshot(path=str(CAP / "02_pagina_completa.png"), full_page=True)

        # Cada componente por separado (filtro superior)
        for vista in ["boton", "toggle", "slider", "tarjeta"]:
            await pagina.click(f'.btn-comp[data-vista="{vista}"]')
            await pagina.wait_for_timeout(250)
            await pagina.locator(".grid-estilos").screenshot(path=str(CAP / f"03_componente_{vista}.png"))
        await pagina.click('.btn-comp[data-vista="todos"]')

        # Interacción con los 4 componentes de los 3 estilos
        for estilo in ["skeu", "flat", "neu"]:
            await pagina.click(f"#{estilo}Btn")
            await pagina.click(f"#{estilo}Toggle")
            await pagina.locator(f".{estilo}-slider").fill("80")
        await pagina.wait_for_timeout(400)
        await pagina.locator(".grid-estilos").screenshot(path=str(CAP / "04_toggles_activados_sliders_80.png"))

        # Estado presionado (:active) de los tres botones
        for estilo in ["skeu", "flat", "neu"]:
            caja = await pagina.locator(f"#{estilo}Btn").bounding_box()
            await pagina.mouse.move(caja["x"] + caja["width"] / 2, caja["y"] + caja["height"] / 2)
            await pagina.mouse.down()
            await pagina.wait_for_timeout(200)
            await pagina.locator(f"#{estilo}Btn").screenshot(path=str(CAP / f"05_boton_presionado_{estilo}.png"))
            await pagina.mouse.up()

        resultado["metricas_panel"] = {k: await pagina.locator(f"#{k}").inner_text() for k in ["mClics", "mSkeu", "mFlat", "mNeu"]}
        await pagina.locator(".tabla-section").screenshot(path=str(CAP / "06_tabla_10_criterios.png"))
        await pagina.locator(".metricas").screenshot(path=str(CAP / "07_panel_metricas.png"))

        # Navegación por teclado: ¿se puede llegar a los toggles con Tab?
        await pagina.goto(HTML)
        await pagina.wait_for_timeout(500)
        recorrido = []
        for _ in range(16):
            await pagina.keyboard.press("Tab")
            recorrido.append(await pagina.evaluate("document.activeElement.id || document.activeElement.className || document.activeElement.tagName"))
        resultado["orden_tabulacion"] = recorrido
        resultado["toggles_alcanzables_con_tab"] = any("Toggle" in x for x in recorrido)

        # Auditoría axe-core por columna de estilo
        await pagina.add_script_tag(content=AXE)
        axe = await pagina.evaluate("""async () => {
            const cols = [...document.querySelectorAll('.columna-estilo')];
            const nombres = ['Esqueumórfico', 'Plano', 'Neumórfico'];
            const salida = {};
            for (let i = 0; i < cols.length; i++) {
                const r = await axe.run(cols[i], { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa'] } });
                salida[nombres[i]] = r.violations.map(v => ({ id: v.id, impacto: v.impact, descripcion: v.help, nodos: v.nodes.length, objetivos: v.nodes.map(n => n.target.join(' ')) }));
            }
            const total = await axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa'] } });
            salida['Página completa'] = total.violations.map(v => ({ id: v.id, impacto: v.impact, descripcion: v.help, nodos: v.nodes.length, objetivos: v.nodes.map(n => n.target.join(' ')) }));
            salida['version_axe'] = axe.version;
            return salida;
        }""")
        resultado["axe"] = axe
        resultado["navegador"] = "Google Chrome " + nav.version
        resultado["errores_consola"] = errores

        # Vista móvil
        movil = await nav.new_page(viewport={"width": 390, "height": 844})
        await movil.goto(HTML)
        await movil.wait_for_timeout(800)
        await movil.screenshot(path=str(CAP / "08_movil.png"), full_page=True)
        await nav.close()

    resultado["contraste"] = tabla_contraste()
    (PASO2 / "resultado_analisis_6_2.json").write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Métricas:", resultado["metricas_panel"])
    print("Toggles alcanzables con Tab:", resultado["toggles_alcanzables_con_tab"], resultado["orden_tabulacion"])
    for k, v in axe.items():
        if k != "version_axe":
            print("axe", k, [(x["id"], x["impacto"], x["nodos"]) for x in v])
    print("Contraste:")
    for f in resultado["contraste"]:
        print(f"  {f['estilo']:<14} {f['componente']:<8} {f['elemento']:<48} {f['razon']:>5}  {f['cumple']}")


asyncio.run(main())
