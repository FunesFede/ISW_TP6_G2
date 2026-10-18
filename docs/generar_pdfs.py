"""Genera los PDF de la entrega a partir de sus fuentes.

- Términos y condiciones: frontend/src/datos/terminos.json (el mismo texto
  que muestra la aplicación), un PDF por actividad.
- Decisiones de diseño y hoja de entrega: archivos Markdown de esta carpeta.

Requisitos: pip install markdown playwright, playwright install chromium,
y npm install en frontend/ (se usa la fuente Lato instalada ahí).

Uso:  python docs/generar_pdfs.py
"""
import html
import json
import tempfile
from pathlib import Path

import markdown
from playwright.sync_api import sync_playwright

DOCS = Path(__file__).resolve().parent
RAIZ = DOCS.parent
FRONTEND = RAIZ / "frontend"
FUENTES = FRONTEND / "node_modules" / "@fontsource" / "lato" / "files"
LOGO = FRONTEND / "public" / "logo-ecoharmony.png"
TERMINOS = FRONTEND / "src" / "datos" / "terminos.json"

ORDEN_COMUNES = ["inscripcion", "datos", "dia", "cambios", "privacidad"]


def css():
    caras = "\n".join(
        f"@font-face {{ font-family: Lato; font-weight: {peso}; "
        f"src: url('{(FUENTES / f'lato-latin-{peso}-normal.woff2').as_uri()}'); }}"
        for peso in (300, 400, 700, 900)
    )
    return caras + """
    :root { --bosque: #386641; --helecho: #6a994e; --brote: #a7c957;
            --crema: #f2e8cf; --rojo: #bc4749; --tinta: #1f2b1d;
            --suave: #56624f; --linea: #ddd3b8; }
    * { box-sizing: border-box; }
    body { margin: 0; font-family: Lato, sans-serif; color: var(--tinta);
           font-size: 10.5pt; line-height: 1.5; }
    header.portada { display: flex; align-items: center; gap: 18px;
                     padding-bottom: 14px; border-bottom: 3px solid var(--bosque);
                     margin-bottom: 18px; }
    header.portada img { width: 150px; }
    header.portada .eyebrow { font-size: 8.5pt; font-weight: 700;
                              letter-spacing: .08em; text-transform: uppercase;
                              color: var(--helecho); margin: 0; }
    h1 { font-weight: 900; font-size: 21pt; line-height: 1.15;
         color: var(--bosque); margin: 2px 0 0; letter-spacing: -.01em; }
    h2 { font-weight: 900; font-size: 13pt; color: var(--bosque);
         margin: 20px 0 6px; break-after: avoid; }
    h3 { font-weight: 700; font-size: 11pt; margin: 14px 0 4px;
         break-after: avoid; }
    p { margin: 0 0 8px; }
    ol, ul { margin: 4px 0 10px; padding-left: 20px; }
    li { margin-bottom: 4px; }
    .resumen { background: var(--crema); border-left: 4px solid var(--helecho);
               padding: 10px 14px; margin: 0 0 6px; }
    table { width: 100%; border-collapse: collapse; margin: 8px 0 12px;
            font-size: 9.5pt; break-inside: avoid; }
    th { text-align: left; background: var(--bosque); color: #fff;
         font-weight: 700; padding: 6px 8px; }
    td { padding: 6px 8px; border-bottom: 1px solid var(--linea);
         vertical-align: top; }
    code { font-family: 'DejaVu Sans Mono', monospace; font-size: 8.8pt;
           background: #f3eedf; padding: 1px 4px; border-radius: 3px; }
    pre { background: #f3eedf; padding: 10px 12px; border-radius: 6px;
          font-size: 8.8pt; line-height: 1.45; break-inside: avoid;
          white-space: pre-wrap; }
    pre code { background: none; padding: 0; }
    blockquote { margin: 0 0 10px; padding: 8px 14px; background: var(--crema);
                 border-left: 4px solid var(--helecho); }
    .firma { margin-top: 26px; padding-top: 12px; border-top: 1px solid var(--linea);
             font-size: 9pt; color: var(--suave); }
    """


def pagina(cuerpo, titulo):
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
    <title>{html.escape(titulo)}</title><style>{css()}</style></head>
    <body>{cuerpo}</body></html>"""


def portada(eyebrow, titulo):
    return (f'<header class="portada"><img src="{LOGO.as_uri()}" alt="">'
            f'<div><p class="eyebrow">{html.escape(eyebrow)}</p>'
            f'<h1>{html.escape(titulo)}</h1></div></header>')


def lista(puntos):
    items = "".join(f"<li>{html.escape(p)}</li>" for p in puntos)
    return f"<ol>{items}</ol>"


def terminos_html(datos, actividad):
    propia = datos["actividades"][actividad]
    secciones = [propia["requisitos"]] + [
        datos["comunes"][clave] for clave in ORDEN_COMUNES
    ]
    cuerpo = portada(
        f"Términos y condiciones · versión {datos['version']}",
        f"{actividad}",
    )
    cuerpo += f'<p class="resumen">{html.escape(propia["resumen"])}</p>'
    for numero, seccion in enumerate(secciones, start=1):
        cuerpo += f"<h2>{numero}. {html.escape(seccion['titulo'])}</h2>"
        cuerpo += lista(seccion["puntos"])
    cuerpo += (
        '<p class="firma">Al marcar "Acepto los términos y condiciones de '
        f'{html.escape(actividad)}" en la aplicación, quien realiza la '
        "inscripción declara haber leído y aceptado estas condiciones en "
        "nombre de todas las personas inscriptas.</p>"
    )
    return pagina(cuerpo, f"Términos y condiciones · {actividad}")


def markdown_html(ruta, eyebrow):
    texto = ruta.read_text(encoding="utf-8")
    primera, _, resto = texto.partition("\n")
    titulo = primera.lstrip("# ").strip()
    cuerpo = portada(eyebrow, titulo)
    cuerpo += markdown.markdown(resto, extensions=["tables", "fenced_code"])
    return pagina(cuerpo, titulo)


def imprimir(navegador, contenido, salida):
    with tempfile.NamedTemporaryFile(
        "w", suffix=".html", delete=False, encoding="utf-8"
    ) as archivo:
        archivo.write(contenido)
        temporal = Path(archivo.name)
    pagina_web = navegador.new_page()
    pagina_web.goto(temporal.as_uri())
    pagina_web.wait_for_load_state("networkidle")
    pagina_web.pdf(
        path=str(salida),
        format="A4",
        print_background=True,
        margin={"top": "16mm", "bottom": "18mm", "left": "18mm",
                "right": "18mm"},
        display_header_footer=True,
        header_template="<span></span>",
        footer_template=(
            '<div style="width:100%;font-size:7.5pt;color:#56624f;'
            'padding:0 18mm;display:flex;justify-content:space-between;'
            'font-family:sans-serif"><span>EcoHarmony Park · TP 6 TDD · '
            'Grupo 2 · 4K1</span><span><span class="pageNumber"></span> / '
            '<span class="totalPages"></span></span></div>'
        ),
    )
    pagina_web.close()
    temporal.unlink()
    print("Generado:", salida.relative_to(RAIZ))


def main():
    datos = json.loads(TERMINOS.read_text(encoding="utf-8"))
    (DOCS / "terminos").mkdir(exist_ok=True)
    with sync_playwright() as p:
        navegador = p.chromium.launch()
        for actividad in datos["actividades"]:
            nombre = actividad.replace("í", "i")
            imprimir(
                navegador,
                terminos_html(datos, actividad),
                DOCS / "terminos" / f"Terminos_y_condiciones_{nombre}.pdf",
            )
        imprimir(
            navegador,
            markdown_html(DOCS / "decisiones_de_diseno.md",
                          "TP 6 · TDD · Inscribirme a actividad"),
            DOCS / "Decisiones_de_diseno.pdf",
        )
        imprimir(
            navegador,
            markdown_html(DOCS / "hoja_de_entrega.md",
                          "Trabajo Práctico N° 6 · TDD · Grupo N° 2 · 4K1 · ISW"),
            DOCS / "Hoja_de_entrega_TP6_G2.pdf",
        )
        navegador.close()


if __name__ == "__main__":
    main()
