# Entrevista y relevamiento por área

Leé este archivo en la Fase 2 y la Fase 3. Para cada área: primero traé los hechos del
aula con la skill `tup-campus-navigator` (todo es de solo lectura), después preguntale
al tutor lo que el campus no sabe.

## Qué cuenta como "trabajo manual"

Todo lo que necesita la intervención del tutor, **aunque use la skill**. Ejemplos:

- Pedirle a la skill los mensajes pendientes, leerlos y escribir cada respuesta.
- Consultar quién adeuda y escribirle a cada alumno lo que le falta.
- Redactar y publicar avisos en el foro, aunque la skill los publique.
- Revisar una corrección hecha con Active-IA antes de publicarla.
- Ver quién no entra al aula y avisarle.

Lo que NO es manual: lo que pasa solo, sin que el tutor haga nada (por ejemplo, un
cuestionario que se corrige solo). Explicale esto al tutor al empezar, porque la
tendencia es decir "eso ya lo hace la skill" y dejarlo afuera.

## Herramientas del campus por área

| Área (bloque) | Hechos que traés con la skill | Qué le preguntás al tutor |
|---|---|---|
| Datos del tutor | `mi_comision(nombre)` (si no lo encuentra: `aulas` + `descubrir_comisiones`) | Rol. Confirmá materia y comisiones. |
| Actividades | `listar_tareas(course_id)`: cuántas tareas hay y de qué tipo (cierres, prácticas, integradores, parciales) | Cuáles le llevan más tiempo y por qué. |
| Seguimiento de atrasados | `alumnos_en_riesgo`, `entregas_tarea`, `sumario` | Cómo les avisa lo que adeudan, cada cuánto, cuánto le lleva. |
| Alumnos que no entran | `sin_entrar_al_aula` | Cómo los contacta y cada cuánto. Recomendá prioridad alta: un alumno que deja de entrar suele no volver si nadie lo contacta. |
| Mensajes y consultas | `mensajes_pendientes(limite=300)`, `foros_pendientes`: cuántos hay y de qué temas son | Qué consultas se repiten (opciones armadas con los temas que viste). |
| Corrección | `pendientes_por_corregir`, `demora_correccion`, `activeia_pendientes` | Cómo corrige, con qué herramienta, qué revisa a mano, casos especiales. |
| Evaluación | `listar_tareas` (parciales, recuperatorios) | Cómo son los parciales: cuestionario, entrega de código, coloquio, turnos. |
| Avisos | `listar_foros(course_id)`: cuántos avisos tiene el foro de la comisión | Qué avisos publica, cada cuánto, cómo controla las fechas. |
| Informes | No hay dato en el campus | Qué informes arma, para quién, cada cuánto. |
| Material del aula | `auditar_aula(course_id, unidad=N)` o el aula entera | Si revisa apuntes, videos o código de ejemplo, y cómo. |
| Otras tareas | — | "¿Hay algo más que hagas seguido y te lleve tiempo?" |

Si una tool falla o devuelve vacío, decilo y preguntale al tutor el dato. Nunca
rellenes un número que no salió del campus o del tutor.

Usá del campus solo **cantidades y hechos del aula** (cantidad de tareas, de avisos,
de links rotos). Nunca pongas nombres de alumnos en el informe. Ojo: `demora_correccion`
devuelve todas las comisiones del curso con el nombre de cada tutor; usá solo las filas
de las comisiones del tutor que estás entrevistando. Y `mi_comision` puede devolver una
sola comisión aunque tenga más (pasó en Programación 1): confirmá siempre con el tutor.

## Conectar el MCP del campus en Codex

En Codex el MCP `moodle-tutor` de `tup-campus-navigator` se registra una vez. Con la
skill del campus instalada en `<carpeta>`:

```bash
codex mcp add moodle-tutor -- "<carpeta>/.venv/Scripts/python.exe" "<carpeta>/mcp/server.py"
```

(En Mac o Linux, el Python del entorno está en `<carpeta>/.venv/bin/python`.) Después
de reiniciar Codex, `codex mcp list` tiene que mostrar `moodle-tutor`. Si el tutor no
lo tiene registrado, ofrecé mostrarle el comando; no lo registres vos sin su OK, porque
cambia la configuración de su Codex.

## Sin la skill del campus

Si el tutor no tiene `tup-campus-navigator` instalada o configurada, hacé la entrevista
igual con las preguntas de la tabla y pedile que te cuente las cantidades que conozca
("¿cuántas tareas tiene el aula, más o menos?"). Para instalarla, mandalo al README de
esa skill. No le pidas su usuario ni su contraseña: eso lo configura la otra skill.

## Cómo preguntar

Usá las **preguntas interactivas** siempre que la respuesta se pueda elegir entre
opciones: el tutor hace clic en vez de escribir, y las respuestas quedan con los
valores exactos que acepta la planilla.

- **Claude Code:** `AskUserQuestion`, hasta 4 preguntas por llamada, de 2 a 4 opciones
  cada una (el tutor siempre puede elegir "Otro" y escribir).
- **Codex:** si la sesión tiene una herramienta para preguntarle al usuario con
  opciones, usala. Si no, escribí las preguntas en texto con las opciones numeradas
  ("1. Diaria  2. Semanal  3. En cada entrega o parcial  4. Ocasional"), pedile que
  responda con el número y **esperá la respuesta antes de seguir**. No supongas la
  respuesta para avanzar.

| Pregunta | Tipo | Opciones |
|---|---|---|
| Rol | Interactiva | Tutor · Profesor · Coordinador |
| Materia (si está en varias) | Interactiva | Las materias que devolvió `mi_comision` |
| Herramientas que usa | Interactiva, selección múltiple | Skill TUP Campus Navigator · Active-IA · Planillas propias · Ninguna |
| ¿Esta tarea te lleva tiempo? (por cada área) | Interactiva | Sí, mucho · Algo · Casi nada · No la hago |
| Frecuencia y tiempo de intervención (juntos, una pregunta) | Interactiva | Ej.: Diaria, mucho tiempo · Diaria, algo de tiempo · Picos en parciales · Semanal (ver el modelo abajo) |
| Prioridad y estado (juntos) | Interactiva, tu propuesta primero con "(Recomendado)" y el porqué | Ej.: Alta / En curso · Alta / Pendiente · Media / En curso |
| Temas o casos de cada área | Interactiva, selección múltiple, armada con lo que viste en el aula | Ej.: Parciales y recuperatorios · TPI y video · Notas y condición · Inicio de cursada |
| ¿Se puede automatizar? | Interactiva | Sí · No · A evaluar |
| Qué hace hoy, por qué lleva tiempo, idea de automatización | Lo redactás vos con sus respuestas y se lo mostrás en el borrador | — |
| OK del borrador | Interactiva | Generar el PDF · Cambiar algo |

Cada pregunta interactiva tiene que entenderse sola: nombrá el área o la tarea en el
texto ("¿Con qué frecuencia avisás a los alumnos que no entran al aula?"), porque el
tutor puede ver solo el cuadro de la pregunta.

### Guiar sin abrumar

- **Una tanda de preguntas por bloque** (los 5 bloques del SKILL.md), hasta 4 juntas.
  El tutor responde con clics.
- **Armá las opciones con el relevamiento.** Así se ve una buena pregunta:

  > Mensajes y consultas (Prog I): hoy tenés 3 mensajes esperando respuesta y las
  > preguntas que se ven son del parcial (zoom, cuestionario, recuperatorio) y del
  > video. ¿Qué consultas se te repiten más?
  > 1. Parciales y recuperatorios: fechas, horarios, zoom, cómo se rinde
  > 2. TPI y video: formato de entrega, video, duplas, README
  > 3. Notas y condición: si promocionó, regulariza, qué le falta
  > 4. Inicio de cursada: instalaciones, cómo usar el aula, Git y Colab

- **Proponé prioridad y estado juntos**, con tu recomendación primero y el porqué:

  > Para la tarea "Seguimiento de atrasados y alumnos que no entran" (Prog I) propongo
  > prioridad Alta y estado En curso (la skill ya te arma la lista, pero vos escribís
  > cada mensaje). ¿Confirmás?
  > 1. Alta / En curso (Recomendado): la skill detecta, vos redactás y enviás
  > 2. Alta / Pendiente: todo es a mano
  > 3. Media / En curso: frecuente pero acotada

  Criterios: **Alta** consume mucho tiempo todas las semanas o afecta a toda la
  comisión; **Media** es frecuente pero acotada; **Baja** es ocasional o ya tiene una
  solución parcial. **Pendiente**: toda la tarea depende del tutor; **En curso**: una
  herramienta ya resuelve una parte; **Resuelto**: ya no necesita su intervención. Lo
  que elija el tutor es lo que va.

  El porqué que das en la pregunta se guarda como **motivo del estado**
  (`estado_motivo`), y sumá **qué falta** para resolverla (`falta`). Ejemplo: motivo
  "La skill ya arma la lista de quién adeuda; escribir y enviar cada mensaje sigue a
  cargo del tutor"; qué falta "que redactar y enviar cada recordatorio no dependa del
  tutor" (la solución concreta va aparte, en "cómo automatizar").
- **Frecuencia y tiempo en una sola pregunta**, con opciones que digan las dos cosas:

  > ¿Con qué frecuencia respondés mensajes privados y consultas de foro de Prog I, y
  > cuánto te lleva?
  > 1. Diaria, mucho tiempo: todos los días, más de 1 hora
  > 2. Diaria, algo de tiempo: todos los días, 20 a 60 minutos
  > 3. Picos en parciales: poco en semanas normales, mucho antes de un parcial o entrega
  > 4. Semanal: una o dos veces por semana

  El tiempo de intervención es el dato que más pesa en el informe. En el JSON va en
  `tiempo_semanal`: pasalo a horas por semana (una de las opciones fijas o "N horas")
  y mostraselo en el borrador para que lo confirme. Si no se puede pasar a horas por
  semana, dejalo como lo dijo: el informe lo muestra igual, pero sin sumarlo al total.
- **Redactá vos** qué hace hoy, por qué le lleva tiempo y cómo se podría automatizar,
  con sus respuestas y lo que viste en el aula. Él lo revisa en el borrador.
- Si un área no la hace o no le lleva tiempo, pasá a la siguiente sin más preguntas.
