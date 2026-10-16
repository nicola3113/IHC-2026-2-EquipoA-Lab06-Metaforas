"""Calcula la razón de contraste WCAG 2.2 de los pares de color de la galería 6.1 v2 (ambos temas)."""
def lum(h):
    h = h.lstrip("#"); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
def razon(a, b):
    la, lb = sorted([lum(a), lum(b)], reverse=True); return (la + 0.05) / (lb + 0.05)
TEMAS = {
    "oscuro": dict(fondo="#0B1120", superficie="#151E32", texto="#E8EDF7", texto_sec="#A9B6CF", primario="#4F8DF7",
                   estructural="#5B95F8", orientacional="#22C38E", ontologica="#A989F7", contenedor="#F5B544", viaje="#F27AA9", conversacional="#2CC3DC"),
    "claro": dict(fondo="#F4F6FB", superficie="#FFFFFF", texto="#111827", texto_sec="#424B5C", primario="#1D5BD8",
                  estructural="#1D5BD8", orientacional="#0B7A55", ontologica="#6D3FD1", contenedor="#9A5B00", viaje="#B5245F", conversacional="#0B6E80"),
}
print("tema,primer_plano,fondo,razon,AA_texto_normal")
for tema, c in TEMAS.items():
    pares = [("texto", "fondo"), ("texto", "superficie"), ("texto_sec", "fondo"), ("texto_sec", "superficie"), ("primario", "superficie")]
    pares += [(t, "superficie") for t in ["estructural", "orientacional", "ontologica", "contenedor", "viaje", "conversacional"]]
    for a, b in pares:
        r = razon(c[a], c[b]); print(f"{tema},{a},{b},{r:.2f},{'sí' if r >= 4.5 else 'no'}")
print(f"blanco_sobre_primario_oscuro,#FFFFFF,#4F8DF7,{razon('#FFFFFF', '#4F8DF7'):.2f}")
print(f"blanco_sobre_primario_claro,#FFFFFF,#1D5BD8,{razon('#FFFFFF', '#1D5BD8'):.2f}")
print(f"v2_oscuro,sobre_primario #0B1120,primario #4F8DF7,{razon('#0B1120', '#4F8DF7'):.2f}")
# Original del docente (insumos/ejercicio_6_1_galeria_metaforas.html)
print("original_docente,texto_sec #94A3B8,superficie #1E293B,%.2f" % razon('#94A3B8', '#1E293B'))
print("original_docente,blanco filtro activo,primario #3B82F6,%.2f" % razon('#FFFFFF', '#3B82F6'))
print("original_docente,primario #3B82F6 (enlaces migas),fondo #0F172A,%.2f" % razon('#3B82F6', '#0F172A'))
print("original_docente,texto_sec #94A3B8 en demos,fondo #0F172A,%.2f" % razon('#94A3B8', '#0F172A'))
