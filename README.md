# auditoria-automatizacion-tup

Skill para que cada tutor de la TUP haga su **informe de la auditoría de tareas de
tutoría** combinando **el relevamiento del aula con tup-campus-navigator**, **una
entrevista guiada** y **un PDF con el estilo de la cátedra** generado por script.

> "La IA pregunta, releva y redacta; el script arma el PDF; los conectores cargan todo."

---

## ¿Qué hace?

1. **Ubica al tutor**: con su nombre obtiene materias y comisiones, y le explica qué
   cuenta como trabajo manual (todo lo que necesita su intervención, aunque use la skill).
2. **Releva el aula**: trae del campus, en solo lectura, la cantidad de tareas, avisos,
   mensajes y foros pendientes, alumnos que no entran y pendientes de corrección.
3. **Entrevista por área**: seguimiento, alumnos que no entran, consultas, corrección,
   evaluación, avisos, informes, material y particularidades de la materia.
4. **Arma el borrador** y espera el OK del tutor.
5. **Genera el PDF** con el estilo de la cátedra.
6. **Carga todo con su OK**: sube el PDF a la carpeta Informes y escribe las filas en
   las pestañas Personas y Hallazgos con los conectores de Google Drive y Google
   Sheets. Sin conectores, lo guía para hacerlo a mano.

## Instalación

Funciona en **Claude Code** y en **Codex**.

```bash
npx skills add https://github.com/cachi001/auditoria-automatizacion-tup
```

El instalador pregunta en qué agentes instalarla: elegí Claude Code, Codex o los dos.
Para instalarla directo, sin preguntas:

```bash
npx skills add https://github.com/cachi001/auditoria-automatizacion-tup -g -a claude-code -a codex -y
```

Queda en `~/.claude/skills/` para Claude Code y en `~/.agents/skills/` para Codex.
También se puede copiar la carpeta a mano en `~/.claude/skills/` o `~/.codex/skills/`.

En Codex, la skill del campus se conecta registrando su MCP una vez:

```bash
codex mcp add moodle-tutor -- "<carpeta de tup-campus-navigator>/.venv/Scripts/python.exe" "<carpeta de tup-campus-navigator>/mcp/server.py"
```

Necesita:
- Python 3.10 o superior (sin paquetes extra).
- Google Chrome o Microsoft Edge (para imprimir el PDF).
- La skill `tup-campus-navigator` configurada, para relevar el aula. Sin ella la skill
  funciona igual, pero los datos del aula los cuenta el tutor.
- Para cargar todo sin copiar nada: los conectores de Google Drive y Google Sheets. En
  Claude Code se activan en claude.ai (Configuración, Conectores) con la misma cuenta.

## Uso

> "Tengo que hacer el informe de la auditoría de Programación 3"

El agente revisa el aula, hace las preguntas de a un área, muestra el borrador, genera
`Informe Auditoria Programacion 3.pdf` y, con tu OK, lo sube y carga las filas en la
planilla de tu materia.

## Estructura

```
auditoria-automatizacion-tup/
├── SKILL.md
├── README.md
├── LICENSE
├── agents/
│   └── openai.yaml        # nombre y prompt de ejemplo en la interfaz de Codex
├── references/
│   ├── entrevista.md      # trabajo manual, tools por área, preguntas y MCP en Codex
│   ├── redaccion.md       # formato del JSON y reglas de redacción
│   └── planillas.md       # IDs, columnas y carga con los conectores de Google
├── scripts/
│   └── render_informe.py  # JSON a PDF
└── assets/
    ├── estilo.css         # estilo de los informes
    └── ejemplos/          # dos informes reales de referencia
```

## Por qué esta estructura

- **El diseño lo arma un script**: la IA escribe un JSON chico con el contenido y
  `render_informe.py` produce siempre el mismo PDF. Ahorra tokens y todos los informes
  quedan iguales.
- **Las filas salen del mismo JSON**: lo que dice el informe y lo que se carga en la
  planilla nunca se contradicen, y se escriben directo con los conectores.
- **Las referencias se cargan por fase**: la entrevista, la redacción y las planillas
  se leen solo cuando hacen falta.
- **Solo lectura en el campus**: la auditoría no manda mensajes ni publica nada.

## Licencia

Apache-2.0
