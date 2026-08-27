# Comandos slash de Claude Code

Referencia completa de los comandos `/` de [Claude Code](https://claude.com/claude-code), extraída
directamente del binario instalado y no de la documentación pública. **132 comandos** con qué hace
cada uno, cómo se escribe, un ejemplo real y cuándo conviene usarlo.

**→ [Ver la referencia](https://oa2p-solutions.github.io/claude-code-cheatsheet/)**

## Por qué existe

El [cheatsheet oficial](https://support.claude.com/en/articles/14553413-claude-code-cheatsheet) no
lista todos los comandos y no incluye ejemplos. Esta referencia sale de parsear las definiciones de
comando del propio binario (`type`, `name`, `description`, `argumentHint`, `aliases`, `isHidden`),
así que incluye los comandos que `/help` te oculta y explica **por qué** los oculta.

Un comando puede existir y no aparecer en tu autocompletado por varias razones: no estás en un
repositorio git, tu plan no lo incluye, falta la integración, está detrás de un feature flag, o solo
aplica en sesiones remotas. La referencia marca cada caso.

## Contenido

| Archivo | Qué es |
|---|---|
| `index.html` | La referencia navegable, con buscador en vivo y filtros por tipo. Autónoma: sin dependencias ni build |
| `CHEATSHEET.md` | La misma referencia en Markdown, para leer en el terminal o en el editor |
| `logo-oa2p.svg` | Logotipo OA2P Solutions, origen del SVG incrustado en la página |

Además de los comandos, cubre la sintaxis que no empieza por `/` (`#` memoria, `!` shell, `@`
archivos, `ultrathink`, `+500k`, `ultracode`), los atajos de teclado por defecto, cómo crear
comandos propios con su frontmatter completo, los eventos de hook disponibles y los flags del CLI.

## Uso

La página es un único archivo HTML sin dependencias. Ábrela directamente:

```bash
open index.html
```

O sírvela en local:

```bash
python3 -m http.server 8000
# http://localhost:8000
```

Atajos dentro de la página: `/` salta al buscador, `Esc` limpia la búsqueda.

## Versión de referencia

Claude Code **2.1.247** sobre macOS arm64. Al actualizar Claude Code la lista puede cambiar:
`/help` es siempre la fuente de verdad de lo que tienes disponible en tu instalación.

## Diseño

Sigue el sistema gráfico de [OA2P Solutions](https://oa2p.com): azul OA2P `#0a1f44` con su escala de
tintes, grafito `#3d4451` / `#8a9099`, tipografía Montserrat y Geist Mono, y la retícula técnica de
56 px del sitio corporativo. El logotipo se incrusta con `currentColor`, de modo que solo aparece en
las dos versiones autorizadas por el manual de marca: color sobre fondo claro y blanco sobre fondo
oscuro.

La página respeta el tema del sistema (claro y oscuro) y `prefers-reduced-motion`.

## Licencia

Contenido documental sobre una herramienta de terceros, publicado como referencia interna de OA2P
Solutions. Claude y Claude Code son marcas de Anthropic.
