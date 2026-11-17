#!/usr/bin/env python3
"""
render_informe.py: arma el informe de auditoría (PDF)
a partir de un JSON con el contenido. Sin IA, sin dependencias: Python stdlib + un
navegador Chromium (Chrome o Edge) en modo headless para imprimir el PDF.

Uso:
  python render_informe.py informe.json
  python render_informe.py informe.json --salida "C:/carpeta/destino"
  python render_informe.py informe.json --solo-html      (no imprime el PDF)

Genera en la carpeta de salida (por defecto, la del JSON):
  Informe Auditoria <Materia>.pdf   el informe final
  Informe Auditoria <Materia>.html  la fuente (se borra si el PDF salió bien)
Las filas de la planilla las escribe el agente con el conector de Google Sheets,
desde el mismo JSON (ver references/planillas.md).

Exit codes: 0 ok · 1 error en el JSON · 2 no se pudo imprimir el PDF (queda el HTML)
"""
import argparse, html, json, os, shutil, subprocess, sys, tempfile, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS = (ROOT / "assets" / "estilo.css").read_text(encoding="utf-8")
e = html.escape

PRIORIDADES = ("alta", "media", "baja")
NOMBRE_PR = {"alta": "Alta", "media": "Media", "baja": "Baja"}
AUTOMATIZABLE = {"Sí", "No", "A evaluar"}
ESTADOS = {"Pendiente", "Parcial", "Cubierta"}
# Nombres anteriores, aceptados para no romper JSON ya armados.
ESTADOS_VIEJOS = {"En curso": "Parcial", "Resuelto": "Cubierta"}
CAMPOS_TAREA = ("prioridad", "titulo", "hoy", "frecuencia", "por_que", "como_automatizar",
                "hallazgo", "automatizable", "como_corto", "estado")
# Opcionales: tiempo_semanal, con_que, estado_motivo, falta. Los campos viejos unidad y evidencia se ignoran.


def sin_tildes(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


RANGOS = {"menos de 1 hora": (0, 1), "1 a 3 horas": (1, 3), "3 a 6 horas": (3, 6), "más de 6 horas": (6, None)}


def rango_horas(txt: str):
    """(mín, máx) de horas por semana; máx None = sin tope. Solo entiende las opciones fijas o
    "N horas" / "N minutos" (por semana). Cualquier otra cosa devuelve None: el total no se
    calcula antes que inventar un número."""
    import re
    s = txt.strip().lower().rstrip(".")
    if s in RANGOS:
        return RANGOS[s]
    m = re.fullmatch(r"(\d+(?:[.,]\d+)?)\s*(horas?|h|minutos?|min)(\s+por\s+semana)?", s)
    if not m:
        return None
    n = float(m.group(1).replace(",", "."))
    n = n / 60 if m.group(2).startswith("min") else n
    return (n, n)


def fmt_h(x: float) -> str:
    return (str(int(x)) if float(x).is_integer() else f"{x:.1f}".replace(".", ",")) + (" hora" if x == 1 else " horas")


def total_texto(tareas) -> str:
    mins, maxs, abierto = 0.0, 0.0, False
    for t in tareas:
        r = rango_horas(str(t.get("tiempo_semanal", "")))
        if r is None:
            return None
        lo, hi = r
        mins += lo
        if hi is None:
            abierto = True
        else:
            maxs += hi
    if abierto:
        return f"más de {fmt_h(mins)} por semana"
    if mins == maxs:
        return f"{fmt_h(mins)} por semana"
    return f"entre {fmt_h(mins).split()[0]} y {fmt_h(maxs)} por semana"


def con_que_html(t: dict) -> str:
    """Debajo del tiempo en la tabla de resumen: con qué lo hace (skill, a mano, Active-IA)."""
    c = str(t.get("con_que", "")).strip()
    return f"<span class='con'>{e(c)}</span>" if c else ""


def tiempo_con_que(t: dict) -> str:
    """"1 a 3 horas, con la skill TUP Campus Navigator": el tiempo atado a la herramienta."""
    tiempo = str(t.get("tiempo_semanal", "")).strip()
    c = str(t.get("con_que", "")).strip().rstrip(".")
    return f"{tiempo.rstrip('.')}, {c[0].lower() + c[1:]}." if tiempo and c else tiempo


def validar(d: dict) -> list[str]:
    errs = []
    for k in ("materia", "comision", "rol", "nombre", "fecha", "relevamiento", "tareas", "conclusion"):
        if not d.get(k):
            errs.append(f"Falta el campo '{k}' o está vacío.")
    for i, t in enumerate(d.get("tareas", []), 1):
        t["estado"] = ESTADOS_VIEJOS.get(t.get("estado"), t.get("estado"))
        for k in CAMPOS_TAREA:
            if not str(t.get(k, "")).strip():
                errs.append(f"Tarea {i}: falta '{k}' (ninguna celda puede quedar vacía).")
        if t.get("prioridad") not in PRIORIDADES:
            errs.append(f"Tarea {i}: prioridad debe ser alta, media o baja.")
        if t.get("automatizable") not in AUTOMATIZABLE:
            errs.append(f"Tarea {i}: automatizable debe ser Sí, No o A evaluar.")
        if t.get("estado") not in ESTADOS:
            errs.append(f"Tarea {i}: estado debe ser Pendiente, Parcial o Cubierta.")
    return errs


def armar_html(d: dict) -> str:
    materia = d["materia"]
    com = d["comision"]
    rot_com = "Comisiones" if (" y " in com or "," in com) else "Comisión"
    objetivo = d.get("objetivo") or (
        f"Identificar las tareas de tutoría de {materia} que hoy necesitan la intervención del tutor "
        "y que consumen más tiempo, y proponer cómo se podrían automatizar total o parcialmente. "
        "El informe no evalúa si el aula está bien armada: se enfoca en el trabajo repetitivo del tutor.")
    o = [f"<!doctype html><html lang='es'><head><meta charset='utf-8'><title>Informe de Auditoría {e(materia)}</title><style>{CSS}</style></head><body>"]
    o.append("<div class='portada'><div class='kicker'>Auditoría de tareas de tutoría · TUP a Distancia · UTN</div>"
             f"<h1>Informe de Auditoría · {e(materia)}</h1><div class='sub'>Tareas que necesitan la intervención del tutor y propuestas de automatización</div></div>"
             "<div class='franja'><span></span><span></span><span></span><span></span></div>")
    filas = [("Materia", materia), (rot_com, com), ("Rol", d["rol"]), ("Nombre y apellido", d["nombre"]), ("Fecha del informe", d["fecha"])]
    o.append("<table class='datos'>" + "".join(f"<tr><td>{e(k)}</td><td>{e(v)}</td></tr>" for k, v in filas) + "</table>")
    n = iter(range(1, 20))
    o.append(f"<h2><span class='num'>{next(n)}</span>Objetivo</h2><p>{e(objetivo)}</p>")

    # Qué cuenta como intervención del tutor: texto fijo, igual en todos los informes
    o.append(f"<h2><span class='num'>{next(n)}</span>Qué se considera intervención del tutor</h2>"
             "<p>En este informe, una tarea manual es <b>toda tarea que necesita la intervención del tutor, aunque una "
             "herramienta haga una parte</b>. No se cuenta solo lo que el tutor hace a mano. También cuenta el trabajo que hace "
             "con herramientas: consultar datos de Moodle con la skill TUP Campus Navigator, revisar las correcciones que propone "
             "Active-IA, redactar los mensajes y avisos que después publica una herramienta, y cualquier paso en el que tenga que "
             "consultar, revisar, decidir, escribir o enviar algo.</p>"
             "<p>Lo que una herramienta resuelve sola, sin que el tutor intervenga, no se cuenta como intervención. Por eso, en "
             "cada tarea se indica qué resuelve ya cada herramienta y qué sigue necesitando al tutor.</p>"
             "<p class='leyenda'><b>Estado de cada tarea: cuánto la cubren las herramientas.</b> Pendiente: ninguna herramienta la cubre; toda la "
             "tarea depende del tutor. Parcial: una herramienta hace una parte y el tutor hace el resto. Cubierta: la tarea ya no "
             "necesita la intervención del tutor.</p>")
    herr = d.get("herramientas") or []
    if herr:
        o.append("<h3 class='sub'>Herramientas que usa el tutor</h3><table class='planilla resumen'><colgroup>"
                 "<col style='width:22%'><col style='width:39%'><col style='width:39%'></colgroup>"
                 "<tr><th>Herramienta</th><th>Qué resuelve</th><th>Qué sigue necesitando al tutor</th></tr>"
                 + "".join(f"<tr><td>{e(h.get('nombre',''))}</td><td>{e(h.get('resuelve',''))}</td><td>{e(h.get('falta',''))}</td></tr>" for h in herr)
                 + "</table>")

    o.append(f"<h2><span class='num'>{next(n)}</span>Cómo se relevó</h2>" + "".join(f"<p>{e(x)}</p>" for x in d["relevamiento"]))
    n_tareas = next(n)
    o.append(f"<h2><span class='num'>{n_tareas}</span>Tareas que necesitan la intervención del tutor</h2><p class='leyenda'>Agrupadas por "
             "prioridad. Prioridad alta: consume mucho tiempo todas las semanas o afecta a toda la comisión. Prioridad media: es "
             "frecuente pero acotada. Prioridad baja: es ocasional o ya tiene una solución parcial.</p>")

    # Resumen: siempre; la columna de tiempo solo si hay tiempos cargados
    con_tiempo = any(str(x.get("tiempo_semanal", "")).strip() for x in d["tareas"])
    orden = sorted(d["tareas"], key=lambda x: PRIORIDADES.index(x["prioridad"]))
    cols = ("<col style='width:38%'><col style='width:11%'><col style='width:13%'><col style='width:20%'><col style='width:18%'>"
            if con_tiempo else "<col style='width:50%'><col style='width:14%'><col style='width:14%'><col style='width:22%'>")
    o.append("<p class='leyenda'>Resumen de las tareas" + (", con el tiempo de intervención del tutor según su propia estimación." if con_tiempo else ".")
             + "</p><table class='planilla resumen'><colgroup>" + cols + "</colgroup><tr><th>Tarea</th><th>Prioridad</th><th>Estado</th>"
             "<th>Frecuencia</th>" + ("<th>Tiempo de intervención</th>" if con_tiempo else "") + "</tr>")
    for x in orden:
        o.append(f"<tr><td>{e(x['titulo'])}</td><td>{NOMBRE_PR[x['prioridad']]}</td><td>{e(x['estado'])}</td>"
                 f"<td>{e(x['frecuencia'].rstrip('.'))}</td>" + (f"<td>{e(x.get('tiempo_semanal') or 'Sin estimar')}{con_que_html(x)}</td>" if con_tiempo else "") + "</tr>")
    if con_tiempo:
        tot = total_texto(d["tareas"])
        alta = [x for x in d["tareas"] if x["prioridad"] == "alta"]
        if tot:
            o.append(f"<tr class='total'><td colspan='4'>Total de intervención del tutor</td><td>{e(tot)}</td></tr>")
            tot_a = total_texto(alta)
            if alta and len(alta) < len(d["tareas"]) and tot_a:
                o.append(f"<tr class='total'><td colspan='4'>Solo tareas de prioridad alta</td><td>{e(tot_a)}</td></tr>")
    o.append("</table>")

    for pr in PRIORIDADES:
        its = [x for x in d["tareas"] if x["prioridad"] == pr]
        if not its:
            continue
        o.append(f"<h3 class='{pr}'>Prioridad {pr}</h3>")
        for x in its:
            fila = lambda k, v: f"<dt>{k}</dt><dd>{e(v)}</dd>" if str(v or "").strip() else ""
            estado = x["estado"] + "."
            if str(x.get("estado_motivo", "")).strip():
                estado += " " + x["estado_motivo"].strip().rstrip(".") + "."
            if str(x.get("falta", "")).strip():
                estado += " Falta: " + x["falta"].strip()[0].lower() + x["falta"].strip()[1:].rstrip(".") + "."
            o.append(f"<div class='hallazgo {pr}'><div class='t'>{e(x['titulo'])}</div><dl>"
                     + fila("Qué se hace hoy", x["hoy"]) + fila("Frecuencia", x["frecuencia"])
                     + fila("Tiempo de intervención", tiempo_con_que(x)) + fila("Por qué lleva tiempo", x["por_que"])
                     + fila("Estado", estado)
                     + fila("Cómo automatizar", x["como_automatizar"]) + "</dl></div>")
    o.append(f"<h2><span class='num'>{next(n)}</span>Conclusión</h2>" + "".join(f"<p>{e(x)}</p>" for x in d["conclusion"]))
    if d.get("pasos"):
        o.append("<div class='cierre'><b>Pasos para entregar el informe</b>1. Armalo con las tareas de tu materia y comisión, "
                 "siguiendo estas secciones. Si ya usás alguna herramienta para una tarea, contá qué resuelve y qué sigue "
                 "necesitando tu intervención. 2. Subilo a la carpeta Informes de tu materia. 3. En la pestaña Personas marcá "
                 "\"Sí\" en \"¿Subió el informe?\" y pegá el link. 4. Cargá cada tarea como una fila en la pestaña Hallazgos.</div>")
    o.append(f"<div class='apaisada'><h2><span class='num'>{next(n)}</span>Cómo se cargan en la pestaña Hallazgos</h2>"
             f"<p>Cada tarea de la sección {n_tareas} es una fila en la pestaña Hallazgos {e(materia)}. Las columnas son las mismas que en "
             "la planilla.</p>"
             "<p class='leyenda'>Prioridad: Alta, Media o Baja. ¿Automatizable?: Sí, No o A evaluar. Estado: Pendiente (ninguna "
             "herramienta la cubre), Parcial (una herramienta hace una parte y el tutor el resto) o Cubierta (ya no necesita al tutor).</p>"
             "<table class='planilla'><colgroup><col style='width:8%'><col style='width:9%'>"
             "<col style='width:13%'><col style='width:20%'><col style='width:12%'><col style='width:6.5%'><col style='width:9.5%'>"
             "<col style='width:14%'><col style='width:8%'></colgroup><tr><th>Fecha</th><th>Nombre y apellido</th>"
             "<th>Tarea</th><th>Hallazgo</th><th>Tiempo por semana</th><th>Prioridad</th><th>¿Automatizable?</th>"
             "<th>Cómo se podría automatizar</th><th>Estado</th></tr>")
    for t in d["tareas"]:
        o.append(f"<tr><td class='nw'>{e(d['fecha'])}</td><td>{e(d['nombre'])}</td><td>{e(t['titulo'])}</td>"
                 f"<td>{e(t['hallazgo'])}</td><td>{e(tiempo_con_que(t) or 'Sin estimar')}</td><td>{NOMBRE_PR[t['prioridad']]}</td>"
                 f"<td>{e(t['automatizable'])}</td><td>{e(t['como_corto'])}</td><td>{e(t['estado'])}</td></tr>")
    o.append("</table></div></body></html>")
    return "".join(o)


def buscar_navegador() -> str | None:
    cands = [
        os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"),
        os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"),
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    ]
    for c in cands:
        if c and Path(c).is_file():
            return c
    for n in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge", "chrome", "msedge"):
        p = shutil.which(n)
        if p:
            return p
    return None


def imprimir_pdf(html_path: Path, pdf_path: Path) -> tuple[bool, str]:
    nav = buscar_navegador()
    if not nav:
        return False, "No encontré Chrome ni Edge instalados."
    perfil = tempfile.mkdtemp(prefix="auditoria-pdf-")
    cmd = [nav, "--headless", "--disable-gpu", "--no-sandbox", "--no-pdf-header-footer",
           f"--user-data-dir={perfil}", f"--print-to-pdf={pdf_path}", html_path.resolve().as_uri()]
    try:
        subprocess.run(cmd, capture_output=True, timeout=120)
    except Exception as ex:
        return False, f"Falló el navegador: {ex}"
    finally:
        shutil.rmtree(perfil, ignore_errors=True)
    if not pdf_path.is_file() or pdf_path.stat().st_size < 2000:
        return False, "El navegador no generó el PDF."
    return True, nav


def contar_paginas(pdf: Path) -> int:
    import re
    return len(re.findall(rb"/Type\s*/Page(?!s)", pdf.read_bytes()))


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Arma el informe de auditoría en PDF")
    ap.add_argument("json")
    ap.add_argument("--salida", default=None)
    ap.add_argument("--solo-html", action="store_true")
    a = ap.parse_args()

    src = Path(a.json).expanduser().resolve()
    try:
        d = json.loads(src.read_text(encoding="utf-8"))
    except Exception as ex:
        print(f"ERROR: no pude leer el JSON: {ex}")
        return 1
    errs = validar(d)
    if errs:
        print("ERROR en el contenido del informe:")
        for x in errs:
            print("  - " + x)
        return 1

    out = Path(a.salida).expanduser().resolve() if a.salida else src.parent
    out.mkdir(parents=True, exist_ok=True)
    base = sin_tildes(d["materia"])
    html_path = out / f"Informe Auditoria {base}.html"
    pdf_path = out / f"Informe Auditoria {base}.pdf"
    html_path.write_text(armar_html(d), encoding="utf-8")

    tot = total_texto(d["tareas"]) if all(str(x.get("tiempo_semanal", "")).strip() for x in d["tareas"]) else None
    if tot:
        alta = [x for x in d["tareas"] if x["prioridad"] == "alta"]
        print(f"Total de intervención: {tot}" + (f" · prioridad alta: {total_texto(alta)}" if alta else ""))
    if a.solo_html:
        print(f"HTML: {html_path}")
        return 0
    ok, info = imprimir_pdf(html_path, pdf_path)
    if not ok:
        print(f"AVISO: {info} Quedó el HTML en {html_path}: abrilo en el navegador e imprimilo como PDF "
              "(Ctrl+P, Guardar como PDF, sin encabezados ni pies de página).")
        return 2
    html_path.unlink(missing_ok=True)
    print(f"PDF: {pdf_path} ({contar_paginas(pdf_path)} páginas, impreso con {Path(info).name})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
