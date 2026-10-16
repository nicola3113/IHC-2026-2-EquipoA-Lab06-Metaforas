"""Genera la versión final autocontenida de la galería 6.1 v2.

Sustituye el marcador /*__ICONOS__*/{} del código fuente por los trazos de los
iconos Lucide v0.469.0 (licencia ISC) que usa la página, para que funcione sin conexión.
Uso: python incrustar_iconos.py
"""
from pathlib import Path

AQUI = Path(__file__).resolve().parent
fuente = (AQUI / "galeria_v2.src.html").read_text(encoding="utf-8")
iconos = (AQUI / "lucide_0.469.0_iconos.json").read_text(encoding="utf-8").strip()
assert "/*__ICONOS__*/{}" in fuente, "Falta el marcador de iconos"
salida = AQUI.parents[1] / "L4_paso_a_paso" / "paso1_galeria" / "03_version_mejorada" / "ejercicio_6_1_galeria_metaforas_v2_EquipoA.html"
salida.write_text(fuente.replace("/*__ICONOS__*/{}", iconos), encoding="utf-8")
print(f"Generado: {salida.name} ({salida.stat().st_size / 1024:.1f} KB)")
