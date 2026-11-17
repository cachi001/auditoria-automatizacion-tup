---
name: auditoria-automatizacion-tup
description: >-
  Acompaña a un tutor de la TUP (UTN) a hacer su informe de la auditoría de tareas de
  tutoría: releva su aula con la skill tup-campus-navigator, lo entrevista área por área
  para detectar las tareas que necesitan su intervención y que se podrían automatizar,
  arma el informe en PDF con el estilo de la cátedra y lo carga, con su OK, en el Drive
  y en las planillas de Personas y Hallazgos con los conectores de Google. Usá esta skill cuando el tutor diga "tengo que
  hacer el informe de la auditoría", "ayudame con la auditoría de mi materia", "armame
  el informe de tareas manuales", "qué pongo en la pestaña Hallazgos", "cómo cargo la
  planilla de la auditoría", o pida relevar qué trabajo repetitivo tiene en su comisión,
  aunque no nombre la skill. NO la uses para auditar cómo está armada el aula (eso es
  auditar_aula de tup-campus-navigator), ni para informes de seguimiento de alumnos o
  de corrección, ni para cargar notas.
license: Apache-2.0
---

# Auditoría de Automatización TUP

La IA pregunta, releva y redacta; el script arma el PDF; los conectores de Google cargan
todo en el Drive y la planilla. Así el informe sale siempre igual, con el estilo de la
cátedra, y la IA no gasta tokens en diseño.

---

## Cuándo aplica

Un tutor tiene que entregar su informe de la auditoría: detectar en qué tareas pierde
tiempo con trabajo que necesita su intervención y pensar cómo automatizarlas. El
resultado es un PDF por materia, subido a su carpeta Informes, y sus filas cargadas en
la planilla de esa materia.

**No usar cuando:**
- Quiere revisar si el aula está bien armada (links rotos, componentes faltantes): eso
  es `auditar_aula` de `tup-campus-navigator`. Acá esa revisión es solo un insumo.
- Quiere un informe de seguimiento de alumnos o de pendientes de corrección: eso lo
  arma `tup-campus-navigator`.

---

## Claude Code y Codex

La skill funciona igual en los dos. Lo que cambia:

| | Claude Code | Codex |
|---|---|---|
| Carpeta de la skill | `~/.claude/skills/auditoria-automatizacion-tup` | `~/.agents/skills/auditoria-automatizacion-tup` (instalada con `npx skills`) o `~/.codex/skills/auditoria-automatizacion-tup` |
| Preguntas con opciones | `AskUserQuestion` (preguntas interactivas) | La herramienta para preguntarle al usuario, si la sesión la tiene; si no, texto con las opciones numeradas, y esperá la respuesta antes de seguir |
| Tools del campus | MCP `moodle-tutor` (de `tup-campus-navigator`) | El mismo MCP, registrado en Codex con `codex mcp add` (ver `references/entrevista.md`) |
| Generar el PDF | Corre directo | Si el sandbox no deja abrir el navegador, pedí permiso para correr el script fuera del sandbox |

Las tools del campus tienen los mismos nombres en los dos (`mi_comision`,
`mensajes_pendientes`, etc.). Si no aparecen, el MCP no está conectado: seguí con la
entrevista sin datos del aula.

---

## Fase 1: Presentar y ubicar al tutor

1. Contale en dos líneas qué van a hacer: revisar su aula, unas preguntas por área,
   el PDF y, al final, la carga en la planilla y en el Drive de su materia.
2. Explicale qué cuenta como trabajo manual: **todo lo que necesita su intervención,
   aunque lo haga con la skill del campus**. Consultar los mensajes pendientes y
   responderlos, escribir en los foros, avisar a cada alumno lo que adeuda, revisar
   una corrección de Active-IA. Lo explicás primero porque la tendencia es dejar afuera
   lo que "ya hace la skill", y es justo lo que la auditoría quiere ver.
3. Pedile su nombre y usá `mi_comision(nombre)` de `tup-campus-navigator` para obtener
   materias y comisiones. Confirmá con él. Si está en varias materias, avisale que se
   hace un informe por materia y preguntale por cuál empiezan.
4. Con una pregunta interactiva, preguntale su rol (Tutor, Profesor, Coordinador) y
   qué herramientas usa (selección múltiple: la skill del campus, Active-IA,
   planillas propias, otras). Por cada herramienta que marque, redactá vos qué le
   resuelve y qué sigue necesitándolo, y confirmalo con él: va en la tabla
   "Herramientas que usa el tutor" del informe.

Si `tup-campus-navigator` no está disponible, seguí igual: ver "Sin la skill del
campus" en `references/entrevista.md`.

---

## Fase 2: Relevar el aula (solo lectura)

Leé `references/entrevista.md`. Traé los hechos del aula con las tools de la tabla:
cantidad y tipo de tareas, avisos del foro de la comisión, mensajes y foros pendientes
(y de qué temas son), alumnos que no entran, pendientes de corrección y, si el tutor
quiere, `auditar_aula` de su aula. Todo es de solo lectura: no escribas nada en el campus.

Mostrale un resumen corto de lo que encontraste, con números. Con eso armás las opciones
de la entrevista: el tutor elige y corrige en vez de contar todo de cero.

---

## Fase 3: Entrevista guiada, sin abrumar

Vos guiás: armás las opciones con lo que viste en el aula, proponés la prioridad y
redactás. El tutor elige, corrige y **tiene la última palabra**. El objetivo es que
responda rápido, con clics, y no que escriba párrafos.

Agrupá las áreas de `references/entrevista.md` en **5 bloques**, una tanda de preguntas
por bloque, para que la entrevista dure unas 7 rondas por materia (6 a 8 minutos) y no
abrume:

| Bloque | Áreas |
|---|---|
| 1. Seguimiento | Alumnos atrasados y alumnos que no entran al aula |
| 2. Comunicación | Mensajes privados, consultas de foro y avisos |
| 3. Corrección y evaluación | Correcciones, integradores, parciales, coloquios |
| 4. Informes y material | Informes para coordinación y revisión del material del aula |
| 5. Algo más | "¿Hay algo más que hagas seguido y te lleve tiempo?" |

Por cada bloque:

1. **Una sola tanda de preguntas interactivas** (hasta 4 juntas), con opciones armadas
   desde el relevamiento. Ejemplo: "Hoy tenés 3 mensajes esperando respuesta y las
   preguntas que se ven son del parcial y del video. ¿Qué consultas se te repiten
   más?", con selección múltiple de los temas que viste.
2. En la misma tanda preguntá **cómo hace cada tarea**: qué parte le resuelve la
   skill del campus (o Active-IA) y qué parte sigue haciendo él, aunque sea con la
   skill. Opciones con escenarios ("La skill me arma la lista y yo redacto y envío
   cada mensaje" · "La skill arma y envía, yo reviso" · "A mano en Moodle"). Va en
   `con_que` y es la base del porqué del estado: sin esto, "menos de 1 hora" no dice
   si es a mano o con la skill.
3. En la misma tanda preguntá **frecuencia y tiempo de intervención en una sola
   pregunta**, con opciones que digan las dos cosas ("Diaria, mucho tiempo: todos los
   días, más de 1 hora"). El tiempo es el dato más importante del informe: es lo que
   muestra cuánto se ahorraría automatizando.
4. **Redactá vos** qué hace hoy, por qué le lleva tiempo y cómo se podría automatizar,
   a partir de sus respuestas y de lo que viste en el aula. No le pidas que lo escriba.
5. **Proponé prioridad y estado** en una sola pregunta, con tu propuesta primero y
   "(Recomendado)", y una línea con el porqué. El estado que proponés sale de lo que
   contestó en "cómo la hacés": no lo vuelvas a decidir de cero. Ejemplo: "Para 'Seguimiento de
   atrasados' propongo Alta / Parcial: la skill te arma la lista, pero vos escribís
   cada mensaje. ¿Confirmás?". Lo que elija el tutor es lo que va.
   El estado dice **cuánto cubren hoy las herramientas la tarea**: Pendiente (ninguna
   la cubre), Parcial (una hace una parte y el tutor el resto) o Cubierta (ya no
   necesita al tutor). **Ese porqué dice qué cubre la herramienta y qué sigue haciendo
   el tutor** (`estado_motivo`), y agregá **qué falta** para cubrirla del todo
   (`falta`): el informe los muestra en la línea del estado.
6. Si dice que un área no la hace o no le lleva tiempo, pasá a la siguiente. Si un
   bloque tiene dos tareas que llevan tiempo, la prioridad de la segunda (o su "cómo
   la hacés") puede ir en la tanda del bloque siguiente, para no pasar de 4 preguntas.

En el bloque 5 suelen aparecer las tareas propias de cada materia (coloquios, videos,
entornos de trabajo). Si el tutor está en varias materias, en la segunda no repitas
lo que ya contestó igual (herramientas, rol): preguntá solo lo que cambia. Usá **preguntas interactivas** (`AskUserQuestion` en Claude Code; en Codex, ver la
tabla de arriba); texto libre solo cuando ninguna opción le sirva. Si el tutor deja una
tanda sin responder, preguntale una sola vez si prefiere seguir otro momento; no
insistas.

---

## Fase 4: Borrador y aprobación

1. Leé `references/redaccion.md` y escribí `informe.json` en la carpeta de trabajo del
   tutor, con entre 5 y 8 tareas. Solo entran las tareas que el tutor confirmó, con la
   prioridad, el estado y el tiempo que eligió.
2. Mostrale al tutor un resumen en el chat: las tareas por prioridad, una línea cada
   una con su tiempo por semana **y con qué lo hace** ("Menos de 1 hora, con la
   skill"), **el estado con su porqué y qué falta** (un estado solo no le dice nada),
   el total y la conclusión. **Esperá su OK antes de generar el PDF**, con una pregunta
   interactiva: "Generar el PDF" o "Cambiar algo". Si pide cambios,
   corregí el JSON, no el PDF.

---

## Fase 5: Generar el PDF

```bash
python <carpeta de esta skill>/scripts/render_informe.py informe.json
```

El script valida el JSON y arma el PDF con el estilo de la cátedra (Chrome o Edge en
modo headless). No genera archivos para las planillas: las filas las cargás en la
Fase 6 desde el mismo JSON.

- Si devuelve errores de contenido (exit 1), corregí el JSON y volvé a correrlo.
- Si no encuentra navegador (exit 2), queda el HTML: explicale al tutor cómo
  imprimirlo como PDF (Ctrl+P, Guardar como PDF, sin encabezados ni pies de página).
- Chequeá la cantidad de páginas que informa el script (lo normal son 4 a 6). Si
  tenés cómo ver el PDF, miralo antes de entregarlo.

---

## Fase 6: Cargar las planillas y entregar

Leé `references/planillas.md`. Lo recomendado es cargar todo con los **conectores de
Google Drive y Google Sheets**, para que el tutor no tenga que copiar nada:

1. Fijate si la sesión tiene esos conectores. Si no, explicale cómo activarlos (la
   referencia dice cómo en Claude Code y en Codex) o seguí con la carga a mano.
2. **Compuerta:** mostrale exactamente qué vas a escribir y dónde (fila de Personas,
   filas de Hallazgos, nombre del PDF) y esperá su OK con una pregunta interactiva. Son
   planillas compartidas por todos los tutores.
3. Con el OK: fila en Personas, PDF a la carpeta Informes de su materia, "Sí", fecha y
   link en Personas, filas en Hallazgos. Después leé de nuevo lo escrito y mostrale
   los links.
4. Credenciales: que cargue él mismo su fila en la planilla de credenciales, una sola
   vez. **Nunca le pidas su usuario ni su contraseña para escribirlos vos.**

Sin conectores, guialo a mano como dice la referencia: las filas van en el chat,
listas para pegar; no generes archivos aparte.

Si está en otra materia, volvé a la Fase 2 con esa materia.

---

## Reglas

- **Solo lectura en el campus.** La auditoría no manda mensajes ni publica nada: las
  tools de escritura de `tup-campus-navigator` no se usan acá.
- **La IA propone, el tutor decide.** Vos armás las opciones, redactás y recomendás;
  la última decisión es del tutor. Si no la confirmó, no está en el informe.
- **El tutor cuenta los hechos, la IA concluye con criterios.** Él dice qué hace, con
  qué, cada cuánto y cuánto tiempo. Si se puede automatizar, cómo, qué falta y el
  estado los concluís vos con los criterios fijos de `references/redaccion.md`, para
  que todos los informes salgan con la misma vara. No le preguntes lo que no tiene por
  qué saber.
- **Cada frase y cada dato responden a algo.** El informe tiene lo que dice "Qué tiene
  que tener el informe" en `references/redaccion.md`; lo demás no va.
- **Pocas preguntas.** Una tanda interactiva por área; lo demás lo redactás vos.
- **Nada inventado.** Cada número sale del campus o del tutor. Si una tool falla o
  devuelve vacío, decilo y preguntá; un 0 puede ser "no hay" o "no se relevó".
- **Sin nombres de alumnos** en el informe ni en las filas: el informe circula entre
  tutores y coordinación.
- **La IA no toca el diseño.** El estilo vive en `assets/estilo.css` y lo aplica el
  script. Si el tutor pide otro formato, decile que el informe tiene que quedar igual
  para todos.
- **Un informe por materia.** Si está en varias, se repite el flujo por cada una.
- **Nada se escribe en el Drive ni en las planillas sin el OK del tutor.**

---

## Recursos

- `references/entrevista.md`: qué es trabajo manual, tools del campus por área,
  preguntas y criterios de prioridad. Leelo en las Fases 2 y 3.
- `references/redaccion.md`: formato del JSON y reglas de redacción. Leelo en la Fase 4.
- `references/planillas.md`: IDs, columnas y carga con los conectores de Google (o a
  mano). Leelo en la Fase 6.
- `scripts/render_informe.py`: JSON a PDF (sin IA).
- `assets/estilo.css`: el estilo de los informes.
- `assets/ejemplos/programacion-1.json` y `assets/ejemplos/programacion-3.json`: dos
  informes reales de referencia.
