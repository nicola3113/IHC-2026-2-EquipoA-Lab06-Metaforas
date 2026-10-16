"""Verifica las referencias de los informes: metadatos de cada DOI en Crossref y estado HTTP de cada URL.
Guarda el resultado en build/informes/referencias_verificadas.json.  Uso: python verificar_referencias.py"""
import json, urllib.request, urllib.parse, urllib.error
from pathlib import Path

DOIS = ["10.1016/S0020-7373(85)80076-6", "10.1109/MC.1983.1654471", "10.1145/1188816.1188820",
        "10.1080/01621459.1937.10503522", "10.2307/3001968", "10.1145/1518701.1518946",
        "10.1038/s41592-019-0686-2", "10.1109/MCSE.2007.55", "10.25080/Majora-92bf1922-011", "10.25080/Majora-92bf1922-00a"]
BUSQUEDAS = ["Examining humanness as a metaphor to design voice user interfaces"]
URLS = ["https://press.uchicago.edu/ucp/books/book/chicago/M/bo3637992.html",
        "https://www.basicbooks.com/titles/don-norman/the-design-of-everyday-things/9780465050659/",
        "https://www.nngroup.com/articles/ten-usability-heuristics/",
        "https://www.nngroup.com/articles/metaphor/",
        "https://www.w3.org/TR/WCAG22/",
        "https://developer.mozilla.org/es/docs/Web/API/Performance/now",
        "https://www.jstor.org/stable/4615733",
        "https://lawsofux.com/"]
H = {"User-Agent": "Mozilla/5.0 (IHC EquipoA; mailto:augusto.cerna@unmsm.edu.pe)"}

def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=40) as r:
        return r.status, r.geturl(), r.read()

salida = {"doi": {}, "busqueda": {}, "url": {}}
for d in DOIS:
    try:
        _, _, b = get("https://api.crossref.org/works/" + urllib.parse.quote(d))
        m = json.loads(b)["message"]
        salida["doi"][d] = {"titulo": (m.get("title") or [""])[0], "revista": (m.get("container-title") or [""])[0],
                            "anio": (m.get("issued", {}).get("date-parts") or [[None]])[0][0], "volumen": m.get("volume"),
                            "numero": m.get("issue"), "paginas": m.get("page"),
                            "autores": [f"{a.get('family','')}, {a.get('given','')}" for a in m.get("author", [])]}
        st, final, _ = get("https://doi.org/" + d) if False else (None, None, None)
    except Exception as e:
        salida["doi"][d] = {"error": str(e)}
for q in BUSQUEDAS:
    _, _, b = get("https://api.crossref.org/works?rows=3&query.bibliographic=" + urllib.parse.quote(q))
    salida["busqueda"][q] = [{"doi": i["DOI"], "titulo": i.get("title", [""])[0], "anio": i.get("issued", {}).get("date-parts", [[None]])[0][0],
                               "evento": (i.get("container-title") or [""])[0], "autores": [a.get("family") for a in i.get("author", [])]}
                              for i in json.loads(b)["message"]["items"]]
for u in URLS:
    try:
        st, final, b = get(u)
        texto = b.decode("utf-8", "ignore")
        import re
        fechas = re.findall(r'(?:datePublished|dateModified|article:modified_time|article:published_time|Last modified|"date")[^0-9]{0,40}(\d{4}-\d{2}-\d{2})', texto)[:4]
        titulo = re.search(r"<title[^>]*>(.*?)</title>", texto, re.S)
        salida["url"][u] = {"estado": st, "final": final, "titulo": titulo.group(1).strip()[:120] if titulo else "", "fechas": fechas}
    except urllib.error.HTTPError as e:
        salida["url"][u] = {"estado": e.code}
    except Exception as e:
        salida["url"][u] = {"error": str(e)}
Path(__file__).with_name("referencias_verificadas.json").write_text(json.dumps(salida, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(salida, ensure_ascii=False, indent=1))
