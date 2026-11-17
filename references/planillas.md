# Planillas y carpetas de la auditoría

Leé este archivo en la Fase 6. Lo ideal es cargar todo con los conectores de Google
Drive y Google Sheets; si no están, guiás al tutor para hacerlo a mano.

## Links e IDs

Credenciales de Moodle: hay una sola planilla para todas las materias, y la carga el
tutor. **Su link no está en esta skill a propósito**: circula solo por el grupo de
tutores. Si el tutor no lo tiene, que lo pida por el grupo.

| Materia | Carpeta | Carpeta Informes (ID) | Planilla de seguimiento (ID) |
|---|---|---|---|
| Programación 1 | https://drive.google.com/drive/folders/1ryR8SSV1Wv695XNHrYzlkC0dOeQhosUG | `1_P6UNmMoJkULKuLgKI_BnYfnnu8vDh6N` | `1tzsiQuVSCCcoElQB9Fwfc3WzPUuIgKHMNavNB1WsBSs` |
| Programación 2 | https://drive.google.com/drive/folders/13TcFSWTrz1C-jjA5U8VyhnawDvzPT_rT | `1rOlI-VyLl2ujtY9hR7KRI55HDJanUfsM` | `1WhDrBh15J3B8KrpEL8DZIsSl5rAM_p4SmrO8TvwHedc` |
| Programación 3 | https://drive.google.com/drive/folders/10ldJn7hgrd-NI3xC0gQqApAEC6dK5DB_ | `1Wa7QWt_o1EmjNrnwrIJqVCTjNzEPIyGD` | `178g_dGzHyw8w3-RaC4AuQ4XJ7utJ882CIr1Ren73CPI` |
| Programación 4 | https://drive.google.com/drive/folders/1-HJg9DDfkNBxWf1Eu6N2zRL2LwBH5l3y | `1OL8_xkO0KPcGOJsbxIL3mNa2UxreeAg0` | `1gm2KM8GmaXeeqVY6mfL9KbvtTWfscI9IqIKLHim_bYw` |

Si el tutor está en varias materias, hace todo una vez por materia (fila en Personas,
informe y hallazgos), salvo las credenciales, que se cargan una sola vez.

## Estructura de cada planilla de materia

Pestañas con el número de la materia en el nombre (`Personas Programación 1`,
`Hallazgos Programación 1`). En las dos, los datos arrancan en la **fila 5**.

**Personas Programación N**

| A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|
| Nombre y apellido | Rol | Comisión | ¿Subió el informe? (Sí/No) | Fecha de entrega | Link al informe | Hallazgos cargados | Observaciones |

La columna G tiene una fórmula que cuenta sola los hallazgos: **no escribas en G**.

**Hallazgos Programación N**

| A | B | C | D | E | F | G | H | I |
|---|---|---|---|---|---|---|---|---|
| Fecha | Nombre y apellido | Unidad o actividad | Hallazgo | Evidencia (link) | Prioridad | ¿Automatizable? | Cómo se podría automatizar | Estado |

Del JSON salen así: `fecha`, `nombre`, `unidad`, `hallazgo`, evidencia (el
`evidencia` de la tarea si el tutor pasó un link real; si no, el link del PDF subido),
prioridad (`Alta`/`Media`/`Baja`, con mayúscula), `automatizable`, `como_corto`,
`estado`. El nombre de la columna B se elige de una lista armada con la pestaña
Personas, así que **Personas va primero** y el nombre tiene que ser idéntico.

## Con los conectores de Google (lo recomendado)

**Antes de empezar**, fijate si la sesión tiene herramientas de Google Drive (crear o
subir archivos) y de Google Sheets (leer y escribir valores).

- **Claude Code:** son los conectores de claude.ai. Si no aparecen, decile al tutor que
  los active en claude.ai (Configuración, Conectores, Google Drive y Google Sheets) con
  la misma cuenta con la que usa Claude Code, y que reinicie la sesión.
- **Codex:** usá los conectores o servidores MCP de Google Drive y Sheets si la sesión
  los tiene. Si no los tiene, seguí con la carga a mano (más abajo).

**Compuerta de aprobación.** Son planillas compartidas por todos los tutores. Antes de
escribir, mostrale al tutor exactamente qué vas a cargar y dónde (la fila de Personas,
las filas de Hallazgos y el nombre del PDF) y esperá su OK con una pregunta interactiva
("Cargar todo" / "Cambiar algo"). Nunca escribas sin ese OK.

**Pasos, en este orden:**

1. **Personas.** Leé `A5:H` de la pestaña Personas. Si el nombre del tutor ya está, usá
   esa fila; si no, la primera fila vacía desde la 5. Escribí `A:C` (nombre, rol,
   comisión).
2. **Subir el PDF** a la carpeta Informes de la materia, con el nombre
   `Informe Auditoria Programacion N - Nombre Apellido.pdf` (así no se pisan los de
   distintos tutores), como PDF y sin convertirlo a documento de Google. En Claude Code,
   la herramienta de crear archivos acepta una referencia al archivo local en vez del
   contenido en base64. Si el conector no permite subir el archivo, pedile al tutor que
   lo suba él y que te pase el link.
3. **Completar Personas** en la misma fila: `D` = `Sí`, `E` = la fecha, `F` = el link
   del PDF.
4. **Hallazgos.** Leé la columna `A` desde la fila 5 para encontrar la primera fila
   vacía. Si ya hay filas de este tutor (por ejemplo, de una carga anterior),
   preguntale si las reemplazás o agregás las nuevas. Escribí todas las tareas en
   `A:I`, una fila por tarea. La comisión no va: ya está en la fila de Personas.
5. **Comprobá** leyendo de nuevo los rangos que escribiste, y mostrale al tutor los
   links del PDF y de la planilla. Si algo no quedó, decilo; no lo des por cargado.

Escribí los valores como texto (sin fórmulas) y leé antes de escribir, para no pisar
datos de otro tutor.

## Sin conectores (carga a mano)

No generes archivos aparte. Guialo así:

1. Mostrale en el chat, dentro de un bloque de código, la fila de Personas y las de
   Hallazgos con los valores separados por tabulaciones. Al pegar un bloque así en la
   columna A de la primera fila vacía, Google Sheets reparte cada valor en su columna.
2. Que pegue primero Personas y después Hallazgos.
3. Que suba el PDF a la carpeta Informes de su materia, copie el link (Compartir,
   Copiar vínculo) y en Personas marque "Sí", la fecha y el link.

## Credenciales

La planilla de credenciales la carga **el tutor con sus propias manos**, una sola vez,
con el link que se compartió por el grupo de tutores (no está en esta skill):
nombre, rol, las casillas de sus materias, usuario y contraseña de Moodle. Nunca le
pidas el usuario ni la contraseña, ni los escribas con un conector.
