# auditoria-automatizacion-tup

Skill para que cada tutor de la TUP arme su **informe de la auditoría de tareas de
tutoría** en pocos minutos: revisa tu aula, te hace unas preguntas, arma el **PDF con
el estilo de la cátedra** y, con tu OK, lo **carga en el Drive y en la planilla** de tu
materia.

> "La IA pregunta, revisa y redacta; vos elegís y decidís."

---

## ¿Qué hace?

La auditoría busca las tareas de tutoría que **necesitan tu intervención**, aunque una
herramienta haga una parte (consultar pendientes con la skill del campus, revisar una
corrección de Active-IA, escribir cada aviso), para pensar cómo automatizarlas.

1. **Te ubica:** con tu nombre encuentra tus materias y comisiones, y te las confirma.
2. **Revisa tu aula** en el campus, sin modificar nada: tareas, mensajes y foros sin
   responder, alumnos que no entran, correcciones pendientes.
3. **Te propone y vos confirmás:** con lo que vio en tu aula te propone qué tareas
   hacés, cómo las hacés y cuánto te llevan, y respondés con clics. Si algo es
   distinto en tu caso, lo agregás. Te propone la prioridad de cada tarea y vos
   decidís.
4. **Te muestra el borrador** y espera tu OK.
5. **Genera el PDF** con el estilo de la cátedra.
6. **Carga todo con tu OK:** sube el PDF a la carpeta Informes de tu materia y completa
   tu fila en la pestaña Personas y tus tareas en la pestaña Hallazgos.

La entrevista lleva unos 3 minutos por materia: la skill propone y vos confirmás. Si estás en varias materias, se
hace un informe por cada una.

## Antes de empezar

Necesitás:

- **Claude Code o Codex** instalado.
- **Python 3.10 o superior** (no hace falta instalar paquetes).
- **Google Chrome o Microsoft Edge**, para generar el PDF.
- **La skill `tup-campus-navigator` configurada**, para revisar tu aula. Sin ella la
  skill funciona igual, pero los datos del aula los contás vos.
- **Los conectores de Google Drive y Google Sheets** (recomendado), para que la carga
  sea automática. En Claude Code se activan en claude.ai, en Configuración, Conectores,
  con la misma cuenta con la que usás Claude Code. Sin ellos, la skill te deja las
  filas listas para pegar.

## Instalación

En una terminal:

```bash
npx skills add https://github.com/cachi001/auditoria-automatizacion-tup
```

El instalador te pregunta en qué agente instalarla: elegí **Claude Code**, **Codex** o
los dos. Para instalarla en los dos sin preguntas:

```bash
npx skills add https://github.com/cachi001/auditoria-automatizacion-tup -g -a claude-code -a codex -y
```

### Solo en Codex: conectar la skill del campus

Claude Code ya usa la skill del campus si la tenés configurada. En Codex hay que
registrarla una vez, reemplazando `<carpeta>` por la carpeta donde está instalada
`tup-campus-navigator`:

```bash
# Windows
codex mcp add moodle-tutor -- "<carpeta>/.venv/Scripts/python.exe" "<carpeta>/mcp/server.py"

# Mac o Linux
codex mcp add moodle-tutor -- "<carpeta>/.venv/bin/python" "<carpeta>/mcp/server.py"
```

Reiniciá Codex y fijate con `codex mcp list` que aparezca `moodle-tutor`.

## Uso

Abrí Claude Code o Codex en la carpeta donde quieras guardar el informe y escribí, por
ejemplo:

> "Tengo que hacer el informe de la auditoría de Programación 3"

Al terminar vas a tener:

- `Informe Auditoria Programacion 3.pdf` en esa carpeta.
- El mismo PDF en la carpeta Informes de tu materia.
- Tu fila en la pestaña Personas, con "Sí" en "¿Subió el informe?" y el link.
- Una fila por tarea en la pestaña Hallazgos.

**Las credenciales de Moodle las cargás vos**, una sola vez, con el link de la planilla
de credenciales que se compartió por el grupo de tutores. La skill nunca te pide tu
usuario ni tu contraseña.

## Preguntas frecuentes

- **¿Cambia algo en el campus?** No. La skill solo lee el aula: no manda mensajes ni
  publica nada.
- **¿Escribe en la planilla sin preguntarme?** No. Antes de cargar te muestra qué va a
  escribir y dónde, y espera tu OK.
- **¿Puedo cambiar lo que redactó?** Sí. En el borrador pedís los cambios y vuelve a
  generar el PDF.
- **No tengo los conectores de Google.** La skill te deja las filas en el chat, listas
  para pegar en la planilla, y te explica cómo subir el PDF.
- **No tengo Chrome ni Edge.** La skill deja el informe como página web para que lo
  imprimas como PDF desde cualquier navegador.

## Estructura

```
auditoria-automatizacion-tup/
├── SKILL.md               # instrucciones para el agente
├── README.md
├── LICENSE
├── agents/
│   └── openai.yaml        # nombre y prompt de ejemplo en la interfaz de Codex
├── references/
│   ├── entrevista.md      # qué cuenta como intervención, bloques y preguntas
│   ├── redaccion.md       # formato del contenido y reglas de redacción
│   └── planillas.md       # carpetas, columnas y carga con los conectores de Google
├── scripts/
│   └── render_informe.py  # arma el PDF a partir del contenido
└── assets/
    ├── estilo.css         # estilo de los informes
    └── ejemplos/          # dos informes completos de referencia
```

## Por qué esta estructura

- **El diseño lo arma un script:** la IA escribe solo el contenido (un JSON chico) y
  `render_informe.py` produce siempre el mismo PDF. Ahorra tokens y todos los informes
  quedan iguales.
- **El informe y la planilla salen del mismo contenido:** lo que dice el PDF y lo que
  se carga en Hallazgos nunca se contradicen.
- **Las referencias se leen por etapa:** la entrevista, la redacción y la carga se
  cargan solo cuando hacen falta.
- **Solo lectura en el campus:** la auditoría no toca el aula de nadie.

## Licencia

Apache-2.0
