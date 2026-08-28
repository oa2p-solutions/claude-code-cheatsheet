#!/usr/bin/env python3
"""Construye index.html y los archivos legibles por agentes.

Las 132 fichas de comando se renderizan como HTML estático, no por JavaScript:
los motores de búsqueda con IA (ChatGPT, Perplexity, Claude) no ejecutan JS, así
que el contenido tiene que estar en la respuesta HTML para poder ser citado.

    python3 build.py
"""
import json, pathlib, re, unicodedata
from datetime import date

RAIZ   = pathlib.Path(__file__).parent
SITIO  = "https://cheatsheet-claude.oa2p-solutions.com"
HOY    = date.today().isoformat()

LABEL = {"core":"de uso diario","cond":"condicional","skill":"skill","cloud":"nube","warn":"cuidado"}
CLS   = {"core":"t-core","cond":"t-cond","skill":"t-skill","cloud":"t-cloud","warn":"t-warn"}


def esc(t):
    return str(t).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def sin_html(t):
    return re.sub(r"<[^>]+>", "", str(t))

def normaliza(t):
    t = unicodedata.normalize("NFD", t.lower())
    return "".join(c for c in t if unicodedata.category(c) != "Mn")

def slug(nombre):
    return "cmd-" + re.sub(r"[^a-z0-9]+", "-", nombre.lower()).strip("-")


def ficha(r, grupo):
    """Una ficha de comando como <article>, con el índice de búsqueda en data-h."""
    hay = normaliza(" ".join([r["n"], r["arg"], r["a"], sin_html(r["w"]),
                              " ".join(r["ex"]), r["q"], grupo["t"]]))
    tags = "".join(f'<span class="tag {CLS[g]}">{LABEL[g]}</span>' for g in r["g"])
    alias = f'<p class="alias">alias {esc(r["a"])}</p>' if r["a"] else ""
    ejemplos = ("<div class=\"ex\">" + "".join(f"<code>{esc(e)}</code>" for e in r["ex"]) + "</div>") if r["ex"] else ""
    return (
        f'<article class="row{" core" if "core" in r["g"] else ""}" id="{slug(r["n"])}"'
        f' data-t="{" ".join(r["g"])}" data-h="{esc(hay)}">'
        f'<div class="c-name"><h3 class="cmd">{r["n"]}<span class="arg">{esc(r["arg"])}</span></h3>'
        f'{f"<div class=\"tags\">{tags}</div>" if tags else ""}{alias}</div>'
        f'<div class="c-what"><p class="what">{r["w"]}</p>{ejemplos}</div>'
        f'<div class="c-when"><span class="whenlab">cuándo usarlo</span>'
        f'<p class="when">{r["q"]}</p></div>'
        f'</article>'
    )


def grupos_html(datos):
    partes = []
    for i, g in enumerate(datos):
        fichas = "".join(ficha(r, g) for r in g["r"])
        nota = f'<p class="gnote">{g["note"]}</p>' if g.get("note") else ""
        partes.append(
            f'<section class="group" id="g{i+1:02d}" data-g="{i}">'
            f'<div class="ghead"><span class="gnum">{i+1:02d}</span><h2>{g["t"]}</h2></div>'
            f'{nota}<div class="rows">{fichas}</div></section>'
        )
    partes.append('<div class="empty" id="empty" hidden>Ningún comando coincide. '
                  'Prueba con menos palabras, o borra los filtros.</div>')
    # El contenedor #groups es al que se engancha el script: sin él,
    # getElementById('groups') devuelve null y la búsqueda deja de funcionar.
    return '<div id="groups">' + "".join(partes) + '</div>'


def jsonld(datos):
    """TechArticle + FAQPage: los "cuándo usarlo" son respuestas a preguntas reales."""
    total = sum(len(g["r"]) for g in datos)
    faq = [{"@type":"Question",
            "name": f'¿Cuándo usar {r["n"]} en Claude Code?',
            "acceptedAnswer":{"@type":"Answer","text": sin_html(r["w"]) + " " + sin_html(r["q"])}}
           for g in datos for r in g["r"] if "core" in r["g"]]
    grafo = [
      {"@type":"TechArticle","@id":f"{SITIO}/#articulo",
       "headline":"Comandos slash de Claude Code",
       "description":(f"Referencia de los {total} comandos slash de Claude Code extraídos del "
                      "binario 2.1.247: qué hace cada uno, ejemplos y cuándo usarlo."),
       "inLanguage":"es","datePublished":"2026-08-27","dateModified":HOY,
       "url":SITIO+"/","mainEntityOfPage":SITIO+"/",
       "author":{"@type":"Organization","name":"OA2P Solutions","url":"https://oa2p.com"},
       "publisher":{"@type":"Organization","name":"OA2P Solutions","url":"https://oa2p.com"},
       "about":{"@type":"SoftwareApplication","name":"Claude Code",
                "applicationCategory":"DeveloperApplication","softwareVersion":"2.1.247",
                "operatingSystem":"macOS, Linux, Windows"},
       "keywords":"Claude Code, comandos slash, CLI, referencia, cheatsheet"},
      {"@type":"FAQPage","@id":f"{SITIO}/#faq","mainEntity":faq},
    ]
    return json.dumps({"@context":"https://schema.org","@graph":grafo},
                      ensure_ascii=False, separators=(",",":"))


def llms_txt(datos):
    total = sum(len(g["r"]) for g in datos)
    l = ["# Comandos slash de Claude Code", "",
         f"> Referencia de los {total} comandos slash de Claude Code, extraídos de las "
         "definiciones del binario 2.1.247 y no de la documentación pública. Cada comando "
         "incluye descripción, alias, argumentos, un ejemplo real y cuándo conviene usarlo. "
         "Publicada por OA2P Solutions.", "",
         "Cubre además la sintaxis que no empieza por `/` (`#` memoria, `!` shell, `@` archivos, "
         "`ultrathink`, `+500k`, `ultracode`), los atajos de teclado, cómo crear comandos propios "
         "con su frontmatter, los eventos de hook y los flags del CLI.", "",
         "## Recursos", "",
         f"- [Referencia completa en Markdown]({SITIO}/CHEATSHEET.md): el documento entero, 43 KB",
         f"- [Datos en JSON]({SITIO}/commands.json): los {total} comandos estructurados",
         f"- [Página web]({SITIO}/): la misma referencia con buscador", "",
         "## Comandos por categoría", ""]
    for g in datos:
        l.append(f"### {g['t']}")
        l.append("")
        for r in g["r"]:
            alias = f" (alias: {r['a']})" if r["a"] else ""
            l.append(f"- `{r['n']}{r['arg']}`{alias}: {sin_html(r['w'])} Cuándo: {sin_html(r['q'])}")
        l.append("")
    return "\n".join(l)


def main():
    datos = json.loads((RAIZ/"commands.json").read_text("utf-8"))
    total = sum(len(g["r"]) for g in datos)
    html = (RAIZ/"template.html").read_text("utf-8")
    html = html.replace("<!--GROUPS-->", grupos_html(datos))
    meses = ("enero","febrero","marzo","abril","mayo","junio","julio",
             "agosto","septiembre","octubre","noviembre","diciembre")
    hoy = date.today()
    html = html.replace("__HOY__", HOY).replace(
        "__FECHA__", f"{hoy.day} de {meses[hoy.month-1]} de {hoy.year}")
    html = html.replace("</head>",
        f'<link rel="canonical" href="{SITIO}/">\n'
        f'<script type="application/ld+json">{jsonld(datos)}</script>\n</head>')
    (RAIZ/"index.html").write_text(html, "utf-8")

    (RAIZ/"llms.txt").write_text(llms_txt(datos), "utf-8")
    (RAIZ/"robots.txt").write_text(
        "# Todos los agentes bienvenidos, incluidos los de IA.\n"
        "User-agent: *\nAllow: /\n\n"
        f"Sitemap: {SITIO}/sitemap.xml\n", "utf-8")
    (RAIZ/"sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f'  <url><loc>{SITIO}/</loc><lastmod>{HOY}</lastmod>'
        '<changefreq>monthly</changefreq><priority>1.0</priority></url>\n'
        f'  <url><loc>{SITIO}/CHEATSHEET.md</loc><lastmod>{HOY}</lastmod>'
        '<changefreq>monthly</changefreq><priority>0.8</priority></url>\n'
        '</urlset>\n', "utf-8")

    print(f"index.html    {len(html):>8,} bytes · {total} fichas estáticas")
    for f in ("llms.txt","robots.txt","sitemap.xml"):
        print(f"{f:<13} {(RAIZ/f).stat().st_size:>8,} bytes")


if __name__ == "__main__":
    main()
