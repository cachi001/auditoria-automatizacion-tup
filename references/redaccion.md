# Redacción y formato del JSON

Leé este archivo en la Fase 4, antes de escribir el JSON del informe.

## El JSON (lo único que escribe la IA)

El diseño y el PDF los arma `scripts/render_informe.py`, y las filas de la planilla salen
de este mismo JSON en la Fase 6. Vos escribís solo el contenido, en un archivo
`informe.json`:

```json
{
  "materia": "Programación 1",
  "comision": "10 y 15",
  "rol": "Tutor",
  "nombre": "Nombre Apellido",
  "fecha": "16/11/2026",
  "relevamiento": ["Párrafo 1: qué se repasó y con qué herramientas.", "Párrafo 2: cómo se priorizó y los datos del aula."],
  "tareas": [
    {
      "prioridad": "alta",
      "titulo": "Alumnos que no ingresan al aula",
      "hoy": "La skill lista los alumnos que no entran al aula hace varios días. Lo que necesita la intervención del tutor es avisarles a cada uno.",
      "frecuencia": "Semanal.",
      "tiempo_semanal": "1 a 3 horas",
      "con_que": "con la skill TUP Campus Navigator",
      "por_que": "Los avisos se envían uno por uno y no pueden esperar.",
      "como_automatizar": "Un aviso automático con plantilla a quienes superen una cantidad de días sin ingresar.",
      "unidad": "Todas las unidades",
      "hallazgo": "La skill lista quién no entra al aula; los avisos se envían uno por uno.",
      "automatizable": "Sí",
      "como_corto": "Aviso automático con plantilla según los días sin ingresar.",
      "estado": "Parcial",
      "estado_motivo": "La skill ya arma la lista de quién no entra; avisarles sigue a cargo del tutor.",
      "falta": "un aviso con plantilla que se envíe solo al pasar cierta cantidad de días sin ingresar."
    }
  ],
  "herramientas": [
    {"nombre": "Skill TUP Campus Navigator", "resuelve": "Consulta Moodle: pendientes, mensajes, quién no entra.", "falta": "Redactar y enviar cada mensaje o aviso."},
    {"nombre": "Active-IA", "resuelve": "Corrige las entregas y propone la nota.", "falta": "Revisar cada corrección y los casos especiales."}
  ],
  "conclusion": ["Dónde se va el tiempo.", "Por dónde conviene empezar y por qué."],
  "pasos": false
}
```

- `prioridad`: `alta`, `media` o `baja`. `automatizable`: `Sí`, `No` o `A evaluar`.
  `estado`: `Pendiente`, `Parcial` o `Cubierta`: cuánto cubren hoy las herramientas la
  tarea. El script rechaza otros valores (acepta los nombres viejos `En curso` y
  `Resuelto` y los pasa a `Parcial` y `Cubierta`).
- `tiempo_semanal`: el tiempo que el tutor interviene por semana en esa tarea. Usá una
  de las opciones (`Menos de 1 hora`, `1 a 3 horas`, `3 a 6 horas`, `Más de 6 horas`)
  o un número que haya dicho el tutor (`2 horas`). El script arma con esto la tabla de
  resumen y el total; si una tarea no es semanal, estimá con el tutor cuánto le lleva
  en promedio por semana.
- `con_que`: cómo hace hoy la tarea, según lo que respondió ("con la skill TUP Campus
  Navigator", "a mano en Moodle", "con Active-IA y revisión del tutor"). El informe lo
  muestra junto al tiempo, para que se entienda que ese tiempo no es todo a mano.
- `evidencia`: opcional, y **solo un link real** que te haya pasado el tutor. Nunca
  pongas textos de ejemplo como "Link a captura". Si no hay, dejalo afuera: en la
  planilla va el link del PDF subido (Fase 6).
- `hoy`, `por_que`, `como_automatizar` van en el cuerpo del informe; `hallazgo` y
  `como_corto` son las versiones cortas (una oración) para la fila de la planilla.
- `estado_motivo` y `falta`: completalos en todas las tareas. El informe los muestra
  juntos en la línea del estado ("Parcial. <motivo>. Falta: <falta>.").
  - `estado_motivo`: qué cubre la herramienta y qué sigue haciendo el tutor (en
    Pendiente, que ninguna herramienta cubre la tarea y por qué).
  - `falta`: qué parte todavía no está resuelta para que la tarea deje de necesitar
    al tutor: la pieza concreta (ver los criterios más abajo). Nunca la frase del
    estado dada vuelta.
- `herramientas`: las que usa el tutor, con qué resuelve cada una y qué sigue
  necesitándolo. Arman la tabla de la sección "Qué se considera intervención del tutor".
- `objetivo` es opcional: si no está, el script usa el texto estándar.
- `pasos: true` agrega el recuadro "Pasos para entregar el informe". Dejalo en `false`
  salvo que el tutor arme un informe de guía para otros.
- Ningún campo obligatorio puede quedar vacío: el script lo rechaza, porque en la planilla una
  celda vacía no se entiende.

Los informes de referencia están en `assets/ejemplos/programacion-1.json` y
`assets/ejemplos/programacion-3.json`. Leé uno si dudás del tono o del largo.

## Qué tiene que tener el informe

Cada tarea responde estas siete cosas, y nada más:

1. Qué hace hoy el tutor y con qué (`hoy`, `con_que`).
2. Cada cuánto y cuánto tiempo le lleva (`frecuencia`, `tiempo_semanal`).
3. Por qué le lleva tiempo (`por_que`).
4. Cuánto la cubren las herramientas: qué hace la herramienta y qué hace el tutor
   (`estado`, `estado_motivo`).
5. Qué pieza concreta falta (`falta`).
6. Cómo se podría automatizar (`automatizable`, `como_automatizar`).
7. Qué prioridad tiene (`prioridad`).

En "Cómo se relevó" van solo los datos del aula que se usan en alguna tarea. **Si una
frase o un dato no responde a ninguna de esas preguntas, o no salió del tutor ni de una
tool que lo confirme, no va.** Antes de mostrar el borrador, pasá cada dato del
relevamiento y cada frase de las tareas por esta regla.

Un dato del campus que contradice lo que dijo el tutor (por ejemplo, la cantidad de
avisos del foro incluye los de otros docentes) no se usa: lo que vale es lo que dijo
el tutor sobre su propio trabajo.

## Qué responde el tutor y qué concluye la IA

El tutor cuenta **los hechos de su trabajo**, que solo él sabe: qué tareas hace, cómo
las hace (a mano, con la skill, con Active-IA), cada cuánto y cuánto tiempo le llevan,
y qué consultas se le repiten. **No le preguntes si algo se puede automatizar ni cómo:**
no tiene por qué saberlo. Eso lo concluís vos con estos criterios, y él lo ve en el
borrador:

| Campo | Criterio |
|---|---|
| `estado` | Sale de cómo hace la tarea. **Pendiente**: ninguna herramienta la cubre. **Parcial**: una herramienta hace una parte y el tutor el resto. **Cubierta**: ya no necesita al tutor. |
| `automatizable` | Se mira **solo la parte que todavía hace el tutor** (lo que ya cubre una herramienta no cuenta). **Sí**: hay al menos una pieza concreta de esa parte que se puede automatizar, aunque el tutor siga revisando (por ejemplo, en el TPI Active-IA ya corrige y lo que queda, detectar reentregas, archivos no aceptados o videos fuera de duración, se puede automatizar). **No**: nada de lo que hace el tutor se puede automatizar, porque es todo criterio o trato personal (leer el contenido de un apunte, tomar un oral). **A evaluar**: solo cuando la propuesta depende de algo que todavía no se sabe, como si la plataforma lo permite o una decisión de la cátedra; decí qué hay que averiguar. Que una parte necesite criterio del tutor no la hace "A evaluar". |
| `como_automatizar` | Una propuesta concreta que use lo que ya existe (la skill, Active-IA, plantillas, avisos programados de Moodle) para la parte que hoy hace el tutor. |
| `falta` | La pieza concreta que falta para cubrir la tarea (una plantilla con lo que adeuda cada alumno, el envío automático, una respuesta modelo). Nunca la frase del estado dada vuelta ("que no dependa del tutor"). |
| `prioridad` (propuesta) | **Alta**: lleva tiempo todas las semanas o afecta a toda la comisión (los alumnos que no entran van siempre en Alta). **Media**: frecuente pero acotada. **Baja**: ocasional. El tutor la confirma. |

## Reglas de redacción

- Español rioplatense, voseo, oraciones cortas y directas.
- En "Qué se hace hoy" decí siempre qué resuelve ya la herramienta y qué sigue
  necesitando la intervención del tutor. No describas como "todo a mano" algo que el
  tutor hace con la skill.
- En la conclusión mencioná el tiempo total por semana y cuánto representan las
  tareas de prioridad alta: es el argumento para automatizar. **No lo calcules vos:**
  corré antes `render_informe.py informe.json --solo-html`, que imprime los totales, y
  copiá esos números a la conclusión.
- Conclusiones firmes: decí qué se detectó y qué conviene hacer. No uses "pendiente de
  verificar" ni la palabra "verificar".
- Nada de guiones largos como conector, ni códigos de una letra, ni abreviaturas que
  no se expliquen.
- Solo datos que salieron del campus o del tutor. Nada de horas inventadas ni números
  aproximados que nadie dijo.
- Sin nombres de alumnos.
- Las tareas, prioridades, estados y tiempos son los que confirmó el tutor.
- Entre 5 y 8 tareas. Si salen más, juntá las parecidas.
