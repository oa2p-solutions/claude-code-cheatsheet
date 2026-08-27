# Cheatsheet de Claude Code — Comandos `/`, sintaxis y atajos

> **Versión de referencia:** Claude Code `2.1.247` (macOS, arm64).
> **Fuente:** inventario extraído directamente del binario instalado en esta máquina
> (`~/.local/share/claude/versions/2.1.247`), no de la documentación pública.
> Por eso incluye comandos que el [cheatsheet oficial](https://support.claude.com/en/articles/14553413-claude-code-cheatsheet) no lista.

---

## 0. Cómo leer esta guía

### Por qué `/help` no te muestra todo

Cada comando tiene una condición `isEnabled` y otra `isHidden`. Un comando puede existir y **no aparecer** en el autocompletado por cualquiera de estas razones:

| Razón | Ejemplo |
|---|---|
| No estás en un repositorio git | `/commit`, `/pr`, `/security-review` desaparecen |
| Tu plan no lo incluye | `/upgrade`, `/usage-credits`, `/passes` |
| Falta el entorno/integración | `/setup-bedrock`, `/chrome`, `/desktop`, `/mobile` |
| Está detrás de un feature flag | `/advisor`, `/brief`, `/btw`, `/sandbox` |
| Solo aplica en sesión remota/background | `/stop`, `/session`, `/remote-env`, `/teleport` |
| Es interno o de diagnóstico | `/heapdump`, `/workflow-launch-exec`, `/rate-limit-options` |
| Es una skill deshabilitada | cualquier `/nombre-de-skill` apagada en `/config` |

**Regla práctica:** escribe `/` y lee la lista; si un comando de esta guía no aparece, es que su condición no se cumple ahora mismo. Escribirlo igualmente suele devolver un mensaje explicando qué falta.

### Marcas usadas en las tablas

| Marca | Significado |
|---|---|
| ⭐ | De uso diario, apréndelo primero |
| 🔒 | Oculto o condicional: solo aparece si se cumple su condición |
| 🧩 | Es una *skill* (prompt), no un comando nativo: puede invocarlo también el modelo |
| ☁️ | Ejecuta trabajo fuera de tu terminal (nube / background) |
| ⚠️ | Destructivo o difícil de revertir: lee la nota |

### Los tres tipos de comando

| Tipo | Qué hace | Cómo se comporta |
|---|---|---|
| `local` / `local-jsx` | Código del CLI | Efecto inmediato, **no consume tokens** |
| `prompt` (skill) | Inyecta instrucciones en la conversación | Consume tokens; el modelo trabaja |
| Tuyo (`.claude/commands/*.md`) | Plantilla de prompt que tú escribes | Igual que una skill (§17) |

Los del primer grupo son gratis: úsalos sin miedo. Los del segundo arrancan un turno real del modelo.

---

## 1. Lo esencial: los 12 que resuelven el 90%

```
/clear        → empezar limpio (la sesión anterior queda guardada)
/compact      → resumir para liberar contexto y seguir en el mismo hilo
/context      → ver cuánto contexto queda antes de tener que decidir
/resume       → volver a una conversación anterior
/rewind       → deshacer código y/o conversación a un punto anterior
/model        → cambiar de modelo
/effort       → subir o bajar el esfuerzo de razonamiento
/plan         → planificar antes de tocar código
/permissions  → dejar de aprobar lo mismo una y otra vez
/config       → todos los ajustes en un sitio
/tasks        → ver qué corre en background
/doctor       → cuando algo va raro
```

---

## 2. Sesión y contexto

| Comando | Alias | Qué hace | Ejemplo | Cuándo usarlo |
|---|---|---|---|---|
| ⭐ `/clear [nombre]` | `/reset`, `/new` | Nueva sesión con contexto vacío; la anterior **queda en disco** y es recuperable con `/resume` | `/clear`<br>`/clear refactor-auth` | Al cambiar de tarea. Es la opción por defecto: más barato y más fiable que arrastrar contexto irrelevante |
| ⭐ `/compact [instrucciones]` | — | Resume la conversación hasta aquí para liberar contexto, **sin perder el hilo** | `/compact`<br>`/compact conserva los nombres de archivo y el diseño del esquema, olvida la exploración` | Estás en medio de una tarea larga y el contexto se llena. Con instrucciones explícitas el resumen es mucho mejor |
| `/autocompact [auto\|<tokens>]` | — | Configura a qué nivel de llenado se auto-resume | `/autocompact auto`<br>`/autocompact 400k` | Si el auto-compact te corta demasiado pronto (súbelo) o si prefieres compactar antes para respuestas más rápidas (bájalo) |
| ⭐ `/context [all]` | — | Cuadrícula de colores con el uso de contexto por categoría | `/context`<br>`/context all` | Antes de empezar algo grande, o cuando notas que responde peor. Te dice si el problema es contexto lleno o skills/MCP comiéndoselo |
| ⭐ `/resume [id o texto]` | `/continue` | Reanuda una conversación anterior; busca por texto | `/resume`<br>`/resume migración prisma` | Retomar el trabajo de ayer sin re-explicar nada |
| ⭐ `/rewind` ⚠️ | `/checkpoint`, `/undo` | Restaura **el código y/o la conversación** a un punto anterior | `/rewind` (elige el punto en la lista) | Claude hizo cambios que no querías. Es el "ctrl+Z" real: revierte archivos, no solo el chat. Puedes elegir revertir solo código, solo conversación, o ambos |
| `/branch [nombre]` | — | Crea una **rama de la conversación** en este punto | `/branch probar-con-redis` | Quieres explorar una alternativa sin perder el hilo actual. La rama original sigue intacta |
| `/fork [prompt]` ☁️ | — | Copia la conversación a una sesión en **background** y tú sigues aquí | `/fork escribe los tests de todo lo que acabamos de tocar` | Delegar la parte mecánica con el contexto completo mientras tú avanzas en otra cosa |
| `/subtask <tarea>` | — | Manda un **subagente** con tu contexto completo; el resultado vuelve a este chat | `/subtask audita todos los usos de fetch() y dime cuáles no manejan errores` | Trabajo de exploración/lectura pesado cuyo resultado quieres aquí, pero cuyo ruido no quieres en tu contexto |
| `/btw [pregunta]` 🔒 | — | Pregunta lateral rápida **sin interrumpir** la conversación principal | `/btw ¿qué hace exactamente git restore --staged?` | Duda tangencial a mitad de una tarea; no contamina el hilo |
| `/recap` | — | Genera un resumen de una línea de la sesión | `/recap` | Antes de cerrar, para dejar rastro de en qué ibas |
| `/export [archivo]` | — | Exporta la conversación a archivo o portapapeles | `/export`<br>`/export debug-sesion.md` | Compartir el razonamiento con un compañero o adjuntarlo a un ticket |
| `/copy [N]` | — | Copia la última respuesta al portapapeles (o la N-ésima más reciente) | `/copy`<br>`/copy 3` | Pegar un bloque de código o una explicación en Slack/Jira |
| `/rename [nombre]` | `/name` | Renombra la conversación | `/rename fix-login-safari` | Para encontrarla luego con `/resume` |
| `/focus` | — | Vista enfocada: solo tu prompt, el resumen y la respuesta | `/focus` | Sesiones muy largas donde el ruido de herramientas te distrae |
| `/brief` 🔒 | — | Modo brief-only: respuestas mínimas | `/brief` | Tareas mecánicas donde no quieres explicaciones |
| `/diff` | — | Panel de cambios sin commitear y diffs por turno | `/diff` | Revisar qué tocó Claude antes de aceptar o commitear |
| `/stop` 🔒 ☁️ | — | Detiene esta sesión de background (se conservan transcript y worktree) | `/stop` | Solo dentro de una sesión en background |

### 2.1 Guía de decisión: contexto lleno o error cometido

```
¿Cambias de tarea?
   └─ Sí ──────────────────────────────► /clear
   └─ No, sigo en la misma tarea
        │
        ├─ Contexto lleno pero el hilo importa ──► /compact "qué conservar"
        ├─ Quiero probar otro camino ────────────► /branch
        ├─ Quiero delegar y seguir yo ───────────► /fork  o  /subtask
        └─ Claude rompió algo ───────────────────► /rewind
```

Diferencias que se confunden a menudo:

| | Contexto | Dónde corre | Resultado |
|---|---|---|---|
| `/branch` | Copia completa | Aquí (cambias a la rama) | Tú sigues en la rama |
| `/fork` | Copia completa | Background | Tú te quedas en el hilo original |
| `/subtask` | Copia completa | Subagente | El resultado vuelve a este chat |
| `/btw` | Aislado | Aquí, aparte | No toca el hilo principal |
| `/clear` | Vacío | Aquí | Sesión nueva, la vieja en disco |

---

## 3. Modelo, esfuerzo y planificación

| Comando | Qué hace | Ejemplo | Cuándo usarlo |
|---|---|---|---|
| ⭐ `/model [modelo]` | Fija el modelo de la sesión | `/model`<br>`/model opus`<br>`/model claude-sonnet-5` | Opus para diseño/depuración difícil; Sonnet para volumen; Haiku para tareas mecánicas |
| ⭐ `/effort [nivel]` | Nivel de razonamiento: `low`, `medium`, `high`, `xhigh`, `max` | `/effort high`<br>`/effort low` | Sube a `high`/`max` en bugs de concurrencia o arquitectura; baja a `low` en renombrados y formateos (más rápido y barato) |
| `/fast [on\|off]` | Modo rápido: **el mismo Opus** con salida más rápida (no degrada a un modelo menor) | `/fast on` | Iteración conversacional donde la latencia molesta más que la profundidad |
| `/advisor [<modelo>\|off]` 🔒 | Deja que Claude consulte un modelo más fuerte en momentos clave | `/advisor` | Sesión larga con un modelo rápido donde quieres una segunda opinión en las decisiones importantes |
| ⭐ `/plan [open\|share\|<desc>]` | Activa plan mode o muestra el plan de la sesión | `/plan`<br>`/plan migrar el módulo de pagos a Stripe v3`<br>`/plan share` | **Antes de cualquier cambio no trivial.** En plan mode Claude investiga y propone, sin escribir. También con `Shift+Tab` |
| `/goal [<condición>\|clear]` | Fija un objetivo que Claude comprueba **antes de parar** | `/goal los tests de integración pasan en verde`<br>`/goal clear` | Tarea con criterio de éxito verificable y varios intentos previsibles. Evita el "¿sigo?" cada dos minutos |
| `/ultraplan <prompt>` 🔒 ☁️ | Claude Code en la web redacta un plan editable que puedes aprobar | `/ultraplan rediseñar el sistema de colas` | Planificación grande que quieres revisar con calma y compartir; corre en la nube y tú sigues trabajando |
| `/ultrareview` 🔒 ☁️ | Busca y **verifica** bugs de tu rama en la nube | `/ultrareview` | Antes de un PR importante; más exhaustivo que `/code-review` local |

> **Ojo con el coste:** `/effort max` y `/model opus` multiplican el gasto. Revisa con `/usage`.

---

## 4. Configuración, permisos y hooks

| Comando | Alias | Qué hace | Ejemplo | Cuándo usarlo |
|---|---|---|---|---|
| ⭐ `/config [key=value]` | `/settings` | Abre los ajustes; o fija uno directamente | `/config`<br>`/config theme=dark` | Punto de entrada a casi todo. Aquí viven el editor mode (antes `/vim`), el output style, el tamaño de workflows, etc. |
| ⭐ `/permissions [open\|share\|<desc>]` | `/allowed-tools` | Gestiona reglas allow/deny de herramientas | `/permissions`<br>`/permissions permite npm test y npm run lint` | **Cuando te cansas de aprobar lo mismo.** `share` genera reglas para compartir con el equipo |
| `/hooks [nombre]` | — | Ver la configuración de hooks por evento | `/hooks` | Diagnosticar por qué algo se dispara (o no) automáticamente |
| `/sandbox` 🔒 | — | Estado y configuración del sandbox de ejecución | `/sandbox` | Verificar si los comandos corren aislados antes de dar permisos amplios |
| `/theme` | — | Cambia el tema de colores | `/theme` | — |
| `/tui [default\|fullscreen]` | — | Renderer de la interfaz de terminal | `/tui fullscreen` | `fullscreen` da una experiencia tipo aplicación; `default` respeta el scroll del terminal |
| `/color [<color>\|default]` | — | Color de la barra de prompt **de esta sesión** | `/color red` | Distinguir de un vistazo varias terminales abiertas (prod vs local) |
| `/statusline` 🧩 | — | Configura la línea de estado (crea el script y lo escribe en settings) | `/statusline muestra la rama de git y el modelo` | Ver rama, modelo o contexto sin ejecutar comandos |
| `/keybindings` | — | Abre tu archivo de atajos (`~/.claude/keybindings.json`) | `/keybindings` | Rebindear teclas (§16) |
| `/keybindings-help` 🧩 | — | Ayuda guiada para escribir atajos, incluidos *chords* | `/keybindings-help quiero ctrl+s para stash` | Cuando no sabes la sintaxis del JSON |
| `/scroll-speed` | — | Velocidad de la rueda del ratón | `/scroll-speed` | — |
| `/terminal-setup` | — | Configura tu terminal (p. ej. `Option+Enter` para saltos de línea) | `/terminal-setup` | Recién instalado, si `Shift+Enter` no funciona |
| `/wellbeing` | `/breaks`, `/downtime` | Recordatorios de descanso y horas de silencio | `/wellbeing` | Sesiones maratonianas |
| `/privacy-settings` | — | Ver y actualizar tus ajustes de privacidad | `/privacy-settings` | Antes de trabajar con código sensible |
| `/update-config` 🧩 | — | Skill que **edita `settings.json` por ti**: hooks, permisos, variables de entorno | `/update-config cuando termines un turno, ejecuta npm run lint`<br>`/update-config permite todos los comandos bq` | Automatizaciones del tipo "cada vez que X, haz Y". Eso requiere un *hook*, y esta skill lo escribe correctamente |
| `/fewer-permission-prompts` 🧩 | — | Analiza tus transcripts y propone una allowlist priorizada en `.claude/settings.json` | `/fewer-permission-prompts` | Si apruebas permisos todo el día. Automatiza lo que harías a mano con `/permissions` |
| `/auto-mode-setup` 🔒 | — | Enseña al *auto mode* cómo es tu entorno y ajusta reglas | `/auto-mode-setup` | Solo si usas auto mode |

### 4.1 Eventos de hook disponibles

Útil al escribir hooks con `/update-config` o a mano:

```
PreToolUse        PostToolUse       UserPromptSubmit   Notification
Stop              SubagentStart     SubagentStop       TaskCompleted
SessionStart      SessionEnd        PreCompact         PostCompact
PermissionDenied  Elicitation       FileChanged
```

### 4.2 Modos de permiso

`default` · `acceptEdits` · `plan` · `bypassPermissions`

Se ciclan en el chat con `Shift+Tab`. `bypassPermissions` (`--dangerously-skip-permissions`) solo en sandbox sin red.

---

## 5. Proyecto, memoria y directorios

| Comando | Alias | Qué hace | Ejemplo | Cuándo usarlo |
|---|---|---|---|---|
| ⭐ `/init` 🧩 | — | Crea un `CLAUDE.md` documentando el codebase (y, según versión, skills/hooks opcionales) | `/init` | **Primer comando en un repo nuevo.** Evita re-explicar la arquitectura en cada sesión |
| `/memory` | — | Edita los `CLAUDE.md` y los ajustes de memoria | `/memory` | Añadir convenciones del proyecto ("usamos pnpm", "no toques `/legacy`") |
| `/pause-memory` | `/memory-pause`, `/toggle-memory` | Pausa la automemoria en esta sesión | `/pause-memory` | Trabajo exploratorio o desechable que no quieres que se recuerde |
| `/add-dir <ruta>` | — | Añade otro directorio de trabajo a la sesión | `/add-dir ../shared-types`<br>`/add-dir ~/Developments/api` | Monorepos o cambios que cruzan dos repos. Sin esto, Claude no puede leer fuera del cwd |
| `/cd <ruta>` | — | Mueve la sesión a otro directorio de trabajo | `/cd packages/web` | Cambiar de subproyecto conservando la conversación |
| `/insights` 🧩 | — | Informe analizando tus sesiones de Claude Code | `/insights` | Retro personal: en qué gastas tiempo y tokens |
| `/team-onboarding` 🧩 | — | Genera una guía de onboarding a partir de tu uso real | `/team-onboarding` | Cuando entra gente nueva al equipo |
| `/import [codex\|gemini] [--dry-run]` | — | Importa configuración de otro agente de código | `/import codex --dry-run`<br>`/import gemini` | Migras desde otra herramienta. **Usa siempre `--dry-run` primero** |

---

## 6. Skills, plugins, MCP y agentes

| Comando | Alias | Qué hace | Ejemplo | Cuándo usarlo |
|---|---|---|---|---|
| `/skills` | — | Lista las skills disponibles | `/skills` | Descubrir qué comandos-skill tienes activos ahora mismo |
| `/reload-skills` 🔒 | — | Recoge skills añadidas o modificadas en disco durante la sesión | `/reload-skills` | Estás escribiendo una skill y no quieres reiniciar |
| `/skill-doctor` | — | Muestra qué skills cargadas **no se usan y te están costando contexto** | `/skill-doctor` | `/context` dice que las skills ocupan mucho. Te dice cuáles apagar |
| `/plugin` | `/plugins`, `/marketplace` | Gestiona plugins (instalar, activar, marketplaces) | `/plugin` | Añadir capacidades: GitHub, Prisma, Context7, security-guidance… |
| `/reload-plugins [--force]` | — | Activa cambios de plugins pendientes en la sesión actual | `/reload-plugins` | Tras instalar un plugin, para no reiniciar |
| `/cloud-plugins` | — | Decide si las sesiones en la nube usan los plugins de esta máquina | `/cloud-plugins` | Antes de usar `/teleport` o `/schedule` |
| `/plugin-types [dir]` | — | Escribe `claude-code-mcp.d.ts` con los tipos de entrada de las tools MCP conectadas | `/plugin-types` | Desarrollas un plugin y quieres tipado real de las tools MCP |
| ⭐ `/mcp [reconnect\|enable\|disable [<servidor>\|all]]` | — | Gestiona servidores MCP | `/mcp`<br>`/mcp reconnect github`<br>`/mcp disable all` | Un servidor MCP falla, pide auth, o quieres apagar los que no usas para ahorrar contexto |
| `/list-agents` | `/peers` | Lista subagentes, compañeros y otras sesiones de Claude a las que puedes mandar mensajes | `/list-agents` | Antes de coordinar trabajo entre sesiones |
| `/agents` | — | **Retirado.** Pide a Claude que cree/gestione subagentes, o edita `.claude/agents/` | — | Usa lenguaje natural o edita los ficheros directamente |
| `/run-skill-generator` 🔒 🧩 | — | Asistente para generar una skill nueva | `/run-skill-generator` | Crear una skill bien estructurada sin partir de cero |

### 6.1 Los comandos `/` que aportan los servidores MCP

Esto casi nadie lo sabe: un servidor MCP puede exponer *prompts*, y Claude Code los registra **como comandos slash**:

```
/mcp__<servidor>__<prompt>
```

Y en servidores HTTP/SSE aceptan además la forma corta `<servidor>:<prompt>`.

En esta máquina hay conectados, entre otros: `claude-in-chrome`, `plugin_github_github`, `claude_ai_Atlassian_Rovo`, `claude_ai_Gmail`, `claude_ai_Google_Drive`, `claude_ai_Miro`. Escribe `/mcp__` y deja que el autocompletado te muestre lo que cada uno ofrece — no todos los servidores exponen prompts.

**Cuándo usarlos:** son los flujos que el equipo del servidor MCP ya ha empaquetado (crear un issue con la plantilla correcta, abrir un board, etc.). Suelen ser mejores que pedírselo en lenguaje natural, porque llevan los campos obligatorios ya resueltos.

> **Contexto y skills:** cada skill cargada consume contexto. El par `/context` → `/skill-doctor` → `/config` es la rutina para recuperarlo.

---

## 7. Background, nube y automatización ☁️

| Comando | Alias | Qué hace | Ejemplo | Cuándo usarlo |
|---|---|---|---|---|
| ⭐ `/tasks` | `/bashes` | Ve y gestiona **todo** lo que corre en background | `/tasks` | Comprobar procesos, subagentes, workflows y loops. Aquí también los detienes |
| `/background [prompt]` | `/bg` | Manda esta sesión al background y libera la terminal | `/background sigue con la migración y avísame` | Tarea larga que no necesita supervisión |
| `/workflows` | — | Explora workflows en curso y completados | `/workflows` | Seguir el progreso de una orquestación multiagente |
| `/loop <intervalo> <prompt o comando>` 🧩 | — | Repite un prompt o comando en un intervalo. **Sin intervalo, el modelo se autorregula** | `/loop 5m /tasks`<br>`/loop 10m comprueba si el deploy terminó`<br>`/loop vigila el PR y arregla lo que falle` | Vigilar CI, un deploy, una cola. No lo uses para tareas de una sola vez |
| `/loops [nombre]` | — | Lista, crea y borra loops | `/loops` | Ver qué loops tienes vivos y matarlos |
| `/schedule` 🧩 | `/routines` | Crea y gestiona **agentes en la nube con cron** (routines) | `/schedule cada lunes a las 9 revisa los PRs abiertos`<br>`/schedule mañana a las 15h recuérdame verificar el rollback` | Tareas recurrentes o de una sola vez programadas, que corren aunque tengas el portátil cerrado |
| `/daemon` | — | Gestiona servicios en background y routines | `/daemon` | Diagnosticar por qué una routine no se dispara |
| `/teleport` | `/tp` | Manda esta sesión a la nube, o recupera una de claude.ai | `/teleport` | Seguir en otro sitio, o soltar una tarea larga y cerrar el portátil |
| `/session` 🔒 | `/remote` | Muestra la URL y el QR de la sesión en la nube | `/session` | Abrir la sesión remota en el móvil |
| `/remote-control` | `/rc` | Controla esta sesión desde el móvil o claude.ai/code | `/remote-control` | Lanzas algo largo y quieres supervisarlo desde el teléfono |
| `/remote-env` 🔒 | — | Elige el entorno por defecto de los agentes de nube | `/remote-env` | Entornos self-hosted (`ccpool_...`) |
| `/autofix-pr` 🔒 | — | Vigila el PR actual y arregla lo que falle | `/autofix-pr` | CI rojo en un PR y no quieres estar mirando |
| `/workflow-launch-exec` 🔒 | — | Interno: ejecuta un handoff de workflow lanzado por el servidor | — | No lo invoques a mano |

### 7.1 `/loop` vs `/schedule` vs `/background`

| | Dónde corre | Sobrevive al cierre del terminal | Cadencia |
|---|---|---|---|
| `/background` | Tu máquina, en background | No | Una vez |
| `/loop` | Esta sesión | No | Cada N minutos, o autorregulada |
| `/schedule` | Nube | **Sí** | Cron |

---

## 8. Git, PRs y calidad de código

> Casi todos requieren estar **dentro de un repositorio git**. Si no aparecen, es por eso.

| Comando | Qué hace | Ejemplo | Cuándo usarlo |
|---|---|---|---|
| ⭐ `/commit [guía]` 🧩 | Prepara y crea un commit: recoge el contexto de git y aplica el estilo de mensaje, reglas de staging y atribución | `/commit`<br>`/commit separa el refactor del fix en dos commits` | Siempre que vayas a commitear. Recoge el diff completo y escribe mejor mensaje que a mano |
| `/pr` 🧩 | Commit + push + abre el pull request | `/pr` | Cerrar el trabajo de una rama de un tirón |
| ⭐ `/code-review [objetivo] [nivel] [--comment\|--fix]` 🧩 | Revisa el diff actual, un PR, una rama o una ruta, buscando **bugs** y limpiezas | `/code-review`<br>`/code-review high`<br>`/code-review 1423 --comment`<br>`/code-review --fix` | Antes de pedir revisión humana. `low`/`medium`: pocos hallazgos de alta confianza. `high`/`max`: cobertura amplia con hallazgos más inciertos. `--comment` los publica como comentarios inline en el PR; `--fix` los aplica al working tree |
| `/simplify` 🧩 | Limpia el código cambiado (reutilización, simplificación, eficiencia) **y aplica los arreglos**. No busca bugs | `/simplify` | Justo después de que algo funcione, antes del commit. Para bugs usa `/code-review` |
| `/security-review` 🧩 | Revisión de seguridad de los cambios pendientes de la rama | `/security-review` | Antes de mergear código que toca auth, entrada de usuario, secretos o dependencias |
| `/run` 🧩 | Arranca y conduce la app del proyecto para **ver el cambio funcionando** | `/run`<br>`/run abre la pantalla de login y hazme una captura` | Confirmar que algo funciona de verdad, no solo que los tests pasan |
| `/debug` 🔒 🧩 | Flujo guiado de depuración | `/debug el login falla solo en Safari` | Bug reproducible pero de causa desconocida |
| `/diff` | Panel de cambios sin commitear y diffs por turno | `/diff` | Revisar antes de commitear |

### 8.1 Orden recomendado antes de un PR

```
1. /diff             ¿qué cambió realmente?
2. /code-review      ¿hay bugs?
3. /simplify         ¿se puede dejar más limpio?
4. /security-review   ¿toca algo sensible?
5. /run              ¿funciona en la app real?
6. /commit  →  /pr
```

---

## 9. Cuenta, uso, versiones y diagnóstico

| Comando | Alias | Qué hace | Ejemplo | Cuándo usarlo |
|---|---|---|---|---|
| ⭐ `/doctor` | `/checkup` | Chequeo de salud y **arreglo** de tu setup: instalación, extensiones sin usar, `CLAUDE.md` duplicados o hinchados, hooks lentos, actualizaciones, permisos | `/doctor` | Primer comando ante cualquier rareza. También cada pocas semanas como mantenimiento |
| ⭐ `/status` | — | Estado: versión, modelo, cuenta, conectividad de API y estado de las tools | `/status` | "¿Estoy en el modelo que creo? ¿Está el MCP conectado?" |
| ⭐ `/usage` | `/cost`, `/stats` | Coste de la sesión, uso del plan y qué está consumiendo tus límites | `/usage` | Antes de lanzar algo caro, o cuando te acercas al límite |
| `/explain-usage` 🔒 🧩 | — | Explica en lenguaje natural por qué has gastado lo que has gastado | `/explain-usage` | El número de `/usage` te sorprende |
| `/usage-credits` 🔒 | — | Configura créditos de uso o pídelos a tu admin al llegar al límite | `/usage-credits` | Límite alcanzado y necesitas seguir |
| `/upgrade` 🔒 | — | Subir a Max: más límite y más Opus | `/upgrade` | Chocas con los límites a diario |
| `/rate-limit-options` 🔒 | — | Opciones al alcanzar el límite | — | Aparece solo automáticamente |
| `/passes` 🔒 | — | Comparte una semana gratis de Claude Code y gana créditos | `/passes` | Si eres elegible |
| `/login` | — | Inicia sesión o **cambia de cuenta** de Anthropic | `/login` | Alternar cuenta personal / de empresa |
| `/logout` | — | Cierra la sesión de tu cuenta | `/logout` | Máquina compartida |
| `/version` | — | Versión que **está corriendo esta sesión** (el autoupdate puede tener otra más nueva descargada) | `/version` | Reportar un bug con precisión |
| `/update` | `/restart` | Cambia a la última versión; **la conversación continúa** | `/update` | Hay versión nueva y quieres el fix ya |
| `/install` | — | Instala la build nativa de Claude Code | `/install` | Migrar de la instalación npm a la nativa |
| `/release-notes` | — | Notas de la versión | `/release-notes` | Tras un `/update`, para ver qué cambió |
| `/exit` | `/quit` | Sale del CLI. En sesión de background, se **desacopla** y ésta sigue corriendo | `/exit` | — |
| `/heapdump` 🔒 | — | Volcado del heap de JS a `~/Desktop` | `/heapdump` | Solo para reportar fugas de memoria a Anthropic |

---

## 10. Integraciones y setup

| Comando | Alias | Qué hace | Ejemplo | Cuándo usarlo |
|---|---|---|---|---|
| `/ide [open]` | — | Gestiona integraciones con IDE y muestra su estado | `/ide` | VS Code / JetBrains no se conecta |
| `/chrome` | — | Ajustes de Claude en Chrome | `/chrome` | Automatizar el navegador: hay que dar permisos por sitio en la extensión |
| `/claude-in-chrome` 🧩 | — | Skill que conduce Chrome: clics, formularios, capturas, consola, red | `/claude-in-chrome comprueba si el formulario de alta lanza errores en consola` | Depurar front-end en el navegador real, no en tests |
| `/desktop` | `/app` | Continúa la sesión en Claude Desktop | `/desktop` | Pasar de terminal a app de escritorio |
| `/mobile` | `/ios`, `/android` | QR para descargar la app móvil | `/mobile` | — |
| `/voice [hold\|tap\|off]` | — | Activa/desactiva el modo voz (pulsar para hablar con `Espacio`) | `/voice tap`<br>`/voice off` | Dictar prompts largos en lugar de teclearlos |
| `/web-setup` | — | Configura Claude Code en la web con tu cuenta de GitHub | `/web-setup` | Requisito para `/ultraplan`, `/ultrareview` y `/teleport` |
| `/install-github-app` | — | Configura Claude GitHub Actions en un repositorio | `/install-github-app` | Quieres que Claude revise PRs automáticamente en CI |
| `/install-slack-app` 🔒 | — | Instala la app de Claude para Slack | `/install-slack-app` | Invocar a Claude desde Slack |
| `/setup-bedrock` | — | Reconfigura autenticación, región o pins de modelo de Amazon Bedrock | `/setup-bedrock` | Empresa con Bedrock |
| `/setup-vertex` | — | Reconfigura autenticación, proyecto, región o pins de Google Vertex AI | `/setup-vertex` | Empresa con Vertex |
| `/setup-cowork` 🔒 🧩 | — | Configuración de trabajo colaborativo | `/setup-cowork` | — |
| `/claude-api` 🧩 | — | Referencia de la Claude API / SDK: IDs de modelo, precios, streaming, tool use, MCP, caching, tokens | `/claude-api ¿cuánto cuesta Opus 5 con prompt caching?` | **Antes de escribir cualquier código que llame a la API.** Los precios e IDs de memoria suelen estar desfasados |

---

## 11. Artifacts, diseño y visualización 🧩

Los *Artifacts* son páginas web privadas publicadas en claude.ai que puedes compartir. Estos comandos son skills.

| Comando | Qué hace | Ejemplo | Cuándo usarlo |
|---|---|---|---|
| `/artifacts` | Explora tus artifacts publicados y los compartidos contigo | `/artifacts` | Recuperar el enlace de algo publicado hace días |
| `/artifact-design` | Fundamentos de diseño para Artifacts | `/artifact-design` | Se carga sola antes de publicar; invócala si quieres las pautas |
| `/artifact-diagramming` | Cómo dibujar diagramas legibles (SVG inline, mermaid) en ambos temas | `/artifact-diagramming` | Un diagrama va a explicar el mecanismo mejor que el texto |
| `/artifact-capabilities` | Capacidades de *runtime*: leer datos vivos, recordar lo que hace la gente (encuestas, checklists), estado compartido, preguntar a Claude desde la página, ficheros | `/artifact-capabilities` | La página tiene que hacer algo más que ser HTML estático |
| `/artifact-components` 🔒 | Catálogo de componentes reutilizables | `/artifact-components` | — |
| `/plan-artifact` 🔒 | Publica un plan como Artifact | `/plan-artifact` | Un plan que va a leer más gente |
| `/prototype` 🔒 | Prototipa una idea como Artifact funcional | `/prototype un dashboard de métricas de la cola` | Validar una idea de UI sin montar el proyecto |
| `/whiteboard` 🔒 | Pizarra compartida: tú dibujas, Claude responde sobre ella | `/whiteboard` | Diseñar arquitectura en conversación |
| `/workshop` 🔒 | Documento de trabajo colaborativo como Artifact | `/workshop` | Documentos que se van editando entre varios |
| ⭐ `/dataviz` | Guía de diseño para **cualquier** gráfico, dashboard o visualización, en cualquier medio (HTML, SVG, matplotlib, Recharts, d3…) | `/dataviz` | **Antes de escribir la primera línea de código de un gráfico.** Paletas accesibles, elección de tipo de gráfico, ejes, leyendas, light/dark |
| `/design` | Crea un *design canvas*: diseño multi-artboard publicado como Artifact y editable visualmente | `/design una landing para el nuevo producto`<br>`/design mockups del flujo de onboarding` | Mockups, wireframes, landings, pósters, one-pagers: cualquier cosa que preferirías ajustar a mano y no en código |
| `/design-sync` 🔒 | Sincroniza con tu sistema de diseño | `/design-sync` | Que los artifacts respeten los tokens de tu marca |
| `/design-login` | Autoriza el acceso al sistema de diseño con tu cuenta claude.ai | `/design-login` | Requisito de `/design-sync` |
| `/design consent` / `/design revoke` 🔒 | Concede o revoca el acceso del agente a tus proyectos de Design | `/design revoke` | Retirar permisos |
| `/batch` 🔒 | Procesamiento por lotes | `/batch` | — |

---

## 12. Ayuda y varios

| Comando | Qué hace | Ejemplo | Cuándo usarlo |
|---|---|---|---|
| ⭐ `/help [open]` | Ayuda y **lista real de comandos disponibles ahora** | `/help` | La fuente de verdad de tu instalación. Esta guía es el mapa; `/help` es el territorio |
| `/powerup [nombre]` | Lecciones interactivas cortas para descubrir funciones | `/powerup` | **Muy recomendable si esta guía te resulta abrumadora.** Aprendes de a poco |
| `/feedback [reporte]` | Manda feedback a Anthropic o reporta un bug | `/feedback el autocompletado de rutas falla con espacios` | Algo debería funcionar mejor |
| `/bug [reporte]` | Reporta un bug o comparte tu conversación | `/bug` | Adjunta el contexto de la sesión automáticamente |
| `/radio` | Radio lo-fi de Claude FM | `/radio` | — |
| `/stickers` | Pide pegatinas de Claude Code | `/stickers` | — |

---

## 13. Sintaxis que no empieza por `/`

Esto es lo que probablemente te faltaba junto con los comandos:

| Sintaxis | Qué hace | Ejemplo |
|---|---|---|
| `#` al inicio | Guarda una **memoria** de proyecto (va a `CLAUDE.md`) | `# siempre usamos pnpm, nunca npm` |
| `!` al inicio | Ejecuta un comando de shell **tú mismo** y su salida entra en la conversación | `! gcloud auth login`<br>`! git log --oneline -10` |
| `@` al inicio de una palabra | Autocompleta y adjunta una ruta de archivo o directorio | `revisa @src/auth/session.ts` |
| `/` al inicio | Comando o skill | `/compact` |
| `ultrathink` en el prompt | Sube el presupuesto de razonamiento de ese turno | `ultrathink por qué este deadlock solo aparece en producción` |
| `+500k` en el prompt | Fija un **techo de tokens** para el turno (los workflows escalan a ese presupuesto) | `+500k audita todo el paquete de pagos` |
| `ultracode` en el prompt | Activa orquestación multiagente para esa petición | `ultracode migra todos los tests a vitest` |
| Pegar una imagen | `Ctrl+V` (`Alt+V` en Windows/WSL) | capturas de errores, mockups |

> **`!` es la vía cuando Claude no puede:** logins interactivos (`gcloud auth login`, `docker login`), comandos que piden contraseña, o cualquier cosa que necesite tu TTY.

---

## 14. Atajos de teclado (valores por defecto)

En macOS `meta` = `Option`/`Alt`.

### Globales
| Atajo | Acción |
|---|---|
| `Ctrl+C` | Interrumpir |
| `Ctrl+D` | Salir |
| `Ctrl+O` | Mostrar/ocultar el transcript completo |
| `Ctrl+T` | Mostrar/ocultar los todos |
| `Ctrl+R` | Buscar en el historial |
| `Ctrl+]` | Abrir el último artifact de la sesión |
| `Ctrl+↑` / `Ctrl+↓` | Navegar la lista de archivos del diff |

### En el chat
| Atajo | Acción |
|---|---|
| `Shift+Tab` | **Ciclar modo de permisos** (incluye plan mode) |
| `Esc` | Cancelar el turno actual |
| `Ctrl+L` | Limpiar el input |
| `Cmd+K` | Limpiar la pantalla |
| `Enter` | Enviar |
| `Ctrl+J` | Salto de línea |
| `Ctrl+X Enter` | Encolar el mensaje (se envía cuando termine el turno) |
| `↑` / `↓` | Historial de prompts |
| `Ctrl+G` o `Ctrl+X Ctrl+E` | Abrir editor externo |
| `Ctrl+S` | Stash del prompt |
| `Ctrl+_` / `Ctrl+-` | Deshacer en el input |
| `Alt+P` | Selector de modelo |
| `Alt+O` | Modo rápido (fast) |
| `Alt+T` | Alternar thinking |
| `Alt+W` | Alternar la palabra clave de workflow (ultracode) |
| `Ctrl+X Ctrl+K` | **Matar todos los agentes** |
| `Ctrl+Shift+B` | Alternar modo brief |
| `Ctrl+V` (`Alt+V` en Win) | Pegar imagen |

### En una tarea / transcript
| Atajo | Acción |
|---|---|
| `Ctrl+B` | Mandar la tarea a background |
| En transcript: `j`/`k`, `g`/`Shift+G`, `Ctrl+U`/`Ctrl+D`, `q` | Navegar y salir |

Todo esto se rebindea en `~/.claude/keybindings.json` (`/keybindings`).

---

## 15. Crear tus propios comandos `/`

Un comando propio es un archivo Markdown. La ruta determina el nombre y el alcance:

```
.claude/commands/deploy.md          →  /deploy        (solo este proyecto, versionable en git)
~/.claude/commands/revisar.md       →  /revisar       (todas tus sesiones)
.claude/commands/db/migrar.md       →  /db:migrar     (los subdirectorios crean namespaces)
```

En este proyecto no hay ninguno todavía (`.claude/commands/` no existe).

### Ejemplo completo

`.claude/commands/revisar-pr.md`:

```markdown
---
description: Revisa un PR contra nuestras convenciones internas
argument-hint: <número-de-pr>
allowed-tools: Bash(gh pr *), Bash(git diff *), Read, Grep
model: opus
effort: high
when_to_use: Cuando haya que revisar un PR ajeno antes de aprobarlo
disable-model-invocation: false
---

Revisa el PR #$ARGUMENTS.

Contexto del repositorio:
- Convenciones: @CONTRIBUTING.md
- Diff actual: !`gh pr diff $ARGUMENTS`

Comprueba, en este orden:
1. ¿Hay tests para el comportamiento nuevo?
2. ¿Se respetan las convenciones de @CONTRIBUTING.md?
3. ¿Hay algún cambio que rompa la API pública?

Devuelve los hallazgos ordenados de más grave a menos, con `archivo:línea`.
```

Uso: `/revisar-pr 1423`

### Sustituciones disponibles en el cuerpo

| Sintaxis | Qué inserta |
|---|---|
| `$ARGUMENTS` | Todo lo que el usuario escribió tras el comando |
| `$1`, `$2`, … | Argumentos posicionales |
| `@ruta/archivo` | El contenido del archivo |
| <code>!`comando`</code> | La salida de ese comando de shell, ejecutada al invocar |
| `${CLAUDE_PROJECT_DIR}` | Raíz del proyecto |
| `${CLAUDE_SKILL_DIR}` | Directorio de la skill (solo en skills) |

### Frontmatter soportado

| Clave | Para qué sirve |
|---|---|
| `name` | Nombre visible. Por defecto, el del archivo |
| `description` | Resumen de una línea que se ve en el listado y en la tool Skill |
| `model` | `haiku`, `sonnet`, `opus`, `fable`, un ID completo, o `inherit` |
| `effort` | `low`, `medium`, `high`, `max`, o un entero |
| `allowed-tools` | Tools disponibles mientras el archivo está activo (string separado por comas o lista YAML) |
| `disallowed-tools` | Tools retiradas mientras está activo |
| `argument-hint` | Texto de ayuda que se muestra tras el nombre del comando |
| `when_to_use` | Guía para que **el modelo** sepa cuándo invocarla; pasa a formar parte de la descripción de la tool |
| `disable-model-invocation` | `true` → solo tú puedes invocarlo, el modelo no |
| `user-invocable` | `false` → lo oculta como comando; solo el modelo puede usarlo |
| `context` | `fork` → se ejecuta con una copia del contexto |
| `agent` | Tipo de subagente que lo ejecuta |
| `background` | Se ejecuta en background |
| `paths` | Lo limita a ciertas rutas del proyecto |
| `hooks` | Hooks propios del comando |
| `shell` | `bash` o `powershell` para los bloques `!` |

Tras crear o editar un archivo, `/reload-skills` lo recoge sin reiniciar.

### Cuándo merece la pena

Crea un comando propio cuando escribas **el mismo prompt por tercera vez**. Casos típicos: el ritual de deploy, la checklist de revisión del equipo, generar un módulo con vuestra estructura, o traducir un ticket de Jira a un plan.

---

## 16. Apéndice: flags del CLI (`claude --help`)

Los más útiles en el día a día:

```bash
claude                                   # sesión interactiva
claude "arregla el test que falla"       # arranca con un prompt
claude -c                                # continúa la conversación más reciente aquí
claude -p "lista los TODO"               # no interactivo (imprime y sale)
claude --model opus                      # fija el modelo
claude --effort high                     # fija el esfuerzo
claude --add-dir ../shared ../types      # directorios extra accesibles
claude --agent reviewer                  # arranca con un agente concreto
claude --bg "corre la suite completa"    # agente en background (gestión: claude agents)
claude --cloud "migra el módulo X"       # sesión en la nube
claude --allowed-tools "Bash(git *)" Edit
claude --autocompact 400k
claude -d api,hooks                      # debug filtrado por categoría
claude --debug-file ./claude-debug.log
claude --chrome                          # habilita Claude in Chrome
claude --import codex                    # importa config de otro agente
claude --bare                            # modo mínimo: sin hooks, LSP, memoria ni CLAUDE.md
claude --disable-slash-commands          # desactiva todas las skills
claude --dangerously-skip-permissions    # ⚠️ solo en sandbox sin red
```

Notas:
- `--bare` es el modo diagnóstico: si un problema desaparece con `--bare`, la causa es un hook, plugin, LSP o `CLAUDE.md`.
- `-p` es lo que usas en scripts y CI.
- Otros subcomandos: `claude doctor`, `claude agents`, `claude plugin`, `claude mcp`.

---

## 17. Rutinas recomendadas

**Repo nuevo**
```
/init  →  /permissions  →  /doctor
```

**Empezar una tarea no trivial**
```
/clear  →  /plan <descripción>  →  (aprobar)  →  trabajar  →  /diff
```

**Cerrar trabajo**
```
/code-review  →  /simplify  →  /run  →  /commit  →  /pr
```

**Cuando va lento o responde peor**
```
/context  →  /skill-doctor  →  /compact "qué conservar"   (o /clear)
```

**Cuando algo está roto en la herramienta**
```
/doctor  →  /status  →  /mcp reconnect  →  claude --bare (para aislar)
```

**Mantenimiento mensual**
```
/doctor  →  /insights  →  /skill-doctor  →  /usage
```

---

## 18. Índice alfabético

`/add-dir` · `/advisor` 🔒 · `/agents` (retirado) · `/artifact-capabilities` · `/artifact-components` 🔒 · `/artifact-design` · `/artifact-diagramming` · `/artifacts` · `/auto-mode-setup` 🔒 · `/autocompact` · `/autofix-pr` 🔒 · `/background` · `/batch` 🔒 · `/branch` · `/brief` 🔒 · `/btw` 🔒 · `/bug` · `/cd` · `/chrome` · `/claude-api` · `/claude-in-chrome` · `/clear` · `/cloud-plugins` · `/code-review` · `/color` · `/commit` · `/compact` · `/config` · `/context` · `/copy` · `/daemon` · `/dataviz` · `/debug` 🔒 · `/design` · `/design-consent` 🔒 · `/design-login` · `/design-revoke` 🔒 · `/design-sync` 🔒 · `/desktop` · `/diff` · `/doctor` · `/effort` · `/exit` · `/explain-usage` 🔒 · `/export` · `/extra-usage` (→ `/usage-credits`) · `/fast` · `/feedback` · `/fewer-permission-prompts` · `/focus` · `/fork` · `/goal` · `/heapdump` 🔒 · `/help` · `/hooks` · `/ide` · `/import` · `/init` · `/insights` · `/install` · `/install-github-app` · `/install-slack-app` 🔒 · `/keybindings` · `/keybindings-help` · `/list-agents` · `/login` · `/logout` · `/loop` · `/loops` · `/mcp` · `/memory` · `/mobile` · `/model` · `/passes` 🔒 · `/pause-memory` · `/permissions` · `/plan` · `/plan-artifact` 🔒 · `/plugin` · `/plugin-types` · `/powerup` · `/privacy-settings` · `/pr` · `/pro-trial-expired` 🔒 · `/prototype` 🔒 · `/radio` · `/rate-limit-options` 🔒 · `/recap` · `/release-notes` · `/reload-plugins` · `/reload-skills` 🔒 · `/remote-control` · `/remote-env` 🔒 · `/rename` · `/resume` · `/rewind` · `/run` · `/run-skill-generator` 🔒 · `/sandbox` 🔒 · `/schedule` · `/scroll-speed` · `/security-review` · `/session` 🔒 · `/setup-bedrock` · `/setup-cowork` 🔒 · `/setup-vertex` · `/simplify` · `/skill-doctor` · `/skills` · `/statusline` · `/status` · `/stickers` · `/stop` 🔒 · `/subtask` · `/tasks` · `/team-onboarding` · `/teleport` · `/terminal-setup` · `/theme` · `/tui` · `/ultraplan` 🔒 · `/ultrareview` 🔒 · `/update` · `/update-config` · `/upgrade` 🔒 · `/usage` · `/usage-credits` 🔒 · `/version` · `/voice` · `/web-setup` · `/wellbeing` · `/whiteboard` 🔒 · `/workflow-launch-exec` 🔒 · `/workflows` · `/workshop` 🔒

**Alias:** `/allowed-tools`→`/permissions` · `/android`→`/mobile` · `/app`→`/desktop` · `/bashes`→`/tasks` · `/bg`→`/background` · `/break-reminder`, `/breaks`, `/downtime`→`/wellbeing` · `/checkup`→`/doctor` · `/checkpoint`, `/undo`→`/rewind` · `/continue`→`/resume` · `/cost`, `/stats`→`/usage` · `/ios`→`/mobile` · `/marketplace`, `/plugins`→`/plugin` · `/memory-pause`, `/toggle-memory`→`/pause-memory` · `/name`→`/rename` · `/new`, `/reset`→`/clear` · `/peers`→`/list-agents` · `/quit`→`/exit` · `/rc`→`/remote-control` · `/remote`→`/session` · `/restart`→`/update` · `/routines`→`/schedule` · `/settings`→`/config` · `/share`→`/bug` · `/tp`→`/teleport`

**Movidos a `/config`:** `/vim` (editor mode) y `/output-style`.

---

*Generado a partir del binario de Claude Code 2.1.247 instalado en esta máquina. Si actualizas la versión, la lista puede cambiar: `/help` es siempre la fuente de verdad de lo que tienes disponible.*
