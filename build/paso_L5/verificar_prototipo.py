"""L.5 — Verificación del prototipo «huerto» en Chrome y Edge y capturas para el informe.

1. ?autotest=1: la página simula una sesión completa y comprueba 11 puntos (datos marcados como PRUEBA).
2. Sesión de demostración con eventos reales (?demo=1, también marcada como PRUEBA) para las capturas.
Firefox se comprueba con su modo headless (ver verificar_firefox.sh).
Uso: python verificar_prototipo.py
"""
import asyncio
import json
from pathlib import Path

from playwright.async_api import async_playwright

RAIZ = Path(__file__).resolve().parents[2]
L5 = RAIZ / "L5_metafora_propia"
CAP = L5 / "capturas"
HTML = (L5 / "prototipo" / "L5_huerto_inversiones_EquipoA.html").as_uri()


async def responder(pg, tarea_n):
    """Responde la tarea actual leyendo el objetivo desde el estado de la página (solo para la demo)."""
    obj = await pg.evaluate("({t: E.actual.t.tipo, o: E.actual.t.objetivo, a: E.actual.t.accion})")
    pref = "sector" if obj["t"] == "sector" else "activo"
    await pg.click(f'#areaVista [data-sel="{pref}:{obj["o"]}"]')
    if obj["t"] == "accion":
        await pg.click("#btnAccion1" if obj["a"] == "aportar" else "#btnAccion2")


async def main():
    CAP.mkdir(parents=True, exist_ok=True)
    salida = {}
    async with async_playwright() as p:
        for canal in ("chrome", "msedge"):
            nav = await p.chromium.launch(channel=canal)
            pg = await nav.new_page(viewport={"width": 1366, "height": 900})
            errores = []
            pg.on("pageerror", lambda e: errores.append(str(e)))
            await pg.goto(HTML + "?autotest=1")
            res = await pg.evaluate("window.__verificacionHuerto")
            if canal == "chrome":
                await pg.locator("#verif").screenshot(path=str(CAP / "L5_verificacion_chrome.png"))
            salida[canal] = {"version": nav.version, "pasan": res["pasan"], "total": res["total"],
                             "pruebas": res["pruebas"], "errores_consola": errores}

            if canal == "chrome":
                ctx = await nav.new_context(viewport={"width": 1366, "height": 900}, accept_downloads=True)
                pg = await ctx.new_page()
                await pg.goto(HTML + "?demo=1")
                await pg.screenshot(path=str(CAP / "L5_01_inicio_mapeo.png"))
                await pg.click("#btnComenzar")
                await pg.screenshot(path=str(CAP / "L5_02_instrucciones_huerto.png"))
                await pg.click("#btnEmpezarBloque")
                await pg.wait_for_timeout(400)
                await pg.screenshot(path=str(CAP / "L5_03_tarea1_huerto.png"), full_page=True)
                for k in range(5):
                    if k == 1:
                        planta = pg.locator("#areaVista .planta").first
                        await planta.hover()
                        await pg.wait_for_timeout(300)
                        await pg.screenshot(path=str(CAP / "L5_04_huerto_tooltip_degradacion.png"), full_page=True)
                    if k == 3:
                        obj = await pg.evaluate("E.actual.t.objetivo")
                        await pg.click(f'#areaVista [data-sel="activo:{obj}"]')
                        await pg.screenshot(path=str(CAP / "L5_05_huerto_regar.png"), full_page=True)
                    await responder(pg, k)
                    if k == 0:
                        await pg.screenshot(path=str(CAP / "L5_06_escala_seq.png"))
                    await pg.click('#botonesSeq [data-seq="6"]')
                await pg.click("#btnEmpezarBloque")
                await pg.wait_for_timeout(300)
                await pg.screenshot(path=str(CAP / "L5_07_tarea1_tabla.png"), full_page=True)
                for k in range(5):
                    await responder(pg, k)
                    await pg.click('#botonesSeq [data-seq="5"]')
                await pg.screenshot(path=str(CAP / "L5_08_fin_resumen.png"), full_page=True)
                async with pg.expect_download() as d:
                    await pg.click("#btnExportar")
                await (await d.value).save_as(str(CAP / "L5_demo_PRUEBA.csv"))
                movil = await nav.new_page(viewport={"width": 390, "height": 844})
                await movil.goto(HTML + "?demo=1")
                await movil.click("#btnComenzar")
                await movil.click("#btnEmpezarBloque")
                await movil.wait_for_timeout(300)
                await movil.screenshot(path=str(CAP / "L5_09_movil_huerto.png"), full_page=True)
            await nav.close()
    (L5 / "prototipo" / "verificacion_prototipo.json").write_text(json.dumps(salida, ensure_ascii=False, indent=2), encoding="utf-8")
    for k, v in salida.items():
        print(k, v["version"], f"{v['pasan']}/{v['total']}", "errores:", v["errores_consola"])
        for prueba in v["pruebas"]:
            if not prueba["cond"]:
                print("  FALLA:", prueba)


asyncio.run(main())
