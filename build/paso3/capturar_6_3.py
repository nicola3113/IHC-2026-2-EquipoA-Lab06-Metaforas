"""Paso 3 — Capturas de la ejecución del Ejercicio 6.3 (sesión de demostración en Google Chrome).

La sesión automatizada solo sirve como evidencia visual del protocolo; sus datos NO se mezclan con los
CSV reales de los participantes (se guardan aparte como demo_no_analizar.csv).
Uso: python capturar_6_3.py
"""
import asyncio
from pathlib import Path

from playwright.async_api import async_playwright

RAIZ = Path(__file__).resolve().parents[2]
CAP = RAIZ / "L4_paso_a_paso" / "paso3_medicion" / "capturas"
HTML = (RAIZ / "insumos" / "ejercicio_6_3_medicion_interaccion.html").as_uri()
OBJETIVO = {1: "#toggleSkeu", 2: "#toggleFlat", 3: "#toggleNeu", 4: "#btnEnviarSkeu", 5: "#btnEnviarFlat", 6: "#btnEnviarNeu"}


async def main():
    CAP.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        nav = await p.chromium.launch(channel="chrome")
        ctx = await nav.new_context(viewport={"width": 1366, "height": 900}, accept_downloads=True)
        pg = await ctx.new_page()
        await pg.goto(HTML)
        await pg.wait_for_timeout(1000)
        await pg.screenshot(path=str(CAP / "6_3_01_protocolo.png"), full_page=True)
        await pg.click("#btnIniciar")
        for n in range(1, 7):
            await pg.wait_for_timeout(700)
            if n in (1, 3, 4, 6):
                await pg.screenshot(path=str(CAP / f"6_3_02_tarea{n}_antes.png"))
            await pg.click(OBJETIVO[n])
            await pg.wait_for_timeout(300)
            if n in (3, 6):
                await pg.screenshot(path=str(CAP / f"6_3_03_tarea{n}_completada.png"))
            await pg.click("#btnSiguiente")
        await pg.wait_for_timeout(500)
        await pg.screenshot(path=str(CAP / "6_3_04_resultados.png"), full_page=True)
        async with pg.expect_download() as d:
            await pg.click("#btnExportar")
        descarga = await d.value
        await descarga.save_as(str(CAP / "demo_no_analizar.csv"))
        await nav.close()
    print((CAP / "demo_no_analizar.csv").read_text(encoding="utf-8"))


asyncio.run(main())
