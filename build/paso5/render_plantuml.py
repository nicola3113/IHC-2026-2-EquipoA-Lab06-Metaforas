"""Renderiza archivos .puml a SVG (y PNG de vista previa) con el servidor oficial de PlantUML.

No hay Java instalado en el equipo, así que se usa https://www.plantuml.com/plantuml con la codificación
estándar de PlantUML (deflate + base64 propio). Si el diagrama tiene un error de sintaxis, el servidor devuelve
un SVG con el mensaje de error; el script lo detecta y falla.
Uso: python render_plantuml.py <carpeta_o_archivo.puml> [<carpeta_salida>]
"""
import asyncio
import sys
import time
import urllib.error
import urllib.request
import zlib
from pathlib import Path

SERVIDOR = "https://www.plantuml.com/plantuml"
ALFABETO = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"


def codificar(texto: str) -> str:
    comprimido = zlib.compress(texto.encode("utf-8"), 9)[2:-4]  # deflate «crudo»
    salida = []
    for i in range(0, len(comprimido), 3):
        trozo = comprimido[i:i + 3] + b"\0" * (3 - len(comprimido[i:i + 3]))
        b1, b2, b3 = trozo
        for v in (b1 >> 2, ((b1 & 0x3) << 4) | (b2 >> 4), ((b2 & 0xF) << 2) | (b3 >> 6), b3 & 0x3F):
            salida.append(ALFABETO[v])
    return "".join(salida)


def descargar(formato: str, codigo: str) -> bytes:
    req = urllib.request.Request(f"{SERVIDOR}/{formato}/{codigo}", headers={"User-Agent": "IHC-EquipoA-Lab06"})
    for intento in range(6):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code not in (429, 503, 509):
                raise
            time.sleep(15 * (intento + 1))  # el servidor público limita la frecuencia de peticiones
    raise RuntimeError("El servidor de PlantUML no respondió tras varios intentos")


async def svg_a_png(svg: Path, png: Path):
    """Vista previa PNG generada localmente con Chromium (Playwright), sin otra petición al servidor."""
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        nav = await p.chromium.launch()
        pag = await nav.new_page(device_scale_factor=1)
        await pag.goto(svg.resolve().as_uri())
        await pag.locator("svg").first.screenshot(path=str(png))
        await nav.close()


def renderizar(puml: Path, destino: Path) -> Path:
    texto = puml.read_text(encoding="utf-8")
    codigo = codificar(texto)
    svg = descargar("svg", codigo)
    if b"Syntax Error" in svg or b"syntax error" in svg.lower():
        raise RuntimeError(f"Error de sintaxis en {puml.name}")
    if b"is ignored" in svg or b"deprecated" in svg.lower():
        print(f"  AVISO: {puml.name} usa una opción obsoleta de PlantUML (se muestra un recuadro de advertencia)")
    destino.mkdir(parents=True, exist_ok=True)
    salida = destino / (puml.stem + ".svg")
    salida.write_bytes(svg)
    asyncio.run(svg_a_png(salida, destino / (puml.stem + ".png")))
    time.sleep(3)
    return salida


if __name__ == "__main__":
    origen = Path(sys.argv[1])
    destino = Path(sys.argv[2]) if len(sys.argv) > 2 else (origen if origen.is_dir() else origen.parent)
    archivos = sorted(origen.glob("*.puml")) if origen.is_dir() else [origen]
    for f in archivos:
        s = renderizar(f, destino)
        print(f"{f.name} → {s.name} ({s.stat().st_size / 1024:.0f} KB)")
