"""Verificación del Paso 1 (galería 6.1) en Google Chrome y Microsoft Edge con Playwright.

- Ejecuta la verificación automática de la página (?autotest=1) y guarda el resultado en JSON.
- Hace la lista de comprobación de la guía con eventos reales del navegador (clics y teclado).
- Toma las capturas de pantalla que se usan en el informe.
Firefox se verifica aparte con su modo headless (ver verificar_firefox.sh).
Uso: python verificar_navegadores.py
"""
import asyncio
import json
from pathlib import Path

from playwright.async_api import async_playwright

RAIZ = Path(__file__).resolve().parents[2]
PASO1 = RAIZ / "L4_paso_a_paso" / "paso1_galeria"
CAPTURAS = PASO1 / "capturas"
VERIF = PASO1 / "verificacion"
V2 = (PASO1 / "03_version_mejorada" / "ejercicio_6_1_galeria_metaforas_v2_EquipoA.html").as_uri()
V1 = (PASO1 / "02_regenerado_desde_prompt" / "ejercicio_6_1_regenerado.html").as_uri()
ORIGINAL = (RAIZ / "insumos" / "ejercicio_6_1_galeria_metaforas.html").as_uri()


async def lista_guia(pagina):
    """Lista de comprobación de la guía ejecutada con eventos reales (no simulados por la página)."""
    r = {}
    r["tarjetas"] = await pagina.locator(".tarjeta").count()
    conteo = {}
    for tipo in ["estructural", "orientacional", "ontologica", "contenedor", "viaje", "conversacional"]:
        await pagina.click(f'.filtro[data-filtro="{tipo}"]')
        conteo[tipo] = await pagina.locator(".tarjeta:not([hidden])").count()
    await pagina.click('.filtro[data-filtro="todas"]')
    r["filtros"] = conteo
    await pagina.click('[data-abrir="migas"]')
    r["modal_abre"] = await pagina.locator("#modalFondo.visible").count() == 1
    await pagina.keyboard.press("Escape")
    r["modal_cierra_escape"] = await pagina.locator("#modalFondo.visible").count() == 0
    await pagina.click('[data-demo="carrito"] [data-agregar]')
    r["demo_carrito"] = await pagina.locator('[data-demo="carrito"] [data-n]').inner_text()
    # Centrar la demo para que la barra fija superior no tape el documento
    await pagina.evaluate("document.querySelector('[data-demo=arrastrar]').scrollIntoView({block: 'center', behavior: 'instant'})")
    await pagina.wait_for_timeout(300)
    caja_doc = await pagina.locator('[data-demo="arrastrar"] [data-doc]').bounding_box()
    caja_dest = await pagina.locator('[data-demo="arrastrar"] [data-destino]').bounding_box()
    await pagina.mouse.move(caja_doc["x"] + 20, caja_doc["y"] + 20)
    await pagina.mouse.down()
    await pagina.mouse.move(caja_dest["x"] + 30, caja_dest["y"] + 30, steps=12)
    await pagina.mouse.up()
    r["demo_arrastre_real"] = await pagina.locator('[data-demo="arrastrar"] .destino-drag.lleno').count() == 1
    r["panel_demos"] = await pagina.locator("#mDemos").inner_text()
    r["panel_clics"] = await pagina.locator("#mClics").inner_text()
    return r


async def capturar(pagina, nombre, completo=False):
    await pagina.screenshot(path=str(CAPTURAS / nombre), full_page=completo)


async def main():
    CAPTURAS.mkdir(parents=True, exist_ok=True)
    VERIF.mkdir(parents=True, exist_ok=True)
    resumen = {}
    async with async_playwright() as p:
        for canal, etiqueta in [("chrome", "chrome"), ("msedge", "edge")]:
            navegador = await p.chromium.launch(channel=canal)
            contexto = await navegador.new_context(viewport={"width": 1366, "height": 900}, device_scale_factor=1)
            pagina = await contexto.new_page()
            errores = []
            pagina.on("pageerror", lambda e: errores.append(str(e)))
            pagina.on("console", lambda m: m.type == "error" and errores.append(m.text))

            # 1) Verificación automática de la página
            await pagina.goto(V2 + "?autotest=1&tema=oscuro")
            await pagina.wait_for_function("window.__resultadoVerificacion !== undefined")
            auto = await pagina.evaluate("window.__resultadoVerificacion")
            await pagina.locator("#verificacion").scroll_into_view_if_needed()
            await pagina.locator("#verificacion").screenshot(path=str(CAPTURAS / f"v2_verificacion_{etiqueta}.png"))

            # 2) Lista de la guía con eventos reales
            await pagina.goto(V2 + "?tema=oscuro")
            await pagina.wait_for_timeout(600)
            guia = await lista_guia(pagina)
            resumen[etiqueta] = {"version_navegador": navegador.version, "verificacion_automatica": auto,
                                 "lista_guia_eventos_reales": guia, "errores_consola": errores}

            if etiqueta == "chrome":
                # Capturas para el informe (solo en Chrome para no duplicar)
                await pagina.goto(V2 + "?tema=oscuro")
                await pagina.wait_for_timeout(800)
                await capturar(pagina, "v2_01_vista_general_oscuro.png")
                await capturar(pagina, "v2_02_pagina_completa_oscuro.png", completo=True)
                await pagina.click('.filtro[data-filtro="contenedor"]')
                await pagina.wait_for_timeout(300)
                await capturar(pagina, "v2_03_filtro_contenedor.png")
                await pagina.click('.filtro[data-filtro="todas"]')
                await pagina.fill("#buscar", "carpeta")
                await pagina.wait_for_timeout(300)
                await capturar(pagina, "v2_04_busqueda_carpeta.png")
                await pagina.fill("#buscar", "")
                await pagina.click('[data-abrir="arrastrar"]')
                await pagina.wait_for_timeout(300)
                await capturar(pagina, "v2_05_modal_criterios.png")
                await pagina.keyboard.press("Escape")
                for selector in ['[data-demo="carrito"] [data-agregar]', '[data-demo="progreso"] [data-mas]',
                                 '[data-demo="asistente"] [data-sig]', '[data-demo="conversacion"] [data-q="Cancela mi vuelo"]']:
                    await pagina.click(selector)
                await pagina.wait_for_timeout(500)
                await pagina.locator("#galeria").screenshot(path=str(CAPTURAS / "v2_06_demos_en_uso.png"))
                for art in await pagina.locator(".rota").all():
                    for _ in range(3):
                        await art.locator("[data-accion]").click()
                await pagina.locator("#rotas").screenshot(path=str(CAPTURAS / "v2_07_metaforas_rotas.png"))
                await pagina.click('[data-abrir="nube"]')
                await pagina.wait_for_timeout(1200)
                await pagina.keyboard.press("Escape")
                await pagina.locator(".panel").screenshot(path=str(CAPTURAS / "v2_08_panel_metricas.png"))
                await pagina.goto(V2 + "?tema=claro")
                await pagina.wait_for_timeout(600)
                await capturar(pagina, "v2_09_tema_claro.png")
                movil = await navegador.new_page(viewport={"width": 390, "height": 844})
                await movil.goto(V2 + "?tema=oscuro")
                await movil.wait_for_timeout(600)
                await movil.screenshot(path=str(CAPTURAS / "v2_10_movil.png"))
                await movil.close()
                # Referencias: original del docente y regeneración
                for url, nombre in [(ORIGINAL, "original_docente.png"), (V1, "v1_regenerado.png")]:
                    await pagina.goto(url)
                    await pagina.wait_for_timeout(1500)
                    await capturar(pagina, nombre)
                    await capturar(pagina, nombre.replace(".png", "_completa.png"), completo=True)
            await navegador.close()
    (VERIF / "resultado_chrome_edge.json").write_text(json.dumps(resumen, ensure_ascii=False, indent=2), encoding="utf-8")
    for nav, datos in resumen.items():
        a = datos["verificacion_automatica"]
        print(f"{nav} {datos['version_navegador']}: {a['superadas']}/{a['total']} · guía: {datos['lista_guia_eventos_reales']} · errores: {datos['errores_consola']}")


asyncio.run(main())
