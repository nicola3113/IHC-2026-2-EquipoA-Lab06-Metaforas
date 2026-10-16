"""Mide la latencia de apertura del modal de la galería 6.1 v2 (24 aperturas: 12 metáforas x 2) en Chrome y Edge.
Uso: python medir_latencia_modal.py file:///ruta/al/html"""
import asyncio, sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        for canal in ("chrome","msedge"):
            b = await p.chromium.launch(channel=canal); pg = await b.new_page(viewport={"width":1366,"height":900})
            await pg.goto(sys.argv[1]); await pg.wait_for_timeout(500)
            for _ in range(2):
                for bt in await pg.locator("[data-abrir]").all():
                    await bt.click(); await pg.wait_for_timeout(50); await pg.keyboard.press("Escape")
            l = await pg.evaluate("metricas.latencias")
            l=sorted(l); n=len(l)
            print(canal, n, "media %.1f mediana %.1f min %.1f max %.1f" % (sum(l)/n, l[n//2], l[0], l[-1]))
            await b.close()
asyncio.run(main())
